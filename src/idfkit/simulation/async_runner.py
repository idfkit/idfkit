"""Async EnergyPlus simulation runner.

Non-blocking counterpart to :func:`~idfkit.simulation.runner.simulate` that
uses :mod:`asyncio` subprocess management instead of :func:`subprocess.run`.

The preparation steps (model copy, directory setup, cache lookup) are
synchronous and fast; only the EnergyPlus subprocess execution is truly
async.  Preprocessing (ExpandObjects, Slab, Basement) is delegated to
a thread via :func:`asyncio.to_thread` because those routines use
:func:`subprocess.run` internally.

Example::

    import asyncio
    from idfkit import load_idf
    from idfkit.simulation import async_simulate

    async def main():
        model = load_idf("building.idf")
        result = await async_simulate(model, "weather.epw")
        print(result.errors.summary())

    asyncio.run(main())
"""

from __future__ import annotations

import asyncio
import contextlib
import inspect
import time
from collections.abc import Callable, Coroutine
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

from ..exceptions import SimulationError
from ._common import (
    async_upload_results,
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
    from .config import EnergyPlusConfig
    from .fs import AsyncFileSystem, FileSystem


def _is_async_fs(fs: object) -> bool:
    """Check whether *fs* is an async file system."""
    return inspect.iscoroutinefunction(getattr(fs, "write_bytes", None))


async def async_simulate(
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
    fs: FileSystem | AsyncFileSystem | None = None,
    on_progress: Callable[[SimulationProgress], Any] | Literal["tqdm"] | None = None,
) -> SimulationResult:
    """Run an EnergyPlus simulation without blocking the event loop.

    This is the async counterpart to :func:`~idfkit.simulation.runner.simulate`.
    All parameters and return values are identical; the only difference is that
    EnergyPlus runs as an :mod:`asyncio` subprocess, allowing the caller to
    ``await`` the result while other coroutines continue executing.

    Cancellation is supported: if the wrapping :class:`asyncio.Task` is
    cancelled, the EnergyPlus subprocess is killed and cleaned up.

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
            storage (e.g., S3).  Both sync :class:`~idfkit.simulation.fs.FileSystem`
            and async :class:`~idfkit.simulation.fs.AsyncFileSystem` are accepted.
            When an ``AsyncFileSystem`` is provided, uploads and result reads
            are truly non-blocking.  A sync ``FileSystem`` is automatically
            wrapped in :func:`asyncio.to_thread` to avoid blocking the event
            loop.
        on_progress: Optional callback invoked with a
            :class:`~idfkit.simulation.progress.SimulationProgress` event
            each time EnergyPlus emits a progress line.  Both synchronous
            and async callables are accepted -- async callables are awaited.
            Pass ``"tqdm"`` to use a built-in tqdm progress bar (requires
            ``pip install idfkit[progress]``).

    Returns:
        SimulationResult with paths to output files.

    Raises:
        SimulationError: On timeout, OS error, or missing weather file.
        ExpandObjectsError: If a preprocessing step fails.
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
                readvars=readvars,
                extra_args=extra_args,
            )
            cached = cache.get(cache_key)
            if cached is not None:
                return cached

        # Copy model to avoid mutation
        sim_model = model.copy()
        ensure_sql_output(sim_model)

        # Preprocessing may invoke subprocesses synchronously — delegate to a
        # thread so we don't block the event loop.
        sim_model, ep_expand = await asyncio.to_thread(
            maybe_preprocess, model, sim_model, config, weather_path, expand_objects
        )

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
            stdout, stderr, returncode = await _run_with_progress(cmd, run_dir, timeout, progress_cb)
        else:
            stdout, stderr, returncode = await _run_simple(cmd, run_dir, timeout)
    finally:
        if progress_cleanup is not None:
            progress_cleanup()

    elapsed = time.monotonic() - start

    if fs is not None:
        remote_dir = Path(str(output_dir))
        if _is_async_fs(fs):
            await async_upload_results(run_dir, remote_dir, fs)  # type: ignore[arg-type]
            result = SimulationResult(
                run_dir=remote_dir,
                success=returncode == 0,
                exit_code=returncode,
                stdout=stdout,
                stderr=stderr,
                runtime_seconds=elapsed,
                output_prefix=output_prefix,
                async_fs=fs,  # type: ignore[arg-type]
            )
        else:
            await asyncio.to_thread(upload_results, run_dir, remote_dir, fs)  # type: ignore[arg-type]
            result = SimulationResult(
                run_dir=remote_dir,
                success=returncode == 0,
                exit_code=returncode,
                stdout=stdout,
                stderr=stderr,
                runtime_seconds=elapsed,
                output_prefix=output_prefix,
                fs=fs,  # type: ignore[arg-type]
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


async def _run_simple(
    cmd: list[str],
    run_dir: Path,
    timeout: float,
) -> tuple[str, str, int]:
    """Run EnergyPlus without progress tracking."""
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(run_dir),
        )
        try:
            stdout_bytes, stderr_bytes = await asyncio.wait_for(
                proc.communicate(),
                timeout=timeout,
            )
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            msg = f"Simulation timed out after {timeout} seconds"
            raise SimulationError(
                msg,
                exit_code=None,
                stderr=None,
            ) from None
    except OSError as exc:
        msg = f"Failed to start EnergyPlus: {exc}"
        raise SimulationError(
            msg,
            exit_code=None,
            stderr=None,
        ) from exc

    stdout = stdout_bytes.decode("utf-8", errors="replace") if stdout_bytes else ""
    stderr = stderr_bytes.decode("utf-8", errors="replace") if stderr_bytes else ""
    returncode = proc.returncode if proc.returncode is not None else -1

    return stdout, stderr, returncode


async def _run_with_progress(
    cmd: list[str],
    run_dir: Path,
    timeout: float,
    on_progress: Callable[[SimulationProgress], Any],
) -> tuple[str, str, int]:
    """Run EnergyPlus with async line-by-line stdout streaming for progress."""
    proc = await _start_process(cmd, run_dir)

    stdout_lines: list[str] = []
    parser = ProgressParser()
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

    return stdout, stderr, returncode


async def _start_process(
    cmd: list[str],
    run_dir: Path,
) -> asyncio.subprocess.Process:
    """Start an async subprocess, wrapping OSError."""
    try:
        return await asyncio.create_subprocess_exec(
            *cmd,
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
        proc.kill()
        await proc.wait()
        await _cancel_tasks(stdout_task, stderr_task)
        stderr_str = _decode_stderr(_get_stderr_result(stderr_task))
        msg = f"Simulation timed out after {timeout} seconds"
        raise SimulationError(msg, exit_code=None, stderr=stderr_str) from None
    except asyncio.CancelledError:
        # External cancellation — kill, clean up, propagate.
        proc.kill()
        await proc.wait()
        await _cancel_tasks(stdout_task, stderr_task)
        raise
    except Exception as exc:
        # Callback error — kill, capture stderr, wrap in SimulationError
        # to match sync runner behaviour.
        proc.kill()
        await proc.wait()
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
