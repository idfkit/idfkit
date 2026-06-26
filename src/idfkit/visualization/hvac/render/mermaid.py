"""Render an :class:`~idfkit.visualization.hvac.model.HVACGraph` as Mermaid.

Produces a ``flowchart`` with one subgraph per loop (optionally split into
supply/demand), components colored by category, and edges labeled with the
EnergyPlus node they flow through. Paste the result into mermaid.live, a Markdown
file, or run it through ``mmdc`` to get an image.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..layout import Layout, plan_layout, truncate, zone_outflow_targets
from ..style import TEXT_COLOR, ZONE_FILL, ZONE_STROKE, style_for

if TYPE_CHECKING:
    from ..model import Category, HVACDiagramConfig, HVACGraph, HVACVertex


#: Above this many components a single flowchart is hard to read; hint at alternatives.
_LARGE_MODEL = 150


def _esc(text: str) -> str:
    """Escape text for a quoted Mermaid label."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


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
    out = [f'  subgraph {sg}["{_esc(name)} · {loop_type}"]']
    for side in ("supply", "demand"):
        verts = layout.by_group.get((loop_id, side), [])
        if not verts:
            continue
        if config.group_by_side:
            out.append(f'    subgraph {sg}_{side}["{side}"]')
            out += _vertices_block(verts, "      ", layout, config.max_label_length, used)
            out.append("    end")
        else:
            out += _vertices_block(verts, "    ", layout, config.max_label_length, used)
    out.append("  end")
    return out


def _zone_subgraph(graph: HVACGraph, layout: Layout) -> list[str]:
    out = ['  subgraph zones["Zones"]']
    for z in graph.zones:
        out.append(f'    {layout.zone_ids[z.name]}["Zone: {_esc(z.name)}"]:::zone')
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
    return out + _zone_edges(graph, layout, config)


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
    lines: list[str] = [f"flowchart {config.direction}"]
    if len(graph.vertices) > _LARGE_MODEL:
        lines.append(
            f"%% {len(graph.vertices)} components across {len(graph.loops)} loops — "
            "use graph.subset(loop_names=[...]) or graph.overview_mermaid() for a readable view"
        )
    used: set[Category] = set()

    for loop in graph.loops:
        lines += _loop_subgraph(loop.loop_id, loop.name, loop.loop_type, layout, config, used)
    if layout.ungrouped:
        lines.append('  subgraph other["Other equipment"]')
        lines += _vertices_block(layout.ungrouped, "    ", layout, config.max_label_length, used)
        lines.append("  end")
    if graph.zones:
        lines += _zone_subgraph(graph, layout)
    lines += _edges(graph, layout, config)
    lines += _classdefs(used, bool(graph.zones))
    return "\n".join(lines)
