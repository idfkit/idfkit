"""Parsers for EnergyPlus .rdd and .mdd files.

Parses Report Data Dictionary (.rdd) and Meter Data Dictionary (.mdd) files
to discover available output variables and meters for a model.
"""

from __future__ import annotations

import re
import warnings
from dataclasses import dataclass
from pathlib import Path

# RDD line patterns. EnergyPlus emits one of two formats depending on the
# `Output:VariableDictionary` key field:
#
#   IDF — `Output:VariableDictionary, IDF`. Each line is a ready-to-paste
#   `Output:Variable` object, with the var type and report type collapsed
#   into a "Zone Average" / "HVAC Sum" descriptor between `!-` and `[units]`.
#   The descriptor is optional (older EP versions omit it):
#
#     Output:Variable,*,Site Outdoor Air Drybulb Temperature,hourly; !- Zone Average [C]
#     Output:Variable,*,Zone Mean Air Temperature,hourly; !- [C]
#
#   Regular — `Output:VariableDictionary, Regular` (the EP default). Each
#   line carries the var type and report type as separate fields, no key,
#   no frequency:
#
#     Zone,Average,Site Outdoor Air Drybulb Temperature [C]
#     HVAC,Sum,Zone Ideal Loads Supply Air Total Heating Energy [J]
#
# Both shapes must parse so callers don't have to know which format the
# upstream model requested. For Regular lines we synthesize ``key="*"`` and
# ``frequency="hourly"`` to match what EnergyPlus would have written in the
# IDF form for the same variable.
_RDD_RE = re.compile(
    r"^Output:Variable"
    r",\s*([^,]*)"  # key (e.g. "*")
    r",\s*([^,]*)"  # variable name
    r",\s*([^;]*)"  # frequency
    r";\s*!-[^\[]*\[([^\]]*)\]",  # optional descriptor + units in comment
)
_RDD_REGULAR_RE = re.compile(
    r"^[A-Za-z]+"  # var type (Zone, HVAC) — discarded
    r",\s*[A-Za-z]+"  # report type (Average, Sum) — discarded
    r",\s*(.+?)\s*"  # variable name (non-greedy)
    r"\[([^\]]*)\]\s*$",  # units in brackets at end
)

# MDD line patterns. EnergyPlus emits one of two formats:
#
#   IDF — up to four Output:Meter* variants, each with a frequency:
#
#     Output:Meter,Electricity:Facility,hourly; !- [J]
#     Output:Meter:MeterFileOnly,Electricity:Facility,hourly; !- [J]
#     Output:Meter:Cumulative,Electricity:Facility,hourly; !- [J]
#     Output:Meter:Cumulative:MeterFileOnly,Electricity:Facility,hourly; !- [J]
#
#   Regular — single shape, no frequency, no cumulative variants:
#
#     Zone,Meter,Electricity:Facility [J]
#
# All shapes are recognized so they are not silently skipped. Cumulative IDF
# variants are matched but dropped because OutputMeter has no notion of
# cumulative-vs-running. For Regular lines we synthesize
# ``frequency="hourly"`` to match what EnergyPlus would have written in the
# IDF form.
#
# TODO: model the IDF four-variant landscape explicitly — likely as a
# `cumulative: bool` and `meter_file_only: bool` pair on OutputMeter (or a
# `kind` enum), with `add_all_to_model` choosing the right Output:Meter*
# object type to inject.
_MDD_RE = re.compile(
    r"^Output:Meter(:Cumulative)?(:MeterFileOnly)?"
    r",\s*([^,]*)"  # meter name
    r",\s*([^;]*)"  # frequency
    r";\s*!-[^\[]*\[([^\]]*)\]",  # optional descriptor + units in comment
)
_MDD_REGULAR_RE = re.compile(
    r"^[A-Za-z]+"  # var type (typically "Zone") — discarded
    r",\s*Meter"  # literal "Meter" column
    r",\s*(.+?)\s*"  # meter name (may include colons and spaces)
    r"\[([^\]]*)\]\s*$",  # units in brackets at end
)


@dataclass(frozen=True, slots=True)
class OutputVariable:
    """An available output variable from a ``.rdd`` file.

    Unlike meters, variables are associated with a specific key (zone,
    surface, etc.).  For post-simulation SQL results where variables and
    meters are stored together, see
    [VariableInfo][idfkit.simulation.parsers.sql.VariableInfo].

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
    """An available meter from a ``.mdd`` file.

    Meters aggregate energy or resource consumption and have no key value,
    unlike [OutputVariable][idfkit.simulation.parsers.rdd.OutputVariable].  For post-simulation SQL results where
    variables and meters are stored together, see
    [VariableInfo][idfkit.simulation.parsers.sql.VariableInfo].

    Attributes:
        name: The meter name (e.g. ``"Electricity:Facility"``).
        frequency: The default reporting frequency (e.g. ``"hourly"``).
        units: The meter units (e.g. ``"J"``).
    """

    name: str
    frequency: str
    units: str


class DictionaryParseWarning(UserWarning):
    """Emitted when a non-empty ``.rdd`` / ``.mdd`` file parses to zero entries.

    A non-empty dictionary file with zero parsed entries almost always means
    EnergyPlus emitted a format the regex doesn't recognize, not that the
    model genuinely exposes no variables / meters. The warning surfaces that
    silent failure so callers don't get a confusingly empty
    [OutputVariableIndex][idfkit.simulation.outputs.OutputVariableIndex].
    """


def _warn_if_silently_empty(text: str, parsed_count: int, kind: str) -> None:
    """Warn when a non-empty dictionary file produced zero parsed entries."""
    if parsed_count > 0:
        return
    if not any(line.strip() and not line.lstrip().startswith("!") for line in text.splitlines()):
        return
    warnings.warn(
        f"Parsed 0 entries from a non-empty {kind} file. The file likely uses a format "
        "this parser does not recognize; please report it at "
        "https://github.com/idfkit/idfkit/issues with a sample line.",
        DictionaryParseWarning,
        stacklevel=3,
    )


def parse_rdd(text: str) -> tuple[OutputVariable, ...]:
    """Parse RDD content from a string.

    Accepts both EnergyPlus output formats. ``Output:VariableDictionary, IDF``
    lines preserve the original ``key`` and ``frequency``. ``Regular`` lines
    don't carry that information, so ``key`` is synthesized as ``"*"`` and
    ``frequency`` as ``"hourly"`` (the values EnergyPlus would have written
    in the IDF form for the same variable).

    Args:
        text: Raw .rdd file contents.

    Returns:
        Tuple of parsed OutputVariable entries.

    Warns:
        DictionaryParseWarning: If *text* contains non-comment lines but
            none of them parsed as either an IDF-form ``Output:Variable``
            entry or a Regular-form variable row.
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
            continue
        m = _RDD_REGULAR_RE.match(line)
        if m:
            results.append(
                OutputVariable(
                    key="*",
                    name=m.group(1).strip(),
                    frequency="hourly",
                    units=m.group(2).strip(),
                )
            )
    _warn_if_silently_empty(text, len(results), ".rdd")
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

    Accepts both EnergyPlus output formats. In ``Output:VariableDictionary,
    IDF`` mode all four meter variants (``Output:Meter``,
    ``Output:Meter:MeterFileOnly``, ``Output:Meter:Cumulative``,
    ``Output:Meter:Cumulative:MeterFileOnly``) are recognized; cumulative
    entries are dropped since [OutputMeter][idfkit.simulation.parsers.rdd.OutputMeter]
    does not yet distinguish cumulative from running, and ``MeterFileOnly``
    variants collapse onto the same ``(name, frequency, units)`` as their
    plain counterpart. ``Regular`` lines don't carry frequency, so it is
    synthesized as ``"hourly"`` (Regular MDD does not list cumulative
    variants).

    Args:
        text: Raw .mdd file contents.

    Returns:
        Tuple of parsed OutputMeter entries (IDF cumulative variants dropped).

    Warns:
        DictionaryParseWarning: If *text* contains non-comment lines but
            none of them parsed as either an IDF-form ``Output:Meter*``
            entry or a Regular-form meter row.
    """
    results: list[OutputMeter] = []
    matched = 0
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("!"):
            continue
        m = _MDD_RE.match(line)
        if m:
            matched += 1
            cumulative = m.group(1) is not None
            if cumulative:
                continue
            results.append(
                OutputMeter(
                    name=m.group(3).strip(),
                    frequency=m.group(4).strip(),
                    units=m.group(5).strip(),
                )
            )
            continue
        m = _MDD_REGULAR_RE.match(line)
        if m:
            matched += 1
            results.append(
                OutputMeter(
                    name=m.group(1).strip(),
                    frequency="hourly",
                    units=m.group(2).strip(),
                )
            )
    _warn_if_silently_empty(text, matched, ".mdd")
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
