"""Public types of the combined model graph.

The vocabulary is closed within a release: adding a node kind, an edge kind or a layer is a minor
change, never a breaking one (FR-056). Code that reads kinds must ignore members it does not know.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Final, Literal, TypeAlias, Union

from idfkit._graph_common import Coverage, ObjectKey

__all__ = [
    "EdgeKind",
    "GraphEdge",
    "GraphNode",
    "JSONValue",
    "Layer",
    "NodeKind",
    "Subgraph",
]

NodeKind = Literal["object", "node", "result_fact", "message"]
"""What a graph node stands for: a model object, a fluid node, a simulation result fact or a message."""

EdgeKind = Literal["reference", "flow", "control", "membership", "result_link"]
"""What a graph edge stands for. ``reference`` is a field naming another object; ``flow`` a field
naming a node the object takes flow from or puts flow into; ``control`` a sensor, actuator or setpoint
use of a node; ``membership`` a component on a loop; ``result_link`` a result linked to an object."""

Layer = Literal["model", "topology", "results"]
"""The layer a node or edge comes from. ``model`` and ``topology`` are always present."""

JSONValue: TypeAlias = Union[None, bool, int, float, str, list["JSONValue"], dict[str, "JSONValue"]]  # noqa: UP007
"""A value the standard library's ``json`` module writes and reads back unchanged."""

Scalar: TypeAlias = "str | int | float | bool | None"
"""The values a graph node or edge attribute can hold."""

NODE_LAYER: Final[Mapping[NodeKind, Layer]] = {
    "object": "model",
    "node": "topology",
    "result_fact": "results",
    "message": "results",
}
"""The layer of each node kind. Fixed by the kind."""

EDGE_LAYER: Final[Mapping[EdgeKind, Layer]] = {
    "reference": "model",
    "flow": "topology",
    "control": "topology",
    "membership": "topology",
    "result_link": "results",
}
"""The layer of each edge kind. Fixed by the kind."""


@dataclass(frozen=True, slots=True)
class GraphNode:
    """One node of the combined graph.

    Attributes:
        id: Stable composite id, such as ``object:ZONE:SPACE1-1`` or ``node:SUPPLY INLET NODE``.
            Names are upper-cased, so equal ids mean equal identity.
        kind: What the node stands for.
        layer: The layer it comes from, fixed by ``kind``.
        key: The object, for an ``object`` node; the owner, for a ``result_fact``. ``None`` otherwise.
        node: The node name in the model's spelling, for a ``node`` node. ``None`` otherwise.
        label: Short display text, such as ``Zone "SPACE1-1"``.
        attrs: Kind-specific scalars: ``category`` for objects, ``fluid`` for nodes.
    """

    id: str
    kind: NodeKind
    layer: Layer
    key: ObjectKey | None
    node: str | None
    label: str
    attrs: Mapping[str, Scalar] = field(default_factory=dict[str, "Scalar"])


@dataclass(frozen=True, slots=True)
class GraphEdge:
    """One directed edge of the combined graph.

    Attributes:
        source: The graph node id the edge leaves.
        target: The graph node id the edge enters.
        kind: What the edge stands for.
        layer: The layer it comes from, fixed by ``kind``.
        key: Unique among the edges joining the same two nodes, such as ``reference:zone_name``
            or ``flow:air_outlet_node_name``.
        attrs: Kind-specific scalars: ``field``, ``connection_type``, ``fluid``, ``provenance``,
            ``side``, ``branch``, ``position``, ``loop_kind``, ``rule``, ``confidence``.
    """

    source: str
    target: str
    kind: EdgeKind
    layer: Layer
    key: str
    attrs: Mapping[str, Scalar] = field(default_factory=dict[str, "Scalar"])


@dataclass(frozen=True, slots=True)
class Subgraph:
    """The bounded neighbourhood of one graph node.

    Attributes:
        start: The graph node id the walk started from.
        nodes: The nodes returned, in breadth-first order from ``start``.
        edges: The edges between returned nodes, in the order the walk found them.
        layers: The layers present in the view.
        unavailable: Each layer missing from the view, and why.
        coverage: What the view could not see: templates, EMS programs, unclassified types.
        truncated: True when the hop or node bound cut the walk.
        omitted_nodes: Nodes reached but not returned. A lower bound, since the walk stops at the cut.
        frontier: Returned node ids with neighbours that were not returned.
        results_state: ``"fresh"`` or ``"stale"`` when the results layer is present, else ``None``.
    """

    start: str
    nodes: list[GraphNode]
    edges: list[GraphEdge]
    layers: list[Layer]
    unavailable: dict[Layer, str]
    coverage: Coverage
    truncated: bool
    omitted_nodes: int
    frontier: list[str]
    results_state: Literal["fresh", "stale"] | None = None
