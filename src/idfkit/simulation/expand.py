"""Expand template and preprocessor objects using EnergyPlus utilities.

Three preprocessors are supported:

* **ExpandObjects** converts ``HVACTemplate:*`` objects into detailed
  low-level HVAC equivalents.
* **Slab** computes monthly ground surface temperatures for slab-on-grade
  foundations (``GroundHeatTransfer:Slab:*``).
* **Basement** computes ground temperatures around basement walls and
  floors (``GroundHeatTransfer:Basement:*``).

Example::

    from idfkit import load_idf
    from idfkit.simulation import expand_objects, run_slab_preprocessor

    model = load_idf("building_with_templates.idf")
    expanded = expand_objects(model)

    model_with_slab = load_idf("building_with_slab.idf")
    expanded = run_slab_preprocessor(model_with_slab)
"""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

from ..exceptions import ExpandObjectsError
from .config import EnergyPlusConfig, find_energyplus

if TYPE_CHECKING:
    from ..document import IDFDocument


# ---------------------------------------------------------------------------
# Schema group / prefix constants
# ---------------------------------------------------------------------------

_HVAC_TEMPLATE_GROUP = "HVAC Templates"
_HVAC_TEMPLATE_PREFIX = "HVACTemplate:"

_GHT_GROUP = "Detailed Ground Heat Transfer"
_SLAB_PREFIX = "GroundHeatTransfer:Slab:"
_BASEMENT_PREFIX = "GroundHeatTransfer:Basement:"
_GHT_CONTROL_TYPE = "GroundHeatTransfer:Control"


# ---------------------------------------------------------------------------
# Detection helpers
# ---------------------------------------------------------------------------


def _has_objects_in_group(model: IDFDocument, group: str, prefix: str) -> bool:
    """Return ``True`` if *model* contains objects belonging to *group*.

    Uses the schema ``group`` field when available, falling back to a name
    prefix match.
    """
    schema = model.schema
    if schema is not None:
        return any(schema.get_group(obj_type) == group for obj_type in model)
    return any(obj_type.startswith(prefix) for obj_type in model)


def _needs_expansion(model: IDFDocument) -> bool:
    """Return ``True`` if *model* contains ``HVACTemplate:*`` objects."""
    return _has_objects_in_group(model, _HVAC_TEMPLATE_GROUP, _HVAC_TEMPLATE_PREFIX)


def _has_slab_objects(model: IDFDocument) -> bool:
    """Return ``True`` if *model* contains ``GroundHeatTransfer:Slab:*`` objects."""
    schema = model.schema
    if schema is not None:
        return any(schema.get_group(t) == _GHT_GROUP and t.startswith(_SLAB_PREFIX) for t in model)
    return any(t.startswith(_SLAB_PREFIX) for t in model)


def _has_basement_objects(model: IDFDocument) -> bool:
    """Return ``True`` if *model* contains ``GroundHeatTransfer:Basement:*`` objects."""
    schema = model.schema
    if schema is not None:
        return any(schema.get_group(t) == _GHT_GROUP and t.startswith(_BASEMENT_PREFIX) for t in model)
    return any(t.startswith(_BASEMENT_PREFIX) for t in model)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _run_subprocess(
    exe: Path,
    *,
    cwd: Path,
    timeout: float,
    label: str,
) -> subprocess.CompletedProcess[str]:
    """Run *exe* in *cwd* and return the completed process.

    Raises :class:`ExpandObjectsError` on timeout or OS errors.
    """
    try:
        return subprocess.run(  # noqa: S603
            [str(exe)],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(cwd),
        )
    except subprocess.TimeoutExpired as exc:
        msg = f"{label} timed out after {timeout} seconds"
        raise ExpandObjectsError(
            msg,
            preprocessor=label,
            exit_code=None,
            stderr=str(exc.stderr) if exc.stderr else None,
        ) from exc
    except OSError as exc:
        msg = f"Failed to start {label}: {exc}"
        raise ExpandObjectsError(
            msg,
            preprocessor=label,
            exit_code=None,
            stderr=None,
        ) from exc


def _require_file(path: Path, *, label: str, proc: subprocess.CompletedProcess[str]) -> None:
    """Raise :class:`ExpandObjectsError` if *path* does not exist."""
    if not path.is_file():
        msg = f"{label} did not produce {path.name}"
        raise ExpandObjectsError(
            msg,
            preprocessor=label,
            exit_code=proc.returncode,
            stderr=proc.stderr.strip() if proc.stderr else None,
        )


_FATAL_PREPROC_RE = re.compile(
    r"Output:PreprocessorMessage\s*,"  # object type
    r"\s*([^,]+)\s*,"  # preprocessor name
    r"\s*Fatal\s*,"  # severity
    r"\s*\n?\s*([^;]+);",  # message (may start on the next line)
)


def _check_for_fatal_preprocessor_message(
    output_path: Path,
    *,
    label: str,
    proc: subprocess.CompletedProcess[str],
) -> None:
    """Raise if a preprocessor output file contains a *Fatal* message.

    EnergyPlus preprocessors (Slab, Basement) report errors via
    ``Output:PreprocessorMessage`` objects written to their output files.
    The process may still exit with code 0, so a non-zero exit code alone
    is not a reliable indicator of failure.  A *Fatal* severity means the
    preprocessor could not produce valid results.
    """
    text = output_path.read_text(encoding="latin-1")
    match = _FATAL_PREPROC_RE.search(text)
    if match:
        source = match.group(1).strip()
        message = match.group(2).strip()
        msg = f"{label} reported a fatal error: {message}"
        raise ExpandObjectsError(
            msg,
            preprocessor=label,
            exit_code=proc.returncode,
            stderr=f"{source}: {message}",
        )


def _run_expand_objects(config: EnergyPlusConfig, run_dir: Path, *, timeout: float) -> None:
    """Run ExpandObjects in *run_dir* (which must already contain ``in.idf``)."""
    exe = config.expand_objects_exe
    if exe is None:
        msg = (
            f"ExpandObjects executable not found in EnergyPlus installation at "
            f"{config.install_dir}.  Ensure you have a complete installation."
        )
        raise ExpandObjectsError(msg, preprocessor="ExpandObjects")

    # Copy Energy+.idd so ExpandObjects can parse the model
    shutil.copy2(config.idd_path, run_dir / "Energy+.idd")

    proc = _run_subprocess(exe, cwd=run_dir, timeout=timeout, label="ExpandObjects")
    _require_file(run_dir / "expanded.idf", label="ExpandObjects", proc=proc)


def _prepare_run_dir(model: IDFDocument, *, weather: str | Path | None = None) -> Path:
    """Write *model* to a temporary directory and return its path.

    If *weather* is provided it is copied into the directory as ``in.epw``
    (the filename the EnergyPlus preprocessors expect).
    """
    from ..writers import write_idf

    run_dir = Path(tempfile.mkdtemp(prefix="idfkit_expand_"))
    write_idf(model, run_dir / "in.idf")
    if weather is not None:
        weather = Path(weather)
        if not weather.is_file():
            msg = f"Weather file not found: {weather}"
            raise ExpandObjectsError(msg)
        shutil.copy2(weather, run_dir / "in.epw")
    return run_dir


def _parse_expanded(run_dir: Path) -> IDFDocument:
    """Parse the ``expanded.idf`` in *run_dir*."""
    from ..idf_parser import parse_idf

    return parse_idf(run_dir / "expanded.idf")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def expand_objects(
    model: IDFDocument,
    *,
    energyplus: EnergyPlusConfig | None = None,
    timeout: float = 120.0,
) -> IDFDocument:
    """Run the EnergyPlus *ExpandObjects* preprocessor and return the expanded document.

    ``ExpandObjects`` replaces ``HVACTemplate:*`` objects with their fully
    specified low-level HVAC equivalents.  The original *model* is **not**
    mutated.

    If the document contains no ``HVACTemplate:*`` objects a
    :meth:`~idfkit.document.IDFDocument.copy` is returned immediately without
    invoking the preprocessor (no EnergyPlus installation required).

    Args:
        model: The EnergyPlus model to expand.
        energyplus: Pre-configured EnergyPlus installation.  If ``None``,
            :func:`~idfkit.simulation.config.find_energyplus` is used for
            auto-discovery.
        timeout: Maximum time in seconds to wait for the preprocessor
            (default 120).

    Returns:
        A new :class:`~idfkit.document.IDFDocument` containing the expanded
        objects.

    Raises:
        EnergyPlusNotFoundError: If no EnergyPlus installation (and therefore
            no ``ExpandObjects`` executable) can be found.
        ExpandObjectsError: If the ``ExpandObjects`` executable is missing
            from the installation or the preprocessor exits with an error.
    """
    if not _needs_expansion(model):
        return model.copy()

    config = energyplus if energyplus is not None else find_energyplus()
    run_dir = _prepare_run_dir(model)
    _run_expand_objects(config, run_dir, timeout=timeout)
    return _parse_expanded(run_dir)


def run_slab_preprocessor(
    model: IDFDocument,
    *,
    energyplus: EnergyPlusConfig | None = None,
    weather: str | Path | None = None,
    timeout: float = 120.0,
) -> IDFDocument:
    """Run the *Slab* ground heat-transfer preprocessor and return the expanded document.

    The workflow is:

    1. ``ExpandObjects`` extracts ``GroundHeatTransfer:Slab:*`` objects from
       the model into ``GHTIn.idf``.
    2. The **Slab** preprocessor reads ``GHTIn.idf`` and computes monthly
       ground surface temperatures, writing ``SLABSurfaceTemps.TXT``.
    3. The resulting temperature schedules are appended to the expanded IDF.

    The original *model* is **not** mutated.

    If the document contains no ``GroundHeatTransfer:Slab:*`` objects a
    :meth:`~idfkit.document.IDFDocument.copy` is returned immediately.

    Args:
        model: The EnergyPlus model containing ``GroundHeatTransfer:Slab:*``
            objects.
        energyplus: Pre-configured EnergyPlus installation.  If ``None``,
            auto-discovery is used.
        weather: Path to a weather file (``.epw``).  Some Slab configurations
            may require weather data.
        timeout: Maximum time in seconds for each subprocess invocation
            (default 120).

    Returns:
        A new :class:`~idfkit.document.IDFDocument` with slab ground
        temperatures appended.

    Raises:
        EnergyPlusNotFoundError: If no EnergyPlus installation is found.
        ExpandObjectsError: If any preprocessor step fails.
    """
    if not _has_slab_objects(model):
        return model.copy()

    config = energyplus if energyplus is not None else find_energyplus()
    run_dir = _prepare_run_dir(model, weather=weather)

    # Step 1: ExpandObjects extracts GHTIn.idf
    _run_expand_objects(config, run_dir, timeout=timeout)

    ght_input = run_dir / "GHTIn.idf"
    if not ght_input.is_file():
        msg = (
            "ExpandObjects did not produce GHTIn.idf.  "
            "Ensure the model contains GroundHeatTransfer:Slab:* objects and "
            "GroundHeatTransfer:Control has run_slab_preprocessor set to Yes."
        )
        raise ExpandObjectsError(msg, preprocessor="ExpandObjects")

    # Step 2: Copy the Slab IDD so the preprocessor can read it
    slab_exe = config.slab_exe
    slab_idd = config.slab_idd
    if slab_exe is None or slab_idd is None:
        msg = (
            f"Slab preprocessor not found in EnergyPlus installation at "
            f"{config.install_dir}.  Expected at PreProcess/GrndTempCalc/Slab."
        )
        raise ExpandObjectsError(msg, preprocessor="Slab")

    shutil.copy2(slab_idd, run_dir / "SlabGHT.idd")

    # Step 3: Run the Slab preprocessor
    proc = _run_subprocess(slab_exe, cwd=run_dir, timeout=timeout, label="Slab")
    slab_output = run_dir / "SLABSurfaceTemps.TXT"
    _require_file(slab_output, label="Slab", proc=proc)
    _check_for_fatal_preprocessor_message(slab_output, label="Slab", proc=proc)

    # Step 4: Append slab results to expanded.idf and parse
    _append_file(run_dir / "expanded.idf", run_dir / "SLABSurfaceTemps.TXT")
    return _parse_expanded(run_dir)


def run_basement_preprocessor(
    model: IDFDocument,
    *,
    energyplus: EnergyPlusConfig | None = None,
    weather: str | Path | None = None,
    timeout: float = 120.0,
) -> IDFDocument:
    """Run the *Basement* ground heat-transfer preprocessor and return the expanded document.

    The workflow is:

    1. ``ExpandObjects`` extracts ``GroundHeatTransfer:Basement:*`` objects
       from the model into ``BasementGHTIn.idf``.
    2. The **Basement** preprocessor reads ``BasementGHTIn.idf`` and computes
       ground temperatures, writing ``EPObjects.TXT``.
    3. The resulting boundary conditions are appended to the expanded IDF.

    The original *model* is **not** mutated.

    If the document contains no ``GroundHeatTransfer:Basement:*`` objects a
    :meth:`~idfkit.document.IDFDocument.copy` is returned immediately.

    Args:
        model: The EnergyPlus model containing
            ``GroundHeatTransfer:Basement:*`` objects.
        energyplus: Pre-configured EnergyPlus installation.  If ``None``,
            auto-discovery is used.
        weather: Path to a weather file (``.epw``).  The Basement preprocessor
            requires weather data to compute ground temperatures.
        timeout: Maximum time in seconds for each subprocess invocation
            (default 120).

    Returns:
        A new :class:`~idfkit.document.IDFDocument` with basement ground
        temperatures appended.

    Raises:
        EnergyPlusNotFoundError: If no EnergyPlus installation is found.
        ExpandObjectsError: If any preprocessor step fails.
    """
    if not _has_basement_objects(model):
        return model.copy()

    config = energyplus if energyplus is not None else find_energyplus()
    run_dir = _prepare_run_dir(model, weather=weather)

    # Step 1: ExpandObjects extracts BasementGHTIn.idf
    _run_expand_objects(config, run_dir, timeout=timeout)

    ght_input = run_dir / "BasementGHTIn.idf"
    if not ght_input.is_file():
        msg = (
            "ExpandObjects did not produce BasementGHTIn.idf.  "
            "Ensure the model contains GroundHeatTransfer:Basement:* objects and "
            "GroundHeatTransfer:Control has run_basement_preprocessor set to Yes."
        )
        raise ExpandObjectsError(msg, preprocessor="ExpandObjects")

    # Step 2: Copy the Basement IDD so the preprocessor can read it
    basement_exe = config.basement_exe
    basement_idd = config.basement_idd
    if basement_exe is None or basement_idd is None:
        msg = (
            f"Basement preprocessor not found in EnergyPlus installation at "
            f"{config.install_dir}.  Expected at PreProcess/GrndTempCalc/Basement."
        )
        raise ExpandObjectsError(msg, preprocessor="Basement")

    shutil.copy2(basement_idd, run_dir / "BasementGHT.idd")

    # Step 3: Run the Basement preprocessor
    proc = _run_subprocess(basement_exe, cwd=run_dir, timeout=timeout, label="Basement")
    basement_output = run_dir / "EPObjects.TXT"
    _require_file(basement_output, label="Basement", proc=proc)
    _check_for_fatal_preprocessor_message(basement_output, label="Basement", proc=proc)

    # Step 4: Append basement results to expanded.idf and parse
    _append_file(run_dir / "expanded.idf", run_dir / "EPObjects.TXT")
    return _parse_expanded(run_dir)


def _append_file(target: Path, source: Path) -> None:
    """Append the contents of *source* to *target*."""
    with open(target, "a", encoding="latin-1") as dst, open(source, encoding="latin-1") as src:
        dst.write("\n")
        dst.write(src.read())
