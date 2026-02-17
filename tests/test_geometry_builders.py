"""Tests for geometry builders (Shoebox, add_block, add_shading_block, etc.)."""

from __future__ import annotations

import pytest

from idfkit import new_document
from idfkit.geometry import calculate_surface_area, calculate_zone_floor_area, get_surface_coords
from idfkit.geometry_builders import (
    Shoebox,
    add_block,
    add_shading_block,
    bounding_box,
    scale_building,
    set_default_constructions,
)

_TOL = 1e-6


def _close(a: float, b: float, tol: float = _TOL) -> bool:
    return abs(a - b) < tol


# ---------------------------------------------------------------------------
# Shoebox
# ---------------------------------------------------------------------------


class TestShoebox:
    def test_properties(self) -> None:
        s = Shoebox(name="Box", width=10, depth=8, floor_to_floor=3, num_stories=2)
        assert s.height == 6.0
        assert s.floor_area == 80.0
        assert s.total_floor_area == 160.0
        assert len(s.footprint) == 4

    def test_footprint_ccw(self) -> None:
        s = Shoebox(name="Box", width=10, depth=5, floor_to_floor=3, origin=(1, 2))
        fp = s.footprint
        assert fp == [(1, 2), (11, 2), (11, 7), (1, 7)]

    def test_build_single_story(self) -> None:
        doc = new_document()
        s = Shoebox(name="Office", width=10, depth=8, floor_to_floor=3)
        objs = s.build(doc)
        assert len(doc["Zone"]) == 1
        assert doc["Zone"]["Office"] is not None
        # 4 walls + 1 floor + 1 roof = 6 surfaces
        assert len(doc["BuildingSurface:Detailed"]) == 6
        assert len(objs) == 7  # 1 zone + 6 surfaces

    def test_build_multi_story(self) -> None:
        doc = new_document()
        s = Shoebox(name="Tower", width=10, depth=10, floor_to_floor=3, num_stories=3)
        s.build(doc)
        assert len(doc["Zone"]) == 3
        # Per story: 4 walls + 1 floor + 1 ceiling/roof = 6; total = 18
        assert len(doc["BuildingSurface:Detailed"]) == 18

    def test_floor_area_matches_calculation(self) -> None:
        doc = new_document()
        s = Shoebox(name="Office", width=10, depth=8, floor_to_floor=3)
        s.build(doc)
        computed = calculate_zone_floor_area(doc, "Office")
        assert _close(computed, 80.0, tol=0.1)

    def test_multi_story_inter_story_boundary(self) -> None:
        doc = new_document()
        s = Shoebox(name="T", width=10, depth=10, floor_to_floor=3, num_stories=2)
        s.build(doc)
        # Story 1 ceiling should reference Story 2 floor
        ceiling = doc.getobject("BuildingSurface:Detailed", "T Story 1 Ceiling")
        assert ceiling is not None
        assert ceiling.outside_boundary_condition == "Surface"
        assert ceiling.outside_boundary_condition_object == "T Story 2 Floor"
        # Story 2 floor should reference Story 1 ceiling
        floor2 = doc.getobject("BuildingSurface:Detailed", "T Story 2 Floor")
        assert floor2 is not None
        assert floor2.outside_boundary_condition == "Surface"
        assert floor2.outside_boundary_condition_object == "T Story 1 Ceiling"

    def test_ground_floor_bc(self) -> None:
        doc = new_document()
        Shoebox(name="B", width=5, depth=5, floor_to_floor=3).build(doc)
        floor = doc.getobject("BuildingSurface:Detailed", "B Floor")
        assert floor is not None
        assert floor.outside_boundary_condition == "Ground"

    def test_roof_bc(self) -> None:
        doc = new_document()
        Shoebox(name="B", width=5, depth=5, floor_to_floor=3).build(doc)
        roof = doc.getobject("BuildingSurface:Detailed", "B Roof")
        assert roof is not None
        assert roof.surface_type == "Roof"
        assert roof.outside_boundary_condition == "Outdoors"


# ---------------------------------------------------------------------------
# add_block
# ---------------------------------------------------------------------------


class TestAddBlock:
    def test_rectangular_footprint(self) -> None:
        doc = new_document()
        objs = add_block(doc, "Rect", [(0, 0), (10, 0), (10, 5), (0, 5)], floor_to_floor=3)
        assert len(doc["Zone"]) == 1
        assert len(doc["BuildingSurface:Detailed"]) == 6  # 4 walls + floor + roof
        assert len(objs) == 7

    def test_triangular_footprint(self) -> None:
        doc = new_document()
        add_block(doc, "Tri", [(0, 0), (10, 0), (5, 8)], floor_to_floor=3)
        # 3 walls + floor + roof = 5 surfaces
        assert len(doc["BuildingSurface:Detailed"]) == 5

    def test_l_shaped_footprint(self) -> None:
        doc = new_document()
        fp = [(0, 0), (10, 0), (10, 5), (5, 5), (5, 10), (0, 10)]
        add_block(doc, "L", fp, floor_to_floor=3)
        # 6 edges → 6 walls + floor + roof = 8
        assert len(doc["BuildingSurface:Detailed"]) == 8

    def test_multi_story(self) -> None:
        doc = new_document()
        add_block(doc, "M", [(0, 0), (5, 0), (5, 5), (0, 5)], floor_to_floor=3, num_stories=3)
        assert len(doc["Zone"]) == 3

    def test_invalid_footprint_raises(self) -> None:
        doc = new_document()
        with pytest.raises(ValueError, match="at least 3 vertices"):
            add_block(doc, "Bad", [(0, 0), (1, 0)], floor_to_floor=3)

    def test_invalid_height_raises(self) -> None:
        doc = new_document()
        with pytest.raises(ValueError, match="positive"):
            add_block(doc, "Bad", [(0, 0), (1, 0), (1, 1)], floor_to_floor=-1)

    def test_wall_area(self) -> None:
        doc = new_document()
        add_block(doc, "B", [(0, 0), (10, 0), (10, 5), (0, 5)], floor_to_floor=3)
        south_wall = doc.getobject("BuildingSurface:Detailed", "B Wall 1")
        assert south_wall is not None
        area = calculate_surface_area(south_wall)
        # Wall along (0,0)→(10,0), height 3 → area 30
        assert _close(area, 30.0, tol=0.1)


# ---------------------------------------------------------------------------
# add_shading_block
# ---------------------------------------------------------------------------


class TestAddShadingBlock:
    def test_creates_shading_surfaces(self) -> None:
        doc = new_document()
        objs = add_shading_block(doc, "Shade", [(0, 0), (5, 0), (5, 5), (0, 5)], height=10)
        # 4 walls + 1 top cap = 5
        assert len(objs) == 5
        assert len(doc["Shading:Site:Detailed"]) == 5

    def test_no_zones_created(self) -> None:
        doc = new_document()
        add_shading_block(doc, "S", [(0, 0), (3, 0), (3, 3), (0, 3)], height=5)
        assert len(doc["Zone"]) == 0

    def test_arbitrary_polygon(self) -> None:
        doc = new_document()
        # Triangle
        add_shading_block(doc, "Tri", [(0, 0), (10, 0), (5, 8)], height=7)
        # 3 walls + 1 top = 4
        assert len(doc["Shading:Site:Detailed"]) == 4

    def test_invalid_footprint_raises(self) -> None:
        doc = new_document()
        with pytest.raises(ValueError, match="at least 3"):
            add_shading_block(doc, "Bad", [(0, 0)], height=5)


# ---------------------------------------------------------------------------
# set_default_constructions
# ---------------------------------------------------------------------------


class TestSetDefaultConstructions:
    def test_assigns_to_empty(self) -> None:
        doc = new_document()
        add_block(doc, "B", [(0, 0), (5, 0), (5, 5), (0, 5)], floor_to_floor=3)
        count = set_default_constructions(doc, "MyConstruction")
        assert count == 6  # 4 walls + floor + roof
        for srf in doc["BuildingSurface:Detailed"]:
            assert srf.construction_name == "MyConstruction"

    def test_preserves_existing(self) -> None:
        doc = new_document()
        add_block(doc, "B", [(0, 0), (5, 0), (5, 5), (0, 5)], floor_to_floor=3)
        wall = doc.getobject("BuildingSurface:Detailed", "B Wall 1")
        assert wall is not None
        wall.construction_name = "SpecialWall"
        count = set_default_constructions(doc)
        assert count == 5  # All except the one already set
        assert wall.construction_name == "SpecialWall"

    def test_returns_count(self) -> None:
        doc = new_document()
        count = set_default_constructions(doc)
        assert count == 0


# ---------------------------------------------------------------------------
# bounding_box
# ---------------------------------------------------------------------------


class TestBoundingBox:
    def test_correct_bbox(self) -> None:
        doc = new_document()
        add_block(doc, "B", [(2, 3), (12, 3), (12, 8), (2, 8)], floor_to_floor=3)
        bb = bounding_box(doc)
        assert bb is not None
        (min_x, min_y), (max_x, max_y) = bb
        assert _close(min_x, 2.0)
        assert _close(min_y, 3.0)
        assert _close(max_x, 12.0)
        assert _close(max_y, 8.0)

    def test_empty_returns_none(self) -> None:
        doc = new_document()
        assert bounding_box(doc) is None


# ---------------------------------------------------------------------------
# scale_building
# ---------------------------------------------------------------------------


class TestScaleBuilding:
    def test_uniform_scale(self) -> None:
        doc = new_document()
        add_block(doc, "B", [(0, 0), (10, 0), (10, 5), (0, 5)], floor_to_floor=3)
        scale_building(doc, 2.0)
        bb = bounding_box(doc)
        assert bb is not None
        (_, _), (max_x, max_y) = bb
        assert _close(max_x, 20.0)
        assert _close(max_y, 10.0)

    def test_axis_independent_scale(self) -> None:
        doc = new_document()
        add_block(doc, "B", [(0, 0), (10, 0), (10, 5), (0, 5)], floor_to_floor=3)
        scale_building(doc, (2.0, 1.0, 1.0))
        bb = bounding_box(doc)
        assert bb is not None
        (_, _), (max_x, max_y) = bb
        assert _close(max_x, 20.0)
        assert _close(max_y, 5.0)

    def test_scale_with_anchor(self) -> None:
        from idfkit.geometry import Vector3D

        doc = new_document()
        add_block(doc, "B", [(0, 0), (10, 0), (10, 10), (0, 10)], floor_to_floor=3)
        # Scale by 2x around center (5, 5, 0) → box expands from (-5,-5) to (15,15)
        scale_building(doc, 2.0, anchor=Vector3D(5, 5, 0))
        bb = bounding_box(doc)
        assert bb is not None
        (min_x, min_y), (max_x, max_y) = bb
        assert _close(min_x, -5.0)
        assert _close(min_y, -5.0)
        assert _close(max_x, 15.0)
        assert _close(max_y, 15.0)

    def test_scale_preserves_surface_count(self) -> None:
        doc = new_document()
        add_block(doc, "B", [(0, 0), (5, 0), (5, 5), (0, 5)], floor_to_floor=3)
        n_before = len(doc["BuildingSurface:Detailed"])
        scale_building(doc, 3.0)
        assert len(doc["BuildingSurface:Detailed"]) == n_before
