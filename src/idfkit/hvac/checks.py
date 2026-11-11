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
| T030 | Node used on only one side of a flow, with no boundary explaining it | warning |
| T090 | Object type with node fields but no connection rule | info |
| T091 | Template system present; topology not covered | info |
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING, Final, Literal

from idfkit._graph_common import ObjectKey
from idfkit.hvac._version_caps import MEASURED_VERSIONS, VERSION_CAPS
from idfkit.hvac.topology import CONNECTIONS, CONSUMES, PRODUCES, PROVENANCES, UNCLASSIFIED, HVACTopology
from idfkit.hvac.types import ConnectionType, Provenance, Severity, TopologyFinding

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
    findings = [*_branch_checks(index), *_one_sided_nodes(index), *_coverage_findings(index)]
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


def _one_sided_nodes(index: TopologyIndex) -> Iterator[TopologyFinding]:
    """T030, following EnergyPlus's own rule: an inlet needs a source. An outlet that nothing takes
    is legal (exhaust fans, air-cooled condensers and relief streams vent outdoors), so it is
    reported only on a stream a branch carries, where the next component should take it."""
    if any(part.kind == "hvac_template" for part in index.coverage.uncovered):
        return  # template systems have no nodes yet, so a missing side is expected (T091 says so)
    carried = _branch_streams(index)
    for nid, uses in enumerate(index.uses):
        if nid in index.loop_nodes:
            continue  # loops join their own inlets and outlets
        sides = _sides(index, uses)
        if sides is None:
            continue
        producers, consumers = sides
        if bool(producers) == bool(consumers):
            continue
        if producers:
            if any(u[2] in _ZONE_SIDE for u in producers):
                continue  # an unused zone return is valid; an unused zone exhaust is T003's
            if not any((u[0], u[3]) in carried for u in producers):
                continue
        one_side = producers or consumers
        provs: list[Provenance] = [PROVENANCES[p] for u in one_side if (p := index.meta[u[1]][3]) is not None]
        objects = tuple(dict.fromkeys(index.obj_key[u[0]] for u in one_side))
        node = index.node_name[nid]
        side = "leaves a component on a branch but nothing takes it" if producers else "nothing supplies it"
        yield TopologyFinding(
            code="T030",
            severity="warning",
            objects=objects,
            message=f"Node '{node}' {side}, and no boundary explains it",
            provenance=_weakest(provs),
            node=node,
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
