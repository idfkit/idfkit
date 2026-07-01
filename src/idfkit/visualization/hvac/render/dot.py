"""Render an :class:`~idfkit.visualization.hvac.model.HVACGraph` as Graphviz DOT.

Produces a ``digraph`` with one ``cluster`` per loop (optionally split into
supply/demand), matching the Mermaid renderer's colors. Pipe the result through
``dot -Tsvg`` (or any Graphviz frontend) to get an image — idfkit itself adds no
Graphviz dependency.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..layout import Layout, plan_layout, split_ungrouped, truncate, zone_outflow_targets
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
    body: list[str] = []
    for side in ("supply", "demand"):
        verts = layout.by_group.get((loop_id, side), [])
        if not verts:
            continue
        if config.group_by_side:
            body.append(f"    subgraph cluster_{cluster}_{side} {{")
            body.append(f'      label="{side}";')
            body += _vertices_block(verts, "      ", layout, config.max_label_length)
            body.append("    }")
        else:
            body += _vertices_block(verts, "    ", layout, config.max_label_length)
    if not body:
        # Skip a loop with no rendered vertices rather than emit an empty cluster.
        return []
    return [
        f"  subgraph cluster_{cluster} {{",
        f'    label="{_esc(name)} ({loop_type})";',
        '    style=rounded; color="#888888";',
        *body,
        "  }",
    ]


def _zone_box(z_name: str, zid: str) -> str:
    return f'{zid} [label="Zone: {_esc(z_name)}", shape=box, fillcolor="{ZONE_FILL}", color="{ZONE_STROKE}"];'


def _zone_cluster(graph: HVACGraph, layout: Layout, config: HVACDiagramConfig) -> list[str]:
    out = ["  subgraph cluster_zones {", '    label="Zones"; style=rounded; color="#888888";']
    for z in graph.zones:
        zid = layout.zone_ids[z.name]
        equip = layout.zone_clusters.get(z.name, [])
        if equip:
            # Nest the zone's own equipment with the zone box so a zonal system
            # (fan coil, VRF terminal unit) reads as one cluster.
            out.append(f"    subgraph cluster_{zid} {{")
            out.append(f'      label="{_esc(z.name)}"; style=rounded; color="#888888";')
            out += _vertices_block(equip, "      ", layout, config.max_label_length)
            out.append("      " + _zone_box(z.name, zid))
            out.append("    }")
        else:
            out.append("    " + _zone_box(z.name, zid))
    out.append("  }")
    return out


def _zone_edges(graph: HVACGraph, layout: Layout, config: HVACDiagramConfig) -> list[str]:
    out: list[str] = []
    outflow = zone_outflow_targets(graph)  # components air leaves the zone into (return mixer, exhaust fan)
    for z in graph.zones:
        zid = layout.zone_ids[z.name]
        exhaust = set(outflow.get(z.name, ()))
        for key in z.equipment_keys:
            if key in exhaust:
                continue  # exhaust device removes air from the zone — drawn as a return leg, not supply
            sid = layout.vertex_ids.get(key)
            if sid is not None:
                out.append(f"  {sid} -> {zid};")
        if config.show_return_air:
            for key in outflow.get(z.name, ()):
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
    return out + _zone_edges(graph, layout, config) + _refrigerant_edges(graph, layout)


def _refrigerant_edges(graph: HVACGraph, layout: Layout) -> list[str]:
    out: list[str] = []
    for r in graph.refrigerant_edges:
        src = layout.vertex_ids.get(r.master_key)
        dst = layout.vertex_ids.get(r.terminal_key)
        if src is not None and dst is not None:
            out.append(f'  {src} -> {dst} [style=dotted, color="#c9785d", label="refrigerant"];')
    return out


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
    other, refrigerant_masters = split_ungrouped(graph, layout)
    if refrigerant_masters:
        lines.append("  subgraph cluster_refrigerant {")
        lines.append('    label="VRF refrigerant system"; style=rounded; color="#888888";')
        lines += _vertices_block(refrigerant_masters, "    ", layout, config.max_label_length)
        lines.append("  }")
    if other:
        lines.append("  subgraph cluster_other {")
        lines.append('    label="Other equipment"; style=rounded; color="#888888";')
        lines += _vertices_block(other, "    ", layout, config.max_label_length)
        lines.append("  }")
    if graph.zones:
        lines += _zone_cluster(graph, layout, config)
    lines += _edges(graph, layout, config)
    lines.append("}")
    return "\n".join(lines)
