"""Shared helpers for sync and async simulation runners.

Internal module — not part of the public API.
"""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from .config import EnergyPlusConfig, find_energyplus

if TYPE_CHECKING:
    from ..document import IDFDocument
    from .fs import AsyncFileSystem, FileSystem


def resolve_config(energyplus: EnergyPlusConfig | None) -> EnergyPlusConfig:
    """Resolve EnergyPlus config, auto-discovering if needed.

    Args:
        energyplus: Optional pre-configured config.

    Returns:
        Validated EnergyPlusConfig.
    """
    if energyplus is not None:
        return energyplus
    return find_energyplus()


def ensure_sql_output(model: IDFDocument) -> None:
    """Add Output:SQLite to the model if not already present.

    Args:
        model: The model to modify in place.
    """
    if "Output:SQLite" not in model:
        model.add("Output:SQLite", "", data={"option_type": "SimpleAndTabular"})


def maybe_preprocess(
    original: IDFDocument,
    sim_model: IDFDocument,
    config: EnergyPlusConfig,
    weather_path: Path,
    expand_objects: bool,
) -> tuple[IDFDocument, bool]:
    """Run ground heat-transfer preprocessing if needed.

    The EnergyPlus CLI's ``-x`` flag runs ExpandObjects for HVACTemplate
    expansion, but does **not** invoke the Slab or Basement Fortran
    solvers.  When GHT objects are present we run the full preprocessing
    pipeline (ExpandObjects + Slab/Basement) ourselves and disable the
    ``-x`` flag.

    Args:
        original: The original (unmutated) model, used for GHT detection.
        sim_model: The working copy of the model.
        config: EnergyPlus configuration.
        weather_path: Resolved path to the weather file.
        expand_objects: Whether the caller requested expansion.

    Returns:
        A ``(model, ep_expand)`` tuple where *model* is either the
        preprocessed model or the original *sim_model*, and *ep_expand*
        indicates whether EnergyPlus should still run ExpandObjects
        via the ``-x`` flag.
    """
    if not expand_objects:
        return sim_model, False

    from .expand import needs_ground_heat_preprocessing, run_preprocessing

    if needs_ground_heat_preprocessing(original):
        preprocessed = run_preprocessing(
            sim_model,
            energyplus=config,
            weather=weather_path,
        )
        return preprocessed, False  # Already expanded by preprocessing

    return sim_model, True  # Let EnergyPlus handle ExpandObjects via -x


def upload_results(local_dir: Path, remote_dir: Path, fs: FileSystem) -> None:
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


async def async_upload_results(local_dir: Path, remote_dir: Path, fs: AsyncFileSystem) -> None:
    """Upload all output files from a local directory to a remote async file system.

    Local file reads are delegated to a thread via :func:`asyncio.to_thread`
    to avoid blocking the event loop.  Remote writes are dispatched
    concurrently via :func:`asyncio.gather`.

    Args:
        local_dir: Local directory containing simulation outputs.
        remote_dir: Remote directory path for the file system.
        fs: Async file system backend to upload to.
    """
    import asyncio

    async def _upload_one(p: Path) -> None:
        remote_path = str(remote_dir / p.name)
        data = await asyncio.to_thread(p.read_bytes)
        await fs.write_bytes(remote_path, data)

    tasks = [asyncio.create_task(_upload_one(p)) for p in local_dir.iterdir() if p.is_file()]
    if tasks:
        await asyncio.gather(*tasks)


def prepare_run_directory(output_dir: str | Path | None, weather_path: Path) -> Path:
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


def build_command(
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
