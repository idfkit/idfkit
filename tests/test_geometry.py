"""Tests for geometry module: Vector3D, Polygon3D, and utility functions."""

from __future__ import annotations

import math

import pytest

from idfkit import IDFDocument, new_document
from idfkit.geometry import (
    Polygon3D,
    Vector3D,
    _inset_polygon,  # pyright: ignore[reportPrivateUsage]
    _orientation_to_azimuth,  # pyright: ignore[reportPrivateUsage]
    _point_in_polygon_2d,  # pyright: ignore[reportPrivateUsage]
    _sutherland_hodgman,  # pyright: ignore[reportPrivateUsage]
    _wall_matches,  # pyright: ignore[reportPrivateUsage]
    calculate_surface_area,
    calculate_surface_azimuth,
    calculate_surface_tilt,
    calculate_zone_ceiling_area,
    calculate_zone_floor_area,
    calculate_zone_height,
    calculate_zone_volume,
    get_surface_coords,
    get_zone_origin,
    get_zone_rotation,
    intersect_match,
    is_convex_2d,
    line_intersect_2d,
    polygon_area_2d,
    polygon_contains_2d,
    polygon_difference_2d,
    polygon_difference_parts_2d,
    polygon_intersection_2d,
    rotate_building,
    set_surface_coords,
    set_wwr,
    translate_building,
    translate_to_world,
    triangulate_2d,
)
from idfkit.objects import IDFObject
from idfkit.schema import get_schema

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
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                ],
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
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 1.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 1.0, "vertex_y_coordinate": 1.0, "vertex_z_coordinate": 0.0},
                ],
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
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                ],
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

    def test_get_surface_coords_canonical_storage(self) -> None:
        """Test canonical storage: obj.data["vertices"] is a list of dicts."""
        surface = IDFObject(
            obj_type="BuildingSurface:Detailed",
            name="SchemaWall",
            data={
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                ],
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
        # No document attached, so set_surface_coords falls back to flat fields
        assert surface.data["vertex_1_x_coordinate"] == 0.0
        assert surface.data["vertex_4_y_coordinate"] == 1.0

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


def _assert_clean_ring(poly: list[tuple[float, float]]) -> None:
    """A ring EnergyPlus accepts: CCW, no repeated vertices, no zero-length or self-crossing edges."""
    assert len(poly) >= 3
    assert polygon_area_2d(poly) > 0
    n = len(poly)
    for i in range(n):
        for j in range(i + 1, n):
            assert math.dist(poly[i], poly[j]) > 1e-6, f"coincident vertices {poly[i]} at {i} and {j}"
    for i in range(n):
        a1, a2 = poly[i], poly[(i + 1) % n]
        for j in range(i + 2, n):
            if i == 0 and j == n - 1:
                continue
            b1, b2 = poly[j], poly[(j + 1) % n]

            def orient(p: tuple[float, float], q: tuple[float, float], r: tuple[float, float]) -> float:
                return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

            crosses = orient(a1, a2, b1) * orient(a1, a2, b2) < 0 and orient(b1, b2, a1) * orient(b1, b2, a2) < 0
            assert not crosses, f"edges {i} and {j} cross"


class TestPolygonDifference2D:
    def test_interior_hole_raises(self) -> None:
        """Issue #164 repro 1: a fully interior cut-out cannot be one simple ring."""
        from idfkit.zoning import footprint_rectangle

        fp = footprint_rectangle(105, 60)
        island = footprint_rectangle(40, 25, origin=(35, 20))
        with pytest.raises(ValueError, match="polygon_difference_parts_2d"):
            polygon_difference_2d(fp, island)

    def test_chained_corner_cuts_are_clean(self) -> None:
        """Issue #164 repro 2: corner cut-outs give a clean ring with the right area."""
        from idfkit.zoning import footprint_rectangle

        fp = footprint_rectangle(105, 60)
        office = footprint_rectangle(33.3, 9.0, origin=(0, 0))
        robot = footprint_rectangle(47.2, 25.4, origin=(57.8, 34.6))
        step = polygon_difference_2d(fp, office)
        assert step is not None
        wh = polygon_difference_2d(step, robot)
        assert wh is not None
        _assert_clean_ring(wh)
        assert len(wh) == 8
        assert polygon_area_2d(wh) == pytest.approx(105 * 60 - 33.3 * 9.0 - 47.2 * 25.4)

    def test_chained_corner_cuts_build_valid_block(self) -> None:
        """The cleaned footprint builds surfaces with no degenerate vertices."""
        from idfkit.zoning import create_block, footprint_rectangle

        fp = footprint_rectangle(105, 60)
        step = polygon_difference_2d(fp, footprint_rectangle(33.3, 9.0))
        assert step is not None
        wh = polygon_difference_2d(step, footprint_rectangle(47.2, 25.4, origin=(57.8, 34.6)))
        assert wh is not None
        doc = new_document()
        create_block(doc, "WH", wh, 6.0)
        for srf in doc["BuildingSurface:Detailed"]:
            coords = get_surface_coords(srf)
            assert coords is not None
            verts = coords.vertices
            assert calculate_surface_area(srf) > 1.0
            for i in range(len(verts)):
                for j in range(i + 1, len(verts)):
                    assert (verts[i] - verts[j]).length() > 1e-6

    def test_edge_notch(self) -> None:
        outer = [(0, 0), (10, 0), (10, 10), (0, 10)]
        notch = [(4, 8), (6, 8), (6, 10), (4, 10)]
        result = polygon_difference_2d(outer, notch)
        assert result == [(0, 0), (10, 0), (10, 10), (6, 10), (6, 8), (4, 8), (4, 10), (0, 10)]

    def test_partial_overlap(self) -> None:
        a = [(0, 0), (10, 0), (10, 5), (0, 5)]
        b = [(5, 0), (15, 0), (15, 5), (5, 5)]
        assert polygon_difference_2d(a, b) == [(0, 0), (5, 0), (5, 5), (0, 5)]

    def test_inner_extends_past_outer(self) -> None:
        outer = [(0, 0), (10, 0), (10, 10), (0, 10)]
        inner = [(8, -2), (12, -2), (12, 3), (8, 3)]
        result = polygon_difference_2d(outer, inner)
        assert result is not None
        _assert_clean_ring(result)
        assert polygon_area_2d(result) == pytest.approx(100 - 2 * 3)

    def test_disjoint_returns_outer(self) -> None:
        outer = [(0, 0), (10, 0), (10, 10), (0, 10)]
        assert polygon_difference_2d(outer, [(20, 20), (30, 20), (30, 30), (20, 30)]) == outer

    def test_clockwise_inputs(self) -> None:
        outer = [(0, 10), (10, 10), (10, 0), (0, 0)]
        corner = [(0, 5), (5, 5), (5, 0), (0, 0)]
        result = polygon_difference_2d(outer, corner)
        assert result is not None
        _assert_clean_ring(result)
        assert polygon_area_2d(result) == pytest.approx(75.0)

    def test_split_in_two_raises(self) -> None:
        outer = [(0, 0), (10, 0), (10, 5), (0, 5)]
        strip = [(4, -1), (6, -1), (6, 6), (4, 6)]
        with pytest.raises(ValueError, match="2 separate polygons"):
            polygon_difference_2d(outer, strip)

    def test_same_polygon_returns_none(self) -> None:
        poly = [(0, 0), (10, 0), (10, 10), (0, 10)]
        result = polygon_difference_2d(poly, poly)
        assert result is None

    def test_covering_inner_returns_none(self) -> None:
        poly = [(0, 0), (10, 0), (10, 10), (0, 10)]
        assert polygon_difference_2d(poly, [(-1, -1), (11, -1), (11, 11), (-1, 11)]) is None


class TestPolygonDifferenceParts2D:
    def test_interior_hole_pieces(self) -> None:
        """Issue #164 repro 1: the pieces cover the right area and are hole-free."""
        from idfkit.zoning import footprint_rectangle

        fp = footprint_rectangle(105, 60)
        island = footprint_rectangle(40, 25, origin=(35, 20))
        parts = polygon_difference_parts_2d(fp, island)
        assert len(parts) == 2
        for part in parts:
            _assert_clean_ring(part)
        assert sum(polygon_area_2d(p) for p in parts) == pytest.approx(5300.0)
        # Pieces do not overlap each other or the island.
        assert polygon_intersection_2d(island, parts[0]) is None
        assert polygon_intersection_2d(island, parts[1]) is None

    def test_rectangles_frame(self) -> None:
        outer = [(0, 0), (20, 0), (20, 20), (0, 20)]
        inner = [(5, 5), (15, 5), (15, 15), (5, 15)]
        parts = polygon_difference_parts_2d(outer, inner)
        assert sum(polygon_area_2d(p) for p in parts) == pytest.approx(300.0)
        for part in parts:
            _assert_clean_ring(part)

    def test_hole_free_result_is_one_piece(self) -> None:
        outer = [(0, 0), (10, 0), (10, 10), (0, 10)]
        corner = [(5, 5), (10, 5), (10, 10), (5, 10)]
        assert polygon_difference_parts_2d(outer, corner) == [polygon_difference_2d(outer, corner)]

    def test_multiple_inners(self) -> None:
        from idfkit.zoning import footprint_rectangle

        fp = footprint_rectangle(105, 60)
        office = footprint_rectangle(33.3, 9.0)
        robot = footprint_rectangle(47.2, 25.4, origin=(57.8, 34.6))
        parts = polygon_difference_parts_2d(fp, office, robot)
        assert len(parts) == 1
        _assert_clean_ring(parts[0])
        assert polygon_area_2d(parts[0]) == pytest.approx(105 * 60 - 33.3 * 9.0 - 47.2 * 25.4)

    def test_overlapping_inners(self) -> None:
        outer = [(0, 0), (10, 0), (10, 10), (0, 10)]
        a = [(2, 2), (6, 2), (6, 6), (2, 6)]
        b = [(4, 4), (8, 4), (8, 8), (4, 8)]
        parts = polygon_difference_parts_2d(outer, a, b)
        for part in parts:
            _assert_clean_ring(part)
        assert sum(polygon_area_2d(p) for p in parts) == pytest.approx(100 - (16 + 16 - 4))

    def test_two_holes(self) -> None:
        outer = [(0, 0), (30, 0), (30, 10), (0, 10)]
        h1 = [(2, 2), (8, 2), (8, 8), (2, 8)]
        h2 = [(20, 3), (25, 3), (25, 7), (20, 7)]
        parts = polygon_difference_parts_2d(outer, h1, h2)
        for part in parts:
            _assert_clean_ring(part)
        assert sum(polygon_area_2d(p) for p in parts) == pytest.approx(300 - 36 - 20)

    def test_split_in_two(self) -> None:
        outer = [(0, 0), (10, 0), (10, 5), (0, 5)]
        strip = [(4, -1), (6, -1), (6, 6), (4, 6)]
        parts = polygon_difference_parts_2d(outer, strip)
        assert sorted(sorted(p) for p in parts) == [
            [(0, 0), (0, 5), (4.0, 0.0), (4.0, 5.0)],
            [(6.0, 0.0), (6.0, 5.0), (10, 0), (10, 5)],
        ]

    def test_hole_touching_boundary_at_a_point(self) -> None:
        outer = [(0, 0), (10, 0), (10, 10), (0, 10)]
        diamond = [(5, 0), (6, 1), (5, 2), (4, 1)]
        parts = polygon_difference_parts_2d(outer, diamond)
        for part in parts:
            _assert_clean_ring(part)
        assert sum(polygon_area_2d(p) for p in parts) == pytest.approx(98.0)

    def test_concave_outer(self) -> None:
        from idfkit.zoning import footprint_l_shape

        l_shape = footprint_l_shape(20, 10, 8, 5)
        hole = [(2, 2), (4, 2), (4, 4), (2, 4)]
        parts = polygon_difference_parts_2d(l_shape, hole)
        for part in parts:
            _assert_clean_ring(part)
        assert sum(polygon_area_2d(p) for p in parts) == pytest.approx(polygon_area_2d(l_shape) - 4)

    def test_nothing_left(self) -> None:
        poly = [(0, 0), (10, 0), (10, 10), (0, 10)]
        assert polygon_difference_parts_2d(poly, poly) == []

    def test_no_inners_returns_outer(self) -> None:
        poly = [(0, 0), (10, 0), (10, 10), (0, 10)]
        assert polygon_difference_parts_2d(poly) == [poly]

    @pytest.mark.parametrize("gap", [1e-6, 1e-5])
    def test_thin_strip_below_probe_distance_survives(self, gap: float) -> None:
        """A strip thinner than the side-probe distance must not wipe out the whole result."""
        outer = [(0, 0), (100, 0), (100, 100), (0, 100)]
        inner = [(10, gap), (110, gap), (110, 110), (10, 110)]
        parts = polygon_difference_parts_2d(outer, inner)
        assert len(parts) == 1
        assert polygon_area_2d(parts[0]) == pytest.approx(10 * 100 + 90 * gap)

    def test_far_away_inner_does_not_inflate_tolerance(self) -> None:
        outer = [(0, 0), (10, 0), (10, 10), (0, 10)]
        far = [(1e6, 0), (1e6 + 1, 0), (1e6 + 1, 1), (1e6, 1)]
        assert polygon_difference_parts_2d(outer, far) == [outer]

    def test_degenerate_outer(self) -> None:
        assert polygon_difference_parts_2d([(0, 0), (1, 1)], [(0, 0), (1, 0), (1, 1)]) == []
        assert polygon_difference_parts_2d([(0, 0), (0, 0), (0, 0)]) == []

    def test_nearly_aligned_holes_share_one_cut(self) -> None:
        """Two holes whose middles are 1 cm apart get one cut, not two that leave slivers."""
        from idfkit.zoning import footprint_rectangle

        outer = footprint_rectangle(60, 40)
        a = footprint_rectangle(10, 10, origin=(5, 5))
        b = footprint_rectangle(10, 10, origin=(5.01, 20))
        parts = polygon_difference_parts_2d(outer, a, b)
        assert len(parts) == 2
        assert min(polygon_area_2d(p) for p in parts) > 1.0
        assert math.isclose(sum(polygon_area_2d(p) for p in parts), 2400 - 200)

    def test_one_cut_crossing_several_holes(self) -> None:
        """A cut through the largest hole also opens every hole whose x-range it crosses."""
        from idfkit.zoning import footprint_rectangle

        outer = footprint_rectangle(60, 40)
        big = footprint_rectangle(20, 8, origin=(10, 4))  # cut at x = 20
        small = footprint_rectangle(6, 6, origin=(16, 24))  # spans x 16..22
        parts = polygon_difference_parts_2d(outer, small, big)
        assert len(parts) == 2
        xs = {x for p in parts for x, _ in p}
        assert 20.0 in xs
        assert 19.0 not in xs  # the small hole's own middle is not cut

    def test_holes_apart_in_x_get_their_own_cuts(self) -> None:
        from idfkit.zoning import footprint_rectangle

        outer = footprint_rectangle(60, 40)
        a = footprint_rectangle(10, 10, origin=(5, 5))
        b = footprint_rectangle(10, 10, origin=(40, 20))
        parts = polygon_difference_parts_2d(outer, a, b)
        assert len(parts) == 3
        assert math.isclose(sum(polygon_area_2d(p) for p in parts), 2400 - 200)
        for p in parts:
            assert polygon_area_2d(p) > 0
            assert len(set(p)) == len(p)


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
        assert is_convex_2d(poly)

    def test_l_shape_not_convex(self) -> None:
        poly = [(0, 0), (2, 0), (2, 1), (1, 1), (1, 2), (0, 2)]
        assert not is_convex_2d(poly)

    def test_triangle_is_convex(self) -> None:
        poly = [(0, 0), (4, 0), (2, 3)]
        assert is_convex_2d(poly)


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


# ---------------------------------------------------------------------------
# translate_to_world
# ---------------------------------------------------------------------------


class TestTranslateToWorld:
    def test_already_world_coordinates(self, simple_doc: IDFDocument) -> None:
        """When coordinate_system is 'World', translate_to_world should be a no-op."""
        rules = simple_doc["GlobalGeometryRules"].first()
        assert rules is not None
        rules.coordinate_system = "World"
        wall = simple_doc.getobject("BuildingSurface:Detailed", "TestWall")
        assert wall is not None
        orig_x = wall.vertices[0].vertex_x_coordinate
        translate_to_world(simple_doc)
        assert wall.vertices[0].vertex_x_coordinate == orig_x

    def test_relative_coordinates_with_zone_origin(self) -> None:
        """Translate relative coordinates with zone origin offset."""
        doc = new_document(version=(24, 1, 0))
        rules = doc["GlobalGeometryRules"].first()
        assert rules is not None
        rules.coordinate_system = "Relative"
        bldg = doc["Building"].first()
        assert bldg is not None
        bldg.north_axis = 0.0
        doc.add("Zone", "Office", {"x_origin": 10.0, "y_origin": 20.0, "z_origin": 0.0})
        doc.add(
            "BuildingSurface:Detailed",
            "OfficeWall",
            {
                "surface_type": "Wall",
                "zone_name": "Office",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 5.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 5.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                ],
            },
            validate=False,
        )
        translate_to_world(doc)
        wall = doc.getobject("BuildingSurface:Detailed", "OfficeWall")
        assert wall is not None
        # vertex 1 was (0, 0, 3) -> translated by (10, 20, 0)
        v0 = wall.vertices[0]
        assert _close(v0.vertex_x_coordinate, 10.0)
        assert _close(v0.vertex_y_coordinate, 20.0)
        # Zone origins reset to 0
        zone = doc.getobject("Zone", "Office")
        assert zone is not None
        assert zone.x_origin == 0.0
        assert zone.y_origin == 0.0
        assert zone.z_origin == 0.0
        assert zone.direction_of_relative_north == 0.0
        # Building north axis reset
        assert bldg.north_axis == 0.0
        # Coordinate system updated to World
        assert rules.coordinate_system == "World"

    def test_relative_coordinates_with_rotation(self) -> None:
        """Zone rotation is applied before translation."""
        doc = new_document(version=(24, 1, 0))
        rules = doc["GlobalGeometryRules"].first()
        assert rules is not None
        rules.coordinate_system = "Relative"
        bldg = doc["Building"].first()
        assert bldg is not None
        bldg.north_axis = 90.0
        doc.add("Zone", "Rotated", {"x_origin": 0.0, "y_origin": 0.0, "z_origin": 0.0})
        doc.add(
            "BuildingSurface:Detailed",
            "RotWall",
            {
                "surface_type": "Wall",
                "zone_name": "Rotated",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 1.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 1.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                ],
            },
            validate=False,
        )
        translate_to_world(doc)
        wall = doc.getobject("BuildingSurface:Detailed", "RotWall")
        assert wall is not None
        # After rotation, coordinates should have changed from original
        # The exact values depend on rotation around polygon centroid
        assert wall.vertices[0].vertex_x_coordinate != 1.0 or wall.vertices[0].vertex_y_coordinate != 0.0

    def test_no_geometry_rules(self) -> None:
        """No GlobalGeometryRules present -- should process surfaces."""
        doc = IDFDocument(version=(24, 1, 0), schema=get_schema((24, 1, 0)))
        doc.add("Zone", "Z1", {"x_origin": 5.0, "y_origin": 5.0, "z_origin": 0.0})
        doc.add(
            "BuildingSurface:Detailed",
            "W1",
            {
                "surface_type": "Wall",
                "zone_name": "Z1",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 3,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 1.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 1.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 1.0},
                ],
            },
            validate=False,
        )
        translate_to_world(doc)
        wall = doc.getobject("BuildingSurface:Detailed", "W1")
        assert wall is not None
        assert _close(wall.vertices[0].vertex_x_coordinate, 5.0)

    def test_surface_without_coords_skipped(self) -> None:
        """Surfaces with no vertex data are skipped gracefully."""
        doc = new_document(version=(24, 1, 0))
        rules = doc["GlobalGeometryRules"].first()
        assert rules is not None
        rules.coordinate_system = "Relative"
        doc.add("Zone", "Z1", {"x_origin": 5.0, "y_origin": 0.0, "z_origin": 0.0})
        # A surface referencing the zone but with no vertex data
        doc.add(
            "BuildingSurface:Detailed",
            "NoCoords",
            {"surface_type": "Wall", "zone_name": "Z1", "outside_boundary_condition": "Outdoors"},
            validate=False,
        )
        # Should not raise
        translate_to_world(doc)


# ---------------------------------------------------------------------------
# calculate_zone_ceiling_area & calculate_zone_height
# ---------------------------------------------------------------------------


class TestZoneCeilingAndHeight:
    def test_calculate_zone_ceiling_area(self) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Office", {})
        doc.add(
            "BuildingSurface:Detailed",
            "Ceiling1",
            {
                "surface_type": "Ceiling",
                "zone_name": "Office",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0, "vertex_y_coordinate": 0, "vertex_z_coordinate": 3},
                    {"vertex_x_coordinate": 0, "vertex_y_coordinate": 5, "vertex_z_coordinate": 3},
                    {"vertex_x_coordinate": 4, "vertex_y_coordinate": 5, "vertex_z_coordinate": 3},
                    {"vertex_x_coordinate": 4, "vertex_y_coordinate": 0, "vertex_z_coordinate": 3},
                ],
            },
            validate=False,
        )
        area = calculate_zone_ceiling_area(doc, "Office")
        assert _close(area, 20.0)

    def test_calculate_zone_ceiling_area_with_non_ceiling(self) -> None:
        """Non-ceiling surfaces in the same zone are skipped when summing ceiling area."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Office", {})
        # A wall (not ceiling) in the same zone
        doc.add(
            "BuildingSurface:Detailed",
            "Wall1",
            {
                "surface_type": "Wall",
                "zone_name": "Office",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0, "vertex_y_coordinate": 0, "vertex_z_coordinate": 3},
                    {"vertex_x_coordinate": 0, "vertex_y_coordinate": 0, "vertex_z_coordinate": 0},
                    {"vertex_x_coordinate": 10, "vertex_y_coordinate": 0, "vertex_z_coordinate": 0},
                    {"vertex_x_coordinate": 10, "vertex_y_coordinate": 0, "vertex_z_coordinate": 3},
                ],
            },
            validate=False,
        )
        # A ceiling in the same zone
        doc.add(
            "BuildingSurface:Detailed",
            "Ceil1",
            {
                "surface_type": "Ceiling",
                "zone_name": "Office",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0, "vertex_y_coordinate": 0, "vertex_z_coordinate": 3},
                    {"vertex_x_coordinate": 0, "vertex_y_coordinate": 5, "vertex_z_coordinate": 3},
                    {"vertex_x_coordinate": 4, "vertex_y_coordinate": 5, "vertex_z_coordinate": 3},
                    {"vertex_x_coordinate": 4, "vertex_y_coordinate": 0, "vertex_z_coordinate": 3},
                ],
            },
            validate=False,
        )
        area = calculate_zone_ceiling_area(doc, "Office")
        assert _close(area, 20.0)  # Only the ceiling, not the wall

    def test_calculate_zone_ceiling_area_wrong_zone(self) -> None:
        """Surfaces in other zones are excluded when calculating ceiling area."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "A", {})
        doc.add("Zone", "B", {})
        doc.add(
            "BuildingSurface:Detailed",
            "CeilA",
            {
                "surface_type": "Ceiling",
                "zone_name": "A",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0, "vertex_y_coordinate": 0, "vertex_z_coordinate": 3},
                    {"vertex_x_coordinate": 0, "vertex_y_coordinate": 5, "vertex_z_coordinate": 3},
                    {"vertex_x_coordinate": 4, "vertex_y_coordinate": 5, "vertex_z_coordinate": 3},
                    {"vertex_x_coordinate": 4, "vertex_y_coordinate": 0, "vertex_z_coordinate": 3},
                ],
            },
            validate=False,
        )
        assert calculate_zone_ceiling_area(doc, "B") == 0.0

    def test_calculate_zone_height_no_coords(self) -> None:
        """Surfaces without valid coordinates are skipped when calculating zone height."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {})
        doc.add(
            "BuildingSurface:Detailed",
            "NoVerts",
            {"surface_type": "Wall", "zone_name": "Z1", "outside_boundary_condition": "Outdoors"},
            validate=False,
        )
        assert calculate_zone_height(doc, "Z1") == 0.0

    def test_calculate_zone_height_with_surfaces(self) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {})
        doc.add(
            "BuildingSurface:Detailed",
            "W1",
            {
                "surface_type": "Wall",
                "zone_name": "Z1",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0, "vertex_y_coordinate": 0, "vertex_z_coordinate": 3},
                    {"vertex_x_coordinate": 0, "vertex_y_coordinate": 0, "vertex_z_coordinate": 0},
                    {"vertex_x_coordinate": 10, "vertex_y_coordinate": 0, "vertex_z_coordinate": 0},
                    {"vertex_x_coordinate": 10, "vertex_y_coordinate": 0, "vertex_z_coordinate": 3},
                ],
            },
            validate=False,
        )
        assert _close(calculate_zone_height(doc, "Z1"), 3.0)


# ---------------------------------------------------------------------------
# translate_building / rotate_building  (edge cases: no coords)
# ---------------------------------------------------------------------------


class TestTranslateRotateBuilding:
    def test_translate_building_skips_no_coords(self) -> None:
        """Surfaces without vertex data are skipped when translating building surfaces."""
        doc = new_document(version=(24, 1, 0))
        doc.add(
            "BuildingSurface:Detailed",
            "Empty",
            {"surface_type": "Wall", "outside_boundary_condition": "Outdoors"},
            validate=False,
        )
        translate_building(doc, Vector3D(10, 10, 0))  # should not raise

    def test_rotate_building_skips_no_coords(self) -> None:
        """Surfaces without vertex data are skipped when rotating building surfaces."""
        doc = new_document(version=(24, 1, 0))
        doc.add(
            "BuildingSurface:Detailed",
            "Empty",
            {"surface_type": "Wall", "outside_boundary_condition": "Outdoors"},
            validate=False,
        )
        rotate_building(doc, 45.0)  # should not raise


# ---------------------------------------------------------------------------
# calculate_zone_volume
# ---------------------------------------------------------------------------


class TestCalculateZoneVolume:
    def test_simple_box_volume(self) -> None:
        """Test volume calculation for a closed box zone."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Box", {})
        # Define 6 faces of a 5x4x3 box
        faces = {
            "Floor": [
                (0, 0, 0),
                (5, 0, 0),
                (5, 4, 0),
                (0, 4, 0),
            ],
            "Ceiling": [
                (0, 0, 3),
                (5, 0, 3),
                (5, 4, 3),
                (0, 4, 3),
            ],
            "WallS": [
                (0, 0, 3),
                (0, 0, 0),
                (5, 0, 0),
                (5, 0, 3),
            ],
            "WallN": [
                (5, 4, 3),
                (5, 4, 0),
                (0, 4, 0),
                (0, 4, 3),
            ],
            "WallE": [
                (5, 0, 3),
                (5, 0, 0),
                (5, 4, 0),
                (5, 4, 3),
            ],
            "WallW": [
                (0, 4, 3),
                (0, 4, 0),
                (0, 0, 0),
                (0, 0, 3),
            ],
        }
        for name, verts in faces.items():
            data: dict[str, object] = {
                "surface_type": "Floor" if "Floor" in name else ("Ceiling" if "Ceiling" in name else "Wall"),
                "zone_name": "Box",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {
                        "vertex_x_coordinate": float(x),
                        "vertex_y_coordinate": float(y),
                        "vertex_z_coordinate": float(z),
                    }
                    for x, y, z in verts
                ],
            }
            doc.add("BuildingSurface:Detailed", name, data, validate=False)
        vol = calculate_zone_volume(doc, "Box")
        assert _close(vol, 60.0, 1e-6)

    def test_zone_volume_no_surfaces(self) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Empty", {})
        assert calculate_zone_volume(doc, "Empty") == 0.0

    def test_zone_volume_wrong_zone(self) -> None:
        """Surfaces in other zones are excluded when calculating zone volume."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "A", {})
        doc.add("Zone", "B", {})
        doc.add(
            "BuildingSurface:Detailed",
            "WallA",
            {
                "surface_type": "Wall",
                "zone_name": "A",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0, "vertex_y_coordinate": 0, "vertex_z_coordinate": 3},
                    {"vertex_x_coordinate": 0, "vertex_y_coordinate": 0, "vertex_z_coordinate": 0},
                    {"vertex_x_coordinate": 10, "vertex_y_coordinate": 0, "vertex_z_coordinate": 0},
                    {"vertex_x_coordinate": 10, "vertex_y_coordinate": 0, "vertex_z_coordinate": 3},
                ],
            },
            validate=False,
        )
        assert calculate_zone_volume(doc, "B") == 0.0


# ---------------------------------------------------------------------------
# set_wwr
# ---------------------------------------------------------------------------


class TestSetWWR:
    def _make_doc_with_outdoor_wall(self) -> IDFDocument:
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {})
        doc.add(
            "BuildingSurface:Detailed",
            "SouthWall",
            {
                "surface_type": "Wall",
                "zone_name": "Z1",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                ],
            },
            validate=False,
        )
        return doc

    def test_set_wwr_creates_window(self) -> None:
        doc = self._make_doc_with_outdoor_wall()
        windows = set_wwr(doc, 0.4)
        assert len(windows) >= 1
        win = windows[0]
        assert win.surface_type == "Window"

    def test_set_wwr_invalid_ratio(self) -> None:
        doc = self._make_doc_with_outdoor_wall()
        with pytest.raises(ValueError, match="wwr must be between"):
            set_wwr(doc, 0.0)
        with pytest.raises(ValueError, match="wwr must be between"):
            set_wwr(doc, 1.0)

    def test_set_wwr_skips_non_outdoor_wall(self) -> None:
        """Walls with non-Outdoors boundary condition are skipped when setting WWR."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {})
        doc.add(
            "BuildingSurface:Detailed",
            "IntWall",
            {
                "surface_type": "Wall",
                "zone_name": "Z1",
                "outside_boundary_condition": "Surface",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                ],
            },
            validate=False,
        )
        windows = set_wwr(doc, 0.4)
        assert windows == []

    def test_set_wwr_skips_tiny_wall(self) -> None:
        """Walls with negligible area are skipped when setting WWR."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {})
        doc.add(
            "BuildingSurface:Detailed",
            "TinyWall",
            {
                "surface_type": "Wall",
                "zone_name": "Z1",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 3,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                ],
            },
            validate=False,
        )
        windows = set_wwr(doc, 0.4)
        assert windows == []

    def test_set_wwr_with_orientation(self) -> None:
        """Fenestrations on walls not matching the target orientation are preserved."""
        doc = self._make_doc_with_outdoor_wall()
        # SouthWall faces south (azimuth ~180). Asking for north should skip it.
        windows = set_wwr(doc, 0.4, orientation="north")
        assert windows == []

    def test_set_wwr_removes_existing_fenestration(self) -> None:
        """Existing fenestration on matching walls is removed."""
        doc = self._make_doc_with_outdoor_wall()
        doc.add(
            "FenestrationSurface:Detailed",
            "OldWindow",
            {
                "surface_type": "Window",
                "building_surface_name": "SouthWall",
                "construction_name": "GlazingConstruction",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 1.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 2.5},
                    {"vertex_x_coordinate": 1.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.5},
                    {"vertex_x_coordinate": 4.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.5},
                    {"vertex_x_coordinate": 4.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 2.5},
                ],
            },
            validate=False,
        )
        windows = set_wwr(doc, 0.3)
        assert len(windows) == 1
        # Old window should be gone
        old = doc.getobject("FenestrationSurface:Detailed", "OldWindow")
        assert old is None
        # Construction should be preserved from old window
        assert windows[0].construction_name == "GlazingConstruction"

    def test_set_wwr_with_explicit_construction(self) -> None:
        doc = self._make_doc_with_outdoor_wall()
        windows = set_wwr(doc, 0.4, construction="MyGlass")
        assert len(windows) >= 1
        assert windows[0].construction_name == "MyGlass"

    def test_set_wwr_wall_no_coords(self) -> None:
        """Walls without valid coordinates are skipped when setting WWR."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {})
        doc.add(
            "BuildingSurface:Detailed",
            "NoCoordWall",
            {
                "surface_type": "Wall",
                "zone_name": "Z1",
                "outside_boundary_condition": "Outdoors",
            },
            validate=False,
        )
        windows = set_wwr(doc, 0.4)
        assert windows == []


# ---------------------------------------------------------------------------
# _orientation_to_azimuth
# ---------------------------------------------------------------------------


class TestOrientationToAzimuth:
    def test_valid_orientations(self) -> None:
        assert _orientation_to_azimuth("north") == 0.0
        assert _orientation_to_azimuth("east") == 90.0
        assert _orientation_to_azimuth("south") == 180.0
        assert _orientation_to_azimuth("west") == 270.0

    def test_invalid_orientation(self) -> None:
        with pytest.raises(ValueError, match="orientation must be one of"):
            _orientation_to_azimuth("northeast")


# ---------------------------------------------------------------------------
# _wall_matches
# ---------------------------------------------------------------------------


class TestWallMatches:
    def test_wrong_surface_type(self) -> None:
        wall = IDFObject(obj_type="BuildingSurface:Detailed", name="Floor1", data={"surface_type": "Floor"})
        assert not _wall_matches(wall, "Wall", None, 10.0)

    def test_no_coords_with_azimuth(self) -> None:
        """A wall surface without valid coordinates returns False when checking azimuth match."""
        wall = IDFObject(obj_type="BuildingSurface:Detailed", name="W", data={"surface_type": "Wall"})
        assert not _wall_matches(wall, "Wall", 180.0, 10.0)

    def test_azimuth_outside_tolerance(self) -> None:
        """A wall with azimuth outside the target tolerance returns False."""
        wall = IDFObject(
            obj_type="BuildingSurface:Detailed",
            name="W",
            data={
                "surface_type": "Wall",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                ],
            },
        )
        # This south-facing wall (~180 deg) should not match east (90 deg) with tight tolerance
        assert not _wall_matches(wall, "Wall", 90.0, 5.0)


# ---------------------------------------------------------------------------
# _inset_polygon
# ---------------------------------------------------------------------------


class TestInsetPolygon:
    def test_degenerate_polygon(self) -> None:
        """A polygon with fewer than 3 vertices returns None for the inset polygon."""
        poly = Polygon3D([Vector3D(0, 0, 0), Vector3D(1, 0, 0)])
        result = _inset_polygon(poly, 0.5)
        assert result is None

    def test_horizontal_wall_inset(self) -> None:
        """A nearly horizontal wall uses the up-vector fallback for the 2D coordinate system."""
        # Horizontal polygon: normal is (0,0,1) -> dot with up > 0.99
        poly = Polygon3D([
            Vector3D(0, 0, 5),
            Vector3D(10, 0, 5),
            Vector3D(10, 10, 5),
            Vector3D(0, 10, 5),
        ])
        result = _inset_polygon(poly, 0.5)
        assert result is not None

    def test_zero_width_wall(self) -> None:
        """A wall with zero width returns None when computing the inset polygon."""
        # All points collinear in 2D projection
        poly = Polygon3D([
            Vector3D(0, 0, 0),
            Vector3D(0, 0, 3),
            Vector3D(0, 0, 3),
            Vector3D(0, 0, 0),
        ])
        result = _inset_polygon(poly, 0.5)
        assert result is None


# ---------------------------------------------------------------------------
# line_intersect_2d
# ---------------------------------------------------------------------------


class TestLineIntersect2D:
    def test_parallel_lines(self) -> None:
        """Parallel lines return None when computing their 2D intersection."""
        result = line_intersect_2d((0, 0), (1, 0), (0, 1), (1, 1))
        assert result is None

    def test_intersecting_lines(self) -> None:
        result = line_intersect_2d((0, 0), (1, 1), (0, 1), (1, 0))
        assert result is not None
        assert _close(result[0], 0.5)
        assert _close(result[1], 0.5)


# ---------------------------------------------------------------------------
# _sutherland_hodgman edge cases
# ---------------------------------------------------------------------------


class TestSutherlandHodgman:
    def test_clipping_with_intersection(self) -> None:
        """Both inside-to-outside and outside-to-inside edge crossings are handled in polygon clipping."""
        subject = [(0, 0), (10, 0), (10, 10), (0, 10)]
        clip = [(5, -5), (15, -5), (15, 5), (5, 5)]
        result = _sutherland_hodgman(subject, clip)
        assert len(result) >= 3


# ---------------------------------------------------------------------------
# is_convex_2d edge cases
# ---------------------------------------------------------------------------


class TestIsConvex2DEdgeCases:
    def test_fewer_than_3_vertices(self) -> None:
        """A polygon with fewer than 3 vertices returns False for the convexity check."""
        assert not is_convex_2d([(0, 0), (1, 0)])

    def test_collinear_edges_skipped(self) -> None:
        """Collinear edges with near-zero cross product are skipped in the convexity check."""
        # Square with an extra collinear point
        poly = [(0, 0), (5, 0), (10, 0), (10, 10), (0, 10)]
        assert is_convex_2d(poly)


# ---------------------------------------------------------------------------
# triangulate_2d
# ---------------------------------------------------------------------------

_Poly2D = list[tuple[float, float]]

#: A 10 x 10 square with its 5 x 5 north-east quarter cut away (area 75).
_L_2D: _Poly2D = [(10, 5), (5, 5), (5, 10), (0, 10), (0, 0), (10, 0)]
#: A 9 x 9 square with a 3 x 6 slot cut from its north edge (area 63).
_U_2D: _Poly2D = [(0, 0), (9, 0), (9, 9), (6, 9), (6, 3), (3, 3), (3, 9), (0, 9)]
#: A 10 x 10 square around a 2 x 2 courtyard, joined by a doubled bridge edge (area 96).
_KEYHOLE_2D: _Poly2D = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0), (4, 4), (4, 6), (6, 6), (6, 4), (4, 4)]
#: Two triangles touching at a single doubled vertex (area 8).
_PINCHED_2D: _Poly2D = [(0, 0), (4, 0), (2, 2), (4, 4), (0, 4), (2, 2)]
#: Two triangles pinched at the origin on the same side of it, so the ring turns convexly across their gap (area 12.5).
_PINCHED_SAME_SIDE_2D: _Poly2D = [(0, 0), (-4, 1), (-3, -3), (0, 0), (-1, -2), (4, -2)]


def _assert_tiles(poly: _Poly2D, expected_area: float) -> None:
    """Assert the triangles tile ``poly``: areas sum to its area, each keeps its winding and lies inside it.

    Summing areas alone would pass a triangulation that double-covers one region and misses
    another, so each triangle's centroid is also checked to lie inside the polygon.
    """
    triangles = triangulate_2d(poly)
    winding = 1.0 if polygon_area_2d(poly) > 0 else -1.0
    areas = [polygon_area_2d([poly[a], poly[b], poly[c]]) for a, b, c in triangles]
    assert all(area * winding > 0 for area in areas)
    assert sum(abs(area) for area in areas) == pytest.approx(expected_area)
    for a, b, c in triangles:
        centroid = ((poly[a][0] + poly[b][0] + poly[c][0]) / 3, (poly[a][1] + poly[b][1] + poly[c][1]) / 3)
        assert _point_in_polygon_2d(centroid, poly)


class TestTriangulate2D:
    @pytest.mark.parametrize(
        ("poly", "area"),
        [(_L_2D, 75.0), (_U_2D, 63.0), (_KEYHOLE_2D, 96.0), (_PINCHED_2D, 8.0), (_PINCHED_SAME_SIDE_2D, 12.5)],
        ids=["L", "U", "keyhole", "pinched", "pinched-same-side"],
    )
    @pytest.mark.parametrize("reverse", [False, True], ids=["ccw", "cw"])
    def test_tiles_from_every_start_vertex(self, poly: _Poly2D, area: float, reverse: bool) -> None:
        ring = list(reversed(poly)) if reverse else poly
        for start in range(len(ring)):
            _assert_tiles(ring[start:] + ring[:start], area)

    def test_keyhole_with_bridge_along_an_edge(self) -> None:
        """The bridge leaves the outer ring midway along an edge, so its doubled end is collinear there."""
        keyhole: _Poly2D = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 5), (4, 5), (4, 6), (6, 6), (6, 4), (4, 4)]
        keyhole += [(4, 5), (0, 5)]
        _assert_tiles(keyhole, 96.0)

    def test_collinear_vertex(self) -> None:
        """A vertex midway along an edge bounds no area and must not stall the clipper."""
        poly = [*_L_2D[:5], (5.0, 0.0), *_L_2D[5:]]
        for start in range(len(poly)):
            _assert_tiles(poly[start:] + poly[:start], 75.0)

    def test_notch_corner_on_a_diagonal_corners_its_triangles(self) -> None:
        """The L's notch corner lies on the diagonal between two outer corners; it is not cut through."""
        _assert_tiles(_L_2D, 75.0)
        assert len(triangulate_2d(_L_2D)) == 4

    def test_duplicate_vertex(self) -> None:
        poly = [*_L_2D[:3], _L_2D[2], *_L_2D[3:]]
        for start in range(len(poly)):
            _assert_tiles(poly[start:] + poly[:start], 75.0)

    def test_scale_invariant(self) -> None:
        """A millimetre-sized and a kilometre-sized L tile alike."""
        for scale in (1e-3, 1e3):
            _assert_tiles([(x * scale, y * scale) for x, y in _L_2D], 75.0 * scale**2)

    def test_self_intersecting_bowtie_covers_every_vertex(self) -> None:
        """No ear is valid in a bowtie; the fallback still clips and uses every vertex."""
        bowtie: _Poly2D = [(0, 0), (2, 2), (2, 0), (1, 3), (0, 2)]
        triangles = triangulate_2d(bowtie)
        assert triangles
        assert {i for tri in triangles for i in tri} == set(range(len(bowtie)))

    def test_degenerate_inputs(self) -> None:
        assert triangulate_2d([]) == []
        assert triangulate_2d([(0, 0), (1, 0)]) == []
        assert triangulate_2d([(0, 0), (1, 0), (2, 0), (3, 0)]) == []

    def test_triangle_keeps_its_winding(self) -> None:
        assert triangulate_2d([(0, 0), (1, 0), (0, 1)]) == [(0, 1, 2)]
        clockwise: _Poly2D = [(0, 0), (0, 1), (1, 0)]
        [(a, b, c)] = triangulate_2d(clockwise)
        assert polygon_area_2d([clockwise[a], clockwise[b], clockwise[c]]) < 0


# ---------------------------------------------------------------------------
# polygon_intersection_2d edge cases
# ---------------------------------------------------------------------------


class TestPolygonIntersection2DEdgeCases:
    def test_both_concave_returns_none(self) -> None:
        """Both polygons concave: returns None (lines 1350-1354)."""
        l1 = [(0, 0), (5, 0), (5, 3), (3, 3), (3, 5), (0, 5)]
        l2 = [(1, 1), (6, 1), (6, 4), (4, 4), (4, 6), (1, 6)]
        result = polygon_intersection_2d(l1, l2)
        assert result is None

    def test_a_convex_b_concave(self) -> None:
        """When polygon A is convex and B is concave, arguments are swapped for intersection."""
        convex = [(0, 0), (10, 0), (10, 10), (0, 10)]
        concave = [(1, 1), (5, 1), (5, 3), (3, 3), (3, 5), (1, 5)]
        result = polygon_intersection_2d(convex, concave)
        # concave is fully inside convex, so the result equals the concave polygon
        assert result is not None
        assert abs(polygon_area_2d(result)) > 0

    def test_tiny_intersection_returns_none(self) -> None:
        """An intersection with negligible area returns None."""
        a = [(0, 0), (10, 0), (10, 10), (0, 10)]
        # b is barely touching a at a corner
        b = [(10, 10), (20, 10), (20, 20), (10, 20)]
        result = polygon_intersection_2d(a, b)
        assert result is None

    def test_result_fewer_than_3_vertices(self) -> None:
        """An intersection result with fewer than 3 vertices returns None."""
        # Barely touching rectangles sharing an edge produce degenerate intersection
        a = [(0, 0), (5, 0), (5, 5), (0, 5)]
        b = [(5, 0), (10, 0), (10, 5), (5, 5)]
        result = polygon_intersection_2d(a, b)
        # Sutherland-Hodgman returns a 4-point degenerate polygon (all at x=5),
        # which has near-zero area; polygon_intersection_2d discards it as None.
        assert result is None


# ---------------------------------------------------------------------------
# intersect_match
# ---------------------------------------------------------------------------


class TestIntersectMatch:
    def _make_adjacent_zones_doc(self) -> IDFDocument:
        """Two zones sharing a wall at y=5."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "ZoneA", {})
        doc.add("Zone", "ZoneB", {})
        # Wall A at y=5 facing +Y (normal +Y)
        doc.add(
            "BuildingSurface:Detailed",
            "WallA",
            {
                "surface_type": "Wall",
                "zone_name": "ZoneA",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 5.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 5.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 5.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 5.0, "vertex_z_coordinate": 3.0},
                ],
            },
            validate=False,
        )
        # Wall B at y=5 facing -Y (normal -Y), same vertices reversed
        doc.add(
            "BuildingSurface:Detailed",
            "WallB",
            {
                "surface_type": "Wall",
                "zone_name": "ZoneB",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 5.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 5.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 5.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 5.0, "vertex_z_coordinate": 3.0},
                ],
            },
            validate=False,
        )
        return doc

    def test_matching_walls(self) -> None:
        doc = self._make_adjacent_zones_doc()
        intersect_match(doc)
        wall_a = doc.getobject("BuildingSurface:Detailed", "WallA")
        wall_b = doc.getobject("BuildingSurface:Detailed", "WallB")
        assert wall_a is not None and wall_b is not None
        assert wall_a.outside_boundary_condition == "Surface"
        assert wall_a.outside_boundary_condition_object == "WallB"
        assert wall_b.outside_boundary_condition == "Surface"
        assert wall_b.outside_boundary_condition_object == "WallA"

    def test_partial_overlap_splits_and_matches(self) -> None:
        """A smaller wall overlapping a larger one splits the larger and matches the overlap.

        Under the intersect-and-split algorithm, unequal overlapping walls are
        no longer skipped: the overlap becomes a matched interior fragment and
        the leftover stays exterior.  Total area on the big wall's zone is
        conserved.
        """
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "A", {})
        doc.add("Zone", "B", {})
        # Big wall (10 x 3 = 30 m²)
        doc.add(
            "BuildingSurface:Detailed",
            "BigWall",
            {
                "surface_type": "Wall",
                "zone_name": "A",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 5.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 5.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 5.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 5.0, "vertex_z_coordinate": 3.0},
                ],
            },
            validate=False,
        )
        # Small wall (same plane, anti-parallel normal, 1 x 1 = 1 m², inside the big wall)
        doc.add(
            "BuildingSurface:Detailed",
            "SmallWall",
            {
                "surface_type": "Wall",
                "zone_name": "B",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 5.0, "vertex_y_coordinate": 5.0, "vertex_z_coordinate": 1.0},
                    {"vertex_x_coordinate": 5.0, "vertex_y_coordinate": 5.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 4.0, "vertex_y_coordinate": 5.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 4.0, "vertex_y_coordinate": 5.0, "vertex_z_coordinate": 1.0},
                ],
            },
            validate=False,
        )
        intersect_match(doc)

        # SmallWall is now interior, matched to a BigWall fragment.
        small = doc.getobject("BuildingSurface:Detailed", "SmallWall")
        assert small is not None
        assert small.outside_boundary_condition == "Surface"
        partner_name = small.outside_boundary_condition_object
        assert partner_name.startswith("BigWall")

        zone_a = [s for s in doc["BuildingSurface:Detailed"] if getattr(s, "zone_name", "") == "A"]
        matched = [s for s in zone_a if s.outside_boundary_condition == "Surface"]
        remainder = [s for s in zone_a if s.outside_boundary_condition == "Outdoors"]
        # One matched fragment (the 1 m² overlap) plus exterior remainder pieces.
        assert len(matched) == 1
        assert matched[0].outside_boundary_condition_object == "SmallWall"
        assert abs(get_surface_coords(matched[0]).area - 1.0) < 1e-6
        assert len(remainder) >= 1
        # Area is conserved across the split.
        total = sum(get_surface_coords(s).area for s in zone_a)
        assert abs(total - 30.0) < 1e-6

    def test_no_match_normals_not_antiparallel(self) -> None:
        """Walls with non-antiparallel normals are not matched as adjacent surfaces."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "A", {})
        doc.add("Zone", "B", {})
        # Both walls face the same direction
        for name in ("Wall1", "Wall2"):
            doc.add(
                "BuildingSurface:Detailed",
                name,
                {
                    "surface_type": "Wall",
                    "zone_name": "A" if name == "Wall1" else "B",
                    "outside_boundary_condition": "Outdoors",
                    "number_of_vertices": 4,
                    "vertices": [
                        {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 5.0, "vertex_z_coordinate": 3.0},
                        {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 5.0, "vertex_z_coordinate": 0.0},
                        {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 5.0, "vertex_z_coordinate": 0.0},
                        {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 5.0, "vertex_z_coordinate": 3.0},
                    ],
                },
                validate=False,
            )
        intersect_match(doc)
        wall1 = doc.getobject("BuildingSurface:Detailed", "Wall1")
        assert wall1 is not None
        assert wall1.outside_boundary_condition == "Outdoors"

    def test_no_match_centroids_far_apart(self) -> None:
        """Walls whose centroids are more than 1m apart are not matched as adjacent surfaces."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "A", {})
        doc.add("Zone", "B", {})
        # Wall A at y=0 facing +Y
        doc.add(
            "BuildingSurface:Detailed",
            "WA",
            {
                "surface_type": "Wall",
                "zone_name": "A",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                ],
            },
            validate=False,
        )
        # Wall B at y=10 facing -Y (anti-parallel normal, but far away)
        doc.add(
            "BuildingSurface:Detailed",
            "WB",
            {
                "surface_type": "Wall",
                "zone_name": "B",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 10.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 10.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 10.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 10.0, "vertex_z_coordinate": 3.0},
                ],
            },
            validate=False,
        )
        intersect_match(doc)
        wa = doc.getobject("BuildingSurface:Detailed", "WA")
        assert wa is not None
        assert wa.outside_boundary_condition == "Outdoors"

    def test_wall_a_no_coords_skipped(self) -> None:
        """Wall A without valid coordinates is skipped in intersection matching."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "A", {})
        doc.add(
            "BuildingSurface:Detailed",
            "NoCoord1",
            {"surface_type": "Wall", "zone_name": "A", "outside_boundary_condition": "Outdoors"},
            validate=False,
        )
        doc.add(
            "BuildingSurface:Detailed",
            "HasCoord",
            {
                "surface_type": "Wall",
                "zone_name": "A",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                ],
            },
            validate=False,
        )
        intersect_match(doc)  # should not raise

    def test_wall_b_no_coords_skipped(self) -> None:
        """Wall B without valid coordinates is skipped in the inner matching loop."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "A", {})
        # Wall A has coords (processed in outer loop)
        doc.add(
            "BuildingSurface:Detailed",
            "WallWithCoords",
            {
                "surface_type": "Wall",
                "zone_name": "A",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                ],
            },
            validate=False,
        )
        # Wall B has no coords (skipped in inner loop)
        doc.add(
            "BuildingSurface:Detailed",
            "NoCoordWall",
            {"surface_type": "Wall", "zone_name": "A", "outside_boundary_condition": "Outdoors"},
            validate=False,
        )
        intersect_match(doc)  # should not raise

    def test_already_matched_wall_b_skipped_in_inner_loop(self) -> None:
        """Wall B that is already matched is skipped in the inner matching loop."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "ZA", {})
        doc.add("Zone", "ZB", {})
        # Wall A: at y=0, facing +Y (south-facing in EnergyPlus convention)
        doc.add(
            "BuildingSurface:Detailed",
            "WA",
            {
                "surface_type": "Wall",
                "zone_name": "ZA",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                ],
            },
            validate=False,
        )
        # Wall B: at x=0, facing +X (east-facing) — won't match WA
        doc.add(
            "BuildingSurface:Detailed",
            "WB",
            {
                "surface_type": "Wall",
                "zone_name": "ZA",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 10.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 10.0, "vertex_z_coordinate": 3.0},
                ],
            },
            validate=False,
        )
        # Wall C: at y=0, facing -Y — matches WA
        doc.add(
            "BuildingSurface:Detailed",
            "WC",
            {
                "surface_type": "Wall",
                "zone_name": "ZB",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                ],
            },
            validate=False,
        )
        # Wall D: at x=0, facing -X — matches WB
        doc.add(
            "BuildingSurface:Detailed",
            "WD",
            {
                "surface_type": "Wall",
                "zone_name": "ZB",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 10.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 10.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                ],
            },
            validate=False,
        )
        intersect_match(doc)
        # WA should be matched with WC
        wa = doc.getobject("BuildingSurface:Detailed", "WA")
        assert wa is not None
        assert wa.outside_boundary_condition == "Surface"
        # WB should be matched with WD
        wb = doc.getobject("BuildingSurface:Detailed", "WB")
        assert wb is not None
        assert wb.outside_boundary_condition == "Surface"

    def test_tiny_area_wall_skipped(self) -> None:
        """Walls with negligible area are skipped in intersection matching."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "A", {})
        doc.add("Zone", "B", {})
        # Degenerate wall (all points same)
        for name in ("Degen1", "Degen2"):
            doc.add(
                "BuildingSurface:Detailed",
                name,
                {
                    "surface_type": "Wall",
                    "zone_name": "A" if name == "Degen1" else "B",
                    "outside_boundary_condition": "Outdoors",
                    "number_of_vertices": 3,
                    "vertices": [
                        {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                        {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                        {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    ],
                },
                validate=False,
            )
        intersect_match(doc)  # should not raise or match

    def test_not_coplanar_walls_skipped(self) -> None:
        """Walls that pass the centroid-distance check but fail the coplanarity check are not matched."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "A", {})
        doc.add("Zone", "B", {})
        # Wall A at y=0
        doc.add(
            "BuildingSurface:Detailed",
            "PlaneA",
            {
                "surface_type": "Wall",
                "zone_name": "A",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                ],
            },
            validate=False,
        )
        # Wall B at y=0.7, facing -Y: centroid distance 0.7 m ≤ 1.0 but coplanarity check d > 0.5
        doc.add(
            "BuildingSurface:Detailed",
            "PlaneB",
            {
                "surface_type": "Wall",
                "zone_name": "B",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.7, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.7, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.7, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.7, "vertex_z_coordinate": 3.0},
                ],
            },
            validate=False,
        )
        intersect_match(doc)
        plane_a = doc.getobject("BuildingSurface:Detailed", "PlaneA")
        assert plane_a is not None
        # centroid distance is 0.7 m (passes dist check) but abs(d)=0.7 > 0.5 (fails coplanarity)
        assert plane_a.outside_boundary_condition == "Outdoors"


# ---------------------------------------------------------------------------
# Polygon3D tilt / azimuth properties
# ---------------------------------------------------------------------------


class TestPolygonTiltAzimuth:
    def test_tilt_vertical_wall(self) -> None:
        """Vertical wall has tilt ~90 degrees (lines 328-331)."""
        poly = Polygon3D([
            Vector3D(0, 0, 3),
            Vector3D(0, 0, 0),
            Vector3D(10, 0, 0),
            Vector3D(10, 0, 3),
        ])
        assert _close(poly.tilt, 90.0, 0.001)

    def test_tilt_horizontal(self) -> None:
        """Horizontal surface has tilt ~0 or ~180."""
        poly = Polygon3D([
            Vector3D(0, 0, 0),
            Vector3D(1, 0, 0),
            Vector3D(1, 1, 0),
            Vector3D(0, 1, 0),
        ])
        assert poly.tilt < 1.0 or poly.tilt > 179.0

    def test_azimuth_horizontal_is_zero(self) -> None:
        """A horizontal surface has an azimuth of 0.0."""
        poly = Polygon3D([
            Vector3D(0, 0, 0),
            Vector3D(1, 0, 0),
            Vector3D(1, 1, 0),
            Vector3D(0, 1, 0),
        ])
        assert poly.azimuth == 0.0

    def test_azimuth_negative_angle_wraps(self) -> None:
        """Negative azimuth angles are wrapped to the positive range [0, 360)."""
        # A wall facing west should have azimuth ~270
        poly = Polygon3D([
            Vector3D(0, 0, 3),
            Vector3D(0, 0, 0),
            Vector3D(0, 10, 0),
            Vector3D(0, 10, 3),
        ])
        az = poly.azimuth
        assert 0 <= az < 360

    def test_azimuth_south_facing(self) -> None:
        """South-facing wall has azimuth ~180."""
        poly = Polygon3D([
            Vector3D(0, 0, 3),
            Vector3D(0, 0, 0),
            Vector3D(10, 0, 0),
            Vector3D(10, 0, 3),
        ])
        assert _close(poly.azimuth, 180.0, 0.001)


# ---------------------------------------------------------------------------
# calculate_surface_tilt / calculate_surface_azimuth
# ---------------------------------------------------------------------------


class TestSurfaceTiltAzimuth:
    def test_calculate_surface_tilt(self) -> None:
        """Exercise calculate_surface_tilt (lines 733-734)."""
        surface = IDFObject(
            obj_type="BuildingSurface:Detailed",
            name="Wall",
            data={
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                ],
            },
        )
        tilt = calculate_surface_tilt(surface)
        assert _close(tilt, 90.0, 1.0)

    def test_calculate_surface_tilt_no_coords(self) -> None:
        surface = IDFObject(obj_type="BuildingSurface:Detailed", name="Empty", data={})
        assert calculate_surface_tilt(surface) == 0.0

    def test_calculate_surface_azimuth(self) -> None:
        """Exercise calculate_surface_azimuth (lines 761-762)."""
        surface = IDFObject(
            obj_type="BuildingSurface:Detailed",
            name="Wall",
            data={
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                ],
            },
        )
        azimuth = calculate_surface_azimuth(surface)
        assert _close(azimuth, 180.0, 5.0)

    def test_calculate_surface_azimuth_no_coords(self) -> None:
        surface = IDFObject(obj_type="BuildingSurface:Detailed", name="Empty", data={})
        assert calculate_surface_azimuth(surface) == 0.0


# ---------------------------------------------------------------------------
# Zone floor area with different zone name
# ---------------------------------------------------------------------------


class TestZoneFloorAreaWrongZone:
    def test_floor_area_wrong_zone_skipped(self) -> None:
        """Surfaces in other zones are excluded when calculating zone floor area."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "A", {})
        doc.add("Zone", "B", {})
        doc.add(
            "BuildingSurface:Detailed",
            "FloorA",
            {
                "surface_type": "Floor",
                "zone_name": "A",
                "outside_boundary_condition": "Ground",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0, "vertex_y_coordinate": 0, "vertex_z_coordinate": 0},
                    {"vertex_x_coordinate": 10, "vertex_y_coordinate": 0, "vertex_z_coordinate": 0},
                    {"vertex_x_coordinate": 10, "vertex_y_coordinate": 10, "vertex_z_coordinate": 0},
                    {"vertex_x_coordinate": 0, "vertex_y_coordinate": 10, "vertex_z_coordinate": 0},
                ],
            },
            validate=False,
        )
        # Zone B has no surfaces, but zone A's floor exists
        assert calculate_zone_floor_area(doc, "B") == 0.0


# ---------------------------------------------------------------------------
# Zone height with surface in wrong zone
# ---------------------------------------------------------------------------


class TestZoneHeightWrongZone:
    def test_zone_height_wrong_zone(self) -> None:
        """Surfaces in other zones are excluded when calculating zone height."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "A", {})
        doc.add("Zone", "B", {})
        doc.add(
            "BuildingSurface:Detailed",
            "WallA",
            {
                "surface_type": "Wall",
                "zone_name": "A",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0, "vertex_y_coordinate": 0, "vertex_z_coordinate": 3},
                    {"vertex_x_coordinate": 0, "vertex_y_coordinate": 0, "vertex_z_coordinate": 0},
                    {"vertex_x_coordinate": 10, "vertex_y_coordinate": 0, "vertex_z_coordinate": 0},
                    {"vertex_x_coordinate": 10, "vertex_y_coordinate": 0, "vertex_z_coordinate": 3},
                ],
            },
            validate=False,
        )
        assert calculate_zone_height(doc, "B") == 0.0


# ---------------------------------------------------------------------------
# set_wwr with fenestration referrers (lines 1099-1108)
# ---------------------------------------------------------------------------


class TestSetWWRFenReferrers:
    def test_set_wwr_repoints_cross_references(self) -> None:
        """Existing fenestration cross-references are repointed to new windows (lines 1099-1108)."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {})
        doc.add(
            "BuildingSurface:Detailed",
            "SouthWall",
            {
                "surface_type": "Wall",
                "zone_name": "Z1",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                ],
            },
            validate=False,
        )
        doc.add(
            "FenestrationSurface:Detailed",
            "OldWindow",
            {
                "surface_type": "Window",
                "building_surface_name": "SouthWall",
                "construction_name": "GlazingC",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 1.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 2.5},
                    {"vertex_x_coordinate": 1.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.5},
                    {"vertex_x_coordinate": 4.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.5},
                    {"vertex_x_coordinate": 4.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 2.5},
                ],
            },
            validate=False,
        )
        # Add an object that references the old window
        doc.add(
            "FenestrationSurface:Detailed",
            "FrameObj",
            {
                "surface_type": "Door",
                "building_surface_name": "OldWindow",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 1.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 2.0},
                    {"vertex_x_coordinate": 1.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 1.0},
                    {"vertex_x_coordinate": 2.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 1.0},
                    {"vertex_x_coordinate": 2.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 2.0},
                ],
            },
            validate=False,
        )
        windows = set_wwr(doc, 0.4)
        assert len(windows) >= 1
        # The referrer should now point to one of the newly created windows,
        # not the original "OldWindow" surface.
        frame = doc.getobject("FenestrationSurface:Detailed", "FrameObj")
        assert frame is not None
        window_names = [w.name for w in windows]
        assert frame.building_surface_name in window_names
        assert frame.building_surface_name != "OldWindow"


# ---------------------------------------------------------------------------
# translate/rotate building with actual surfaces
# ---------------------------------------------------------------------------


class TestTranslateRotateBuildingWithSurfaces:
    def test_translate_building_moves_coords(self) -> None:
        """translate_building applies a translation offset to all surface vertices."""
        doc = new_document(version=(24, 1, 0))
        doc.add(
            "BuildingSurface:Detailed",
            "W1",
            {
                "surface_type": "Wall",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 3,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 1.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 1.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 1.0},
                ],
            },
            validate=False,
        )
        translate_building(doc, Vector3D(100, 200, 0))
        wall = doc.getobject("BuildingSurface:Detailed", "W1")
        assert wall is not None
        assert _close(wall.vertices[0].vertex_x_coordinate, 100.0)

    def test_rotate_building_changes_coords(self) -> None:
        """rotate_building rotates all surface vertices around the Z axis."""
        doc = new_document(version=(24, 1, 0))
        doc.add(
            "BuildingSurface:Detailed",
            "W1",
            {
                "surface_type": "Wall",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                ],
            },
            validate=False,
        )
        rotate_building(doc, 90.0)
        wall = doc.getobject("BuildingSurface:Detailed", "W1")
        assert wall is not None
        # After 90-degree rotation: vertex 3 was (10, 0, 0), should be (0, 10, 0)
        assert wall.vertices[2].vertex_y_coordinate == pytest.approx(10.0)


# ---------------------------------------------------------------------------
# _wall_matches azimuth > 180 difference wraps around
# ---------------------------------------------------------------------------


class TestWallMatchesAzimuthWrap:
    def test_azimuth_diff_over_180_wraps(self) -> None:
        """When azimuth difference exceeds 180 degrees, it wraps to find the true angle."""
        # Create a wall with azimuth ~350 (nearly north, slightly west)
        # Normal should point roughly toward azimuth 350 (between north and west)
        angle_rad = math.radians(350)  # 350 degrees clockwise from north
        nx = math.sin(angle_rad)  # x component of normal
        ny = math.cos(angle_rad)  # y component of normal

        # Create a wall whose outward normal points at azimuth 350
        # Wall vertices: perpendicular to (nx, ny, 0) direction
        # Tangent along wall: (-ny, nx, 0)
        tx, ty = -ny, nx
        wall = IDFObject(
            obj_type="BuildingSurface:Detailed",
            name="NearNorthWall",
            data={
                "surface_type": "Wall",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": -tx * 5, "vertex_y_coordinate": -ty * 5, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": -tx * 5, "vertex_y_coordinate": -ty * 5, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": tx * 5, "vertex_y_coordinate": ty * 5, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": tx * 5, "vertex_y_coordinate": ty * 5, "vertex_z_coordinate": 3.0},
                ],
            },
        )
        # Target azimuth 10 degrees. diff = |350 - 10| = 340 > 180, wraps to 20.
        # With tolerance 25, this should match.
        result = _wall_matches(wall, "Wall", 10.0, 25.0)
        assert result is True

    def test_azimuth_diff_over_180_but_outside_tolerance(self) -> None:
        """Wrapped diff still outside tolerance returns False."""
        angle_rad = math.radians(350)
        nx = math.sin(angle_rad)
        ny = math.cos(angle_rad)
        tx, ty = -ny, nx
        wall = IDFObject(
            obj_type="BuildingSurface:Detailed",
            name="NearNorthWall",
            data={
                "surface_type": "Wall",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": -tx * 5, "vertex_y_coordinate": -ty * 5, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": -tx * 5, "vertex_y_coordinate": -ty * 5, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": tx * 5, "vertex_y_coordinate": ty * 5, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": tx * 5, "vertex_y_coordinate": ty * 5, "vertex_z_coordinate": 3.0},
                ],
            },
        )
        # Target 10, wall ~350, wrapped diff ~20, tolerance 5 -> should NOT match
        result = _wall_matches(wall, "Wall", 10.0, 5.0)
        assert result is False


# ---------------------------------------------------------------------------
# calculate_zone_volume with surface no coords
# ---------------------------------------------------------------------------


class TestCalculateZoneVolumeNoCoords:
    def test_volume_surface_no_coords_skipped(self) -> None:
        """Surfaces without valid coordinates are skipped when calculating zone volume."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {})
        doc.add(
            "BuildingSurface:Detailed",
            "NoCoord",
            {"surface_type": "Wall", "zone_name": "Z1", "outside_boundary_condition": "Outdoors"},
            validate=False,
        )
        assert calculate_zone_volume(doc, "Z1") == 0.0


# ---------------------------------------------------------------------------
# set_wwr: fenestration on non-matching wall and no new window for referrer
# ---------------------------------------------------------------------------


class TestSetWWREdgeCases:
    def test_fen_on_non_matching_wall_not_removed(self) -> None:
        """Fenestrations on walls that don't match the target orientation are preserved."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {})
        # South wall (matching)
        doc.add(
            "BuildingSurface:Detailed",
            "SouthWall",
            {
                "surface_type": "Wall",
                "zone_name": "Z1",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                ],
            },
            validate=False,
        )
        # North wall (not matching with south orientation)
        doc.add(
            "BuildingSurface:Detailed",
            "NorthWall",
            {
                "surface_type": "Wall",
                "zone_name": "Z1",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 10.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 10.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 10.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 10.0, "vertex_z_coordinate": 3.0},
                ],
            },
            validate=False,
        )
        # Fen on north wall (should not be removed when filtering for south)
        doc.add(
            "FenestrationSurface:Detailed",
            "NorthWindow",
            {
                "surface_type": "Window",
                "building_surface_name": "NorthWall",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 8.0, "vertex_y_coordinate": 10.0, "vertex_z_coordinate": 2.5},
                    {"vertex_x_coordinate": 8.0, "vertex_y_coordinate": 10.0, "vertex_z_coordinate": 0.5},
                    {"vertex_x_coordinate": 2.0, "vertex_y_coordinate": 10.0, "vertex_z_coordinate": 0.5},
                    {"vertex_x_coordinate": 2.0, "vertex_y_coordinate": 10.0, "vertex_z_coordinate": 2.5},
                ],
            },
            validate=False,
        )
        windows = set_wwr(doc, 0.4, orientation="south")
        # North window should still exist
        north_win = doc.getobject("FenestrationSurface:Detailed", "NorthWindow")
        assert north_win is not None
        assert len(windows) >= 1

    def test_fen_referrer_no_new_window(self) -> None:
        """A fenestration referrer whose parent wall doesn't produce a new window is handled gracefully."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {})
        # Interior wall (matches by type but not Outdoors → no new window)
        doc.add(
            "BuildingSurface:Detailed",
            "IntWall",
            {
                "surface_type": "Wall",
                "zone_name": "Z1",
                "outside_boundary_condition": "Surface",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                ],
            },
            validate=False,
        )
        # Fen on the interior wall
        doc.add(
            "FenestrationSurface:Detailed",
            "IntWindow",
            {
                "surface_type": "Window",
                "building_surface_name": "IntWall",
                "construction_name": "GlazingC",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 1.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 2.5},
                    {"vertex_x_coordinate": 1.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.5},
                    {"vertex_x_coordinate": 4.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.5},
                    {"vertex_x_coordinate": 4.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 2.5},
                ],
            },
            validate=False,
        )
        # Add an object referencing the fen
        doc.add(
            "FenestrationSurface:Detailed",
            "SubSurface",
            {
                "surface_type": "Door",
                "building_surface_name": "IntWindow",
                "number_of_vertices": 4,
                "vertices": [
                    {"vertex_x_coordinate": 1.5, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 2.0},
                    {"vertex_x_coordinate": 1.5, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 1.0},
                    {"vertex_x_coordinate": 2.5, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 1.0},
                    {"vertex_x_coordinate": 2.5, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 2.0},
                ],
            },
            validate=False,
        )
        # No Outdoors walls → no new windows, but fen_referrers will have entries
        windows = set_wwr(doc, 0.4)
        assert windows == []
        # The referrer should remain unchanged since no new window was created
        sub_surface = doc.getobject("FenestrationSurface:Detailed", "SubSurface")
        assert sub_surface is not None
        assert sub_surface.building_surface_name == "IntWindow"
