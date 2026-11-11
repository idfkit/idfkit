"""Simulation results attached to the model objects they concern.

After a simulation, :meth:`ResultIndex.build` links what EnergyPlus wrote to its SQLite output to the
objects of the document that was simulated:

- component sizing rows (``ComponentSizes``),
- timeseries output keys (``ReportDataDictionary``; values are never read),
- object rows of tabular reports (``TabularData``),
- error and warning messages (``Errors``), classified by the message catalogue.

Each link is a :class:`Resolution`: the object it found, the rule that found it and how much to trust
it. The rules run in a fixed order, and the first that answers wins:

1. ``exact``: the source names the object type, and an object of that type has the name.
2. ``typed``: the name is known, and the context (a variable name, a table, a message) picks the type.
3. ``zonelist_composite``: ``"<ZONE> <OBJECT>"``, an object applied to every zone of a zone list.
4. ``space_to_zone``: ``"<ZONE>_SPACE"``, the implicit space of a zone.
5. ``mirrored_shading``: ``"Mir-<SURFACE>"``, the shading surface EnergyPlus mirrors from a surface.
6. ``aggregate``: ``Total``, ``Total Facility``, ``Whole Building`` and other report totals.
7. ``ideal_loads_suffix``: ``"<ZONE> Ideal Loads Air System"``, from an ideal-loads template.
8. ``ems_key``: the ``EMS`` key of an ``EnergyManagementSystem:OutputVariable``.
9. ``substring``: the longest known name inside the key, always ``weak``.

Items no rule answers are listed in :attr:`ResultIndex.unresolved`, never dropped (FR-021). Zone facts
carry the zone multiplier, so a total built from zone rows can apply it (FR-025). The index belongs to
one run; :meth:`ResultIndex.is_fresh` says whether the document still matches it (FR-026).
"""

from __future__ import annotations

import re
import sqlite3
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal, NamedTuple, cast

from idfkit._derived import get_or_build_stamped
from idfkit._graph_common import MAX_EXAMPLES, Coverage, ObjectKey, UncoveredPart

from .parsers.err_catalog import classify_message

if TYPE_CHECKING:
    from idfkit.document import IDFDocument
    from idfkit.objects import IDFObject
    from idfkit.schema import EpJSONSchema

    from .parsers.sql import SQLResult, VariableInfo
    from .result import SimulationResult

__all__ = [
    "Confidence",
    "LinkedMessage",
    "ObjectNeighbour",
    "ObjectResults",
    "Resolution",
    "ResolutionRule",
    "ResultFact",
    "ResultIndex",
    "ResultSource",
]

Confidence = Literal["exact", "typed", "convention", "weak"]
"""How much to trust a link: by type and name, by name and context, by naming convention, or by substring."""

ResolutionRule = Literal[
    "exact",
    "typed",
    "zonelist_composite",
    "space_to_zone",
    "mirrored_shading",
    "aggregate",
    "ideal_loads_suffix",
    "ems_key",
    "substring",
    "unresolved",
]
"""The resolver rule that produced a link, or ``"unresolved"`` when none did."""

ResultSource = Literal["sizing", "tabular", "timeseries_stat"]
"""Where a result fact comes from."""

MessageSeverity = Literal["info", "warning", "severe", "fatal"]

ResultItemSource = Literal["sizing", "tabular", "timeseries", "message"]
"""What kind of result item a raw key came from, as recorded in :attr:`ResultIndex.unresolved`."""

_MAX_NEIGHBOURS = 20


# --------------------------------------------------------------------------------------------------
# Public records
# --------------------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Resolution:
    """One link from a raw result key to a model object, node or aggregate.

    Attributes:
        key: The object linked to, in the model's spelling. ``None`` means unresolved.
        rule: The resolver rule that found it.
        confidence: ``"exact"`` (type and name), ``"typed"`` (name, type from context),
            ``"convention"`` (a naming convention) or ``"weak"`` (a substring match, or a name shared
            by several types that the context could not tell apart). ``substring`` is always
            ``weak``; ``ems_key`` is always ``convention``.
        via: Other objects the link passes through. A zone-list composite links to the load object
            and names the zone here.
    """

    key: ObjectKey | None
    rule: ResolutionRule
    confidence: Confidence
    via: tuple[ObjectKey, ...] = ()


@dataclass(frozen=True, slots=True)
class ResultFact:
    """One value EnergyPlus reported for an object.

    Attributes:
        source: ``"sizing"`` (``ComponentSizes``), ``"tabular"`` (a tabular report cell) or
            ``"timeseries_stat"`` (a statistic of a series).
        metric: Snake-case name with units, such as ``design_size_nominal_capacity_w``.
        value: The value: a number when the cell holds one, otherwise its text.
        units: The units EnergyPlus gave, or ``None``.
        where: Where it was read: ``Report/Table/Row/Column`` or ``ComponentSizes#<index>``.
        multiplier: For a zone fact, the zone's multiplier times its list multiplier. The value is
            per zone instance; multiply before adding zone rows into a total. ``None`` for other
            objects.
    """

    source: ResultSource
    metric: str
    value: float | str | None
    units: str | None
    where: str
    multiplier: int | None = None


@dataclass(frozen=True, slots=True)
class LinkedMessage:
    """One EnergyPlus error or warning, with the objects it names.

    Attributes:
        severity: ``"info"``, ``"warning"``, ``"severe"`` or ``"fatal"``, from the ``Errors`` table.
        kind: The message catalogue id, or ``"other"`` when no catalogue entry matches.
        text: The first line of the message. The rest is in the run's ERR file.
        objects: The objects the message names, resolved.
        occurrences: How many times EnergyPlus reported it. For one object's messages, the total
            over the messages of the same kind.
        first_seen: ``"<environment> MM/DD HH:MM"`` when EnergyPlus reported when it first occurred.
    """

    severity: MessageSeverity
    kind: str
    text: str
    objects: tuple[Resolution, ...]
    occurrences: int
    first_seen: str | None = None


@dataclass(frozen=True, slots=True)
class ObjectNeighbour:
    """An object one hop away, with its first result fact.

    Attributes:
        object: The neighbour.
        top_fact: Its first fact, sizing before tabular, or ``None`` when it has none.
    """

    object: ObjectKey
    top_fact: ResultFact | None


@dataclass(frozen=True, slots=True)
class ObjectResults:
    """Everything one run reported about one object.

    Attributes:
        object: The object, or node, asked about.
        facts: Its facts, sizing first, in table order.
        messages: The messages naming it, one per kind, with occurrences summed.
        available_variables: The output variables recorded for it, sorted. Values are not read;
            fetch one with :meth:`SQLResult.get_timeseries`.
        neighbours: Objects one hop away over the HVAC topology or the reference graph, at most 20.
        coverage: What the index could not link.
    """

    object: ObjectKey
    facts: tuple[ResultFact, ...]
    messages: tuple[LinkedMessage, ...]
    available_variables: tuple[str, ...]
    neighbours: tuple[ObjectNeighbour, ...]
    coverage: Coverage


# --------------------------------------------------------------------------------------------------
# The model side: names, nodes and families
# --------------------------------------------------------------------------------------------------


class _Context(NamedTuple):
    """Where a raw key was found: the item source and a hint naming or suggesting its type."""

    source: ResultItemSource
    hint: str


_NODE = "Node"
_AGGREGATE = "Aggregate"

# Keyword in a variable name, table name or message type → type-name prefixes it suggests, most
# specific first. A type matches a prefix when its upper-case name starts with it.
_FAMILIES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("SYSTEM NODE", (_NODE.upper(),)),
    ("NODE", (_NODE.upper(),)),
    ("ZONE IDEAL LOADS", ("ZONEHVAC:IDEALLOADSAIRSYSTEM",)),
    ("AIR TERMINAL", ("AIRTERMINAL:",)),
    ("TERMINAL", ("AIRTERMINAL:",)),
    ("HEATING COIL", ("COIL:HEATING", "COIL:")),
    ("COOLING COIL", ("COIL:COOLING", "COIL:")),
    ("COIL", ("COIL:",)),
    ("FAN", ("FAN:",)),
    ("PUMP", ("PUMP:", "HEADEREDPUMPS:")),
    ("BOILER", ("BOILER:",)),
    ("CHILLER", ("CHILLER:", "CHILLERHEATER:")),
    ("COOLING TOWER", ("COOLINGTOWER:",)),
    ("EVAPORATIVE COOLER", ("EVAPORATIVECOOLER:",)),
    ("WATER HEATER", ("WATERHEATER:",)),
    ("WATERUSE CONNECTIONS", ("WATERUSE:CONNECTIONS",)),
    ("WATER USE CONNECTIONS", ("WATERUSE:CONNECTIONS",)),
    ("WATER USE", ("WATERUSE:",)),
    ("WATERUSE", ("WATERUSE:",)),
    ("PLANT", ("PLANTLOOP", "CONDENSERLOOP")),
    ("CONDENSER", ("CONDENSERLOOP",)),
    ("AIR SYSTEM", ("AIRLOOPHVAC",)),
    ("AIRLOOP", ("AIRLOOPHVAC",)),
    ("AIR LOOP", ("AIRLOOPHVAC",)),
    ("UNITARY", ("AIRLOOPHVAC:UNITARY",)),
    ("PEOPLE", ("PEOPLE",)),
    ("LIGHTS", ("LIGHTS",)),
    ("LIGHTING", ("LIGHTS", "DAYLIGHTING:")),
    ("ELECTRIC EQUIPMENT", ("ELECTRICEQUIPMENT",)),
    ("GAS EQUIPMENT", ("GASEQUIPMENT",)),
    ("HOT WATER EQUIPMENT", ("HOTWATEREQUIPMENT",)),
    ("INFILTRATION", ("ZONEINFILTRATION:",)),
    ("VENTILATION", ("ZONEVENTILATION:",)),
    ("PHOTOVOLTAIC", ("GENERATOR:PHOTOVOLTAIC", "SOLARCOLLECTOR:")),
    ("GENERATOR", ("GENERATOR:",)),
    ("INVERTER", ("ELECTRICLOADCENTER:INVERTER:",)),
    ("SOLAR COLLECTOR", ("SOLARCOLLECTOR:",)),
    ("WINDOW", ("FENESTRATIONSURFACE:", "WINDOW", "GLAZEDDOOR")),
    ("FENESTRATION", ("FENESTRATIONSURFACE:", "WINDOW", "GLAZEDDOOR", "DOOR")),
    ("SURFACE", ("BUILDINGSURFACE:", "FENESTRATIONSURFACE:", "WALL:", "ROOF", "FLOOR:", "CEILING:", "SHADING:")),
    ("OPAQUE", ("BUILDINGSURFACE:", "WALL:", "ROOF", "FLOOR:", "CEILING:", "DOOR")),
    ("ENVELOPE", ("BUILDINGSURFACE:", "FENESTRATIONSURFACE:", "WALL:", "ROOF", "FLOOR:", "CEILING:")),
    ("SHADING", ("SHADING:",)),
    ("INTERNAL MASS", ("INTERNALMASS",)),
    ("CONSTRUCTION", ("CONSTRUCTION",)),
    ("SCHEDULE", ("SCHEDULE:",)),
    ("SETPOINT MANAGER", ("SETPOINTMANAGER:",)),
    ("SPACE", ("SPACE",)),
    ("ZONE", ("ZONE", "SPACE")),
)

# When a name is shared by several types and the context names none of them, report rows and keys
# are, by EnergyPlus convention, keyed by the zone or the loop rather than by an object named after it.
_ROW_PREFERENCE: tuple[str, ...] = ("ZONE", "SPACE", "AIRLOOPHVAC", "PLANTLOOP", "CONDENSERLOOP")

_AGGREGATES: frozenset[str] = frozenset({
    "TOTAL",
    "TOTALS",
    "TOTAL FACILITY",
    "TOTAL BUILDING",
    "TOTAL HVAC",
    "CONDITIONED TOTAL",
    "UNCONDITIONED TOTAL",
    "NOT PART OF TOTAL",
    "WHOLE BUILDING",
    "FACILITY",
    "BUILDING",
    "ENVIRONMENT",
    "SIMHVAC",
    "SUM",
    "AVERAGE",
    "MINIMUM",
    "MAXIMUM",
    "MIN",
    "MAX",
    "SUM OR AVERAGE",
    "NONE",
    "NOTINCLUDED",
    "OTHER",
    "ELECTRIC LOAD CENTER",
})

_IDEAL_SUFFIXES: tuple[str, ...] = (" IDEAL LOADS AIR SYSTEM", " IDEAL LOADS AIR", "_IDEALAIR", " IDEALAIR")
_SPACE_SUFFIXES: tuple[str, ...] = ("_SPACE", " SPACE")
_MIN_SUBSTRING = 4
_FIRST_SEEN = re.compile(r"Environment=([^,]+?),\s*at Simulation time=(\d\d/\d\d \d\d:\d\d)")
_SNAKE = re.compile(r"[^0-9a-z]+")
_NUMBER = re.compile(r"^\s*[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?\s*$")


def _family(hint: str) -> tuple[str, ...]:
    """The type-name prefixes of the first family a variable name, table name or message type names, or ``()``."""
    upper = hint.upper()
    for keyword, prefixes in _FAMILIES:
        if keyword in upper:
            return prefixes
    return ()


def _families(hint: str) -> tuple[str, ...]:
    """The type-name prefixes of every family *hint* names, in family order."""
    upper = hint.upper()
    return tuple(prefix for keyword, prefixes in _FAMILIES if keyword in upper for prefix in prefixes)


def _in_family(obj_type: str, prefixes: tuple[str, ...]) -> bool:
    upper = obj_type.upper()
    return any(upper.startswith(prefix) for prefix in prefixes)


def _objects(doc: IDFDocument, obj_type: str) -> list[IDFObject]:
    """The objects of one type, or ``[]`` when the document has none."""
    collection = doc.collections.get(obj_type)
    return list(collection) if collection is not None else []


class _Model:
    """The document's names, nodes and zones, upper-cased once for linking."""

    __slots__ = (
        "_substring_names",
        "ems_outputs",
        "ideal_loads",
        "names",
        "schema",
        "spelling",
        "templates",
        "type_spelling",
        "zone_of_space",
        "zones",
    )

    def __init__(self, doc: IDFDocument) -> None:
        from idfkit.hvac import HVACTopology

        names: dict[str, list[str]] = {}
        spelling: dict[tuple[str, str], str] = {}
        type_spelling: dict[str, str] = {_NODE.upper(): _NODE}
        for obj_type, collection in doc.collections.items():
            type_upper = obj_type.upper()
            type_spelling[type_upper] = obj_type
            for obj in collection:
                if obj.name:
                    name_upper = obj.name.upper()
                    names.setdefault(name_upper, []).append(obj_type)
                    spelling[(type_upper, name_upper)] = obj.name
        for node in HVACTopology.from_document(doc).nodes():
            node_upper = node.upper()
            names.setdefault(node_upper, []).append(_NODE)
            spelling[(_NODE.upper(), node_upper)] = node
        self.schema = doc.schema
        self.names = names
        self.spelling = spelling
        self.type_spelling = type_spelling
        self.zones = {obj.name.upper(): obj.name for obj in _objects(doc, "Zone") if obj.name}
        self.zone_of_space = {
            obj.name.upper(): zone
            for obj in _objects(doc, "Space")
            if obj.name and isinstance(zone := obj.data.get("zone_name"), str) and zone
        }
        self.ems_outputs = {
            obj.name.upper(): obj.name for obj in _objects(doc, "EnergyManagementSystem:OutputVariable") if obj.name
        }
        self.ideal_loads = {
            zone.upper(): obj.name or zone
            for obj in _objects(doc, "HVACTemplate:Zone:IdealLoadsAirSystem")
            if isinstance(zone := obj.data.get("zone_name"), str) and zone
        }
        self.templates = tuple(
            ObjectKey(obj_type, obj.name or obj_type)
            for obj_type, collection in doc.collections.items()
            if obj_type.upper().startswith("HVACTEMPLATE:")
            for obj in collection
        )
        self._substring_names: list[str] | None = None

    def key(self, obj_type: str, name_upper: str) -> ObjectKey:
        """The key of a known object, in the model's spelling."""
        type_upper = obj_type.upper()
        return ObjectKey(
            self.type_spelling.get(type_upper, obj_type),
            self.spelling.get((type_upper, name_upper), name_upper),
        )

    def pick(self, name_upper: str, hint: str) -> tuple[str, Confidence] | None:
        """The type of a known name, narrowed by *hint*, with how sure the choice is."""
        types = self.names.get(name_upper)
        if not types:
            return None
        if len(types) == 1:
            return types[0], "typed"
        for prefix in _families(hint):
            for obj_type in types:
                if obj_type.upper().startswith(prefix):
                    return obj_type, "typed"
        for preferred in _ROW_PREFERENCE:
            for obj_type in types:
                if obj_type.upper() == preferred:
                    return obj_type, "convention"
        return types[0], "weak"

    def substring_names(self) -> list[str]:
        """Every object name long enough to search for inside a key, longest first."""
        if self._substring_names is None:
            self._substring_names = sorted(
                (name for name in self.names if len(name) >= _MIN_SUBSTRING), key=len, reverse=True
            )
        return self._substring_names


# --------------------------------------------------------------------------------------------------
# The resolver chain: (raw key, context, model) -> Resolution | None
# --------------------------------------------------------------------------------------------------


def _exact(raw: str, ctx: _Context, model: _Model) -> Resolution | None:
    type_upper = ctx.hint.upper()
    name_upper = raw.upper()
    if (type_upper, name_upper) in model.spelling:
        return Resolution(model.key(type_upper, name_upper), "exact", "exact")
    return None


def _typed(raw: str, ctx: _Context, model: _Model) -> Resolution | None:
    name_upper = raw.upper()
    picked = model.pick(name_upper, ctx.hint)
    if picked is None:
        return None
    obj_type, confidence = picked
    named_type = _named_type(ctx.hint, model)
    if named_type is not None and obj_type.upper() != named_type:
        # The source names a type and the name belongs to another one. Only the template an object
        # was expanded from is the same thing, by convention; anything else is a different object.
        if not obj_type.upper().startswith("HVACTEMPLATE:"):
            return None
        confidence = "convention"
    elif obj_type.upper().startswith("HVACTEMPLATE:") and not ctx.hint.upper().startswith("HVACTEMPLATE:"):
        confidence = "convention"
    others = tuple(model.key(t, name_upper) for t in model.names[name_upper] if t != obj_type)
    return Resolution(model.key(obj_type, name_upper), "typed", confidence, others if confidence == "weak" else ())


def _named_type(hint: str, model: _Model) -> str | None:
    """The upper-case type *hint* names exactly (a sizing ``CompType``, a message ``Type=``), or ``None``."""
    upper = hint.strip().upper()
    if upper in model.type_spelling or upper in _schema_types(model.schema):
        return upper
    return None


_SCHEMA_TYPES: dict[int, frozenset[str]] = {}


def _schema_types(schema: EpJSONSchema | None) -> frozenset[str]:
    """Every object type of *schema*, upper-cased, computed once per schema."""
    if schema is None:
        return frozenset()
    held = _SCHEMA_TYPES.get(id(schema))
    if held is None:
        held = frozenset(t.upper() for t in schema.object_types)
        _SCHEMA_TYPES[id(schema)] = held
    return held


def _zonelist_composite(raw: str, ctx: _Context, model: _Model) -> Resolution | None:
    upper = raw.upper()
    start = upper.find(" ")
    while start != -1:
        prefix, rest = upper[:start], upper[start + 1 :]
        zone_upper = prefix if prefix in model.zones else None
        if zone_upper is None and prefix in model.zone_of_space:
            zone_upper = prefix
        if zone_upper is not None:
            picked = model.pick(rest, ctx.hint)
            if picked is not None:
                zone_type = "Zone" if prefix in model.zones else "Space"
                confidence: Confidence = "weak" if picked[1] == "weak" else "convention"
                return Resolution(
                    model.key(picked[0], rest), "zonelist_composite", confidence, (model.key(zone_type, prefix),)
                )
        start = upper.find(" ", start + 1)
    return None


def _space_to_zone(raw: str, ctx: _Context, model: _Model) -> Resolution | None:
    upper = raw.upper()
    for suffix in _SPACE_SUFFIXES:
        if upper.endswith(suffix) and upper[: -len(suffix)] in model.zones:
            return Resolution(model.key("Zone", upper[: -len(suffix)]), "space_to_zone", "convention")
    return None


def _mirrored_shading(raw: str, ctx: _Context, model: _Model) -> Resolution | None:
    upper = raw.upper()
    if not upper.startswith("MIR-"):
        return None
    picked = model.pick(upper[4:], "SURFACE")
    if picked is None:
        return None
    return Resolution(model.key(picked[0], upper[4:]), "mirrored_shading", "convention")


def _aggregate(raw: str, ctx: _Context, model: _Model) -> Resolution | None:
    upper = raw.strip().upper()
    if upper in _AGGREGATES or upper.startswith("TOTAL ") or upper.endswith((" TOTAL", " TOTAL OR AVERAGE")):
        return Resolution(ObjectKey(_AGGREGATE, raw.strip()), "aggregate", "convention")
    return None


def _ideal_loads_suffix(raw: str, ctx: _Context, model: _Model) -> Resolution | None:
    upper = raw.upper()
    for suffix in _IDEAL_SUFFIXES:
        if upper.endswith(suffix):
            zone_upper = upper[: -len(suffix)]
            if zone_upper not in model.zones:
                return None
            zone = model.key("Zone", zone_upper)
            template = model.ideal_loads.get(zone_upper)
            if template is not None:
                key = model.key("HVACTemplate:Zone:IdealLoadsAirSystem", template.upper())
                return Resolution(key, "ideal_loads_suffix", "convention", (zone,))
            return Resolution(zone, "ideal_loads_suffix", "convention")
    return None


def _ems_key(raw: str, ctx: _Context, model: _Model) -> Resolution | None:
    hint_upper = ctx.hint.upper()
    if raw.strip().upper() == "EMS" and hint_upper in model.ems_outputs:
        return Resolution(model.key("EnergyManagementSystem:OutputVariable", hint_upper), "ems_key", "convention")
    return None


def _substring(raw: str, ctx: _Context, model: _Model) -> Resolution | None:
    upper = raw.upper()
    family = _family(ctx.hint)
    for name_upper in model.substring_names():
        at = upper.find(name_upper)
        if at == -1:
            continue
        end = at + len(name_upper)
        if (at == 0 or not upper[at - 1].isalnum()) and (end == len(upper) or not upper[end].isalnum()):
            picked = model.pick(name_upper, ctx.hint)
            if picked is not None and (not family or _in_family(picked[0], family)):
                return Resolution(model.key(picked[0], name_upper), "substring", "weak")
    return None


_Rule = Callable[[str, _Context, _Model], "Resolution | None"]

RESOLVERS: tuple[_Rule, ...] = (
    _exact,
    _typed,
    _zonelist_composite,
    _space_to_zone,
    _mirrored_shading,
    _aggregate,
    _ideal_loads_suffix,
    _ems_key,
    _substring,
)
"""The resolver chain, in the order it is tried."""


def _resolve(raw: str, ctx: _Context, model: _Model, *, substring: bool = True) -> Resolution | None:
    if not raw.strip():
        return None
    for rule in RESOLVERS:
        if rule is _substring and not substring:
            return None
        found = rule(raw, ctx, model)
        if found is not None:
            return found
    return None


# --------------------------------------------------------------------------------------------------
# The index
# --------------------------------------------------------------------------------------------------


def _metric(text: str, units: str | None) -> str:
    """``"Design Size Nominal Capacity", "W"`` → ``"design_size_nominal_capacity_w"``."""
    label = f"{text} {units}" if units else text
    return _SNAKE.sub("_", label.lower()).strip("_")


def _cell_value(value: str) -> float | str | None:
    stripped = value.strip()
    if not stripped:
        return None
    if _NUMBER.match(stripped):
        return float(stripped)
    return stripped


def _first_line(message: str) -> str:
    line = message.split("\n", 1)[0]
    return line.split("  ", 1)[0].strip()


def _first_seen(message: str) -> str | None:
    match = _FIRST_SEEN.search(message)
    if match is None:
        return None
    return f"{match.group(1).strip()} {match.group(2)}"


_SEVERITY_RANK: dict[str, int] = {"info": 0, "warning": 1, "severe": 2, "fatal": 3}

_FactRow = tuple[ResultSource, str, float | str | None, str | None, str]
"""(source, metric, value, units, where); the multiplier is added when facts are returned."""


@dataclass(slots=True)
class _Tally:
    resolved: int = 0
    resolved_by: dict[str, int] = field(default_factory=dict[str, int])
    links: dict[ObjectKey, Resolution] = field(default_factory=dict[ObjectKey, Resolution])
    unresolved: list[tuple[ResultItemSource, str]] = field(default_factory=list[tuple["ResultItemSource", str]])


class ResultIndex:
    """One simulation run's results, linked to the objects of the document that was simulated.

    Build it with :meth:`build`. The index holds the links and a small number of values (sizing
    rows and the cells of object rows in tabular reports); timeseries are recorded by key only.

    Attributes:
        run_revision: The document revision that was simulated.
        run_model_hash: The hash of the model text that was simulated, as given to :meth:`build`.
        messages: Every warning, severe and fatal message of the run, linked.
        unresolved: ``(source, raw key)`` for every result item no rule could link.

    Examples:
        ```python
        from idfkit.simulation import ObjectKey, ResultIndex, simulate

        result = simulate(model, "weather.epw")
        index = ResultIndex.build(model, result, run_revision=model.revision, run_model_hash="")
        for fact in index.for_object(ObjectKey("Coil:Heating:Water", "SPACE1-1 Zone Coil")).facts:
            print(fact.metric, fact.value, fact.units)
        ```
    """

    __slots__ = (
        "_doc",
        "_facts",
        "_message_index",
        "_multipliers",
        "_series",
        "_tally",
        "_uncovered",
        "messages",
        "run_model_hash",
        "run_revision",
        "unresolved",
    )

    def __init__(
        self,
        doc: IDFDocument,
        *,
        facts: dict[ObjectKey, list[_FactRow]],
        series: dict[ObjectKey, list[str]],
        messages: list[LinkedMessage],
        multipliers: dict[str, int],
        tally: _Tally,
        uncovered: tuple[UncoveredPart, ...],
        run_revision: int,
        run_model_hash: str,
    ) -> None:
        self._doc = doc
        self._facts = facts
        self._series = series
        self._multipliers = multipliers
        self._tally = tally
        self._uncovered = uncovered
        self.messages = tuple(messages)
        self.unresolved = tuple(tally.unresolved)
        self.run_revision = run_revision
        self.run_model_hash = run_model_hash
        message_index: dict[ObjectKey, list[int]] = {}
        for position, message in enumerate(self.messages):
            for link in message.objects:
                if link.key is not None:
                    message_index.setdefault(link.key, []).append(position)
        self._message_index = message_index

    # ---------------------------------------------------------------- building

    @classmethod
    def build(
        cls, doc: IDFDocument, result: SimulationResult, *, run_revision: int, run_model_hash: str
    ) -> ResultIndex:
        """Link a run's SQLite output to *doc*.

        The index is cached on the document for this run: a second call with the same run, revision
        and hash returns it without reading the database again.

        Args:
            doc: The document that was simulated. Linking reads its names as they are now; build
                right after the run, before editing.
            result: The run. It must have SQLite output (``Output:SQLite``).
            run_revision: ``doc.revision`` when the model was written for EnergyPlus.
            run_model_hash: A hash of the model text EnergyPlus ran, used by :meth:`is_fresh`.

        Returns:
            The index.

        Raises:
            ValueError: If the run has no SQLite output.
        """
        stamp = (str(result.run_dir), run_revision, run_model_hash)
        return get_or_build_stamped(
            doc, "results", stamp, lambda: cls._build(doc, result, run_revision, run_model_hash)
        )

    @classmethod
    def _build(cls, doc: IDFDocument, result: SimulationResult, run_revision: int, run_model_hash: str) -> ResultIndex:
        sql = result.sql
        if sql is None:
            msg = f"The run in {result.run_dir} has no SQLite output; add Output:SQLite to link its results"
            raise ValueError(msg)
        model = _Model(doc)
        tally = _Tally()
        facts: dict[ObjectKey, list[_FactRow]] = {}
        series: dict[ObjectKey, list[str]] = {}

        multipliers = {row.name.upper(): row.multiplier * row.list_multiplier for row in sql.zones()}
        _link_sizing(sql, model, facts, tally)
        _link_series(sql.report_keys(), model, series, tally)
        _link_tabular(sql, model, facts, tally)
        messages = _link_messages(sql, model, tally)

        uncovered: list[UncoveredPart] = []
        if tally.unresolved:
            examples = tuple(ObjectKey("Unresolved", raw) for _, raw in tally.unresolved[:MAX_EXAMPLES])
            uncovered.append(
                UncoveredPart(
                    "unlinked_result",
                    len(tally.unresolved),
                    examples,
                    "These result items name nothing in the model by any rule; they are listed in unresolved.",
                )
            )
        if model.templates:
            uncovered.append(
                UncoveredPart(
                    "hvac_template",
                    len(model.templates),
                    model.templates[:MAX_EXAMPLES],
                    "Objects EnergyPlus expanded from HVACTemplate objects are not in the model; "
                    "their results link only by naming convention or not at all.",
                )
            )
        return cls(
            doc,
            facts=facts,
            series=series,
            messages=messages,
            multipliers=multipliers,
            tally=tally,
            uncovered=tuple(uncovered),
            run_revision=run_revision,
            run_model_hash=run_model_hash,
        )

    # ---------------------------------------------------------------- queries

    @property
    def coverage(self) -> Coverage:
        """What the index linked and what it did not: ``resolved`` and ``unresolved`` count result items."""
        return Coverage.of(self._uncovered, resolved=self._tally.resolved, unresolved=len(self._tally.unresolved))

    @property
    def keys(self) -> frozenset[ObjectKey]:
        """Every object, node and aggregate that has a fact, a series or a message."""
        return frozenset(self._facts) | frozenset(self._series) | frozenset(self._message_index)

    def facts(self, key: ObjectKey) -> tuple[ResultFact, ...]:
        """The facts of one object, sizing first, in table order. Zone facts carry the multiplier."""
        multiplier = self._multipliers.get(key.name.upper()) if key.object_type.upper() == "ZONE" else None
        if key.object_type.upper() == "ZONE" and multiplier is None:
            multiplier = 1
        return tuple(
            ResultFact(source, metric, value, units, where, multiplier)
            for source, metric, value, units, where in self._facts.get(key, ())
        )

    def link(self, key: ObjectKey) -> Resolution | None:
        """How the results of one object were linked to it: the first link that named it, or ``None``."""
        return self._tally.links.get(key)

    def variables(self, key: ObjectKey) -> tuple[str, ...]:
        """The output variables recorded for one key, sorted, without their values."""
        return tuple(sorted(set(self._series.get(key, ()))))

    def messages_for(self, key: ObjectKey) -> tuple[LinkedMessage, ...]:
        """The messages naming one object, one per kind, most severe first, occurrences summed."""
        merged: dict[str, LinkedMessage] = {}
        for position in self._message_index.get(key, ()):
            message = self.messages[position]
            held = merged.get(message.kind)
            if held is None:
                merged[message.kind] = message
                continue
            severity = (
                held.severity if _SEVERITY_RANK[held.severity] >= _SEVERITY_RANK[message.severity] else message.severity
            )
            merged[message.kind] = LinkedMessage(
                severity,
                held.kind,
                held.text,
                held.objects,
                held.occurrences + message.occurrences,
                held.first_seen or message.first_seen,
            )
        return tuple(sorted(merged.values(), key=lambda m: -_SEVERITY_RANK[m.severity]))

    def for_object(self, key: ObjectKey) -> ObjectResults:
        """Everything the run reported about one object or node (FR-024).

        Args:
            key: The object, or ``ObjectKey("Node", name)`` for a fluid node. Matched case-insensitively.

        Returns:
            Its facts, messages deduplicated by kind, recorded variables and neighbours. All empty
            when the run reported nothing for it.
        """
        return ObjectResults(
            object=self._spelled(key),
            facts=self.facts(key),
            messages=self.messages_for(key),
            available_variables=self.variables(key),
            neighbours=self._neighbours(key),
            coverage=self.coverage,
        )

    def objects_with(self, metric: str, *, top: int = 10) -> list[tuple[ObjectKey, ResultFact]]:
        """The objects with the largest numeric values of one metric, largest first.

        Args:
            metric: A fact metric, such as ``design_size_nominal_capacity_w``.
            top: The most pairs returned.

        Returns:
            ``(object, fact)`` pairs. Values are per instance; zone facts carry their multiplier.
        """
        found: list[tuple[float, ObjectKey, ResultFact]] = []
        for key, rows in self._facts.items():
            for row in rows:
                if row[1] == metric and isinstance(row[2], float):
                    fact = next(f for f in self.facts(key) if f.where == row[4])
                    found.append((row[2], key, fact))
        found.sort(key=lambda item: -item[0])
        return [(key, fact) for _, key, fact in found[:top]]

    def is_fresh(self, doc: IDFDocument, model_hash: str | None = None) -> bool:
        """Whether *doc* is still the model this run simulated (FR-026).

        Args:
            doc: The document now.
            model_hash: The hash of its model text now, when the caller has one. Without it only the
                revision is compared.

        Returns:
            ``True`` when the revision, and the hash if given, equal those of the run.
        """
        if doc.revision != self.run_revision:
            return False
        return model_hash is None or model_hash == self.run_model_hash

    # ---------------------------------------------------------------- helpers

    def _spelled(self, key: ObjectKey) -> ObjectKey:
        for held in (self._facts, self._series, self._message_index):
            for candidate in held:
                if candidate == key:
                    return candidate
        return key

    def _top_fact(self, key: ObjectKey) -> ResultFact | None:
        facts = self.facts(key)
        return facts[0] if facts else None

    def _neighbours(self, key: ObjectKey) -> tuple[ObjectNeighbour, ...]:
        from idfkit.graph import ModelGraph

        graph = ModelGraph(self._doc)
        start: ObjectKey | str = key.name if key.object_type.upper() == _NODE.upper() else key
        try:
            sub = graph.neighbourhood(start, hops=1, max_nodes=_MAX_NEIGHBOURS + 1)
        except KeyError:
            return ()
        found: list[ObjectNeighbour] = []
        for node in sub.nodes:
            if node.key is not None:
                neighbour = node.key
            elif node.node is not None:
                neighbour = ObjectKey(_NODE, node.node)
            else:
                continue
            if neighbour == key:
                continue
            found.append(ObjectNeighbour(neighbour, self._top_fact(neighbour)))
        return tuple(found[:_MAX_NEIGHBOURS])


# --------------------------------------------------------------------------------------------------
# Linking each source
# --------------------------------------------------------------------------------------------------


def _record(tally: _Tally, source: ResultItemSource, raw: str, found: Resolution | None) -> ObjectKey | None:
    if found is None or found.key is None:
        tally.unresolved.append((source, raw))
        return None
    tally.resolved += 1
    tally.resolved_by[source] = tally.resolved_by.get(source, 0) + 1
    tally.links.setdefault(found.key, found)
    return found.key


def _link_sizing(sql: SQLResult, model: _Model, facts: dict[ObjectKey, list[_FactRow]], tally: _Tally) -> None:
    cache: dict[tuple[str, str], ObjectKey | None] = {}
    for row in sql.component_sizes():
        pair = (row.component_type.upper(), row.component_name.upper())
        if pair in cache:
            key = cache[pair]
            if key is None:
                tally.unresolved.append(("sizing", row.component_name))
            else:
                tally.resolved += 1
                tally.resolved_by["sizing"] = tally.resolved_by.get("sizing", 0) + 1
        else:
            found = _resolve(row.component_name, _Context("sizing", row.component_type), model, substring=False)
            key = _record(tally, "sizing", row.component_name, found)
            cache[pair] = key
        if key is not None:
            units = row.units or None
            facts.setdefault(key, []).append((
                "sizing",
                _metric(row.description, units),
                row.value,
                units,
                f"ComponentSizes#{row.index}",
            ))


def _link_series(
    keys: Iterable[VariableInfo], model: _Model, series: dict[ObjectKey, list[str]], tally: _Tally
) -> None:
    seen: dict[str, ObjectKey | None] = {}
    for info in keys:
        if info.is_meter or not info.key_value:
            continue
        cache_key = f"{info.key_value.upper()}\x00{_family(info.name)}"
        if cache_key in seen:
            key = seen[cache_key]
        else:
            found = _resolve(info.key_value, _Context("timeseries", info.name), model)
            key = _record(tally, "timeseries", info.key_value, found)
            seen[cache_key] = key
        if key is not None:
            series.setdefault(key, []).append(info.name)


def _ids(rows: list[tuple[object, ...]]) -> list[tuple[int, ...]]:
    """Rows of ``*Index`` columns, which SQLite returns as ``int``: typed without converting each cell."""
    return cast("list[tuple[int, ...]]", rows)


_Triple = tuple[int, int, int]


def _object_rows(
    strings: dict[int, str], rows: list[tuple[object, ...]], model: _Model, tally: _Tally
) -> dict[_Triple, ObjectKey]:
    """Link the rows of every object-keyed table, keyed by ``(report, table, row)`` string ids.

    A table is object-keyed when at least half of its distinct row labels link to an object or are
    aggregates, and not all of them are aggregates. Only those tables count; their unlinked rows are
    listed as unresolved.
    """
    tables: dict[tuple[int, int], list[int]] = {}
    for report, table, row in _ids(rows):
        tables.setdefault((report, table), []).append(row)
    linked: dict[_Triple, ObjectKey] = {}
    for (report, table), row_ids in tables.items():
        if strings.get(report) == "ComponentSizingSummary":
            # Its tables repeat ComponentSizes, which the sizing source already links.
            continue
        context = _Context("tabular", strings.get(table, ""))
        results = [
            (row_id, strings.get(row_id, ""), _resolve(strings.get(row_id, ""), context, model, substring=False))
            for row_id in row_ids
        ]
        found_rules = [found.rule for _, _, found in results if found is not None]
        if len(found_rules) * 2 < len(row_ids) or all(rule == "aggregate" for rule in found_rules):
            continue
        for row_id, raw, found in results:
            key = _record(tally, "tabular", raw, found)
            if key is not None and found is not None and found.rule != "aggregate":
                linked[(report, table, row_id)] = key
    return linked


def _link_tabular(sql: SQLResult, model: _Model, facts: dict[ObjectKey, list[_FactRow]], tally: _Tally) -> None:
    """Link the object rows of tabular reports and read the cells of the linked rows only."""
    try:
        strings = {
            cast("int", index): str(value or "") for index, value in sql.query("SELECT StringIndex, Value FROM Strings")
        }
        rows = sql.query("SELECT DISTINCT ReportNameIndex, TableNameIndex, RowNameIndex FROM TabularData")
    except sqlite3.Error:
        return
    linked = _object_rows(strings, rows, model, tally)
    if not linked:
        return
    targets = {triple: facts.setdefault(key, []) for triple, key in linked.items()}
    row_ids = ",".join(str(row) for row in sorted({row for _, _, row in linked}))
    columns = "ReportNameIndex, TableNameIndex, RowNameIndex, ColumnNameIndex, UnitsIndex, Value"
    # The ids are integers read back from the database, never text from outside it.
    query = f"SELECT {columns} FROM TabularData WHERE RowNameIndex IN ({row_ids}) AND Value <> ''"  # noqa: S608
    cells = sql.query(query)
    described: dict[tuple[int, int], tuple[str, str | None, str]] = {}
    for report, table, row, column, units_id, value in cells:
        triple = cast("_Triple", (report, table, row))
        target = targets.get(triple)
        if target is None:
            continue
        cell = _cell_value(cast("str", value))
        if cell is None:
            continue
        column_key = cast("tuple[int, int]", (column, units_id))
        if column_key not in described:
            units = strings.get(column_key[1]) or None
            column_name = strings.get(column_key[0], "")
            described[column_key] = (_metric(column_name, units), units, column_name)
        metric, units, column_name = described[column_key]
        where = f"{strings.get(triple[0], '')}/{strings.get(triple[1], '')}/{strings.get(triple[2], '')}/{column_name}"
        target.append(("tabular", metric, cell, units, where))


def _link_messages(sql: SQLResult, model: _Model, tally: _Tally) -> list[LinkedMessage]:
    messages: list[LinkedMessage] = []
    for row in sql.errors():
        if row.severity == "info":
            continue
        kind, pairs = classify_message(row.message)
        links: list[Resolution] = []
        for obj_type, name in pairs:
            found = _resolve(name, _Context("message", obj_type or ""), model, substring=False)
            if _record(tally, "message", name, found) is not None and found is not None:
                links.append(found)
        if not pairs:
            found = _substring(_first_line(row.message), _Context("message", ""), model)
            if found is not None:
                links.append(found)
        messages.append(
            LinkedMessage(
                severity=row.severity,
                kind=kind.kind if kind is not None else "other",
                text=_first_line(row.message),
                objects=tuple(links),
                occurrences=max(row.count, 1),
                first_seen=_first_seen(row.message),
            )
        )
    return messages
