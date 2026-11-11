"""Walk-time adapters over the model, topology and results layers.

Nothing here is stored between calls: a walker is made for one walk or one export, answers "the
neighbours of this graph node" from each layer's own index, and builds dataclasses only for what it
returns (research R-21, R-23). The view adds no domain logic: every edge is a field the reference
graph or the HVAC topology already knows.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Collection, Iterator, Mapping
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, cast

from idfkit._graph_common import ObjectKey, display_name
from idfkit.graph.types import EDGE_LAYER, NODE_LAYER, EdgeKind, GraphEdge, GraphNode, NodeKind, Scalar
from idfkit.hvac import ConnectionType, Fluid, HVACTopology, LoopMembership, NodeUse, category_of

if TYPE_CHECKING:
    from idfkit.document import IDFDocument
    from idfkit.objects import IDFObject
    from idfkit.simulation.linking import LinkedMessage, ResultFact, ResultIndex

NODE_KINDS: tuple[NodeKind, ...] = tuple(NODE_LAYER)
EDGE_KINDS: tuple[EdgeKind, ...] = tuple(EDGE_LAYER)

_CONTROL = frozenset({ConnectionType.SENSOR, ConnectionType.ACTUATOR, ConnectionType.SETPOINT})
_INTO_OBJECT = frozenset({ConnectionType.INLET, ConnectionType.ZONE_INLET})
_LOOP_HOLDERS = frozenset({
    "AIRLOOPHVAC",
    "PLANTLOOP",
    "CONDENSERLOOP",
    "ZONEHVAC:EQUIPMENTCONNECTIONS",
    "SPACEHVAC:EQUIPMENTCONNECTIONS",
})
"""Types a membership edge can enter: the loops, and the equipment connections of zone equipment."""


class FactItem(NamedTuple):
    """A ``result_fact`` graph node: one fact and the object or node it belongs to."""

    owner: ObjectKey
    fact: ResultFact


class MessageItem(NamedTuple):
    """A ``message`` graph node: one message and its position in the run."""

    position: int
    message: LinkedMessage


Payload: TypeAlias = "IDFObject | str | FactItem | MessageItem"
"""What a graph node stands for: an object, a node name, a result fact or a message."""


class RawEdge(NamedTuple):
    source: str
    target: str
    kind: EdgeKind
    key: str
    attrs: dict[str, Scalar]


def node_id(name: str) -> str:
    """The graph node id of a fluid node."""
    return f"node:{name.upper()}"


def known(values: Collection[str] | None, vocabulary: tuple[str, ...]) -> frozenset[str]:
    """The members of *values* that are in *vocabulary*; all of it when *values* is ``None``."""
    if values is None:
        return frozenset(vocabulary)
    return frozenset(str(v) for v in values) & frozenset(vocabulary)


class Walker:
    """Answers neighbour queries over the model, topology and results layers of one document revision."""

    __slots__ = (
        "_by_display",
        "_collections",
        "_doc",
        "_edge_kinds",
        "_found",
        "_ids",
        "_messages_of",
        "_node_kinds",
        "_refs",
        "_results",
        "_stale",
        "_targets",
        "_topo",
    )

    def __init__(
        self,
        doc: IDFDocument[Any],
        *,
        node_kinds: Collection[str] | None = None,
        edge_kinds: Collection[str] | None = None,
        results: ResultIndex | None = None,
    ) -> None:
        self._doc = doc
        self._results = results
        self._stale = results is not None and not results.is_fresh(doc)
        self._messages_of: dict[ObjectKey, list[int]] | None = None
        self._topo = HVACTopology.from_document(doc)
        self._refs = doc.references
        self._node_kinds = known(node_kinds, NODE_KINDS)
        self._edge_kinds = known(edge_kinds, EDGE_KINDS)
        self._ids: dict[int, str] = {}
        self._found: dict[tuple[str, str], IDFObject | None] = {}
        self._collections = {t.upper(): c for t, c in doc.collections.items()}
        self._by_display: dict[str, dict[str, IDFObject]] = {}
        self._targets: dict[tuple[str, str], frozenset[str]] = {}

    @property
    def topology(self) -> HVACTopology:
        return self._topo

    @property
    def results(self) -> ResultIndex | None:
        return self._results

    @property
    def document(self) -> IDFDocument[Any]:
        return self._doc

    # ------------------------------------------------------------------------------------------ #
    # Identity
    # ------------------------------------------------------------------------------------------ #

    def object_id(self, obj: IDFObject) -> str:
        """``object:<TYPE>:<NAME>``; an object with no name and no zone gets its index in its type."""
        cached = self._ids.get(id(obj))
        if cached is not None:
            return cached
        name = display_name(obj)
        if not obj.name and name == obj.obj_type:
            index = next(i for i, o in enumerate(self._doc.get_collection(obj.obj_type)) if o is obj)
            name = f"#{index}"
        vid = f"object:{obj.obj_type.upper()}:{name.upper()}"
        self._ids[id(obj)] = vid
        return vid

    def find(self, key: ObjectKey) -> IDFObject | None:
        """The object a key names: by name, then by the zone or space an unnamed object serves."""
        return self.named(key.object_type, key.name, by_display=True)

    def named(self, object_type: str, name: str, *, by_display: bool = False) -> IDFObject | None:
        """The object of *object_type* called *name*, in any letter case.

        With *by_display*, an unnamed object is also found by the zone or space it serves, as the
        topology keys it.
        """
        cache_key = (object_type.upper(), name.upper())
        if cache_key in self._found:
            return self._found[cache_key]
        collection = self._collections.get(cache_key[0])
        found = collection.get(name) if collection is not None else None
        if found is None and by_display and collection is not None:
            index: dict[str, IDFObject] | None = self._by_display.get(cache_key[0])
            if index is None:
                index = {}
                for obj in collection:
                    index.setdefault(display_name(obj).upper(), obj)
                self._by_display[cache_key[0]] = index
            found = index.get(cache_key[1])
        if found is not None or by_display:
            self._found[cache_key] = found
        return found

    def start(self, target: ObjectKey | str) -> tuple[str, Payload]:
        """The graph node id and payload of a walk start.

        Raises:
            KeyError: If the object or node is not in the model.
        """
        if isinstance(target, ObjectKey):
            obj = self.find(target)
            if obj is None:
                msg = f"No {target.object_type} named {target.name!r} in the model"
                raise KeyError(msg)
            return self.object_id(obj), obj
        uses = self._topo.uses(target)
        name = uses[0].node if uses else target
        return node_id(name), name

    # ------------------------------------------------------------------------------------------ #
    # Graph nodes
    # ------------------------------------------------------------------------------------------ #

    def kind_of(self, payload: Payload) -> NodeKind:
        if isinstance(payload, str):
            return "node"
        if isinstance(payload, FactItem):
            return "result_fact"
        if isinstance(payload, MessageItem):
            return "message"
        return "object"

    def graph_node(self, vid: str, payload: Payload) -> GraphNode:
        if isinstance(payload, FactItem):
            return self._fact_node(vid, payload)
        if isinstance(payload, MessageItem):
            return self._message_node(vid, payload)
        if isinstance(payload, str):
            return GraphNode(
                vid, "node", "topology", None, payload, f'Node "{payload}"', {"fluid": self._fluid(payload)}
            )
        name = display_name(payload)
        key = ObjectKey(payload.obj_type, name)
        attrs: dict[str, Scalar] = {"category": category_of(payload.obj_type).value}
        return GraphNode(vid, "object", "model", key, None, f'{payload.obj_type} "{name}"', attrs)

    def category(self, payload: Payload) -> str | None:
        if isinstance(payload, (str, FactItem, MessageItem)):
            return None
        return category_of(payload.obj_type).value

    def _fact_node(self, vid: str, item: FactItem) -> GraphNode:
        fact = item.fact
        units = f" {fact.units}" if fact.units else ""
        attrs: dict[str, Scalar] = {
            "metric": fact.metric,
            "value": fact.value,
            "units": fact.units,
            "source": fact.source,
            "where": fact.where,
            "multiplier": fact.multiplier,
            "stale": self._stale,
        }
        return GraphNode(vid, "result_fact", "results", item.owner, None, f"{fact.metric} = {fact.value}{units}", attrs)

    def _message_node(self, vid: str, item: MessageItem) -> GraphNode:
        message = item.message
        attrs: dict[str, Scalar] = {
            "severity": message.severity,
            "message_kind": message.kind,
            "text": message.text,
            "occurrences": message.occurrences,
            "first_seen": message.first_seen,
            "stale": self._stale,
        }
        return GraphNode(vid, "message", "results", None, None, f"{message.severity} {message.kind}", attrs)

    def _fluid(self, name: str) -> str:
        for use in self._topo.uses(name):
            if use.fluid is not Fluid.UNKNOWN:
                return use.fluid.value
        return Fluid.UNKNOWN.value

    # ------------------------------------------------------------------------------------------ #
    # Neighbours
    # ------------------------------------------------------------------------------------------ #

    def neighbours(self, vid: str, payload: Payload) -> Iterator[tuple[RawEdge, str, Payload]]:
        """Every edge at *vid*, either direction, with the graph node at its other end."""
        if isinstance(payload, (FactItem, MessageItem)):
            yield from self._result_owners(vid, payload)
            return
        if isinstance(payload, str):
            yield from self._node_neighbours(vid, payload)
            yield from self._results_at(vid, ObjectKey("Node", payload))
            return
        if "reference" in self._edge_kinds and "object" in self._node_kinds:
            yield from self._references_out(vid, payload)
            yield from self._references_in(vid, payload)
        yield from self._ports(vid, payload)
        if "membership" in self._edge_kinds and "object" in self._node_kinds:
            yield from self._memberships(vid, payload)
            if payload.obj_type.upper() in _LOOP_HOLDERS:
                yield from self._members(vid, payload)
        yield from self._results_at(vid, ObjectKey(payload.obj_type, display_name(payload)))

    def out_edges(self, vid: str, payload: IDFObject) -> Iterator[tuple[RawEdge, str, Payload]]:
        """The edges an object contributes once to a whole-model export: those it is the owner of."""
        if "reference" in self._edge_kinds and "object" in self._node_kinds:
            yield from self._references_out(vid, payload)
        yield from self._ports(vid, payload)
        if "membership" in self._edge_kinds and "object" in self._node_kinds:
            yield from self._memberships(vid, payload)

    def _node_neighbours(self, vid: str, name: str) -> Iterator[tuple[RawEdge, str, Payload]]:
        if "object" not in self._node_kinds:
            return
        for use in self._topo.uses(name):
            obj = self.find(use.object)
            if obj is None:
                continue
            oid = self.object_id(obj)
            edge = self._use_edge(use, oid, vid)
            if edge is not None:
                yield edge, oid, obj

    def _ports(self, vid: str, obj: IDFObject) -> Iterator[tuple[RawEdge, str, Payload]]:
        if "node" not in self._node_kinds or not self._edge_kinds & {"flow", "control"}:
            return
        own = ObjectKey(obj.obj_type, display_name(obj))
        for use in self._topo.ports(obj):
            if use.object != own:
                # A zone answers with its equipment connections' uses; those are that object's edges.
                continue
            nid = node_id(use.node)
            edge = self._use_edge(use, vid, nid)
            if edge is not None:
                yield edge, nid, use.node

    def _use_edge(self, use: NodeUse, oid: str, nid: str) -> RawEdge | None:
        conn = use.connection
        attrs: dict[str, Scalar] = {
            "field": use.field,
            "connection_type": conn.value if conn is not None else None,
            "provenance": use.provenance,
        }
        if use.via_nodelist is not None:
            attrs["via_nodelist"] = use.via_nodelist
        if conn in _CONTROL:
            if "control" not in self._edge_kinds:
                return None
            if use.rule == "ems_key":
                attrs["rule"] = "ems_key"
                attrs["confidence"] = "convention"
            return RawEdge(oid, nid, "control", f"control:{use.field}", attrs)
        if "flow" not in self._edge_kinds:
            return None
        attrs["fluid"] = use.fluid.value
        if conn in _INTO_OBJECT:
            return RawEdge(nid, oid, "flow", f"flow:{use.field}", attrs)
        return RawEdge(oid, nid, "flow", f"flow:{use.field}", attrs)

    def _target_types(self, obj_type: str, field: str) -> frozenset[str]:
        """The object types (upper case) a reference field can name, from its object lists."""
        cache_key = (obj_type.upper(), field)
        cached = self._targets.get(cache_key)
        if cached is not None:
            return cached
        schema = self._doc.schema
        types: set[str] = set()
        if schema is not None:
            lists = schema.get_field_object_list(obj_type, field)
            if lists is None:
                lists = _extensible_object_list(
                    schema.get_inner_schema(obj_type), schema.get_extensible_wrapper_key(obj_type), field
                )
            for list_name in lists or ():
                types.update(t.upper() for t in schema.get_types_providing_reference(list_name))
        result = frozenset(types)
        self._targets[cache_key] = result
        return result

    def _references_out(self, vid: str, obj: IDFObject) -> Iterator[tuple[RawEdge, str, Payload]]:
        for name, field in sorted(self._refs.get_references_with_fields(obj), key=lambda p: (p[1], p[0])):
            for target_type in sorted(self._target_types(obj.obj_type, field)):
                target = self.named(target_type, name)
                if target is None or target is obj:
                    continue
                tid = self.object_id(target)
                yield RawEdge(vid, tid, "reference", f"reference:{field}", {"field": field}), tid, target

    def _references_in(self, vid: str, obj: IDFObject) -> Iterator[tuple[RawEdge, str, Payload]]:
        if not obj.name:
            return
        own_type = obj.obj_type.upper()
        edges = self._refs.get_referencing_with_fields(obj.name)
        for source, field in sorted(edges, key=lambda p: (p[0].obj_type, p[0].name, p[1])):
            if source is obj or own_type not in self._target_types(source.obj_type, field):
                continue
            sid = self.object_id(source)
            yield RawEdge(sid, vid, "reference", f"reference:{field}", {"field": field}), sid, source

    def _memberships(self, vid: str, obj: IDFObject) -> Iterator[tuple[RawEdge, str, Payload]]:
        for membership in self._topo.memberships(obj):
            loop = self.find(membership.loop)
            if loop is None:
                continue
            lid = self.object_id(loop)
            yield _membership_edge(vid, lid, membership), lid, loop

    def _members(self, vid: str, loop: IDFObject) -> Iterator[tuple[RawEdge, str, Payload]]:
        key = ObjectKey(loop.obj_type, display_name(loop))
        for member, membership in self._topo._members_of(key):  # pyright: ignore[reportPrivateUsage]
            mid = self.object_id(member)
            yield _membership_edge(mid, vid, membership), mid, member

    # ------------------------------------------------------------------------------------------ #
    # Results
    # ------------------------------------------------------------------------------------------ #

    def fact_id(self, owner: ObjectKey, fact: ResultFact) -> str:
        """``fact:<TYPE>:<NAME>:<where>``: stable for the same model and the same report location."""
        return f"fact:{owner.object_type.upper()}:{owner.name.upper()}:{fact.where}"

    @staticmethod
    def message_id(index: int, message: LinkedMessage) -> str:
        """``message:<kind>:<index>``, the message's position in the run's ``Errors`` order."""
        return f"message:{message.kind}:{index}"

    def _messages_naming(self, key: ObjectKey) -> list[int]:
        if self._results is None:
            return []
        if self._messages_of is None:
            index: dict[ObjectKey, list[int]] = {}
            for position, message in enumerate(self._results.messages):
                for link in message.objects:
                    if link.key is not None:
                        index.setdefault(link.key, []).append(position)
            self._messages_of = index
        return self._messages_of.get(key, [])

    def _link_attrs(self, key: ObjectKey) -> dict[str, Scalar]:
        link = self._results.link(key) if self._results is not None else None
        if link is None:
            return {"confidence": None, "rule": None}
        return {"confidence": link.confidence, "rule": link.rule}

    def _results_at(self, vid: str, key: ObjectKey) -> Iterator[tuple[RawEdge, str, Payload]]:
        """The facts and messages linked to the object or node *key*, each joined by a ``result_link``."""
        results = self._results
        if results is None or "result_link" not in self._edge_kinds:
            return
        if "result_fact" in self._node_kinds:
            attrs = self._link_attrs(key)
            for fact in results.facts(key):
                fid = self.fact_id(key, fact)
                yield RawEdge(fid, vid, "result_link", "result_link", attrs), fid, FactItem(key, fact)
        if "message" in self._node_kinds:
            for position in self._messages_naming(key):
                message = results.messages[position]
                mid = self.message_id(position, message)
                link = next((ln for ln in message.objects if ln.key == key), None)
                attrs: dict[str, Scalar] = {
                    "confidence": link.confidence if link is not None else None,
                    "rule": link.rule if link is not None else None,
                }
                yield RawEdge(mid, vid, "result_link", "result_link", attrs), mid, MessageItem(position, message)

    def _result_owners(self, vid: str, item: FactItem | MessageItem) -> Iterator[tuple[RawEdge, str, Payload]]:
        """The objects and nodes a fact or message is linked to."""
        if "result_link" not in self._edge_kinds:
            return
        owners: list[tuple[ObjectKey, dict[str, Scalar]]]
        if isinstance(item, FactItem):
            owners = [(item.owner, self._link_attrs(item.owner))]
        else:
            owners = [
                (ln.key, {"confidence": ln.confidence, "rule": ln.rule})
                for ln in item.message.objects
                if ln.key is not None
            ]
        for owner, attrs in owners:
            target = self._owner(owner)
            if target is not None:
                yield RawEdge(vid, target[0], "result_link", "result_link", attrs), target[0], target[1]

    def _owner(self, key: ObjectKey) -> tuple[str, Payload] | None:
        if key.object_type.upper() == "NODE":
            if "node" not in self._node_kinds:
                return None
            uses = self._topo.uses(key.name)
            name = uses[0].node if uses else key.name
            return node_id(name), name
        if "object" not in self._node_kinds:
            return None
        obj = self.find(key)
        return (self.object_id(obj), obj) if obj is not None else None


def _membership_edge(member: str, loop: str, membership: LoopMembership) -> RawEdge:
    attrs: dict[str, Scalar] = {
        "side": membership.side,
        "branch": membership.branch.name if membership.branch is not None else None,
        "position": membership.position,
        "loop_kind": membership.kind,
    }
    return RawEdge(member, loop, "membership", f"membership:{membership.kind}", attrs)


def _extensible_object_list(inner: Mapping[str, Any] | None, wrapper: str | None, field: str) -> list[str] | None:
    """The object lists of a field inside an extensible group."""
    if inner is None or wrapper is None:
        return None
    group = cast("Mapping[str, Any]", inner.get("properties", {})).get(wrapper)
    if not isinstance(group, dict):
        return None
    items = cast("dict[str, Any]", group).get("items", {})
    if not isinstance(items, dict):
        return None
    props = cast("Mapping[str, Any]", cast("dict[str, Any]", items).get("properties", {}))
    spec = props.get(field)
    if not isinstance(spec, dict):
        return None
    lists = cast("dict[str, Any]", spec).get("object_list")
    return cast("list[str]", lists) if isinstance(lists, list) else None


# ---------------------------------------------------------------------------------------------- #
# Breadth-first walk
# ---------------------------------------------------------------------------------------------- #


class Walk(NamedTuple):
    start: str
    nodes: list[GraphNode]
    edges: list[GraphEdge]
    truncated: bool
    omitted: int
    frontier: list[str]


class _Reach(NamedTuple):
    order: list[str]
    payloads: dict[str, Payload]
    parent: dict[str, str | None]
    edges: dict[tuple[str, str, str], RawEdge]
    others: dict[str, set[str]]
    expanded: set[str]


def walk(
    walker: Walker,
    start: ObjectKey | str,
    *,
    hops: int,
    categories: Collection[str] | None,
    max_nodes: int | None,
) -> Walk:
    """Breadth-first search from *start*, up to *hops* hops and *max_nodes* nodes.

    With *categories*, the walk first reaches every node within *hops*, keeps the start, the object
    nodes of those categories and the non-object nodes on the breadth-first paths to them, then
    applies the node bound in breadth-first order.
    """
    sid, first = walker.start(start)
    reach = _reach(walker, sid, first, hops, max_nodes if categories is None else None)
    kept = reach.order
    if categories is not None:
        kept = _keep(walker, reach.order, reach.payloads, reach.parent, frozenset(categories), sid)
    # Nodes the category filter left out are not a cut, so they make no frontier.
    filtered = set(reach.order).difference(kept)
    dropped_by_bound = 0
    if max_nodes is not None and len(kept) > max_nodes:
        dropped_by_bound = len(kept) - max_nodes
        kept = kept[:max_nodes]
    returned = set(kept)

    frontier: list[str] = []
    omitted: set[str] = set()
    for vid in kept:
        others = reach.others.setdefault(vid, set())
        if vid not in reach.expanded:
            for edge, other, _ in walker.neighbours(vid, reach.payloads[vid]):
                if other in returned:
                    _record(reach, edge)
                elif other not in filtered:
                    others.add(other)
        outside = [o for o in others if o not in returned and o not in filtered]
        if outside:
            frontier.append(vid)
            omitted.update(outside)

    nodes = [walker.graph_node(vid, reach.payloads[vid]) for vid in kept]
    graph_edges = [
        GraphEdge(e.source, e.target, e.kind, EDGE_LAYER[e.kind], e.key, e.attrs)
        for e in reach.edges.values()
        if e.source in returned and e.target in returned
    ]
    total_omitted = max(len(omitted), dropped_by_bound)
    return Walk(sid, nodes, graph_edges, bool(frontier) or dropped_by_bound > 0, total_omitted, frontier)


def _record(reach: _Reach, edge: RawEdge) -> None:
    reach.edges.setdefault((edge.source, edge.target, edge.key), edge)
    reach.others.setdefault(edge.source, set()).add(edge.target)
    reach.others.setdefault(edge.target, set()).add(edge.source)


def _reach(walker: Walker, sid: str, first: Payload, hops: int, limit: int | None) -> _Reach:
    """Every node within *hops* of *sid*, breadth first, stopping when *limit* nodes are reached."""
    reach = _Reach([sid], {sid: first}, {sid: None}, {}, {}, set())
    depth = {sid: 0}
    queue = deque([sid])
    while queue:
        vid = queue.popleft()
        if depth[vid] >= hops:
            continue
        for edge, other, payload in walker.neighbours(vid, reach.payloads[vid]):
            if other not in depth:
                if limit is not None and len(reach.order) >= limit:
                    return reach
                depth[other] = depth[vid] + 1
                reach.parent[other] = vid
                reach.payloads[other] = payload
                reach.order.append(other)
                queue.append(other)
            _record(reach, edge)
        reach.expanded.add(vid)
    return reach


def _keep(
    walker: Walker,
    order: list[str],
    payloads: dict[str, Payload],
    parent: dict[str, str | None],
    categories: frozenset[str],
    start: str,
) -> list[str]:
    keep: set[str] = {start}
    for vid in order:
        category = walker.category(payloads[vid])
        if category is None or category not in categories:
            continue
        keep.add(vid)
        step = parent[vid]
        while step is not None and step not in keep:
            if walker.kind_of(payloads[step]) != "object":
                keep.add(step)
            step = parent[step]
    return [vid for vid in order if vid in keep]
