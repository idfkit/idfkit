"""
Geometry utilities for IDF models.

Provides coordinate handling and transformations without geomeppy dependency.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .document import IDFDocument
    from .objects import IDFObject


@dataclass(frozen=True, slots=True)
class Vector3D:
    """
    Immutable 3D vector.

    Example:
        >>> v = Vector3D(1.0, 2.0, 3.0)
        >>> v2 = v + Vector3D(1, 0, 0)
        >>> print(v2)
        Vector3D(2.0, 2.0, 3.0)
    """

    x: float
    y: float
    z: float

    def __add__(self, other: Vector3D) -> Vector3D:
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector3D) -> Vector3D:
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> Vector3D:
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar: float) -> Vector3D:
        return self * scalar

    def __truediv__(self, scalar: float) -> Vector3D:
        return Vector3D(self.x / scalar, self.y / scalar, self.z / scalar)

    def __neg__(self) -> Vector3D:
        return Vector3D(-self.x, -self.y, -self.z)

    def dot(self, other: Vector3D) -> float:
        """Dot product."""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vector3D) -> Vector3D:
        """Cross product."""
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def length(self) -> float:
        """Vector magnitude."""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self) -> Vector3D:
        """Return unit vector."""
        mag = self.length()
        if mag == 0:
            return Vector3D(0, 0, 0)
        return self / mag

    def rotate_z(self, angle_deg: float) -> Vector3D:
        """Rotate around Z axis by angle in degrees."""
        angle_rad = math.radians(angle_deg)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        return Vector3D(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a,
            self.z,
        )

    def as_tuple(self) -> tuple[float, float, float]:
        """Return as tuple."""
        return (self.x, self.y, self.z)

    @classmethod
    def from_tuple(cls, t: Sequence[float]) -> Vector3D:
        """Create from tuple or list."""
        return cls(float(t[0]), float(t[1]), float(t[2]))

    @classmethod
    def origin(cls) -> Vector3D:
        """Return origin vector."""
        return cls(0.0, 0.0, 0.0)


@dataclass
class Polygon3D:
    """
    3D polygon defined by vertices.

    Example:
        >>> vertices = [Vector3D(0, 0, 0), Vector3D(1, 0, 0), Vector3D(1, 1, 0), Vector3D(0, 1, 0)]
        >>> poly = Polygon3D(vertices)
        >>> print(poly.area)
        1.0
    """

    vertices: list[Vector3D]

    @property
    def num_vertices(self) -> int:
        """Number of vertices."""
        return len(self.vertices)

    @property
    def normal(self) -> Vector3D:
        """Surface normal vector."""
        if self.num_vertices < 3:
            return Vector3D(0, 0, 1)

        # Use Newell's method for robustness
        n = Vector3D(0, 0, 0)
        for i in range(self.num_vertices):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % self.num_vertices]
            n = Vector3D(
                n.x + (v1.y - v2.y) * (v1.z + v2.z),
                n.y + (v1.z - v2.z) * (v1.x + v2.x),
                n.z + (v1.x - v2.x) * (v1.y + v2.y),
            )
        return n.normalize()

    @property
    def area(self) -> float:
        """Surface area using cross product method."""
        if self.num_vertices < 3:
            return 0.0

        # Triangulate and sum areas
        total = Vector3D(0, 0, 0)
        v0 = self.vertices[0]

        for i in range(1, self.num_vertices - 1):
            v1 = self.vertices[i]
            v2 = self.vertices[i + 1]
            edge1 = v1 - v0
            edge2 = v2 - v0
            cross = edge1.cross(edge2)
            total = total + cross

        return total.length() / 2.0

    @property
    def centroid(self) -> Vector3D:
        """Geometric center."""
        if not self.vertices:
            return Vector3D.origin()

        x = sum(v.x for v in self.vertices) / self.num_vertices
        y = sum(v.y for v in self.vertices) / self.num_vertices
        z = sum(v.z for v in self.vertices) / self.num_vertices
        return Vector3D(x, y, z)

    @property
    def tilt(self) -> float:
        """Surface tilt angle in degrees.

        0 = facing up (horizontal roof/ceiling), 90 = vertical wall,
        180 = facing down (horizontal floor).  Computed from the surface
        normal using the same convention as EnergyPlus / eppy.
        """
        n = self.normal
        # Clamp to avoid floating-point issues with acos
        clamped = max(-1.0, min(1.0, n.z))
        return math.degrees(math.acos(clamped))

    @property
    def azimuth(self) -> float:
        """Surface azimuth in degrees (0=north, 90=east, 180=south, 270=west).

        Uses the same convention as EnergyPlus / eppy: the angle of the
        outward normal projected onto the horizontal plane, measured
        clockwise from north (+Y axis).

        Returns 0.0 for perfectly horizontal surfaces (tilt 0 or 180).
        """
        n = self.normal
        # For horizontal surfaces the azimuth is undefined
        if abs(n.x) < 1e-10 and abs(n.y) < 1e-10:
            return 0.0
        # atan2 gives angle from +X axis counter-clockwise.
        # We want angle from +Y axis clockwise.
        angle = math.degrees(math.atan2(n.x, n.y))
        if angle < 0:
            angle += 360.0
        return angle

    @property
    def is_horizontal(self) -> bool:
        """Check if polygon is horizontal (floor/ceiling)."""
        n = self.normal
        return abs(n.z) > 0.99

    @property
    def is_vertical(self) -> bool:
        """Check if polygon is vertical (wall)."""
        n = self.normal
        return abs(n.z) < 0.01

    def translate(self, offset: Vector3D) -> Polygon3D:
        """Return translated polygon."""
        return Polygon3D([v + offset for v in self.vertices])

    def rotate_z(self, angle_deg: float, anchor: Vector3D | None = None) -> Polygon3D:
        """Rotate around Z axis."""
        if anchor is None:
            anchor = self.centroid

        rotated: list[Vector3D] = []
        for v in self.vertices:
            # Translate to anchor, rotate, translate back
            relative = v - anchor
            rotated_rel = relative.rotate_z(angle_deg)
            rotated.append(rotated_rel + anchor)

        return Polygon3D(rotated)

    def as_tuple_list(self) -> list[tuple[float, float, float]]:
        """Return vertices as list of tuples."""
        return [v.as_tuple() for v in self.vertices]

    @classmethod
    def from_tuples(cls, coords: Sequence[Sequence[float]]) -> Polygon3D:
        """Create from sequence of coordinate tuples."""
        return cls([Vector3D.from_tuple(c) for c in coords])


def get_surface_coords(surface: IDFObject) -> Polygon3D | None:
    """
    Extract coordinates from a surface object.

    Works with BuildingSurface:Detailed, FenestrationSurface:Detailed, etc.
    Supports both field naming conventions:

    - Classic/programmatic: ``vertex_1_x_coordinate``, ``vertex_2_x_coordinate``, ...
    - epJSON schema: ``vertex_x_coordinate``, ``vertex_x_coordinate_2``, ...
    """
    vertices = _get_vertices_classic(surface)
    if not vertices:
        vertices = _get_vertices_schema(surface)
    if len(vertices) < 3:
        return None
    return Polygon3D(vertices)


def _get_vertices_classic(surface: IDFObject) -> list[Vector3D]:
    """Extract vertices using ``vertex_{i}_x_coordinate`` naming."""
    num_verts = getattr(surface, "number_of_vertices", None)
    if num_verts is None:
        i = 1
        while getattr(surface, f"vertex_{i}_x_coordinate", None) is not None:
            i += 1
        num_verts = i - 1

    vertices: list[Vector3D] = []
    for i in range(1, int(num_verts) + 1):
        x = getattr(surface, f"vertex_{i}_x_coordinate", None)
        y = getattr(surface, f"vertex_{i}_y_coordinate", None)
        z = getattr(surface, f"vertex_{i}_z_coordinate", None)
        if x is not None and y is not None and z is not None:
            vertices.append(Vector3D(float(x), float(y), float(z)))
    return vertices


def _get_vertices_schema(surface: IDFObject) -> list[Vector3D]:
    """Extract vertices using ``vertex_x_coordinate``, ``vertex_x_coordinate_2`` naming."""
    vertices: list[Vector3D] = []
    x = getattr(surface, "vertex_x_coordinate", None)
    y = getattr(surface, "vertex_y_coordinate", None)
    z = getattr(surface, "vertex_z_coordinate", None)
    if x is not None and y is not None and z is not None:
        vertices.append(Vector3D(float(x), float(y), float(z)))

    i = 2
    while True:
        x = getattr(surface, f"vertex_x_coordinate_{i}", None)
        y = getattr(surface, f"vertex_y_coordinate_{i}", None)
        z = getattr(surface, f"vertex_z_coordinate_{i}", None)
        if x is None or y is None or z is None:
            break
        vertices.append(Vector3D(float(x), float(y), float(z)))
        i += 1
    return vertices


def set_surface_coords(surface: IDFObject, polygon: Polygon3D) -> None:
    """
    Set coordinates on a surface object.

    Updates vertex fields and number_of_vertices.
    """
    # Set number of vertices
    surface.number_of_vertices = len(polygon.vertices)

    # Set vertex coordinates
    for i, vertex in enumerate(polygon.vertices, 1):
        setattr(surface, f"vertex_{i}_x_coordinate", vertex.x)
        setattr(surface, f"vertex_{i}_y_coordinate", vertex.y)
        setattr(surface, f"vertex_{i}_z_coordinate", vertex.z)


def get_zone_origin(zone: IDFObject) -> Vector3D:
    """Get the origin point of a zone."""
    x = getattr(zone, "x_origin", 0) or 0
    y = getattr(zone, "y_origin", 0) or 0
    z = getattr(zone, "z_origin", 0) or 0
    return Vector3D(float(x), float(y), float(z))


def get_zone_rotation(zone: IDFObject) -> float:
    """Get the rotation angle of a zone in degrees."""
    angle = getattr(zone, "direction_of_relative_north", 0)
    return float(angle) if angle else 0.0


def translate_to_world(doc: IDFDocument) -> None:  # noqa: C901
    """
    Translate model from relative to world coordinates.

    Applies zone origins and rotations to surface coordinates.
    """
    # Check coordinate system
    geo_rules = doc["GlobalGeometryRules"]
    if geo_rules:
        rules = geo_rules.first()
        coord_system = getattr(rules, "coordinate_system", "World")
        if coord_system and coord_system.lower() == "world":
            return  # Already in world coordinates

    # Get building north axis
    building = doc["Building"]
    north_axis = 0.0
    if building:
        b = building.first()
        north_axis = float(getattr(b, "north_axis", 0) or 0)

    # Process each zone
    for zone in doc["Zone"]:
        zone_origin = get_zone_origin(zone)
        zone_rotation = get_zone_rotation(zone)
        total_rotation = north_axis + zone_rotation

        # Get surfaces in this zone
        zone_name = zone.name
        surfaces = list(doc.get_referencing(zone_name))

        for surface in surfaces:
            # Only process surfaces with coordinates
            coords = get_surface_coords(surface)
            if coords is None:
                continue

            # Apply rotation
            if total_rotation != 0:
                coords = coords.rotate_z(total_rotation)

            # Apply translation
            coords = coords.translate(zone_origin)

            # Update surface
            set_surface_coords(surface, coords)

    # Update zone origins to zero
    for zone in doc["Zone"]:
        zone.x_origin = 0.0
        zone.y_origin = 0.0
        zone.z_origin = 0.0
        zone.direction_of_relative_north = 0.0

    # Update building north axis
    if building:
        b = building.first()
        if b is not None:
            b.north_axis = 0.0

    # Update coordinate system to World
    if geo_rules:
        rules = geo_rules.first()
        if rules is not None:
            rules.coordinate_system = "World"


def calculate_surface_area(surface: IDFObject) -> float:
    """Calculate the area of a surface."""
    coords = get_surface_coords(surface)
    return coords.area if coords else 0.0


def calculate_surface_tilt(surface: IDFObject) -> float:
    """Calculate the tilt of a surface in degrees (eppy compatibility).

    0 = facing up, 90 = vertical, 180 = facing down.
    """
    coords = get_surface_coords(surface)
    return coords.tilt if coords else 0.0


def calculate_surface_azimuth(surface: IDFObject) -> float:
    """Calculate the azimuth of a surface in degrees (eppy compatibility).

    0 = north, 90 = east, 180 = south, 270 = west.
    """
    coords = get_surface_coords(surface)
    return coords.azimuth if coords else 0.0


def calculate_zone_floor_area(doc: IDFDocument, zone_name: str) -> float:
    """Calculate the total floor area of a zone."""
    total_area = 0.0

    for surface in doc["BuildingSurface:Detailed"]:
        if getattr(surface, "zone_name", "").upper() != zone_name.upper():
            continue

        surface_type = getattr(surface, "surface_type", "")
        if surface_type and surface_type.lower() == "floor":
            total_area += calculate_surface_area(surface)

    return total_area


def calculate_zone_ceiling_area(doc: IDFDocument, zone_name: str) -> float:
    """Calculate the total ceiling/roof area of a zone (eppy compatibility)."""
    total_area = 0.0

    for surface in doc["BuildingSurface:Detailed"]:
        if getattr(surface, "zone_name", "").upper() != zone_name.upper():
            continue

        surface_type = getattr(surface, "surface_type", "")
        if surface_type and surface_type.lower() in ("ceiling", "roof"):
            total_area += calculate_surface_area(surface)

    return total_area


def calculate_zone_height(doc: IDFDocument, zone_name: str) -> float:
    """Calculate the height of a zone from its surfaces.

    Returns the difference between the maximum and minimum Z coordinates
    across all surfaces belonging to the zone.
    """
    z_min = float("inf")
    z_max = float("-inf")

    for surface in doc["BuildingSurface:Detailed"]:
        if getattr(surface, "zone_name", "").upper() != zone_name.upper():
            continue

        coords = get_surface_coords(surface)
        if coords is None:
            continue

        for v in coords.vertices:
            z_min = min(z_min, v.z)
            z_max = max(z_max, v.z)

    if z_min == float("inf"):
        return 0.0
    return z_max - z_min


def translate_building(doc: IDFDocument, offset: Vector3D) -> None:
    """Translate all building surfaces by the given offset vector.

    Modifies the document in-place, shifting every surface's vertices
    by *offset*.
    """
    surface_types = [
        "BuildingSurface:Detailed",
        "FenestrationSurface:Detailed",
        "Shading:Site:Detailed",
        "Shading:Building:Detailed",
        "Shading:Zone:Detailed",
    ]
    for stype in surface_types:
        for surface in doc[stype]:
            coords = get_surface_coords(surface)
            if coords is not None:
                set_surface_coords(surface, coords.translate(offset))


def rotate_building(doc: IDFDocument, angle_deg: float, anchor: Vector3D | None = None) -> None:
    """Rotate all building surfaces around the Z axis.

    Args:
        doc: The document to modify in-place.
        angle_deg: Rotation angle in degrees (positive = counter-clockwise when
            viewed from above).
        anchor: Point to rotate around.  If ``None``, the origin ``(0, 0, 0)``
            is used.
    """
    if anchor is None:
        anchor = Vector3D.origin()

    surface_types = [
        "BuildingSurface:Detailed",
        "FenestrationSurface:Detailed",
        "Shading:Site:Detailed",
        "Shading:Building:Detailed",
        "Shading:Zone:Detailed",
    ]
    for stype in surface_types:
        for surface in doc[stype]:
            coords = get_surface_coords(surface)
            if coords is not None:
                set_surface_coords(surface, coords.rotate_z(angle_deg, anchor=anchor))


def calculate_zone_volume(doc: IDFDocument, zone_name: str) -> float:
    """
    Calculate the volume of a zone from its surfaces.

    Uses the divergence theorem to compute volume from surface polygons.
    """
    volume = 0.0

    for surface in doc["BuildingSurface:Detailed"]:
        if getattr(surface, "zone_name", "").upper() != zone_name.upper():
            continue

        coords = get_surface_coords(surface)
        if coords is None or coords.num_vertices < 3:
            continue

        # Contribution to volume using signed volume of tetrahedra
        centroid = coords.centroid
        for i in range(coords.num_vertices):
            v1 = coords.vertices[i]
            v2 = coords.vertices[(i + 1) % coords.num_vertices]

            # Volume of tetrahedron with origin
            volume += v1.dot(v2.cross(centroid)) / 6.0

    return abs(volume)
