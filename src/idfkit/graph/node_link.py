"""Node-link JSON export of the model graph (research R-24, ``contracts/node-link-json.md``).

The format is networkx's node-link layout with the edge list under ``"edges"``, which
``networkx.node_link_graph`` (3.6 or later) reads with no keyword arguments. On networkx 3.4 and
3.5, pass ``edges="edges"``. d3-force expects ``links``: rename the key in one line.
"""

from __future__ import annotations

import json
import os
from collections.abc import Collection
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final

from idfkit._graph_common import Coverage, ObjectKey
from idfkit.graph._walk import Walker, known, walk
from idfkit.graph.types import EDGE_LAYER, NODE_LAYER, EdgeKind, GraphEdge, GraphNode, JSONValue, Layer, NodeKind
from idfkit.graph.view import NO_RESULTS, PRESENT

if TYPE_CHECKING:
    from idfkit.document import IDFDocument
    from idfkit.graph.view import ModelGraph

__all__ = ["NODE_LINK_FORMAT_VERSION", "save_node_link", "write_node_link"]

NODE_LINK_FORMAT_VERSION: Final = 1
"""The version of the node-link format. A change that removes or renames a key, or changes what a
kind means, raises it. Adding an optional attribute, a kind or a layer does not."""

FORMAT: Final = "idfkit-model-graph"
ALL_LAYERS: tuple[Layer, ...] = ("model", "topology", "results")


def write_node_link(
    graph: ModelGraph,
    *,
    layers: Collection[Layer] | None = None,
    node_kinds: Collection[NodeKind] | None = None,
    edge_kinds: Collection[EdgeKind] | None = None,
    start: ObjectKey | str | None = None,
    hops: int | None = None,
) -> str:
    """Return the graph as node-link JSON text. The keywords are those of ``ModelGraph.to_node_link``.

    Examples:
        >>> import json
        >>> from idfkit import new_document
        >>> from idfkit.graph import ModelGraph, write_node_link
        >>> doc = new_document()
        >>> _ = doc.add("Zone", "Office")
        >>> data = json.loads(write_node_link(ModelGraph(doc), node_kinds=["object"]))
        >>> data["graph"]["format"], data["graph"]["format_version"]
        ('idfkit-model-graph', 1)
        >>> [n["id"] for n in data["nodes"] if n["object_type"] == "Zone"]
        ['object:ZONE:OFFICE']
    """
    data = graph.to_node_link(layers=layers, node_kinds=node_kinds, edge_kinds=edge_kinds, start=start, hops=hops)
    return json.dumps(data, ensure_ascii=False)


def save_node_link(
    graph: ModelGraph,
    path: str | os.PathLike[str],
    *,
    layers: Collection[Layer] | None = None,
    node_kinds: Collection[NodeKind] | None = None,
    edge_kinds: Collection[EdgeKind] | None = None,
    start: ObjectKey | str | None = None,
    hops: int | None = None,
) -> None:
    """Write the graph as node-link JSON to *path*, in UTF-8. The keywords are those of ``ModelGraph.to_node_link``."""
    text = write_node_link(graph, layers=layers, node_kinds=node_kinds, edge_kinds=edge_kinds, start=start, hops=hops)
    Path(path).write_text(text, encoding="utf-8")


def build_node_link(
    doc: IDFDocument[Any],
    *,
    layers: Collection[str] | None,
    node_kinds: Collection[str] | None,
    edge_kinds: Collection[str] | None,
    start: ObjectKey | str | None,
    hops: int | None,
) -> dict[str, JSONValue]:
    """Build the node-link data for ``ModelGraph.to_node_link``."""
    if (start is None) != (hops is None):
        msg = "start and hops must be given together"
        raise ValueError(msg)
    if hops is not None and hops < 0:
        msg = f"hops must be 0 or more, got {hops}"
        raise ValueError(msg)
    asked = known(layers, ALL_LAYERS)
    present = [layer for layer in PRESENT if layer in asked]
    unavailable: dict[str, JSONValue] = {"results": NO_RESULTS} if "results" in asked else {}
    wanted_nodes = known(node_kinds, tuple(NODE_LAYER))
    wanted_edges = known(edge_kinds, tuple(EDGE_LAYER))
    nk = [k for k, layer in NODE_LAYER.items() if k in wanted_nodes and layer in present]
    ek = [k for k, layer in EDGE_LAYER.items() if k in wanted_edges and layer in present]
    walker = Walker(doc, node_kinds=nk, edge_kinds=ek)

    start_id: str | None = None
    if start is not None and hops is not None:
        found = walk(walker, start, hops=hops, categories=None, max_nodes=None)
        start_id, nodes, edges = found.start, found.nodes, found.edges
    else:
        nodes, edges = _everything(walker, nk)

    major, minor, patch = doc.version
    graph: dict[str, JSONValue] = {
        "format": FORMAT,
        "format_version": NODE_LINK_FORMAT_VERSION,
        "idfkit_version": _idfkit_version(),
        "energyplus_version": f"{major}.{minor}.{patch}",
        "layers": list(present),
        "unavailable": unavailable,
        "coverage": _coverage(walker.topology.coverage),
        "scope": _scope(start_id, hops, node_kinds, edge_kinds),
        "results_state": None,
    }
    return {
        "directed": True,
        "multigraph": True,
        "graph": graph,
        "nodes": [_node(n) for n in nodes],
        "edges": [_edge(e) for e in edges],
    }


def _scope(
    start: str | None, hops: int | None, node_kinds: Collection[str] | None, edge_kinds: Collection[str] | None
) -> dict[str, JSONValue]:
    def listed(kinds: Collection[str] | None) -> JSONValue:
        return None if kinds is None else [str(k) for k in sorted(kinds)]

    return {
        "start": start,
        "hops": hops,
        "node_kinds": listed(node_kinds),
        "edge_kinds": listed(edge_kinds),
        "categories": None,
    }


def _everything(walker: Walker, node_kinds: Collection[str]) -> tuple[list[GraphNode], list[GraphEdge]]:
    """Every node of the kinds asked for, and every edge between them, each once, in model order."""
    nodes: dict[str, GraphNode] = {}
    raw: dict[tuple[str, str, str], GraphEdge] = {}
    doc_objects = list(walker.document.all_objects) if "object" in node_kinds else []
    for obj in doc_objects:
        vid = walker.object_id(obj)
        if vid not in nodes:
            nodes[vid] = walker.graph_node(vid, obj)
    if "node" in node_kinds:
        for name in walker.topology.nodes():
            vid = f"node:{name.upper()}"
            if vid not in nodes:
                nodes[vid] = walker.graph_node(vid, name)
    for obj in doc_objects:
        for e, _, _ in walker.out_edges(walker.object_id(obj), obj):
            if e.source in nodes and e.target in nodes:
                raw.setdefault(
                    (e.source, e.target, e.key),
                    GraphEdge(e.source, e.target, e.kind, EDGE_LAYER[e.kind], e.key, e.attrs),
                )
    return list(nodes.values()), list(raw.values())


def _node(node: GraphNode) -> dict[str, JSONValue]:
    out: dict[str, JSONValue] = {"id": node.id, "kind": node.kind, "layer": node.layer, "label": node.label}
    if node.key is not None:
        out["object_type"] = node.key.object_type
        out["name"] = node.key.name
    if node.node is not None:
        out["name"] = node.node
    out.update(node.attrs)
    return out


def _edge(edge: GraphEdge) -> dict[str, JSONValue]:
    out: dict[str, JSONValue] = {
        "source": edge.source,
        "target": edge.target,
        "key": edge.key,
        "kind": edge.kind,
        "layer": edge.layer,
    }
    out.update(edge.attrs)
    return out


def _coverage(coverage: Coverage) -> dict[str, JSONValue]:
    return {
        "partial": coverage.partial,
        "uncovered": [
            {
                "kind": part.kind,
                "count": part.count,
                "examples": [{"object_type": k.object_type, "name": k.name} for k in part.examples],
                "reason": part.reason,
            }
            for part in coverage.uncovered
        ],
    }


def _idfkit_version() -> str:
    import idfkit

    return idfkit.__version__
