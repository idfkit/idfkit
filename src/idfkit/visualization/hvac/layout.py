"""Shared layout planning for the Mermaid and DOT renderers.

Assigns stable, deterministic render ids and groups each vertex into the loop/side
subgraph it should be drawn in. A vertex that belongs to more than one loop — a
water coil on an air supply branch and a plant demand branch — is drawn once, in
the first of its memberships whose loop is present in the graph; edges to its
other loops simply cross subgraph boundaries. Falling through to the first
*present* membership (rather than always the first) keeps dual-loop components
inside a kept loop after ``HVACGraph.subset`` filters the other loop out.
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
    zone_clusters: dict[str, list[HVACVertex]]


def plan_layout(graph: HVACGraph) -> Layout:
    """Assign render ids and group vertices by loop/side, zone, or "other"."""
    vertex_ids = {v.key: f"n{i}" for i, v in enumerate(graph.vertices)}
    loop_ids = {loop.loop_id: f"loop{i}" for i, loop in enumerate(graph.loops)}
    zone_ids = {z.name: f"z{i}" for i, z in enumerate(graph.zones)}
    by_group: dict[tuple[str, str], list[HVACVertex]] = {}
    zone_clusters: dict[str, list[HVACVertex]] = {}
    ungrouped: list[HVACVertex] = []
    for v in graph.vertices:
        # Group under the first membership whose loop is present in this graph. A
        # dual-loop vertex (e.g. a water coil on an air supply branch *and* a plant
        # demand branch) lists the air loop first, so after subset(loop_types=[...])
        # filters that loop out we must fall through to the surviving membership
        # rather than dropping the coil into "Other equipment".
        pm = next((m for m in v.memberships if m.loop_id in loop_ids), None)
        if pm is not None:
            by_group.setdefault((pm.loop_id, pm.side), []).append(v)
        elif v.zone is not None and v.zone in zone_ids:
            # Zone equipment with no loop side (a fan-coil fan, an OA mixer, a VRF
            # terminal-unit coil) is drawn inside its zone's cluster, not "Other".
            zone_clusters.setdefault(v.zone, []).append(v)
        else:
            ungrouped.append(v)
    return Layout(
        vertex_ids=vertex_ids,
        loop_ids=loop_ids,
        by_group=by_group,
        ungrouped=ungrouped,
        zone_ids=zone_ids,
        zone_clusters=zone_clusters,
    )


def split_ungrouped(graph: HVACGraph, layout: Layout) -> tuple[list[HVACVertex], list[HVACVertex]]:
    """Partition the ungrouped vertices into ``(other, refrigerant_masters)``.

    VRF outdoor units are pulled out so the renderers can draw them in a dedicated
    "VRF refrigerant system" cluster rather than the generic "Other equipment" bin.
    """
    masters = {r.master_key for r in graph.refrigerant_edges}
    other = [v for v in layout.ungrouped if v.key not in masters]
    refrigerant_masters = [v for v in layout.ungrouped if v.key in masters]
    return other, refrigerant_masters


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
