"""Static connection checks over the HVAC topology view (FR-012, FR-013, FR-013a).

Each check runs once over the view's integer structures, never as one query per object. The checks
are QA: a clean result does not mean the model simulates, and a finding is not a runtime error
(Principle IV). Only a qualified check may be an error, a finding that relies on a ``hand_written``
rule never is, and a model of an earlier EnergyPlus version may have its severities capped by the
measured table in ``_version_caps.py``.

| Code | Check | Severity |
|---|---|---|
| T010 | A branch's listed nodes differ from the component's own ports | see ``QUALIFIED`` |
| T011 | Consecutive branch components are not connected | see ``QUALIFIED`` |
| T001 | A component inlet nothing supplies, not a loop inlet and not outdoor air | warning |
| T002 | A zone inlet nothing supplies | warning |
| T003 | A zone exhaust nothing draws from | warning |
| T004 | A setpoint, sensor or actuator node no component carries flow through | warning |
| T030 | An outlet a branch carries that nothing takes | warning |
| T012 | A branch a loop side's splitter or mixer names that its BranchList omits, or the reverse | warning |
| T013 | A coil on a plant loop's supply side, or a boiler on its demand side | warning |
| T090 | Object type with node fields but no connection rule | info |
| T091 | Template system present; topology not covered | info |
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING, Final, Literal, NamedTuple

from idfkit._graph_common import ObjectKey
from idfkit.hvac._categories import category_of
from idfkit.hvac._version_caps import MEASURED_VERSIONS, VERSION_CAPS
from idfkit.hvac.topology import (
    CONNECTIONS,
    CONSUMES,
    CONTROLS,
    LOOP_ORDER,
    LOOP_SIDES,
    PRODUCES,
    PROVENANCES,
    UNCLASSIFIED,
    HVACTopology,
)
from idfkit.hvac.types import ComponentCategory, ConnectionType, Provenance, Severity, TopologyFinding

if TYPE_CHECKING:
    from idfkit.document import IDFDocument
    from idfkit.hvac._index import TopologyIndex, Use
    from idfkit.objects import IDFObject

__all__ = ["check_topology"]

QUALIFIED: Final[dict[str, Severity]] = {
    "T010": "error",
    "T011": "error",
}
"""The severity each qualified check reports before any version cap.

A check moves from warning to error only when the 26.2 corpus test reports no finding for it on any
example file (FR-013), and the promotion is recorded in the changelog.
"""

_RANK: Final[dict[Severity, int]] = {"info": 0, "warning": 1, "error": 2}
_WEAKEST: Final[dict[Provenance, int]] = {"hand_written": 0, "eplus_test_model": 1, "eplus_examples": 2}

_INLET = CONNECTIONS.index(ConnectionType.INLET)
_OUTLET = CONNECTIONS.index(ConnectionType.OUTLET)
_ZONE_RETURN = CONNECTIONS.index(ConnectionType.ZONE_RETURN)
_ZONE_SIDE = frozenset({_ZONE_RETURN, CONNECTIONS.index(ConnectionType.ZONE_EXHAUST)})
_STRUCTURAL_PARENTS = frozenset({"BRANCH", "AIRLOOPHVAC", "PLANTLOOP", "CONDENSERLOOP"})
_BOUNDARY = frozenset({CONNECTIONS.index(ConnectionType.OUTSIDE_AIR), CONNECTIONS.index(ConnectionType.RELIEF_AIR)})


def check_topology(doc: IDFDocument) -> list[TopologyFinding]:
    """Run every connection check on *doc*.

    A convenience for ``HVACTopology.from_document(doc).check()``.

    Args:
        doc: The document.

    Returns:
        The findings, severities after the version cap.
    """
    return HVACTopology.from_document(doc).check()


def run_checks(index: TopologyIndex) -> list[TopologyFinding]:
    """Run every check over a view's index. Called by :meth:`HVACTopology.check`, which caches the result."""
    sides = _side_lists(index)
    findings = [
        *_branch_checks(index),
        *_branch_list_checks(sides),
        *_plant_side_checks(index, sides),
        *_one_sided_nodes(index),
        *_coverage_findings(index),
    ]
    return [cap_severity(f, index.doc.version) for f in findings]


# --------------------------------------------------------------------------------------------- #
# Severity
# --------------------------------------------------------------------------------------------- #


def _weakest(provenances: list[Provenance]) -> Provenance:
    return min(provenances, key=lambda p: _WEAKEST[p]) if provenances else "eplus_examples"


def qualified_severity(code: str, provenance: Provenance) -> Severity:
    """The severity a qualified check reports, before the version cap, for a finding of *provenance*."""
    severity = QUALIFIED[code]
    if provenance == "hand_written" and severity == "error":
        return "warning"  # a rule EnergyPlus never reported cannot carry an error
    return severity


def _cap_row(code: str, version: tuple[int, int, int]) -> tuple[Literal["warning", "info"], str] | None:
    if not MEASURED_VERSIONS or version >= (26, 2, 0):
        return None
    at_or_below = [v for v in MEASURED_VERSIONS if v <= version]
    measured = at_or_below[-1] if at_or_below else MEASURED_VERSIONS[0]
    for row in VERSION_CAPS:
        if row.code == code and row.version == measured:
            shown = ".".join(str(p) for p in measured)
            reason = (
                f"{code} produced {row.false_findings} false finding(s) on the {row.models} EnergyPlus {shown} "
                "example files"
            )
            return row.max_severity, reason
    return None


def cap_severity(finding: TopologyFinding, version: tuple[int, int, int]) -> TopologyFinding:
    """Apply the measured cap for *version* to an error finding (FR-013a); other findings pass through."""
    if finding.severity != "error":
        return finding
    row = _cap_row(finding.code, version)
    if row is None or _RANK[row[0]] >= _RANK[finding.severity]:
        return finding
    return TopologyFinding(
        code=finding.code,
        severity=row[0],
        objects=finding.objects,
        message=finding.message,
        provenance=finding.provenance,
        node=finding.node,
        field=finding.field,
        expected=finding.expected,
        actual=finding.actual,
        capped_from="error",
        cap_reason=row[1],
    )


# --------------------------------------------------------------------------------------------- #
# T010, T011: branches
# --------------------------------------------------------------------------------------------- #

_Ports = dict[int, tuple[dict[int, str], dict[int, str], list[Provenance]]]
"""Per stream: ``(inlet node id -> field, outlet node id -> field, provenances)``."""


def _ports(index: TopologyIndex, oid: int) -> _Ports:
    ports: _Ports = {}
    for nid, mid, conn, stream, _ in index.obj_uses[oid]:
        if conn not in (_INLET, _OUTLET):
            continue
        field, _, _, prov, _ = index.meta[mid]
        inlets, outlets, provs = ports.setdefault(stream, ({}, {}, []))
        (inlets if conn == _INLET else outlets).setdefault(nid, field)
        if prov is not None:
            provs.append(PROVENANCES[prov])
    return ports


def _oa_mixer_ports(index: TopologyIndex, system: IDFObject, objects: dict[ObjectKey, int]) -> _Ports:
    """An outdoor air system has no node fields; its branch nodes are its mixer's return and mixed air."""
    list_name = system.data.get("outdoor_air_equipment_list_name")
    if not isinstance(list_name, str) or "AirLoopHVAC:OutdoorAirSystem:EquipmentList" not in index.doc:
        return {}
    collection = index.doc.get_collection("AirLoopHVAC:OutdoorAirSystem:EquipmentList")
    equipment = collection.get(list_name)
    if equipment is None:
        return {}
    for item in equipment.extensible_items("equipment"):
        if str(item.get("component_object_type", "")).upper() != "OUTDOORAIR:MIXER":
            continue
        mixer = objects.get(ObjectKey("OutdoorAir:Mixer", str(item.get("component_name", ""))))
        if mixer is None:
            return {}
        ports: _Ports = {}
        for nid, mid, _, _, _ in index.obj_uses[mixer]:
            field, _, _, prov, _ = index.meta[mid]
            if field in ("return_air_stream_node_name", "mixed_air_node_name"):
                inlets, outlets, provs = ports.setdefault(1, ({}, {}, []))
                (inlets if field == "return_air_stream_node_name" else outlets)[nid] = f"OutdoorAir:Mixer.{field}"
                if prov is not None:
                    provs.append(PROVENANCES[prov])
        return ports
    return {}


def _branch_checks(index: TopologyIndex) -> Iterator[TopologyFinding]:
    if "Branch" not in index.doc:
        return
    objects = {key: oid for oid, key in enumerate(index.obj_key)}
    for branch in index.doc.get_collection("Branch"):
        bkey = ObjectKey("Branch", branch.name)
        items = branch.extensible_items("components")
        for i, item in enumerate(items):
            ctype = str(item.get("component_object_type", "") or "")
            cname = str(item.get("component_name", "") or "")
            node_in = str(item.get("component_inlet_node_name", "") or "")
            node_out = str(item.get("component_outlet_node_name", "") or "")
            ckey = ObjectKey(ctype, cname)
            oid = objects.get(ckey)
            if ctype.upper() == "AIRLOOPHVAC:OUTDOORAIRSYSTEM" and "AirLoopHVAC:OutdoorAirSystem" in index.doc:
                system = index.doc.get_collection("AirLoopHVAC:OutdoorAirSystem").get(cname)
                ports = _oa_mixer_ports(index, system, objects) if system is not None else {}
            else:
                ports = _ports(index, oid) if oid is not None else {}
            if ports:
                yield from _t010(index, bkey, ckey, node_in, node_out, ports)
            if i + 1 < len(items):
                nxt = items[i + 1]
                next_in = str(nxt.get("component_inlet_node_name", "") or "")
                if node_out and next_in and node_out.upper() != next_in.upper():
                    next_key = ObjectKey(str(nxt.get("component_object_type", "")), str(nxt.get("component_name", "")))
                    yield TopologyFinding(
                        code="T011",
                        severity=qualified_severity("T011", "eplus_examples"),
                        objects=(bkey, ckey, next_key),
                        message=(
                            f"Branch '{branch.name}' takes {ckey.object_type} '{ckey.name}' out to '{node_out}', "
                            f"but the next component, {next_key.object_type} '{next_key.name}', is listed "
                            f"with inlet '{next_in}'"
                        ),
                        provenance="eplus_examples",
                        node=node_out,
                        field="components.component_inlet_node_name",
                        expected=node_out,
                        actual=next_in,
                    )


def _t010(
    index: TopologyIndex,
    bkey: ObjectKey,
    ckey: ObjectKey,
    node_in: str,
    node_out: str,
    ports: _Ports,
) -> Iterator[TopologyFinding]:
    nin = index.node_id.get(node_in.upper())
    nout = index.node_id.get(node_out.upper())
    for inlets, outlets, _ in ports.values():
        if nin in inlets and nout in outlets:
            return  # one stream matches both ends
    # Choose the stream the branch most likely means: one end matches, else the first full stream.
    streams = sorted(ports.items())
    chosen = next((s for s in streams if nin in s[1][0] or nout in s[1][1]), None)
    chosen = chosen or next((s for s in streams if s[1][0] and s[1][1]), streams[0])
    inlets, outlets, provs = chosen[1]
    provenance = _weakest(provs)
    for end, branch_node, nid, own in (("inlet", node_in, nin, inlets), ("outlet", node_out, nout, outlets)):
        if not branch_node or nid in own or not own:
            continue
        actual_id, field = next(iter(own.items()))
        actual = index.node_name[actual_id]
        yield TopologyFinding(
            code="T010",
            severity=qualified_severity("T010", provenance),
            objects=(bkey, ckey),
            message=(
                f"Branch '{bkey.name}' lists the {end} of {ckey.object_type} '{ckey.name}' as '{branch_node}', "
                f"but the component's {field} is '{actual}'"
            ),
            provenance=provenance,
            node=actual,
            field=field,
            expected=branch_node,
            actual=actual,
        )


# --------------------------------------------------------------------------------------------- #
# T030: one-sided nodes
# --------------------------------------------------------------------------------------------- #


def _branch_streams(index: TopologyIndex) -> set[tuple[int, int]]:
    """``(object id, stream)`` pairs a branch carries: the stream whose inlet the branch lists."""
    carried: set[tuple[int, int]] = set()
    if "Branch" not in index.doc:
        return carried
    objects = {key: oid for oid, key in enumerate(index.obj_key)}
    for branch in index.doc.get_collection("Branch"):
        for item in branch.extensible_items("components"):
            oid = objects.get(
                ObjectKey(str(item.get("component_object_type", "")), str(item.get("component_name", "")))
            )
            nid = index.node_id.get(str(item.get("component_inlet_node_name", "") or "").upper())
            if oid is None or nid is None:
                continue
            for stream, (inlets, _, _) in _ports(index, oid).items():
                if nid in inlets:
                    carried.add((oid, stream))
    return carried


def _sides(index: TopologyIndex, uses: list[Use]) -> tuple[list[Use], list[Use]] | None:
    """The producing and consuming flow uses of a node, or ``None`` when a boundary or an unknown
    role explains whatever is missing. A parent use counts only when no child takes that side:
    some parents (four-pipe beams, induction secondary inlets) hold the node themselves."""
    producers: list[Use] = []
    consumers: list[Use] = []
    parent_producers: list[Use] = []
    parent_consumers: list[Use] = []
    for use in uses:
        conn = use[2]
        if conn in _BOUNDARY or conn == UNCLASSIFIED:
            return None
        parent = index.meta[use[1]][2]
        if parent and index.obj[use[0]].obj_type.upper() in _STRUCTURAL_PARENTS:
            continue  # branches and loops only list nodes
        if conn in PRODUCES:
            (parent_producers if parent else producers).append(use)
        elif conn in CONSUMES:
            (parent_consumers if parent else consumers).append(use)
    return (producers or parent_producers, consumers or parent_consumers)


_ZONE_INLET = CONNECTIONS.index(ConnectionType.ZONE_INLET)
_ZONE_EXHAUST = CONNECTIONS.index(ConnectionType.ZONE_EXHAUST)


def _finding(index: TopologyIndex, code: str, nid: int, uses: list[Use], text: str) -> TopologyFinding:
    provs: list[Provenance] = [PROVENANCES[p] for u in uses if (p := index.meta[u[1]][3]) is not None]
    node = index.node_name[nid]
    return TopologyFinding(
        code=code,
        severity="warning",
        objects=tuple(dict.fromkeys(index.obj_key[u[0]] for u in uses)),
        message=f"Node '{node}' {text}",
        provenance=_weakest(provs),
        node=node,
    )


def _one_sided_nodes(index: TopologyIndex) -> Iterator[TopologyFinding]:
    """T001, T002, T003, T030 and T004, one finding per node, following EnergyPlus's own rule: an
    inlet needs a source.

    - T001: a component inlet nothing supplies, not a loop's own inlet and not outdoor air.
    - T002: a zone inlet nothing supplies.
    - T003: a zone exhaust nothing draws from.
    - T030: an outlet a branch carries that nothing takes. Elsewhere an outlet nothing takes is
      legal (exhaust fans, air-cooled condensers and relief streams vent outdoors); an unused zone
      return is legal too.
    - T004: a node only setpoint managers, sensors, controllers or actuators name.
    """
    if any(part.kind == "hvac_template" for part in index.coverage.uncovered):
        return  # template systems have no nodes yet, so a missing side is expected (T091 says so)
    carried = _branch_streams(index)
    for nid, uses in enumerate(index.uses):
        if nid in index.loop_nodes:
            continue  # loops join their own inlets and outlets
        if uses and all(u[2] in CONTROLS for u in uses):
            yield _finding(index, "T004", nid, uses, "is set or sensed, but no component carries flow through it")
            continue
        sides = _sides(index, uses)
        if sides is None:
            continue
        producers, consumers = sides
        if bool(producers) == bool(consumers):
            continue
        if consumers:
            zone = any(u[2] == _ZONE_INLET for u in consumers)
            yield _finding(index, "T002" if zone else "T001", nid, consumers, "is an inlet nothing supplies")
        elif any(u[2] == _ZONE_EXHAUST for u in producers):
            yield _finding(index, "T003", nid, producers, "is a zone exhaust nothing draws from")
        elif not any(u[2] in _ZONE_SIDE for u in producers) and any((u[0], u[3]) in carried for u in producers):
            yield _finding(index, "T030", nid, producers, "leaves a component on a branch but nothing takes it")


# --------------------------------------------------------------------------------------------- #
# T012: branch lists against connectors; T013: plant equipment on the wrong side
# --------------------------------------------------------------------------------------------- #

_CONNECTOR_LIST_FIELDS: Final[dict[tuple[str, str], str]] = {
    ("AIRLOOPHVAC", "supply"): "connector_list_name",
    ("PLANTLOOP", "supply"): "plant_side_connector_list_name",
    ("PLANTLOOP", "demand"): "demand_side_connector_list_name",
    ("CONDENSERLOOP", "supply"): "condenser_side_connector_list_name",
    ("CONDENSERLOOP", "demand"): "condenser_demand_side_connector_list_name",
}
"""The field naming each loop side's ``ConnectorList``; the ``BranchList`` field comes from ``LOOP_SIDES``."""

_WRONG_SIDE: Final[dict[str, frozenset[ComponentCategory]]] = {
    "supply": frozenset({ComponentCategory.HEATING_COIL, ComponentCategory.COOLING_COIL}),
    "demand": frozenset({ComponentCategory.BOILER}),
}
"""Categories that never belong on a ``PlantLoop`` side. A chiller is left out: its condenser sits on
a demand side by design."""


class _Connector(NamedTuple):
    """A splitter or mixer: its trunk branch (splitter inlet or mixer outlet) and its parallel branches."""

    obj: IDFObject
    is_splitter: bool
    trunk: str
    parallel: list[str]


class _SideLists(NamedTuple):
    """One loop side with a ``BranchList``, and the splitters and mixers its ``ConnectorList`` names
    (``None`` when the side has no ``ConnectorList``)."""

    loop: IDFObject
    side: str
    branch_list: IDFObject
    connectors: list[_Connector] | None


def _text(obj: IDFObject, field: str) -> str:
    return str(obj.get(field, "") or "")


def _get(index: TopologyIndex, object_type: str, name: str) -> IDFObject | None:
    if not name or object_type not in index.doc:
        return None
    return index.doc.get_collection(object_type).get(name)


def _list_branches(branch_list: IDFObject) -> list[str]:
    return [str(item.get("branch_name", "") or "") for item in branch_list.extensible_items("branches")]


def _side_lists(index: TopologyIndex) -> list[_SideLists]:
    """Every loop side with a ``BranchList``, read once per check run and shared by T012 and T013."""
    found: list[_SideLists] = []
    for loop_type in LOOP_ORDER:
        if loop_type not in index.doc:
            continue
        _, sides = LOOP_SIDES[loop_type.upper()]
        for loop in index.doc.get_collection(loop_type):
            for side, list_field in sides:
                branch_list = _get(index, "BranchList", _text(loop, list_field))
                if branch_list is None:
                    continue
                connector_field = _CONNECTOR_LIST_FIELDS[(loop_type.upper(), side)]
                connector_list = _get(index, "ConnectorList", _text(loop, connector_field))
                connectors = None if connector_list is None else list(_connectors(index, connector_list))
                found.append(_SideLists(loop, side, branch_list, connectors))
    return found


def _connectors(index: TopologyIndex, connector_list: IDFObject) -> Iterator[_Connector]:
    """The splitters and mixers a ``ConnectorList`` names."""
    for i in (1, 2):
        ctype = _text(connector_list, f"connector_{i}_object_type")
        connector = _get(index, ctype, _text(connector_list, f"connector_{i}_name"))
        if connector is None:
            continue
        is_splitter = ctype.upper() == "CONNECTOR:SPLITTER"
        trunk = _text(connector, "inlet_branch_name" if is_splitter else "outlet_branch_name")
        key = "outlet_branch_name" if is_splitter else "inlet_branch_name"
        parallel = [str(item.get(key, "") or "") for item in connector.extensible_items("branches")]
        yield _Connector(connector, is_splitter, trunk, [b for b in parallel if b])


def _branch_list_checks(sides: list[_SideLists]) -> Iterator[TopologyFinding]:
    """T012, both directions: a branch a splitter or mixer names that the side's ``BranchList``
    omits, and a listed branch, other than a connector's trunk branch, that no splitter feeds."""
    for entry in sides:
        if entry.connectors is not None:
            yield from _unlisted_branches(entry, entry.connectors)
            yield from _unfed_branches(entry, entry.connectors)


def _unlisted_branches(entry: _SideLists, connectors: list[_Connector]) -> Iterator[TopologyFinding]:
    loop, side, branch_list, _ = entry
    listed = {b.upper() for b in _list_branches(branch_list)}
    reported: set[str] = set()
    for connector in connectors:
        for name in ([connector.trunk] if connector.trunk else []) + connector.parallel:
            if name.upper() in listed or name.upper() in reported:
                continue
            reported.add(name.upper())
            yield TopologyFinding(
                code="T012",
                severity="warning",
                objects=(
                    ObjectKey("BranchList", branch_list.name),
                    ObjectKey("Branch", name),
                    ObjectKey(connector.obj.obj_type, connector.obj.name),
                ),
                message=(
                    f"{connector.obj.obj_type} '{connector.obj.name}' on the {side} side of {loop.obj_type} "
                    f"'{loop.name}' names branch '{name}', but BranchList '{branch_list.name}' does not list it"
                ),
                provenance="hand_written",
                field="branches",
                expected=name,
            )


def _unfed_branches(entry: _SideLists, connectors: list[_Connector]) -> Iterator[TopologyFinding]:
    splitters = [c for c in connectors if c.is_splitter]
    if not splitters:
        return
    loop, side, branch_list, _ = entry
    fed = {b.upper() for c in splitters for b in c.parallel} | {c.trunk.upper() for c in connectors if c.trunk}
    reported: set[str] = set()
    for name in _list_branches(branch_list):
        if not name or name.upper() in fed or name.upper() in reported:
            continue
        reported.add(name.upper())
        yield TopologyFinding(
            code="T012",
            severity="warning",
            objects=(ObjectKey("BranchList", branch_list.name), ObjectKey("Branch", name)),
            message=(
                f"BranchList '{branch_list.name}' lists branch '{name}' on the {side} side of "
                f"{loop.obj_type} '{loop.name}', but no splitter on that side feeds it"
            ),
            provenance="hand_written",
            field="branches",
            actual=name,
        )


def _plant_side_checks(index: TopologyIndex, sides: list[_SideLists]) -> Iterator[TopologyFinding]:
    """T013: no heating or cooling coil on a ``PlantLoop``'s supply side and no boiler on its demand side."""
    for loop, side, branch_list, _ in sides:
        if loop.obj_type.upper() != "PLANTLOOP":
            continue
        wrong = _WRONG_SIDE[side]
        for branch_name in _list_branches(branch_list):
            branch = _get(index, "Branch", branch_name)
            if branch is None:
                continue
            for item in branch.extensible_items("components"):
                ctype = str(item.get("component_object_type", "") or "")
                category = category_of(ctype)
                if category not in wrong:
                    continue
                cname = str(item.get("component_name", "") or "")
                belongs = "demand" if side == "supply" else "supply"
                yield TopologyFinding(
                    code="T013",
                    severity="warning",
                    objects=(
                        ObjectKey(ctype, cname),
                        ObjectKey("Branch", branch.name),
                        ObjectKey(loop.obj_type, loop.name),
                    ),
                    message=(
                        f"{ctype} '{cname}' is on branch '{branch.name}' on the {side} side of PlantLoop "
                        f"'{loop.name}'; a {category.value.replace('_', ' ')} belongs on the {belongs} side"
                    ),
                    provenance="hand_written",
                    expected=belongs,
                    actual=side,
                )


# --------------------------------------------------------------------------------------------- #
# T090, T091: what the view cannot judge
# --------------------------------------------------------------------------------------------- #


def _coverage_findings(index: TopologyIndex) -> Iterator[TopologyFinding]:
    for part in index.coverage.uncovered:
        if part.kind == "unclassified_type":
            for key in part.examples:
                yield TopologyFinding(
                    code="T090",
                    severity="info",
                    objects=(key,),
                    message=(
                        f"{key.object_type} names nodes but has no connection rule; its connections are not checked"
                    ),
                    provenance="hand_written",
                )
        elif part.kind == "hvac_template":
            yield TopologyFinding(
                code="T091",
                severity="info",
                objects=part.examples,
                message=(
                    f"{part.count} HVACTemplate object(s) present; their systems have no nodes until expanded, "
                    "so their connections are not checked"
                ),
                provenance="hand_written",
            )
