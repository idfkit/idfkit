"""
Geometry utilities for IDF models.

Provides coordinate handling and transformations without geomeppy dependency.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .document import IDFDocument
    from .objects import IDFObject

# Surface types that carry vertex geometry.  Used by translate_building,
# rotate_building, scale_building, and related functions.
VERTEX_SURFACE_TYPES: list[str] = [
    "BuildingSurface:Detailed",
    "FenestrationSurface:Detailed",
    "Shading:Site:Detailed",
    "Shading:Building:Detailed",
    "Shading:Zone:Detailed",
]


@dataclass(frozen=True, slots=True)
class Vector3D:
    """
    Immutable 3D vector.

    Supports arithmetic operations (``+``, ``-``, ``*``, ``/``, unary ``-``)
    and common vector operations (dot product, cross product, normalization).

    Examples:
        >>> v = Vector3D(1.0, 2.0, 3.0)
        >>> v.x, v.y, v.z
        (1.0, 2.0, 3.0)

        Vectors support arithmetic:

        >>> Vector3D(1, 2, 3) + Vector3D(4, 5, 6)
        Vector3D(x=5, y=7, z=9)
        >>> Vector3D(3, 0, 0) * 2
        Vector3D(x=6, y=0, z=0)
        >>> -Vector3D(1, 0, 0)
        Vector3D(x=-1, y=0, z=0)
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
        """Dot product.

        Examples:
            >>> Vector3D(1, 0, 0).dot(Vector3D(0, 1, 0))
            0
            >>> Vector3D(3.0, 0.0, 0.0).dot(Vector3D(4.0, 0.0, 0.0))
            12.0
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vector3D) -> Vector3D:
        """Cross product.

        Examples:
            >>> Vector3D(1, 0, 0).cross(Vector3D(0, 1, 0))
            Vector3D(x=0, y=0, z=1)
            >>> Vector3D(3, 0, 0).cross(Vector3D(0, 4, 0))
            Vector3D(x=0, y=0, z=12)
        """
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def length(self) -> float:
        """Vector magnitude.

        Examples:
            >>> Vector3D(3, 4, 0).length()
            5.0
            >>> Vector3D(1, 0, 0).length()
            1.0
        """
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self) -> Vector3D:
        """Return unit vector.

        Examples:
            >>> Vector3D(3, 0, 0).normalize()
            Vector3D(x=1.0, y=0.0, z=0.0)
            >>> Vector3D(0, 0, 5).normalize()
            Vector3D(x=0.0, y=0.0, z=1.0)
        """
        mag = self.length()
        if mag == 0:
            return Vector3D(0, 0, 0)
        return self / mag

    def rotate_z(self, angle_deg: float) -> Vector3D:
        """Rotate around Z axis by angle in degrees.

        Examples:
            >>> v = Vector3D(1, 0, 0).rotate_z(90)
            >>> round(v.x, 10), round(v.y, 10)
            (0.0, 1.0)
            >>> Vector3D(1, 0, 5).rotate_z(180)  # doctest: +SKIP
            Vector3D(x=-1.0, y=0.0, z=5.0)
        """
        angle_rad = math.radians(angle_deg)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        return Vector3D(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a,
            self.z,
        )

    def as_tuple(self) -> tuple[float, float, float]:
        """Return as tuple.

        Examples:
            >>> Vector3D(1.0, 2.0, 3.0).as_tuple()
            (1.0, 2.0, 3.0)
            >>> Vector3D.origin().as_tuple()
            (0.0, 0.0, 0.0)
        """
        return (self.x, self.y, self.z)

    @classmethod
    def from_tuple(cls, t: Sequence[float]) -> Vector3D:
        """Create from tuple or list.

        Examples:
            >>> Vector3D.from_tuple((1.0, 2.0, 3.0))
            Vector3D(x=1.0, y=2.0, z=3.0)
            >>> Vector3D.from_tuple([0, 0, 0])
            Vector3D(x=0.0, y=0.0, z=0.0)
        """
        return cls(float(t[0]), float(t[1]), float(t[2]))

    @classmethod
    def origin(cls) -> Vector3D:
        """Return origin vector.

        Examples:
            >>> Vector3D.origin()
            Vector3D(x=0.0, y=0.0, z=0.0)
        """
        return cls(0.0, 0.0, 0.0)


@dataclass
class Polygon3D:
    """
    3D polygon defined by vertices.

    Computes geometric properties (area, normal, tilt, azimuth) and supports
    transformations (translate, rotate).

    Examples:
        A 5 m x 4 m ground-floor slab:

        >>> floor = Polygon3D([
        ...     Vector3D(0, 0, 0), Vector3D(5, 0, 0),
        ...     Vector3D(5, 4, 0), Vector3D(0, 4, 0),
        ... ])
        >>> floor.area
        20.0
        >>> floor.is_horizontal
        True

        A 10 m wide, 3 m high south-facing exterior wall:

        >>> south_wall = Polygon3D([
        ...     Vector3D(0, 0, 0), Vector3D(10, 0, 0),
        ...     Vector3D(10, 0, 3), Vector3D(0, 0, 3),
        ... ])
        >>> south_wall.area
        30.0
        >>> south_wall.tilt
        90.0
        >>> south_wall.azimuth
        180.0
    """

    vertices: list[Vector3D]

    @property
    def num_vertices(self) -> int:
        """Number of vertices.

        Examples:
            >>> Polygon3D([Vector3D(0,0,0), Vector3D(1,0,0), Vector3D(0,1,0)]).num_vertices
            3
        """
        return len(self.vertices)

    @property
    def normal(self) -> Vector3D:
        """Surface normal vector.

        Examples:
            >>> floor = Polygon3D([
            ...     Vector3D(0, 0, 0), Vector3D(1, 0, 0),
            ...     Vector3D(1, 1, 0), Vector3D(0, 1, 0),
            ... ])
            >>> floor.normal
            Vector3D(x=0.0, y=0.0, z=1.0)
        """
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
        """Surface area using cross product method.

        Examples:
            A 5 m x 5 m floor slab:

            >>> Polygon3D([
            ...     Vector3D(0,0,0), Vector3D(5,0,0),
            ...     Vector3D(5,5,0), Vector3D(0,5,0),
            ... ]).area
            25.0
        """
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
        """Geometric center.

        Examples:
            >>> Polygon3D([
            ...     Vector3D(0,0,0), Vector3D(4,0,0),
            ...     Vector3D(4,4,0), Vector3D(0,4,0),
            ... ]).centroid
            Vector3D(x=2.0, y=2.0, z=0.0)
        """
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

        Examples:
            Flat roof (tilt 0 = facing up):

            >>> Polygon3D([
            ...     Vector3D(0,0,3), Vector3D(5,0,3),
            ...     Vector3D(5,5,3), Vector3D(0,5,3),
            ... ]).tilt
            0.0

            Exterior wall (tilt 90 = vertical):

            >>> Polygon3D([
            ...     Vector3D(0,0,0), Vector3D(10,0,0),
            ...     Vector3D(10,0,3), Vector3D(0,0,3),
            ... ]).tilt
            90.0
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

        Examples:
            South-facing wall (normal points toward -Y):

            >>> Polygon3D([
            ...     Vector3D(0,0,0), Vector3D(10,0,0),
            ...     Vector3D(10,0,3), Vector3D(0,0,3),
            ... ]).azimuth
            180.0

            Horizontal surface has azimuth 0:

            >>> Polygon3D([
            ...     Vector3D(0,0,0), Vector3D(1,0,0),
            ...     Vector3D(1,1,0), Vector3D(0,1,0),
            ... ]).azimuth
            0.0
        """
        n = self.normal
        # For horizontal surfaces the azimuth is undefined
        if abs(n.x) < 1e-10 and abs(n.y) < 1e-10:
            return 0.0
        # atan2(x, y) gives the angle from +Y axis toward +X axis,
        # which is clockwise from north -- exactly the convention we need.
        angle = math.degrees(math.atan2(n.x, n.y))
        if angle < 0:
            angle += 360.0
        return angle

    @property
    def is_horizontal(self) -> bool:
        """Check if polygon is horizontal (floor/ceiling).

        Examples:
            >>> Polygon3D([
            ...     Vector3D(0,0,0), Vector3D(1,0,0),
            ...     Vector3D(1,1,0), Vector3D(0,1,0),
            ... ]).is_horizontal
            True
            >>> Polygon3D([
            ...     Vector3D(0,0,0), Vector3D(1,0,0),
            ...     Vector3D(1,0,1), Vector3D(0,0,1),
            ... ]).is_horizontal
            False
        """
        n = self.normal
        return abs(n.z) > 0.99

    @property
    def is_vertical(self) -> bool:
        """Check if polygon is vertical (wall).

        Examples:
            >>> Polygon3D([
            ...     Vector3D(0,0,0), Vector3D(1,0,0),
            ...     Vector3D(1,0,1), Vector3D(0,0,1),
            ... ]).is_vertical
            True
            >>> Polygon3D([
            ...     Vector3D(0,0,0), Vector3D(1,0,0),
            ...     Vector3D(1,1,0), Vector3D(0,1,0),
            ... ]).is_vertical
            False
        """
        n = self.normal
        return abs(n.z) < 0.01

    def translate(self, offset: Vector3D) -> Polygon3D:
        """Return translated polygon.

        Examples:
            >>> tri = Polygon3D([Vector3D(0,0,0), Vector3D(1,0,0), Vector3D(0,1,0)])
            >>> moved = tri.translate(Vector3D(10, 20, 0))
            >>> moved.centroid
            Vector3D(x=10.333333333333334, y=20.333333333333332, z=0.0)
        """
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
        """Return vertices as list of tuples.

        Examples:
            >>> tri = Polygon3D([Vector3D(0,0,0), Vector3D(1,0,0), Vector3D(0,1,0)])
            >>> tri.as_tuple_list()
            [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
        """
        return [v.as_tuple() for v in self.vertices]

    @classmethod
    def from_tuples(cls, coords: Sequence[Sequence[float]]) -> Polygon3D:
        """Create from sequence of coordinate tuples.

        Examples:
            >>> poly = Polygon3D.from_tuples([(0,0,0), (5,0,0), (5,5,0), (0,5,0)])
            >>> poly.area
            25.0
            >>> poly.num_vertices
            4
        """
        return cls([Vector3D.from_tuple(c) for c in coords])


def get_surface_coords(surface: IDFObject) -> Polygon3D | None:
    """
    Extract coordinates from a surface object.

    Works with BuildingSurface:Detailed, FenestrationSurface:Detailed, etc.
    Supports both field naming conventions:

    - Classic/programmatic: ``vertex_1_x_coordinate``, ``vertex_2_x_coordinate``, ...
    - epJSON schema: ``vertex_x_coordinate``, ``vertex_x_coordinate_2``, ...

    Examples:
        Extract geometry from a 10 m x 3 m south-facing exterior wall:

        >>> from idfkit import new_document
        >>> model = new_document()
        >>> wall = model.add("BuildingSurface:Detailed", "South_Wall",
        ...     surface_type="Wall", construction_name="", zone_name="",
        ...     outside_boundary_condition="Outdoors",
        ...     sun_exposure="SunExposed", wind_exposure="WindExposed",
        ...     number_of_vertices=4,
        ...     vertex_1_x_coordinate=0, vertex_1_y_coordinate=0, vertex_1_z_coordinate=3,
        ...     vertex_2_x_coordinate=0, vertex_2_y_coordinate=0, vertex_2_z_coordinate=0,
        ...     vertex_3_x_coordinate=10, vertex_3_y_coordinate=0, vertex_3_z_coordinate=0,
        ...     vertex_4_x_coordinate=10, vertex_4_y_coordinate=0, vertex_4_z_coordinate=3,
        ...     validate=False)
        >>> poly = get_surface_coords(wall)
        >>> poly.area
        30.0
        >>> poly.azimuth
        180.0
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

    Examples:
        Shorten a wall from 10 m to 5 m by replacing its vertices:

        >>> from idfkit import new_document
        >>> model = new_document()
        >>> wall = model.add("BuildingSurface:Detailed", "South_Wall",
        ...     surface_type="Wall", construction_name="", zone_name="",
        ...     outside_boundary_condition="Outdoors",
        ...     sun_exposure="SunExposed", wind_exposure="WindExposed",
        ...     number_of_vertices=4,
        ...     vertex_1_x_coordinate=0, vertex_1_y_coordinate=0, vertex_1_z_coordinate=3,
        ...     vertex_2_x_coordinate=0, vertex_2_y_coordinate=0, vertex_2_z_coordinate=0,
        ...     vertex_3_x_coordinate=10, vertex_3_y_coordinate=0, vertex_3_z_coordinate=0,
        ...     vertex_4_x_coordinate=10, vertex_4_y_coordinate=0, vertex_4_z_coordinate=3,
        ...     validate=False)
        >>> shorter = Polygon3D.from_tuples([(0,0,0),(5,0,0),(5,0,3),(0,0,3)])
        >>> set_surface_coords(wall, shorter)
        >>> get_surface_coords(wall).area
        15.0
    """
    # Set number of vertices
    surface.number_of_vertices = len(polygon.vertices)

    # Set vertex coordinates
    for i, vertex in enumerate(polygon.vertices, 1):
        setattr(surface, f"vertex_{i}_x_coordinate", vertex.x)
        setattr(surface, f"vertex_{i}_y_coordinate", vertex.y)
        setattr(surface, f"vertex_{i}_z_coordinate", vertex.z)


def get_zone_origin(zone: IDFObject) -> Vector3D:
    """Get the origin point of a zone.

    Examples:
        A second-floor zone offset 3.5 m above ground:

        >>> from idfkit import new_document
        >>> model = new_document()
        >>> zone = model.add("Zone", "Floor2_Office",
        ...     x_origin=10.0, y_origin=20.0, z_origin=3.5)
        >>> get_zone_origin(zone)
        Vector3D(x=10.0, y=20.0, z=3.5)
    """
    x = getattr(zone, "x_origin", 0) or 0
    y = getattr(zone, "y_origin", 0) or 0
    z = getattr(zone, "z_origin", 0) or 0
    return Vector3D(float(x), float(y), float(z))


def get_zone_rotation(zone: IDFObject) -> float:
    """Get the rotation angle of a zone in degrees.

    Examples:
        A zone rotated 45 degrees from true north (common for
        buildings aligned to a street grid):

        >>> from idfkit import new_document
        >>> model = new_document()
        >>> zone = model.add("Zone", "Corner_Office",
        ...     direction_of_relative_north=45.0)
        >>> get_zone_rotation(zone)
        45.0
    """
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
    """Calculate the area of a surface in m².

    Examples:
        Area of a 10 m wide, 3 m high exterior wall:

        >>> from idfkit import new_document
        >>> model = new_document()
        >>> wall = model.add("BuildingSurface:Detailed", "South_Wall",
        ...     surface_type="Wall", construction_name="", zone_name="",
        ...     outside_boundary_condition="Outdoors",
        ...     sun_exposure="SunExposed", wind_exposure="WindExposed",
        ...     number_of_vertices=4,
        ...     vertex_1_x_coordinate=0, vertex_1_y_coordinate=0, vertex_1_z_coordinate=3,
        ...     vertex_2_x_coordinate=0, vertex_2_y_coordinate=0, vertex_2_z_coordinate=0,
        ...     vertex_3_x_coordinate=10, vertex_3_y_coordinate=0, vertex_3_z_coordinate=0,
        ...     vertex_4_x_coordinate=10, vertex_4_y_coordinate=0, vertex_4_z_coordinate=3,
        ...     validate=False)
        >>> calculate_surface_area(wall)
        30.0
    """
    coords = get_surface_coords(surface)
    return coords.area if coords else 0.0


def calculate_surface_tilt(surface: IDFObject) -> float:
    """Calculate the tilt of a surface in degrees (eppy compatibility).

    0 = facing up (roof), 90 = vertical (wall), 180 = facing down (floor).

    Examples:
        Verify that an exterior wall is vertical:

        >>> from idfkit import new_document
        >>> model = new_document()
        >>> wall = model.add("BuildingSurface:Detailed", "South_Wall",
        ...     surface_type="Wall", construction_name="", zone_name="",
        ...     outside_boundary_condition="Outdoors",
        ...     sun_exposure="SunExposed", wind_exposure="WindExposed",
        ...     number_of_vertices=4,
        ...     vertex_1_x_coordinate=0, vertex_1_y_coordinate=0, vertex_1_z_coordinate=3,
        ...     vertex_2_x_coordinate=0, vertex_2_y_coordinate=0, vertex_2_z_coordinate=0,
        ...     vertex_3_x_coordinate=10, vertex_3_y_coordinate=0, vertex_3_z_coordinate=0,
        ...     vertex_4_x_coordinate=10, vertex_4_y_coordinate=0, vertex_4_z_coordinate=3,
        ...     validate=False)
        >>> calculate_surface_tilt(wall)
        90.0
    """
    coords = get_surface_coords(surface)
    return coords.tilt if coords else 0.0


def calculate_surface_azimuth(surface: IDFObject) -> float:
    """Calculate the azimuth of a surface in degrees (eppy compatibility).

    0 = north, 90 = east, 180 = south, 270 = west.  Useful for
    identifying solar exposure for glazing and shading studies.

    Examples:
        Confirm a wall faces south (azimuth 180):

        >>> from idfkit import new_document
        >>> model = new_document()
        >>> wall = model.add("BuildingSurface:Detailed", "SouthWall",
        ...     surface_type="Wall", construction_name="", zone_name="",
        ...     outside_boundary_condition="Outdoors",
        ...     sun_exposure="SunExposed", wind_exposure="WindExposed",
        ...     number_of_vertices=4,
        ...     vertex_1_x_coordinate=0, vertex_1_y_coordinate=0, vertex_1_z_coordinate=3,
        ...     vertex_2_x_coordinate=0, vertex_2_y_coordinate=0, vertex_2_z_coordinate=0,
        ...     vertex_3_x_coordinate=10, vertex_3_y_coordinate=0, vertex_3_z_coordinate=0,
        ...     vertex_4_x_coordinate=10, vertex_4_y_coordinate=0, vertex_4_z_coordinate=3,
        ...     validate=False)
        >>> calculate_surface_azimuth(wall)
        180.0
    """
    coords = get_surface_coords(surface)
    return coords.azimuth if coords else 0.0


def calculate_zone_floor_area(doc: IDFDocument, zone_name: str) -> float:
    """Calculate the total floor area of a zone.

    Sums the area of all ``BuildingSurface:Detailed`` objects whose
    ``surface_type`` is ``"Floor"`` and whose ``zone_name`` matches.

    Examples:
        Calculate the floor area of a 5 m x 4 m office:

        >>> from idfkit import new_document
        >>> model = new_document()
        >>> model.add("Zone", "Office")  # doctest: +ELLIPSIS
        Zone('Office')
        >>> model.add("BuildingSurface:Detailed", "Office_Floor",
        ...     surface_type="Floor", construction_name="", zone_name="Office",
        ...     outside_boundary_condition="Ground",
        ...     number_of_vertices=4,
        ...     vertex_1_x_coordinate=0, vertex_1_y_coordinate=0, vertex_1_z_coordinate=0,
        ...     vertex_2_x_coordinate=5, vertex_2_y_coordinate=0, vertex_2_z_coordinate=0,
        ...     vertex_3_x_coordinate=5, vertex_3_y_coordinate=4, vertex_3_z_coordinate=0,
        ...     vertex_4_x_coordinate=0, vertex_4_y_coordinate=4, vertex_4_z_coordinate=0,
        ...     validate=False)  # doctest: +ELLIPSIS
        BuildingSurface:Detailed('Office_Floor')
        >>> calculate_zone_floor_area(model, "Office")
        20.0
    """
    total_area = 0.0

    for surface in doc["BuildingSurface:Detailed"]:
        if (getattr(surface, "zone_name", None) or "").upper() != zone_name.upper():
            continue

        surface_type = getattr(surface, "surface_type", None) or ""
        if surface_type and surface_type.lower() == "floor":
            total_area += calculate_surface_area(surface)

    return total_area


def calculate_zone_ceiling_area(doc: IDFDocument, zone_name: str) -> float:
    """Calculate the total ceiling/roof area of a zone (eppy compatibility).

    Sums the area of all surfaces whose ``surface_type`` is ``"Ceiling"``
    or ``"Roof"`` in the given zone.

    Examples:
        Calculate the ceiling area of a 5 m x 4 m office at z=3 m:

        >>> from idfkit import new_document
        >>> model = new_document()
        >>> model.add("Zone", "Office")  # doctest: +ELLIPSIS
        Zone('Office')
        >>> model.add("BuildingSurface:Detailed", "Office_Ceiling",
        ...     surface_type="Ceiling", construction_name="", zone_name="Office",
        ...     outside_boundary_condition="Outdoors",
        ...     number_of_vertices=4,
        ...     vertex_1_x_coordinate=0, vertex_1_y_coordinate=0, vertex_1_z_coordinate=3,
        ...     vertex_2_x_coordinate=0, vertex_2_y_coordinate=4, vertex_2_z_coordinate=3,
        ...     vertex_3_x_coordinate=5, vertex_3_y_coordinate=4, vertex_3_z_coordinate=3,
        ...     vertex_4_x_coordinate=5, vertex_4_y_coordinate=0, vertex_4_z_coordinate=3,
        ...     validate=False)  # doctest: +ELLIPSIS
        BuildingSurface:Detailed('Office_Ceiling')
        >>> calculate_zone_ceiling_area(model, "Office")
        20.0
    """
    total_area = 0.0

    for surface in doc["BuildingSurface:Detailed"]:
        if (getattr(surface, "zone_name", None) or "").upper() != zone_name.upper():
            continue

        surface_type = getattr(surface, "surface_type", None) or ""
        if surface_type and surface_type.lower() in ("ceiling", "roof"):
            total_area += calculate_surface_area(surface)

    return total_area


def calculate_zone_height(doc: IDFDocument, zone_name: str) -> float:
    """Calculate the height of a zone from its surfaces.

    Returns the difference between the maximum and minimum Z coordinates
    across all surfaces belonging to the zone.

    Examples:
        Determine the floor-to-ceiling height of a 3 m tall office:

        >>> from idfkit import new_document
        >>> model = new_document()
        >>> model.add("Zone", "Office")  # doctest: +ELLIPSIS
        Zone('Office')
        >>> model.add("BuildingSurface:Detailed", "South_Wall",
        ...     surface_type="Wall", construction_name="", zone_name="Office",
        ...     outside_boundary_condition="Outdoors",
        ...     sun_exposure="SunExposed", wind_exposure="WindExposed",
        ...     number_of_vertices=4,
        ...     vertex_1_x_coordinate=0, vertex_1_y_coordinate=0, vertex_1_z_coordinate=3,
        ...     vertex_2_x_coordinate=0, vertex_2_y_coordinate=0, vertex_2_z_coordinate=0,
        ...     vertex_3_x_coordinate=5, vertex_3_y_coordinate=0, vertex_3_z_coordinate=0,
        ...     vertex_4_x_coordinate=5, vertex_4_y_coordinate=0, vertex_4_z_coordinate=3,
        ...     validate=False)  # doctest: +ELLIPSIS
        BuildingSurface:Detailed('South_Wall')
        >>> calculate_zone_height(model, "Office")
        3.0
    """
    z_min = float("inf")
    z_max = float("-inf")

    for surface in doc["BuildingSurface:Detailed"]:
        if (getattr(surface, "zone_name", None) or "").upper() != zone_name.upper():
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

    .. note::

       Only vertex coordinates are modified.  ``Zone`` origin fields
       and the ``Building`` object are **not** updated.  Use
       :func:`translate_to_world` if you need to collapse zone-relative
       coordinates into world coordinates.

    Examples:
        Reposition a building on its site (e.g., from local to
        geo-referenced coordinates):

        >>> from idfkit import new_document
        >>> model = new_document()
        >>> wall = model.add("BuildingSurface:Detailed", "South_Wall",
        ...     surface_type="Wall", construction_name="", zone_name="",
        ...     outside_boundary_condition="Outdoors",
        ...     sun_exposure="SunExposed", wind_exposure="WindExposed",
        ...     number_of_vertices=4,
        ...     vertex_1_x_coordinate=0, vertex_1_y_coordinate=0, vertex_1_z_coordinate=3,
        ...     vertex_2_x_coordinate=0, vertex_2_y_coordinate=0, vertex_2_z_coordinate=0,
        ...     vertex_3_x_coordinate=10, vertex_3_y_coordinate=0, vertex_3_z_coordinate=0,
        ...     vertex_4_x_coordinate=10, vertex_4_y_coordinate=0, vertex_4_z_coordinate=3,
        ...     validate=False)
        >>> translate_building(model, Vector3D(100, 200, 0))
        >>> wall.vertex_1_x_coordinate
        100.0
    """
    for stype in VERTEX_SURFACE_TYPES:
        for surface in doc[stype]:
            coords = get_surface_coords(surface)
            if coords is not None:
                set_surface_coords(surface, coords.translate(offset))


def rotate_building(doc: IDFDocument, angle_deg: float, anchor: Vector3D | None = None) -> None:
    """Rotate all building surfaces around the Z axis.

    Only vertex coordinates are modified; ``Building.north_axis`` and
    ``Zone`` rotation fields are **not** updated.

    Args:
        doc: The document to modify in-place.
        angle_deg: Rotation angle in degrees (positive = counter-clockwise when
            viewed from above).
        anchor: Point to rotate around.  If ``None``, the origin ``(0, 0, 0)``
            is used.
    """
    if anchor is None:
        anchor = Vector3D.origin()

    for stype in VERTEX_SURFACE_TYPES:
        for surface in doc[stype]:
            coords = get_surface_coords(surface)
            if coords is not None:
                set_surface_coords(surface, coords.rotate_z(angle_deg, anchor=anchor))


def calculate_zone_volume(doc: IDFDocument, zone_name: str) -> float:
    """
    Calculate the volume of a zone from its surfaces.

    Uses the divergence theorem to compute volume from surface polygons.
    Returns 0.0 if the zone has no surfaces.
    """
    volume = 0.0

    for surface in doc["BuildingSurface:Detailed"]:
        if (getattr(surface, "zone_name", None) or "").upper() != zone_name.upper():
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


# ---------------------------------------------------------------------------
# Window-Wall Ratio (WWR)
# ---------------------------------------------------------------------------


def set_wwr(  # noqa: C901
    doc: IDFDocument,
    wwr: float,
    *,
    construction: str | None = None,
    surface_type: str = "Wall",
    orientation: str | None = None,
    tolerance: float = 10.0,
) -> list[IDFObject]:
    """Add or replace windows to achieve a target window-wall ratio.

    For each exterior wall matching the filter criteria, a single
    rectangular sub-surface (``FenestrationSurface:Detailed``) is
    created whose area equals ``wwr * wall_area``.  Any existing
    ``FenestrationSurface:Detailed`` sub-surfaces on matching walls are
    removed first.

    This is the idfkit equivalent of geomeppy's ``idf.set_wwr()``.

    Args:
        doc: The document to modify in-place.
        wwr: Target window-wall ratio in the range ``(0, 1)``.
        construction: Name of the window ``Construction`` to assign.
            If ``None``, the field is left empty (EnergyPlus will
            require it to be set before simulation).
        surface_type: Only walls whose ``surface_type`` matches (case-
            insensitive) are considered.  Defaults to ``"Wall"``.
        orientation: Optional cardinal direction filter — one of
            ``"north"``, ``"south"``, ``"east"``, ``"west"``.  Only
            walls within *tolerance* degrees of that azimuth are modified.
        tolerance: Azimuth tolerance in degrees when *orientation* is
            given.  Defaults to 10°.

    Returns:
        List of newly created ``FenestrationSurface:Detailed`` objects.

    Raises:
        ValueError: If *wwr* is not in ``(0, 1)``.
    """
    if not 0 < wwr < 1:
        msg = f"wwr must be between 0 and 1 (exclusive), got {wwr}"
        raise ValueError(msg)

    azimuth_target = _orientation_to_azimuth(orientation) if orientation else None

    # Remove existing fenestration on matching walls
    existing_fen: list[IDFObject] = []
    wall_names: set[str] = set()
    for wall in doc["BuildingSurface:Detailed"]:
        if not _wall_matches(wall, surface_type, azimuth_target, tolerance):
            continue
        wall_names.add(wall.name.upper())

    for fen in list(doc["FenestrationSurface:Detailed"]):
        bsn = getattr(fen, "building_surface_name", None) or ""
        if bsn.upper() in wall_names:
            existing_fen.append(fen)
    for fen in existing_fen:
        doc.removeidfobject(fen)

    # Create new windows
    new_windows: list[IDFObject] = []
    for wall in doc["BuildingSurface:Detailed"]:
        if not _wall_matches(wall, surface_type, azimuth_target, tolerance):
            continue
        obc = getattr(wall, "outside_boundary_condition", None) or ""
        if obc.upper() != "OUTDOORS":
            continue

        coords = get_surface_coords(wall)
        if coords is None or coords.area < 1e-6:
            continue

        window_poly = _inset_polygon(coords, wwr)
        if window_poly is None:
            continue

        win_name = f"{wall.name}_Window"
        win_data: dict[str, Any] = {
            "surface_type": "Window",
            "building_surface_name": wall.name,
            "number_of_vertices": window_poly.num_vertices,
        }
        if construction is not None:
            win_data["construction_name"] = construction
        for i, v in enumerate(window_poly.vertices, 1):
            win_data[f"vertex_{i}_x_coordinate"] = round(v.x, 6)
            win_data[f"vertex_{i}_y_coordinate"] = round(v.y, 6)
            win_data[f"vertex_{i}_z_coordinate"] = round(v.z, 6)

        win_obj = doc.add("FenestrationSurface:Detailed", win_name, win_data, validate=False)
        new_windows.append(win_obj)

    return new_windows


def _orientation_to_azimuth(orientation: str) -> float:
    """Convert cardinal direction to azimuth degrees."""
    mapping = {"north": 0.0, "east": 90.0, "south": 180.0, "west": 270.0}
    key = orientation.strip().lower()
    if key not in mapping:
        msg = f"orientation must be one of {list(mapping)}, got '{orientation}'"
        raise ValueError(msg)
    return mapping[key]


def _wall_matches(
    wall: IDFObject,
    surface_type: str,
    azimuth_target: float | None,
    tolerance: float,
) -> bool:
    """Check if a wall matches the surface type and orientation filter."""
    st = getattr(wall, "surface_type", None) or ""
    if st.upper() != surface_type.upper():
        return False
    if azimuth_target is not None:
        coords = get_surface_coords(wall)
        if coords is None:
            return False
        az = coords.azimuth
        diff = abs(az - azimuth_target)
        if diff > 180:
            diff = 360 - diff
        if diff > tolerance:
            return False
    return True


def _inset_polygon(wall_poly: Polygon3D, wwr: float) -> Polygon3D | None:
    """Create a rectangular window polygon inset into a wall polygon.

    The window is centred on the wall and sized so that its area equals
    ``wwr * wall_area``.  The inset preserves the wall's plane — it
    simply scales the bounding rectangle toward the centroid.
    """
    if wall_poly.num_vertices < 3:
        return None

    # Build a 2D coordinate system on the wall plane
    normal = wall_poly.normal
    # Pick a "horizontal" axis on the wall plane
    up = Vector3D(0, 0, 1)
    if abs(normal.dot(up)) > 0.99:
        # Wall is nearly horizontal — unusual, but handle it
        up = Vector3D(0, 1, 0)
    right = up.cross(normal).normalize()
    local_up = normal.cross(right).normalize()

    origin = wall_poly.centroid

    # Project vertices to 2D
    coords_2d: list[tuple[float, float]] = []
    for v in wall_poly.vertices:
        d = v - origin
        coords_2d.append((right.dot(d), local_up.dot(d)))

    # Bounding rectangle in 2D
    xs = [c[0] for c in coords_2d]
    ys = [c[1] for c in coords_2d]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    wall_w = max_x - min_x
    wall_h = max_y - min_y
    if wall_w < 1e-6 or wall_h < 1e-6:
        return None

    # Scale factor: window area = wwr * wall polygon area
    # We size the window proportional to the bounding rect
    scale = math.sqrt(wwr)
    win_w = wall_w * scale
    win_h = wall_h * scale

    cx = (min_x + max_x) / 2.0
    cy = (min_y + max_y) / 2.0

    # 2D corners of window (counter-clockwise from bottom-left)
    hw, hh = win_w / 2.0, win_h / 2.0
    win_2d = [
        (cx - hw, cy - hh),
        (cx + hw, cy - hh),
        (cx + hw, cy + hh),
        (cx - hw, cy + hh),
    ]

    # Project back to 3D
    window_verts = [origin + right * u + local_up * v for u, v in win_2d]
    return Polygon3D(window_verts)


# ---------------------------------------------------------------------------
# Surface Intersection and Boundary Matching
# ---------------------------------------------------------------------------


def intersect_match(doc: IDFDocument) -> None:  # noqa: C901
    """Match adjacent surfaces and set boundary conditions.

    Scans all ``BuildingSurface:Detailed`` walls and identifies pairs
    whose polygons are coincident (same plane, overlapping area).  For
    each matched pair, the boundary conditions are updated so the
    surfaces reference each other.

    This is the idfkit equivalent of geomeppy's
    ``idf.intersect_match()``.

    The algorithm is O(n²) over exterior walls but uses normal-vector
    and centroid-distance filters to skip most comparisons quickly.

    Args:
        doc: The document to modify in-place.

    .. note::

        This implementation handles the common case of full-overlap
        matching (same-size surfaces on opposite sides of a shared
        wall).  Partial intersection and surface splitting are **not**
        implemented — use EnergyPlus' ``ExpandObjects`` preprocessor
        or manual surface definition for complex cases.
    """
    walls: list[IDFObject] = []
    for surface in doc["BuildingSurface:Detailed"]:
        st = getattr(surface, "surface_type", None) or ""
        if st.upper() == "WALL":
            walls.append(surface)

    matched: set[int] = set()

    for i, wall_a in enumerate(walls):
        if id(wall_a) in matched:
            continue
        coords_a = get_surface_coords(wall_a)
        if coords_a is None:
            continue

        normal_a = coords_a.normal
        centroid_a = coords_a.centroid

        for j in range(i + 1, len(walls)):
            wall_b = walls[j]
            if id(wall_b) in matched:
                continue
            coords_b = get_surface_coords(wall_b)
            if coords_b is None:
                continue

            # Quick filter: normals must be anti-parallel
            normal_b = coords_b.normal
            dot = normal_a.dot(normal_b)
            if dot > -0.99:
                continue

            # Quick filter: centroids must be close
            centroid_b = coords_b.centroid
            dist = (centroid_a - centroid_b).length()
            if dist > 1.0:  # Allow 1 m tolerance for thick walls
                continue

            # Check coplanarity: centroid_b must lie on plane of A
            d = (centroid_b - centroid_a).dot(normal_a)
            if abs(d) > 0.5:  # Allow 0.5 m for wall thickness
                continue

            # Check area similarity
            area_a = coords_a.area
            area_b = coords_b.area
            if area_a < 1e-6:
                continue
            ratio = area_b / area_a
            if ratio < 0.9 or ratio > 1.1:
                continue

            # Match found — update boundary conditions
            wall_a.outside_boundary_condition = "Surface"
            wall_a.outside_boundary_condition_object = wall_b.name
            wall_a.sun_exposure = "NoSun"
            wall_a.wind_exposure = "NoWind"

            wall_b.outside_boundary_condition = "Surface"
            wall_b.outside_boundary_condition_object = wall_a.name
            wall_b.sun_exposure = "NoSun"
            wall_b.wind_exposure = "NoWind"

            matched.add(id(wall_a))
            matched.add(id(wall_b))
            break
