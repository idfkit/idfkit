"""Batch simulation execution with thread-pool parallelism.

Runs multiple EnergyPlus simulations concurrently using a
:class:`~concurrent.futures.ThreadPoolExecutor`.  Thread-based parallelism
is appropriate because :func:`simulate` delegates to ``subprocess.run``
which releases the GIL.
"""

from __future__ import annotations

import os
import time
from collections.abc import Callable, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from ..exceptions import SimulationError
from .progress import SimulationProgress
from .progress_bars import resolve_on_progress
from .result import SimulationResult
from .runner import simulate

if TYPE_CHECKING:
    from .cache import SimulationCache
    from .config import EnergyPlusConfig
    from .fs import FileSystem


@dataclass(frozen=True, slots=True)
class SimulationJob:
    """Specification for a single simulation within a batch.

    Attributes:
        model: The EnergyPlus model to simulate.
        weather: Path to the weather file.
        label: Human-readable label for progress reporting.
        output_dir: Directory for output files (default: auto temp dir).
        expand_objects: Run ExpandObjects before simulation.
        annual: Run annual simulation.
        design_day: Run design-day-only simulation.
        output_prefix: Prefix for output files.
        output_suffix: Output file naming suffix (``"C"``, ``"L"``, or ``"D"``).
        readvars: Run ReadVarsESO after simulation.
        timeout: Maximum runtime in seconds.
        extra_args: Additional command-line arguments.
    """

    model: object  # IDFDocument — use object to avoid import at class level
    weather: str | Path
    label: str = ""
    output_dir: str | Path | None = None
    expand_objects: bool = True
    annual: bool = False
    design_day: bool = False
    output_prefix: str = "eplus"
    output_suffix: Literal["C", "L", "D"] = "C"
    readvars: bool = False
    timeout: float = 3600.0
    extra_args: tuple[str, ...] | None = None


@dataclass(frozen=True, slots=True)
class BatchResult:
    """Aggregated results from a batch simulation run.

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

    def __getitem__(self, index: int) -> SimulationResult:
        return self.results[index]


def simulate_batch(
    jobs: Sequence[SimulationJob],
    *,
    energyplus: EnergyPlusConfig | None = None,
    max_workers: int | None = None,
    cache: SimulationCache | None = None,
    progress: Callable[..., None] | None = None,
    fs: FileSystem | None = None,
    on_progress: Callable[[SimulationProgress], None] | None = None,
) -> BatchResult:
    """Run multiple EnergyPlus simulations in parallel.

    Uses :class:`~concurrent.futures.ThreadPoolExecutor` to dispatch
    simulations concurrently.  Individual job failures are captured as
    failed :class:`SimulationResult` entries -- the batch never raises
    due to a single job failing.

    Args:
        jobs: Sequence of simulation jobs to execute.
        energyplus: Shared EnergyPlus configuration (auto-discovered if
            ``None``).
        max_workers: Maximum number of concurrent simulations.  Defaults
            to ``min(len(jobs), os.cpu_count() or 1)``.
        cache: Optional simulation cache for content-hash lookups.
        progress: Optional callback invoked after each job completes.
            Called as ``progress(completed=N, total=M, label=label,
            success=bool)``.
        fs: Optional file system backend passed through to each
            :func:`simulate` call.
        on_progress: Optional callback invoked with
            :class:`~idfkit.simulation.progress.SimulationProgress` events
            during each individual simulation.  Events include
            ``job_index`` and ``job_label`` to identify which batch job
            they belong to.  The ``"tqdm"`` shorthand is not supported
            for batch runners; use
            :func:`~idfkit.simulation.progress_bars.tqdm_progress`
            with a custom per-job callback instead.

    Returns:
        A :class:`BatchResult` with results in the same order as *jobs*.

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
        if max_workers is None:
            max_workers = min(len(jobs), os.cpu_count() or 1)

        results: list[SimulationResult | None] = [None] * len(jobs)
        completed_count = 0
        total = len(jobs)

        start = time.monotonic()

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_index = {
                executor.submit(_run_job, idx, job, energyplus, cache, fs, progress_cb): idx
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
    finally:
        if progress_cleanup is not None:
            progress_cleanup()

    elapsed = time.monotonic() - start

    # All slots filled — assert for type checker
    final: list[SimulationResult] = []
    for r in results:
        assert r is not None  # noqa: S101
        final.append(r)

    return BatchResult(results=tuple(final), total_runtime_seconds=elapsed)


def _run_job(
    idx: int,
    job: SimulationJob,
    energyplus: EnergyPlusConfig | None,
    cache: SimulationCache | None,
    fs: FileSystem | None,
    on_progress: Callable[[SimulationProgress], None] | None,
) -> SimulationResult:
    """Execute a single simulation job, catching SimulationError."""
    # Wrap the user callback to inject batch job context
    job_cb: Callable[[SimulationProgress], None] | None = None
    if on_progress is not None:
        job_cb = _make_job_progress_callback(on_progress, idx, job.label)

    try:
        return simulate(
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
        # Use the job's output_dir if specified, otherwise indicate failure with None-ish path
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
