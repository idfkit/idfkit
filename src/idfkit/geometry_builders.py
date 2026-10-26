"""Geometry utility functions for EnergyPlus surface manipulation.

Provides shading block creation, default construction assignment, bounding
box queries, building scaling, horizontal adjacency detection, surface
splitting, and ``GlobalGeometryRules`` vertex-ordering helpers.

For building zone and surface creation, see [zoning][idfkit.zoning] which
provides [create_block][idfkit.zoning.create_block] and
[ZonedBlock][idfkit.zoning.ZonedBlock].
"""

from __future__ import annotations

import logging
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .geometry import (
    VERTEX_SURFACE_TYPES,
    Polygon3D,
    Vector3D,
    get_surface_coords,
    polygon_area_2d,
    polygon_difference_parts_2d,
    polygon_intersection_2d,
    set_surface_coords,
)

if TYPE_CHECKING:
    from .document import IDFDocument
    from .objects import IDFObject

    _SurfacesByZ = dict[float, list[tuple[IDFObject, list[tuple[float, float]]]]]

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# GlobalGeometryRules helpers
# ---------------------------------------------------------------------------

# Wall corner indices in canonical order [UL, LL, LR, UR].
# The tuple gives the output index order for each
# (starting_vertex_position, clockwise) combination.
WALL_ORDER: dict[tuple[str, bool], tuple[int, int, int, int]] = {
    # Counterclockwise ---------------------------------------------------
    ("UpperLeftCorner", False): (0, 1, 2, 3),  # UL LL LR UR
    ("LowerLeftCorner", False): (1, 2, 3, 0),  # LL LR UR UL
    ("LowerRightCorner", False): (2, 3, 0, 1),  # LR UR UL LL
    ("UpperRightCorner", False): (3, 0, 1, 2),  # UR UL LL LR
    # Clockwise ----------------------------------------------------------
    ("UpperLeftCorner", True): (0, 3, 2, 1),  # UL UR LR LL
    ("UpperRightCorner", True): (3, 2, 1, 0),  # UR LR LL UL
    ("LowerRightCorner", True): (2, 1, 0, 3),  # LR LL UL UR
    ("LowerLeftCorner", True): (1, 0, 3, 2),  # LL UL UR LR
}


def get_geometry_convention(doc: IDFDocument) -> tuple[str, bool]:
    """Read the vertex ordering convention from ``GlobalGeometryRules``.

    Returns:
        ``(starting_vertex_position, clockwise)`` where *clockwise* is
        ``True`` when ``vertex_entry_direction`` is ``"Clockwise"``.
        Defaults to ``("UpperLeftCorner", False)`` if no rules exist.
    """
    geo_rules = doc["GlobalGeometryRules"]
    if not geo_rules:
        return ("UpperLeftCorner", False)
    rules = geo_rules.first()
    if rules is None:
        return ("UpperLeftCorner", False)
    svp = getattr(rules, "starting_vertex_position", None) or "UpperLeftCorner"
    ved = getattr(rules, "vertex_entry_direction", None) or "Counterclockwise"
    return (str(svp), str(ved).lower() == "clockwise")


# ---------------------------------------------------------------------------
# add_shading_block
# ---------------------------------------------------------------------------


def add_shading_block(
    doc: IDFDocument,
    name: str,
    footprint: Sequence[tuple[float, float]],
    height: float,
    base_z: float = 0.0,
) -> list[IDFObject]:
    """Create ``Shading:Site:Detailed`` surfaces from a 2D footprint.

    Creates one shading surface per footprint edge (walls) plus a
    horizontal top cap.  No zones or thermal surfaces are created.

    Args:
        doc: The document to add objects to.
        name: Base name for shading surfaces.
        footprint: 2D footprint as ``(x, y)`` tuples (counter-clockwise).
        height: Height of the shading block in metres.
        base_z: Z-coordinate of the block base (default ``0.0``).
            Use this to create elevated shading surfaces such as canopies.

    Returns:
        List of created ``Shading:Site:Detailed`` objects.

    Raises:
        ValueError: If footprint has fewer than 3 vertices or height <= 0.
    """
    fp = list(footprint)
    if len(fp) < 3:
        msg = f"Footprint must have at least 3 vertices, got {len(fp)}"
        raise ValueError(msg)
    if height <= 0:
        msg = f"Height must be positive, got {height}"
        raise ValueError(msg)

    svp, clockwise = get_geometry_convention(doc)
    wall_order = WALL_ORDER.get((svp, clockwise), (0, 1, 2, 3))

    z_bot = base_z
    z_top = base_z + height
    created: list[IDFObject] = []
    n = len(fp)

    # Walls
    for j in range(n):
        p1 = fp[j]
        p2 = fp[(j + 1) % n]
        wall_name = f"{name} Wall {j + 1}"
        corners = [
            Vector3D(p1[0], p1[1], z_top),  # UL
            Vector3D(p1[0], p1[1], z_bot),  # LL
            Vector3D(p2[0], p2[1], z_bot),  # LR
            Vector3D(p2[0], p2[1], z_top),  # UR
        ]
        poly = Polygon3D([corners[k] for k in wall_order])
        obj = doc.add("Shading:Site:Detailed", wall_name, validate=False)
        set_surface_coords(obj, poly)
        created.append(obj)

    # Top cap — horizontal surface with normal pointing up
    cap_name = f"{name} Top"
    cap = doc.add("Shading:Site:Detailed", cap_name, validate=False)
    set_surface_coords(cap, horizontal_poly(fp, z_top, reverse=clockwise))
    created.append(cap)

    return created


# ---------------------------------------------------------------------------
# set_default_constructions / bounding_box / scale_building
# ---------------------------------------------------------------------------


def set_default_constructions(doc: IDFDocument, construction_name: str = "Default Construction") -> int:
    """Assign a placeholder construction to surfaces that lack one.

    Iterates all ``BuildingSurface:Detailed`` and
    ``FenestrationSurface:Detailed`` objects and sets
    ``construction_name`` for any whose current value is empty or ``None``.

    Does **not** create the ``Construction`` object itself — the caller
    is responsible for ensuring it exists.

    Args:
        doc: The document to modify.
        construction_name: Name of the construction to assign.

    Returns:
        Number of surfaces updated.
    """
    count = 0
    for stype in ("BuildingSurface:Detailed", "FenestrationSurface:Detailed"):
        for srf in doc.get_collection(stype):
            if not srf.get("Construction Name"):
                srf.construction_name = construction_name
                count += 1
    return count


def bounding_box(doc: IDFDocument) -> tuple[tuple[float, float], tuple[float, float]] | None:
    """Return the 2D axis-aligned bounding box of all building surfaces.

    Scans all ``BuildingSurface:Detailed`` vertices and returns the
    bounding envelope projected onto the XY plane.

    !!! note
        Only ``BuildingSurface:Detailed`` objects are considered.
        Fenestration and shading surfaces are excluded because they
        are either coplanar with (windows) or outside (shading) the
        thermal envelope.

    Returns:
        ``((min_x, min_y), (max_x, max_y))`` or ``None`` if no
        surfaces with valid coordinates exist.
    """
    min_x = float("inf")
    min_y = float("inf")
    max_x = float("-inf")
    max_y = float("-inf")
    found = False

    for srf in doc["BuildingSurface:Detailed"]:
        coords = get_surface_coords(srf)
        if coords is None:
            continue
        for v in coords.vertices:
            min_x = min(min_x, v.x)
            min_y = min(min_y, v.y)
            max_x = max(max_x, v.x)
            max_y = max(max_y, v.y)
            found = True

    if not found:
        return None
    return ((min_x, min_y), (max_x, max_y))


def scale_building(
    doc: IDFDocument,
    factor: float | tuple[float, float, float],
    anchor: Vector3D | None = None,
) -> None:
    """Scale all surface vertices around an anchor point.

    Args:
        doc: The document to modify in-place.
        factor: Scale factor.  A single ``float`` applies uniform scaling;
            a ``(fx, fy, fz)`` tuple scales each axis independently
            (e.g. ``(2.0, 1.0, 1.0)`` doubles X only).
        anchor: Point to scale around.  If ``None``, the origin
            ``(0, 0, 0)`` is used.
    """
    if isinstance(factor, tuple):
        fx, fy, fz = factor
    else:
        fx = fy = fz = factor

    ax, ay, az = (anchor.x, anchor.y, anchor.z) if anchor else (0.0, 0.0, 0.0)

    for stype in VERTEX_SURFACE_TYPES:
        for srf in doc.get_collection(stype):
            coords = get_surface_coords(srf)
            if coords is None:
                continue
            new_vertices = [
                Vector3D(
                    ax + (v.x - ax) * fx,
                    ay + (v.y - ay) * fy,
                    az + (v.z - az) * fz,
                )
                for v in coords.vertices
            ]
            set_surface_coords(srf, Polygon3D(new_vertices))


# ---------------------------------------------------------------------------
# Horizontal polygon helper
# ---------------------------------------------------------------------------


def horizontal_poly(footprint: list[tuple[float, float]], z: float, *, reverse: bool) -> Polygon3D:
    """Build a horizontal polygon at height *z*.

    When *reverse* is ``True`` the footprint is reversed, flipping the
    polygon normal.  Used to produce floor and ceiling polygons in the
    correct winding for the active ``GlobalGeometryRules`` convention.
    """
    pts = reversed(footprint) if reverse else footprint
    return Polygon3D([Vector3D(p[0], p[1], z) for p in pts])


# ---------------------------------------------------------------------------
# Horizontal surface adjacency detection and linking
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class HorizontalAdjacency:
    """A detected adjacency between a roof and floor surface at the same elevation.

    Attributes:
        roof_surface: The roof surface from the lower block.
        floor_surface: The floor surface from the upper block.
        z: The shared elevation in metres.
        intersection: 2-D polygon of the overlapping area.
        intersection_area: Area of the overlap in square metres.
    """

    roof_surface: IDFObject
    floor_surface: IDFObject
    z: float
    intersection: list[tuple[float, float]]
    intersection_area: float


_HORIZONTAL_Z_TOL = 0.01  # metres


def _extract_horizontal_footprint(
    surface: IDFObject,
) -> tuple[float, list[tuple[float, float]]] | None:
    """Extract the z-elevation and 2-D footprint from a horizontal surface.

    Returns ``(z, footprint_2d)`` or ``None`` if the surface has no
    coordinates or is not horizontal (z-spread > tolerance).
    """
    coords = get_surface_coords(surface)
    if coords is None:
        return None
    z_values = [v.z for v in coords.vertices]
    z_min = min(z_values)
    z_max = max(z_values)
    if z_max - z_min > _HORIZONTAL_Z_TOL:
        return None
    z = z_values[0]
    fp = [(v.x, v.y) for v in coords.vertices]
    # Normalise to CCW winding so polygon_intersection_2d works correctly.
    if polygon_area_2d(fp) < 0:
        fp.reverse()
    return z, fp


def _collect_outdoor_horizontal_surfaces(
    doc: IDFDocument,
) -> tuple[_SurfacesByZ, _SurfacesByZ]:
    """Partition ``Outdoors``-BC horizontal surfaces into roofs and floors by z."""
    roofs: _SurfacesByZ = {}
    floors: _SurfacesByZ = {}
    for srf in doc["BuildingSurface:Detailed"]:
        st = (getattr(srf, "surface_type", "") or "").upper()
        bc = (getattr(srf, "outside_boundary_condition", "") or "").upper()
        if bc != "OUTDOORS":
            continue
        result = _extract_horizontal_footprint(srf)
        if result is None:
            continue
        z, fp = result
        z_key = round(z, 4)
        if st == "ROOF":
            roofs.setdefault(z_key, []).append((srf, fp))
        elif st == "FLOOR":
            floors.setdefault(z_key, []).append((srf, fp))
    return roofs, floors


def detect_horizontal_adjacencies(
    doc: IDFDocument,
) -> list[HorizontalAdjacency]:
    """Find roof/floor surface pairs at matching elevations.

    Scans all ``BuildingSurface:Detailed`` surfaces for horizontal Roof
    surfaces with ``Outdoors`` boundary condition and horizontal Floor
    surfaces with ``Outdoors`` boundary condition at the same elevation.

    For each overlapping pair the 2-D polygon intersection is computed.

    Args:
        doc: The document to scan.

    Returns:
        List of :class:`HorizontalAdjacency` records for each detected
        overlap.
    """
    roofs, floors = _collect_outdoor_horizontal_surfaces(doc)

    adjacencies: list[HorizontalAdjacency] = []
    for z_key, roof_list in roofs.items():
        floor_list = floors.get(z_key)
        if floor_list is None:
            continue
        for roof_srf, roof_fp in roof_list:
            for floor_srf, floor_fp in floor_list:
                inter = polygon_intersection_2d(roof_fp, floor_fp)
                if inter is None:
                    continue
                area = abs(polygon_area_2d(inter))
                if area < 0.01:
                    continue
                adjacencies.append(
                    HorizontalAdjacency(
                        roof_surface=roof_srf,
                        floor_surface=floor_srf,
                        z=z_key,
                        intersection=inter,
                        intersection_area=area,
                    )
                )
    return adjacencies


def _add_horizontal_like(
    doc: IDFDocument,
    template: IDFObject,
    base_name: str,
    footprint: list[tuple[float, float]],
    z: float,
    *,
    reverse: bool,
) -> IDFObject:
    """Add a surface copying *template*'s attributes with a new footprint and a unique name."""
    name = base_name
    counter = 1
    while doc.getobject("BuildingSurface:Detailed", name) is not None:
        counter += 1
        name = f"{base_name} {counter}"
    srf = doc.add(
        "BuildingSurface:Detailed",
        name,
        surface_type=getattr(template, "surface_type", "") or "",
        construction_name=getattr(template, "construction_name", "") or "",
        zone_name=getattr(template, "zone_name", "") or "",
        outside_boundary_condition=getattr(template, "outside_boundary_condition", "") or "",
        outside_boundary_condition_object=getattr(template, "outside_boundary_condition_object", "") or "",
        sun_exposure=getattr(template, "sun_exposure", "") or "",
        wind_exposure=getattr(template, "wind_exposure", "") or "",
        validate=False,
    )
    set_surface_coords(srf, horizontal_poly(footprint, z, reverse=reverse))
    return srf


def split_horizontal_surface_by_regions(
    doc: IDFDocument,
    surface: IDFObject,
    regions: Sequence[Sequence[tuple[float, float]]],
) -> tuple[list[IDFObject], list[IDFObject]]:
    """Split a horizontal surface under several non-overlapping 2-D regions at once.

    One new surface is created per region, covering the part of the
    surface inside that region.  The rest of the surface (the surface
    minus all regions together) is computed with
    [polygon_difference_parts_2d][idfkit.geometry.polygon_difference_parts_2d],
    so it is always EnergyPlus-safe: no holes and no zero-width slits.  The
    original surface takes the largest remaining piece.  When more pieces
    remain, for example around a region sitting in the middle of the
    surface, each extra piece becomes a new surface named
    ``"<surface name> Remainder"`` (numbered when that name is taken) that
    copies the original's construction, zone, and boundary conditions.

    Splitting under every region in one call matters when the regions are
    adjacent, such as the floors of a core-and-perimeter tower standing on
    a podium roof.  Their union is subtracted in one step, so the remainder
    is cut only where it has to be.

    Args:
        doc: The document containing the surface.
        surface: Horizontal surface to split (floor, ceiling, or roof).
        regions: 2-D polygons to split at.  Each must overlap the surface
            and be convex or have a convex overlap with it.

    Returns:
        ``(region_surfaces, remaining_surfaces)``.  *region_surfaces*
        holds one surface per region, in order.  *remaining_surfaces*
        starts with the original surface, followed by any extra remainder
        pieces.  It is empty when the regions cover the whole surface; the
        original surface is then left unchanged.

    Raises:
        ValueError: If the surface has no coordinates or a region does not
            overlap it.
    """
    result = _extract_horizontal_footprint(surface)
    if result is None:
        msg = f"Surface '{surface.name}' has no coordinates"
        raise ValueError(msg)
    z, footprint = result
    _, clockwise = get_geometry_convention(doc)

    inters: list[list[tuple[float, float]]] = []
    for region in regions:
        inter = polygon_intersection_2d(footprint, list(region))
        if inter is None:
            msg = f"Region does not overlap surface '{surface.name}'"
            raise ValueError(msg)
        inters.append(inter)

    # Determine surface type for winding
    st = (getattr(surface, "surface_type", "") or "").upper()
    # For roofs/ceilings, winding is clockwise; for floors, not clockwise
    reverse = clockwise if st in ("ROOF", "CEILING") else not clockwise

    region_surfaces = [
        _add_horizontal_like(doc, surface, f"{surface.name} Split", inter, z, reverse=reverse) for inter in inters
    ]

    pieces = [p for p in polygon_difference_parts_2d(footprint, *inters) if abs(polygon_area_2d(p)) >= 0.01]
    if not pieces:
        return region_surfaces, []

    # Update original surface geometry to the largest remaining piece
    set_surface_coords(surface, horizontal_poly(pieces[0], z, reverse=reverse))
    remaining = [surface]
    remaining.extend(
        _add_horizontal_like(doc, surface, f"{surface.name} Remainder", piece, z, reverse=reverse)
        for piece in pieces[1:]
    )
    return region_surfaces, remaining


def split_horizontal_surface(
    doc: IDFDocument,
    surface: IDFObject,
    region: Sequence[tuple[float, float]],
) -> tuple[IDFObject, IDFObject | None]:
    """Split a horizontal surface at a 2-D region boundary.

    A new surface is created for the area *inside* the region.  The
    original surface is shrunk to the area *outside* the region.

    When the region sits strictly inside the surface, the outside area is
    a frame with a hole, which no single EnergyPlus surface can describe.
    The frame is then cut into hole-free pieces: the original surface
    keeps the largest, and each other piece is added to *doc* as a new
    surface named ``"<surface name> Remainder"`` (numbered when that name
    is taken).  Use
    [split_horizontal_surface_by_regions][idfkit.geometry_builders.split_horizontal_surface_by_regions]
    to get those extra surfaces back, or to split under several regions
    at once.

    Args:
        doc: The document containing the surface.
        surface: Horizontal surface to split (floor, ceiling, or roof).
        region: 2-D polygon defining the split region.

    Returns:
        ``(new_region_surface, remaining_surface)``.
        *remaining_surface* is ``None`` if the region covers the entire
        surface (i.e. no remaining area).
    """
    region_surfaces, remaining = split_horizontal_surface_by_regions(doc, surface, [region])
    return region_surfaces[0], (remaining[0] if remaining else None)


def link_horizontal_surfaces(ceiling: IDFObject, floor: IDFObject) -> None:
    """Set mutual ``Surface`` boundary conditions between ceiling and floor.

    Modifies both surfaces in-place:

    * The ceiling's ``surface_type`` is set to ``Ceiling``.
    * Both surfaces get ``outside_boundary_condition = "Surface"``
      pointing at each other, with sun/wind exposure set to ``NoSun``
      / ``NoWind``.

    Args:
        ceiling: The surface to designate as the ceiling.
        floor: The surface to designate as the floor.
    """
    ceiling.surface_type = "Ceiling"
    ceiling.outside_boundary_condition = "Surface"
    ceiling.outside_boundary_condition_object = floor.name
    ceiling.sun_exposure = "NoSun"
    ceiling.wind_exposure = "NoWind"

    floor.outside_boundary_condition = "Surface"
    floor.outside_boundary_condition_object = ceiling.name
    floor.sun_exposure = "NoSun"
    floor.wind_exposure = "NoWind"
