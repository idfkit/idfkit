"""Batch simulation execution with thread-pool parallelism.

Runs multiple EnergyPlus simulations concurrently using a
[ThreadPoolExecutor][concurrent.futures.ThreadPoolExecutor].  Thread-based parallelism
is appropriate because [simulate][idfkit.simulation.runner.simulate] waits on an EnergyPlus subprocess,
which releases the GIL.

If the caller is interrupted while a batch runs (Ctrl-C, or any other exception
raised in the waiting thread), queued jobs are cancelled and the EnergyPlus
processes already running are killed before the exception propagates.
"""

from __future__ import annotations

import inspect
import logging
import os
import time
from collections.abc import Callable, Iterator, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Protocol, overload

from ._cancel import ProcessGroup
from .progress import SimulationProgress
from .progress_bars import resolve_on_progress
from .result import REFUSED_RUN_DIR, SimulationResult
from .runner import simulate

if TYPE_CHECKING:
    from ..document import AnyIDFDocument
    from .cache import SimulationCache
    from .config import EnergyPlusConfig
    from .fs import FileSystem

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class SimulationJob:
    """Specification for a single simulation within a batch.

    Attributes:
        model: The EnergyPlus model to simulate.
        weather: Path to the weather file, or ``None`` to run without one.
            ``None`` is accepted only for a design-day-only job
            (``design_day=True`` and ``annual=False``); see
            [simulate][idfkit.simulation.runner.simulate] for the models that
            still require a weather file. A refused job is reported as a
            failed result whose ``refusal`` carries the reason.
        label: Human-readable label for progress reporting.
        output_dir: Directory for output files. ``None`` (the default) runs
            in a new temporary directory, deleted by
            [BatchResult.cleanup][idfkit.simulation.batch.BatchResult.cleanup].
        expand_objects: Run ExpandObjects before simulation.
        annual: Run annual simulation.
        design_day: Run design-day-only simulation.
        output_prefix: Prefix for output files.
        output_suffix: Output file naming suffix (``"C"``, ``"L"``, or ``"D"``).
        readvars: Run ReadVarsESO after simulation.
        timeout: Maximum runtime in seconds for the main EnergyPlus
            subprocess.
        preprocessor_timeout: Per-subprocess timeout (seconds) applied
            individually to ExpandObjects, Slab, and Basement when they
            run automatically.  ``None`` consults the
            ``IDFKIT_PREPROCESSOR_TIMEOUT`` environment variable, falling
            back to 120 s.
        extra_args: Additional command-line arguments. Any sequence of
            strings is accepted, as ``simulate(extra_args=...)`` takes, and
            stored as a tuple.
        auto_migrate: Forward-migrate a copy of the model to the installed
            EnergyPlus version before the run, as
            ``simulate(..., auto_migrate=True)`` does.

    Raises:
        TypeError: If *model* is a path rather than a loaded document (load it
            with [load_idf][idfkit.load_idf] first), or *extra_args* is a
            single string rather than a sequence of them.
    """

    model: AnyIDFDocument
    weather: str | Path | None = None
    label: str = ""
    output_dir: str | Path | None = None
    expand_objects: bool = True
    annual: bool = False
    design_day: bool = False
    output_prefix: str = "eplus"
    output_suffix: Literal["C", "L", "D"] = "C"
    readvars: bool = False
    timeout: float = 3600.0
    preprocessor_timeout: float | None = None
    extra_args: Sequence[str] | None = None
    auto_migrate: bool = False

    def __post_init__(self) -> None:
        model: object = self.model
        if isinstance(model, (str, os.PathLike)):
            msg = (
                f"SimulationJob(model=...) takes a loaded document, not the path {str(model)!r}; "
                "load it with load_idf() or load_epjson() first."
            )
            raise TypeError(msg)
        extra_args: object = self.extra_args
        if isinstance(extra_args, str):
            msg = f"extra_args takes a sequence of arguments, not the string {extra_args!r}; pass [{extra_args!r}]."
            raise TypeError(msg)
        if self.extra_args is not None and not isinstance(self.extra_args, tuple):
            # Frozen: store an immutable copy, so the job stays hashable and a caller's list edits do not leak in.
            object.__setattr__(self, "extra_args", tuple(self.extra_args))


class BatchProgressCallback(Protocol):
    """The ``progress=`` callback of [simulate_batch][idfkit.simulation.batch.simulate_batch].

    Called once per finished job, with keyword arguments only, so a callback
    must accept all four by name (``def progress(*, completed, total, label,
    success)``, or ``**kwargs``).
    """

    def __call__(self, *, completed: int, total: int, label: str, success: bool) -> None:
        """Report that *completed* of *total* jobs have finished, the last being *label*."""
        ...


@dataclass(frozen=True, slots=True)
class BatchResult(Sequence[SimulationResult]):
    """Aggregated results from a batch simulation run.

    A real [Sequence][collections.abc.Sequence] of the results, in job order, so
    ``for result in batch``, ``enumerate(batch)``, ``batch[0]``, ``len(batch)``,
    ``reversed(batch)`` and ``result in batch`` all work and all type-check.

    It behaved that way at runtime long before it type-checked. ``__len__`` and
    ``__getitem__`` alone make an object iterable through the legacy sequence
    protocol, so ``for result in batch`` ran fine and every static checker rejected
    it, which pushed seven documented examples into writing ``batch.results``
    instead. Documenting a workaround for a call that already worked is worse than
    either fixing it or removing it, so the base class is declared.

    Attributes:
        results: Simulation results in the same order as the input jobs.
        total_runtime_seconds: Wall-clock time for the entire batch.
    """

    results: tuple[SimulationResult, ...]
    total_runtime_seconds: float

    @property
    def succeeded(self) -> tuple[SimulationResult, ...]:
        """Results that completed successfully."""
        return tuple(r for r in self.results if r.success)

    @property
    def failed(self) -> tuple[SimulationResult, ...]:
        """Results that failed."""
        return tuple(r for r in self.results if not r.success)

    @property
    def all_succeeded(self) -> bool:
        """Whether every job in the batch succeeded."""
        return all(r.success for r in self.results)

    def __len__(self) -> int:
        return len(self.results)

    @overload
    def __getitem__(self, index: int) -> SimulationResult: ...

    @overload
    def __getitem__(self, index: slice) -> tuple[SimulationResult, ...]: ...

    def __getitem__(self, index: int | slice) -> SimulationResult | tuple[SimulationResult, ...]:
        return self.results[index]

    def __iter__(self) -> Iterator[SimulationResult]:
        # Sequence would synthesise this from __getitem__, one index at a time. Iterating the
        # underlying tuple directly is the same answer without the index arithmetic, and it is
        # the path every `for result in batch` actually takes.
        return iter(self.results)

    def cleanup(self) -> None:
        """Call [SimulationResult.cleanup][idfkit.simulation.result.SimulationResult.cleanup] on every result.

        Deletes the temporary run directories idfkit created for jobs without an
        ``output_dir``; a job's own ``output_dir`` is never touched. Using the
        batch as a context manager (``with simulate_batch(jobs) as batch:``)
        calls this on exit. Safe to call more than once.
        """
        for result in self.results:
            result.cleanup()

    async def async_cleanup(self) -> None:
        """Non-blocking [cleanup][idfkit.simulation.batch.BatchResult.cleanup]; ``async with`` calls it on exit."""
        for result in self.results:
            await result.async_cleanup()

    def __enter__(self) -> BatchResult:
        return self

    def __exit__(self, *exc: object) -> None:
        self.cleanup()

    async def __aenter__(self) -> BatchResult:
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.async_cleanup()


def simulate_batch(
    jobs: Sequence[SimulationJob],
    *,
    energyplus: EnergyPlusConfig | None = None,
    max_workers: int | None = None,
    cache: SimulationCache | None = None,
    progress: BatchProgressCallback | None = None,
    fs: FileSystem | None = None,
    on_progress: Callable[[SimulationProgress], None] | None = None,
) -> BatchResult:
    """Run multiple EnergyPlus simulations in parallel.

    Uses [ThreadPoolExecutor][concurrent.futures.ThreadPoolExecutor] to dispatch
    simulations concurrently.  Individual job failures are captured as
    failed [SimulationResult][idfkit.simulation.result.SimulationResult] entries -- the batch never raises
    due to a single job failing.

    An exception in the calling thread -- Ctrl-C, or one raised by a
    *progress* callback -- stops the batch: queued jobs never start, running
    EnergyPlus processes are killed, and the exception propagates once the
    workers have stopped. To abort on the first failed job, raise from
    *progress* when ``success`` is false.

    Args:
        jobs: Sequence of simulation jobs to execute.
        energyplus: Shared EnergyPlus configuration (auto-discovered if
            ``None``).
        max_workers: Maximum number of concurrent simulations.  Defaults
            to ``min(len(jobs), os.cpu_count() or 1)``.
        cache: Optional simulation cache for content-hash lookups.  See
            [SimulationCache][idfkit.simulation.cache.SimulationCache] for what
            the key covers and which models are never cached.
        progress: Optional callback invoked after each job completes.
            Called as ``progress(completed=N, total=M, label=label,
            success=bool)``; see
            [BatchProgressCallback][idfkit.simulation.batch.BatchProgressCallback].
            A callback that cannot take those keywords is refused before any
            job runs.
        fs: Optional file system backend passed through to each
            [simulate][idfkit.simulation.runner.simulate] call.
        on_progress: Optional callback invoked with
            [SimulationProgress][idfkit.simulation.progress.SimulationProgress] events
            during each individual simulation.  Events include
            ``job_index`` and ``job_label`` to identify which batch job
            they belong to.  The ``"tqdm"`` shorthand is not supported
            for batch runners; use
            [tqdm_progress][idfkit.simulation.progress_bars.tqdm_progress]
            with a custom per-job callback instead.

    Returns:
        A [BatchResult][idfkit.simulation.batch.BatchResult] with results in the same order as *jobs*.

    Raises:
        ValueError: If *jobs* is empty, or *fs* is given and a job has no
            ``output_dir``.
        TypeError: If *progress* cannot be called with the four keyword
            arguments above.
    """
    if not jobs:
        msg = "jobs must not be empty"
        raise ValueError(msg)
    check_jobs_for_fs(jobs, fs)
    if progress is not None:
        _check_progress_callback(progress)

    if on_progress == "tqdm":
        msg = (
            'on_progress="tqdm" is not supported for batch simulations because a single '
            "progress bar cannot represent multiple concurrent jobs. Use the tqdm_progress() "
            "context manager with a custom callback instead."
        )
        raise ValueError(msg)

    progress_cb, progress_cleanup = resolve_on_progress(on_progress)

    try:
        if max_workers is None:
            max_workers = min(len(jobs), os.cpu_count() or 1)

        logger.info("Starting batch of %d jobs with %d workers", len(jobs), max_workers)

        results: list[SimulationResult | None] = [None] * len(jobs)
        completed_count = 0
        total = len(jobs)

        start = time.monotonic()

        group = ProcessGroup()
        executor = ThreadPoolExecutor(max_workers=max_workers)
        try:
            future_to_index = {
                executor.submit(_run_job, idx, job, energyplus, cache, fs, progress_cb, group): idx
                for idx, job in enumerate(jobs)
            }

            for future in as_completed(future_to_index):
                idx = future_to_index[future]
                job = jobs[idx]
                result = future.result()  # _run_job never raises
                results[idx] = result
                completed_count += 1

                if progress is not None:
                    progress(
                        completed=completed_count,
                        total=total,
                        label=job.label,
                        success=result.success,
                    )
        except BaseException:
            # Interrupted (Ctrl-C, or a progress callback raised): start no queued job,
            # kill the EnergyPlus processes that are running, then wait for the workers.
            executor.shutdown(wait=False, cancel_futures=True)
            group.cancel()
            executor.shutdown(wait=True)
            raise
        executor.shutdown(wait=True)
    finally:
        if progress_cleanup is not None:
            progress_cleanup()

    elapsed = time.monotonic() - start

    # All slots filled — assert for type checker
    final: list[SimulationResult] = []
    for r in results:
        assert r is not None  # noqa: S101
        final.append(r)

    batch_result = BatchResult(results=tuple(final), total_runtime_seconds=elapsed)
    logger.info(
        "Batch complete: %d succeeded, %d failed in %.1fs",
        len(batch_result.succeeded),
        len(batch_result.failed),
        elapsed,
    )
    return batch_result


def _check_progress_callback(progress: BatchProgressCallback) -> None:
    """Refuse a *progress* callback that cannot take the keywords it will be called with.

    Checked up front: otherwise the mismatch surfaces only after the first job has run, as a
    ``TypeError`` that discards the results of every job in the batch.
    """
    try:
        signature = inspect.signature(progress)
    except (TypeError, ValueError):  # a builtin or C callable without a signature: nothing to check
        return
    try:
        signature.bind(completed=0, total=0, label="", success=True)
    except TypeError as exc:
        msg = (
            f"simulate_batch(progress=...) is called as progress(completed=, total=, label=, success=); "
            f"{getattr(progress, '__qualname__', repr(progress))}{signature} cannot take that ({exc})."
        )
        raise TypeError(msg) from exc


def _run_job(
    idx: int,
    job: SimulationJob,
    energyplus: EnergyPlusConfig | None,
    cache: SimulationCache | None,
    fs: FileSystem | None,
    on_progress: Callable[[SimulationProgress], None] | None,
    group: ProcessGroup,
) -> SimulationResult:
    """Execute a single simulation job, catching SimulationError.

    The subprocesses the job starts join *group*, so the batch can kill them when it is interrupted.
    """
    with group.bind():
        return _run_job_in_group(idx, job, energyplus, cache, fs, on_progress)


def _run_job_in_group(
    idx: int,
    job: SimulationJob,
    energyplus: EnergyPlusConfig | None,
    cache: SimulationCache | None,
    fs: FileSystem | None,
    on_progress: Callable[[SimulationProgress], None] | None,
) -> SimulationResult:
    # Wrap the user callback to inject batch job context
    job_cb: Callable[[SimulationProgress], None] | None = None
    if on_progress is not None:
        job_cb = _make_job_progress_callback(on_progress, idx, job.label)

    before = err_snapshot(job, fs)
    try:
        return simulate(
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


#: The ``.err`` files of a job's local ``output_dir``, by name, with what identifies each version of one.
ErrSnapshot = dict[str, tuple[int, int, int]]


def err_snapshot(job: SimulationJob, fs: object | None) -> ErrSnapshot | None:
    """The ``.err`` files in *job*'s local ``output_dir``, to tell whether EnergyPlus wrote one there.

    Taken before and after a job that raised: EnergyPlus writes its ``.err`` as soon as it starts, so
    a changed snapshot means the exception came after EnergyPlus ran in ``output_dir`` (a timeout, a
    crash), and its outputs are this run's. ``None`` when the job runs elsewhere: in a temporary
    directory (no ``output_dir``) or locally before an upload to *fs*.
    """
    if fs is not None or job.output_dir is None:
        return None
    snapshot: ErrSnapshot = {}
    try:
        for path in Path(job.output_dir).glob("*.err"):
            st = path.stat()
            snapshot[path.name] = (st.st_mtime_ns, st.st_ino, st.st_size)
    except OSError:
        return None
    return snapshot


def _exception_reason(exc: Exception) -> str:
    """The message of *exc* without the exit code and stderr tail a SimulationError appends to it."""
    reason = str(exc)
    stderr = getattr(exc, "stderr", None)
    if isinstance(stderr, str) and stderr:
        tail = f"\nstderr: {stderr.strip()[:500]}"
        if reason.endswith(tail):
            reason = reason[: -len(tail)]
    exit_code = getattr(exc, "exit_code", None)
    if isinstance(exit_code, int):
        head, sep, rest = reason.partition("\n")
        marker = f" (exit code {exit_code})"
        if head.endswith(marker):
            reason = head[: -len(marker)] + sep + rest
    return reason or type(exc).__name__


def failed_job_result(job: SimulationJob, exc: Exception, *, ran: bool = False) -> SimulationResult:
    """Build the failed result for a job whose simulation raised *exc*.

    Args:
        job: The job that failed.
        exc: What ``simulate`` raised for it.
        ran: Whether EnergyPlus had already written its outputs to the job's ``output_dir``
            (a timeout or a crash mid-run). Such a result reads those outputs like any failed
            run; otherwise the job was refused and its result carries ``refusal``.
    """
    stderr = getattr(exc, "stderr", None)
    return SimulationResult(
        run_dir=Path(job.output_dir) if job.output_dir is not None else REFUSED_RUN_DIR,
        success=False,
        exit_code=getattr(exc, "exit_code", None),
        stdout="",
        stderr=stderr if isinstance(stderr, str) and stderr else str(exc),
        runtime_seconds=0.0,
        output_prefix=job.output_prefix,
        refusal=None if ran and job.output_dir is not None else _exception_reason(exc),
    )


def check_jobs_for_fs(jobs: Sequence[SimulationJob], fs: object | None) -> None:
    """Refuse a batch whose file system backend has no ``output_dir`` to write to.

    Checked before any job runs: ``simulate`` would refuse each such job the
    same way, turning one configuration error into a failed result per job.

    Raises:
        ValueError: If *fs* is given and a job has no ``output_dir``.
    """
    if fs is None:
        return
    missing = [job.label or f"#{i}" for i, job in enumerate(jobs) if job.output_dir is None]
    if missing:
        shown = ", ".join(missing[:5]) + (f" and {len(missing) - 5} more" if len(missing) > 5 else "")
        msg = f"output_dir is required on every job when using a file system backend; missing on: {shown}"
        raise ValueError(msg)


def _make_job_progress_callback(
    user_cb: Callable[[SimulationProgress], None],
    job_index: int,
    job_label: str,
) -> Callable[[SimulationProgress], None]:
    """Create a wrapper that stamps each event with batch job context."""

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
