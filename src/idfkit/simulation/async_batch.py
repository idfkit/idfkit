"""Async batch simulation with semaphore-based concurrency control.

Non-blocking counterpart to [simulate_batch][idfkit.simulation.batch.simulate_batch]
that uses [asyncio][] for concurrency instead of
[ThreadPoolExecutor][concurrent.futures.ThreadPoolExecutor].

Two entry points are provided:

* [async_simulate_batch][idfkit.simulation.async_batch.async_simulate_batch] — runs all jobs and returns an aggregated
  [BatchResult][idfkit.simulation.batch.BatchResult], mirroring the sync API.
* [async_simulate_batch_stream][idfkit.simulation.async_batch.async_simulate_batch_stream] — an async generator that yields
  [SimulationEvent][idfkit.simulation.async_batch.SimulationEvent] objects as each simulation completes, enabling
  real-time progress monitoring without callbacks.

Examples:
    ```python
    import asyncio
    from idfkit.simulation import async_simulate_batch, SimulationJob

    async def main():
        jobs = [SimulationJob(model=m, weather="weather.epw", label=f"run-{i}") for i, m in enumerate(models)]
        batch = await async_simulate_batch(jobs, max_concurrent=4)
        print(f"{len(batch.succeeded)}/{len(batch)} succeeded")

    asyncio.run(main())
    ```

Streaming example:

    ```python
    from idfkit.simulation import async_simulate_batch_stream

    async def main():
        jobs = [...]
        async for event in async_simulate_batch_stream(jobs, max_concurrent=4):
            status = "OK" if event.result.success else "FAIL"
            print(f"[{event.completed}/{event.total}] {event.label}: {status}")
    ```
"""

from __future__ import annotations

import asyncio
import logging
import os
import time
from collections.abc import AsyncGenerator, Awaitable, Callable, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from .async_runner import async_simulate
from .batch import (
    BatchResult,
    SimulationJob,
    cancelled_job_result,
    check_jobs_for_fs,
    err_snapshot,
    fail_fast_reason,
    failed_job_result,
)
from .progress import SimulationProgress
from .progress_bars import resolve_on_progress
from .result import SimulationResult

if TYPE_CHECKING:
    from .cache import SimulationCache
    from .config import EnergyPlusConfig
    from .fs import AsyncFileSystem, FileSystem

__all__ = [
    "SimulationEvent",
    "async_simulate_batch",
    "async_simulate_batch_stream",
]

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class SimulationEvent:
    """Progress event emitted by [async_simulate_batch_stream][idfkit.simulation.async_batch.async_simulate_batch_stream].

    Each event represents a single simulation that has finished (successfully
    or not).  Events are yielded in *completion order*, not submission order.

    Attributes:
        index: Zero-based position of this job in the original *jobs* sequence.
        label: Human-readable label from the [SimulationJob][idfkit.simulation.batch.SimulationJob].
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
    fs: FileSystem | AsyncFileSystem | None = None,
    on_progress: Callable[[SimulationProgress], Any] | None = None,
    fail_fast: bool = False,
) -> BatchResult:
    """Run multiple EnergyPlus simulations concurrently using asyncio.

    This is the async counterpart to
    [simulate_batch][idfkit.simulation.batch.simulate_batch].  Concurrency is
    controlled with an [asyncio.Semaphore][] instead of a thread pool.

    Individual job failures are captured as failed
    [SimulationResult][idfkit.simulation.result.SimulationResult] entries -- the batch
    never raises due to a single job failing, and by default every other job
    still runs. With ``fail_fast=True`` the first failed job cancels the jobs
    still queued or running (their EnergyPlus processes are killed) and the
    batch returns, reporting them in
    [BatchResult.cancelled][idfkit.simulation.batch.BatchResult.cancelled].

    Args:
        jobs: Sequence of simulation jobs to execute.
        energyplus: Shared EnergyPlus configuration (auto-discovered if
            ``None``).
        max_concurrent: Maximum number of concurrent simulations.  Defaults
            to ``min(len(jobs), os.cpu_count() or 1)``.
        cache: Optional simulation cache for content-hash lookups.  See
            [SimulationCache][idfkit.simulation.cache.SimulationCache] for what
            the key covers and which models are never cached.
        fs: Optional file system backend passed through to each
            [async_simulate][idfkit.simulation.async_runner.async_simulate] call.
        on_progress: Optional callback invoked with
            [SimulationProgress][idfkit.simulation.progress.SimulationProgress] events
            during each individual simulation.  Events include
            ``job_index`` and ``job_label`` to identify which batch job
            they belong to.  Both sync and async callables are accepted.
            The ``"tqdm"`` shorthand is not supported for batch runners;
            use [tqdm_progress][idfkit.simulation.progress_bars.tqdm_progress]
            with a custom per-job callback instead.
        fail_fast: Stop the batch at the first failed job, cancelling the jobs
            still queued or running, instead of running every job.

    Returns:
        A [BatchResult][idfkit.simulation.batch.BatchResult] with results in the
        same order as *jobs*.

    Raises:
        ValueError: If *jobs* is empty, or *fs* is given and a job has no
            ``output_dir``.
    """
    if not jobs:
        msg = "jobs must not be empty"
        raise ValueError(msg)
    check_jobs_for_fs(jobs, fs)

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

        logger.info("Starting async batch of %d jobs with concurrency %d", len(jobs), max_concurrent)

        semaphore = asyncio.Semaphore(max_concurrent)
        results: list[SimulationResult | None] = [None] * len(jobs)
        start = time.monotonic()
        stopper = _FailFast(enabled=fail_fast, semaphore=semaphore)

        async def _run_one(idx: int, job: SimulationJob) -> None:
            results[idx] = await stopper.run(
                idx, job, lambda: _async_run_job(idx, job, energyplus, cache, fs, progress_cb)
            )

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

    batch_result = BatchResult(results=tuple(final), total_runtime_seconds=elapsed)
    logger.info(
        "Async batch complete: %d succeeded, %d failed, %d cancelled in %.1fs",
        len(batch_result.succeeded),
        len(batch_result.failed),
        len(batch_result.cancelled),
        elapsed,
    )
    return batch_result


async def async_simulate_batch_stream(
    jobs: Sequence[SimulationJob],
    *,
    energyplus: EnergyPlusConfig | None = None,
    max_concurrent: int | None = None,
    cache: SimulationCache | None = None,
    fs: FileSystem | AsyncFileSystem | None = None,
    on_progress: Callable[[SimulationProgress], Any] | None = None,
    fail_fast: bool = False,
) -> AsyncGenerator[SimulationEvent, None]:
    """Run simulations concurrently, yielding events as each one completes.

    This is an async generator variant of [async_simulate_batch][idfkit.simulation.async_batch.async_simulate_batch] that
    yields [SimulationEvent][idfkit.simulation.async_batch.SimulationEvent] objects in *completion order*.  This
    enables real-time progress reporting without needing a callback:

    .. code-block:: python

        async for event in async_simulate_batch_stream(jobs, max_concurrent=4):
            print(f"[{event.completed}/{event.total}] {event.label}")

    Closing the generator cancels the jobs still queued or running and kills
    their EnergyPlus processes. Leaving an ``async for`` loop early closes it
    once the generator is garbage-collected; to close it at a known point,
    iterate inside ``contextlib.aclosing(async_simulate_batch_stream(...))``.

    With ``fail_fast=True`` the first failed job cancels the jobs still queued
    or running. The stream still yields one event per job: each cancelled job's
    event follows, with ``event.result.cancelled`` set.

    Args:
        jobs: Sequence of simulation jobs to execute.
        energyplus: Shared EnergyPlus configuration (auto-discovered if
            ``None``).
        max_concurrent: Maximum number of concurrent simulations.  Defaults
            to ``min(len(jobs), os.cpu_count() or 1)``.
        cache: Optional simulation cache for content-hash lookups.  See
            [SimulationCache][idfkit.simulation.cache.SimulationCache] for what
            the key covers and which models are never cached.
        fs: Optional file system backend.
        on_progress: Optional callback invoked with
            [SimulationProgress][idfkit.simulation.progress.SimulationProgress] events
            during each individual simulation.  Events include
            ``job_index`` and ``job_label``.  The ``"tqdm"`` shorthand
            is not supported for batch runners; use
            [tqdm_progress][idfkit.simulation.progress_bars.tqdm_progress]
            with a custom per-job callback instead.
        fail_fast: Stop the batch at the first failed job, cancelling the jobs
            still queued or running, instead of running every job.

    Yields:
        [SimulationEvent][idfkit.simulation.async_batch.SimulationEvent] for each completed simulation, in the order
        they finish.

    Raises:
        ValueError: If *jobs* is empty, or *fs* is given and a job has no
            ``output_dir``.
    """
    if not jobs:
        msg = "jobs must not be empty"
        raise ValueError(msg)
    check_jobs_for_fs(jobs, fs)

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
    stopper = _FailFast(enabled=fail_fast, semaphore=semaphore)

    async def _run_one(idx: int, job: SimulationJob) -> None:
        nonlocal completed_count
        result = await stopper.run(idx, job, lambda: _async_run_job(idx, job, energyplus, cache, fs, progress_cb))
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


class _FailFast:
    """Runs the jobs of one async batch, and with *enabled* stops the batch at the first failed job.

    The first failure cancels the other jobs' tasks; a task cancelled that way, queued or running,
    returns a cancelled result instead of raising, so the batch still has one result per job. Any
    other cancellation (the caller's) propagates as usual.
    """

    def __init__(self, *, enabled: bool, semaphore: asyncio.Semaphore) -> None:
        self.enabled = enabled
        self.semaphore = semaphore
        self.reason: str | None = None
        # Tasks currently inside run(). Only these are cancelled: cancelling a task that has not
        # started yet would cancel it before run() could turn the cancellation into a result.
        self._entered: set[asyncio.Task[Any]] = set()

    async def run(
        self, idx: int, job: SimulationJob, simulate: Callable[[], Awaitable[SimulationResult]]
    ) -> SimulationResult:
        """Run *job* (number *idx*) through *simulate* under the batch's concurrency limit."""
        if not self.enabled:
            async with self.semaphore:
                return await simulate()
        if self.reason is not None:
            return cancelled_job_result(job, self.reason, started=False)
        current = asyncio.current_task()
        if current is not None:
            self._entered.add(current)
        started = False
        try:
            async with self.semaphore:
                if self.reason is not None:
                    return cancelled_job_result(job, self.reason, started=False)
                started = True
                result = await simulate()
        except asyncio.CancelledError:
            if self.reason is None:
                raise  # not ours: the caller cancelled the batch
            return cancelled_job_result(job, self.reason, started=started)
        finally:
            if current is not None:
                self._entered.discard(current)
        if not result.success and self.reason is None:
            self.reason = fail_fast_reason(idx, job)
            # Tasks that have not entered run() yet see self.reason on entry and return a cancelled
            # result; only the ones suspended inside it need cancelling.
            stopping = [task for task in self._entered if task is not current and not task.done()]
            logger.info("Job %s failed; fail_fast cancels %d jobs", job.label or f"#{idx}", len(stopping))
            for task in stopping:
                task.cancel()
        return result


async def _async_run_job(
    idx: int,
    job: SimulationJob,
    energyplus: EnergyPlusConfig | None,
    cache: SimulationCache | None,
    fs: FileSystem | AsyncFileSystem | None,
    on_progress: Callable[[SimulationProgress], Any] | None,
) -> SimulationResult:
    """Execute a single simulation job, catching SimulationError."""
    # Wrap the user callback to inject batch job context
    job_cb: Callable[[SimulationProgress], Any] | None = None
    if on_progress is not None:
        job_cb = _make_async_job_progress_callback(on_progress, idx, job.label)

    before = err_snapshot(job, fs)
    try:
        return await async_simulate(
            model=job.model,
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
            preprocessor_timeout=job.preprocessor_timeout,
            extra_args=list(job.extra_args) if job.extra_args else None,
            cache=cache,
            fs=fs,
            on_progress=job_cb,
            auto_migrate=job.auto_migrate,
        )
    except Exception as exc:
        # Catch all exceptions (SimulationError, ExpandObjectsError,
        # EnergyPlusNotFoundError, etc.) so that a single job failure
        # never crashes the entire batch.
        return failed_job_result(job, exc, ran=err_snapshot(job, fs) != before)


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
