"""Catalogue of common EnergyPlus warning and error message kinds.

EnergyPlus reports problems as free text, in the ``.err`` file and in the
``Errors`` table of the SQLite output. This module recognises the messages
that come up most often and turns each into a :class:`MessageKind`: a stable
dotted id, a one-sentence hint at the likely causes, the neighbouring object
types worth inspecting, and the result symptoms the message can explain.

It also pulls the ``(type, name)`` pairs a message names, so a caller can link
the message back to objects in the model. The module is pure data and regular
expressions: it imports nothing from the document model, and a ``type`` is
returned as the message writes it (``"AirLoop"``, ``"Coil:Cooling:DX:SingleSpeed"``),
leaving the mapping onto schema object types to the caller.

The catalogue is internal-ish data. Every kind is tested against real
EnergyPlus output, mostly read from the SQLite fixtures in
``tests/fixtures/simulation/linked``, so a version whose wording drifts fails
the tests rather than silently classifying fewer messages.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

__all__ = ["MESSAGE_KINDS", "MessageKind", "classify_message"]


@dataclass(frozen=True, slots=True)
class MessageKind:
    """One recognised kind of EnergyPlus message.

    Attributes:
        kind: Stable dotted lowercase id, such as ``"dxcoil.low_outlet_temp"``.
        pattern: Compiled regular expression searched in the message text. It
            may define the named groups ``type`` and ``name`` (an object of a
            named type) or ``key`` (an object whose type the message does not
            state).
        hint: The likely causes, in one sentence.
        inspect: Neighbouring EnergyPlus object types worth checking.
        symptoms: The result symptoms this kind can explain (``unmet_heating``,
            ``unmet_cooling``, ``peak_outlier``, ``sizing_zero``). The symptom
            ``message:<kind>`` is implied and not listed.
    """

    kind: str
    pattern: re.Pattern[str]
    hint: str
    inspect: tuple[str, ...]
    symptoms: tuple[str, ...]


# A name that is not quoted runs until two spaces, a comma, a semicolon or the end.
_UNQUOTED_END = r"(?=\s{2,}|[,;]|\s*$)"

MESSAGE_KINDS: tuple[MessageKind, ...] = (
    MessageKind(
        kind="sizing.zero_load",
        pattern=re.compile(r"Calculated design (?:cooling|heating) load for zone=(?P<key>.+?) is zero"),
        hint="The zone has no design load, usually because it has no thermostat, no loads, or is excluded from sizing.",
        inspect=("Sizing:Zone", "ZoneControl:Thermostat", "ZoneHVAC:EquipmentConnections"),
        symptoms=("sizing_zero",),
    ),
    MessageKind(
        kind="dxcoil.low_outlet_temp",
        pattern=re.compile(
            r"(?P<type>Coil:Cooling:DX[\w:]*) \"(?P<name>[^\"]+)\" - "
            r"Full load outlet air dry-bulb temperature < 2C"
        ),
        hint="The DX coil sees too little air flow per unit of capacity or too cold an inlet, so it risks frosting.",
        inspect=("Sizing:System", "Fan:OnOff", "OutdoorAir:Mixer", "ZoneHVAC:WindowAirConditioner"),
        symptoms=("unmet_cooling", "peak_outlier"),
    ),
    MessageKind(
        kind="dxcoil.low_ambient",
        pattern=re.compile(
            r"(?P<type>Coil:Cooling:DX[\w:]*) \"(?P<name>[^\"]+)\" - "
            r"Air-cooled condenser inlet dry-bulb temperature below 0 C"
        ),
        hint="The DX coil runs in cooling at sub-zero outdoor air, often because economiser or availability is absent.",
        inspect=("Controller:OutdoorAir", "AvailabilityManager:LowTemperatureTurnOff", "Curve:Biquadratic"),
        symptoms=("peak_outlier",),
    ),
    MessageKind(
        kind="zonehvac.max_iterations",
        pattern=re.compile(r"(?P<type>ZoneHVAC:[\w:]+)=\"(?P<name>[^\"]+)\" -- Exceeded max iterations"),
        hint="The zone unit cannot settle on a part-load ratio, usually because it is undersized or its fan cycles.",
        inspect=("Coil:Cooling:DX:SingleSpeed", "Fan:OnOff", "ZoneControl:Thermostat"),
        symptoms=("unmet_cooling", "unmet_heating"),
    ),
    MessageKind(
        kind="sizing.system_flow_ratio",
        pattern=re.compile(
            r"FinalSystemSizing: (?P<type>AirLoop)=\"(?P<name>[^\"]+)\", "
            r"Sizing:System Central Heating Maximum System Air Flow Ratio"
        ),
        hint="The Sizing:System heating air flow ratio is lower than the zones need, so the heating coil may undersize.",
        inspect=("Sizing:System", "Sizing:Zone", "AirLoopHVAC"),
        symptoms=("unmet_heating",),
    ),
    MessageKind(
        kind="airloop.no_controllers",
        pattern=re.compile(r"GetAirPathData: (?P<type>AirLoopHVAC)=\"(?P<name>[^\"]+)\" has no Controllers"),
        hint="The air loop has no controller list, which is fine without water coils or outdoor air control.",
        inspect=("AirLoopHVAC:ControllerList", "Controller:OutdoorAir", "Controller:WaterCoil"),
        symptoms=(),
    ),
    MessageKind(
        kind="designday.pressure",
        pattern=re.compile(
            r"SetUpDesignDay: Entered DesignDay Barometric Pressure=.*?"
            r"occurs in DesignDay=(?P<key>.+?), Standard Pressure",
            re.DOTALL,
        ),
        hint="The design day barometric pressure does not match the site elevation, so the standard pressure is used.",
        inspect=("SizingPeriod:DesignDay", "Site:Location"),
        symptoms=("peak_outlier",),
    ),
    MessageKind(
        kind="location.weather_file",
        pattern=re.compile(
            r"Weather file location will be used rather than entered \(IDF\) Location object\."
            r"(?:\s*\.\.Location object=(?P<key>.+?)" + _UNQUOTED_END + ")?"
        ),
        hint="The Site:Location differs from the weather file, so design days and the run period disagree on climate.",
        inspect=("Site:Location", "SizingPeriod:DesignDay"),
        symptoms=("peak_outlier", "unmet_heating", "unmet_cooling"),
    ),
    MessageKind(
        kind="output.variable_not_generated",
        pattern=re.compile(r"The following Report Variables were requested but not generated"),
        hint="An output variable is misspelled, needs advanced diagnostics, or names a component the model lacks.",
        inspect=("Output:Variable", "Output:Diagnostics"),
        symptoms=(),
    ),
    MessageKind(
        kind="schedule.unused",
        pattern=re.compile(r"The following schedule names are \"Unused Schedules\""),
        hint="Some schedules are defined but never referenced, which is harmless but may hide a broken reference.",
        inspect=("Schedule:Compact", "Schedule:Constant", "Schedule:Year"),
        symptoms=(),
    ),
    MessageKind(
        kind="schedule.day_interval",
        pattern=re.compile(r"ProcessScheduleInput: (?P<type>Schedule:Day:Interval)=\"(?P<name>[^\"]+)\""),
        hint="A Schedule:Day:Interval has invalid times, values or limits, so the schedule may not evaluate as meant.",
        inspect=("ScheduleTypeLimits", "Schedule:Week:Daily"),
        symptoms=("unmet_heating", "unmet_cooling"),
    ),
    MessageKind(
        kind="schedule.input",
        pattern=re.compile(r"ProcessScheduleInput: (?P<type>Schedule:[\w:]+)=\"(?P<name>[^\"]+)\""),
        hint="A schedule has invalid input or names missing type limits, so its values may not be what was meant.",
        inspect=("ScheduleTypeLimits",),
        symptoms=("unmet_heating", "unmet_cooling"),
    ),
    MessageKind(
        kind="surface.shadowing",
        pattern=re.compile(r"GetSurfaceData: There are \d+ window/glass door\(s\) that may cause inaccurate shadowing"),
        hint="Windows on non-convex zones under a full-interior solar distribution can misplace solar gains.",
        inspect=("Building", "ShadowCalculation"),
        symptoms=("peak_outlier",),
    ),
    MessageKind(
        kind="surface.ground_temperatures",
        pattern=re.compile(r"GetHTSurfaceData: Surfaces with interface to Ground found but no \"Ground Temperatures\""),
        hint="Ground-contact surfaces use the default 18 C ground temperature because none was entered.",
        inspect=("Site:GroundTemperature:BuildingSurface",),
        symptoms=("unmet_heating", "peak_outlier"),
    ),
    MessageKind(
        kind="surface.vertices",
        pattern=re.compile(r"GetSurfaceData: Surface (?P<key>.+?) has \d+ vertices which is less than minimum"),
        hint="A surface has fewer than three vertices, usually from a vertex count that does not match the list.",
        inspect=("GlobalGeometryRules", "Zone"),
        symptoms=(),
    ),
    MessageKind(
        kind="psychro.out_of_range",
        pattern=re.compile(r"Temperature out of range \[[^\]]*\] \(Psy\w+\)"),
        hint="A node temperature left the physical range, usually from an unconditioned loop or a runaway setpoint.",
        inspect=("SetpointManager:Scheduled", "ZoneHVAC:EquipmentConnections"),
        symptoms=("peak_outlier",),
    ),
    MessageKind(
        kind="psychro.not_converged",
        pattern=re.compile(r"WetBulb not converged after \d+ iterations\s*\(Psy\w+\)"),
        hint="A wet-bulb calculation failed on an extreme air state, usually a very dry or very cold node.",
        inspect=("SetpointManager:Scheduled", "ZoneHVAC:EquipmentConnections"),
        symptoms=("peak_outlier",),
    ),
    MessageKind(
        kind="waterheater.ratings",
        pattern=re.compile(r"Water heater = (?P<key>.+?):\s+Recovery Efficiency and Energy Factor could not be calc"),
        hint="The water heater never recovered its setpoint in the rating test, so its capacity or setpoint is odd.",
        inspect=("WaterHeater:Mixed", "WaterHeater:Stratified", "Schedule:Compact"),
        symptoms=(),
    ),
    MessageKind(
        kind="coilsystem.sensor_node",
        pattern=re.compile(
            r"Occurs in (?P<type>CoilSystem:Cooling:DX[\w:]*) = (?P<name>.+?)" + _UNQUOTED_END + r"\s*"
            r"Cooling coil control/sensor node is not the same as the cooling coil outlet node"
        ),
        hint="The coil system controls on a node downstream of the coil, so components in between skew its control.",
        inspect=("SetpointManager:MixedAir", "AirLoopHVAC", "Branch"),
        symptoms=("unmet_cooling",),
    ),
    MessageKind(
        kind="wateruse.target_temp",
        pattern=re.compile(
            r"CalcEquipmentFlowRates: \"(?P<key>[^\"]+)\" - Target water temperature is greater than the hot water"
        ),
        hint="The water use target temperature exceeds the supplied hot water temperature, so the demand is unmet.",
        inspect=("WaterUse:Connections", "WaterHeater:Mixed", "Schedule:Compact"),
        symptoms=(),
    ),
    MessageKind(
        kind="node.connection",
        pattern=re.compile(r"Node Connection Error, Node=\"(?P<key>[^\"]+)\""),
        hint="A node is used as an inlet or outlet with no matching partner, so the loop topology is broken.",
        inspect=("NodeList", "Branch", "AirLoopHVAC", "PlantLoop"),
        symptoms=("unmet_heating", "unmet_cooling"),
    ),
)


# Types a message may name without a colon. Typed with a colon (``Coil:Heating:Fuel``) are always accepted.
_PLAIN_TYPES = frozenset({
    "AirLoop",
    "AirLoopHVAC",
    "Branch",
    "Building",
    "Construction",
    "DesignDay",
    "Material",
    "PlantLoop",
    "CondenserLoop",
    "Schedule",
    "Zone",
})

_TYPE = r"(?P<type>[A-Z][A-Za-z0-9]*(?::[A-Za-z0-9]+)*)"
# ``Type="NAME"``, ``Type = "NAME"`` and, for coil-style messages, ``Type "NAME"``.
_GENERIC_QUOTED = re.compile(r"(?<![\w:])" + _TYPE + r"\s*=?\s*\"(?P<name>[^\"]+)\"")
# ``Type = NAME`` or ``Type=NAME`` with an unquoted name, for colon types only.
_GENERIC_UNQUOTED = re.compile(r"(?<![\w:])" + _TYPE + r"\s*=\s*(?P<name>[^\s\",;][^\",;]*?)" + _UNQUOTED_END)


def _clean(name: str) -> str:
    return name.strip().strip("\"'").strip()


def _accepts_type(type_: str) -> bool:
    return ":" in type_ or type_ in _PLAIN_TYPES


def classify_message(text: str) -> tuple[MessageKind | None, list[tuple[str | None, str]]]:
    """Classify an EnergyPlus message and list the objects it names.

    Args:
        text: The message text: the first line of an ``.err`` message, or that
            line joined with its continuation lines, as the SQLite ``Errors``
            table stores it.

    Returns:
        The first catalogue kind whose pattern matches (``None`` when none
        does) and the ``(type, name)`` pairs the message names, deduplicated
        in order of appearance. The kind's own groups come first; a ``key``
        group gives a pair whose type is ``None``. Generic ``Type="NAME"``
        occurrences follow, when ``Type`` contains a colon or is a known plain
        type such as ``AirLoop``. Names are stripped but keep their case.

    Examples:
        >>> kind, pairs = classify_message('GetAirPathData: AirLoopHVAC="EVAP COOLER SYSTEM" has no Controllers.')
        >>> kind.kind if kind else None
        'airloop.no_controllers'
        >>> pairs
        [('AirLoopHVAC', 'EVAP COOLER SYSTEM')]
    """
    pairs: list[tuple[str | None, str]] = []
    seen_names: set[str] = set()

    def add(type_: str | None, name: str) -> None:
        cleaned = _clean(name)
        if cleaned and cleaned not in seen_names:
            seen_names.add(cleaned)
            pairs.append((type_, cleaned))

    matched = _match_kind(text)
    if matched is not None:
        _, found = matched
        groups = found.groupdict()
        if groups.get("name") is not None:
            add(groups.get("type"), groups["name"])
        if groups.get("key") is not None:
            add(None, groups["key"])
    for type_, name in _generic_pairs(text):
        add(type_, name)
    return (matched[0] if matched is not None else None), pairs


def _match_kind(text: str) -> tuple[MessageKind, re.Match[str]] | None:
    for kind in MESSAGE_KINDS:
        found = kind.pattern.search(text)
        if found is not None:
            return kind, found
    return None


def _generic_pairs(text: str) -> list[tuple[str, str]]:
    found_pairs: list[tuple[str, str]] = []
    for found in _GENERIC_QUOTED.finditer(text):
        if _accepts_type(found.group("type")):
            found_pairs.append((found.group("type"), found.group("name")))
    for found in _GENERIC_UNQUOTED.finditer(text):
        if ":" in found.group("type"):
            found_pairs.append((found.group("type"), found.group("name")))
    return found_pairs
