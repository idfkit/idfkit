"""The combined, read-only view over the model, topology and results layers (research R-23)."""

from __future__ import annotations

from collections.abc import Collection
from typing import TYPE_CHECKING, Any, Literal

from idfkit._graph_common import Coverage, ObjectKey
from idfkit.graph._walk import Walker, walk
from idfkit.graph.types import EdgeKind, JSONValue, Layer, NodeKind, Subgraph
from idfkit.hvac import ComponentCategory, HVACTopology

if TYPE_CHECKING:
    from idfkit.document import IDFDocument
    from idfkit.simulation.linking import ResultIndex

__all__ = ["ModelGraph"]

PRESENT: tuple[Layer, ...] = ("model", "topology")
"""The layers every view has: both are core and need no data."""

NO_RESULTS = "no ResultIndex was passed in"


class ModelGraph:
    """One graph over a document's objects, fluid nodes and their connections.

    It is an adapter, not a copy: construction stores the document and returns, and every walk asks
    the reference graph and the cached :class:`~idfkit.hvac.HVACTopology` for neighbours at walk
    time, so the view is always current. It adds no domain logic.

    The vocabulary is fixed: ``object`` nodes (layer ``model``) joined by ``reference`` edges, and
    ``node`` nodes (layer ``topology``) joined to objects by ``flow``, ``control`` and
    ``membership`` edges. Given a :class:`~idfkit.simulation.ResultIndex`, the ``results`` layer adds
    ``result_fact`` and ``message`` nodes joined to the objects and nodes they concern by
    ``result_link`` edges; without one it is listed in :attr:`unavailable`. Results that no longer
    match the document are still walked and marked ``stale``. Code that reads kinds must ignore kinds
    it does not know.

    Examples:
        >>> from idfkit import new_document
        >>> from idfkit.graph import ModelGraph
        >>> from idfkit.hvac import ObjectKey
        >>> doc = new_document()
        >>> fan = doc.add("Fan:ConstantVolume", "Fan", air_inlet_node_name="Mixed Air",
        ...               air_outlet_node_name="Supply Air", validate=False)
        >>> graph = ModelGraph(doc)
        >>> graph.layers
        ['model', 'topology']
        >>> sub = graph.neighbourhood(ObjectKey("Fan:ConstantVolume", "Fan"))
        >>> [n.id for n in sub.nodes]
        ['object:FAN:CONSTANTVOLUME:FAN', 'node:MIXED AIR', 'node:SUPPLY AIR']
        >>> [(e.source, e.target) for e in sub.edges if e.kind == "flow"][0]
        ('node:MIXED AIR', 'object:FAN:CONSTANTVOLUME:FAN')
    """

    __slots__ = ("_doc", "_results")

    def __init__(self, doc: IDFDocument[Any], *, results: ResultIndex | None = None) -> None:
        """Store *doc* and *results*. No layer is built until a walk or an export asks for it.

        Args:
            doc: The model.
            results: A run's results linked to *doc*, for the ``results`` layer.
        """
        self._doc = doc
        self._results = results

    @property
    def layers(self) -> list[Layer]:
        """The layers present in the view: ``model``, ``topology`` and, given results, ``results``."""
        return [*PRESENT, "results"] if self._results is not None else list(PRESENT)

    @property
    def unavailable(self) -> dict[Layer, str]:
        """Each layer missing from the view, and why."""
        return {} if self._results is not None else {"results": NO_RESULTS}

    @property
    def results_state(self) -> Literal["fresh", "stale"] | None:
        """``"fresh"`` or ``"stale"`` for the results layer (FR-026), ``None`` without one."""
        if self._results is None:
            return None
        return "fresh" if self._results.is_fresh(self._doc) else "stale"

    @property
    def coverage(self) -> Coverage:
        """What the view cannot see: unexpanded templates, EMS programs, unclassified types."""
        return HVACTopology.from_document(self._doc).coverage

    def node_id(self, target: ObjectKey | str) -> str:
        """The graph node id of an object (an :class:`ObjectKey`) or of a fluid node (its name).

        Raises:
            KeyError: If the object or node is not in the model.
        """
        vid, _ = Walker(self._doc, results=self._results).start(target)
        return vid

    def neighbourhood(
        self,
        start: ObjectKey | str,
        *,
        hops: int = 1,
        node_kinds: Collection[NodeKind] | None = None,
        edge_kinds: Collection[EdgeKind] | None = None,
        categories: Collection[ComponentCategory | str] | None = None,
        max_nodes: int = 200,
    ) -> Subgraph:
        """The graph nodes within *hops* edges of *start*, walked breadth first in both directions.

        Args:
            start: An object, as an :class:`ObjectKey`, or a fluid node, by name.
            hops: The most edges from *start*. ``0`` returns *start* alone.
            node_kinds: Only walk through nodes of these kinds. Unknown kinds are ignored.
            edge_kinds: Only walk along edges of these kinds. Unknown kinds are ignored.
            categories: Keep only object nodes of these component categories, plus the start and the
                fluid nodes on the paths to them. Applied before *max_nodes*.
            max_nodes: The most nodes returned, the start included.

        Returns:
            The subgraph, with ``truncated``, ``omitted_nodes`` and the ``frontier`` to continue from.

        Raises:
            ValueError: If *hops* is negative or *max_nodes* is less than 1.
            KeyError: If *start* is not in the model.
        """
        if hops < 0:
            msg = f"hops must be 0 or more, got {hops}"
            raise ValueError(msg)
        if max_nodes < 1:
            msg = f"max_nodes must be 1 or more, got {max_nodes}"
            raise ValueError(msg)
        return self._walk(start, hops, node_kinds, edge_kinds, categories, max_nodes)

    def _walk(
        self,
        start: ObjectKey | str,
        hops: int,
        node_kinds: Collection[str] | None,
        edge_kinds: Collection[str] | None,
        categories: Collection[ComponentCategory | str] | None,
        max_nodes: int | None,
    ) -> Subgraph:
        walker = Walker(self._doc, node_kinds=node_kinds, edge_kinds=edge_kinds, results=self._results)
        wanted = None if categories is None else {getattr(c, "value", c) for c in categories}
        found = walk(walker, start, hops=hops, categories=wanted, max_nodes=max_nodes)
        return Subgraph(
            start=found.start,
            nodes=found.nodes,
            edges=found.edges,
            layers=self.layers,
            unavailable=self.unavailable,
            coverage=walker.topology.coverage,
            truncated=found.truncated,
            omitted_nodes=found.omitted,
            frontier=found.frontier,
            results_state=self.results_state,
        )

    def to_node_link(
        self,
        *,
        layers: Collection[Layer] | None = None,
        node_kinds: Collection[NodeKind] | None = None,
        edge_kinds: Collection[EdgeKind] | None = None,
        start: ObjectKey | str | None = None,
        hops: int | None = None,
    ) -> dict[str, JSONValue]:
        """The view as node-link JSON data, in the format of ``contracts/node-link-json.md``.

        Args:
            layers: Only these layers. A layer asked for but absent is listed in ``unavailable``.
            node_kinds: Only nodes of these kinds. Unknown kinds are ignored.
            edge_kinds: Only edges of these kinds. Unknown kinds are ignored.
            start: Export only the neighbourhood of this object or node. Needs *hops*.
            hops: The radius of the neighbourhood around *start*, with no node bound.

        Returns:
            A dict that ``json.dumps`` writes and ``networkx.node_link_graph`` (3.6 or later) reads.

        Raises:
            ValueError: If only one of *start* and *hops* is given, or *hops* is negative.
            KeyError: If *start* is not in the model.
        """
        from idfkit.graph.node_link import build_node_link

        return build_node_link(
            self._doc,
            layers=layers,
            node_kinds=node_kinds,
            edge_kinds=edge_kinds,
            start=start,
            hops=hops,
            results=self._results,
        )
