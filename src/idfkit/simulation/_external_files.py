"""Files an EnergyPlus model reads besides the IDF and the weather file.

Internal module — not part of the public API.

EnergyPlus finds each of these files with ``CheckForActualFilePath``, which
tries, in order, the path as written (absolute, or relative to the working
directory), the IDF's directory, and the directory of the EnergyPlus
executable, then the directories named by the ``epin`` and ``input_path``
environment variables.  idfkit runs EnergyPlus with the run directory as both
the working directory and the IDF's directory, so a relative path resolves
against the run directory first and the EnergyPlus executable's directory
second.  [resolve_external_file][idfkit.simulation._external_files.resolve_external_file]
applies the same order so that the cache key hashes the file EnergyPlus will
read.  The two environment variables are not consulted.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

    from ..document import IDFDocument

EXTERNAL_FILE_FIELDS: dict[str, tuple[str, ...]] = {
    "Schedule:File": ("file_name",),
    "Schedule:File:Shading": ("file_name",),
    "Table:IndependentVariable": ("external_file_name",),
    "Table:Lookup": ("external_file_name",),
    "Table:MultiVariableLookup": ("external_file_name",),
    "Table:TwoIndependentVariables": ("external_file_name",),
    "Construction:WindowDataFile": ("file_name",),
    "Chiller:Electric:ASHRAE205": ("representation_file_name",),
    "Coil:DX:ASHRAE205:Performance": ("representation_file_name",),
    "ExternalInterface:FunctionalMockupUnitImport": ("fmu_file_name",),
}
"""Object types whose fields name a file EnergyPlus reads, across every bundled schema version."""

DEFAULT_FILE_NAMES: dict[tuple[str, str], str] = {
    ("Construction:WindowDataFile", "file_name"): "Window5DataFile.dat",
}
"""The file EnergyPlus reads when one of the fields above is left blank."""

UNCACHEABLE_INTERFACES = frozenset({"ptolemyserver", "functionalmockupunitexport"})
"""``ExternalInterface`` modes that exchange data with another program while EnergyPlus runs."""


@dataclass(frozen=True, slots=True)
class ExternalFileRef:
    """One field of one object that names a file EnergyPlus reads."""

    obj_type: str
    field: str
    value: str


def external_file_refs(model: IDFDocument) -> list[ExternalFileRef]:
    """Return the distinct external file references in *model*, sorted.

    A blank field with a default file name (``Construction:WindowDataFile``)
    contributes that default; any other blank field contributes nothing.
    """
    refs: set[ExternalFileRef] = set()
    for obj_type, fields in EXTERNAL_FILE_FIELDS.items():
        if obj_type not in model:
            continue
        for obj in model.get_collection(obj_type):
            for field in fields:
                value = obj.get(field)
                text = str(value).strip() if value is not None else ""
                if not text:
                    text = DEFAULT_FILE_NAMES.get((obj_type, field), "")
                if text:
                    refs.add(ExternalFileRef(obj_type, field, text))
    return sorted(refs, key=lambda r: (r.obj_type, r.field, r.value))


def resolve_external_file(value: str, search_dirs: Sequence[Path]) -> Path | None:
    """Return the file EnergyPlus would read for the path *value*, or ``None`` if there is none.

    An absolute path is used as is.  A relative path is tried against each of
    *search_dirs* in order.  Backslashes are treated as separators on POSIX,
    as EnergyPlus does.
    """
    native = value.replace("\\", "/") if os.sep == "/" else value
    path = Path(native)
    if path.is_absolute():
        return path if path.is_file() else None
    for directory in search_dirs:
        candidate = directory / path
        if candidate.is_file():
            return candidate
    return None


def search_dirs_for_run(output_dir: str | Path | None, executable: Path) -> list[Path]:
    """Return the directories a relative external file path resolves against for one run.

    A run without *output_dir* uses a fresh temporary directory, which holds
    no caller file, so only the EnergyPlus executable's directory remains.
    """
    dirs = [Path(output_dir).resolve()] if output_dir is not None else []
    dirs.append(executable.resolve().parent)
    return dirs


def uncacheable_reason(model: IDFDocument) -> str | None:
    """Explain why a run of *model* must not use the cache, or return ``None`` if it may.

    The cache key covers every file the model names.  It cannot cover a
    Python plugin, which can read any file and import any module, or an
    external interface that exchanges data with another program during the
    run.
    """
    if "PythonPlugin:Instance" in model:
        return "the model runs a PythonPlugin:Instance, which can read inputs the cache key cannot cover"
    for mode in _external_interface_modes(model):
        if mode.lower() in UNCACHEABLE_INTERFACES:
            return f"the model's ExternalInterface ({mode}) exchanges data with another program during the run"
    return None


def _external_interface_modes(model: IDFDocument) -> list[str]:
    """Return the ``Name of External Interface`` of every ``ExternalInterface`` object in *model*."""
    obj_type = "ExternalInterface"
    if obj_type not in model:
        return []
    return [str(obj.get("name_of_external_interface") or "") for obj in model.get_collection(obj_type)]
