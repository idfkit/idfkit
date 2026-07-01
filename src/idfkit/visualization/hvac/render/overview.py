"""A building-level *overview* render: one node per loop and per zone.

For large models a component-level flowchart is unreadable (hundreds of nodes).
The overview collapses each loop and each zone to a single node and draws the
relationships between them: plant/condenser loops feeding air loops (through
shared coils), and air loops serving zones. It answers "how is the building's
HVAC wired together" without the per-component detail.
"""

from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

from ..style import TEXT_COLOR, ZONE_FILL, ZONE_STROKE
from ._common import mermaid_escape as _esc

if TYPE_CHECKING:
    from ..model import HVACDiagramConfig, HVACGraph

_LOOP_CLASS: dict[str, str] = {
    "AirLoopHVAC": "airloop",
    "PlantLoop": "plantloop",
    "CondenserLoop": "condenserloop",
}


def _loop_coupling_edges(graph: HVACGraph, loop_node: dict[str, str], loop_type: dict[str, str]) -> list[str]:
    """Edges between loops that share a component (a coil on both loops)."""
    pair_counts: Counter[tuple[str, str]] = Counter()
    for v in graph.vertices:
        loops = sorted({m.loop_id for m in v.memberships})
        for i in range(len(loops)):
            for j in range(i + 1, len(loops)):
                pair_counts[(loops[i], loops[j])] += 1
    out: list[str] = []
    for (a, b), count in sorted(pair_counts.items()):
        na, nb = loop_node.get(a), loop_node.get(b)
        if na is None or nb is None:
            continue
        # Orient plant/condenser -> air loop (the plant serves the air-side coil).
        if loop_type.get(a) == "AirLoopHVAC" and loop_type.get(b) != "AirLoopHVAC":
            na, nb = nb, na
        label = "coil" if count == 1 else f"{count} coils"
        out.append(f'  {na} -->|"{label}"| {nb}')
    return out


def _loop_zone_edges(graph: HVACGraph, loop_node: dict[str, str], zone_node: dict[str, str]) -> list[str]:
    """Edges from a loop to each zone its equipment serves."""
    key_loops = {v.key: {m.loop_id for m in v.memberships} for v in graph.vertices}
    out: list[str] = []
    for z in graph.zones:
        zid = zone_node[z.name]
        serving = sorted({lid for k in z.equipment_keys for lid in key_loops.get(k, set())})
        for lid in serving:
            ln = loop_node.get(lid)
            if ln is not None:
                out.append(f"  {ln} --> {zid}")
    return out


def render_overview_mermaid(graph: HVACGraph, config: HVACDiagramConfig) -> str:
    """Return a building-level Mermaid ``flowchart`` (loops and zones as nodes)."""
    if not graph.loops and not graph.zones:
        return f'flowchart {config.direction}\n  empty["No HVAC loops found"]'

    lines: list[str] = []
    if config.layout == "elk":
        # Match render_mermaid: ELK lays out large graphs the default dagre engine cannot.
        lines += ["---", "config:", "  layout: elk", "---"]
    lines.append(f"flowchart {config.direction}")
    loop_node: dict[str, str] = {}
    loop_type: dict[str, str] = {loop.loop_id: loop.loop_type for loop in graph.loops}
    for i, loop in enumerate(graph.loops):
        nid = f"L{i}"
        loop_node[loop.loop_id] = nid
        size = len(loop.supply_keys) + len(loop.demand_keys)
        cls = _LOOP_CLASS.get(loop.loop_type, "airloop")
        lines.append(f'  {nid}["{_esc(loop.name)}<br/>{loop.loop_type} · {size} comp"]:::{cls}')

    zone_node: dict[str, str] = {}
    for i, z in enumerate(graph.zones):
        zid = f"Z{i}"
        zone_node[z.name] = zid
        lines.append(f'  {zid}(["{_esc(z.name)}"]):::zone')

    lines += _loop_coupling_edges(graph, loop_node, loop_type)
    lines += _loop_zone_edges(graph, loop_node, zone_node)

    lines.append("  classDef airloop fill:#cfe3f5,stroke:#5a7a8c,color:" + TEXT_COLOR + ";")
    lines.append("  classDef plantloop fill:#f3d6c8,stroke:#8c4f3c,color:" + TEXT_COLOR + ";")
    lines.append("  classDef condenserloop fill:#d8d0e8,stroke:#8c7fb0,color:" + TEXT_COLOR + ";")
    lines.append(f"  classDef zone fill:{ZONE_FILL},stroke:{ZONE_STROKE},color:{TEXT_COLOR};")
    return "\n".join(lines)
