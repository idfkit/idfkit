"""Geometry utility functions for EnergyPlus surface manipulation.

Provides shading block creation, default construction assignment, bounding
box queries, building scaling, and ``GlobalGeometryRules`` vertex-ordering
helpers.

For building zone and surface creation, see [zoning][idfkit.zoning] which
provides [create_building][idfkit.zoning.create_building] and
[ZonedBlock][idfkit.zoning.ZonedBlock].
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from .geometry import (
    VERTEX_SURFACE_TYPES,
    Polygon3D,
    Vector3D,
    get_surface_coords,
    set_surface_coords,
)

if TYPE_CHECKING:
    from .document import IDFDocument
    from .objects import IDFObject

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
        for srf in doc[stype]:
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
        for srf in doc[stype]:
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
