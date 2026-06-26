"""Shared layout planning for the Mermaid and DOT renderers.

Assigns stable, deterministic render ids and groups each vertex into the loop/side
subgraph it should be drawn in (its *primary* membership). A vertex that belongs
to more than one loop — a water coil on an air supply branch and a plant demand
branch — is drawn once, in its first membership; edges to its other loops simply
cross subgraph boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass

from .model import HVACGraph, HVACVertex


@dataclass(frozen=True)
class Layout:
    """Precomputed ids and groupings for rendering."""

    vertex_ids: dict[str, str]
    loop_ids: dict[str, str]
    by_group: dict[tuple[str, str], list[HVACVertex]]
    ungrouped: list[HVACVertex]
    zone_ids: dict[str, str]


def plan_layout(graph: HVACGraph) -> Layout:
    """Assign render ids and group vertices by primary loop/side membership."""
    vertex_ids = {v.key: f"n{i}" for i, v in enumerate(graph.vertices)}
    loop_ids = {loop.loop_id: f"loop{i}" for i, loop in enumerate(graph.loops)}
    by_group: dict[tuple[str, str], list[HVACVertex]] = {}
    ungrouped: list[HVACVertex] = []
    for v in graph.vertices:
        pm = v.primary_membership
        if pm is None or pm.loop_id not in loop_ids:
            ungrouped.append(v)
        else:
            by_group.setdefault((pm.loop_id, pm.side), []).append(v)
    zone_ids = {z.name: f"z{i}" for i, z in enumerate(graph.zones)}
    return Layout(vertex_ids=vertex_ids, loop_ids=loop_ids, by_group=by_group, ungrouped=ungrouped, zone_ids=zone_ids)


def truncate(text: str, limit: int) -> str:
    """Shorten *text* to *limit* characters with an ellipsis (``limit <= 0`` keeps all)."""
    if limit > 0 and len(text) > limit:
        return text[: max(1, limit - 1)] + "…"
    return text


def zone_outflow_targets(graph: HVACGraph) -> dict[str, list[str]]:
    """Map each zone to the vertex keys that consume its return/exhaust nodes.

    These are the components air flows *into* on its way out of the zone — the
    return mixer or plenum (and any zone exhaust fan) — used to draw the return
    leg that closes the air loop.
    """
    node_consumers = {n.name.upper(): n.consumers for n in graph.nodes}
    out: dict[str, list[str]] = {}
    for z in graph.zones:
        seen: set[str] = set()
        targets: list[str] = []
        for name in (*z.return_nodes, *z.exhaust_nodes):
            for key in node_consumers.get(name.upper(), ()):
                if key not in seen:
                    seen.add(key)
                    targets.append(key)
        out[z.name] = targets
    return out
