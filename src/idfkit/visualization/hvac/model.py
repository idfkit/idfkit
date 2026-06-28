"""Data model for HVAC topology graphs.

The graph is a small, immutable, stdlib-only representation of an EnergyPlus
HVAC system reconstructed from an :class:`~idfkit.IDFDocument`. A
:class:`HVACVertex` is a component (coil, fan, pump, chiller, splitter, ...),
an :class:`HVACEdge` is a directed connection through a shared node, and the
vertices are grouped into :class:`HVACLoop` sides for rendering.

All public dataclasses are frozen with tuple fields so a built graph is hashable,
reproducible, and safe to share. The renderers in :mod:`.render` and the
serializers below consume this model; nothing here imports EnergyPlus or any
third-party package.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, replace
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping

#: Which side of a loop a component sits on.
Side = Literal["supply", "demand", "other"]

#: Coarse component category, used only for coloring and node shapes.
Category = Literal[
    "coil",
    "fan",
    "pump",
    "plant_equipment",
    "junction",
    "terminal",
    "outdoor_air",
    "pipe",
    "other",
]

#: Loop kind, mirrors the EnergyPlus object type that defines it.
LoopType = Literal["AirLoopHVAC", "PlantLoop", "CondenserLoop"]

#: Kind of a non-fatal diagnostic recorded while building the graph.
WarningKind = Literal[
    "suspicious_node",
    "unconnected_component",
    "missing_branch",
    "missing_object",
    "unsupported",
]


@dataclass(frozen=True)
class HVACDiagramConfig:
    """Rendering options shared by every output format.

    Attributes:
        direction: Flowchart direction (``"LR"`` left-to-right like the
            EnergyPlus HVAC-Diagram, ``"TB"`` top-to-bottom, etc.).
        show_node_labels: Annotate each edge with the EnergyPlus node name it
            flows through. Turn off to declutter large systems.
        group_by_side: Nest a ``supply``/``demand`` subgraph inside each loop.
        show_return_air: Draw the return leg (zone → return mixer/plenum) as a
            dashed edge, so the air loop reads as a closed supply/return circuit.
        include_controls: Reserved — controls and setpoint managers are excluded
            from the flow graph regardless (kept for forward compatibility).
        max_label_length: Truncate component names longer than this in labels.
        layout: Mermaid layout engine. ``"dagre"`` (default) is universally
            supported but its cluster layout fails on large multi-loop models
            (dozens of subgraphs). ``"elk"`` handles those reliably but requires
            the viewer to have the Mermaid ELK plugin (GitHub, mermaid.live, and
            ``mmdc`` do; older embedded renderers may not).
    """

    direction: Literal["LR", "RL", "TB", "BT"] = "LR"
    show_node_labels: bool = True
    group_by_side: bool = True
    show_return_air: bool = True
    include_controls: bool = False
    max_label_length: int = 40
    layout: Literal["dagre", "elk"] = "dagre"


@dataclass(frozen=True)
class LoopMembership:
    """Records that a vertex participates in a given loop on a given side."""

    loop_id: str
    side: Side


@dataclass(frozen=True)
class HVACNode:
    """An EnergyPlus node — a connection point between components.

    Attributes:
        name: The node name as written in the IDF (original case preserved).
        fluid_type: Best-effort fluid guess (``"air"``, ``"water"``,
            ``"steam"`` or ``"unknown"``) inferred from the field names that
            reference it.
        producers: Vertex keys whose *outlet* is this node.
        consumers: Vertex keys whose *inlet* is this node.
    """

    name: str
    fluid_type: str
    producers: tuple[str, ...]
    consumers: tuple[str, ...]


@dataclass(frozen=True)
class HVACVertex:
    """A component in the HVAC graph.

    A component is identified by ``key`` (``"OBJTYPE::NAME"``, upper-cased), so a
    water coil enumerated on both an air branch and a plant branch is a single
    vertex carrying both node pairs and both loop memberships.

    Attributes:
        key: Stable identity ``f"{obj_type.upper()}::{name.upper()}"``.
        obj_type: EnergyPlus object type (e.g. ``"Coil:Cooling:Water"``).
        name: Object name (original case).
        category: Coarse category for coloring/shape.
        inlet_nodes: Node names feeding this component.
        outlet_nodes: Node names leaving this component.
        memberships: Loop/side memberships (may be more than one).
        zone: Name of the thermal zone this component serves, if any.
    """

    key: str
    obj_type: str
    name: str
    category: Category
    inlet_nodes: tuple[str, ...]
    outlet_nodes: tuple[str, ...]
    memberships: tuple[LoopMembership, ...]
    zone: str | None = None


@dataclass(frozen=True)
class HVACEdge:
    """A directed connection between two vertices through a shared node."""

    src: str
    dst: str
    via_node: str
    fluid_type: str


@dataclass(frozen=True)
class HVACRefrigerantEdge:
    """A refrigerant-network link from a VRF outdoor unit to a terminal-unit coil.

    Variable-refrigerant-flow systems couple their condensing unit to the zone
    terminal units through a named terminal-unit *list*, not through air/water
    nodes — so this connection is tracked separately from :class:`HVACEdge` and
    rendered as a distinct dashed "refrigerant" edge.
    """

    master_key: str
    terminal_key: str


@dataclass(frozen=True)
class HVACLoop:
    """A loop and the vertices on each of its sides."""

    loop_id: str
    name: str
    loop_type: LoopType
    supply_keys: tuple[str, ...]
    demand_keys: tuple[str, ...]


@dataclass(frozen=True)
class HVACZone:
    """A conditioned zone and the nodes/equipment that serve it."""

    name: str
    air_node: str | None
    inlet_nodes: tuple[str, ...]
    exhaust_nodes: tuple[str, ...]
    return_nodes: tuple[str, ...]
    equipment_keys: tuple[str, ...]


@dataclass(frozen=True)
class HVACWarning:
    """A non-fatal diagnostic recorded while building the graph."""

    kind: WarningKind
    message: str
    ref: str | None = None


def _empty_vertex_map() -> dict[str, HVACVertex]:
    return {}


@dataclass(frozen=True)
class HVACGraph:
    """A reconstructed HVAC system.

    Build one with :func:`idfkit.visualization.build_hvac_graph` and render it
    with :meth:`to_mermaid`, :meth:`to_dot`, or :meth:`to_dict`/:meth:`to_json`.
    """

    version: tuple[int, int, int] | None
    loops: tuple[HVACLoop, ...] = ()
    vertices: tuple[HVACVertex, ...] = ()
    nodes: tuple[HVACNode, ...] = ()
    edges: tuple[HVACEdge, ...] = ()
    zones: tuple[HVACZone, ...] = ()
    warnings: tuple[HVACWarning, ...] = ()
    refrigerant_edges: tuple[HVACRefrigerantEdge, ...] = ()
    _by_key: Mapping[str, HVACVertex] = field(default_factory=_empty_vertex_map, repr=False, compare=False)

    def vertex(self, key: str) -> HVACVertex | None:
        """Return the vertex with *key*, or ``None``."""
        if self._by_key:
            return self._by_key.get(key)
        return next((v for v in self.vertices if v.key == key), None)

    @property
    def is_empty(self) -> bool:
        """True when no HVAC components were found."""
        return not self.vertices

    @property
    def is_complex(self) -> bool:
        """True when the full component diagram is too large to lay out reliably.

        The Mermaid/Graphviz default (dagre) layout fails on flowcharts with many
        subgraphs — a whole-building model with dozens of loops and zones. Use
        :meth:`overview_mermaid`, :meth:`subset`, or ``HVACDiagramConfig(layout="elk")``
        for those; :meth:`_repr_markdown_` falls back to the overview automatically.
        """
        return len(self.vertices) > 80 or len(self.loops) > 5 or len(self.zones) > 12

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable view of the graph."""
        return {
            "version": list(self.version) if self.version else None,
            "loops": [
                {
                    "loop_id": loop.loop_id,
                    "name": loop.name,
                    "loop_type": loop.loop_type,
                    "supply": list(loop.supply_keys),
                    "demand": list(loop.demand_keys),
                }
                for loop in self.loops
            ],
            "vertices": [
                {
                    "key": v.key,
                    "obj_type": v.obj_type,
                    "name": v.name,
                    "category": v.category,
                    "inlet_nodes": list(v.inlet_nodes),
                    "outlet_nodes": list(v.outlet_nodes),
                    "memberships": [{"loop_id": m.loop_id, "side": m.side} for m in v.memberships],
                    "zone": v.zone,
                }
                for v in self.vertices
            ],
            "edges": [
                {"src": e.src, "dst": e.dst, "via_node": e.via_node, "fluid_type": e.fluid_type} for e in self.edges
            ],
            "zones": [
                {
                    "name": z.name,
                    "air_node": z.air_node,
                    "inlet_nodes": list(z.inlet_nodes),
                    "exhaust_nodes": list(z.exhaust_nodes),
                    "return_nodes": list(z.return_nodes),
                    "equipment": list(z.equipment_keys),
                }
                for z in self.zones
            ],
            "warnings": [{"kind": w.kind, "message": w.message, "ref": w.ref} for w in self.warnings],
            "refrigerant": [{"master": r.master_key, "terminal": r.terminal_key} for r in self.refrigerant_edges],
        }

    def to_json(self, *, indent: int | None = 2) -> str:
        """Return the graph as a JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    def to_mermaid(self, config: HVACDiagramConfig | None = None) -> str:
        """Render the graph as a Mermaid ``flowchart``."""
        from .render.mermaid import render_mermaid

        return render_mermaid(self, config or HVACDiagramConfig())

    def to_dot(self, config: HVACDiagramConfig | None = None) -> str:
        """Render the graph as a Graphviz DOT ``digraph``."""
        from .render.dot import render_dot

        return render_dot(self, config or HVACDiagramConfig())

    def overview_mermaid(self, config: HVACDiagramConfig | None = None) -> str:
        """Render a building-level Mermaid overview (one node per loop and zone).

        Use this instead of :meth:`to_mermaid` for large models, where a
        component-level flowchart has too many nodes to read. Each loop and zone
        becomes a single node; edges show plant→air-loop coupling and the zones
        each loop serves.
        """
        from .render.overview import render_overview_mermaid

        return render_overview_mermaid(self, config or HVACDiagramConfig())

    def subset(
        self,
        *,
        loop_names: Iterable[str] | None = None,
        loop_types: Iterable[str] | None = None,
    ) -> HVACGraph:
        """Return a new graph restricted to the selected loops.

        Filter by loop name and/or loop type (``"AirLoopHVAC"``, ``"PlantLoop"``,
        ``"CondenserLoop"``), both matched case-insensitively. The result keeps
        every component on a selected loop, the edges among the kept components,
        and — so the diagram stays honest about *how* each space is conditioned —
        the zones those loops serve together with each served zone's full
        equipment cluster (zone-only fans, OA mixers, VRF terminal coils that
        carry no loop membership) and the refrigerant links among kept
        components, pulling in the outdoor unit each link references. A served
        zone is therefore never rendered as a bare box. Passing neither argument
        returns an equivalent graph.
        """
        if loop_names is None and loop_types is None:
            # No filter selects every loop, so the result is the whole graph.
            return HVACGraph(
                version=self.version,
                loops=self.loops,
                vertices=self.vertices,
                nodes=self.nodes,
                edges=self.edges,
                zones=self.zones,
                warnings=self.warnings,
                refrigerant_edges=self.refrigerant_edges,
                _by_key={v.key: v for v in self.vertices},
            )
        name_set = {n.strip().upper() for n in loop_names} if loop_names is not None else None
        type_set = {t.strip().upper() for t in loop_types} if loop_types is not None else None
        selected_loops = tuple(
            loop
            for loop in self.loops
            if (name_set is None or loop.name.strip().upper() in name_set)
            and (type_set is None or loop.loop_type.strip().upper() in type_set)
        )
        selected_ids = {loop.loop_id for loop in selected_loops}
        # Components on a selected loop, then the zones they serve and each served
        # zone's whole equipment cluster (including zone-only vertices with no loop
        # membership) so a kept zone shows its full conditioning train.
        loop_keys = {v.key for v in self.vertices if any(m.loop_id in selected_ids for m in v.memberships)}
        served_zones = {z.name for z in self.zones if any(k in loop_keys for k in z.equipment_keys)}
        keys = loop_keys | {v.key for v in self.vertices if v.zone in served_zones}
        # Refrigerant links whose terminal is in view, plus the outdoor unit they reference.
        refrigerant = tuple(r for r in self.refrigerant_edges if r.terminal_key in keys)
        keys |= {r.master_key for r in refrigerant}
        vertices = tuple(v for v in self.vertices if v.key in keys)
        edges = tuple(e for e in self.edges if e.src in keys and e.dst in keys)
        nodes = tuple(n for n in self.nodes if keys.intersection((*n.producers, *n.consumers)))
        zones = tuple(
            replace(z, equipment_keys=tuple(k for k in z.equipment_keys if k in keys))
            for z in self.zones
            if z.name in served_zones
        )
        return HVACGraph(
            version=self.version,
            loops=selected_loops,
            vertices=vertices,
            nodes=nodes,
            edges=edges,
            zones=zones,
            warnings=(),
            refrigerant_edges=refrigerant,
            _by_key={v.key: v for v in vertices},
        )

    def _repr_markdown_(self) -> str:
        """Render as a Mermaid code fence so the graph displays in Jupyter.

        For a complex model the full component flowchart overruns the default
        Mermaid (dagre) layout, so the inline preview falls back to the building
        overview with a pointer to the detailed views, rather than emitting a
        diagram the notebook cannot render.
        """
        if self.is_complex:
            note = (
                f"> **{len(self.vertices)} components across {len(self.loops)} loops, "
                f"{len(self.zones)} zones** — showing the building overview. "
                "For the full diagram use `graph.subset(loop_names=[...])`, or "
                '`graph.to_mermaid(HVACDiagramConfig(layout="elk"))` in an ELK-capable viewer.'
            )
            return f"{note}\n\n```mermaid\n{self.overview_mermaid()}\n```"
        return f"```mermaid\n{self.to_mermaid()}\n```"
