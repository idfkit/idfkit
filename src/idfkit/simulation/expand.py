"""Expand HVACTemplate and other macro objects using the EnergyPlus ExpandObjects preprocessor.

The ``ExpandObjects`` utility ships with every EnergyPlus installation and
converts high-level template objects (such as ``HVACTemplate:*``) into their
detailed low-level equivalents.  This module wraps that utility so users can
inspect the expanded result without running a full simulation.

Example::

    from idfkit import load_idf
    from idfkit.simulation import expand_objects

    model = load_idf("building_with_templates.idf")
    expanded = expand_objects(model)

    # Browse the generated HVAC objects
    for obj in expanded["ZoneHVAC:IdealLoadsAirSystem"]:
        print(obj.name)
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

from ..exceptions import ExpandObjectsError
from .config import EnergyPlusConfig, find_energyplus

if TYPE_CHECKING:
    from ..document import IDFDocument


_EXPANDABLE_GROUPS = frozenset({
    "HVAC Templates",
    "Detailed Ground Heat Transfer",
})
"""Schema group names whose objects are handled by the ExpandObjects preprocessor."""

_EXPANDABLE_PREFIXES = (
    "HVACTemplate:",
    "GroundHeatTransfer:",
)
"""Fallback prefixes used when the document has no schema loaded."""


def _needs_expansion(model: IDFDocument) -> bool:
    """Return ``True`` if *model* contains any object types handled by ExpandObjects.

    When a schema is available the check is driven by the schema's ``group``
    field, which is authoritative and version-aware.  When no schema is loaded
    we fall back to object-type prefix matching.
    """
    schema = model.schema
    if schema is not None:
        return any(schema.get_group(obj_type) in _EXPANDABLE_GROUPS for obj_type in model)
    return any(obj_type.startswith(_EXPANDABLE_PREFIXES) for obj_type in model)


def expand_objects(
    model: IDFDocument,
    *,
    energyplus: EnergyPlusConfig | None = None,
    timeout: float = 120.0,
) -> IDFDocument:
    """Run the EnergyPlus *ExpandObjects* preprocessor and return the expanded document.

    ``ExpandObjects`` replaces high-level template objects
    (``HVACTemplate:*``, ``GroundHeatTransfer:*``, etc.) with their fully
    specified low-level equivalents.  The original *model* is **not** mutated.

    If the document contains no expandable objects, a
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

    exe = config.expand_objects_exe
    if exe is None:
        msg = (
            f"ExpandObjects executable not found in EnergyPlus installation at "
            f"{config.install_dir}.  Ensure you have a complete installation."
        )
        raise ExpandObjectsError(msg)

    from ..idf_parser import parse_idf
    from ..writers import write_idf

    run_dir = Path(tempfile.mkdtemp(prefix="idfkit_expand_"))

    # ExpandObjects expects the input file to be named ``in.idf`` in the
    # current working directory and writes ``expanded.idf`` alongside it.
    idf_path = run_dir / "in.idf"
    write_idf(model, idf_path)

    try:
        proc = subprocess.run(  # noqa: S603
            [str(exe)],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(run_dir),
        )
    except subprocess.TimeoutExpired as exc:
        msg = f"ExpandObjects timed out after {timeout} seconds"
        raise ExpandObjectsError(msg) from exc
    except OSError as exc:
        msg = f"Failed to start ExpandObjects: {exc}"
        raise ExpandObjectsError(msg) from exc

    expanded_path = run_dir / "expanded.idf"
    if not expanded_path.is_file():
        stderr = proc.stderr.strip() if proc.stderr else ""
        msg = f"ExpandObjects did not produce expanded.idf (exit code {proc.returncode})"
        if stderr:
            msg += f"\nstderr: {stderr[:500]}"
        raise ExpandObjectsError(msg)

    return parse_idf(expanded_path)
