"""Async batch simulation with semaphore-based concurrency control.

Non-blocking counterpart to :func:`~idfkit.simulation.batch.simulate_batch`
that uses :mod:`asyncio` for concurrency instead of
:class:`~concurrent.futures.ThreadPoolExecutor`.

Two entry points are provided:

* :func:`async_simulate_batch` — runs all jobs and returns an aggregated
  :class:`~idfkit.simulation.batch.BatchResult`, mirroring the sync API.
* :func:`async_simulate_batch_stream` — an async generator that yields
  :class:`SimulationEvent` objects as each simulation completes, enabling
  real-time progress monitoring without callbacks.

Example::

    import asyncio
    from idfkit.simulation import async_simulate_batch, SimulationJob

    async def main():
        jobs = [SimulationJob(model=m, weather="weather.epw", label=f"run-{i}") for i, m in enumerate(models)]
        batch = await async_simulate_batch(jobs, max_concurrent=4)
        print(f"{len(batch.succeeded)}/{len(batch)} succeeded")

    asyncio.run(main())

Streaming example::

    from idfkit.simulation import async_simulate_batch_stream

    async def main():
        jobs = [...]
        async for event in async_simulate_batch_stream(jobs, max_concurrent=4):
            status = "OK" if event.result.success else "FAIL"
            print(f"[{event.completed}/{event.total}] {event.label}: {status}")
"""

from __future__ import annotations

import asyncio
import os
import time
from collections.abc import AsyncIterator, Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from ..exceptions import SimulationError
from .async_runner import async_simulate
from .batch import BatchResult, SimulationJob
from .progress import SimulationProgress
from .progress_bars import resolve_on_progress
from .result import SimulationResult

if TYPE_CHECKING:
    from .cache import SimulationCache
    from .config import EnergyPlusConfig
    from .fs import FileSystem


@dataclass(frozen=True, slots=True)
class SimulationEvent:
    """Progress event emitted by :func:`async_simulate_batch_stream`.

    Each event represents a single simulation that has finished (successfully
    or not).  Events are yielded in *completion order*, not submission order.

    Attributes:
        index: Zero-based position of this job in the original *jobs* sequence.
        label: Human-readable label from the :class:`SimulationJob`.
        result: The simulation result.
        completed: Number of jobs completed so far (including this one).
        total: Total number of jobs in the batch.
    """

    index: int
    label: str
    result: SimulationResult
    completed: int
    total: int


async def async_simulate_batch(
    jobs: Sequence[SimulationJob],
    *,
    energyplus: EnergyPlusConfig | None = None,
    max_concurrent: int | None = None,
    cache: SimulationCache | None = None,
    fs: FileSystem | None = None,
    on_progress: Callable[[SimulationProgress], Any] | None = None,
) -> BatchResult:
    """Run multiple EnergyPlus simulations concurrently using asyncio.

    This is the async counterpart to
    :func:`~idfkit.simulation.batch.simulate_batch`.  Concurrency is
    controlled with an :class:`asyncio.Semaphore` instead of a thread pool.

    Individual job failures are captured as failed
    :class:`~idfkit.simulation.result.SimulationResult` entries -- the batch
    never raises due to a single job failing.

    Args:
        jobs: Sequence of simulation jobs to execute.
        energyplus: Shared EnergyPlus configuration (auto-discovered if
            ``None``).
        max_concurrent: Maximum number of concurrent simulations.  Defaults
            to ``min(len(jobs), os.cpu_count() or 1)``.
        cache: Optional simulation cache for content-hash lookups.
        fs: Optional file system backend passed through to each
            :func:`~idfkit.simulation.async_runner.async_simulate` call.
        on_progress: Optional callback invoked with
            :class:`~idfkit.simulation.progress.SimulationProgress` events
            during each individual simulation.  Events include
            ``job_index`` and ``job_label`` to identify which batch job
            they belong to.  Both sync and async callables are accepted.
            The ``"tqdm"`` shorthand is not supported for batch runners;
            use :func:`~idfkit.simulation.progress_bars.tqdm_progress`
            with a custom per-job callback instead.

    Returns:
        A :class:`~idfkit.simulation.batch.BatchResult` with results in the
        same order as *jobs*.

    Raises:
        ValueError: If *jobs* is empty.
    """
    if not jobs:
        msg = "jobs must not be empty"
        raise ValueError(msg)

    if on_progress == "tqdm":
        msg = (
            'on_progress="tqdm" is not supported for batch simulations because a single '
            "progress bar cannot represent multiple concurrent jobs. Use the tqdm_progress() "
            "context manager with a custom callback instead."
        )
        raise ValueError(msg)

    progress_cb, progress_cleanup = resolve_on_progress(on_progress)

    try:
        if max_concurrent is None:
            max_concurrent = min(len(jobs), os.cpu_count() or 1)

        semaphore = asyncio.Semaphore(max_concurrent)
        results: list[SimulationResult | None] = [None] * len(jobs)
        start = time.monotonic()

        async def _run_one(idx: int, job: SimulationJob) -> None:
            async with semaphore:
                results[idx] = await _async_run_job(idx, job, energyplus, cache, fs, progress_cb)

        tasks = [asyncio.create_task(_run_one(i, job)) for i, job in enumerate(jobs)]
        await asyncio.gather(*tasks)
    finally:
        if progress_cleanup is not None:
            progress_cleanup()

    elapsed = time.monotonic() - start

    final: list[SimulationResult] = []
    for r in results:
        assert r is not None  # noqa: S101
        final.append(r)

    return BatchResult(results=tuple(final), total_runtime_seconds=elapsed)


async def async_simulate_batch_stream(
    jobs: Sequence[SimulationJob],
    *,
    energyplus: EnergyPlusConfig | None = None,
    max_concurrent: int | None = None,
    cache: SimulationCache | None = None,
    fs: FileSystem | None = None,
    on_progress: Callable[[SimulationProgress], Any] | None = None,
) -> AsyncIterator[SimulationEvent]:
    """Run simulations concurrently, yielding events as each one completes.

    This is an async generator variant of :func:`async_simulate_batch` that
    yields :class:`SimulationEvent` objects in *completion order*.  This
    enables real-time progress reporting without needing a callback:

    .. code-block:: python

        async for event in async_simulate_batch_stream(jobs, max_concurrent=4):
            print(f"[{event.completed}/{event.total}] {event.label}")

    Args:
        jobs: Sequence of simulation jobs to execute.
        energyplus: Shared EnergyPlus configuration (auto-discovered if
            ``None``).
        max_concurrent: Maximum number of concurrent simulations.  Defaults
            to ``min(len(jobs), os.cpu_count() or 1)``.
        cache: Optional simulation cache for content-hash lookups.
        fs: Optional file system backend.
        on_progress: Optional callback invoked with
            :class:`~idfkit.simulation.progress.SimulationProgress` events
            during each individual simulation.  Events include
            ``job_index`` and ``job_label``.  The ``"tqdm"`` shorthand
            is not supported for batch runners; use
            :func:`~idfkit.simulation.progress_bars.tqdm_progress`
            with a custom per-job callback instead.

    Yields:
        :class:`SimulationEvent` for each completed simulation, in the order
        they finish.

    Raises:
        ValueError: If *jobs* is empty.
    """
    if not jobs:
        msg = "jobs must not be empty"
        raise ValueError(msg)

    if on_progress == "tqdm":
        msg = (
            'on_progress="tqdm" is not supported for batch simulations because a single '
            "progress bar cannot represent multiple concurrent jobs. Use the tqdm_progress() "
            "context manager with a custom callback instead."
        )
        raise ValueError(msg)

    progress_cb, progress_cleanup = resolve_on_progress(on_progress)

    if max_concurrent is None:
        max_concurrent = min(len(jobs), os.cpu_count() or 1)

    semaphore = asyncio.Semaphore(max_concurrent)
    total = len(jobs)
    queue: asyncio.Queue[SimulationEvent] = asyncio.Queue()
    completed_count = 0

    async def _run_one(idx: int, job: SimulationJob) -> None:
        nonlocal completed_count
        async with semaphore:
            result = await _async_run_job(idx, job, energyplus, cache, fs, progress_cb)
        completed_count += 1
        await queue.put(
            SimulationEvent(
                index=idx,
                label=job.label,
                result=result,
                completed=completed_count,
                total=total,
            )
        )

    tasks = [asyncio.create_task(_run_one(i, job)) for i, job in enumerate(jobs)]

    try:
        for _ in range(total):
            event = await queue.get()
            yield event
    finally:
        if progress_cleanup is not None:
            progress_cleanup()
        # If the consumer breaks out early, cancel remaining tasks.
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


async def _async_run_job(
    idx: int,
    job: SimulationJob,
    energyplus: EnergyPlusConfig | None,
    cache: SimulationCache | None,
    fs: FileSystem | None,
    on_progress: Callable[[SimulationProgress], Any] | None,
) -> SimulationResult:
    """Execute a single simulation job, catching SimulationError."""
    # Wrap the user callback to inject batch job context
    job_cb: Callable[[SimulationProgress], Any] | None = None
    if on_progress is not None:
        job_cb = _make_async_job_progress_callback(on_progress, idx, job.label)

    try:
        return await async_simulate(
            model=job.model,  # type: ignore[arg-type]
            weather=job.weather,
            output_dir=job.output_dir,
            energyplus=energyplus,
            expand_objects=job.expand_objects,
            annual=job.annual,
            design_day=job.design_day,
            output_prefix=job.output_prefix,
            output_suffix=job.output_suffix,
            readvars=job.readvars,
            timeout=job.timeout,
            extra_args=list(job.extra_args) if job.extra_args else None,
            cache=cache,
            fs=fs,
            on_progress=job_cb,
        )
    except SimulationError as exc:
        failed_run_dir = Path(job.output_dir) if job.output_dir is not None else Path("/dev/null")
        return SimulationResult(
            run_dir=failed_run_dir,
            success=False,
            exit_code=exc.exit_code,
            stdout="",
            stderr=exc.stderr or "",
            runtime_seconds=0.0,
            output_prefix=job.output_prefix,
        )


def _make_async_job_progress_callback(
    user_cb: Callable[[SimulationProgress], Any],
    job_index: int,
    job_label: str,
) -> Callable[[SimulationProgress], Any]:
    """Create a wrapper that stamps each event with batch job context.

    Preserves the sync/async nature of the user callback.
    """
    import inspect

    is_async = inspect.iscoroutinefunction(user_cb)

    if is_async:

        async def _async_wrapper(event: SimulationProgress) -> None:
            stamped = SimulationProgress(
                phase=event.phase,
                message=event.message,
                percent=event.percent,
                environment=event.environment,
                warmup_day=event.warmup_day,
                sim_day=event.sim_day,
                sim_total_days=event.sim_total_days,
                job_index=job_index,
                job_label=job_label,
            )
            await user_cb(stamped)

        return _async_wrapper

    def _wrapper(event: SimulationProgress) -> None:
        stamped = SimulationProgress(
            phase=event.phase,
            message=event.message,
            percent=event.percent,
            environment=event.environment,
            warmup_day=event.warmup_day,
            sim_day=event.sim_day,
            sim_total_days=event.sim_total_days,
            job_index=job_index,
            job_label=job_label,
        )
        user_cb(stamped)

    return _wrapper
