"""High-level geometry construction functions.

Provides building-block primitives for creating EnergyPlus zone and surface
geometry from simple 2D footprints.  The :class:`Shoebox` dataclass describes
a rectangular building; call :meth:`Shoebox.build` to realise it in a
document.  For arbitrary polygon footprints, use :func:`add_block` directly.

These functions complement the lower-level :mod:`~idfkit.geometry` module
which operates on *existing* surfaces.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
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
# Shoebox (describe-then-apply pattern)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Shoebox:
    """A rectangular building block described by width, depth, and stories.

    This is a pure data object — it does **not** modify any document.  Call
    :meth:`build` to realise the geometry in an :class:`~idfkit.document.IDFDocument`.

    Attributes:
        name: Base name for zones and surfaces.
        width: Building width in metres (along X axis).
        depth: Building depth in metres (along Y axis).
        floor_to_floor: Floor-to-floor height in metres.
        num_stories: Number of above-ground stories (default 1).
        origin: ``(x, y)`` position of the lower-left corner (default ``(0, 0)``).
    """

    name: str
    width: float
    depth: float
    floor_to_floor: float
    num_stories: int = 1
    origin: tuple[float, float] = (0.0, 0.0)

    def __post_init__(self) -> None:
        if self.width <= 0:
            msg = f"width must be positive, got {self.width}"
            raise ValueError(msg)
        if self.depth <= 0:
            msg = f"depth must be positive, got {self.depth}"
            raise ValueError(msg)
        if self.floor_to_floor <= 0:
            msg = f"floor_to_floor must be positive, got {self.floor_to_floor}"
            raise ValueError(msg)
        if self.num_stories < 1:
            msg = f"num_stories must be >= 1, got {self.num_stories}"
            raise ValueError(msg)

    @property
    def footprint(self) -> list[tuple[float, float]]:
        """The rectangular footprint as 4 counter-clockwise ``(x, y)`` tuples."""
        x, y = self.origin
        return [
            (x, y),
            (x + self.width, y),
            (x + self.width, y + self.depth),
            (x, y + self.depth),
        ]

    @property
    def height(self) -> float:
        """Total building height."""
        return self.floor_to_floor * self.num_stories

    @property
    def floor_area(self) -> float:
        """Single-floor area (width * depth)."""
        return self.width * self.depth

    @property
    def total_floor_area(self) -> float:
        """Total floor area across all stories."""
        return self.floor_area * self.num_stories

    def build(self, doc: IDFDocument) -> list[IDFObject]:
        """Realise this shoebox geometry in the document.

        Creates zones, walls, floors, and ceiling/roof surfaces.
        Inter-story floors/ceilings are matched with ``Surface`` boundary
        conditions.

        Returns:
            All created :class:`~idfkit.objects.IDFObject` instances
            (zones + surfaces).
        """
        return _build_block(doc, self.name, self.footprint, self.floor_to_floor, self.num_stories)


# ---------------------------------------------------------------------------
# add_block / add_shading_block (general-purpose)
# ---------------------------------------------------------------------------


def add_block(
    doc: IDFDocument,
    name: str,
    footprint: Sequence[tuple[float, float]],
    floor_to_floor: float,
    num_stories: int = 1,
) -> list[IDFObject]:
    """Create zones and surfaces from an arbitrary 2D footprint.

    For each story, creates a ``Zone`` and ``BuildingSurface:Detailed``
    objects for walls (one per footprint edge), a floor, and a
    ceiling/roof.

    This is the general-purpose alternative to :class:`Shoebox` for
    non-rectangular footprints.

    Args:
        doc: The document to add objects to.
        name: Base name for zones and surfaces.
        footprint: 2D footprint as ``(x, y)`` tuples.
            Vertices should be in counter-clockwise order when viewed
            from above.
        floor_to_floor: Floor-to-floor height in metres.
        num_stories: Number of stories (default 1).

    Returns:
        All created IDFObject instances (zones + surfaces).

    Raises:
        ValueError: If footprint has fewer than 3 vertices, height <= 0,
            or num_stories < 1.
    """
    return _build_block(doc, name, list(footprint), floor_to_floor, num_stories)


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

    z_bot = base_z
    z_top = base_z + height
    created: list[IDFObject] = []
    n = len(fp)

    # Walls
    for j in range(n):
        p1 = fp[j]
        p2 = fp[(j + 1) % n]
        wall_name = f"{name} Wall {j + 1}"
        poly = Polygon3D([
            Vector3D(p1[0], p1[1], z_top),
            Vector3D(p1[0], p1[1], z_bot),
            Vector3D(p2[0], p2[1], z_bot),
            Vector3D(p2[0], p2[1], z_top),
        ])
        obj = doc.add("Shading:Site:Detailed", wall_name, validate=False)
        set_surface_coords(obj, poly)
        created.append(obj)

    # Top cap — footprint at z_top (normal up: CCW viewed from above)
    cap_name = f"{name} Top"
    cap_poly = Polygon3D([Vector3D(p[0], p[1], z_top) for p in fp])
    cap = doc.add("Shading:Site:Detailed", cap_name, validate=False)
    set_surface_coords(cap, cap_poly)
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

    .. note::

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
# _build_block — shared implementation for Shoebox.build() and add_block()
# ---------------------------------------------------------------------------


def _build_block(
    doc: IDFDocument,
    name: str,
    footprint: list[tuple[float, float]],
    floor_to_floor: float,
    num_stories: int,
) -> list[IDFObject]:
    """Create zones and surfaces from a footprint (internal helper)."""
    if len(footprint) < 3:
        msg = f"Footprint must have at least 3 vertices, got {len(footprint)}"
        raise ValueError(msg)
    if floor_to_floor <= 0:
        msg = f"floor_to_floor must be positive, got {floor_to_floor}"
        raise ValueError(msg)
    if num_stories < 1:
        msg = f"num_stories must be >= 1, got {num_stories}"
        raise ValueError(msg)

    created: list[IDFObject] = []
    n = len(footprint)

    # Pre-compute zone names so we can set up inter-story references.
    zone_names: list[str] = []
    for i in range(num_stories):
        zone_names.append(f"{name} Story {i + 1}" if num_stories > 1 else name)

    for i in range(num_stories):
        z_bot = i * floor_to_floor
        z_top = (i + 1) * floor_to_floor
        zone_name = zone_names[i]

        # --- Zone ---
        zone = doc.add("Zone", zone_name, validate=False)
        created.append(zone)

        # --- Walls (one per footprint edge) ---
        for j in range(n):
            p1 = footprint[j]
            p2 = footprint[(j + 1) % n]
            wall_name = f"{zone_name} Wall {j + 1}"
            # Upper-left-first convention: outward-facing normal for CCW footprint
            wall = doc.add(
                "BuildingSurface:Detailed",
                wall_name,
                surface_type="Wall",
                construction_name="",
                zone_name=zone_name,
                outside_boundary_condition="Outdoors",
                sun_exposure="SunExposed",
                wind_exposure="WindExposed",
                validate=False,
            )
            poly = Polygon3D([
                Vector3D(p1[0], p1[1], z_top),
                Vector3D(p1[0], p1[1], z_bot),
                Vector3D(p2[0], p2[1], z_bot),
                Vector3D(p2[0], p2[1], z_top),
            ])
            set_surface_coords(wall, poly)
            created.append(wall)

        # --- Floor ---
        floor_name = f"{zone_name} Floor"
        if i == 0:
            floor_bc = "Ground"
            floor_bc_obj = ""
        else:
            floor_bc = "Surface"
            floor_bc_obj = f"{zone_names[i - 1]} Ceiling"

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
        # Floor normal should point down → reverse vertex order
        floor_poly = Polygon3D([Vector3D(p[0], p[1], z_bot) for p in reversed(footprint)])
        set_surface_coords(floor_srf, floor_poly)
        created.append(floor_srf)

        # --- Ceiling / Roof ---
        is_top = i == num_stories - 1
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
            ceil_bc = "Surface"
            ceil_bc_obj = f"{zone_names[i + 1]} Floor"
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
        # Ceiling/roof normal should point up → footprint order (CCW from above)
        ceil_poly = Polygon3D([Vector3D(p[0], p[1], z_top) for p in footprint])
        set_surface_coords(ceil_srf, ceil_poly)
        created.append(ceil_srf)

    return created
