"""Async EnergyPlus simulation runner.

Non-blocking counterpart to [simulate][idfkit.simulation.runner.simulate] that
uses [asyncio][] subprocess management instead of [subprocess.run][].

The preparation steps (model copy, directory setup, cache lookup) are
synchronous and fast; only the EnergyPlus subprocess execution is truly
async.  Preprocessing (ExpandObjects, Slab, Basement) is delegated to
a thread via [asyncio.to_thread][] because those routines use
[subprocess.run][] internally.

Examples:
    ```python
    import asyncio
    from idfkit import load_idf
    from idfkit.simulation import async_simulate

    async def main():
        model = load_idf("building.idf")
        result = await async_simulate(model, "weather.epw")
        print(result.errors.summary())

    asyncio.run(main())
    ```
"""

from __future__ import annotations

import asyncio
import contextlib
import inspect
import logging
import shutil
import tempfile
import time
from collections.abc import Callable, Coroutine
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, TypeGuard, TypeVar, cast, overload

from ..exceptions import SimulationError
from ._cancel import ProcessGroup
from ._common import (
    admit_annual,
    admit_design_day,
    admit_environments,
    admit_model,
    admit_weather,
    async_resolve_version_mismatch,
    async_upload_results,
    build_command,
    ensure_sql_output,
    maybe_preprocess,
    prepare_run_directory,
    publish_exclude,
    resolve_config,
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
    from .config import EnergyPlusConfig
    from .fs import AsyncFileSystem, FileSystem

logger = logging.getLogger(__name__)

_T = TypeVar("_T")


def _is_async_fs(fs: FileSystem | AsyncFileSystem) -> TypeGuard[AsyncFileSystem]:
    """Check whether *fs* is an async file system."""
    return inspect.iscoroutinefunction(getattr(fs, "write_bytes", None))


@overload
async def async_simulate(
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
    fs: FileSystem | AsyncFileSystem | None = None,
    on_progress: Callable[[SimulationProgress], Any] | Literal["tqdm"] | None = None,
    auto_migrate: bool = False,
) -> SimulationResult: ...


@overload
async def async_simulate(
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
    fs: FileSystem | AsyncFileSystem | None = None,
    on_progress: Callable[[SimulationProgress], Any] | Literal["tqdm"] | None = None,
    auto_migrate: bool = False,
) -> SimulationResult: ...


async def async_simulate(
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
    fs: FileSystem | AsyncFileSystem | None = None,
    on_progress: Callable[[SimulationProgress], Any] | Literal["tqdm"] | None = None,
    auto_migrate: bool = False,
) -> SimulationResult:
    """Run an EnergyPlus simulation without blocking the event loop.

    This is the async counterpart to [simulate][idfkit.simulation.runner.simulate].
    All parameters and return values are identical; the only difference is that
    EnergyPlus runs as an [asyncio][] subprocess, allowing the caller to
    ``await`` the result while other coroutines continue executing.

    Cancellation is supported: if the wrapping [asyncio.Task][] is
    cancelled, the EnergyPlus subprocess is killed and cleaned up.

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
            to the main EnergyPlus subprocess; preprocessor stages have an
            independent budget — see *preprocessor_timeout*.
        preprocessor_timeout: Per-subprocess timeout (seconds) applied
            individually to ExpandObjects, Slab, and Basement when they
            run automatically.  ``None`` (the default) consults the
            ``IDFKIT_PREPROCESSOR_TIMEOUT`` environment variable, falling
            back to 120 s.  Independent of *timeout*.
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
            storage (e.g., S3).  Both sync [FileSystem][idfkit.simulation.fs.FileSystem]
            and async [AsyncFileSystem][idfkit.simulation.fs.AsyncFileSystem] are accepted.
            When an ``AsyncFileSystem`` is provided, uploads and result reads
            are truly non-blocking.  A sync ``FileSystem`` is automatically
            wrapped in [asyncio.to_thread][] to avoid blocking the event
            loop.  As in ``simulate``, the weather file is not uploaded and
            the local temp directory is deleted afterwards.  Combined with
            *cache*, a miss is cached from the local run directory and a hit uploads the cached outputs to
            ``output_dir``, so the remote folder exists either way.
        on_progress: Optional callback invoked with a
            [SimulationProgress][idfkit.simulation.progress.SimulationProgress] event
            each time EnergyPlus emits a progress line.  Both synchronous
            and async callables are accepted -- async callables are awaited.
            Pass ``"tqdm"`` to use a built-in tqdm progress bar (requires
            ``pip install idfkit[progress]``).
        auto_migrate: When ``True`` and ``model.version`` differs from the
            installed EnergyPlus version, forward-migrate the model before
            running. See [simulate][idfkit.simulation.runner.simulate] for
            the full semantics.

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
        ExpandObjectsError: If a preprocessing step fails.
        EnergyPlusNotFoundError: If EnergyPlus cannot be found.
        VersionMismatchError: If ``model.version`` names another release line
            than the installed EnergyPlus (a ``9.0`` model on 9.0.1 matches) and
            *auto_migrate* is ``False``, or if the model is
            newer than the installed EnergyPlus.
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
        return await _simulate_local(model, weather, output_dir=output_dir, **options)
    if output_dir is None:
        msg = "output_dir is required when using a file system backend"
        raise ValueError(msg)
    # EnergyPlus runs in a local scratch directory, which is uploaded to output_dir and then deleted.
    scratch = Path(tempfile.mkdtemp(prefix="idfkit_sim_"))
    try:
        remote_dir = Path(str(output_dir))
        return await _simulate_local(
            model,
            weather,
            output_dir=scratch,
            publish=lambda local, weather_path: _publish(local, remote_dir, fs, weather_path),
            **options,
        )
    finally:
        await asyncio.to_thread(shutil.rmtree, scratch, ignore_errors=True)


async def _simulate_local(
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
    publish: Callable[[SimulationResult, Path | None], Coroutine[Any, Any, SimulationResult]] | None = None,
) -> SimulationResult:
    """Run EnergyPlus in the local *output_dir* (a new temp directory when ``None``); see `async_simulate`.

    With *publish*, the result (a cache hit as stored, uncopied) is passed to it
    with the resolved weather file, and what it returns is returned.
    """
    progress_cb, progress_cleanup = resolve_on_progress(on_progress)

    try:
        # Admission is a pure argument check, so it runs before EnergyPlus discovery.
        admit_model(model, "async_simulate")
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

        sim_input_model, migration_report = await async_resolve_version_mismatch(
            model=model,
            config=config,
            auto_migrate=auto_migrate,
        )

        logger.info(
            "Starting async simulation %s",
            "without a weather file" if weather_path is None else f"with weather {weather_path.name}",
        )

        # Copy model to avoid mutation.  The copy is taken before any await so
        # that the cache key and the simulated model describe the same state,
        # even if another coroutine mutates the caller's model meanwhile.
        sim_model = sim_input_model.copy()

        cache_key = None
        if cache is not None:
            # Hashing the model's external files is blocking I/O, so it runs off the event loop.
            cache_key = await asyncio.to_thread(
                runner_cache_key,
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
                cached.migration_report = migration_report
                if publish is not None:
                    return await publish(cached, weather_path)  # uploaded straight from the cache entry
                # Copy the hit into output_dir, as a fresh run would fill it (no copy without one).
                return await asyncio.to_thread(restore_cached_result, cached, local_output_dir, weather_path)

        ensure_sql_output(sim_model)

        # Preprocessing may invoke subprocesses synchronously — delegate to a
        # thread so we don't block the event loop, and kill them if this coroutine is cancelled.
        sim_model, ep_expand = await _to_thread_killable(
            maybe_preprocess,
            # The copy, not the caller's model: this runs on a worker thread, which must not read a
            # model another coroutine may be editing meanwhile.
            sim_model,
            config,
            weather_path,
            expand_objects,
            preprocessor_timeout,
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

        start = time.monotonic()

        if progress_cb is not None:
            parser = ProgressParser(environment_days(sim_model))
            stdout, stderr, returncode = await _run_with_progress(cmd, run_dir, timeout, progress_cb, parser)
        else:
            stdout, stderr, returncode = await _run_simple(cmd, run_dir, timeout)
    finally:
        if progress_cleanup is not None:
            progress_cleanup()

    elapsed = time.monotonic() - start

    logger.info("Async simulation finished (exit_code=%d) in %.1fs", returncode, elapsed)

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
        return await publish(result, weather_path)
    return result


async def _publish(
    local: SimulationResult, remote_dir: Path, fs: FileSystem | AsyncFileSystem, weather_path: Path | None
) -> SimulationResult:
    """Upload a local result's outputs to *remote_dir* on *fs* and return a result that reads them there."""
    exclude = publish_exclude(weather_path)
    if _is_async_fs(fs):
        await async_upload_results(local.run_dir, remote_dir, fs, exclude=exclude)
        async_fs: AsyncFileSystem | None = fs
        sync_fs: FileSystem | None = None
    else:
        sync_fs = cast("FileSystem", fs)
        await asyncio.to_thread(upload_results, local.run_dir, remote_dir, sync_fs, exclude=exclude)
        async_fs = None
    return SimulationResult(
        run_dir=remote_dir,
        success=local.success,
        exit_code=local.exit_code,
        stdout=local.stdout,
        stderr=local.stderr,
        runtime_seconds=local.runtime_seconds,
        output_prefix=local.output_prefix,
        fs=sync_fs,
        async_fs=async_fs,
        migration_report=local.migration_report,
        output_suffix=local.output_suffix,
        cached=local.cached,
    )


async def _run_simple(
    cmd: list[str],
    run_dir: Path,
    timeout: float,
) -> tuple[str, str, int]:
    """Run EnergyPlus without progress tracking.

    The process is killed and reaped on timeout and on cancellation, so a
    cancelled caller (``asyncio.wait_for``, a dropped request) leaves no
    EnergyPlus behind.
    """
    proc = await _start_process(cmd, run_dir)
    try:
        stdout_bytes, stderr_bytes = await asyncio.wait_for(proc.communicate(), timeout=timeout)
    except asyncio.TimeoutError:
        await _kill(proc)
        msg = f"Simulation timed out after {timeout} seconds"
        raise SimulationError(msg, exit_code=None, stderr=None) from None
    except BaseException:
        # Cancelled (or interrupted): kill, reap, propagate.
        await _kill(proc)
        raise

    stdout = stdout_bytes.decode("utf-8", errors="replace") if stdout_bytes else ""
    stderr = stderr_bytes.decode("utf-8", errors="replace") if stderr_bytes else ""
    returncode = proc.returncode if proc.returncode is not None else -1

    return stdout, stderr, returncode


async def _to_thread_killable(func: Callable[..., _T], /, *args: Any) -> _T:
    """Run *func* in a worker thread as [asyncio.to_thread][] does, killing its subprocesses on cancellation.

    A worker thread cannot be interrupted, so the subprocesses it starts through
    [run_process][idfkit.simulation._cancel.run_process] join a
    [ProcessGroup][idfkit.simulation._cancel.ProcessGroup] that is cancelled when the
    awaiting task is. The thread is then awaited, so it has finished when this re-raises.
    """
    group = ProcessGroup()

    def call() -> _T:
        with group.bind():
            return func(*args)

    task = asyncio.ensure_future(asyncio.to_thread(call))
    try:
        return await asyncio.shield(task)
    except BaseException:
        if not task.done():
            group.cancel()
            # The thread's outcome (its killed subprocess fails it) is moot: the cancellation wins.
            with contextlib.suppress(BaseException):
                await asyncio.shield(task)
        raise


async def _kill(proc: asyncio.subprocess.Process) -> None:
    """Kill *proc* and wait for it to exit, even if the awaiting task is cancelled again meanwhile."""
    with contextlib.suppress(ProcessLookupError):  # it has already exited
        proc.kill()
    await asyncio.shield(proc.wait())


async def _run_with_progress(
    cmd: list[str],
    run_dir: Path,
    timeout: float,
    on_progress: Callable[[SimulationProgress], Any],
    parser: ProgressParser,
) -> tuple[str, str, int]:
    """Run EnergyPlus with async line-by-line stdout streaming for progress."""
    proc = await _start_process(cmd, run_dir)

    stdout_lines: list[str] = []
    is_async_cb = inspect.iscoroutinefunction(on_progress)

    async def _read_stdout() -> None:
        assert proc.stdout is not None  # noqa: S101
        while True:
            raw_line = await proc.stdout.readline()
            if not raw_line:
                break
            line = raw_line.decode("utf-8", errors="replace")
            stdout_lines.append(line)
            event = parser.parse_line(line)
            if event is not None:
                if is_async_cb:
                    await on_progress(event)
                else:
                    on_progress(event)

    async def _read_stderr() -> bytes:
        assert proc.stderr is not None  # noqa: S101
        return await proc.stderr.read()

    stderr_bytes = await _gather_with_timeout(proc, _read_stdout(), _read_stderr(), timeout)

    stdout = "".join(stdout_lines)
    stderr = stderr_bytes.decode("utf-8", errors="replace") if stderr_bytes else ""
    returncode = proc.returncode if proc.returncode is not None else -1

    # EnergyPlus reports "EnergyPlus Completed Successfully" on stderr.
    await _emit_stderr_progress(parser, stderr, on_progress, is_async_cb=is_async_cb)

    return stdout, stderr, returncode


async def _emit_stderr_progress(
    parser: ProgressParser,
    stderr: str,
    on_progress: Callable[[SimulationProgress], Any],
    *,
    is_async_cb: bool,
) -> None:
    """Pass the progress events *parser* finds in *stderr* to *on_progress*.

    A callback error is wrapped in [SimulationError][idfkit.exceptions.SimulationError],
    as it is for a stdout event, whichever stream the line came from.
    """
    try:
        for line in stderr.splitlines():
            event = parser.parse_line(line)
            if event is None:
                continue
            if is_async_cb:
                await on_progress(event)
            else:
                on_progress(event)
    except Exception as exc:
        msg = f"Failed during EnergyPlus execution: {exc}"
        raise SimulationError(msg, exit_code=None, stderr=stderr or None) from exc


async def _start_process(
    cmd: list[str],
    run_dir: Path,
) -> asyncio.subprocess.Process:
    """Start an async subprocess, wrapping OSError."""
    try:
        return await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(run_dir),
        )
    except OSError as exc:
        msg = f"Failed to start EnergyPlus: {exc}"
        raise SimulationError(msg, exit_code=None, stderr=None) from exc


async def _gather_with_timeout(
    proc: asyncio.subprocess.Process,
    stdout_coro: Coroutine[Any, Any, None],
    stderr_coro: Coroutine[Any, Any, bytes],
    timeout: float,
) -> bytes:
    """Run stdout/stderr readers concurrently with a timeout.

    Ensures the subprocess is always killed and awaited on error,
    timeout, or cancellation to prevent leaked EnergyPlus processes.
    """
    stdout_task = asyncio.create_task(stdout_coro)
    stderr_task = asyncio.create_task(stderr_coro)

    try:
        await asyncio.wait_for(
            asyncio.gather(stdout_task, stderr_task),
            timeout=timeout,
        )
    except asyncio.TimeoutError:
        await _kill(proc)
        await _cancel_tasks(stdout_task, stderr_task)
        stderr_str = _decode_stderr(_get_stderr_result(stderr_task))
        msg = f"Simulation timed out after {timeout} seconds"
        raise SimulationError(msg, exit_code=None, stderr=stderr_str) from None
    except asyncio.CancelledError:
        # External cancellation — kill, clean up, propagate.
        await _kill(proc)
        await _cancel_tasks(stdout_task, stderr_task)
        raise
    except Exception as exc:
        # Callback error — kill, capture stderr, wrap in SimulationError
        # to match sync runner behaviour.
        await _kill(proc)
        await _cancel_tasks(stdout_task, stderr_task)
        stderr_str = _decode_stderr(_get_stderr_result(stderr_task))
        msg = f"Failed during EnergyPlus execution: {exc}"
        raise SimulationError(msg, exit_code=None, stderr=stderr_str) from exc

    await proc.wait()

    return _get_stderr_result(stderr_task)


async def _cancel_tasks(*tasks: asyncio.Task[Any]) -> None:
    """Cancel tasks and suppress their exceptions."""
    for task in tasks:
        task.cancel()
    for task in tasks:
        with contextlib.suppress(asyncio.CancelledError, Exception):
            await task


def _get_stderr_result(stderr_task: asyncio.Task[bytes]) -> bytes:
    """Safely extract stderr bytes from a completed task."""
    if not stderr_task.done() or stderr_task.cancelled():
        return b""
    try:
        return stderr_task.result()
    except Exception:
        return b""


def _decode_stderr(data: bytes) -> str | None:
    """Decode stderr bytes, returning ``None`` when empty."""
    if not data:
        return None
    return data.decode("utf-8", errors="replace")
