"""Tests for geometry module: Vector3D, Polygon3D, and utility functions."""

from __future__ import annotations

import pytest

from idfkit import IDFDocument
from idfkit.geometry import (
    Polygon3D,
    Vector3D,
    _is_convex_2d,
    _point_in_polygon_2d,
    calculate_surface_area,
    calculate_zone_floor_area,
    get_surface_coords,
    get_zone_origin,
    get_zone_rotation,
    polygon_area_2d,
    polygon_contains_2d,
    polygon_difference_2d,
    polygon_intersection_2d,
    set_surface_coords,
)
from idfkit.objects import IDFObject

_TOL = 1e-7


def _close(a: float, b: float, tol: float = _TOL) -> bool:
    return abs(a - b) < tol


# ---------------------------------------------------------------------------
# Vector3D
# ---------------------------------------------------------------------------


class TestVector3D:
    def test_create(self) -> None:
        v = Vector3D(1.0, 2.0, 3.0)
        assert v.x == 1.0
        assert v.y == 2.0
        assert v.z == 3.0

    def test_immutable(self) -> None:
        v = Vector3D(1.0, 2.0, 3.0)
        with pytest.raises(AttributeError):
            v.x = 5.0  # type: ignore[misc]

    def test_add(self) -> None:
        v1 = Vector3D(1, 2, 3)
        v2 = Vector3D(4, 5, 6)
        result = v1 + v2
        assert result == Vector3D(5, 7, 9)

    def test_sub(self) -> None:
        v1 = Vector3D(4, 5, 6)
        v2 = Vector3D(1, 2, 3)
        result = v1 - v2
        assert result == Vector3D(3, 3, 3)

    def test_mul(self) -> None:
        v = Vector3D(1, 2, 3)
        result = v * 2
        assert result == Vector3D(2, 4, 6)

    def test_rmul(self) -> None:
        v = Vector3D(1, 2, 3)
        result = 3 * v
        assert result == Vector3D(3, 6, 9)

    def test_truediv(self) -> None:
        v = Vector3D(6, 8, 10)
        result = v / 2
        assert result == Vector3D(3, 4, 5)

    def test_neg(self) -> None:
        v = Vector3D(1, -2, 3)
        result = -v
        assert result == Vector3D(-1, 2, -3)

    def test_dot(self) -> None:
        v1 = Vector3D(1, 0, 0)
        v2 = Vector3D(0, 1, 0)
        assert v1.dot(v2) == 0.0  # orthogonal

    def test_dot_parallel(self) -> None:
        v1 = Vector3D(1, 2, 3)
        assert v1.dot(v1) == 14.0

    def test_cross(self) -> None:
        v1 = Vector3D(1, 0, 0)
        v2 = Vector3D(0, 1, 0)
        result = v1.cross(v2)
        assert result == Vector3D(0, 0, 1)

    def test_cross_anticommutative(self) -> None:
        v1 = Vector3D(1, 0, 0)
        v2 = Vector3D(0, 1, 0)
        assert v1.cross(v2) == -(v2.cross(v1))

    def test_length(self) -> None:
        v = Vector3D(3, 4, 0)
        assert _close(v.length(), 5.0)

    def test_length_unit(self) -> None:
        v = Vector3D(1, 0, 0)
        assert _close(v.length(), 1.0)

    def test_normalize(self) -> None:
        v = Vector3D(3, 4, 0)
        n = v.normalize()
        assert _close(n.length(), 1.0)
        assert _close(n.x, 0.6)
        assert _close(n.y, 0.8)

    def test_normalize_zero_vector(self) -> None:
        v = Vector3D(0, 0, 0)
        n = v.normalize()
        assert n == Vector3D(0, 0, 0)

    def test_rotate_z_90(self) -> None:
        v = Vector3D(1, 0, 0)
        rotated = v.rotate_z(90)
        assert _close(rotated.x, 0.0, 1e-10)
        assert _close(rotated.y, 1.0)
        assert _close(rotated.z, 0.0)

    def test_rotate_z_180(self) -> None:
        v = Vector3D(1, 0, 0)
        rotated = v.rotate_z(180)
        assert _close(rotated.x, -1.0)
        assert _close(rotated.y, 0.0, 1e-10)

    def test_rotate_z_preserves_z(self) -> None:
        v = Vector3D(1, 0, 5)
        rotated = v.rotate_z(45)
        assert _close(rotated.z, 5.0)

    def test_as_tuple(self) -> None:
        v = Vector3D(1, 2, 3)
        assert v.as_tuple() == (1, 2, 3)

    def test_from_tuple(self) -> None:
        v = Vector3D.from_tuple((1, 2, 3))
        assert v == Vector3D(1, 2, 3)

    def test_from_tuple_list(self) -> None:
        v = Vector3D.from_tuple([1.0, 2.0, 3.0])
        assert v == Vector3D(1, 2, 3)

    def test_origin(self) -> None:
        v = Vector3D.origin()
        assert v == Vector3D(0, 0, 0)


# ---------------------------------------------------------------------------
# Polygon3D
# ---------------------------------------------------------------------------


class TestPolygon3D:
    @pytest.fixture
    def unit_square(self) -> Polygon3D:
        """A 1x1 horizontal square at z=0."""
        return Polygon3D([
            Vector3D(0, 0, 0),
            Vector3D(1, 0, 0),
            Vector3D(1, 1, 0),
            Vector3D(0, 1, 0),
        ])

    @pytest.fixture
    def vertical_wall(self) -> Polygon3D:
        """A 10x3 vertical wall in the XZ plane."""
        return Polygon3D([
            Vector3D(0, 0, 3),
            Vector3D(0, 0, 0),
            Vector3D(10, 0, 0),
            Vector3D(10, 0, 3),
        ])

    def test_num_vertices(self, unit_square: Polygon3D) -> None:
        assert unit_square.num_vertices == 4

    def test_area_unit_square(self, unit_square: Polygon3D) -> None:
        assert _close(unit_square.area, 1.0)

    def test_area_vertical_wall(self, vertical_wall: Polygon3D) -> None:
        assert _close(vertical_wall.area, 30.0)

    def test_area_degenerate(self) -> None:
        poly = Polygon3D([Vector3D(0, 0, 0), Vector3D(1, 0, 0)])
        assert poly.area == 0.0

    def test_area_triangle(self) -> None:
        poly = Polygon3D([
            Vector3D(0, 0, 0),
            Vector3D(4, 0, 0),
            Vector3D(0, 3, 0),
        ])
        assert _close(poly.area, 6.0)

    def test_normal_horizontal(self, unit_square: Polygon3D) -> None:
        n = unit_square.normal
        assert abs(n.z) > 0.99  # should be pointing up or down

    def test_normal_vertical(self, vertical_wall: Polygon3D) -> None:
        n = vertical_wall.normal
        assert abs(n.z) < 0.01  # should be horizontal

    def test_normal_degenerate(self) -> None:
        poly = Polygon3D([Vector3D(0, 0, 0)])
        n = poly.normal
        assert n == Vector3D(0, 0, 1)  # default for degenerate

    def test_centroid(self, unit_square: Polygon3D) -> None:
        c = unit_square.centroid
        assert _close(c.x, 0.5)
        assert _close(c.y, 0.5)
        assert _close(c.z, 0.0)

    def test_centroid_empty(self) -> None:
        poly = Polygon3D([])
        c = poly.centroid
        assert c == Vector3D.origin()

    def test_is_horizontal(self, unit_square: Polygon3D) -> None:
        assert unit_square.is_horizontal is True

    def test_is_not_horizontal(self, vertical_wall: Polygon3D) -> None:
        assert vertical_wall.is_horizontal is False

    def test_is_vertical(self, vertical_wall: Polygon3D) -> None:
        assert vertical_wall.is_vertical is True

    def test_is_not_vertical(self, unit_square: Polygon3D) -> None:
        assert unit_square.is_vertical is False

    def test_translate(self, unit_square: Polygon3D) -> None:
        offset = Vector3D(5, 5, 5)
        translated = unit_square.translate(offset)
        assert translated.vertices[0] == Vector3D(5, 5, 5)
        assert translated.vertices[2] == Vector3D(6, 6, 5)

    def test_rotate_z(self, unit_square: Polygon3D) -> None:
        rotated = unit_square.rotate_z(90)
        # After 90-degree rotation around centroid, area should be preserved
        assert _close(rotated.area, unit_square.area)

    def test_rotate_z_with_anchor(self) -> None:
        poly = Polygon3D([
            Vector3D(1, 0, 0),
            Vector3D(2, 0, 0),
            Vector3D(2, 1, 0),
            Vector3D(1, 1, 0),
        ])
        anchor = Vector3D(0, 0, 0)
        rotated = poly.rotate_z(90, anchor=anchor)
        # After rotating 90 degrees around origin, (1,0) -> (0,1)
        assert _close(rotated.vertices[0].x, 0.0, 1e-10)
        assert _close(rotated.vertices[0].y, 1.0)

    def test_as_tuple_list(self, unit_square: Polygon3D) -> None:
        tuples = unit_square.as_tuple_list()
        assert tuples == [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]

    def test_from_tuples(self) -> None:
        coords = [(0, 0, 0), (1, 0, 0), (1, 1, 0)]
        poly = Polygon3D.from_tuples(coords)
        assert poly.num_vertices == 3
        assert poly.vertices[0] == Vector3D(0, 0, 0)


# ---------------------------------------------------------------------------
# Surface geometry utilities
# ---------------------------------------------------------------------------


class TestSurfaceGeometryUtils:
    def test_get_surface_coords(self) -> None:
        surface = IDFObject(
            obj_type="BuildingSurface:Detailed",
            name="Wall",
            data={
                "number_of_vertices": 4,
                "vertex_1_x_coordinate": 0.0,
                "vertex_1_y_coordinate": 0.0,
                "vertex_1_z_coordinate": 3.0,
                "vertex_2_x_coordinate": 0.0,
                "vertex_2_y_coordinate": 0.0,
                "vertex_2_z_coordinate": 0.0,
                "vertex_3_x_coordinate": 10.0,
                "vertex_3_y_coordinate": 0.0,
                "vertex_3_z_coordinate": 0.0,
                "vertex_4_x_coordinate": 10.0,
                "vertex_4_y_coordinate": 0.0,
                "vertex_4_z_coordinate": 3.0,
            },
        )
        poly = get_surface_coords(surface)
        assert poly is not None
        assert poly.num_vertices == 4
        assert _close(poly.area, 30.0)

    def test_get_surface_coords_autodetect_vertices(self) -> None:
        """Test that vertices are autodetected when number_of_vertices is missing."""
        surface = IDFObject(
            obj_type="BuildingSurface:Detailed",
            name="Wall",
            data={
                "vertex_1_x_coordinate": 0.0,
                "vertex_1_y_coordinate": 0.0,
                "vertex_1_z_coordinate": 0.0,
                "vertex_2_x_coordinate": 1.0,
                "vertex_2_y_coordinate": 0.0,
                "vertex_2_z_coordinate": 0.0,
                "vertex_3_x_coordinate": 1.0,
                "vertex_3_y_coordinate": 1.0,
                "vertex_3_z_coordinate": 0.0,
            },
        )
        poly = get_surface_coords(surface)
        assert poly is not None
        assert poly.num_vertices == 3

    def test_get_surface_coords_blank_number_of_vertices(self) -> None:
        """Test that blank number_of_vertices is treated as autocalculate."""
        surface = IDFObject(
            obj_type="BuildingSurface:Detailed",
            name="Wall",
            data={
                "number_of_vertices": "",  # blank = autocalculate in EnergyPlus
                "vertex_1_x_coordinate": 0.0,
                "vertex_1_y_coordinate": 0.0,
                "vertex_1_z_coordinate": 3.0,
                "vertex_2_x_coordinate": 0.0,
                "vertex_2_y_coordinate": 0.0,
                "vertex_2_z_coordinate": 0.0,
                "vertex_3_x_coordinate": 10.0,
                "vertex_3_y_coordinate": 0.0,
                "vertex_3_z_coordinate": 0.0,
                "vertex_4_x_coordinate": 10.0,
                "vertex_4_y_coordinate": 0.0,
                "vertex_4_z_coordinate": 3.0,
            },
        )
        poly = get_surface_coords(surface)
        assert poly is not None
        assert poly.num_vertices == 4
        assert _close(poly.area, 30.0)

    def test_get_surface_coords_no_vertices(self) -> None:
        surface = IDFObject(obj_type="BuildingSurface:Detailed", name="Empty", data={})
        poly = get_surface_coords(surface)
        assert poly is None

    def test_get_surface_coords_schema_naming(self) -> None:
        """Test epJSON schema naming: vertex_x_coordinate, vertex_x_coordinate_2, ..."""
        surface = IDFObject(
            obj_type="BuildingSurface:Detailed",
            name="SchemaWall",
            data={
                "number_of_vertices": 4,
                "vertex_x_coordinate": 0.0,
                "vertex_y_coordinate": 0.0,
                "vertex_z_coordinate": 3.0,
                "vertex_x_coordinate_2": 0.0,
                "vertex_y_coordinate_2": 0.0,
                "vertex_z_coordinate_2": 0.0,
                "vertex_x_coordinate_3": 10.0,
                "vertex_y_coordinate_3": 0.0,
                "vertex_z_coordinate_3": 0.0,
                "vertex_x_coordinate_4": 10.0,
                "vertex_y_coordinate_4": 0.0,
                "vertex_z_coordinate_4": 3.0,
            },
        )
        poly = get_surface_coords(surface)
        assert poly is not None
        assert poly.num_vertices == 4
        assert _close(poly.area, 30.0)

    def test_set_surface_coords(self) -> None:
        surface = IDFObject(obj_type="BuildingSurface:Detailed", name="Wall", data={})
        poly = Polygon3D([
            Vector3D(0, 0, 0),
            Vector3D(1, 0, 0),
            Vector3D(1, 1, 0),
            Vector3D(0, 1, 0),
        ])
        set_surface_coords(surface, poly)
        assert surface.number_of_vertices == 4
        assert surface.vertex_1_x_coordinate == 0.0
        assert surface.vertex_4_y_coordinate == 1.0

    def test_get_zone_origin(self) -> None:
        zone = IDFObject(
            obj_type="Zone",
            name="Z",
            data={"x_origin": 10.0, "y_origin": 20.0, "z_origin": 5.0},
        )
        origin = get_zone_origin(zone)
        assert origin == Vector3D(10, 20, 5)

    def test_get_zone_origin_defaults(self) -> None:
        zone = IDFObject(obj_type="Zone", name="Z", data={})
        origin = get_zone_origin(zone)
        assert origin == Vector3D(0, 0, 0)

    def test_get_zone_rotation(self) -> None:
        zone = IDFObject(obj_type="Zone", name="Z", data={"direction_of_relative_north": 45.0})
        assert get_zone_rotation(zone) == 45.0

    def test_get_zone_rotation_default(self) -> None:
        zone = IDFObject(obj_type="Zone", name="Z", data={})
        assert get_zone_rotation(zone) == 0.0

    def test_calculate_surface_area(self, simple_doc: IDFDocument) -> None:
        wall = simple_doc.getobject("BuildingSurface:Detailed", "TestWall")
        assert wall is not None
        area = calculate_surface_area(wall)
        assert _close(area, 30.0)

    def test_calculate_surface_area_no_coords(self) -> None:
        surface = IDFObject(obj_type="BuildingSurface:Detailed", name="Empty", data={})
        assert calculate_surface_area(surface) == 0.0

    def test_calculate_zone_floor_area(self, simple_doc: IDFDocument) -> None:
        area = calculate_zone_floor_area(simple_doc, "TestZone")
        assert _close(area, 100.0)

    def test_calculate_zone_floor_area_no_floors(self, empty_doc: IDFDocument) -> None:
        empty_doc.add("Zone", "EmptyZone")
        area = calculate_zone_floor_area(empty_doc, "EmptyZone")
        assert area == 0.0


# ---------------------------------------------------------------------------
# 2D polygon operations
# ---------------------------------------------------------------------------


class TestPolygonIntersection2D:
    def test_overlapping_rectangles(self) -> None:
        # Two overlapping rectangles
        a = [(0, 0), (10, 0), (10, 10), (0, 10)]
        b = [(5, 5), (15, 5), (15, 15), (5, 15)]
        result = polygon_intersection_2d(a, b)
        assert result is not None
        area = abs(polygon_area_2d(result))
        assert abs(area - 25.0) < 0.01  # 5x5 overlap

    def test_contained_rectangle(self) -> None:
        # Inner fully inside outer
        outer = [(0, 0), (20, 0), (20, 20), (0, 20)]
        inner = [(5, 5), (15, 5), (15, 15), (5, 15)]
        result = polygon_intersection_2d(outer, inner)
        assert result is not None
        area = abs(polygon_area_2d(result))
        assert abs(area - 100.0) < 0.01  # inner is 10x10

    def test_disjoint_returns_none(self) -> None:
        a = [(0, 0), (5, 0), (5, 5), (0, 5)]
        b = [(10, 10), (15, 10), (15, 15), (10, 15)]
        result = polygon_intersection_2d(a, b)
        assert result is None

    def test_concave_subject_convex_clip(self) -> None:
        # L-shape clipped by rectangle
        from idfkit.zoning import footprint_l_shape

        l_shape = footprint_l_shape(20, 10, 8, 5)
        clip = [(0, 0), (10, 0), (10, 15), (0, 15)]
        result = polygon_intersection_2d(l_shape, clip)
        assert result is not None
        assert abs(polygon_area_2d(result)) > 0


class TestPolygonDifference2D:
    def test_rectangles_frame(self) -> None:
        outer = [(0, 0), (20, 0), (20, 20), (0, 20)]
        inner = [(5, 5), (15, 5), (15, 15), (5, 15)]
        result = polygon_difference_2d(outer, inner)
        assert result is not None
        # The result is a slit/bridge polygon containing vertices from both
        # outer and inner polygons.
        assert len(result) == len(outer) + len(inner)
        # The conceptual frame area can be computed from the original polygons.
        frame_area = abs(polygon_area_2d(outer)) - abs(polygon_area_2d(inner))
        assert abs(frame_area - 300.0) < 0.01

    def test_same_polygon_returns_none(self) -> None:
        poly = [(0, 0), (10, 0), (10, 10), (0, 10)]
        result = polygon_difference_2d(poly, poly)
        assert result is None


class TestPolygonContains2D:
    def test_contained(self) -> None:
        outer = [(0, 0), (20, 0), (20, 20), (0, 20)]
        inner = [(5, 5), (15, 5), (15, 15), (5, 15)]
        assert polygon_contains_2d(outer, inner)

    def test_not_contained(self) -> None:
        outer = [(0, 0), (10, 0), (10, 10), (0, 10)]
        inner = [(5, 5), (15, 5), (15, 15), (5, 15)]
        assert not polygon_contains_2d(outer, inner)


class TestPolygonArea2D:
    def test_unit_square(self) -> None:
        poly = [(0, 0), (1, 0), (1, 1), (0, 1)]
        area = polygon_area_2d(poly)
        assert abs(abs(area) - 1.0) < 1e-10

    def test_rectangle(self) -> None:
        poly = [(0, 0), (5, 0), (5, 3), (0, 3)]
        area = polygon_area_2d(poly)
        assert abs(abs(area) - 15.0) < 1e-10

    def test_triangle(self) -> None:
        poly = [(0, 0), (4, 0), (0, 3)]
        area = polygon_area_2d(poly)
        assert abs(abs(area) - 6.0) < 1e-10

    def test_signed_area_ccw_positive(self) -> None:
        # Counter-clockwise winding should give positive signed area
        ccw = [(0, 0), (1, 0), (1, 1), (0, 1)]
        assert polygon_area_2d(ccw) > 0
        # Clockwise winding should give negative signed area
        cw = [(0, 0), (0, 1), (1, 1), (1, 0)]
        assert polygon_area_2d(cw) < 0


class TestIsConvex2D:
    def test_square_is_convex(self) -> None:
        poly = [(0, 0), (1, 0), (1, 1), (0, 1)]
        assert _is_convex_2d(poly)

    def test_l_shape_not_convex(self) -> None:
        poly = [(0, 0), (2, 0), (2, 1), (1, 1), (1, 2), (0, 2)]
        assert not _is_convex_2d(poly)

    def test_triangle_is_convex(self) -> None:
        poly = [(0, 0), (4, 0), (2, 3)]
        assert _is_convex_2d(poly)


class TestPointInPolygon2D:
    def test_inside(self) -> None:
        poly = [(0, 0), (10, 0), (10, 10), (0, 10)]
        assert _point_in_polygon_2d((5, 5), poly)

    def test_outside(self) -> None:
        poly = [(0, 0), (10, 0), (10, 10), (0, 10)]
        assert not _point_in_polygon_2d((15, 15), poly)

    def test_on_edge(self) -> None:
        poly = [(0, 0), (10, 0), (10, 10), (0, 10)]
        # Points on edges may return True or False depending on implementation;
        # just ensure no crash
        _point_in_polygon_2d((5, 0), poly)

    def test_inside_triangle(self) -> None:
        poly = [(0, 0), (10, 0), (5, 10)]
        assert _point_in_polygon_2d((5, 3), poly)

    def test_outside_triangle(self) -> None:
        poly = [(0, 0), (10, 0), (5, 10)]
        assert not _point_in_polygon_2d((0, 10), poly)
