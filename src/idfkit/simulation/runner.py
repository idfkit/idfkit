"""EnergyPlus simulation runner.

Executes EnergyPlus as a subprocess and returns structured results.
"""

from __future__ import annotations

import subprocess
import threading
import time
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

from ..exceptions import SimulationError
from ._common import (
    build_command,
    ensure_sql_output,
    maybe_preprocess,
    prepare_run_directory,
    resolve_config,
    upload_results,
)
from .progress import ProgressParser, SimulationProgress
from .progress_bars import resolve_on_progress
from .result import SimulationResult

if TYPE_CHECKING:
    from ..document import IDFDocument
    from .cache import CacheKey, SimulationCache
    from .fs import FileSystem


def simulate(
    model: IDFDocument,
    weather: str | Path,
    *,
    output_dir: str | Path | None = None,
    energyplus: EnergyPlusConfig | None = None,
    expand_objects: bool = True,
    annual: bool = False,
    design_day: bool = False,
    output_prefix: str = "eplus",
    output_suffix: Literal["C", "L", "D"] = "C",
    readvars: bool = False,
    timeout: float = 3600.0,
    extra_args: list[str] | None = None,
    cache: SimulationCache | None = None,
    fs: FileSystem | None = None,
    on_progress: Callable[[SimulationProgress], Any] | Literal["tqdm"] | None = None,
) -> SimulationResult:
    """Run an EnergyPlus simulation.

    Creates an isolated run directory, writes the model, and executes
    EnergyPlus as a subprocess. The caller's model is not mutated.

    When *expand_objects* is ``True`` (the default) and the model contains
    ``GroundHeatTransfer:Slab:*`` or ``GroundHeatTransfer:Basement:*``
    objects, the Slab and/or Basement ground heat-transfer preprocessors
    are run automatically before simulation.  This is equivalent to
    calling :func:`~idfkit.simulation.expand.run_slab_preprocessor` or
    :func:`~idfkit.simulation.expand.run_basement_preprocessor`
    individually, but happens transparently.

    Args:
        model: The EnergyPlus model to simulate.
        weather: Path to the weather file (.epw).
        output_dir: Directory for output files (default: auto temp dir).
        energyplus: Pre-configured EnergyPlus installation. If None,
            uses :func:`find_energyplus` for auto-discovery.
        expand_objects: Run ExpandObjects before simulation.  When
            ``True``, also runs the Slab and Basement ground heat-transfer
            preprocessors if the model contains the corresponding objects.
        annual: Run annual simulation (``-a`` flag).
        design_day: Run design-day-only simulation (``-D`` flag).
        output_prefix: Prefix for output files (default "eplus").
        output_suffix: Output file naming suffix: ``"C"`` for combined table
            files (default), ``"L"`` for legacy separate table files, or
            ``"D"`` for timestamped separate files.
        readvars: Run ReadVarsESO after simulation (``-r`` flag).
        timeout: Maximum runtime in seconds (default 3600).
        extra_args: Additional command-line arguments.
        cache: Optional simulation cache for content-hash lookups.
        fs: Optional file system backend for storing results on remote
            storage (e.g., S3). When provided, ``output_dir`` is required
            and specifies the remote destination path. EnergyPlus runs
            locally in a temp directory; results are then uploaded to
            ``output_dir`` via *fs* after execution.

            .. note::

                The ``fs`` parameter handles **output storage only**.
                The ``weather`` file must be a local path — remote weather
                files are not automatically downloaded. For cloud workflows,
                download weather files first using :class:`~idfkit.weather.WeatherDownloader`
                or pre-stage them locally before calling ``simulate()``.
        on_progress: Optional callback invoked with a
            :class:`~idfkit.simulation.progress.SimulationProgress` event
            each time EnergyPlus emits a progress line (warmup iterations,
            simulation day changes, post-processing steps, etc.).  Pass
            ``"tqdm"`` to use a built-in tqdm progress bar (requires
            ``pip install idfkit[progress]``).

    Returns:
        SimulationResult with paths to output files.

    Raises:
        SimulationError: On timeout, OS error, or missing weather file.
        ExpandObjectsError: If a preprocessing step (ExpandObjects, Slab,
            or Basement) fails during automatic preprocessing.
        EnergyPlusNotFoundError: If EnergyPlus cannot be found.
    """
    if fs is not None and output_dir is None:
        msg = "output_dir is required when using a file system backend"
        raise ValueError(msg)

    progress_cb, progress_cleanup = resolve_on_progress(on_progress)

    try:
        config = resolve_config(energyplus)
        weather_path = Path(weather).resolve()

        if not weather_path.is_file():
            msg = f"Weather file not found: {weather_path}"
            raise SimulationError(msg)

        cache_key: CacheKey | None = None
        if cache is not None:
            cache_key = cache.compute_key(
                model,
                weather_path,
                expand_objects=expand_objects,
                annual=annual,
                design_day=design_day,
                output_suffix=output_suffix,
                extra_args=extra_args,
            )
            cached = cache.get(cache_key)
            if cached is not None:
                return cached

        # Copy model to avoid mutation
        sim_model = model.copy()
        ensure_sql_output(sim_model)

        # Auto-preprocess ground heat-transfer objects when needed.
        sim_model, ep_expand = maybe_preprocess(model, sim_model, config, weather_path, expand_objects)

        # When using a remote fs, always run locally in a temp dir
        local_output_dir = None if fs is not None else output_dir
        run_dir = prepare_run_directory(local_output_dir, weather_path)
        idf_path = run_dir / "in.idf"

        from ..writers import write_idf

        write_idf(sim_model, idf_path)

        cmd = build_command(
            config=config,
            idf_path=idf_path,
            weather_path=run_dir / weather_path.name,
            output_dir=run_dir,
            output_prefix=output_prefix,
            output_suffix=output_suffix,
            expand_objects=ep_expand,
            annual=annual,
            design_day=design_day,
            readvars=readvars,
            extra_args=extra_args,
        )

        start = time.monotonic()

        if progress_cb is not None:
            stdout, stderr, returncode = _run_with_progress(cmd, run_dir, timeout, start, progress_cb)
        else:
            stdout, stderr, returncode = _run_simple(cmd, run_dir, timeout, start)
    finally:
        if progress_cleanup is not None:
            progress_cleanup()

    elapsed = time.monotonic() - start

    if fs is not None:
        remote_dir = Path(str(output_dir))
        upload_results(run_dir, remote_dir, fs)
        result = SimulationResult(
            run_dir=remote_dir,
            success=returncode == 0,
            exit_code=returncode,
            stdout=stdout,
            stderr=stderr,
            runtime_seconds=elapsed,
            output_prefix=output_prefix,
            fs=fs,
        )
    else:
        result = SimulationResult(
            run_dir=run_dir,
            success=returncode == 0,
            exit_code=returncode,
            stdout=stdout,
            stderr=stderr,
            runtime_seconds=elapsed,
            output_prefix=output_prefix,
        )
    if cache is not None and cache_key is not None and result.success:
        cache.put(cache_key, result)
    return result


def _run_simple(
    cmd: list[str],
    run_dir: Path,
    timeout: float,
    start: float,
) -> tuple[str, str, int]:
    """Run EnergyPlus without progress tracking (original code path)."""
    try:
        proc = subprocess.run(  # noqa: S603
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(run_dir),
        )
    except subprocess.TimeoutExpired as exc:
        msg = f"Simulation timed out after {timeout} seconds"
        raise SimulationError(
            msg,
            exit_code=None,
            stderr=str(exc.stderr) if exc.stderr else None,
        ) from exc
    except OSError as exc:
        msg = f"Failed to start EnergyPlus: {exc}"
        raise SimulationError(
            msg,
            exit_code=None,
            stderr=None,
        ) from exc

    return proc.stdout, proc.stderr, proc.returncode


def _run_with_progress(
    cmd: list[str],
    run_dir: Path,
    timeout: float,
    start: float,
    on_progress: Callable[[SimulationProgress], Any],
) -> tuple[str, str, int]:
    """Run EnergyPlus with line-by-line stdout streaming for progress callbacks."""
    try:
        proc = subprocess.Popen(  # noqa: S603
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(run_dir),
        )
    except OSError as exc:
        msg = f"Failed to start EnergyPlus: {exc}"
        raise SimulationError(
            msg,
            exit_code=None,
            stderr=None,
        ) from exc

    # Read stderr in a background thread to avoid deadlocks when both
    # stdout and stderr pipes fill up.
    stderr_lines: list[str] = []

    def _read_stderr() -> None:
        assert proc.stderr is not None  # noqa: S101
        for line in proc.stderr:
            stderr_lines.append(line)

    stderr_thread = threading.Thread(target=_read_stderr, daemon=True)
    stderr_thread.start()

    stdout_lines: list[str] = []
    parser = ProgressParser()
    timed_out = False

    try:
        assert proc.stdout is not None  # noqa: S101
        for line in proc.stdout:
            stdout_lines.append(line)
            event = parser.parse_line(line)
            if event is not None:
                on_progress(event)

            # Check timeout
            if time.monotonic() - start > timeout:
                proc.kill()
                proc.wait()
                timed_out = True
                break

        if not timed_out:
            proc.wait()
    except Exception as exc:
        proc.kill()
        proc.wait()
        stderr_thread.join(timeout=5.0)
        stderr = "".join(stderr_lines)
        msg = f"Failed during EnergyPlus execution: {exc}"
        raise SimulationError(
            msg,
            exit_code=None,
            stderr=stderr or None,
        ) from exc
    finally:
        # Always join the stderr thread so it doesn't leak.
        stderr_thread.join(timeout=5.0)

    stderr = "".join(stderr_lines)

    if timed_out:
        msg = f"Simulation timed out after {timeout} seconds"
        raise SimulationError(msg, exit_code=None, stderr=stderr or None)

    stdout = "".join(stdout_lines)
    returncode = proc.returncode if proc.returncode is not None else -1

    return stdout, stderr, returncode


# Backward-compatible aliases for existing test imports.
from .config import EnergyPlusConfig  # noqa: E402

_build_command = build_command
_ensure_sql_output = ensure_sql_output
_prepare_run_directory = prepare_run_directory
