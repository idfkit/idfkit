"""Render an :class:`~idfkit.visualization.hvac.model.HVACGraph` as Mermaid.

Produces a ``flowchart`` with one subgraph per loop (optionally split into
supply/demand), components colored by category, and edges labeled with the
EnergyPlus node they flow through. Paste the result into mermaid.live, a Markdown
file, or run it through ``mmdc`` to get an image.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..layout import Layout, plan_layout, split_ungrouped, truncate, zone_outflow_targets
from ..style import TEXT_COLOR, ZONE_FILL, ZONE_STROKE, style_for
from ._common import mermaid_escape as _esc

if TYPE_CHECKING:
    from ..model import Category, HVACDiagramConfig, HVACGraph, HVACVertex


def _node_def(vertex: HVACVertex, node_id: str, limit: int) -> str:
    style = style_for(vertex.category)
    open_, close = style.mermaid_shape
    label = f"{_esc(vertex.obj_type)}<br/>{_esc(truncate(vertex.name, limit))}"
    return f'{node_id}{open_}"{label}"{close}:::{vertex.category}'


def _vertices_block(
    vertices: list[HVACVertex], indent: str, layout: Layout, limit: int, used: set[Category]
) -> list[str]:
    out: list[str] = []
    for v in vertices:
        out.append(indent + _node_def(v, layout.vertex_ids[v.key], limit))
        used.add(v.category)
    return out


def _loop_subgraph(
    loop_id: str, name: str, loop_type: str, layout: Layout, config: HVACDiagramConfig, used: set[Category]
) -> list[str]:
    sg = layout.loop_ids[loop_id]
    body: list[str] = []
    for side in ("supply", "demand"):
        verts = layout.by_group.get((loop_id, side), [])
        if not verts:
            continue
        if config.group_by_side:
            body.append(f'    subgraph {sg}_{side}["{side}"]')
            body += _vertices_block(verts, "      ", layout, config.max_label_length, used)
            body.append("    end")
        else:
            body += _vertices_block(verts, "    ", layout, config.max_label_length, used)
    if not body:
        # A loop with no rendered vertices (all claimed by an earlier loop) would
        # be an empty subgraph, which the ELK layout engine rejects — emit nothing.
        return []
    return [f'  subgraph {sg}["{_esc(name)} · {loop_type}"]', *body, "  end"]


def _zone_subgraph(graph: HVACGraph, layout: Layout, config: HVACDiagramConfig, used: set[Category]) -> list[str]:
    out = ['  subgraph zones["Zones"]']
    for z in graph.zones:
        zid = layout.zone_ids[z.name]
        equip = layout.zone_clusters.get(z.name, [])
        if equip:
            # Wrap the zone's own equipment (fan coil train, VRF terminal unit, ...)
            # together with the zone box so a zonal system reads as one cluster.
            out.append(f'    subgraph {zid}_grp["{_esc(z.name)}"]')
            out += _vertices_block(equip, "      ", layout, config.max_label_length, used)
            out.append(f'      {zid}["Zone: {_esc(z.name)}"]:::zone')
            out.append("    end")
        else:
            out.append(f'    {zid}["Zone: {_esc(z.name)}"]:::zone')
    out.append("  end")
    return out


def _zone_edges(graph: HVACGraph, layout: Layout, config: HVACDiagramConfig) -> list[str]:
    out: list[str] = []
    returns = zone_outflow_targets(graph) if config.show_return_air else {}
    for z in graph.zones:
        zid = layout.zone_ids[z.name]
        for key in z.equipment_keys:
            sid = layout.vertex_ids.get(key)
            if sid is not None:
                out.append(f"  {sid} --> {zid}")  # supply: equipment delivers to zone
        for key in returns.get(z.name, ()):
            tid = layout.vertex_ids.get(key)
            if tid is not None:
                out.append(f"  {zid} -.->|return| {tid}")  # return: zone air back to the mixer
    return out


def _edges(graph: HVACGraph, layout: Layout, config: HVACDiagramConfig) -> list[str]:
    out: list[str] = []
    for e in graph.edges:
        src = layout.vertex_ids.get(e.src)
        dst = layout.vertex_ids.get(e.dst)
        if src is None or dst is None:
            continue
        if config.show_node_labels:
            out.append(f'  {src} -->|"{_esc(e.via_node)}"| {dst}')
        else:
            out.append(f"  {src} --> {dst}")
    return out + _zone_edges(graph, layout, config) + _refrigerant_edges(graph, layout)


def _refrigerant_edges(graph: HVACGraph, layout: Layout) -> list[str]:
    out: list[str] = []
    for r in graph.refrigerant_edges:
        src = layout.vertex_ids.get(r.master_key)
        dst = layout.vertex_ids.get(r.terminal_key)
        if src is not None and dst is not None:
            out.append(f"  {src} -.->|refrigerant| {dst}")
    return out


def _classdefs(used: set[Category], has_zones: bool) -> list[str]:
    out: list[str] = []
    for category in sorted(used):
        style = style_for(category)
        out.append(f"  classDef {category} fill:{style.fill},stroke:{style.stroke},color:{TEXT_COLOR};")
    if has_zones:
        out.append(f"  classDef zone fill:{ZONE_FILL},stroke:{ZONE_STROKE},color:{TEXT_COLOR};")
    return out


def render_mermaid(graph: HVACGraph, config: HVACDiagramConfig) -> str:
    """Return a Mermaid ``flowchart`` string for *graph*."""
    if graph.is_empty:
        return f'flowchart {config.direction}\n  empty["No HVAC components found"]'

    layout = plan_layout(graph)
    lines: list[str] = []
    if config.layout == "elk":
        # ELK lays out many-subgraph diagrams that the default dagre engine cannot.
        lines += ["---", "config:", "  layout: elk", "---"]
    lines.append(f"flowchart {config.direction}")
    if graph.is_complex:
        lines.append(
            f"%% {len(graph.vertices)} components across {len(graph.loops)} loops — the default "
            "layout may fail to render this many subgraphs; use graph.subset(loop_names=[...]), "
            'graph.overview_mermaid(), or HVACDiagramConfig(layout="elk")'
        )
    used: set[Category] = set()

    for loop in graph.loops:
        lines += _loop_subgraph(loop.loop_id, loop.name, loop.loop_type, layout, config, used)
    other, refrigerant_masters = split_ungrouped(graph, layout)
    if refrigerant_masters:
        lines.append('  subgraph refrigerant["VRF refrigerant system"]')
        lines += _vertices_block(refrigerant_masters, "    ", layout, config.max_label_length, used)
        lines.append("  end")
    if other:
        lines.append('  subgraph other["Other equipment"]')
        lines += _vertices_block(other, "    ", layout, config.max_label_length, used)
        lines.append("  end")
    if graph.zones:
        lines += _zone_subgraph(graph, layout, config, used)
    lines += _edges(graph, layout, config)
    lines += _classdefs(used, bool(graph.zones))
    return "\n".join(lines)
