"""The HVAC topology view: node uses, flow edges and coverage, derived from a document.

A node is a string, not an object, so the reference graph never sees it. This module derives, on
demand, which fields of which objects name each node, with the connection role EnergyPlus gives that
field (``_port_rules.py``), and the flow edges those roles imply. The view is a pure function of the
document, cached on it per revision (research R-05, R-06).

Performance is part of the contract (research R-21). Inside the view everything is integers and
tuples: node names are interned to dense ids, objects are indexed, each node's uses and each
object's flow edges are lists of tuples. The public dataclasses are built only for what a call
returns. Per-type plans, which pair each node field with its compiled rules, are computed once per
schema version and shared by every document of that version.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Collection, Iterable, Mapping
from typing import TYPE_CHECKING, Any, NamedTuple, cast

from idfkit._derived import get_or_build
from idfkit._graph_common import MAX_EXAMPLES, Coverage, ObjectKey, UncoveredPart
from idfkit.hvac._categories import category_of
from idfkit.hvac._node_fields import NODE_FIELDS
from idfkit.hvac._port_rules import PORT_RULES
from idfkit.hvac._rule_types import PortRule
from idfkit.hvac.types import (
    ComponentCategory,
    ConnectionType,
    FlowEdge,
    FlowEdgeKind,
    Fluid,
    NodeUse,
    Provenance,
    TopologyFinding,
)

if TYPE_CHECKING:
    from idfkit.document import IDFDocument
    from idfkit.objects import IDFObject
    from idfkit.schema import EpJSONSchema

__all__ = ["HVACTopology"]

# --------------------------------------------------------------------------------------------- #
# Codes: the view stores small integers, decoded only at the boundary.
# --------------------------------------------------------------------------------------------- #

CONNECTIONS: tuple[ConnectionType, ...] = tuple(ConnectionType)
FLUIDS: tuple[Fluid, ...] = tuple(Fluid)
PROVENANCES: tuple[Provenance, ...] = ("eplus_examples", "eplus_test_model", "hand_written")
EDGE_KINDS: tuple[FlowEdgeKind, ...] = ("component", "branch_junction", "zone")
UNCLASSIFIED = -1

_C = {c: i for i, c in enumerate(CONNECTIONS)}
_F = {f: i for i, f in enumerate(FLUIDS)}
_P = {p: i for i, p in enumerate(PROVENANCES)}

PRODUCES = frozenset(
    _C[c]
    for c in (
        ConnectionType.OUTLET,
        ConnectionType.OUTSIDE_AIR,
        ConnectionType.RELIEF_AIR,
        ConnectionType.ZONE_RETURN,
        ConnectionType.ZONE_EXHAUST,
    )
)
"""Roles that put flow into a node. EnergyPlus matches every inlet against one of these."""

CONSUMES = frozenset(_C[c] for c in (ConnectionType.INLET, ConnectionType.ZONE_INLET))
"""Roles that take flow out of a node."""

CONTROLS = frozenset(_C[c] for c in (ConnectionType.SENSOR, ConnectionType.ACTUATOR, ConnectionType.SETPOINT))
"""Roles that read or set a node without carrying flow."""

BOUNDARIES = frozenset(_C[c] for c in (ConnectionType.OUTSIDE_AIR, ConnectionType.RELIEF_AIR))
"""Roles that connect a node to the outdoors."""

ZONE_TYPES = {"ZONEHVAC:EQUIPMENTCONNECTIONS": "Zone", "SPACEHVAC:EQUIPMENTCONNECTIONS": "Space"}
ZONE_VERTEX = {"ZONE": "ZONEHVAC:EQUIPMENTCONNECTIONS", "SPACE": "SPACEHVAC:EQUIPMENTCONNECTIONS"}
"""A zone or space stands in the flow graph as its equipment connections; a start names either."""
"""Object types that stand for a zone or space in the flow graph, and the key type they report."""

CONNECTOR_TYPES = frozenset({"CONNECTOR:SPLITTER", "CONNECTOR:MIXER"})
STRUCTURAL_TYPES = frozenset({"NodeList"})
"""Node-bearing types that only list nodes for other objects; they have no connection of their own."""

EMS_RULE = "ems_key"

# --------------------------------------------------------------------------------------------- #
# Per-type plans, compiled once per schema version.
# --------------------------------------------------------------------------------------------- #


class _Rule(NamedTuple):
    conn: int
    stream: int
    fluid: int
    is_parent: bool
    accepts_nodelist: bool
    when: tuple[str, str] | None
    prov: int


class _FieldPlan(NamedTuple):
    field: str
    """Display field name: ``name`` or ``group.name`` for an extensible sub-field."""
    key: str
    """The key in ``obj.data`` (top level) or in each extensible item."""
    rules: tuple[_Rule, ...]


class _TypePlan(NamedTuple):
    object_type: str
    top: tuple[_FieldPlan, ...]
    wrapper: str | None
    ext: tuple[_FieldPlan, ...]
    classified: bool
    """False when no field of the type has any rule."""


_PLANS: dict[tuple[int, int, int], dict[str, _TypePlan]] = {}


def _compile(rule: PortRule) -> _Rule:
    return _Rule(
        _C[rule.connection],
        rule.stream,
        _F[rule.fluid],
        rule.is_parent,
        rule.accepts_nodelist,
        rule.when,
        _P[rule.provenance],
    )


def _plans_for(schema: EpJSONSchema) -> dict[str, _TypePlan]:
    cached = _PLANS.get(schema.version)
    if cached is not None:
        return cached
    plans: dict[str, _TypePlan] = {}
    for object_type, (top, ext) in NODE_FIELDS.items():
        if object_type in STRUCTURAL_TYPES or schema.get_object_schema(object_type) is None:
            continue
        by_field: dict[str, list[_Rule]] = {}
        for rule in PORT_RULES.get(object_type, ()):
            by_field.setdefault(rule.field, []).append(_compile(rule))
        wrapper = schema.get_extensible_wrapper_key(object_type) if ext else None
        top_plans = tuple(_FieldPlan(f, f, tuple(by_field.get(f, ()))) for f in top)
        ext_plans = tuple(
            _FieldPlan(
                f"{wrapper}.{e}",
                e,
                tuple(by_field.get(f"{wrapper}.{e}", ()) or by_field.get(f"*.{e}", ())),
            )
            for e in ext
            if wrapper is not None
        )
        classified = any(fp.rules for fp in (*top_plans, *ext_plans))
        plans[object_type] = _TypePlan(object_type, top_plans, wrapper, ext_plans, classified)
    _PLANS[schema.version] = plans
    return plans


def _effective(obj: IDFObject, schema: EpJSONSchema, field: str) -> str:
    value = obj.data.get(field)
    if isinstance(value, str) and value:
        return value.upper()
    default = schema.get_field_default(obj.obj_type, field)
    return default.upper() if isinstance(default, str) else ""


def _select(rules: tuple[_Rule, ...], obj: IDFObject, schema: EpJSONSchema) -> _Rule | None:
    """The first rule whose predicate holds, else the unconditional rule, else ``None``."""
    fallback: _Rule | None = None
    for rule in rules:
        if rule.when is None:
            fallback = fallback or rule
        elif _effective(obj, schema, rule.when[0]) == rule.when[1].upper():
            return rule
    return fallback


def _display_name(obj: IDFObject) -> str:
    """The name an object is known by: its name, or for unnamed types the zone or space it serves."""
    if obj.name:
        return obj.name
    for field in ("zone_name", "space_name"):
        value = obj.data.get(field)
        if isinstance(value, str) and value:
            return value
    return obj.obj_type


# --------------------------------------------------------------------------------------------- #
# The view
# --------------------------------------------------------------------------------------------- #

_Use = tuple[int, int, int, int, "str | None"]
"""``(object id or node id, meta id, connection code, stream, NodeList name or None)``."""

_Edge = tuple[int, int, int, int]
"""``(source object id, target object id, node id, edge kind code)``."""

_Meta = tuple[str, int, bool, "int | None", "str | None"]
"""``(field, fluid code, is_parent, provenance code or None, rule tag or None)``."""


class HVACTopology:
    """The node-level HVAC topology of one document, at one revision.

    Build it with :meth:`from_document`, which returns the cached view while the document is
    unchanged. Every query is read-only and answers from integer structures built once.

    Node names compare case-insensitively, as EnergyPlus compares them; answers keep the model's
    spelling.

    Examples:
        >>> from idfkit import new_document
        >>> doc = new_document()
        >>> fan = doc.add("Fan:ConstantVolume", "Fan", air_inlet_node_name="Mixed Air",
        ...               air_outlet_node_name="Supply Air", validate=False)
        >>> topo = HVACTopology.from_document(doc)
        >>> [u.connection.value for u in topo.ports(fan)]
        ['Inlet', 'Outlet']
        >>> HVACTopology.from_document(doc) is topo
        True
    """

    __slots__ = (
        "_coverage",
        "_doc",
        "_edges",
        "_ems_unresolved",
        "_findings",
        "_in_adj",
        "_meta",
        "_node_edges",
        "_node_id",
        "_node_name",
        "_obj",
        "_obj_cat",
        "_obj_index",
        "_obj_key",
        "_obj_lookup",
        "_obj_uses",
        "_out_adj",
        "_uses",
    )

    def __init__(self, doc: IDFDocument) -> None:
        """Build the view of *doc*. Prefer :meth:`from_document`, which caches it."""
        self._doc = doc
        self._node_id: dict[str, int] = {}
        self._node_name: list[str] = []
        self._uses: list[list[_Use]] = []
        self._obj: list[IDFObject] = []
        self._obj_key: list[ObjectKey] = []
        self._obj_cat: list[ComponentCategory] = []
        self._obj_index: dict[int, int] = {}
        self._obj_lookup: dict[tuple[str, str], int] = {}
        self._obj_uses: list[list[_Use]] = []
        self._meta: list[_Meta] = []
        self._edges: list[_Edge] = []
        self._out_adj: list[list[int]] = []
        self._in_adj: list[list[int]] = []
        self._node_edges: list[list[int]] = []
        self._ems_unresolved: list[ObjectKey] = []
        self._coverage = Coverage.of(())
        self._findings: list[TopologyFinding] | None = None
        self._build()

    @classmethod
    def from_document(cls, doc: IDFDocument) -> HVACTopology:
        """Return the topology view of *doc*, built once per document revision.

        Args:
            doc: The document.

        Returns:
            The cached view while ``doc.revision`` is unchanged since it was built, otherwise a new
            view, which is then cached.
        """
        return get_or_build(doc, "hvac", lambda: cls(doc))

    # ----------------------------------------------------------------------------------------- #
    # Build
    # ----------------------------------------------------------------------------------------- #

    def _intern(self, name: str) -> int:
        key = name.upper()
        nid = self._node_id.get(key)
        if nid is None:
            nid = len(self._node_name)
            self._node_id[key] = nid
            self._node_name.append(name)
            self._uses.append([])
            self._node_edges.append([])
        return nid

    def _add_object(self, obj: IDFObject) -> int:
        oid = len(self._obj)
        self._obj.append(obj)
        self._obj_key.append(ObjectKey(obj.obj_type, _display_name(obj)))
        self._obj_cat.append(category_of(obj.obj_type))
        self._obj_index[id(obj)] = oid
        self._obj_lookup.setdefault((obj.obj_type.upper(), _display_name(obj).upper()), oid)
        self._obj_uses.append([])
        self._out_adj.append([])
        self._in_adj.append([])
        return oid

    def _add_use(self, oid: int, node: str, meta: int, conn: int, stream: int, via: str | None) -> None:
        nid = self._intern(node)
        self._uses[nid].append((oid, meta, conn, stream, via))
        self._obj_uses[oid].append((nid, meta, conn, stream, via))

    def _build(self) -> None:  # noqa: C901
        doc = self._doc
        schema = doc.schema
        if schema is None:
            return
        nodelists = self._nodelists()
        metas: dict[tuple[str, _Rule | None, str | None], int] = {}

        def meta_id(field: str, rule: _Rule | None, tag: str | None = None, fluid: int | None = None) -> int:
            key = (field, rule, tag)
            mid = metas.get(key)
            if mid is None:
                mid = len(self._meta)
                if rule is None:
                    self._meta.append((field, fluid if fluid is not None else _F[Fluid.UNKNOWN], False, None, tag))
                else:
                    self._meta.append((field, rule.fluid, rule.is_parent, rule.prov, tag))
                metas[key] = mid
            return mid

        unclassified: list[IDFObject] = []
        for object_type, plan in _plans_for(schema).items():
            if object_type not in doc:
                continue
            for obj in doc.get_collection(object_type):
                oid = self._add_object(obj)
                data = obj.data
                used = False
                for fp in plan.top:
                    value = data.get(fp.key)
                    if isinstance(value, str) and value:
                        used = True
                        self._place(oid, obj, schema, fp, value, nodelists, meta_id)
                if plan.wrapper is not None and plan.ext:
                    for item in obj.extensible_items(plan.wrapper):
                        for fp in plan.ext:
                            value = item.get(fp.key)
                            if isinstance(value, str) and value:
                                used = True
                                self._place(oid, obj, schema, fp, value, nodelists, meta_id)
                if used and not plan.classified:
                    unclassified.append(obj)

        self._add_outdoor_air_nodes(meta_id)
        self._add_connectors(meta_id)
        self._link_flow()
        self._link_loops()
        ems_programs = self._add_ems(meta_id)
        self._coverage = self._make_coverage(unclassified, ems_programs)

    def _nodelists(self) -> dict[str, tuple[str, ...]]:
        lists: dict[str, tuple[str, ...]] = {}
        if "NodeList" in self._doc:
            for nl in self._doc.get_collection("NodeList"):
                names = [str(i.get("node_name", "")) for i in nl.extensible_items("nodes")]
                lists[nl.name.upper()] = tuple(n for n in names if n)
        return lists

    def _place(
        self,
        oid: int,
        obj: IDFObject,
        schema: EpJSONSchema,
        fp: _FieldPlan,
        value: str,
        nodelists: Mapping[str, tuple[str, ...]],
        meta_id: Any,
    ) -> None:
        rule = _select(fp.rules, obj, schema) if fp.rules else None
        mid = cast("int", meta_id(fp.field, rule))
        conn = rule.conn if rule is not None else UNCLASSIFIED
        stream = rule.stream if rule is not None else 1
        accepts = rule.accepts_nodelist if rule is not None else "nodelist" in fp.field
        members = nodelists.get(value.upper()) if accepts else None
        if members is not None:
            # EnergyPlus resolves a NodeList first when the field may name one.
            for member in members:
                self._add_use(oid, member, mid, conn, stream, value)
        else:
            self._add_use(oid, value, mid, conn, stream, None)

    def _add_outdoor_air_nodes(self, meta_id: Any) -> None:
        """An ``OutdoorAir:Node`` is named after the node it declares outdoor air."""
        if "OutdoorAir:Node" not in self._doc:
            return
        rule = _Rule(_C[ConnectionType.OUTSIDE_AIR], 1, _F[Fluid.AIR], False, False, None, _P["eplus_examples"])
        mid = cast("int", meta_id("name", rule))
        for obj in self._doc.get_collection("OutdoorAir:Node"):
            if obj.name:
                self._add_use(self._add_object(obj), obj.name, mid, rule.conn, 1, None)

    def _branch_ends(self) -> dict[str, tuple[str, str]]:
        ends: dict[str, tuple[str, str]] = {}
        if "Branch" in self._doc:
            for branch in self._doc.get_collection("Branch"):
                items = branch.extensible_items("components")
                if items:
                    first = str(items[0].get("component_inlet_node_name", "") or "")
                    last = str(items[-1].get("component_outlet_node_name", "") or "")
                    ends[branch.name.upper()] = (first, last)
        return ends

    def _add_connectors(self, meta_id: Any) -> None:
        """Splitters and mixers name branches, not nodes: they join the last outlet of one branch to
        the first inlet of the next. EnergyPlus reports them as non-parent connections on those nodes.
        """
        if not any(t in self._doc for t in ("Connector:Splitter", "Connector:Mixer")):
            return
        ends = self._branch_ends()
        prov = _P["eplus_examples"]
        inlet = _Rule(_C[ConnectionType.INLET], 1, _F[Fluid.UNKNOWN], False, False, None, prov)
        outlet = _Rule(_C[ConnectionType.OUTLET], 1, _F[Fluid.UNKNOWN], False, False, None, prov)
        for object_type, single, many in (
            ("Connector:Splitter", "inlet_branch_name", "outlet_branch_name"),
            ("Connector:Mixer", "outlet_branch_name", "inlet_branch_name"),
        ):
            if object_type not in self._doc:
                continue
            splitter = object_type == "Connector:Splitter"
            single_mid = cast("int", meta_id(single, inlet if splitter else outlet))
            many_mid = cast("int", meta_id(f"branches.{many}", outlet if splitter else inlet))
            for obj in self._doc.get_collection(object_type):
                oid = self._add_object(obj)
                branch = ends.get(str(obj.data.get(single, "") or "").upper())
                if branch is not None:
                    node = branch[1] if splitter else branch[0]
                    conn = inlet.conn if splitter else outlet.conn
                    if node:
                        self._add_use(oid, node, single_mid, conn, 1, None)
                for item in obj.extensible_items("branches"):
                    branch = ends.get(str(item.get(many, "") or "").upper())
                    if branch is None:
                        continue
                    node = branch[0] if splitter else branch[1]
                    conn = outlet.conn if splitter else inlet.conn
                    if node:
                        self._add_use(oid, node, many_mid, conn, 1, None)

    def _edge_kind(self, a: int, b: int) -> int:
        types = (self._obj[a].obj_type.upper(), self._obj[b].obj_type.upper())
        if any(t in ZONE_TYPES for t in types):
            return 2
        if any(t in CONNECTOR_TYPES for t in types):
            return 1
        return 0

    def _add_edge(self, src: int, dst: int, nid: int, kind: int, seen: set[tuple[int, int, int]]) -> int | None:
        if src == dst or (src, dst, nid) in seen:
            return None
        seen.add((src, dst, nid))
        eid = len(self._edges)
        self._edges.append((src, dst, nid, kind))
        self._out_adj[src].append(eid)
        self._in_adj[dst].append(eid)
        self._node_edges[nid].append(eid)
        return eid

    def _flow_ends(self, nid: int) -> tuple[list[int], list[int]]:
        producers: list[int] = []
        consumers: list[int] = []
        for oid, mid, conn, _, _ in self._uses[nid]:
            if self._meta[mid][2]:  # parent uses add no flow edge
                continue
            if conn in PRODUCES:
                producers.append(oid)
            elif conn in CONSUMES:
                consumers.append(oid)
        return producers, consumers

    def _link_flow(self) -> None:
        seen: set[tuple[int, int, int]] = set()
        for nid in range(len(self._node_name)):
            producers, consumers = self._flow_ends(nid)
            for p in producers:
                for c in consumers:
                    self._add_edge(p, c, nid, self._edge_kind(p, c), seen)

    def _loop_crossings(self) -> Iterable[tuple[str, str]]:
        """Pairs ``(from node, to node)`` that a loop joins internally: supply outlet to demand inlet
        and demand outlet back to supply inlet."""
        doc = self._doc
        lists = self._nodelists()

        def expand(value: object) -> list[str]:
            if not isinstance(value, str) or not value:
                return []
            return list(lists.get(value.upper(), (value,)))

        if "AirLoopHVAC" in doc:
            for loop in doc.get_collection("AirLoopHVAC"):
                data = loop.data
                outs = expand(data.get("supply_side_outlet_node_names"))
                ins = expand(data.get("demand_side_inlet_node_names"))
                # A dual-duct loop pairs its supply outlets with its demand inlets in order.
                yield from zip(outs, ins, strict=False)
                yield from zip(
                    expand(data.get("demand_side_outlet_node_name")),
                    expand(data.get("supply_side_inlet_node_name")),
                    strict=False,
                )
        for loop_type, side in (("PlantLoop", "plant_side"), ("CondenserLoop", "condenser_side")):
            if loop_type not in doc:
                continue
            for loop in doc.get_collection(loop_type):
                data = loop.data
                yield from zip(
                    expand(data.get(f"{side}_outlet_node_name")),
                    expand(data.get("demand_side_inlet_node_name")),
                    strict=False,
                )
                yield from zip(
                    expand(data.get("demand_side_outlet_node_name")),
                    expand(data.get(f"{side}_inlet_node_name")),
                    strict=False,
                )

    def _link_loops(self) -> None:
        seen = {(s, d, n) for s, d, n, _ in self._edges}
        for a, b in self._loop_crossings():
            na = self._node_id.get(a.upper())
            nb = self._node_id.get(b.upper())
            if na is None or nb is None or na == nb:
                continue
            producers, _ = self._flow_ends(na)
            _, consumers = self._flow_ends(nb)
            for p in producers:
                for c in consumers:
                    # The edge passes through both nodes: a start at either one finds it.
                    eid = self._add_edge(p, c, nb, self._edge_kind(p, c), seen)
                    if eid is not None:
                        self._node_edges[na].append(eid)

    def _add_ems(self, meta_id: Any) -> list[IDFObject]:  # noqa: C901
        """Link EMS sensors and actuators whose key names a node, as control uses (rule ``ems_key``).

        Program text is never searched. Keys that name neither a node nor an object are listed by
        :meth:`unresolved_ems`.
        """
        doc = self._doc
        programs: list[IDFObject] = []
        for t in ("EnergyManagementSystem:Program", "EnergyManagementSystem:Subroutine"):
            if t in doc:
                programs.extend(doc.get_collection(t))
        specs = (
            ("EnergyManagementSystem:Sensor", "output_variable_or_output_meter_index_key_name", ConnectionType.SENSOR),
            ("EnergyManagementSystem:Actuator", "actuated_component_unique_name", ConnectionType.ACTUATOR),
        )
        if not any(t in doc for t, _, _ in specs):
            return programs
        names: set[str] | None = None
        prov = _P["hand_written"]
        for object_type, field, connection in specs:
            if object_type not in doc:
                continue
            rule = _Rule(_C[connection], 1, _F[Fluid.UNKNOWN], False, False, None, prov)
            mid = cast("int", meta_id(field, rule, EMS_RULE))
            for obj in doc.get_collection(object_type):
                key = obj.data.get(field)
                if not isinstance(key, str) or not key or key == "*":
                    continue
                if key.upper() in self._node_id:
                    self._add_use(self._add_object(obj), key, mid, rule.conn, 1, None)
                    continue
                if names is None:
                    names = {o.name.upper() for o in doc.all_objects if o.name}
                if key.upper() not in names:
                    self._ems_unresolved.append(ObjectKey(obj.obj_type, obj.name))
        return programs

    def _make_coverage(self, unclassified: list[IDFObject], ems_programs: list[IDFObject]) -> Coverage:
        parts: list[UncoveredPart] = []
        templates = [o for t in self._doc if t.startswith("HVACTemplate:") for o in self._doc.get_collection(t)]
        if templates:
            parts.append(
                UncoveredPart(
                    "hvac_template",
                    len(templates),
                    tuple(ObjectKey(o.obj_type, _display_name(o)) for o in templates[:MAX_EXAMPLES]),
                    "HVACTemplate objects have no nodes until ExpandObjects expands them; their systems are not covered.",
                )
            )
        if ems_programs:
            parts.append(
                UncoveredPart(
                    "ems_program",
                    len(ems_programs),
                    tuple(ObjectKey(o.obj_type, o.name) for o in ems_programs[:MAX_EXAMPLES]),
                    "EMS program text is not parsed; what it controls is not visible.",
                )
            )
        if unclassified:
            parts.append(
                UncoveredPart(
                    "unclassified_type",
                    len(unclassified),
                    tuple(ObjectKey(o.obj_type, _display_name(o)) for o in unclassified[:MAX_EXAMPLES]),
                    "These object types name nodes but have no connection rule; their connections are not known.",
                )
            )
        return Coverage.of(tuple(parts))

    # ----------------------------------------------------------------------------------------- #
    # Lookups
    # ----------------------------------------------------------------------------------------- #

    def _nid(self, node: str) -> int:
        nid = self._node_id.get(node.upper())
        if nid is None:
            msg = f"No node named {node!r} in the model"
            raise KeyError(msg)
        return nid

    def _oid(self, obj: IDFObject) -> int | None:
        oid = self._obj_index.get(id(obj))
        if oid is not None and self._obj[oid] is obj:
            return oid
        object_type = obj.obj_type.upper()
        object_type = ZONE_VERTEX.get(object_type, object_type)
        return self._obj_lookup.get((object_type, _display_name(obj).upper()))

    def _start_nodes(self, name: str) -> list[int]:
        """Node ids for a walk start: the node itself, or every node of a ``NodeList`` of that name."""
        nid = self._node_id.get(name.upper())
        if nid is not None:
            return [nid]
        members = self._nodelists().get(name.upper())
        if members:
            found = [self._node_id[m.upper()] for m in members if m.upper() in self._node_id]
            if found:
                return found
        msg = f"No node or NodeList named {name!r} in the model"
        raise KeyError(msg)

    def _node_use(self, nid: int, use: _Use) -> NodeUse:
        oid, mid, conn, stream, via = use
        field, fluid, is_parent, prov, tag = self._meta[mid]
        return NodeUse(
            node=self._node_name[nid],
            object=self._obj_key[oid],
            category=self._obj_cat[oid],
            field=field,
            connection=CONNECTIONS[conn] if conn != UNCLASSIFIED else None,
            stream=stream,
            fluid=FLUIDS[fluid],
            is_parent=is_parent,
            via_nodelist=via,
            rule=tag,
            provenance=PROVENANCES[prov] if prov is not None else None,
        )

    def _edge(self, eid: int) -> FlowEdge:
        src, dst, nid, kind = self._edges[eid]
        fluid = Fluid.UNKNOWN
        for oid, mid, conn, _, _ in self._uses[nid]:
            if oid == src and conn in PRODUCES:
                fluid = FLUIDS[self._meta[mid][1]]
                break
        if fluid is Fluid.UNKNOWN:
            for oid, mid, conn, _, _ in self._uses[nid]:
                if oid == dst and conn in CONSUMES:
                    fluid = FLUIDS[self._meta[mid][1]]
                    break
        return FlowEdge(self._vertex_key(src), self._vertex_key(dst), self._node_name[nid], fluid, EDGE_KINDS[kind])

    def _vertex_key(self, oid: int) -> ObjectKey:
        """A zone's equipment connections stand for the zone (or space) in the flow graph."""
        key = self._obj_key[oid]
        pseudo = ZONE_TYPES.get(key.object_type.upper())
        return ObjectKey(pseudo, key.name) if pseudo is not None else key

    # ----------------------------------------------------------------------------------------- #
    # Public queries
    # ----------------------------------------------------------------------------------------- #

    def nodes(self) -> list[str]:
        """Every node named anywhere in the model, in the model's spelling."""
        return list(self._node_name)

    def uses(self, node: str) -> list[NodeUse]:
        """Every field of every object that names *node*, parents and unclassified fields included.

        Raises:
            KeyError: If no field names the node.
        """
        nid = self._nid(node)
        return [self._node_use(nid, u) for u in self._uses[nid]]

    def producers(self, node: str) -> list[IDFObject]:
        """The non-parent objects that put flow into *node* (outlets, zone returns and exhausts, boundaries).

        Raises:
            KeyError: If no field names the node.
        """
        producers, _ = self._flow_ends(self._nid(node))
        return [self._obj[o] for o in dict.fromkeys(producers)]

    def consumers(self, node: str) -> list[IDFObject]:
        """The non-parent objects that take flow from *node* (inlets and zone inlets).

        Raises:
            KeyError: If no field names the node.
        """
        _, consumers = self._flow_ends(self._nid(node))
        return [self._obj[o] for o in dict.fromkeys(consumers)]

    def controls(self, node: str) -> list[NodeUse]:
        """The sensor, actuator and setpoint uses of *node*, EMS uses (rule ``ems_key``) included.

        Raises:
            KeyError: If no field names the node.
        """
        nid = self._nid(node)
        return [self._node_use(nid, u) for u in self._uses[nid] if u[2] in CONTROLS]

    def ports(self, obj: IDFObject) -> list[NodeUse]:
        """Every node use of *obj*, ordered by stream. Empty for an object with no node fields.

        A ``Zone`` or ``Space`` answers with the node uses of its equipment connections.
        """
        oid = self._oid(obj)
        if oid is None:
            return []
        uses = sorted(self._obj_uses[oid], key=lambda u: u[3])
        return [self._node_use(nid, (oid, mid, conn, stream, via)) for nid, mid, conn, stream, via in uses]

    def downstream(
        self,
        start: IDFObject | str,
        *,
        hops: int = 2,
        categories: Collection[ComponentCategory] | None = None,
    ) -> list[FlowEdge]:
        """The flow edges reached going downstream from a component or a node, breadth first.

        Args:
            start: A component; a ``Zone`` or ``Space`` (walked as its equipment connections); a
                node name; or a ``NodeList`` name, which starts from every node it lists. The walk
                follows every stream of each component it passes, so it can cross from air to water
                at a coil.
            hops: The most edges walked from the start. ``0`` returns nothing.
            categories: When given, keep only edges whose downstream end is a component of one of
                these categories. The walk still passes through components of other categories.

        Returns:
            The edges in breadth-first order.

        Raises:
            KeyError: If *start* is a name that is neither a node nor a ``NodeList`` of used nodes,
                or an object with no connections in this view.
            ValueError: If *hops* is negative.
        """
        return self._walk(start, hops, categories, downstream=True)

    def upstream(
        self,
        start: IDFObject | str,
        *,
        hops: int = 2,
        categories: Collection[ComponentCategory] | None = None,
    ) -> list[FlowEdge]:
        """The flow edges reached going upstream from a component or a node, breadth first.

        Args:
            start: A component; a ``Zone`` or ``Space`` (walked as its equipment connections); a
                node name; or a ``NodeList`` name, which starts from every node it lists. The walk
                follows every stream of each component it passes, so it can cross from air to water
                at a coil.
            hops: The most edges walked from the start. ``0`` returns nothing.
            categories: When given, keep only edges whose upstream end is a component of one of
                these categories. The walk still passes through components of other categories.

        Returns:
            The edges in breadth-first order.

        Raises:
            KeyError: If *start* is a name that is neither a node nor a ``NodeList`` of used nodes,
                or an object with no connections in this view.
            ValueError: If *hops* is negative.
        """
        return self._walk(start, hops, categories, downstream=False)

    def _walk(  # noqa: C901
        self,
        start: IDFObject | str,
        hops: int,
        categories: Collection[ComponentCategory] | None,
        *,
        downstream: bool,
    ) -> list[FlowEdge]:
        if hops < 0:
            msg = f"hops must not be negative, got {hops}"
            raise ValueError(msg)
        keep = frozenset(categories) if categories is not None else None
        adj = self._out_adj if downstream else self._in_adj
        far = 1 if downstream else 0
        found: list[int] = []
        seen_edges: set[int] = set()
        visited: set[int] = set()
        queue: deque[tuple[int, int]] = deque()

        def take(eid: int, depth: int) -> None:
            if eid in seen_edges:
                return
            seen_edges.add(eid)
            end = self._edges[eid][far]
            if keep is None or self._obj_cat[end] in keep:
                found.append(eid)
            if end not in visited:
                visited.add(end)
                queue.append((end, depth))

        if hops == 0:
            return []
        if isinstance(start, str):
            for nid in self._start_nodes(start):
                for eid in self._node_edges[nid]:
                    take(eid, 1)
        else:
            oid = self._oid(start)
            if oid is None:
                msg = f"{start.obj_type} {start.name!r} has no HVAC connections in this view"
                raise KeyError(msg)
            visited.add(oid)
            queue.append((oid, 0))
        while queue:
            oid, depth = queue.popleft()
            if depth >= hops:
                continue
            for eid in adj[oid]:
                take(eid, depth + 1)
        return [self._edge(e) for e in found]

    def check(self) -> list[TopologyFinding]:
        """Run the static connection checks; computed once per view.

        Severities are effective: a qualified check may be an error, a finding that relies on a
        ``hand_written`` rule never is, and a model of an earlier EnergyPlus version is capped by the
        measured table (FR-013a). A clean result is QA, not proof the model simulates.

        Returns:
            The findings, branch checks first.
        """
        if self._findings is None:
            from idfkit.hvac._index import TopologyIndex
            from idfkit.hvac.checks import run_checks

            loop_types = {"AIRLOOPHVAC", "PLANTLOOP", "CONDENSERLOOP"}
            loop_nodes = frozenset(
                use[0]
                for oid, obj in enumerate(self._obj)
                if obj.obj_type.upper() in loop_types
                for use in self._obj_uses[oid]
            )
            index = TopologyIndex(
                doc=self._doc,
                node_name=self._node_name,
                node_id=self._node_id,
                uses=self._uses,
                obj=self._obj,
                obj_key=self._obj_key,
                obj_cat=self._obj_cat,
                obj_uses=self._obj_uses,
                meta=self._meta,
                loop_nodes=loop_nodes,
                coverage=self._coverage,
            )
            self._findings = run_checks(index)
        return list(self._findings)

    @property
    def coverage(self) -> Coverage:
        """What the view does not cover: unexpanded templates, EMS programs, unclassified types."""
        return self._coverage

    def unresolved_ems(self) -> list[ObjectKey]:
        """EMS sensors and actuators whose key names neither a node nor any object in the model."""
        return list(self._ems_unresolved)
