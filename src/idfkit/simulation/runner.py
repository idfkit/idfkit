"""EnergyPlus simulation runner.

Executes EnergyPlus as a subprocess and returns structured results.
"""

from __future__ import annotations

import logging
import subprocess
import tempfile
import threading
import time
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, overload

from ..exceptions import SimulationError
from ._cancel import run_process, tracked
from ._common import (
    admit_annual,
    admit_design_day,
    admit_environments,
    admit_model,
    admit_weather,
    build_command,
    ensure_sql_output,
    maybe_preprocess,
    prepare_run_directory,
    publish_exclude,
    resolve_config,
    resolve_version_mismatch,
    restore_cached_result,
    upload_results,
)
from .cache import runner_cache_key
from .progress import ProgressParser, SimulationProgress, environment_days
from .progress_bars import resolve_on_progress
from .result import SimulationResult

if TYPE_CHECKING:
    from ..document import AnyIDFDocument
    from .cache import SimulationCache
    from .fs import FileSystem

logger = logging.getLogger(__name__)


@overload
def simulate(
    model: AnyIDFDocument,
    weather: str | Path | None,
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
    preprocessor_timeout: float | None = None,
    extra_args: list[str] | None = None,
    cache: SimulationCache | None = None,
    fs: FileSystem | None = None,
    on_progress: Callable[[SimulationProgress], Any] | Literal["tqdm"] | None = None,
    auto_migrate: bool = False,
) -> SimulationResult: ...


@overload
def simulate(
    model: AnyIDFDocument,
    weather: None = None,
    *,
    output_dir: str | Path | None = None,
    energyplus: EnergyPlusConfig | None = None,
    expand_objects: bool = True,
    annual: Literal[False] = False,
    design_day: Literal[True],
    output_prefix: str = "eplus",
    output_suffix: Literal["C", "L", "D"] = "C",
    readvars: bool = False,
    timeout: float = 3600.0,
    preprocessor_timeout: float | None = None,
    extra_args: list[str] | None = None,
    cache: SimulationCache | None = None,
    fs: FileSystem | None = None,
    on_progress: Callable[[SimulationProgress], Any] | Literal["tqdm"] | None = None,
    auto_migrate: bool = False,
) -> SimulationResult: ...


def simulate(
    model: AnyIDFDocument,
    weather: str | Path | None = None,
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
    preprocessor_timeout: float | None = None,
    extra_args: list[str] | None = None,
    cache: SimulationCache | None = None,
    fs: FileSystem | None = None,
    on_progress: Callable[[SimulationProgress], Any] | Literal["tqdm"] | None = None,
    auto_migrate: bool = False,
) -> SimulationResult:
    """Run an EnergyPlus simulation.

    Creates an isolated run directory, writes the model, and executes
    EnergyPlus as a subprocess. The caller's model is not mutated.

    When *expand_objects* is ``True`` (the default) and the model contains
    ``GroundHeatTransfer:Slab:*`` or ``GroundHeatTransfer:Basement:*``
    objects, the Slab and/or Basement ground heat-transfer preprocessors
    are run automatically before simulation.  This is equivalent to
    calling [run_slab_preprocessor][idfkit.simulation.expand.run_slab_preprocessor] or
    [run_basement_preprocessor][idfkit.simulation.expand.run_basement_preprocessor]
    individually, but happens transparently.

    Args:
        model: The EnergyPlus model to simulate.
        weather: Path to the weather file (.epw), or ``None`` to run without
            a weather file. ``None`` is accepted only for a design-day-only
            run (``design_day=True`` and ``annual=False``). A model that
            contains ``GroundHeatTransfer:Slab:*`` or
            ``GroundHeatTransfer:Basement:*`` objects requires a weather
            file when *expand_objects* is ``True`` and
            ``GroundHeatTransfer:Control`` sets the matching
            ``run_slab_preprocessor`` or ``run_basement_preprocessor`` field
            to ``Yes``, because the Slab and Basement preprocessors read it. Without a weather file,
            a model that contains ``SizingPeriod:WeatherFileDays`` or
            ``SizingPeriod:WeatherFileConditionType`` fails in EnergyPlus and
            the result has ``success=False``; a model whose
            ``Site:WaterMainsTemperature`` uses ``CorrelationFromWeatherFile``
            completes with one severe error and a fixed mains temperature of
            10 °C.
        output_dir: Directory for output files (default: auto temp dir).
        energyplus: Pre-configured EnergyPlus installation. If None,
            uses [find_energyplus][idfkit.simulation.config.find_energyplus] for auto-discovery.
        expand_objects: Run ExpandObjects before simulation.  When
            ``True``, also runs the Slab and Basement ground heat-transfer
            preprocessors if the model contains the corresponding objects.
        annual: Run annual simulation (``-a`` flag). The model needs a
            ``RunPeriod``; without one the run is refused (see Raises).
        design_day: Run design-day-only simulation (``-D`` flag). With
            neither flag, ``SimulationControl`` decides: by default, the
            model's sizing periods and then its ``RunPeriod`` objects, so the
            model needs at least one of them (see Raises).
        output_prefix: Prefix for output files (default "eplus").
        output_suffix: EnergyPlus ``--output-suffix`` style, which names the
            output files: ``"C"`` (capital, default) gives ``eplus.err`` and
            ``eplusTable.htm``, ``"L"`` (legacy) gives ``eplusout.err`` and
            ``eplustbl.htm``, and ``"D"`` (dash) gives ``eplus.err`` and
            ``eplus-table.htm``.
        readvars: Run ReadVarsESO after simulation (``-r`` flag).
        timeout: Maximum runtime in seconds (default 3600).  Applied only
            to the main EnergyPlus subprocess; preprocessor stages
            (ExpandObjects, Slab, Basement) have an independent budget — see
            *preprocessor_timeout*.
        preprocessor_timeout: Per-subprocess timeout (seconds) applied
            individually to ExpandObjects, Slab, and Basement when they
            run automatically.  ``None`` (the default) consults the
            ``IDFKIT_PREPROCESSOR_TIMEOUT`` environment variable, falling
            back to 120 s.  Independent of *timeout* — there is no shared
            wall-clock cap across the pipeline.
        extra_args: Additional command-line arguments.
        cache: Optional simulation cache for content-hash lookups.  The key
            covers the contents of every file the model names (a
            ``Schedule:File`` CSV staged into *output_dir*, for example).  A
            model with a ``PythonPlugin:Instance`` or a co-simulation
            ``ExternalInterface`` is never cached; a warning is logged.
            A hit is copied into *output_dir* like a fresh run; without one,
            its ``run_dir`` is the read-only cache entry. Either way the
            result has ``cached=True``.
        fs: Optional file system backend for storing results on remote
            storage (e.g., S3). When provided, ``output_dir`` is required
            and specifies the remote destination path. EnergyPlus runs
            locally in a temp directory; its outputs (not the copy of the
            weather file) are then uploaded to ``output_dir`` via *fs*, and
            the temp directory is deleted, also when the run raises.  Combined
            with *cache*, a miss is cached from the local run directory and a
            hit uploads the cached outputs to ``output_dir``, so the remote
            folder exists either way.

            !!! note
                The ``fs`` parameter handles **output storage only**.
                The ``weather`` file must be a local path — remote weather
                files are not automatically downloaded. For cloud workflows,
                download weather files first using [WeatherDownloader][idfkit.weather.WeatherDownloader]
                or pre-stage them locally before calling ``simulate()``.
        on_progress: Optional callback invoked with a
            [SimulationProgress][idfkit.simulation.progress.SimulationProgress] event
            each time EnergyPlus emits a progress line (warmup iterations,
            simulation day changes, post-processing steps, etc.).  Pass
            ``"tqdm"`` to use a built-in tqdm progress bar (requires
            ``pip install idfkit[progress]``).
        auto_migrate: When ``True`` and ``model.version`` differs from the
            installed EnergyPlus version, forward-migrate the model before
            running the simulation. The resulting [MigrationReport][idfkit.migration.report.MigrationReport]
            is attached to the returned [SimulationResult.migration_report][idfkit.simulation.result.SimulationResult.migration_report].
            Backward migration (installed EP older than the model) is never
            attempted and always raises [VersionMismatchError][idfkit.exceptions.VersionMismatchError].

    Returns:
        SimulationResult with paths to output files.

    Raises:
        SimulationError: On timeout or OS error, or when the weather argument
            is refused before EnergyPlus starts: *weather* is an empty
            string; *weather* names a file that does not exist; *weather* is
            ``None`` and the run is not design-day-only; *weather* is
            ``None``, *expand_objects* is ``True`` and the model contains
            Slab or Basement ground heat-transfer objects whose preprocessor
            ``GroundHeatTransfer:Control`` enables; or *weather* is
            ``None`` and the run directory already contains ``in.epw``. Also
            raised before EnergyPlus starts when *annual* is ``True`` and the
            model has no ``RunPeriod``, when *design_day* is ``True`` and
            the model has no ``SizingPeriod:DesignDay``, or when neither is
            set and ``SimulationControl`` leaves EnergyPlus nothing to run:
            no ``RunPeriod`` and no ``SizingPeriod:*`` (as a fresh
            ``new_document()`` has), or both turned off.
        TypeError: If *model* is not a document (``None``, or a path).
        ExpandObjectsError: If a preprocessing step (ExpandObjects, Slab,
            or Basement) fails during automatic preprocessing.
        EnergyPlusNotFoundError: If EnergyPlus cannot be found.
        VersionMismatchError: If ``model.version`` names another release line
            than the installed EnergyPlus (a ``9.0`` model on 9.0.1 matches) and
            *auto_migrate* is ``False`` — or if the
            model is newer than the installed EnergyPlus (backward migration
            is not supported).
    """
    options: dict[str, Any] = {
        "energyplus": energyplus,
        "expand_objects": expand_objects,
        "annual": annual,
        "design_day": design_day,
        "output_prefix": output_prefix,
        "output_suffix": output_suffix,
        "readvars": readvars,
        "timeout": timeout,
        "preprocessor_timeout": preprocessor_timeout,
        "extra_args": extra_args,
        "cache": cache,
        "on_progress": on_progress,
        "auto_migrate": auto_migrate,
    }
    if fs is None:
        return _simulate_local(model, weather, output_dir=output_dir, **options)
    if output_dir is None:
        msg = "output_dir is required when using a file system backend"
        raise ValueError(msg)
    # EnergyPlus runs in a local scratch directory, which is uploaded to output_dir and then deleted.
    remote_dir = Path(str(output_dir))
    with tempfile.TemporaryDirectory(prefix="idfkit_sim_", ignore_cleanup_errors=True) as scratch:
        return _simulate_local(
            model,
            weather,
            output_dir=scratch,
            publish=lambda local, weather_path: _publish(local, remote_dir, fs, weather_path),
            **options,
        )


def _simulate_local(
    model: AnyIDFDocument,
    weather: str | Path | None,
    *,
    output_dir: str | Path | None,
    energyplus: EnergyPlusConfig | None,
    expand_objects: bool,
    annual: bool,
    design_day: bool,
    output_prefix: str,
    output_suffix: Literal["C", "L", "D"],
    readvars: bool,
    timeout: float,
    preprocessor_timeout: float | None,
    extra_args: list[str] | None,
    cache: SimulationCache | None,
    on_progress: Callable[[SimulationProgress], Any] | Literal["tqdm"] | None,
    auto_migrate: bool,
    publish: Callable[[SimulationResult, Path | None], SimulationResult] | None = None,
) -> SimulationResult:
    """Run EnergyPlus in the local *output_dir* (a new temp directory when ``None``); see `simulate`.

    With *publish*, the result (a cache hit as stored, uncopied) is passed to it
    with the resolved weather file, and what it returns is returned.
    """
    progress_cb, progress_cleanup = resolve_on_progress(on_progress)

    try:
        # Admission is a pure argument check, so it runs before EnergyPlus discovery.
        admit_model(model, "simulate")
        local_output_dir = output_dir
        weather_path = admit_weather(
            weather,
            model=model,
            design_day=design_day,
            annual=annual,
            expand_objects=expand_objects,
            run_dir=local_output_dir,
        )
        admit_annual(model, annual=annual)
        admit_design_day(model, design_day=design_day)
        admit_environments(model, annual=annual, design_day=design_day)
        config = resolve_config(energyplus)
        logger.debug("EnergyPlus: %s (version %d.%d.%d)", config.executable, *config.version)

        sim_input_model, migration_report = resolve_version_mismatch(
            model=model,
            config=config,
            auto_migrate=auto_migrate,
        )

        logger.info(
            "Starting simulation %s",
            "without a weather file" if weather_path is None else f"with weather {weather_path.name}",
        )

        # Copy the model first, so the cache key and the simulated model describe the same state even
        # if another thread edits the caller's model meanwhile (the async runner does the same).
        sim_model = sim_input_model.copy()

        cache_key = runner_cache_key(
            cache,
            sim_model,
            weather_path,
            output_dir=local_output_dir,
            config=config,
            expand_objects=expand_objects,
            annual=annual,
            design_day=design_day,
            output_suffix=output_suffix,
            readvars=readvars,
            extra_args=extra_args,
        )
        if cache is not None and cache_key is not None:
            cached = cache.get(cache_key)
            if cached is not None:
                logger.debug("Cache hit for key %s", cache_key.hex_digest[:12])
                cached.migration_report = migration_report
                if publish is not None:
                    return publish(cached, weather_path)  # uploaded straight from the cache entry
                # Copy the hit into output_dir, as a fresh run would fill it (no copy without one).
                return restore_cached_result(cached, local_output_dir, weather_path)
            logger.debug("Cache miss for key %s", cache_key.hex_digest[:12])

        ensure_sql_output(sim_model)

        # Auto-preprocess ground heat-transfer objects when needed.
        sim_model, ep_expand = maybe_preprocess(
            sim_model,
            config,
            weather_path,
            expand_objects,
            preprocessor_timeout=preprocessor_timeout,
        )

        run_dir = prepare_run_directory(local_output_dir, weather_path)
        idf_path = run_dir / "model.idf"

        from ..writers import save_idf

        save_idf(sim_model, idf_path)

        cmd = build_command(
            config=config,
            idf_path=idf_path,
            weather_path=None if weather_path is None else run_dir / weather_path.name,
            output_dir=run_dir,
            output_prefix=output_prefix,
            output_suffix=output_suffix,
            expand_objects=ep_expand,
            annual=annual,
            design_day=design_day,
            readvars=readvars,
            extra_args=extra_args,
        )
        logger.debug("Command: %s", " ".join(cmd))

        start = time.monotonic()

        if progress_cb is not None:
            parser = ProgressParser(environment_days(sim_model))
            stdout, stderr, returncode = _run_with_progress(cmd, run_dir, timeout, start, progress_cb, parser)
        else:
            stdout, stderr, returncode = _run_simple(cmd, run_dir, timeout, start)
    finally:
        if progress_cleanup is not None:
            progress_cleanup()

    elapsed = time.monotonic() - start

    if returncode != 0:
        logger.warning("Simulation exited with code %d in %.1fs", returncode, elapsed)
    else:
        logger.info("Simulation completed successfully in %.1fs", elapsed)

    result = SimulationResult(
        run_dir=run_dir,
        success=returncode == 0,
        exit_code=returncode,
        stdout=stdout,
        stderr=stderr,
        runtime_seconds=elapsed,
        output_prefix=output_prefix,
        migration_report=migration_report,
        output_suffix=output_suffix,
    )
    if cache is not None and cache_key is not None and result.success:
        cache.put(cache_key, result)
    if publish is not None:
        return publish(result, weather_path)
    return result


def _publish(local: SimulationResult, remote_dir: Path, fs: FileSystem, weather_path: Path | None) -> SimulationResult:
    """Upload a local result's outputs to *remote_dir* on *fs* and return a result that reads them there."""
    upload_results(local.run_dir, remote_dir, fs, exclude=publish_exclude(weather_path))
    return SimulationResult(
        run_dir=remote_dir,
        success=local.success,
        exit_code=local.exit_code,
        stdout=local.stdout,
        stderr=local.stderr,
        runtime_seconds=local.runtime_seconds,
        output_prefix=local.output_prefix,
        fs=fs,
        migration_report=local.migration_report,
        output_suffix=local.output_suffix,
        cached=local.cached,
    )


def _run_simple(
    cmd: list[str],
    run_dir: Path,
    timeout: float,
    start: float,
) -> tuple[str, str, int]:
    """Run EnergyPlus without progress tracking (original code path)."""
    try:
        proc = run_process(cmd, cwd=run_dir, timeout=timeout)
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
    parser: ProgressParser,
) -> tuple[str, str, int]:
    """Run EnergyPlus with line-by-line stdout streaming for progress callbacks."""
    try:
        proc = subprocess.Popen(  # noqa: S603
            cmd,
            stdin=subprocess.DEVNULL,
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

    try:
        with tracked(proc):
            timed_out = _stream_stdout(proc, stdout_lines, parser, on_progress, deadline=start + timeout)
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
    except BaseException:
        # KeyboardInterrupt and the like: do not leave EnergyPlus running behind them.
        proc.kill()
        proc.wait()
        raise
    finally:
        # Always join the stderr thread so it doesn't leak.
        stderr_thread.join(timeout=5.0)

    stderr = "".join(stderr_lines)

    if timed_out:
        msg = f"Simulation timed out after {timeout} seconds"
        raise SimulationError(msg, exit_code=None, stderr=stderr or None)

    # EnergyPlus reports "EnergyPlus Completed Successfully" on stderr.
    _emit_progress(parser, stderr_lines, on_progress)

    stdout = "".join(stdout_lines)
    returncode = proc.returncode if proc.returncode is not None else -1

    return stdout, stderr, returncode


def _stream_stdout(
    proc: subprocess.Popen[str],
    stdout_lines: list[str],
    parser: ProgressParser,
    on_progress: Callable[[SimulationProgress], Any],
    *,
    deadline: float,
) -> bool:
    """Collect *proc*'s stdout into *stdout_lines*, passing progress events on, until it exits.

    Returns ``True`` if *proc* was killed for running past *deadline* (a [time.monotonic][] value).
    """
    assert proc.stdout is not None  # noqa: S101
    for line in proc.stdout:
        stdout_lines.append(line)
        event = parser.parse_line(line)
        if event is not None:
            on_progress(event)
        if time.monotonic() > deadline:
            proc.kill()
            proc.wait()
            return True
    proc.wait()
    return False


def _emit_progress(parser: ProgressParser, lines: list[str], on_progress: Callable[[SimulationProgress], Any]) -> None:
    """Pass the progress events *parser* finds in stderr *lines* to *on_progress*.

    A callback error is wrapped in [SimulationError][idfkit.exceptions.SimulationError],
    as it is for a stdout event, whichever stream the line came from.
    """
    try:
        for line in lines:
            event = parser.parse_line(line)
            if event is not None:
                on_progress(event)
    except Exception as exc:
        stderr = "".join(lines)
        msg = f"Failed during EnergyPlus execution: {exc}"
        raise SimulationError(msg, exit_code=None, stderr=stderr or None) from exc


# Backward-compatible aliases for existing test imports.
from .config import EnergyPlusConfig  # noqa: E402

_build_command = build_command
_ensure_sql_output = ensure_sql_output
_prepare_run_directory = prepare_run_directory
