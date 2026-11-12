"""The combined model graph: one walkable view over a model's objects and fluid nodes.

``ModelGraph`` joins the reference graph (``object`` nodes, ``reference`` edges) and the HVAC
topology (``node`` nodes; ``flow``, ``control`` and ``membership`` edges) under one closed
vocabulary, walks a bounded neighbourhood of any object or node, and exports node-link JSON that
networkx 3.6 or later reads unchanged. Each layer stays usable on its own; the view adds no domain
logic and copies no data.

Examples:
    >>> from idfkit import new_document
    >>> from idfkit.graph import ModelGraph
    >>> from idfkit.hvac import ObjectKey
    >>> doc = new_document()
    >>> _ = doc.add("Zone", "Office")
    >>> sub = ModelGraph(doc).neighbourhood(ObjectKey("Zone", "Office"), hops=1)
    >>> sub.start, sub.truncated
    ('object:ZONE:OFFICE', False)
"""

from __future__ import annotations

from idfkit._graph_common import Coverage, ObjectKey
from idfkit.graph.node_link import NODE_LINK_FORMAT_VERSION, save_node_link, write_node_link
from idfkit.graph.types import EdgeKind, GraphEdge, GraphNode, JSONValue, Layer, NodeKind, Subgraph
from idfkit.graph.view import ModelGraph

__all__ = [
    "NODE_LINK_FORMAT_VERSION",
    "Coverage",
    "EdgeKind",
    "GraphEdge",
    "GraphNode",
    "JSONValue",
    "Layer",
    "ModelGraph",
    "NodeKind",
    "ObjectKey",
    "Subgraph",
    "save_node_link",
    "write_node_link",
]
