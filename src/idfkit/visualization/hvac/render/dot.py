"""Render an :class:`~idfkit.visualization.hvac.model.HVACGraph` as Graphviz DOT.

Produces a ``digraph`` with one ``cluster`` per loop (optionally split into
supply/demand), matching the Mermaid renderer's colors. Pipe the result through
``dot -Tsvg`` (or any Graphviz frontend) to get an image — idfkit itself adds no
Graphviz dependency.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..layout import Layout, plan_layout, truncate, zone_outflow_targets
from ..style import ZONE_FILL, ZONE_STROKE, style_for

if TYPE_CHECKING:
    from ..model import HVACDiagramConfig, HVACGraph, HVACVertex


def _esc(text: str) -> str:
    """Escape text for a quoted DOT string."""
    return text.replace("\\", "\\\\").replace('"', '\\"')


def _node_def(vertex: HVACVertex, node_id: str, limit: int) -> str:
    style = style_for(vertex.category)
    label = f"{_esc(vertex.obj_type)}\\n{_esc(truncate(vertex.name, limit))}"
    return f'{node_id} [label="{label}", shape={style.dot_shape}, fillcolor="{style.fill}", color="{style.stroke}"];'


def _vertices_block(vertices: list[HVACVertex], indent: str, layout: Layout, limit: int) -> list[str]:
    return [indent + _node_def(v, layout.vertex_ids[v.key], limit) for v in vertices]


def _loop_cluster(loop_id: str, name: str, loop_type: str, layout: Layout, config: HVACDiagramConfig) -> list[str]:
    cluster = layout.loop_ids[loop_id]
    out = [
        f"  subgraph cluster_{cluster} {{",
        f'    label="{_esc(name)} ({loop_type})";',
        '    style=rounded; color="#888888";',
    ]
    for side in ("supply", "demand"):
        verts = layout.by_group.get((loop_id, side), [])
        if not verts:
            continue
        if config.group_by_side:
            out.append(f"    subgraph cluster_{cluster}_{side} {{")
            out.append(f'      label="{side}";')
            out += _vertices_block(verts, "      ", layout, config.max_label_length)
            out.append("    }")
        else:
            out += _vertices_block(verts, "    ", layout, config.max_label_length)
    out.append("  }")
    return out


def _zone_cluster(graph: HVACGraph, layout: Layout) -> list[str]:
    out = ["  subgraph cluster_zones {", '    label="Zones"; style=rounded; color="#888888";']
    for z in graph.zones:
        out.append(
            f'    {layout.zone_ids[z.name]} [label="Zone: {_esc(z.name)}", '
            f'shape=box, fillcolor="{ZONE_FILL}", color="{ZONE_STROKE}"];'
        )
    out.append("  }")
    return out


def _zone_edges(graph: HVACGraph, layout: Layout, config: HVACDiagramConfig) -> list[str]:
    out: list[str] = []
    returns = zone_outflow_targets(graph) if config.show_return_air else {}
    for z in graph.zones:
        zid = layout.zone_ids[z.name]
        for key in z.equipment_keys:
            sid = layout.vertex_ids.get(key)
            if sid is not None:
                out.append(f"  {sid} -> {zid};")
        for key in returns.get(z.name, ()):
            tid = layout.vertex_ids.get(key)
            if tid is not None:
                out.append(f'  {zid} -> {tid} [style=dashed, label="return"];')
    return out


def _edges(graph: HVACGraph, layout: Layout, config: HVACDiagramConfig) -> list[str]:
    out: list[str] = []
    for e in graph.edges:
        src = layout.vertex_ids.get(e.src)
        dst = layout.vertex_ids.get(e.dst)
        if src is None or dst is None:
            continue
        label = f' [label="{_esc(e.via_node)}"]' if config.show_node_labels else ""
        out.append(f"  {src} -> {dst}{label};")
    return out + _zone_edges(graph, layout, config)


def render_dot(graph: HVACGraph, config: HVACDiagramConfig) -> str:
    """Return a Graphviz DOT ``digraph`` string for *graph*."""
    lines: list[str] = [
        "digraph hvac {",
        f"  rankdir={config.direction};",
        '  node [fontname="Helvetica", style="filled,rounded"];',
        '  edge [fontname="Helvetica", fontsize=9];',
    ]
    if graph.is_empty:
        lines.append('  empty [label="No HVAC components found", style=filled, fillcolor="#e8e4dc"];')
        lines.append("}")
        return "\n".join(lines)

    layout = plan_layout(graph)
    for loop in graph.loops:
        lines += _loop_cluster(loop.loop_id, loop.name, loop.loop_type, layout, config)
    if layout.ungrouped:
        lines.append("  subgraph cluster_other {")
        lines.append('    label="Other equipment"; style=rounded; color="#888888";')
        lines += _vertices_block(layout.ungrouped, "    ", layout, config.max_label_length)
        lines.append("  }")
    if graph.zones:
        lines += _zone_cluster(graph, layout)
    lines += _edges(graph, layout, config)
    lines.append("}")
    return "\n".join(lines)
