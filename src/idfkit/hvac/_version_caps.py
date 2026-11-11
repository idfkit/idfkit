"""Auto-generated per-version severity caps for the connection checks (research R-34).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_version_caps --corpus VERSION=PATH [--corpus VERSION=PATH ...]

Each row caps one check for models of one measured EnergyPlus version, from a corpus measurement of
that version's example files. A model takes the row of the nearest measured version at or below its
own; a model older than the oldest measured version takes the oldest; 26.2 is never capped.
"""

from __future__ import annotations

from typing import Final

from idfkit.hvac._rule_types import VersionCap

MEASURED_VERSIONS: Final[tuple[tuple[int, int, int], ...]] = ((9, 6, 0), (23, 2, 0))
"""The versions whose example files were measured, oldest first."""

VERSION_CAPS: Final[tuple[VersionCap, ...]] = ()
