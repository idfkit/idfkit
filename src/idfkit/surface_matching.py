"""Robust intersect-and-match for interzone surfaces.

Splits coplanar, oppositely-facing building surfaces that overlap into
congruent *matched* fragments (interior ``Surface`` boundary conditions) plus
*remainder* fragments (which keep their original, usually exterior, boundary).
Unlike a simple congruent-pair matcher, this handles the one-to-many case: a
single long wall shared with several smaller neighbouring zones is split into
one matched fragment per neighbour, with any leftover left exterior.

The algorithm is dependency-free and convex-preserving:

1. **Cluster** eligible surfaces by plane (anti-parallel normals share a
   cluster; tolerances absorb wall thickness).
2. **Project** every surface (and its detailed fenestration) into a shared 2-D
   frame for the plane, snap-rounding coordinates so shared edges become
   exactly shared.
3. For each host surface ``P`` facing neighbours ``M1..Mk``, the **matched
   fragments** are the intersections ``P & Mj`` and the **remainder** is ``P``
   minus the union of all ``Mj``.  Because intersection is symmetric, the
   fragment computed from ``P``'s side is congruent to the one from ``Mj``'s
   side, so both zones get matching surfaces with no ordering effects.
4. **Re-lift** each 2-D fragment onto its *own* source surface's plane, so each
   zone's surface stays exactly where the modeller drew it (wall-thickness
   offsets are preserved). Winding falls out: the plus-side lifts to ``+N`` and
   its minus-side partner to ``-N`` -- the reversed-vertex pair EnergyPlus wants.
5. **Rewrite** the document: the first fragment keeps the original surface's
   name (so inbound references survive untouched); the rest become new
   surfaces; detailed windows are re-homed onto the fragment that contains them.

The remainder is computed with a convex-cutter *onion difference* built entirely
on half-plane clipping, so every output piece stays convex (EnergyPlus-friendly
and window-safe). A concave cutter or subject (rare) is ear-clipped into
triangles first.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .geometry import (
    Polygon2D as Poly2D,
)
from .geometry import (
    Polygon3D,
    Vector3D,
    get_surface_coords,
    is_convex_2d,
    line_intersect_2d,
    polygon_area_2d,
    polygon_contains_2d,
    polygon_intersection_2d,
    set_surface_coords,
)

if TYPE_CHECKING:
    from .document import IDFDocument
    from .objects import IDFObject

logger = logging.getLogger(__name__)

_EPS = 1e-9
_LINE_EPS = 1e-15


# ---------------------------------------------------------------------------
# Options and report (typed — no raw dicts)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MatchOptions:
    """Tunable tolerances and scope for :func:`intersect_and_match`.

    Attributes:
        angle_tol_deg: Two surfaces are treated as coplanar when the angle
            between their normals (modulo sign) is within this tolerance.
            Defaults to ~8.1°, matching the ``dot <= -0.99`` antiparallel
            tolerance of the previous ``intersect_match`` implementation.
        max_thickness: Maximum plane-offset difference (metres) tolerated when
            clustering surfaces onto one plane — absorbs construction thickness.
        snap_tol: 2-D snap-rounding grid (metres). Projected coordinates are
            quantised to this grid so shared edges coincide exactly.
        min_area: Fragments below this area (m²) are dropped as slivers.
        min_edge: Fragments with any edge shorter than this (metres) are
            dropped as slivers.
        surface_classes: Uppercase ``surface_type`` values eligible for
            matching. Defaults to walls, floors, ceilings and roofs.
        match_same_zone: When ``False`` (default), two surfaces belonging to the
            same zone are never matched to each other.
    """

    angle_tol_deg: float = 8.1
    max_thickness: float = 0.5
    snap_tol: float = 1e-4
    min_area: float = 1e-4
    min_edge: float = 1e-3
    surface_classes: tuple[str, ...] = ("WALL", "FLOOR", "CEILING", "ROOF")
    match_same_zone: bool = False


@dataclass
class MatchReport:
    """Summary of what :func:`intersect_and_match` changed.

    Attributes:
        pairs_matched: Number of matched interior fragment pairs created.
        surfaces_split: Number of original surfaces broken into >1 fragment.
        fragments_created: Number of *new* surfaces added (kept originals are
            not counted).
        slivers_dropped: Number of below-tolerance fragments discarded.
        fenestration_conflicts: Names of surfaces left unsplit because a
            window/door straddled a cut line (never silently clipped).
        unmatched_exteriors: Number of eligible surfaces that ended up with no
            matched fragment (remained fully exterior).
    """

    pairs_matched: int = 0
    surfaces_split: int = 0
    fragments_created: int = 0
    slivers_dropped: int = 0
    fenestration_conflicts: list[str] = field(default_factory=lambda: [])
    unmatched_exteriors: int = 0


# ---------------------------------------------------------------------------
# 2-D geometry kernel
# ---------------------------------------------------------------------------


def _signed_area(poly: Poly2D) -> float:
    return polygon_area_2d(poly)


def _ensure_ccw(poly: Poly2D) -> Poly2D:
    return poly if _signed_area(poly) >= 0 else list(reversed(poly))


def _bbox(poly: Poly2D) -> tuple[float, float, float, float]:
    xs = [x for x, _ in poly]
    ys = [y for _, y in poly]
    return min(xs), min(ys), max(xs), max(ys)


def _bbox_disjoint(a: Poly2D, b: Poly2D) -> bool:
    ax0, ay0, ax1, ay1 = _bbox(a)
    bx0, by0, bx1, by1 = _bbox(b)
    return ax1 < bx0 - _EPS or bx1 < ax0 - _EPS or ay1 < by0 - _EPS or by1 < ay0 - _EPS


def _is_convex(poly: Poly2D) -> bool:
    return is_convex_2d(poly, eps=_EPS)


def _line_intersect(
    a1: tuple[float, float],
    a2: tuple[float, float],
    b1: tuple[float, float],
    b2: tuple[float, float],
) -> tuple[float, float] | None:
    return line_intersect_2d(a1, a2, b1, b2, eps=_LINE_EPS)


def _clip_halfplane(
    subject: Poly2D,
    e0: tuple[float, float],
    e1: tuple[float, float],
    *,
    keep_left: bool,
) -> Poly2D:
    """Clip *subject* to one side of the directed line ``e0 → e1``.

    ``keep_left`` keeps the region to the left of the edge (the interior of a
    CCW polygon); otherwise the strict complement is kept.
    """

    def side(p: tuple[float, float]) -> float:
        return (e1[0] - e0[0]) * (p[1] - e0[1]) - (e1[1] - e0[1]) * (p[0] - e0[0])

    out: Poly2D = []
    n = len(subject)
    for j in range(n):
        cur = subject[j]
        nxt = subject[(j + 1) % n]
        sc, sn = side(cur), side(nxt)
        cur_in = (sc >= -_EPS) if keep_left else (sc <= _EPS)
        nxt_in = (sn >= -_EPS) if keep_left else (sn <= _EPS)
        if cur_in:
            out.append(cur)
            if not nxt_in:
                pt = _line_intersect(cur, nxt, e0, e1)
                if pt is not None:
                    out.append(pt)
        elif nxt_in:
            pt = _line_intersect(cur, nxt, e0, e1)
            if pt is not None:
                out.append(pt)
    return out


def _ear_cross(verts: list[tuple[float, float]], idx: list[int], k: int) -> float:
    """Cross product at candidate ear tip ``idx[k]`` (larger = more convex)."""
    m = len(idx)
    a, b, c = verts[idx[(k - 1) % m]], verts[idx[k]], verts[idx[(k + 1) % m]]
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _triangulate(poly: Poly2D) -> list[Poly2D]:
    """Ear-clip a simple polygon into triangles (each convex)."""
    verts = _ensure_ccw(_clean_poly(poly))
    if len(verts) < 3:
        return []
    if len(verts) == 3:
        return [verts]
    triangles: list[Poly2D] = []
    idx = list(range(len(verts)))
    guard = 0
    while len(idx) > 3 and guard < len(idx) * len(idx):
        guard += 1
        ear_found = False
        m = len(idx)
        for k in range(m):
            i0, i1, i2 = idx[(k - 1) % m], idx[k], idx[(k + 1) % m]
            a, b, c = verts[i0], verts[i1], verts[i2]
            cross = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
            if cross <= _EPS:  # reflex or collinear — not an ear tip
                continue
            tri = [a, b, c]
            if any(idx[o] not in (i0, i1, i2) and _point_in_triangle(verts[idx[o]], a, b, c) for o in range(m)):
                continue
            triangles.append(tri)
            idx.pop(k)
            ear_found = True
            break
        if not ear_found:
            # No strictly-valid ear (degenerate/near-collinear vertices from
            # snap-rounding can starve the strict test). Clip the least-reflex
            # candidate anyway so triangulation always covers the full
            # polygon instead of silently dropping the untriangulated tail.
            best_k = max(range(m), key=lambda k: _ear_cross(verts, idx, k))
            i0, i1, i2 = idx[(best_k - 1) % m], idx[best_k], idx[(best_k + 1) % m]
            triangles.append([verts[i0], verts[i1], verts[i2]])
            idx.pop(best_k)
    if len(idx) == 3:
        triangles.append([verts[idx[0]], verts[idx[1]], verts[idx[2]]])
    return triangles


def _point_in_triangle(
    p: tuple[float, float],
    a: tuple[float, float],
    b: tuple[float, float],
    c: tuple[float, float],
) -> bool:
    def sign(u: tuple[float, float], v: tuple[float, float], w: tuple[float, float]) -> float:
        return (u[0] - w[0]) * (v[1] - w[1]) - (v[0] - w[0]) * (u[1] - w[1])

    d1, d2, d3 = sign(p, a, b), sign(p, b, c), sign(p, c, a)
    has_neg = d1 < -_EPS or d2 < -_EPS or d3 < -_EPS
    has_pos = d1 > _EPS or d2 > _EPS or d3 > _EPS
    return not (has_neg and has_pos)


def _convex_difference(subject: Poly2D, cutter: Poly2D) -> list[Poly2D]:
    """``subject`` minus a **convex** ``cutter``, as disjoint convex pieces.

    Onion decomposition: ``piece[i] = subject & inside(e0..e[i-1]) & outside(e[i])``.
    The union of pieces equals ``subject`` minus ``cutter`` exactly and every
    piece is convex.
    """
    if _bbox_disjoint(subject, cutter):
        return [subject]
    cutter = _ensure_ccw(cutter)
    pieces: list[Poly2D] = []
    remaining = list(subject)
    n = len(cutter)
    for i in range(n):
        e0, e1 = cutter[i], cutter[(i + 1) % n]
        outside = _clip_halfplane(remaining, e0, e1, keep_left=False)
        if len(outside) >= 3 and abs(_signed_area(outside)) > _EPS:
            pieces.append(outside)
        remaining = _clip_halfplane(remaining, e0, e1, keep_left=True)
        if len(remaining) < 3:
            break
    return pieces


def _difference_one(subject: Poly2D, cutter: Poly2D) -> list[Poly2D]:
    """``subject`` minus an arbitrary simple ``cutter``, as convex pieces.

    ``_convex_difference`` only guarantees convex output when ``subject``
    itself is convex, so a concave subject is triangulated first (a concave
    cutter is already handled below).
    """
    if not _is_convex(subject):
        pieces: list[Poly2D] = []
        for tri in _triangulate(subject):
            pieces.extend(_difference_one(tri, cutter))
        return pieces
    if _is_convex(cutter):
        return _convex_difference(subject, cutter)
    pieces = [subject]
    for tri in _triangulate(cutter):
        nxt: list[Poly2D] = []
        for p in pieces:
            nxt.extend(_convex_difference(p, tri))
        pieces = nxt
    return pieces


def _difference_many(subject: Poly2D, cutters: list[Poly2D]) -> list[Poly2D]:
    """``subject`` minus the union of several cutters."""
    pieces = [subject]
    for c in cutters:
        nxt: list[Poly2D] = []
        for p in pieces:
            nxt.extend(_difference_one(p, c))
        pieces = nxt
    return pieces


def _clean_poly(poly: Poly2D) -> Poly2D:
    """Drop duplicate and collinear consecutive vertices."""
    pts = list(poly)
    # Remove consecutive duplicates.
    deduped: Poly2D = []
    for p in pts:
        if not deduped or abs(p[0] - deduped[-1][0]) > _EPS or abs(p[1] - deduped[-1][1]) > _EPS:
            deduped.append(p)
    if len(deduped) > 1 and abs(deduped[0][0] - deduped[-1][0]) <= _EPS and abs(deduped[0][1] - deduped[-1][1]) <= _EPS:
        deduped.pop()
    n = len(deduped)
    if n < 3:
        return deduped
    # Remove collinear vertices.
    out: Poly2D = []
    for i in range(n):
        a, b, c = deduped[(i - 1) % n], deduped[i], deduped[(i + 1) % n]
        cross = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        if abs(cross) > _EPS:
            out.append(b)
    return out if len(out) >= 3 else deduped


def _min_edge_len(poly: Poly2D) -> float:
    n = len(poly)
    if n < 2:
        return 0.0
    return min(math.hypot(poly[(i + 1) % n][0] - poly[i][0], poly[(i + 1) % n][1] - poly[i][1]) for i in range(n))


# ---------------------------------------------------------------------------
# Plane frame + projection
# ---------------------------------------------------------------------------


@dataclass
class _PlaneFrame:
    """Orthonormal 2-D frame ``(u, v, normal)`` anchored at ``origin``."""

    origin: Vector3D
    u: Vector3D
    v: Vector3D
    normal: Vector3D

    def to_2d(self, p: Vector3D, snap_tol: float) -> tuple[float, float]:
        rel = p - self.origin
        a = round(rel.dot(self.u) / snap_tol) * snap_tol
        b = round(rel.dot(self.v) / snap_tol) * snap_tol
        return (a, b)

    def to_3d(self, uv: tuple[float, float], plane_offset: float) -> Vector3D:
        """Lift ``uv`` back to 3-D onto the plane ``point·normal == plane_offset``."""
        base = self.origin + self.u * uv[0] + self.v * uv[1]
        return base + self.normal * (plane_offset - base.dot(self.normal))


def _build_frame(normal: Vector3D, verts: list[Vector3D]) -> _PlaneFrame:
    axes = (Vector3D(1, 0, 0), Vector3D(0, 1, 0), Vector3D(0, 0, 1))
    ref = min(axes, key=lambda ax: abs(normal.dot(ax)))
    u = normal.cross(ref).normalize()
    v = normal.cross(u).normalize()
    ox = sum(p.x for p in verts) / len(verts)
    oy = sum(p.y for p in verts) / len(verts)
    oz = sum(p.z for p in verts) / len(verts)
    return _PlaneFrame(Vector3D(ox, oy, oz), u, v, normal)


def _canonical_normal(n: Vector3D) -> Vector3D:
    """Flip *n* to a deterministic sign (largest-magnitude component positive)."""
    ax, ay, az = abs(n.x), abs(n.y), abs(n.z)
    if az >= ax and az >= ay:
        comp = n.z
    elif ay >= ax:
        comp = n.y
    else:
        comp = n.x
    return -n if comp < 0 else n


# ---------------------------------------------------------------------------
# Internal working structures
# ---------------------------------------------------------------------------


@dataclass
class _Surf:
    obj: IDFObject
    normal: Vector3D
    verts: list[Vector3D]
    centroid: Vector3D
    zone: str
    surface_type: str


@dataclass
class _ProjSurf:
    surf: _Surf
    poly2d: Poly2D  # CCW in the cluster frame
    side: int  # +1 or -1 relative to the cluster's canonical normal
    plane_offset: float  # verts · frame.normal


@dataclass
class _Region:
    rid: int
    plus: _ProjSurf
    minus: _ProjSurf
    overlap: Poly2D


@dataclass
class _Frag:
    poly2d: Poly2D
    kind: str  # "matched" | "remainder"
    region: _Region | None


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def intersect_and_match(doc: IDFDocument, options: MatchOptions | None = None) -> MatchReport:
    """Intersect and match coplanar interzone surfaces, splitting as needed.

    Coplanar, oppositely-facing surfaces that overlap are split into congruent
    matched fragments (interior ``Surface`` boundary) plus exterior remainders.
    A single surface abutting several neighbours is split into one matched
    fragment per neighbour. The document is modified in place.

    Args:
        doc: The document to modify.
        options: Tolerances and scope; defaults to :class:`MatchOptions`.

    Returns:
        A :class:`MatchReport` describing what changed.

    Examples:
        >>> from idfkit import new_document
        >>> doc = new_document(version=(24, 1, 0))
        >>> report = intersect_and_match(doc)
        >>> report.pairs_matched
        0
    """
    opts = options or MatchOptions()
    report = MatchReport()

    surfs = _collect_surfaces(doc, opts)
    clusters = _cluster_by_plane(surfs, opts)

    for cluster in clusters:
        _process_cluster(doc, cluster, opts, report)

    logger.debug(
        "intersect_and_match: %d pairs, %d split, %d new fragments, %d slivers, %d conflicts",
        report.pairs_matched,
        report.surfaces_split,
        report.fragments_created,
        report.slivers_dropped,
        len(report.fenestration_conflicts),
    )
    return report


def _collect_surfaces(doc: IDFDocument, opts: MatchOptions) -> list[_Surf]:
    result: list[_Surf] = []
    for obj in doc["BuildingSurface:Detailed"]:
        st = (getattr(obj, "surface_type", None) or "").upper()
        if st not in opts.surface_classes:
            continue
        poly = get_surface_coords(obj)
        if poly is None:
            continue
        result.append(
            _Surf(
                obj=obj,
                normal=poly.normal,
                verts=list(poly.vertices),
                centroid=poly.centroid,
                zone=(getattr(obj, "zone_name", None) or ""),
                surface_type=st,
            )
        )
    return result


def _cluster_by_plane(surfs: list[_Surf], opts: MatchOptions) -> list[list[_Surf]]:
    cos_tol = math.cos(math.radians(opts.angle_tol_deg))
    clusters: list[list[_Surf]] = []
    reps: list[tuple[Vector3D, float]] = []  # (canonical normal, plane offset)

    for s in surfs:
        cn = _canonical_normal(s.normal)
        offset = s.centroid.dot(cn)
        placed = False
        for idx, (rn, roff) in enumerate(reps):
            if abs(cn.dot(rn)) >= cos_tol and abs(offset - roff) <= opts.max_thickness:
                clusters[idx].append(s)
                placed = True
                break
        if not placed:
            clusters.append([s])
            reps.append((cn, offset))
    return [c for c in clusters if len(c) >= 2]


def _process_cluster(doc: IDFDocument, cluster: list[_Surf], opts: MatchOptions, report: MatchReport) -> None:
    normal = _canonical_normal(cluster[0].normal)
    all_verts = [v for s in cluster for v in s.verts]
    frame = _build_frame(normal, all_verts)

    projected: list[_ProjSurf] = []
    for s in cluster:
        poly2d = [frame.to_2d(v, opts.snap_tol) for v in s.verts]
        poly2d = _clean_poly(poly2d)
        if len(poly2d) < 3:
            continue
        side = 1 if s.normal.dot(normal) >= 0 else -1
        plane_offset = s.centroid.dot(normal)
        projected.append(_ProjSurf(s, _ensure_ccw(poly2d), side, plane_offset))

    plus = [p for p in projected if p.side > 0]
    minus = [p for p in projected if p.side < 0]
    if not plus or not minus:
        return

    regions, region_drops = _build_regions(plus, minus, opts)
    report.slivers_dropped += region_drops
    if not regions:
        return

    # Resolve window-straddle conflicts by cancelling all regions touching a
    # conflicted surface, then recomputing, until stable.
    conflicted: set[int] = set()
    surviving: list[_Region] = []
    frags_by_surf: dict[int, list[_Frag]] = {}
    remainder_drops = 0
    while True:
        surviving = [
            r for r in regions if id(r.plus.surf.obj) not in conflicted and id(r.minus.surf.obj) not in conflicted
        ]
        frags_by_surf = {}
        remainder_drops = 0
        for p in projected:
            frags, dropped = _fragments_for(p, surviving, opts)
            frags_by_surf[id(p.surf.obj)] = frags
            remainder_drops += dropped
        new_conflicts = _detect_conflicts(doc, projected, frags_by_surf, frame, opts, conflicted)
        if not new_conflicts:
            break
        conflicted |= new_conflicts
    report.slivers_dropped += remainder_drops

    for name in sorted({_name_of(p, conflicted) for p in projected if id(p.surf.obj) in conflicted}):
        if name:
            report.fenestration_conflicts.append(name)

    _emit(doc, projected, surviving, frags_by_surf, frame, opts, report, conflicted)


def _name_of(p: _ProjSurf, conflicted: set[int]) -> str:
    return p.surf.obj.name if id(p.surf.obj) in conflicted else ""


def _build_regions(plus: list[_ProjSurf], minus: list[_ProjSurf], opts: MatchOptions) -> tuple[list[_Region], int]:
    regions: list[_Region] = []
    dropped = 0
    rid = 0
    for p in plus:
        for m in minus:
            if not opts.match_same_zone and p.surf.zone and p.surf.zone == m.surf.zone:
                continue
            if _bbox_disjoint(p.poly2d, m.poly2d):
                continue
            inter = polygon_intersection_2d(p.poly2d, m.poly2d)
            if inter is None:
                continue
            inter = _clean_poly(list(inter))
            if len(inter) < 3:
                continue
            if abs(_signed_area(inter)) < opts.min_area or _min_edge_len(inter) < opts.min_edge:
                dropped += 1
                continue
            regions.append(_Region(rid, p, m, _ensure_ccw(inter)))
            rid += 1
    return regions, dropped


def _fragments_for(p: _ProjSurf, regions: list[_Region], opts: MatchOptions) -> tuple[list[_Frag], int]:
    mine = [r for r in regions if r.plus.surf.obj is p.surf.obj or r.minus.surf.obj is p.surf.obj]
    frags: list[_Frag] = [_Frag(r.overlap, "matched", r) for r in mine]
    remainder = _difference_many(p.poly2d, [r.overlap for r in mine])
    dropped = 0
    for piece in remainder:
        piece = _clean_poly(piece)
        if len(piece) < 3:
            continue
        if abs(_signed_area(piece)) >= opts.min_area and _min_edge_len(piece) >= opts.min_edge:
            frags.append(_Frag(_ensure_ccw(piece), "remainder", None))
        else:
            dropped += 1
    return frags, dropped


def _detect_conflicts(
    doc: IDFDocument,
    projected: list[_ProjSurf],
    frags_by_surf: dict[int, list[_Frag]],
    frame: _PlaneFrame,
    opts: MatchOptions,
    already: set[int],
) -> set[int]:
    new_conflicts: set[int] = set()
    for p in projected:
        sid = id(p.surf.obj)
        if sid in already:
            continue
        frags = frags_by_surf[sid]
        if len(frags) <= 1:
            continue  # not split → nothing to reassign
        detailed, others = _collect_children(doc, p.surf.obj.name)
        # Un-locatable children (simple Window/Door) block a split.
        if others:
            new_conflicts.add(sid)
            continue
        for win in detailed:
            wpoly = get_surface_coords(win)
            if wpoly is None:
                continue
            w2d = _ensure_ccw([frame.to_2d(v, opts.snap_tol) for v in wpoly.vertices])
            if not any(polygon_contains_2d(f.poly2d, w2d) for f in frags):
                new_conflicts.add(sid)
                break
    return new_conflicts


def _collect_children(doc: IDFDocument, name: str) -> tuple[list[IDFObject], list[IDFObject]]:
    """Split objects referencing *name* into re-homable windows and blockers.

    ``detailed`` holds ``FenestrationSurface:Detailed`` objects attached via
    ``building_surface_name`` — they get re-homed onto the fragment that
    contains them. Everything else that references *name* in any field (a
    simple ``Window``/``Door``, an AirflowNetwork surface component, a
    ``SurfaceProperty:*``, ...) goes to ``others`` and blocks the split,
    since it cannot be safely re-homed onto a specific fragment.
    """
    detailed: list[IDFObject] = []
    others: list[IDFObject] = []
    for ref, field_name in doc.references.get_referencing_with_fields(name):
        if field_name == "building_surface_name" and ref.obj_type == "FenestrationSurface:Detailed":
            detailed.append(ref)
        else:
            others.append(ref)
    return detailed, others


def _emit(
    doc: IDFDocument,
    projected: list[_ProjSurf],
    regions: list[_Region],
    frags_by_surf: dict[int, list[_Frag]],
    frame: _PlaneFrame,
    opts: MatchOptions,
    report: MatchReport,
    conflicted: set[int],
) -> None:
    report.pairs_matched += len(regions)

    # Pass 1: assign a name to every fragment and record it per region+side.
    names: dict[int, list[str]] = {}  # surf id -> fragment names (parallel to frags)
    region_names: dict[int, dict[int, str]] = {}  # region id -> {side: name}
    used = {o.name for o in doc["BuildingSurface:Detailed"]}
    for p in projected:
        sid = id(p.surf.obj)
        if sid in conflicted:
            continue
        frags = frags_by_surf[sid]
        if _is_noop(frags):
            continue
        frag_names: list[str] = []
        for i, frag in enumerate(frags):
            fname = p.surf.obj.name if i == 0 else _unique_name(p.surf.obj.name, i, used)
            used.add(fname)
            frag_names.append(fname)
            if frag.region is not None:
                region_names.setdefault(frag.region.rid, {})[p.side] = fname
        names[sid] = frag_names

    # Pass 2: write geometry, boundary conditions and re-home windows.
    for p in projected:
        sid = id(p.surf.obj)
        if sid not in names:
            if sid not in conflicted and not any(f.kind == "matched" for f in frags_by_surf.get(sid, [])):
                report.unmatched_exteriors += 1
            continue
        _emit_surface(doc, p, frags_by_surf[sid], names[sid], region_names, frame, opts, report)


def _is_noop(frags: list[_Frag]) -> bool:
    return len(frags) == 1 and frags[0].kind == "remainder"


def _unique_name(base: str, i: int, used: set[str]) -> str:
    candidate = f"{base} {i + 1}"
    n = i + 1
    while candidate in used:
        n += 1
        candidate = f"{base} {n}"
    return candidate


def _emit_surface(
    doc: IDFDocument,
    p: _ProjSurf,
    frags: list[_Frag],
    frag_names: list[str],
    region_names: dict[int, dict[int, str]],
    frame: _PlaneFrame,
    opts: MatchOptions,
    report: MatchReport,
) -> None:
    surf = p.surf.obj
    orig_bc = _capture_bc(surf)
    construction = getattr(surf, "construction_name", None) or ""
    detailed, _ = _collect_children(doc, surf.name)

    if len(frags) > 1:
        report.surfaces_split += 1

    for i, (frag, fname) in enumerate(zip(frags, frag_names, strict=True)):
        poly3d = _lift_fragment(frag.poly2d, p, frame)
        target = surf if i == 0 else _add_surface(doc, fname, p.surf, construction)
        if i != 0:
            report.fragments_created += 1
        set_surface_coords(target, poly3d)
        _apply_bc(target, frag, region_names, p.side, orig_bc)
        _rehome_windows(detailed, frag, fname, surf.name, frame, opts)


def _lift_fragment(poly2d: Poly2D, p: _ProjSurf, frame: _PlaneFrame) -> Polygon3D:
    ordered = poly2d if p.side > 0 else list(reversed(poly2d))
    return Polygon3D([frame.to_3d(uv, p.plane_offset) for uv in ordered])


@dataclass
class _BC:
    obc: str
    obc_object: str
    sun: str
    wind: str


def _capture_bc(surf: IDFObject) -> _BC:
    return _BC(
        obc=getattr(surf, "outside_boundary_condition", None) or "Outdoors",
        obc_object=getattr(surf, "outside_boundary_condition_object", None) or "",
        sun=getattr(surf, "sun_exposure", None) or "SunExposed",
        wind=getattr(surf, "wind_exposure", None) or "WindExposed",
    )


def _apply_bc(
    target: IDFObject,
    frag: _Frag,
    region_names: dict[int, dict[int, str]],
    side: int,
    orig_bc: _BC,
) -> None:
    if frag.kind == "matched" and frag.region is not None:
        partner = region_names.get(frag.region.rid, {}).get(-side, "")
        target.outside_boundary_condition = "Surface"
        target.outside_boundary_condition_object = partner
        target.sun_exposure = "NoSun"
        target.wind_exposure = "NoWind"
    else:
        target.outside_boundary_condition = orig_bc.obc
        target.outside_boundary_condition_object = orig_bc.obc_object
        target.sun_exposure = orig_bc.sun
        target.wind_exposure = orig_bc.wind


def _add_surface(doc: IDFDocument, name: str, template: _Surf, construction: str) -> IDFObject:
    return doc.add(
        "BuildingSurface:Detailed",
        name,
        {
            "surface_type": template.surface_type.title(),
            "construction_name": construction,
            "zone_name": template.zone,
        },
        validate=False,
    )


def _rehome_windows(
    detailed: list[IDFObject],
    frag: _Frag,
    frag_name: str,
    orig_name: str,
    frame: _PlaneFrame,
    opts: MatchOptions,
) -> None:
    if frag_name == orig_name:
        return  # windows already reference this name
    for win in detailed:
        if (getattr(win, "building_surface_name", None) or "") != orig_name:
            continue
        wpoly = get_surface_coords(win)
        if wpoly is None:
            continue
        w2d = _ensure_ccw([frame.to_2d(v, opts.snap_tol) for v in wpoly.vertices])
        if polygon_contains_2d(frag.poly2d, w2d):
            win.building_surface_name = frag_name
