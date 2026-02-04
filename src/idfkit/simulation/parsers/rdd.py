"""Parsers for EnergyPlus .rdd and .mdd files.

Parses Report Data Dictionary (.rdd) and Meter Data Dictionary (.mdd) files
to discover available output variables and meters for a model.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

# RDD line pattern:
#   Output:Variable,*,Site Outdoor Air Drybulb Temperature,hourly; !- [C]
_RDD_RE = re.compile(
    r"^Output:Variable"
    r",\s*([^,]*)"  # key (e.g. "*")
    r",\s*([^,]*)"  # variable name
    r",\s*([^;]*)"  # frequency
    r";\s*!-\s*\[([^\]]*)\]",  # units in comment
)

# MDD line pattern:
#   Output:Meter,Electricity:Facility,hourly; !- [J]
_MDD_RE = re.compile(
    r"^Output:Meter"
    r",\s*([^,]*)"  # meter name
    r",\s*([^;]*)"  # frequency
    r";\s*!-\s*\[([^\]]*)\]",  # units in comment
)


@dataclass(frozen=True, slots=True)
class OutputVariable:
    """An available output variable from a .rdd file.

    Attributes:
        key: The key value (e.g. ``"*"`` or ``"ZONE 1"``).
        name: The variable name (e.g. ``"Zone Mean Air Temperature"``).
        frequency: The default reporting frequency (e.g. ``"hourly"``).
        units: The variable units (e.g. ``"C"``, ``"W"``).
    """

    key: str
    name: str
    frequency: str
    units: str


@dataclass(frozen=True, slots=True)
class OutputMeter:
    """An available meter from a .mdd file.

    Attributes:
        name: The meter name (e.g. ``"Electricity:Facility"``).
        frequency: The default reporting frequency (e.g. ``"hourly"``).
        units: The meter units (e.g. ``"J"``).
    """

    name: str
    frequency: str
    units: str


def parse_rdd(text: str) -> tuple[OutputVariable, ...]:
    """Parse RDD content from a string.

    Args:
        text: Raw .rdd file contents.

    Returns:
        Tuple of parsed OutputVariable entries.
    """
    results: list[OutputVariable] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("!"):
            continue
        m = _RDD_RE.match(line)
        if m:
            results.append(
                OutputVariable(
                    key=m.group(1).strip(),
                    name=m.group(2).strip(),
                    frequency=m.group(3).strip(),
                    units=m.group(4).strip(),
                )
            )
    return tuple(results)


def parse_rdd_file(path: str | Path) -> tuple[OutputVariable, ...]:
    """Parse a .rdd file from disk.

    Args:
        path: Path to the .rdd file.

    Returns:
        Tuple of parsed OutputVariable entries.
    """
    text = Path(path).read_text(encoding="latin-1")
    return parse_rdd(text)


def parse_mdd(text: str) -> tuple[OutputMeter, ...]:
    """Parse MDD content from a string.

    Args:
        text: Raw .mdd file contents.

    Returns:
        Tuple of parsed OutputMeter entries.
    """
    results: list[OutputMeter] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("!"):
            continue
        m = _MDD_RE.match(line)
        if m:
            results.append(
                OutputMeter(
                    name=m.group(1).strip(),
                    frequency=m.group(2).strip(),
                    units=m.group(3).strip(),
                )
            )
    return tuple(results)


def parse_mdd_file(path: str | Path) -> tuple[OutputMeter, ...]:
    """Parse a .mdd file from disk.

    Args:
        path: Path to the .mdd file.

    Returns:
        Tuple of parsed OutputMeter entries.
    """
    text = Path(path).read_text(encoding="latin-1")
    return parse_mdd(text)
