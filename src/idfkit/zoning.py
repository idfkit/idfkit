"""Automatic thermal zoning for EnergyPlus models.

Splits a 2-D building footprint into thermal zones using one of several
standard schemes and creates all ``Zone``, ``BuildingSurface:Detailed``,
and (optionally) ``Construction:AirBoundary`` objects needed for
simulation.

Three zoning schemes are provided:

* **by_storey** - one zone per floor.
* **core_perimeter** - four orientation-based perimeter zones plus an
  interior core zone per floor.  Perimeter depth defaults to
  **4.57 m (15 ft)** per ASHRAE 90.1 Appendix G and the DOE prototype
  buildings.
* **custom** - the caller supplies named polygons for each floor.

Footprint helpers for common commercial shapes (rectangle, L, U, T, H,
courtyard) are included so users never have to compute vertices by hand.

Examples:
    ```python
    from idfkit import new_document
    from idfkit.zoning import (
        ZoningScheme,
        create_building,
        footprint_rectangle,
    )

    doc = new_document()
    zones = create_building(
        doc,
        name="Office",
        footprint=footprint_rectangle(50, 30),
        floor_to_floor=3.5,
        num_stories=3,
        zoning=ZoningScheme.CORE_PERIMETER,
        perimeter_depth=4.57,
    )
    ```
"""

from __future__ import annotations

import enum
import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .geometry import Polygon3D, Vector3D, set_surface_coords
from .geometry_builders import WALL_ORDER, get_geometry_convention, horizontal_poly

if TYPE_CHECKING:
    from .document import IDFDocument
    from .objects import IDFObject

# ASHRAE 90.1 Appendix G default perimeter depth (15 ft ≈ 4.57 m).
ASHRAE_PERIMETER_DEPTH: float = 4.57

# Minimum footprint inradius below which core-perimeter zoning falls back
# to single-zone.
_MIN_INRADIUS: float = 0.5


# ---------------------------------------------------------------------------
# ZoningScheme enum
# ---------------------------------------------------------------------------


class ZoningScheme(enum.Enum):
    """Thermal zoning strategy.

    Attributes:
        BY_STOREY: One zone per floor.
        CORE_PERIMETER: Core + 4 perimeter zones per floor.
        CUSTOM: User-supplied zone polygons per floor.
    """

    BY_STOREY = "by_storey"
    CORE_PERIMETER = "core_perimeter"
    CUSTOM = "custom"


# ---------------------------------------------------------------------------
# Footprint generators
# ---------------------------------------------------------------------------


def footprint_rectangle(
    width: float,
    depth: float,
    origin: tuple[float, float] = (0.0, 0.0),
) -> list[tuple[float, float]]:
    """Return a rectangular footprint (counter-clockwise).

    Args:
        width: Dimension along the X axis (metres).
        depth: Dimension along the Y axis (metres).
        origin: ``(x, y)`` of the lower-left corner.
    """
    x, y = origin
    return [(x, y), (x + width, y), (x + width, y + depth), (x, y + depth)]


def footprint_l_shape(
    width: float,
    depth: float,
    wing_width: float,
    wing_depth: float,
    origin: tuple[float, float] = (0.0, 0.0),
) -> list[tuple[float, float]]:
    """Return an L-shaped footprint (counter-clockwise).

    The *base* rectangle runs from the origin along ``width`` (X) and
    ``depth`` (Y).  A shorter wing extends upward from the left side
    with dimensions ``wing_width`` x ``wing_depth``.

        ```text
        ┌────────┐
        │  wing  │
        │        │
        ├────────┴──────────┐
        │      base         │
        └───────────────────┘
        ```

    Args:
        width: Base width (X).
        depth: Base depth (Y).
        wing_width: Wing width (X), must be <= *width*.
        wing_depth: Wing depth (Y), added above the base.
        origin: ``(x, y)`` of the lower-left corner.
    """
    if wing_width > width:
        msg = f"wing_width ({wing_width}) must be <= width ({width})"
        raise ValueError(msg)
    x, y = origin
    return [
        (x, y),
        (x + width, y),
        (x + width, y + depth),
        (x + wing_width, y + depth),
        (x + wing_width, y + depth + wing_depth),
        (x, y + depth + wing_depth),
    ]


def footprint_u_shape(
    width: float,
    depth: float,
    courtyard_width: float,
    courtyard_depth: float,
    origin: tuple[float, float] = (0.0, 0.0),
) -> list[tuple[float, float]]:
    """Return a U-shaped footprint (counter-clockwise).

    The overall bounding box is ``width`` x ``depth``.  A rectangular
    courtyard is cut from the top centre of the footprint.

        ```text
        ┌──────┐    ┌──────┐
        │      │    │      │
        │      └────┘      │
        │                  │
        └──────────────────┘
        ```

    Args:
        width: Overall width (X).
        depth: Overall depth (Y).
        courtyard_width: Width of the courtyard opening (X).
        courtyard_depth: Depth of the courtyard from the top edge (Y).
        origin: ``(x, y)`` of the lower-left corner.
    """
    if courtyard_width >= width:
        msg = f"courtyard_width ({courtyard_width}) must be < width ({width})"
        raise ValueError(msg)
    if courtyard_depth >= depth:
        msg = f"courtyard_depth ({courtyard_depth}) must be < depth ({depth})"
        raise ValueError(msg)
    x, y = origin
    cx_left = x + (width - courtyard_width) / 2
    cx_right = cx_left + courtyard_width
    cy_bottom = y + depth - courtyard_depth
    return [
        (x, y),
        (x + width, y),
        (x + width, y + depth),
        (cx_right, y + depth),
        (cx_right, cy_bottom),
        (cx_left, cy_bottom),
        (cx_left, y + depth),
        (x, y + depth),
    ]


def footprint_t_shape(
    base_width: float,
    base_depth: float,
    top_width: float,
    top_depth: float,
    origin: tuple[float, float] = (0.0, 0.0),
) -> list[tuple[float, float]]:
    """Return a T-shaped footprint (counter-clockwise).

    A narrower base rectangle is centred below a wider top bar.

        ```text
        ┌──────────────────────┐
        │       top bar        │
        └───┐              ┌───┘
            │    base      │
            └──────────────┘
        ```

    Args:
        base_width: Width of the stem (X).
        base_depth: Depth of the stem (Y).
        top_width: Width of the top bar (X), must be >= *base_width*.
        top_depth: Depth of the top bar (Y).
        origin: ``(x, y)`` of the lower-left corner of the stem.
    """
    if top_width < base_width:
        msg = f"top_width ({top_width}) must be >= base_width ({base_width})"
        raise ValueError(msg)
    x, y = origin
    overhang = (top_width - base_width) / 2
    return [
        (x, y),
        (x + base_width, y),
        (x + base_width, y + base_depth),
        (x + base_width + overhang, y + base_depth),
        (x + base_width + overhang, y + base_depth + top_depth),
        (x - overhang, y + base_depth + top_depth),
        (x - overhang, y + base_depth),
        (x, y + base_depth),
    ]


def footprint_h_shape(
    width: float,
    depth: float,
    courtyard_width: float,
    courtyard_depth: float,
    origin: tuple[float, float] = (0.0, 0.0),
) -> list[tuple[float, float]]:
    """Return an H-shaped footprint (counter-clockwise).

    Two symmetrical courtyards are cut from the left and right sides of
    the bounding rectangle.

        ```text
        ┌──────┐    ┌──────┐
        │      └────┘      │
        │     connector    │
        │      ┌────┐      │
        └──────┘    └──────┘
        ```

    Args:
        width: Overall width (X).
        depth: Overall depth (Y).
        courtyard_width: Width of each courtyard notch (X).
        courtyard_depth: Depth of each courtyard notch (Y).
        origin: ``(x, y)`` of the lower-left corner.
    """
    if courtyard_width >= width:
        msg = f"courtyard_width ({courtyard_width}) must be < width ({width})"
        raise ValueError(msg)
    if 2 * courtyard_depth >= depth:
        msg = f"2 * courtyard_depth ({2 * courtyard_depth}) must be < depth ({depth})"
        raise ValueError(msg)
    x, y = origin
    w2 = (width - courtyard_width) / 2
    cy_bot_top = y + courtyard_depth
    cy_top_bot = y + depth - courtyard_depth
    cx_left = x + w2
    cx_right = x + w2 + courtyard_width
    return [
        (x, y),
        (cx_left, y),
        (cx_left, cy_bot_top),
        (cx_right, cy_bot_top),
        (cx_right, y),
        (x + width, y),
        (x + width, y + depth),
        (cx_right, y + depth),
        (cx_right, cy_top_bot),
        (cx_left, cy_top_bot),
        (cx_left, y + depth),
        (x, y + depth),
    ]


def footprint_courtyard(
    outer_width: float,
    outer_depth: float,
    inner_width: float,
    inner_depth: float,
    origin: tuple[float, float] = (0.0, 0.0),
) -> list[tuple[float, float]]:
    """Return a courtyard (donut) footprint as a single slit polygon.

    The polygon traces the outer boundary counter-clockwise, steps into
    the inner courtyard through a slit at the bottom-right corner, traces
    the courtyard clockwise, and returns.  This is a valid simple polygon
    that EnergyPlus can handle.

        ```text
        ┌──────────────────┐
        │  ┌────────────┐  │
        │  │  courtyard │  │
        │  └────────────┘  │
        └──────────────────┘
        ```

    Args:
        outer_width: Outer bounding box width (X).
        outer_depth: Outer bounding box depth (Y).
        inner_width: Courtyard width (X), must be < *outer_width*.
        inner_depth: Courtyard depth (Y), must be < *outer_depth*.
        origin: ``(x, y)`` of the lower-left corner.
    """
    if inner_width >= outer_width:
        msg = f"inner_width ({inner_width}) must be < outer_width ({outer_width})"
        raise ValueError(msg)
    if inner_depth >= outer_depth:
        msg = f"inner_depth ({inner_depth}) must be < outer_depth ({outer_depth})"
        raise ValueError(msg)
    x, y = origin
    margin_x = (outer_width - inner_width) / 2
    margin_y = (outer_depth - inner_depth) / 2
    # Outer CCW
    ix0 = x + margin_x
    iy0 = y + margin_y
    ix1 = ix0 + inner_width
    iy1 = iy0 + inner_depth
    return [
        # Outer rectangle (CCW)
        (x, y),
        (x + outer_width, y),
        (x + outer_width, y + outer_depth),
        (x, y + outer_depth),
        # Slit down to inner (from outer top-left back down to inner)
        (x, y + margin_y),  # slit entry
        # Inner rectangle (CW to cut a hole)
        (ix0, iy0),
        (ix0, iy1),
        (ix1, iy1),
        (ix1, iy0),
        # Slit back out
        (x, y + margin_y),  # slit exit (same point, degenerate edge)
    ]


# ---------------------------------------------------------------------------
# Core-perimeter polygon splitting
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ZoneFootprint:
    """Named 2-D polygon for one thermal zone on one floor."""

    name_suffix: str  # e.g. "Core", "Perimeter_South"
    polygon: list[tuple[float, float]]


def _offset_edge(
    p1: tuple[float, float],
    p2: tuple[float, float],
    dist: float,
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Offset a directed edge inward (to the left) by *dist*."""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    length = math.hypot(dx, dy)
    if length < 1e-12:
        return p1, p2
    # Inward normal (left of travel direction)
    nx = -dy / length * dist
    ny = dx / length * dist
    return (p1[0] + nx, p1[1] + ny), (p2[0] + nx, p2[1] + ny)


def _line_intersection(
    a1: tuple[float, float],
    a2: tuple[float, float],
    b1: tuple[float, float],
    b2: tuple[float, float],
) -> tuple[float, float] | None:
    """Intersection of infinite lines through (a1,a2) and (b1,b2)."""
    d1x = a2[0] - a1[0]
    d1y = a2[1] - a1[1]
    d2x = b2[0] - b1[0]
    d2y = b2[1] - b1[1]
    denom = d1x * d2y - d1y * d2x
    if abs(denom) < 1e-12:
        return None  # parallel
    t = ((b1[0] - a1[0]) * d2y - (b1[1] - a1[1]) * d2x) / denom
    return (a1[0] + t * d1x, a1[1] + t * d1y)


def _polygon_area_signed(poly: list[tuple[float, float]]) -> float:
    """Signed area of a 2-D polygon (positive = CCW)."""
    n = len(poly)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += poly[i][0] * poly[j][1]
        area -= poly[j][0] * poly[i][1]
    return area / 2.0


def _inset_polygon_2d(
    footprint: list[tuple[float, float]],
    depth: float,
) -> list[tuple[float, float]] | None:
    """Offset a convex CCW polygon inward by *depth*.

    Returns ``None`` if the resulting polygon degenerates (self-intersects
    or collapses).
    """
    n = len(footprint)
    if n < 3:
        return None

    # Offset each edge inward
    offset_edges: list[tuple[tuple[float, float], tuple[float, float]]] = []
    for i in range(n):
        p1 = footprint[i]
        p2 = footprint[(i + 1) % n]
        offset_edges.append(_offset_edge(p1, p2, depth))

    # Intersect consecutive offset edges to find inner vertices
    inner: list[tuple[float, float]] = []
    for i in range(n):
        prev = (i - 1) % n
        pt = _line_intersection(
            offset_edges[prev][0],
            offset_edges[prev][1],
            offset_edges[i][0],
            offset_edges[i][1],
        )
        if pt is None:
            return None  # parallel edges → degenerate
        inner.append(pt)

    # Check that the result is still a valid polygon (positive area,
    # not self-intersecting in the simple convex case).
    if _polygon_area_signed(inner) < 1e-6:
        return None  # collapsed

    return inner


def _segments_intersect(
    a1: tuple[float, float],
    a2: tuple[float, float],
    b1: tuple[float, float],
    b2: tuple[float, float],
) -> bool:
    """Check whether two line segments (a1-a2) and (b1-b2) cross."""
    d1x = a2[0] - a1[0]
    d1y = a2[1] - a1[1]
    d2x = b2[0] - b1[0]
    d2y = b2[1] - b1[1]
    denom = d1x * d2y - d1y * d2x
    if abs(denom) < 1e-12:
        return False  # parallel
    t = ((b1[0] - a1[0]) * d2y - (b1[1] - a1[1]) * d2x) / denom
    u = ((b1[0] - a1[0]) * d1y - (b1[1] - a1[1]) * d1x) / denom
    eps = 1e-10
    return eps < t < 1 - eps and eps < u < 1 - eps


def _quad_is_self_intersecting(quad: list[tuple[float, float]]) -> bool:
    """Check if a quadrilateral has crossing diagonals (bowtie shape).

    Tests the two pairs of non-adjacent edges for intersection.
    """
    # Edge 0-1 vs edge 2-3
    if _segments_intersect(quad[0], quad[1], quad[2], quad[3]):
        return True
    # Edge 1-2 vs edge 3-0
    return _segments_intersect(quad[1], quad[2], quad[3], quad[0])


def _classify_edge_orientation(
    p1: tuple[float, float],
    p2: tuple[float, float],
) -> str:
    """Classify a footprint edge as north / south / east / west.

    Uses the outward-facing normal of the edge (right-hand side of
    the CCW travel direction).
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    # Outward normal (right of travel for CCW polygon)
    nx = dy
    ny = -dx
    # Cardinal direction via atan2: angle from +Y measured CW
    angle = math.degrees(math.atan2(nx, ny)) % 360
    if angle < 45 or angle >= 315:
        return "North"
    if 45 <= angle < 135:
        return "East"
    if 135 <= angle < 225:
        return "South"
    return "West"


def _split_core_perimeter_convex(
    footprint: list[tuple[float, float]],
    depth: float,
) -> list[ZoneFootprint]:
    """Split a convex footprint into core + perimeter zones.

    Each footprint edge produces one perimeter zone.  The inward-offset
    polygon becomes the core zone.  If the footprint is too small for the
    requested depth, falls back to a single zone.
    """
    n = len(footprint)
    inner = _inset_polygon_2d(footprint, depth)
    if inner is None:
        return [ZoneFootprint("Whole", footprint)]

    # Count zones per orientation so we can append indices if duplicates arise
    orient_count: dict[str, int] = {}
    zones: list[ZoneFootprint] = []

    for i in range(n):
        j = (i + 1) % n
        outer_p1 = footprint[i]
        outer_p2 = footprint[j]
        inner_p1 = inner[i]
        inner_p2 = inner[j]

        # Perimeter zone: quad from outer edge to inner edge
        perim_poly = [outer_p1, outer_p2, inner_p2, inner_p1]

        # Verify the quad is a valid simple polygon (not a bowtie).
        # When the offset exceeds the apothem, the inner vertices
        # swap and non-adjacent edges of the quad cross each other.
        if _quad_is_self_intersecting(perim_poly):
            return [ZoneFootprint("Whole", footprint)]

        orientation = _classify_edge_orientation(outer_p1, outer_p2)
        orient_count[orientation] = orient_count.get(orientation, 0) + 1
        count = orient_count[orientation]
        suffix = f"Perimeter_{orientation}" if count == 1 else f"Perimeter_{orientation}_{count}"

        zones.append(ZoneFootprint(suffix, perim_poly))

    # Rename first occurrence if there are duplicates
    for orient, cnt in orient_count.items():
        if cnt > 1:
            target = f"Perimeter_{orient}"
            for k, z in enumerate(zones):
                if z.name_suffix == target:
                    zones[k] = ZoneFootprint(f"Perimeter_{orient}_1", z.polygon)
                    break

    zones.append(ZoneFootprint("Core", inner))
    return zones


def _is_convex(footprint: list[tuple[float, float]]) -> bool:
    """Check whether a 2-D polygon is convex."""
    n = len(footprint)
    if n < 3:
        return False
    sign = None
    for i in range(n):
        p0 = footprint[i]
        p1 = footprint[(i + 1) % n]
        p2 = footprint[(i + 2) % n]
        cross = (p1[0] - p0[0]) * (p2[1] - p1[1]) - (p1[1] - p0[1]) * (p2[0] - p1[0])
        if abs(cross) < 1e-10:
            continue
        s = cross > 0
        if sign is None:
            sign = s
        elif s != sign:
            return False
    return True


def _split_core_perimeter(
    footprint: list[tuple[float, float]],
    depth: float,
) -> list[ZoneFootprint]:
    """Split a footprint into core + perimeter zones.

    Handles convex polygons directly.  For concave polygons, falls back
    to a single zone rather than producing invalid geometry.
    """
    if _is_convex(footprint):
        return _split_core_perimeter_convex(footprint, depth)
    # Concave footprint: fall back to single zone
    return [ZoneFootprint("Whole", footprint)]


# ---------------------------------------------------------------------------
# Surface creation internals
# ---------------------------------------------------------------------------


def _make_zone_name(base: str, story: int, num_stories: int, suffix: str) -> str:
    """Build a zone name following DOE prototype conventions.

    Examples:
        >>> _make_zone_name("Office", 1, 3, "Core")
        'Office Story 1 Core'
        >>> _make_zone_name("Office", 1, 1, "Whole")
        'Office'
        >>> _make_zone_name("Office", 1, 1, "Core")
        'Office Core'
    """
    parts: list[str] = [base]
    if num_stories > 1:
        parts.append(f"Story {story}")
    if suffix != "Whole":
        parts.append(suffix)
    return " ".join(parts)


@dataclass
class _StorySpec:
    """Zone layout for a single story."""

    story: int
    z_bot: float
    z_top: float
    zones: list[ZoneFootprint]


def _build_story_surfaces(
    doc: IDFDocument,
    base_name: str,
    spec: _StorySpec,
    num_stories: int,
    *,
    all_story_specs: list[_StorySpec],
    air_boundary: bool,
) -> list[IDFObject]:
    """Create zones and surfaces for one story."""
    svp, clockwise = get_geometry_convention(doc)
    wall_order = WALL_ORDER.get((svp, clockwise), (0, 1, 2, 3))

    created: list[IDFObject] = []
    zone_names_this_story: list[str] = []

    for zf in spec.zones:
        zone_name = _make_zone_name(base_name, spec.story, num_stories, zf.name_suffix)
        zone_names_this_story.append(zone_name)

        # --- Zone ---
        zone = doc.add("Zone", zone_name, validate=False)
        created.append(zone)

        fp = zf.polygon
        n = len(fp)

        # --- Exterior / inter-zone walls ---
        for j in range(n):
            p1 = fp[j]
            p2 = fp[(j + 1) % n]
            wall_name = f"{zone_name} Wall {j + 1}"

            # Determine if this wall edge is shared with another zone on
            # this story by checking if the reversed edge belongs to
            # another zone's polygon.
            adjacent_zone = _find_adjacent_zone(zf, spec.zones, base_name, spec.story, num_stories, p1, p2)

            if adjacent_zone is not None:
                bc = "Surface"
                bc_obj = adjacent_zone
                sun = "NoSun"
                wind = "NoWind"
            else:
                bc = "Outdoors"
                bc_obj = ""
                sun = "SunExposed"
                wind = "WindExposed"

            wall = doc.add(
                "BuildingSurface:Detailed",
                wall_name,
                surface_type="Wall",
                construction_name="",
                zone_name=zone_name,
                outside_boundary_condition=bc,
                outside_boundary_condition_object=bc_obj,
                sun_exposure=sun,
                wind_exposure=wind,
                validate=False,
            )
            corners = [
                Vector3D(p1[0], p1[1], spec.z_top),  # UL
                Vector3D(p1[0], p1[1], spec.z_bot),  # LL
                Vector3D(p2[0], p2[1], spec.z_bot),  # LR
                Vector3D(p2[0], p2[1], spec.z_top),  # UR
            ]
            poly = Polygon3D([corners[k] for k in wall_order])
            set_surface_coords(wall, poly)
            created.append(wall)

        # --- Floor ---
        floor_name = f"{zone_name} Floor"
        if spec.story == 1:
            floor_bc = "Ground"
            floor_bc_obj = ""
        else:
            # Link to the ceiling of the same zone suffix on the story below
            below_spec = all_story_specs[spec.story - 2]
            below_zone = _find_matching_zone_below(zf.name_suffix, below_spec, base_name, num_stories)
            floor_bc = "Surface"
            floor_bc_obj = f"{below_zone} Ceiling"

        floor_srf = doc.add(
            "BuildingSurface:Detailed",
            floor_name,
            surface_type="Floor",
            construction_name="",
            zone_name=zone_name,
            outside_boundary_condition=floor_bc,
            outside_boundary_condition_object=floor_bc_obj,
            sun_exposure="NoSun",
            wind_exposure="NoWind",
            validate=False,
        )
        set_surface_coords(floor_srf, horizontal_poly(fp, spec.z_bot, reverse=not clockwise))
        created.append(floor_srf)

        # --- Ceiling / Roof ---
        is_top = spec.story == num_stories
        if is_top:
            ceil_name = f"{zone_name} Roof"
            ceil_type = "Roof"
            ceil_bc = "Outdoors"
            ceil_bc_obj = ""
            ceil_sun = "SunExposed"
            ceil_wind = "WindExposed"
        else:
            ceil_name = f"{zone_name} Ceiling"
            ceil_type = "Ceiling"
            above_spec = all_story_specs[spec.story]
            above_zone = _find_matching_zone_above(zf.name_suffix, above_spec, base_name, num_stories)
            ceil_bc = "Surface"
            ceil_bc_obj = f"{above_zone} Floor"
            ceil_sun = "NoSun"
            ceil_wind = "NoWind"

        ceil_srf = doc.add(
            "BuildingSurface:Detailed",
            ceil_name,
            surface_type=ceil_type,
            construction_name="",
            zone_name=zone_name,
            outside_boundary_condition=ceil_bc,
            outside_boundary_condition_object=ceil_bc_obj,
            sun_exposure=ceil_sun,
            wind_exposure=ceil_wind,
            validate=False,
        )
        set_surface_coords(ceil_srf, horizontal_poly(fp, spec.z_top, reverse=clockwise))
        created.append(ceil_srf)

    # Optionally apply Construction:AirBoundary to inter-zone walls
    if air_boundary:
        _apply_air_boundaries(doc, created)

    return created


def _find_matching_zone_below(
    suffix: str,
    below_spec: _StorySpec,
    base_name: str,
    num_stories: int,
) -> str:
    """Find the zone name on the story below that matches *suffix*."""
    # Try exact suffix match first
    for zf in below_spec.zones:
        if zf.name_suffix == suffix:
            return _make_zone_name(base_name, below_spec.story, num_stories, zf.name_suffix)
    # Fallback: if zoning changed between stories, use the first zone
    return _make_zone_name(base_name, below_spec.story, num_stories, below_spec.zones[0].name_suffix)


def _find_matching_zone_above(
    suffix: str,
    above_spec: _StorySpec,
    base_name: str,
    num_stories: int,
) -> str:
    """Find the zone name on the story above that matches *suffix*."""
    for zf in above_spec.zones:
        if zf.name_suffix == suffix:
            return _make_zone_name(base_name, above_spec.story, num_stories, zf.name_suffix)
    return _make_zone_name(base_name, above_spec.story, num_stories, above_spec.zones[0].name_suffix)


def _edge_key(p1: tuple[float, float], p2: tuple[float, float]) -> tuple[float, float, float, float]:
    """Canonical key for an edge (rounded to avoid float issues)."""
    return (round(p1[0], 8), round(p1[1], 8), round(p2[0], 8), round(p2[1], 8))


def _find_adjacent_zone(
    current: ZoneFootprint,
    all_zones: list[ZoneFootprint],
    base_name: str,
    story: int,
    num_stories: int,
    p1: tuple[float, float],
    p2: tuple[float, float],
) -> str | None:
    """Check if the reversed edge (p2→p1) belongs to another zone polygon.

    Returns the wall surface name of the adjacent zone's matching wall,
    or ``None`` if the edge is exterior.
    """
    key_reversed = _edge_key(p2, p1)
    for zf in all_zones:
        if zf is current:
            continue
        other_fp = zf.polygon
        n = len(other_fp)
        for j in range(n):
            ep1 = other_fp[j]
            ep2 = other_fp[(j + 1) % n]
            if _edge_key(ep1, ep2) == key_reversed:
                other_zone_name = _make_zone_name(base_name, story, num_stories, zf.name_suffix)
                return f"{other_zone_name} Wall {j + 1}"
    return None


def _apply_air_boundaries(doc: IDFDocument, created: list[IDFObject]) -> None:
    """Set ``Construction:AirBoundary`` on inter-zone walls.

    Creates a single ``Construction:AirBoundary`` object if one doesn't
    already exist, then assigns it to all ``Surface``-boundary walls.
    """
    air_name = "Air Boundary"
    if not list(doc["Construction:AirBoundary"]):
        doc.add("Construction:AirBoundary", air_name, validate=False)

    for obj in created:
        if obj.obj_type != "BuildingSurface:Detailed":
            continue
        st = getattr(obj, "surface_type", None) or ""
        bc = getattr(obj, "outside_boundary_condition", None) or ""
        if st.upper() == "WALL" and bc.upper() == "SURFACE":
            obj.construction_name = air_name


# ---------------------------------------------------------------------------
# ZonedBlock dataclass (describe-then-apply)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ZonedBlock:
    """Describes a building block with a zoning strategy.

    This is a pure data object.  Call `build()` to realise the
    geometry in an [IDFDocument][idfkit.document.IDFDocument].

    Attributes:
        name: Base name for zones and surfaces.
        footprint: 2-D footprint as ``(x, y)`` tuples (CCW).
        floor_to_floor: Floor-to-floor height in metres.
        num_stories: Number of above-ground stories.
        zoning: Zoning strategy.
        perimeter_depth: Perimeter zone depth (metres), used only
            when ``zoning`` is ``CORE_PERIMETER``.
        custom_zones: Per-floor named zone polygons, used only when
            ``zoning`` is ``CUSTOM``.
        air_boundary: Whether to use ``Construction:AirBoundary``
            between inter-zone walls.
    """

    name: str
    footprint: Sequence[tuple[float, float]]
    floor_to_floor: float
    num_stories: int = 1
    zoning: ZoningScheme = ZoningScheme.BY_STOREY
    perimeter_depth: float = ASHRAE_PERIMETER_DEPTH
    custom_zones: list[ZoneFootprint] | None = None
    air_boundary: bool = False

    def __post_init__(self) -> None:
        if len(self.footprint) < 3:
            msg = f"Footprint must have at least 3 vertices, got {len(self.footprint)}"
            raise ValueError(msg)
        if self.floor_to_floor <= 0:
            msg = f"floor_to_floor must be positive, got {self.floor_to_floor}"
            raise ValueError(msg)
        if self.num_stories < 1:
            msg = f"num_stories must be >= 1, got {self.num_stories}"
            raise ValueError(msg)
        if self.perimeter_depth <= 0:
            msg = f"perimeter_depth must be positive, got {self.perimeter_depth}"
            raise ValueError(msg)
        if self.zoning == ZoningScheme.CUSTOM and not self.custom_zones:
            msg = "custom_zones is required when zoning is CUSTOM"
            raise ValueError(msg)

    @property
    def height(self) -> float:
        """Total building height in metres."""
        return self.floor_to_floor * self.num_stories

    @property
    def floor_area(self) -> float:
        """Single-floor footprint area in square metres."""
        return abs(_polygon_area_signed(list(self.footprint)))

    @property
    def total_floor_area(self) -> float:
        """Total floor area across all stories in square metres."""
        return self.floor_area * self.num_stories

    def build(self, doc: IDFDocument) -> list[IDFObject]:
        """Realise the zoned geometry in the document.

        Returns:
            All created [IDFObject][idfkit.objects.IDFObject] instances.
        """
        fp = list(self.footprint)

        # Determine zone layout per floor
        if self.zoning == ZoningScheme.CORE_PERIMETER:
            zone_footprints = _split_core_perimeter(fp, self.perimeter_depth)
        elif self.zoning == ZoningScheme.CUSTOM:
            zone_footprints = self.custom_zones or [ZoneFootprint("Whole", fp)]
        else:  # BY_STOREY
            zone_footprints = [ZoneFootprint("Whole", fp)]

        # Build story specs
        story_specs: list[_StorySpec] = []
        for i in range(self.num_stories):
            z_bot = i * self.floor_to_floor
            z_top = (i + 1) * self.floor_to_floor
            story_specs.append(_StorySpec(i + 1, z_bot, z_top, zone_footprints))

        # Create surfaces for each story
        created: list[IDFObject] = []
        for spec in story_specs:
            created.extend(
                _build_story_surfaces(
                    doc,
                    self.name,
                    spec,
                    self.num_stories,
                    all_story_specs=story_specs,
                    air_boundary=self.air_boundary,
                )
            )
        return created


# ---------------------------------------------------------------------------
# create_building — high-level entry point
# ---------------------------------------------------------------------------


def create_building(
    doc: IDFDocument,
    name: str,
    footprint: Sequence[tuple[float, float]],
    floor_to_floor: float,
    num_stories: int = 1,
    *,
    zoning: ZoningScheme = ZoningScheme.BY_STOREY,
    perimeter_depth: float = ASHRAE_PERIMETER_DEPTH,
    custom_zones: list[ZoneFootprint] | None = None,
    air_boundary: bool = False,
) -> list[IDFObject]:
    """Create a fully-zoned building in one call.

    This is the primary entry point for the zoning module.  It combines
    footprint definition, zoning strategy, and multi-story extrusion into
    a single function call.

    Args:
        doc: The document to add objects to.
        name: Base name for zones and surfaces (e.g. ``"Office"``).
        footprint: 2-D footprint as ``(x, y)`` tuples (CCW order).
        floor_to_floor: Floor-to-floor height in metres.
        num_stories: Number of above-ground stories.
        zoning: Zoning strategy (default: one zone per floor).
        perimeter_depth: Depth of perimeter zones in metres.
            Only used when ``zoning`` is ``CORE_PERIMETER``.
            Defaults to 4.57 m (ASHRAE 90.1 / DOE prototypes).
        custom_zones: Named zone polygons, required when ``zoning``
            is ``CUSTOM``.
        air_boundary: If ``True``, apply ``Construction:AirBoundary``
            to all inter-zone walls (for open-plan spaces).

    Returns:
        All created [IDFObject][idfkit.objects.IDFObject] instances.

    Examples:
        Core-perimeter zoning for a 3-story office:

            ```python
            from idfkit import new_document
            from idfkit.zoning import (
                ZoningScheme,
                create_building,
                footprint_rectangle,
            )

            doc = new_document()
            create_building(
                doc,
                name="Office",
                footprint=footprint_rectangle(50, 30),
                floor_to_floor=3.5,
                num_stories=3,
                zoning=ZoningScheme.CORE_PERIMETER,
            )
            ```
    """
    block = ZonedBlock(
        name=name,
        footprint=footprint,
        floor_to_floor=floor_to_floor,
        num_stories=num_stories,
        zoning=zoning,
        perimeter_depth=perimeter_depth,
        custom_zones=custom_zones,
        air_boundary=air_boundary,
    )
    return block.build(doc)
