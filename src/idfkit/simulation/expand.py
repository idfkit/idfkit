"""Expand template and preprocessor objects using EnergyPlus utilities.

Three preprocessors are supported:

* **ExpandObjects** (C++) converts ``HVACTemplate:*`` objects into detailed
  low-level HVAC equivalents.
* **Slab** (Fortran) computes monthly ground surface temperatures for
  slab-on-grade foundations (``GroundHeatTransfer:Slab:*``).
* **Basement** (Fortran) computes ground temperatures around basement walls
  and floors (``GroundHeatTransfer:Basement:*``).

Example::

    from idfkit import load_idf
    from idfkit.simulation import expand_objects, run_slab_preprocessor

    model = load_idf("building_with_templates.idf")
    expanded = expand_objects(model)

    model_with_slab = load_idf("building_with_slab.idf")
    expanded = run_slab_preprocessor(model_with_slab)

Design rationale
----------------

**Why three separate functions instead of one?**

Each preprocessor has distinct inputs (IDD files, weather data), different
output files, and independent failure modes.  Keeping them separate lets
callers run only what they need -- most models use at most one of the
three -- and avoids hiding long-running ground heat-transfer solvers behind
a simple ``expand()`` call.

**Detection: schema groups with prefix fallback**

Whether a model *needs* a given preprocessor is determined by querying the
EpJSON schema's ``group`` field (e.g. ``"HVAC Templates"``,
``"Detailed Ground Heat Transfer"``).  This is more robust than name-prefix
matching alone because it is authoritative.  When no schema is loaded, we
fall back to prefix matching (``HVACTemplate:``, ``GroundHeatTransfer:Slab:``).
Slab and Basement objects share the same group, so detection combines group
membership with a prefix filter to distinguish between the two.

**Four-layer error detection for Slab & Basement**

The Fortran-based Slab and Basement preprocessors have several quirks that
a single ``returncode != 0`` check cannot cover.  In testing we observed:

1. *Non-zero exit codes only from crashes* -- both preprocessors always exit
   with code 0, even on fatal input errors.  A non-zero code (e.g. 139 for
   SIGSEGV) means an abnormal termination such as a segfault.
2. *Fatal errors reported in output files* -- input validation errors are
   written as ``Output:PreprocessorMessage`` IDF objects with
   ``Fatal`` severity, while the process still exits 0.
3. *Silent solver failures* -- if the iterative 3-D solver fails to converge
   (e.g. from extreme material properties), the process exits 0 and the
   output file exists but is **empty** (0 bytes).  No
   ``Output:PreprocessorMessage`` is written.

To catch all of these, each preprocessor run passes through four checks in
order::

    _check_process_exit_code   →  catches crashes (SIGSEGV, etc.)
    _require_file              →  catches missing output file
    _check_output_not_empty    →  catches silent solver failures
    _check_for_fatal_preprocessor_message  →  catches IDF-level Fatal errors

ExpandObjects (C++) does not use the exit-code or empty-file checks because
its error semantics differ from the Fortran preprocessors.

**Automatic integration with ``simulate()``**

The :func:`~idfkit.simulation.runner.simulate` function automatically
detects ground heat-transfer objects and runs the preprocessing pipeline
before simulation.  It invokes :func:`run_preprocessing`, which runs
ExpandObjects once, then checks which preprocessor input files were
produced (``GHTIn.idf`` and/or ``BasementGHTIn.idf``) and runs the
corresponding solver.  This means users do not need to call the
preprocessors explicitly -- ``simulate()`` does the right thing.  The
individual public functions are retained for cases where the user wants
to inspect or modify the preprocessed model before simulation.

**File handling mirrors the simulation runner**

The same care taken in :func:`~idfkit.simulation.runner.simulate` --
copying ``Energy+.idd`` to the run directory, isolating work in a temp
directory, cleaning up afterward -- is applied here.  Each preprocessor
also requires its own IDD (``SlabGHT.idd``, ``BasementGHT.idd``) and
expects a weather file named ``in.epw`` in its working directory.
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


def _check_process_exit_code(
    proc: subprocess.CompletedProcess[str],
    *,
    label: str,
) -> None:
    """Raise if the subprocess exited with a non-zero code.

    The Slab and Basement preprocessors (Fortran) always exit with code 0
    even on errors (using Fortran ``STOP`` statements).  A non-zero exit
    code therefore indicates an abnormal termination such as a crash
    (e.g. SIGSEGV, exit code 139).
    """
    if proc.returncode != 0:
        msg = f"{label} crashed with exit code {proc.returncode}"
        raise ExpandObjectsError(
            msg,
            preprocessor=label,
            exit_code=proc.returncode,
            stderr=proc.stderr.strip() if proc.stderr else None,
        )


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


def _check_output_not_empty(
    path: Path,
    *,
    label: str,
    proc: subprocess.CompletedProcess[str],
) -> None:
    """Raise if the output file is empty, indicating a silent computation failure.

    The Slab and Basement preprocessors may exit with code 0 but produce
    an empty output file when the solver fails to converge or encounters
    an unrecoverable numerical error.  In these cases no
    ``Output:PreprocessorMessage`` is written, making the empty file the
    only reliable signal.
    """
    if path.stat().st_size == 0:
        msg = f"{label} produced an empty output file ({path.name}), indicating a computation failure"
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


def _append_file(target: Path, source: Path) -> None:
    """Append the contents of *source* to *target*."""
    with open(target, "a", encoding="latin-1") as dst, open(source, encoding="latin-1") as src:
        dst.write("\n")
        dst.write(src.read())


# ---------------------------------------------------------------------------
# In-directory preprocessor runners
# ---------------------------------------------------------------------------


def _run_slab_in_dir(config: EnergyPlusConfig, run_dir: Path, *, timeout: float) -> None:
    """Run the Slab preprocessor in a directory where ExpandObjects has already run.

    Assumes ``GHTIn.idf`` exists in *run_dir*.  Copies ``SlabGHT.idd``,
    invokes the Slab solver, validates the output, and appends the
    resulting ``SLABSurfaceTemps.TXT`` to ``expanded.idf``.
    """
    slab_exe = config.slab_exe
    slab_idd = config.slab_idd
    if slab_exe is None or slab_idd is None:
        msg = (
            f"Slab preprocessor not found in EnergyPlus installation at "
            f"{config.install_dir}.  Expected at PreProcess/GrndTempCalc/Slab."
        )
        raise ExpandObjectsError(msg, preprocessor="Slab")

    shutil.copy2(slab_idd, run_dir / "SlabGHT.idd")

    proc = _run_subprocess(slab_exe, cwd=run_dir, timeout=timeout, label="Slab")
    _check_process_exit_code(proc, label="Slab")
    slab_output = run_dir / "SLABSurfaceTemps.TXT"
    _require_file(slab_output, label="Slab", proc=proc)
    _check_output_not_empty(slab_output, label="Slab", proc=proc)
    _check_for_fatal_preprocessor_message(slab_output, label="Slab", proc=proc)

    _append_file(run_dir / "expanded.idf", slab_output)


def _run_basement_in_dir(config: EnergyPlusConfig, run_dir: Path, *, timeout: float) -> None:
    """Run the Basement preprocessor in a directory where ExpandObjects has already run.

    Assumes ``BasementGHTIn.idf`` exists in *run_dir*.  Copies
    ``BasementGHT.idd``, invokes the Basement solver, validates the
    output, and appends the resulting ``EPObjects.TXT`` to
    ``expanded.idf``.
    """
    basement_exe = config.basement_exe
    basement_idd = config.basement_idd
    if basement_exe is None or basement_idd is None:
        msg = (
            f"Basement preprocessor not found in EnergyPlus installation at "
            f"{config.install_dir}.  Expected at PreProcess/GrndTempCalc/Basement."
        )
        raise ExpandObjectsError(msg, preprocessor="Basement")

    shutil.copy2(basement_idd, run_dir / "BasementGHT.idd")

    proc = _run_subprocess(basement_exe, cwd=run_dir, timeout=timeout, label="Basement")
    _check_process_exit_code(proc, label="Basement")
    basement_output = run_dir / "EPObjects.TXT"
    _require_file(basement_output, label="Basement", proc=proc)
    _check_output_not_empty(basement_output, label="Basement", proc=proc)
    _check_for_fatal_preprocessor_message(basement_output, label="Basement", proc=proc)

    _append_file(run_dir / "expanded.idf", basement_output)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def needs_ground_heat_preprocessing(model: IDFDocument) -> bool:
    """Return ``True`` if *model* contains ground heat-transfer objects.

    Checks for ``GroundHeatTransfer:Slab:*`` and
    ``GroundHeatTransfer:Basement:*`` objects that require the Slab or
    Basement preprocessor before simulation.

    This is used by :func:`~idfkit.simulation.runner.simulate` to decide
    whether to auto-run the preprocessing pipeline.
    """
    return _has_slab_objects(model) or _has_basement_objects(model)


def run_preprocessing(
    model: IDFDocument,
    *,
    energyplus: EnergyPlusConfig | None = None,
    weather: str | Path | None = None,
    timeout: float = 120.0,
) -> IDFDocument:
    """Run ExpandObjects and any required ground heat-transfer preprocessors.

    This is a convenience function that runs all needed preprocessors in
    a single call.  It runs ExpandObjects once, then checks which
    preprocessor input files were produced (``GHTIn.idf`` and/or
    ``BasementGHTIn.idf``) and runs the corresponding Fortran solvers.

    :func:`~idfkit.simulation.runner.simulate` calls this automatically
    when the model contains ground heat-transfer objects and
    *expand_objects* is ``True``.  Call it directly only when you need to
    inspect or modify the preprocessed model before simulation.

    Args:
        model: The EnergyPlus model to preprocess.
        energyplus: Pre-configured EnergyPlus installation.  If ``None``,
            auto-discovery is used.
        weather: Path to a weather file (``.epw``).  Required by the
            Slab and Basement solvers.
        timeout: Maximum time in seconds for each subprocess invocation
            (default 120).

    Returns:
        A new :class:`~idfkit.document.IDFDocument` with all
        preprocessing applied.

    Raises:
        EnergyPlusNotFoundError: If no EnergyPlus installation is found.
        ExpandObjectsError: If any preprocessor step fails.
    """
    config = energyplus if energyplus is not None else find_energyplus()
    run_dir = _prepare_run_dir(model, weather=weather)
    try:
        _run_expand_objects(config, run_dir, timeout=timeout)

        if (run_dir / "GHTIn.idf").is_file():
            _run_slab_in_dir(config, run_dir, timeout=timeout)

        if (run_dir / "BasementGHTIn.idf").is_file():
            _run_basement_in_dir(config, run_dir, timeout=timeout)

        return _parse_expanded(run_dir)
    finally:
        shutil.rmtree(run_dir, ignore_errors=True)


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
    try:
        _run_expand_objects(config, run_dir, timeout=timeout)
        return _parse_expanded(run_dir)
    finally:
        shutil.rmtree(run_dir, ignore_errors=True)


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
    try:
        _run_expand_objects(config, run_dir, timeout=timeout)

        ght_input = run_dir / "GHTIn.idf"
        if not ght_input.is_file():
            msg = (
                "ExpandObjects did not produce GHTIn.idf.  "
                "Ensure the model contains GroundHeatTransfer:Slab:* objects and "
                "GroundHeatTransfer:Control has run_slab_preprocessor set to Yes."
            )
            raise ExpandObjectsError(msg, preprocessor="ExpandObjects")

        _run_slab_in_dir(config, run_dir, timeout=timeout)
        return _parse_expanded(run_dir)
    finally:
        shutil.rmtree(run_dir, ignore_errors=True)


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
    try:
        _run_expand_objects(config, run_dir, timeout=timeout)

        ght_input = run_dir / "BasementGHTIn.idf"
        if not ght_input.is_file():
            msg = (
                "ExpandObjects did not produce BasementGHTIn.idf.  "
                "Ensure the model contains GroundHeatTransfer:Basement:* objects and "
                "GroundHeatTransfer:Control has run_basement_preprocessor set to Yes."
            )
            raise ExpandObjectsError(msg, preprocessor="ExpandObjects")

        _run_basement_in_dir(config, run_dir, timeout=timeout)
        return _parse_expanded(run_dir)
    finally:
        shutil.rmtree(run_dir, ignore_errors=True)
