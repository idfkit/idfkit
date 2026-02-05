"""EnergyPlus simulation runner.

Executes EnergyPlus as a subprocess and returns structured results.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from ..exceptions import SimulationError
from .config import EnergyPlusConfig, find_energyplus
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
) -> SimulationResult:
    """Run an EnergyPlus simulation.

    Creates an isolated run directory, writes the model, and executes
    EnergyPlus as a subprocess. The caller's model is not mutated.

    Args:
        model: The EnergyPlus model to simulate.
        weather: Path to the weather file (.epw).
        output_dir: Directory for output files (default: auto temp dir).
        energyplus: Pre-configured EnergyPlus installation. If None,
            uses :func:`find_energyplus` for auto-discovery.
        expand_objects: Run ExpandObjects before simulation.
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

    Returns:
        SimulationResult with paths to output files.

    Raises:
        SimulationError: On timeout, OS error, or missing weather file.
        EnergyPlusNotFoundError: If EnergyPlus cannot be found.
    """
    if fs is not None and output_dir is None:
        msg = "output_dir is required when using a file system backend"
        raise ValueError(msg)

    config = _resolve_config(energyplus)
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
    _ensure_sql_output(sim_model)

    # When using a remote fs, always run locally in a temp dir
    local_output_dir = None if fs is not None else output_dir
    run_dir = _prepare_run_directory(local_output_dir, weather_path)
    idf_path = run_dir / "in.idf"

    from ..writers import write_idf

    write_idf(sim_model, idf_path)

    cmd = _build_command(
        config=config,
        idf_path=idf_path,
        weather_path=run_dir / weather_path.name,
        output_dir=run_dir,
        output_prefix=output_prefix,
        output_suffix=output_suffix,
        expand_objects=expand_objects,
        annual=annual,
        design_day=design_day,
        readvars=readvars,
        extra_args=extra_args,
    )

    start = time.monotonic()
    try:
        proc = subprocess.run(  # noqa: S603
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(run_dir),
        )
    except subprocess.TimeoutExpired as exc:
        elapsed = time.monotonic() - start
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
    else:
        elapsed = time.monotonic() - start

        if fs is not None:
            remote_dir = Path(str(output_dir))
            _upload_results(run_dir, remote_dir, fs)
            result = SimulationResult(
                run_dir=remote_dir,
                success=proc.returncode == 0,
                exit_code=proc.returncode,
                stdout=proc.stdout,
                stderr=proc.stderr,
                runtime_seconds=elapsed,
                output_prefix=output_prefix,
                fs=fs,
            )
        else:
            result = SimulationResult(
                run_dir=run_dir,
                success=proc.returncode == 0,
                exit_code=proc.returncode,
                stdout=proc.stdout,
                stderr=proc.stderr,
                runtime_seconds=elapsed,
                output_prefix=output_prefix,
            )
        if cache is not None and cache_key is not None and result.success:
            cache.put(cache_key, result)
        return result


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _upload_results(local_dir: Path, remote_dir: Path, fs: FileSystem) -> None:
    """Upload all output files from a local directory to a remote file system.

    Args:
        local_dir: Local directory containing simulation outputs.
        remote_dir: Remote directory path for the file system.
        fs: File system backend to upload to.
    """
    for p in local_dir.iterdir():
        if p.is_file():
            remote_path = str(remote_dir / p.name)
            fs.write_bytes(remote_path, p.read_bytes())


def _resolve_config(energyplus: EnergyPlusConfig | None) -> EnergyPlusConfig:
    """Resolve EnergyPlus config, auto-discovering if needed.

    Args:
        energyplus: Optional pre-configured config.

    Returns:
        Validated EnergyPlusConfig.
    """
    if energyplus is not None:
        return energyplus
    return find_energyplus()


def _ensure_sql_output(model: IDFDocument) -> None:
    """Add Output:SQLite to the model if not already present.

    Args:
        model: The model to modify in place.
    """
    if "Output:SQLite" not in model:
        model.add("Output:SQLite", "", data={"option_type": "SimpleAndTabular"})


def _prepare_run_directory(output_dir: str | Path | None, weather_path: Path) -> Path:
    """Create and populate the simulation run directory.

    Args:
        output_dir: Explicit output directory, or None for a temp dir.
        weather_path: Path to the weather file to copy.

    Returns:
        Path to the run directory.
    """
    if output_dir is not None:
        run_dir = Path(output_dir).resolve()
        run_dir.mkdir(parents=True, exist_ok=True)
    else:
        run_dir = Path(tempfile.mkdtemp(prefix="idfkit_sim_"))

    # Copy weather file into run dir
    dest = run_dir / weather_path.name
    if not dest.exists():
        shutil.copy2(weather_path, dest)

    return run_dir


def _build_command(
    *,
    config: EnergyPlusConfig,
    idf_path: Path,
    weather_path: Path,
    output_dir: Path,
    output_prefix: str,
    output_suffix: Literal["C", "L", "D"],
    expand_objects: bool,
    annual: bool,
    design_day: bool,
    readvars: bool,
    extra_args: list[str] | None,
) -> list[str]:
    """Build the EnergyPlus command-line invocation.

    Args:
        config: EnergyPlus configuration.
        idf_path: Path to the IDF file.
        weather_path: Path to the weather file in the run dir.
        output_dir: Output directory path.
        output_prefix: Output file prefix.
        output_suffix: Output file naming suffix ("C", "L", or "D").
        expand_objects: Whether to run ExpandObjects.
        annual: Whether to run annual simulation.
        design_day: Whether to run design-day-only simulation.
        readvars: Whether to run ReadVarsESO.
        extra_args: Additional arguments.

    Returns:
        Command as a list of strings.
    """
    cmd: list[str] = [
        str(config.executable),
        "-w",
        str(weather_path),
        "-d",
        str(output_dir),
        "-p",
        output_prefix,
        "-s",
        output_suffix,
        "-i",
        str(config.idd_path),
    ]

    if expand_objects:
        cmd.append("-x")
    if annual:
        cmd.append("-a")
    if design_day:
        cmd.append("-D")
    if readvars:
        cmd.append("-r")
    if extra_args:
        cmd.extend(extra_args)

    cmd.append(str(idf_path))

    return cmd
