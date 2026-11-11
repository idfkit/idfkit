"""Generate ``idfkit.hvac._port_rules`` from EnergyPlus's own node connection report.

WHY GENERATED FROM ENERGYPLUS

The schema says *that* a field names a node, never *how* it connects. EnergyPlus decides that per
call site in C++ and reports it, for every node use of a run, in the branch-and-node file
``eplusout.bnd``: one ``Parent Node Connection`` or ``Non-Parent Node Connection`` row per use, with
the object, the node, the connection type and the fluid stream. That report is the only source of
truth for the rule table (research R-04). Field naming is a cross-check that never decides a role:
it misreads boundaries named as inlets, parents that pair perfectly by name, streams and
value-dependent roles.

THE SIX STEPS

1. Run every 26.2 example file, and each minimal model under ``port_rule_models/``, for design
   days only (``energyplus -D -x``), keeping ``eplusout.bnd`` and the expanded input.
2. Parse the parent and non-parent node connection rows, and the node fluid table.
3. Map each row back to a field by matching the node against that object's node fields, through
   ``NodeList``s where a field names one.
4. Merge across files. A field whose role differs between files becomes a predicate candidate for
   review; an object that uses the same node in two fields is an ambiguous match, also for review.
5. Cross-check every generated role against the field's name. A disagreement fails generation until
   a person has reviewed it and recorded the resolution in ``port_rule_overrides.toml``.
6. Write ``_port_rules.py``, with the provenance of every rule.

Fields EnergyPlus never reported in any run get a rule from their name, recorded as
``hand_written``; a finding that relies on one is never an error. Fields whose name says nothing
get no rule and are reported as unclassified at run time.

EnergyPlus is needed only to run this script, never at run time. ``--work-dir`` keeps the runs, so
review iterations re-read them instead of re-simulating.

Usage::

    python -m idfkit.codegen.generate_port_rules --energyplus /usr/local/EnergyPlus-26-2-0 \\
        --work-dir /tmp/port-rules [--jobs 4] [--report candidates.toml]
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from collections.abc import Iterable, Iterator, Mapping
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final, NamedTuple, cast

import tomllib

from idfkit.hvac._node_fields import NODE_FIELDS
from idfkit.hvac.types import ConnectionType, Fluid, Provenance

_HERE: Final = Path(__file__).resolve().parent
_OUTPUT_PATH: Final = _HERE.parent / "hvac" / "_port_rules.py"
_OVERRIDES_PATH: Final = _HERE / "port_rule_overrides.toml"
_TEST_MODELS_DIR: Final = _HERE / "port_rule_models"
_KEEP: Final = frozenset({"eplusout.bnd", "eplusout.err", "eplusout.expidf", "rc"})

# EnergyPlus 26.2 reports fifteen connection types; the public vocabulary has twelve.
_CONNECTION_MAP: Final[dict[str, ConnectionType | None]] = {
    "Inlet": ConnectionType.INLET,
    "Outlet": ConnectionType.OUTLET,
    "Internal": ConnectionType.INTERNAL,
    "ZoneNode": ConnectionType.ZONE_NODE,
    "Sensor": ConnectionType.SENSOR,
    "Actuator": ConnectionType.ACTUATOR,
    "OutdoorAir": ConnectionType.OUTSIDE_AIR,
    "OutsideAir": ConnectionType.OUTSIDE_AIR,
    "OutsideAirReference": ConnectionType.OUTSIDE_AIR,
    "ReliefAir": ConnectionType.RELIEF_AIR,
    "ZoneInlet": ConnectionType.ZONE_INLET,
    "ZoneReturn": ConnectionType.ZONE_RETURN,
    "ZoneExhaust": ConnectionType.ZONE_EXHAUST,
    "Setpoint": ConnectionType.SETPOINT,
    # Only a return plenum's induced-air outlet carries this: the plenum supplies that node to an
    # induction unit's secondary inlet, so it is a flow outlet.
    "InducedAir": ConnectionType.OUTLET,
    # Electric "nodes" are not fluid nodes.
    "Electric": None,
}

_FLUID_MAP: Final[dict[str, Fluid]] = {
    "AIR": Fluid.AIR,
    "WATER": Fluid.WATER,
    "STEAM": Fluid.STEAM,
    "REFRIGERANT": Fluid.REFRIGERANT,
}

_ROW = re.compile(r"^\s*(Parent|Non-Parent) Node Connection,(.*)$")
_NODE_ROW = re.compile(r"^\s*Node,\d+,(.*),([^,]*),\d+\s*$")


# --------------------------------------------------------------------------------------------- #
# Step 1: run EnergyPlus
# --------------------------------------------------------------------------------------------- #


def _run_one(args: tuple[str, str, str]) -> tuple[str, int]:
    """Run one model for design days only; keep only what the harvest reads."""
    energyplus, idf, out = args
    out_dir = Path(out)
    if (out_dir / "eplusout.bnd").exists():
        return idf, 0
    shutil.rmtree(out_dir, ignore_errors=True)
    out_dir.mkdir(parents=True)
    # Each run has its own working directory: ExpandObjects writes in.idf and GHTIn.idf into the
    # current directory, and parallel runs in a shared one collide.
    proc = subprocess.run(  # noqa: S603
        [energyplus, "-D", "-x", "-d", str(out_dir), idf],
        cwd=out_dir,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPYCACHEPREFIX": str(out_dir / "pycache")},
        capture_output=True,
        timeout=1800,
        check=False,
    )
    (out_dir / "rc").write_text(str(proc.returncode), encoding="utf-8")
    for path in out_dir.iterdir():
        if path.name not in _KEEP:
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
            else:
                path.unlink(missing_ok=True)
    return idf, proc.returncode


_BASE = re.compile(r"^!\s*base:\s*(\S+)\s*$", re.MULTILINE)


def assemble_test_model(patch: Path, example_dir: Path, out_dir: Path) -> Path:
    """Write the runnable form of one test model and return its path.

    A test model under ``port_rule_models/`` is a patch: a ``! base: <example>.idf`` line and the
    objects to append to that 26.2 example file. Appending keeps the committed files to the
    objects under test instead of a copy of a whole example.
    """
    text = patch.read_text(encoding="utf-8")
    match = _BASE.search(text)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / patch.name
    if match is None:
        target.write_text(text, encoding="utf-8")
    else:
        base = (example_dir / match.group(1)).read_text(encoding="latin-1")
        target.write_text(base + "\n" + text, encoding="latin-1")
    return target


def run_models(energyplus: Path, models: Iterable[Path], work_dir: Path, jobs: int) -> None:
    """Run each model into ``work_dir/<stem>``, skipping those already run."""
    exe = energyplus / "energyplus" if energyplus.is_dir() else energyplus
    tasks = [(str(exe), str(m), str(work_dir / m.stem)) for m in models]
    with ProcessPoolExecutor(max_workers=jobs) as pool:
        for idf, code in pool.map(_run_one, tasks):
            if code != 0:
                print(f"  run failed ({code}): {Path(idf).name}", file=sys.stderr)


# --------------------------------------------------------------------------------------------- #
# Step 2: parse eplusout.bnd
# --------------------------------------------------------------------------------------------- #


class BndRow(NamedTuple):
    parent: bool
    node: str
    object_type: str
    object_name: str
    connection: str
    stream: int


def parse_bnd(text: str) -> tuple[list[BndRow], dict[str, str]]:
    """Return the node connection rows and the node fluid table (upper-cased node name to fluid)."""
    rows: list[BndRow] = []
    fluids: dict[str, str] = {}
    for line in text.splitlines():
        m = _ROW.match(line)
        if m:
            # IDF values cannot contain commas, so a plain split is exact.
            parts = [p.strip() for p in m.group(2).split(",")]
            if len(parts) != 5:
                continue
            node, object_type, object_name, connection, stream = parts
            rows.append(
                BndRow(
                    m.group(1) == "Parent",
                    node.upper(),
                    object_type.upper(),
                    object_name.upper(),
                    connection,
                    int(stream) if stream.isdigit() else 1,
                )
            )
            continue
        n = _NODE_ROW.match(line)
        if n:
            fluids[n.group(1).strip().upper()] = n.group(2).strip().upper()
    return rows, fluids


# --------------------------------------------------------------------------------------------- #
# Step 3: map rows back to fields
# --------------------------------------------------------------------------------------------- #


class Observation(NamedTuple):
    object_type: str
    field: str
    connection: ConnectionType
    stream: int
    fluid: Fluid
    is_parent: bool
    via_nodelist: bool
    model: str
    values: tuple[tuple[str, str], ...]
    """The object's top-level string field values, for predicate inference."""


class Ambiguous(NamedTuple):
    object_type: str
    fields: tuple[str, ...]
    connection: ConnectionType
    model: str


@dataclass
class ModelHarvest:
    model: str
    observations: list[Observation] = field(default_factory=lambda: list[Observation]())
    ambiguous: list[Ambiguous] = field(default_factory=lambda: list[Ambiguous]())
    unmapped: Counter[str] = field(default_factory=lambda: Counter[str]())


def _node_values(obj_data: Mapping[str, Any], top: tuple[str, ...], ext: tuple[str, ...]) -> Iterator[tuple[str, str]]:
    """Yield ``(field, value)`` for every node field of one object, extensible ones as ``group.field``."""
    for name in top:
        value = obj_data.get(name)
        if isinstance(value, str) and value:
            yield name, value
    if ext:
        for group, items in obj_data.items():
            if not isinstance(items, list):
                continue
            for item in cast("list[Any]", items):
                if not isinstance(item, dict):
                    continue
                for name in ext:
                    value = cast("dict[str, Any]", item).get(name)
                    if isinstance(value, str) and value:
                        yield f"{group}.{name}", value


def _predicate_values(doc: Any, object_type: str, data: Mapping[str, Any]) -> tuple[tuple[str, str], ...]:
    """The object's top-level string values, with a blank choice field taking its schema default.

    A blank ``condenser_type`` means the default, and EnergyPlus decides the role from the effective
    value, so predicates are inferred over effective values too.
    """
    values = {k: str(v) for k, v in data.items() if isinstance(v, str) and v}
    schema = doc.schema
    for name in schema.get_field_names(object_type):
        if name in values:
            continue
        default = schema.get_field_default(object_type, name)
        if isinstance(default, str) and default:
            values[name] = default
    return tuple(values.items())


def harvest_model(args: tuple[str, str]) -> ModelHarvest:  # noqa: C901
    """Map one run's connection rows back to the fields of its input."""
    from idfkit import load_idf

    model, run_dir_text = args
    run_dir = Path(run_dir_text)
    harvest = ModelHarvest(model=Path(model).stem)
    bnd = run_dir / "eplusout.bnd"
    if not bnd.exists():
        return harvest
    rows, fluids = parse_bnd(bnd.read_text(encoding="latin-1"))
    # ExpandObjects writes the expanded input as eplusout.expidf; HVACTemplate objects only have
    # nodes there.
    expanded = run_dir / "eplusout.expidf"
    source = expanded if expanded.exists() else Path(model)
    try:
        doc = load_idf(str(source))
    except Exception as exc:
        print(f"  cannot load {source.name}: {exc}", file=sys.stderr)
        return harvest

    type_names = {t.upper(): t for t in NODE_FIELDS}
    nodelists: dict[str, set[str]] = {}
    if "NodeList" in doc:
        for nl in doc.get_collection("NodeList"):
            entries = cast("list[dict[str, Any]]", nl.data.get("nodes", []) or [])
            nodelists[nl.name.upper()] = {str(e.get("node_name", "")).upper() for e in entries}
    by_type: dict[str, list[Any]] = {}
    objects: dict[tuple[str, str], Any] = {}
    for object_type in NODE_FIELDS:
        if object_type in doc:
            members: list[Any] = list(doc.get_collection(object_type))
            by_type[object_type.upper()] = members
            for obj in members:
                if obj.name:
                    objects[(object_type.upper(), obj.name.upper())] = obj

    for row in rows:
        connection = _CONNECTION_MAP.get(row.connection)
        if connection is None:
            if row.connection not in _CONNECTION_MAP:
                harvest.unmapped[f"connection type {row.connection}"] += 1
            continue
        object_type = type_names.get(row.object_type)
        if object_type is None or row.object_type not in by_type:
            harvest.unmapped[row.object_type] += 1
            continue
        top, ext = NODE_FIELDS[object_type]
        named = objects.get((row.object_type, row.object_name))
        # Unnamed types (ZoneHVAC:EquipmentConnections, OutdoorAir:NodeList) are reported under
        # another name, such as the zone's; find the one object of the type that holds the node.
        # Named types never fall back: EnergyPlus sometimes reports a row under a sibling type
        # (a heating coil's rows under the cooling coil's type), and a node match would then
        # attribute it to the wrong object.
        candidates = [named] if named is not None else [o for o in by_type[row.object_type] if not o.name]
        found: list[tuple[Any, list[str], list[str]]] = []
        for candidate in candidates:
            direct: list[str] = []
            listed: list[str] = []
            for name, value in _node_values(candidate.data, top, ext):
                upper = value.upper()
                # EnergyPlus resolves a NodeList first when a field may name one.
                if upper in nodelists and row.node in nodelists[upper]:
                    listed.append(name)
                elif upper == row.node:
                    direct.append(name)
            if direct or listed:
                found.append((candidate, direct, listed))
        if len(found) != 1:
            harvest.unmapped[f"{object_type} ({'no' if not found else 'several'} objects hold the node)"] += 1
            continue
        obj, direct, listed = found[0]
        data = cast("Mapping[str, Any]", obj.data)
        matches = direct + listed
        # An extensible field matched on several items is one field, not an ambiguity.
        distinct: list[str] = list(dict.fromkeys(matches))
        if not distinct:
            harvest.unmapped[f"{object_type} (no field holds the node)"] += 1
            continue
        if len(distinct) > 1:
            harvest.ambiguous.append(Ambiguous(object_type, tuple(distinct), connection, harvest.model))
            continue
        values = _predicate_values(doc, object_type, data)
        fluid = _FLUID_MAP.get(fluids.get(row.node, ""), Fluid.UNKNOWN)
        harvest.observations.append(
            Observation(
                object_type,
                distinct[0],
                connection,
                row.stream,
                fluid,
                row.parent,
                distinct[0] in listed and distinct[0] not in direct,
                harvest.model,
                values,
            )
        )
    return harvest


# --------------------------------------------------------------------------------------------- #
# Steps 4 and 5: merge, infer predicates, cross-check against naming
# --------------------------------------------------------------------------------------------- #


class Rule(NamedTuple):
    object_type: str
    field: str
    connection: ConnectionType
    stream: int
    fluid: Fluid
    is_parent: bool
    accepts_nodelist: bool
    when: tuple[str, str] | None
    provenance: Provenance


_Role = tuple[ConnectionType, int, bool]


def naming_roles(field_name: str) -> frozenset[ConnectionType] | None:
    """The connection types a field's name allows, or ``None`` when the name says nothing.

    This is the cross-check of step 5 and the source of ``hand_written`` rules. It never overrides
    a role EnergyPlus reported.
    """
    leaf = field_name.rsplit(".", 1)[-1]
    c = ConnectionType
    if "setpoint" in leaf:
        return frozenset({c.SETPOINT})
    if "sensor" in leaf or "reference" in leaf or "control_node" in leaf:
        return frozenset({c.SENSOR, c.ACTUATOR, c.OUTSIDE_AIR})
    if "relief" in leaf:
        return frozenset({c.RELIEF_AIR, c.OUTLET})
    if leaf in ("zone_air_node_name", "zone_node_name"):
        return frozenset({c.ZONE_NODE})
    if "exhaust" in leaf and "zone" in leaf:
        return frozenset({c.ZONE_EXHAUST, c.INLET})
    if "return" in leaf and "zone" in leaf:
        return frozenset({c.ZONE_RETURN, c.INLET})
    if "inlet" in leaf:
        return frozenset({c.INLET, c.OUTSIDE_AIR, c.ZONE_INLET, c.INTERNAL})
    if "outlet" in leaf:
        return frozenset({c.OUTLET, c.RELIEF_AIR, c.ZONE_RETURN, c.ZONE_EXHAUST, c.INTERNAL})
    if "outdoor_air" in leaf or "outside_air" in leaf:
        return frozenset({c.OUTSIDE_AIR})
    return None


def _hand_written_role(field_name: str) -> ConnectionType | None:  # noqa: C901
    leaf = field_name.rsplit(".", 1)[-1]
    c = ConnectionType
    # A heat gain added to a return air node, or a node an object reads, is not a flow use.
    # EnergyPlus does not register these as connections at all; Sensor is the non-flow role.
    if "heat_gain" in leaf or (leaf.endswith("return_air_node_name") and "zone_return" not in leaf):
        return c.SENSOR
    if "demand_calculation" in leaf:
        return c.SENSOR
    if leaf in ("zone_air_node_name", "zone_node_name", "space_air_node_name"):
        return c.ZONE_NODE
    if "ambient" in leaf:
        return c.OUTSIDE_AIR
    if "setpoint" in leaf:
        return c.SETPOINT
    if "sensor" in leaf or "reference" in leaf:
        return c.SENSOR
    if leaf in ("zone_air_node_name", "zone_node_name"):
        return c.ZONE_NODE
    if "relief" in leaf:
        return c.RELIEF_AIR
    if "inlet" in leaf:
        return c.INLET
    if "outlet" in leaf:
        return c.OUTLET
    if "outdoor_air" in leaf or "outside_air" in leaf:
        return c.OUTSIDE_AIR
    return None


def _hand_written_fluid(field_name: str) -> Fluid:
    leaf = field_name.rsplit(".", 1)[-1]
    if "air" in leaf:
        return Fluid.AIR
    if "water" in leaf:
        return Fluid.WATER
    if "steam" in leaf:
        return Fluid.STEAM
    return Fluid.UNKNOWN


def _stream_prefix(field_name: str) -> str:
    leaf = field_name.rsplit(".", 1)[-1]
    return re.sub(r"_?(inlet|outlet)_?.*$", "", leaf)


def _infer_predicate(obs: list[Observation]) -> tuple[str, dict[_Role, frozenset[str]]] | None:
    """Find one top-level choice field whose values separate the roles observed for a field, if any.

    Each role gets the set of values it was observed with; the sets must not overlap. Fields ending
    in ``_name`` name other objects and are never predicates.
    """
    by_role: dict[_Role, list[Observation]] = defaultdict(list)
    for o in obs:
        by_role[(o.connection, o.stream, o.is_parent)].append(o)
    if not obs:
        return None
    key_sets = [{k for k, _ in o.values} for o in obs]
    candidates: set[str] = key_sets[0].intersection(*key_sets[1:])
    for name in sorted(c for c in candidates if not c.endswith("_name")):
        value_of = {role: frozenset(dict(o.values)[name].upper() for o in items) for role, items in by_role.items()}
        union: set[str] = set()
        disjoint = True
        for values in value_of.values():
            if union & values:
                disjoint = False
                break
            union |= values
        if disjoint:
            return name, value_of
    return None


@dataclass
class Review:
    disagreements: list[str] = field(default_factory=lambda: list[str]())
    naming: list[str] = field(default_factory=lambda: list[str]())
    ambiguous: list[str] = field(default_factory=lambda: list[str]())

    def empty(self) -> bool:
        return not (self.disagreements or self.naming or self.ambiguous)


def _load_overrides(path: Path) -> tuple[dict[tuple[str, str], list[Rule]], set[tuple[str, str, str]]]:
    if not path.exists():
        return {}, set()
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    rules: dict[tuple[str, str], list[Rule]] = defaultdict(list)
    for entry in cast("list[dict[str, Any]]", data.get("rule", [])):
        when = cast("list[str] | None", entry.get("when"))
        rules[(entry["object_type"], entry["field"])].append(
            Rule(
                entry["object_type"],
                entry["field"],
                ConnectionType(entry["connection"]),
                int(entry.get("stream", 1)),
                Fluid(entry.get("fluid", "Unknown")),
                bool(entry.get("is_parent", False)),
                bool(entry.get("accepts_nodelist", False)),
                (when[0], when[1]) if when else None,
                cast("Provenance", entry.get("provenance", "eplus_examples")),
            )
        )
    accepted = {
        (e["object_type"], e["field"], e["connection"]) for e in cast("list[dict[str, Any]]", data.get("accept", []))
    }
    accepted |= {
        (e["object_type"], "|".join(e["fields"]), "ambiguous")
        for e in cast("list[dict[str, Any]]", data.get("ambiguous", []))
    }
    return dict(rules), accepted


def merge(  # noqa: C901
    harvests: Iterable[ModelHarvest],
    test_models: frozenset[str],
    overrides: Mapping[tuple[str, str], list[Rule]],
    accepted: set[tuple[str, str, str]],
) -> tuple[dict[str, list[Rule]], Review, Counter[str]]:
    """Merge observations into rules, returning the rules, what needs review and the unmapped counts."""
    by_field: dict[tuple[str, str], list[Observation]] = defaultdict(list)
    ambiguous: dict[tuple[str, tuple[str, ...]], set[str]] = defaultdict(set)
    unmapped: Counter[str] = Counter()
    for h in harvests:
        for o in h.observations:
            by_field[(o.object_type, o.field)].append(o)
        for a in h.ambiguous:
            ambiguous[(a.object_type, a.fields)].add(a.model)
        unmapped.update(h.unmapped)

    review = Review()
    rules: dict[str, list[Rule]] = defaultdict(list)
    for (object_type, field_name), obs in sorted(by_field.items()):
        if (object_type, field_name) in overrides:
            continue
        provenance: Provenance = (
            "eplus_examples" if any(o.model not in test_models for o in obs) else "eplus_test_model"
        )
        nodelist = any(o.via_nodelist for o in obs) or "nodelist" in field_name
        fluids = Counter(o.fluid for o in obs if o.fluid is not Fluid.UNKNOWN)
        fluid = fluids.most_common(1)[0][0] if fluids else Fluid.UNKNOWN
        roles = Counter((o.connection, o.stream, o.is_parent) for o in obs)
        if len(roles) == 1:
            (connection, stream, is_parent), _ = roles.most_common(1)[0]
            allowed = naming_roles(field_name)
            if (
                allowed is not None
                and connection not in allowed
                and (object_type, field_name, connection.value) not in accepted
            ):
                review.naming.append(
                    f"{object_type}.{field_name}: EnergyPlus says {connection.value}, the name allows "
                    f"{sorted(c.value for c in allowed)} ({len(obs)} uses, e.g. {obs[0].model})"
                )
            rules[object_type].append(
                Rule(object_type, field_name, connection, stream, fluid, is_parent, nodelist, None, provenance)
            )
            continue
        predicate = _infer_predicate(obs)
        detail = ", ".join(f"{c.value}/{s}{'/parent' if p else ''} x{n}" for (c, s, p), n in roles.most_common())
        if predicate is None:
            review.disagreements.append(f"{object_type}.{field_name}: {detail}; no single field value separates them")
        else:
            name, values = predicate
            parts = ", ".join(f"{name} in {sorted(v)} -> {c.value}/{s}" for (c, s, _), v in values.items())
            review.disagreements.append(f"{object_type}.{field_name}: {detail}; predicate candidate: {parts}")

    for (object_type, fields), models in sorted(ambiguous.items()):
        if all(((object_type, f) in by_field or (object_type, f) in overrides) for f in fields):
            continue  # each field was resolved unambiguously elsewhere
        if (object_type, "|".join(fields), "ambiguous") in accepted:
            continue  # reviewed: the unresolved field keeps a hand-written rule from its name
        review.ambiguous.append(f"{object_type}: same node in {list(fields)} (e.g. {sorted(models)[0]})")

    for (object_type, _), entries in overrides.items():
        rules[object_type].extend(entries)
    return dict(rules), review, unmapped


def add_hand_written(rules: dict[str, list[Rule]]) -> None:
    """Give every node field EnergyPlus never reported a rule, as ``hand_written``.

    An ``X:Instance`` type takes the rule EnergyPlus reported for the same field of ``X``; any other
    field takes a rule from its name. Fields whose name says nothing get no rule.
    """
    for object_type, (top, ext) in NODE_FIELDS.items():
        have = {r.field for r in rules.get(object_type, [])}
        names = list(top) + [f"*.{e}" for e in ext]
        # A field EnergyPlus never reported takes the stream and fluid of its reported partner:
        # heat_recovery_outlet pairs with heat_recovery_inlet. Unpaired prefixes take new streams.
        streams: dict[str, int] = {}
        fluids: dict[str, Fluid] = {}
        for r in rules.get(object_type, []):
            if r.connection in (ConnectionType.INLET, ConnectionType.OUTLET):
                streams.setdefault(_stream_prefix(r.field), r.stream)
                fluids.setdefault(_stream_prefix(r.field), r.fluid)
        next_stream = max(streams.values(), default=0) + 1
        sibling = {r.field: r for r in rules.get(object_type.removesuffix(":Instance"), [])}
        for name in names:
            if name in have or any(h.endswith("." + name[2:]) for h in have if name.startswith("*.")):
                continue
            if object_type.endswith(":Instance") and name in sibling:
                rules.setdefault(object_type, []).append(
                    sibling[name]._replace(object_type=object_type, provenance="hand_written")
                )
                continue
            connection = _hand_written_role(name)
            if connection is None and object_type.startswith("SetpointManager:"):
                connection = ConnectionType.SENSOR  # a setpoint manager only reads its other nodes
            if connection is None:
                continue
            prefix = _stream_prefix(name)
            if prefix not in streams:
                streams[prefix] = next_stream
                next_stream += 1
            rules.setdefault(object_type, []).append(
                Rule(
                    object_type,
                    name,
                    connection,
                    streams[prefix],
                    fluids.get(prefix, _hand_written_fluid(name)),
                    False,
                    "nodelist" in name,
                    None,
                    "hand_written",
                )
            )


# --------------------------------------------------------------------------------------------- #
# Step 6: write the table
# --------------------------------------------------------------------------------------------- #

_HEADER: Final = '''"""Auto-generated connection rules per object type, from EnergyPlus's node connection report.

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_port_rules --energyplus <EnergyPlus 26.2> --work-dir <dir>

Each rule records how one node field connects (connection type, fluid stream, fluid, parent flag)
and where the rule came from: ``eplus_examples`` (EnergyPlus's ``eplusout.bnd`` for the 26.2
example files), ``eplus_test_model`` (the same for a minimal model under
``codegen/port_rule_models/``) or ``hand_written`` (from the field's name, never reported by
EnergyPlus). Reviewed resolutions come from ``codegen/port_rule_overrides.toml``.

An extensible field is written ``group.field``; ``*.field`` matches any extensible group.
"""

from __future__ import annotations

from typing import Final

from idfkit.hvac._rule_types import PortRule
from idfkit.hvac.types import ConnectionType as C
from idfkit.hvac.types import Fluid as F

PORT_RULES: Final[dict[str, tuple[PortRule, ...]]] = {
'''


def render(rules: Mapping[str, list[Rule]]) -> str:
    """Render the rules as the module source written to ``_port_rules.py``."""
    out = [_HEADER]
    for object_type in sorted(rules):
        out.append(f'    "{object_type}": (\n')
        ordered = sorted(rules[object_type], key=lambda r: (r.field, r.when or ("", "")))
        for r in ordered:
            when = f'("{r.when[0]}", "{r.when[1]}")' if r.when else "None"
            out.append(
                f'        PortRule("{r.field}", C.{r.connection.name}, {r.stream}, F.{r.fluid.name}, '
                f'{r.is_parent}, {r.accepts_nodelist}, {when}, "{r.provenance}"),\n'
            )
        out.append("    ),\n")
    out.append("}\n")
    return "".join(out)


def _write_report(path: Path, review: Review, unmapped: Counter[str]) -> None:
    lines = ["# Port-rule generation: items needing review\n"]
    for title, items in (
        ("Role disagreements", review.disagreements),
        ("Naming cross-check", review.naming),
        ("Ambiguous matches", review.ambiguous),
    ):
        lines.append(f"\n## {title} ({len(items)})\n\n")
        lines.extend(f"- {i}\n" for i in items)
    lines.append(f"\n## Unmapped rows ({sum(unmapped.values())})\n\n")
    lines.extend(f"- {k}: {v}\n" for k, v in unmapped.most_common())
    path.write_text("".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    """Run, harvest, merge, check and write. Returns 1 while anything is unreviewed."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--energyplus", type=Path, required=True, help="EnergyPlus 26.2 installation directory")
    parser.add_argument("--work-dir", type=Path, help="keep runs here and reuse them (default: a temporary dir)")
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--report", type=Path, help="write the items needing review to this Markdown file")
    parser.add_argument("--models", type=Path, nargs="*", help="run only these models (development)")
    args = parser.parse_args(argv)

    work = args.work_dir or Path(tempfile.mkdtemp(prefix="idfkit-port-rules-"))
    work.mkdir(parents=True, exist_ok=True)
    example_dir = args.energyplus / "ExampleFiles"
    examples = args.models or sorted(example_dir.glob("*.idf"))
    tests = [assemble_test_model(p, example_dir, work / "_test_models") for p in sorted(_TEST_MODELS_DIR.glob("*.idf"))]
    test_stems = frozenset(t.stem for t in tests)
    models = [*examples, *tests]
    print(f"Running {len(models)} models into {work}")
    run_models(args.energyplus, models, work, args.jobs)

    print("Harvesting connection rows")
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        harvests = list(pool.map(harvest_model, [(str(m), str(work / m.stem)) for m in models], chunksize=8))

    overrides, accepted = _load_overrides(_OVERRIDES_PATH)
    rules, review, unmapped = merge(harvests, test_stems, overrides, accepted)
    add_hand_written(rules)
    if args.report:
        _write_report(args.report, review, unmapped)
    counts = Counter(r.provenance for rs in rules.values() for r in rs)
    print(
        f"{len(rules)} object types, {sum(counts.values())} rules: "
        + ", ".join(f"{k} {v}" for k, v in sorted(counts.items()))
    )
    if not review.empty():
        print(
            f"Unreviewed: {len(review.disagreements)} disagreements, {len(review.naming)} naming mismatches, "
            f"{len(review.ambiguous)} ambiguous matches. Record resolutions in {_OVERRIDES_PATH.name}.",
            file=sys.stderr,
        )
        return 1
    _OUTPUT_PATH.write_text(render(rules), encoding="utf-8")
    # Format like the committed file, so `make check` diffs content and not layout.
    subprocess.run([sys.executable, "-m", "ruff", "format", "--quiet", str(_OUTPUT_PATH)], check=True)  # noqa: S603
    print(f"Wrote {_OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
