"""Tests for the zoning module."""

from __future__ import annotations

import pytest

from idfkit import new_document
from idfkit.geometry import calculate_surface_area, get_surface_coords
from idfkit.zoning import (
    ASHRAE_PERIMETER_DEPTH,
    ZonedBlock,
    ZoningScheme,
    _classify_edge_orientation,
    _inset_polygon_2d,
    _is_convex,
    _polygon_area_signed,
    _split_core_perimeter,
    _ZoneFootprint,
    create_building,
    footprint_courtyard,
    footprint_h_shape,
    footprint_l_shape,
    footprint_rectangle,
    footprint_t_shape,
    footprint_u_shape,
)

_TOL = 1e-4


def _close(a: float, b: float, tol: float = _TOL) -> bool:
    return abs(a - b) < tol


# =========================================================================
# Footprint generators
# =========================================================================


class TestFootprintRectangle:
    def test_default_origin(self) -> None:
        fp = footprint_rectangle(10, 5)
        assert fp == [(0.0, 0.0), (10.0, 0.0), (10.0, 5.0), (0.0, 5.0)]

    def test_custom_origin(self) -> None:
        fp = footprint_rectangle(10, 5, origin=(3.0, 7.0))
        assert fp[0] == (3.0, 7.0)
        assert fp[2] == (13.0, 12.0)

    def test_is_ccw(self) -> None:
        fp = footprint_rectangle(10, 5)
        assert _polygon_area_signed(fp) > 0


class TestFootprintLShape:
    def test_vertex_count(self) -> None:
        fp = footprint_l_shape(20, 10, 8, 5)
        assert len(fp) == 6

    def test_is_ccw(self) -> None:
        fp = footprint_l_shape(20, 10, 8, 5)
        assert _polygon_area_signed(fp) > 0

    def test_area(self) -> None:
        fp = footprint_l_shape(20, 10, 8, 5)
        area = abs(_polygon_area_signed(fp))
        # Base: 20x10 = 200, Wing: 8x5 = 40 → total 240
        assert _close(area, 240.0)

    def test_wing_wider_than_base_raises(self) -> None:
        with pytest.raises(ValueError, match="wing_width"):
            footprint_l_shape(10, 10, 15, 5)


class TestFootprintUShape:
    def test_vertex_count(self) -> None:
        fp = footprint_u_shape(30, 20, 10, 8)
        assert len(fp) == 8

    def test_is_ccw(self) -> None:
        fp = footprint_u_shape(30, 20, 10, 8)
        assert _polygon_area_signed(fp) > 0

    def test_area(self) -> None:
        fp = footprint_u_shape(30, 20, 10, 8)
        area = abs(_polygon_area_signed(fp))
        # Overall 30x20=600 minus courtyard 10x8=80 → 520
        assert _close(area, 520.0)

    def test_courtyard_wider_than_building_raises(self) -> None:
        with pytest.raises(ValueError, match="courtyard_width"):
            footprint_u_shape(20, 20, 20, 5)

    def test_courtyard_deeper_than_building_raises(self) -> None:
        with pytest.raises(ValueError, match="courtyard_depth"):
            footprint_u_shape(20, 20, 10, 20)


class TestFootprintTShape:
    def test_vertex_count(self) -> None:
        fp = footprint_t_shape(10, 15, 30, 5)
        assert len(fp) == 8

    def test_is_ccw(self) -> None:
        fp = footprint_t_shape(10, 15, 30, 5)
        assert _polygon_area_signed(fp) > 0

    def test_area(self) -> None:
        fp = footprint_t_shape(10, 15, 30, 5)
        area = abs(_polygon_area_signed(fp))
        # Stem: 10x15=150, Top bar: 30x5=150 → 300
        assert _close(area, 300.0)

    def test_top_narrower_than_base_raises(self) -> None:
        with pytest.raises(ValueError, match="top_width"):
            footprint_t_shape(20, 10, 10, 5)


class TestFootprintHShape:
    def test_vertex_count(self) -> None:
        fp = footprint_h_shape(30, 20, 10, 5)
        assert len(fp) == 12

    def test_is_ccw(self) -> None:
        fp = footprint_h_shape(30, 20, 10, 5)
        assert _polygon_area_signed(fp) > 0

    def test_area(self) -> None:
        fp = footprint_h_shape(30, 20, 10, 5)
        area = abs(_polygon_area_signed(fp))
        # Overall 30x20=600 minus 2 courtyards 10x5=50 each → 500
        assert _close(area, 500.0)

    def test_courtyard_wider_than_building_raises(self) -> None:
        with pytest.raises(ValueError, match="courtyard_width"):
            footprint_h_shape(20, 20, 25, 5)

    def test_courtyard_too_deep_raises(self) -> None:
        with pytest.raises(ValueError, match="courtyard_depth"):
            footprint_h_shape(20, 20, 5, 11)


class TestFootprintCourtyard:
    def test_vertex_count(self) -> None:
        fp = footprint_courtyard(30, 20, 10, 8)
        assert len(fp) == 10

    def test_inner_wider_than_outer_raises(self) -> None:
        with pytest.raises(ValueError, match="inner_width"):
            footprint_courtyard(20, 20, 20, 5)

    def test_inner_deeper_than_outer_raises(self) -> None:
        with pytest.raises(ValueError, match="inner_depth"):
            footprint_courtyard(20, 20, 5, 20)


# =========================================================================
# Polygon utilities
# =========================================================================


class TestPolygonUtils:
    def test_is_convex_square(self) -> None:
        assert _is_convex(footprint_rectangle(10, 10))

    def test_is_convex_triangle(self) -> None:
        assert _is_convex([(0, 0), (10, 0), (5, 8)])

    def test_l_shape_is_not_convex(self) -> None:
        assert not _is_convex(footprint_l_shape(20, 10, 8, 5))

    def test_polygon_area_signed_ccw(self) -> None:
        area = _polygon_area_signed(footprint_rectangle(10, 5))
        assert _close(area, 50.0)

    def test_inset_polygon_square(self) -> None:
        fp = footprint_rectangle(20, 20)
        inner = _inset_polygon_2d(fp, 3)
        assert inner is not None
        assert len(inner) == 4
        inner_area = abs(_polygon_area_signed(inner))
        assert _close(inner_area, 14 * 14)  # (20-2*3)^2 = 196

    def test_inset_polygon_too_deep_returns_none(self) -> None:
        fp = footprint_rectangle(10, 10)
        # Inset by exactly half the width → collapsed to a point
        assert _inset_polygon_2d(fp, 5) is None

    def test_inset_polygon_exceeds_half_still_has_area(self) -> None:
        """An inset slightly less than half produces a tiny but valid polygon."""
        fp = footprint_rectangle(10, 10)
        inner = _inset_polygon_2d(fp, 4.9)
        assert inner is not None
        assert abs(_polygon_area_signed(inner)) > 0

    def test_classify_edge_south(self) -> None:
        # Edge from (0,0) to (10,0): travels east, outward normal is south
        assert _classify_edge_orientation((0, 0), (10, 0)) == "South"

    def test_classify_edge_east(self) -> None:
        # Edge from (10,0) to (10,10): travels north, outward normal is east
        assert _classify_edge_orientation((10, 0), (10, 10)) == "East"

    def test_classify_edge_north(self) -> None:
        # Edge from (10,10) to (0,10): travels west, outward normal is north
        assert _classify_edge_orientation((10, 10), (0, 10)) == "North"

    def test_classify_edge_west(self) -> None:
        # Edge from (0,10) to (0,0): travels south, outward normal is west
        assert _classify_edge_orientation((0, 10), (0, 0)) == "West"


# =========================================================================
# Core-perimeter splitting
# =========================================================================


class TestSplitCorePerimeter:
    def test_rectangle_produces_5_zones(self) -> None:
        fp = footprint_rectangle(50, 30)
        zones = _split_core_perimeter(fp, 4.57)
        assert len(zones) == 5  # 4 perimeter + 1 core
        suffixes = {z.name_suffix for z in zones}
        assert "Core" in suffixes
        assert any("South" in s for s in suffixes)
        assert any("East" in s for s in suffixes)
        assert any("North" in s for s in suffixes)
        assert any("West" in s for s in suffixes)

    def test_rectangle_core_area(self) -> None:
        fp = footprint_rectangle(50, 30)
        zones = _split_core_perimeter(fp, 5.0)
        core = next(z for z in zones if z.name_suffix == "Core")
        core_area = abs(_polygon_area_signed(core.polygon))
        # Core should be (50-10)x(30-10) = 40x20 = 800
        assert _close(core_area, 800.0)

    def test_perimeter_areas_sum(self) -> None:
        fp = footprint_rectangle(50, 30)
        zones = _split_core_perimeter(fp, 5.0)
        total_perim = sum(abs(_polygon_area_signed(z.polygon)) for z in zones if z.name_suffix != "Core")
        total = abs(_polygon_area_signed(fp))
        core = abs(_polygon_area_signed(next(z for z in zones if z.name_suffix == "Core").polygon))
        assert _close(total_perim, total - core, tol=0.1)

    def test_small_footprint_falls_back(self) -> None:
        """Footprint too small for perimeter depth → single zone."""
        fp = footprint_rectangle(8, 8)
        zones = _split_core_perimeter(fp, 5)  # 5m depth on 8m → bowties
        assert len(zones) == 1
        assert zones[0].name_suffix == "Whole"

    def test_narrow_footprint_still_valid(self) -> None:
        """A footprint with small perimeter depth still splits correctly."""
        fp = footprint_rectangle(6, 6)
        zones = _split_core_perimeter(fp, 2)
        assert len(zones) == 5  # 4 perimeter + core

    def test_concave_footprint_falls_back(self) -> None:
        """Concave (L-shape) falls back to single zone."""
        fp = footprint_l_shape(20, 10, 8, 5)
        zones = _split_core_perimeter(fp, 3)
        assert len(zones) == 1
        assert zones[0].name_suffix == "Whole"

    def test_triangle_produces_4_zones(self) -> None:
        """Triangle: 3 perimeter zones + 1 core."""
        fp = [(0, 0), (30, 0), (15, 26)]  # roughly equilateral
        zones = _split_core_perimeter(fp, 3)
        assert len(zones) == 4  # 3 perimeter + 1 core

    def test_all_zone_polygons_have_positive_area(self) -> None:
        fp = footprint_rectangle(40, 25)
        zones = _split_core_perimeter(fp, ASHRAE_PERIMETER_DEPTH)
        for z in zones:
            area = abs(_polygon_area_signed(z.polygon))
            assert area > 0, f"Zone {z.name_suffix} has zero area"


# =========================================================================
# ZonedBlock dataclass
# =========================================================================


class TestZonedBlock:
    def test_validation_errors(self) -> None:
        with pytest.raises(ValueError, match="at least 3"):
            ZonedBlock(name="X", footprint=[(0, 0)], floor_to_floor=3)

        with pytest.raises(ValueError, match="positive"):
            ZonedBlock(name="X", footprint=[(0, 0), (1, 0), (1, 1)], floor_to_floor=0)

        with pytest.raises(ValueError, match="num_stories"):
            ZonedBlock(name="X", footprint=[(0, 0), (1, 0), (1, 1)], floor_to_floor=3, num_stories=0)

        with pytest.raises(ValueError, match="perimeter_depth"):
            ZonedBlock(
                name="X",
                footprint=[(0, 0), (1, 0), (1, 1)],
                floor_to_floor=3,
                perimeter_depth=-1,
            )

        with pytest.raises(ValueError, match="custom_zones"):
            ZonedBlock(
                name="X",
                footprint=[(0, 0), (1, 0), (1, 1)],
                floor_to_floor=3,
                zoning=ZoningScheme.CUSTOM,
            )

    def test_by_storey_single_story(self) -> None:
        doc = new_document()
        block = ZonedBlock(
            name="Office",
            footprint=footprint_rectangle(50, 30),
            floor_to_floor=3.5,
            zoning=ZoningScheme.BY_STOREY,
        )
        block.build(doc)
        assert len(doc["Zone"]) == 1
        assert doc["Zone"]["Office"] is not None

    def test_by_storey_multi_story(self) -> None:
        doc = new_document()
        block = ZonedBlock(
            name="Tower",
            footprint=footprint_rectangle(20, 20),
            floor_to_floor=3,
            num_stories=5,
            zoning=ZoningScheme.BY_STOREY,
        )
        block.build(doc)
        assert len(doc["Zone"]) == 5


# =========================================================================
# BY_STOREY zoning (via create_building)
# =========================================================================


class TestByStorey:
    def test_single_story(self) -> None:
        doc = new_document()
        objs = create_building(
            doc,
            "Box",
            footprint_rectangle(10, 8),
            floor_to_floor=3,
        )
        assert len(doc["Zone"]) == 1
        # 4 walls + floor + roof = 6 surfaces
        assert len(doc["BuildingSurface:Detailed"]) == 6
        # 1 zone + 6 surfaces
        assert len(objs) == 7

    def test_multi_story(self) -> None:
        doc = new_document()
        create_building(
            doc,
            "Stack",
            footprint_rectangle(10, 10),
            floor_to_floor=3,
            num_stories=3,
        )
        assert len(doc["Zone"]) == 3
        # 3 * (4 walls + floor + ceiling/roof) = 18
        assert len(doc["BuildingSurface:Detailed"]) == 18

    def test_ground_floor_bc(self) -> None:
        doc = new_document()
        create_building(doc, "B", footprint_rectangle(10, 10), floor_to_floor=3)
        floor = doc.getobject("BuildingSurface:Detailed", "B Floor")
        assert floor is not None
        assert floor.outside_boundary_condition == "Ground"

    def test_roof_bc(self) -> None:
        doc = new_document()
        create_building(doc, "B", footprint_rectangle(10, 10), floor_to_floor=3)
        roof = doc.getobject("BuildingSurface:Detailed", "B Roof")
        assert roof is not None
        assert roof.surface_type == "Roof"
        assert roof.outside_boundary_condition == "Outdoors"

    def test_inter_story_boundary(self) -> None:
        doc = new_document()
        create_building(
            doc,
            "T",
            footprint_rectangle(10, 10),
            floor_to_floor=3,
            num_stories=2,
        )
        ceil = doc.getobject("BuildingSurface:Detailed", "T Story 1 Ceiling")
        assert ceil is not None
        assert ceil.outside_boundary_condition == "Surface"
        assert ceil.outside_boundary_condition_object == "T Story 2 Floor"

        floor2 = doc.getobject("BuildingSurface:Detailed", "T Story 2 Floor")
        assert floor2 is not None
        assert floor2.outside_boundary_condition == "Surface"
        assert floor2.outside_boundary_condition_object == "T Story 1 Ceiling"


# =========================================================================
# CORE_PERIMETER zoning (via create_building)
# =========================================================================


class TestCorePerimeter:
    def test_single_story_5_zones(self) -> None:
        doc = new_document()
        create_building(
            doc,
            "Office",
            footprint_rectangle(50, 30),
            floor_to_floor=3.5,
            zoning=ZoningScheme.CORE_PERIMETER,
        )
        assert len(doc["Zone"]) == 5

    def test_zone_names(self) -> None:
        doc = new_document()
        create_building(
            doc,
            "Office",
            footprint_rectangle(50, 30),
            floor_to_floor=3.5,
            zoning=ZoningScheme.CORE_PERIMETER,
        )
        zone_names = {z.name for z in doc["Zone"]}
        assert "Office Core" in zone_names
        assert any("Perimeter_South" in n for n in zone_names)
        assert any("Perimeter_East" in n for n in zone_names)
        assert any("Perimeter_North" in n for n in zone_names)
        assert any("Perimeter_West" in n for n in zone_names)

    def test_multi_story_zone_count(self) -> None:
        doc = new_document()
        create_building(
            doc,
            "Office",
            footprint_rectangle(50, 30),
            floor_to_floor=3.5,
            num_stories=3,
            zoning=ZoningScheme.CORE_PERIMETER,
        )
        assert len(doc["Zone"]) == 15  # 5 zones * 3 stories

    def test_multi_story_zone_names(self) -> None:
        doc = new_document()
        create_building(
            doc,
            "O",
            footprint_rectangle(50, 30),
            floor_to_floor=3.5,
            num_stories=2,
            zoning=ZoningScheme.CORE_PERIMETER,
        )
        zone_names = {z.name for z in doc["Zone"]}
        assert "O Story 1 Core" in zone_names
        assert "O Story 2 Core" in zone_names

    def test_inter_zone_walls_paired(self) -> None:
        """Interior walls between perimeter and core must be paired."""
        doc = new_document()
        create_building(
            doc,
            "B",
            footprint_rectangle(50, 30),
            floor_to_floor=3,
            zoning=ZoningScheme.CORE_PERIMETER,
        )
        interior_walls = [
            s
            for s in doc["BuildingSurface:Detailed"]
            if (getattr(s, "surface_type", "") or "").upper() == "WALL"
            and (getattr(s, "outside_boundary_condition", "") or "").upper() == "SURFACE"
        ]
        # Every interior wall must have a matching partner
        assert len(interior_walls) > 0
        for wall in interior_walls:
            partner_name = wall.outside_boundary_condition_object
            partner = doc.getobject("BuildingSurface:Detailed", partner_name)
            assert partner is not None, f"Missing partner: {partner_name}"
            assert partner.outside_boundary_condition_object == wall.name

    def test_exterior_walls_are_outdoors(self) -> None:
        """Walls on the building perimeter must face Outdoors."""
        doc = new_document()
        create_building(
            doc,
            "B",
            footprint_rectangle(50, 30),
            floor_to_floor=3,
            zoning=ZoningScheme.CORE_PERIMETER,
        )
        for zone in doc["Zone"]:
            if "Perimeter" in zone.name:
                zone_walls = [
                    s
                    for s in doc["BuildingSurface:Detailed"]
                    if (getattr(s, "zone_name", "") or "") == zone.name
                    and (getattr(s, "surface_type", "") or "").upper() == "WALL"
                ]
                has_exterior = any(
                    (getattr(w, "outside_boundary_condition", "") or "").upper() == "OUTDOORS" for w in zone_walls
                )
                assert has_exterior, f"{zone.name} has no exterior wall"

    def test_core_has_no_exterior_walls(self) -> None:
        """Core zone should have no outdoor-facing walls."""
        doc = new_document()
        create_building(
            doc,
            "B",
            footprint_rectangle(50, 30),
            floor_to_floor=3,
            zoning=ZoningScheme.CORE_PERIMETER,
        )
        core_walls = [
            s
            for s in doc["BuildingSurface:Detailed"]
            if (getattr(s, "zone_name", "") or "") == "B Core"
            and (getattr(s, "surface_type", "") or "").upper() == "WALL"
        ]
        for w in core_walls:
            assert (getattr(w, "outside_boundary_condition", "") or "").upper() == "SURFACE"

    def test_total_floor_area_preserved(self) -> None:
        """Sum of zone floor areas equals the footprint area."""
        doc = new_document()
        fp = footprint_rectangle(50, 30)
        create_building(
            doc,
            "B",
            fp,
            floor_to_floor=3,
            zoning=ZoningScheme.CORE_PERIMETER,
        )
        total_floor = sum(
            calculate_surface_area(s)
            for s in doc["BuildingSurface:Detailed"]
            if (getattr(s, "surface_type", "") or "").upper() == "FLOOR"
        )
        expected = abs(_polygon_area_signed(fp))
        assert _close(total_floor, expected, tol=0.1)

    def test_custom_perimeter_depth(self) -> None:
        """A larger perimeter depth means a smaller core."""
        doc1 = new_document()
        create_building(
            doc1,
            "A",
            footprint_rectangle(50, 30),
            floor_to_floor=3,
            zoning=ZoningScheme.CORE_PERIMETER,
            perimeter_depth=3.0,
        )
        doc2 = new_document()
        create_building(
            doc2,
            "A",
            footprint_rectangle(50, 30),
            floor_to_floor=3,
            zoning=ZoningScheme.CORE_PERIMETER,
            perimeter_depth=6.0,
        )
        core1_floor = [
            s
            for s in doc1["BuildingSurface:Detailed"]
            if (getattr(s, "zone_name", "") or "") == "A Core"
            and (getattr(s, "surface_type", "") or "").upper() == "FLOOR"
        ]
        core2_floor = [
            s
            for s in doc2["BuildingSurface:Detailed"]
            if (getattr(s, "zone_name", "") or "") == "A Core"
            and (getattr(s, "surface_type", "") or "").upper() == "FLOOR"
        ]
        area1 = calculate_surface_area(core1_floor[0])
        area2 = calculate_surface_area(core2_floor[0])
        assert area1 > area2

    def test_inter_story_boundary_core(self) -> None:
        """Core zone ceilings/floors are paired across stories."""
        doc = new_document()
        create_building(
            doc,
            "O",
            footprint_rectangle(50, 30),
            floor_to_floor=3.5,
            num_stories=2,
            zoning=ZoningScheme.CORE_PERIMETER,
        )
        ceil = doc.getobject("BuildingSurface:Detailed", "O Story 1 Core Ceiling")
        assert ceil is not None
        assert ceil.outside_boundary_condition == "Surface"
        assert ceil.outside_boundary_condition_object == "O Story 2 Core Floor"

    def test_small_footprint_degrades_gracefully(self) -> None:
        """Footprint too small for core-perimeter → single zone per floor."""
        doc = new_document()
        create_building(
            doc,
            "Tiny",
            footprint_rectangle(8, 8),
            floor_to_floor=3,
            zoning=ZoningScheme.CORE_PERIMETER,
            perimeter_depth=5,
        )
        # Should fall back to 1 zone since 5m on 8m causes bowtie quads
        assert len(doc["Zone"]) == 1


# =========================================================================
# CUSTOM zoning
# =========================================================================


class TestCustomZoning:
    def test_custom_zones(self) -> None:
        doc = new_document()
        custom = [
            _ZoneFootprint("East_Wing", [(0, 0), (10, 0), (10, 10), (0, 10)]),
            _ZoneFootprint("West_Wing", [(10, 0), (20, 0), (20, 10), (10, 10)]),
        ]
        create_building(
            doc,
            "Building",
            footprint_rectangle(20, 10),
            floor_to_floor=3,
            zoning=ZoningScheme.CUSTOM,
            custom_zones=custom,
        )
        assert len(doc["Zone"]) == 2
        zone_names = {z.name for z in doc["Zone"]}
        assert "Building East_Wing" in zone_names
        assert "Building West_Wing" in zone_names


# =========================================================================
# Air boundary support
# =========================================================================


class TestAirBoundary:
    def test_air_boundary_created(self) -> None:
        doc = new_document()
        create_building(
            doc,
            "Open",
            footprint_rectangle(50, 30),
            floor_to_floor=3,
            zoning=ZoningScheme.CORE_PERIMETER,
            air_boundary=True,
        )
        # Construction:AirBoundary object should exist
        air_boundaries = list(doc["Construction:AirBoundary"])
        assert len(air_boundaries) == 1

    def test_interior_walls_use_air_boundary(self) -> None:
        doc = new_document()
        create_building(
            doc,
            "Open",
            footprint_rectangle(50, 30),
            floor_to_floor=3,
            zoning=ZoningScheme.CORE_PERIMETER,
            air_boundary=True,
        )
        interior_walls = [
            s
            for s in doc["BuildingSurface:Detailed"]
            if (getattr(s, "surface_type", "") or "").upper() == "WALL"
            and (getattr(s, "outside_boundary_condition", "") or "").upper() == "SURFACE"
        ]
        for wall in interior_walls:
            assert wall.construction_name == "Air Boundary"

    def test_exterior_walls_not_air_boundary(self) -> None:
        doc = new_document()
        create_building(
            doc,
            "Open",
            footprint_rectangle(50, 30),
            floor_to_floor=3,
            zoning=ZoningScheme.CORE_PERIMETER,
            air_boundary=True,
        )
        exterior_walls = [
            s
            for s in doc["BuildingSurface:Detailed"]
            if (getattr(s, "surface_type", "") or "").upper() == "WALL"
            and (getattr(s, "outside_boundary_condition", "") or "").upper() == "OUTDOORS"
        ]
        for wall in exterior_walls:
            assert wall.construction_name != "Air Boundary"

    def test_no_air_boundary_by_default(self) -> None:
        doc = new_document()
        create_building(
            doc,
            "B",
            footprint_rectangle(50, 30),
            floor_to_floor=3,
            zoning=ZoningScheme.CORE_PERIMETER,
        )
        assert len(list(doc["Construction:AirBoundary"])) == 0


# =========================================================================
# Default perimeter depth
# =========================================================================


class TestDefaultPerimeterDepth:
    def test_ashrae_default(self) -> None:
        assert _close(ASHRAE_PERIMETER_DEPTH, 4.57, tol=0.01)

    def test_default_used_by_create_building(self) -> None:
        """Verify the default perimeter depth is ASHRAE 4.57 m."""
        doc = new_document()
        fp = footprint_rectangle(50, 30)
        create_building(
            doc,
            "B",
            fp,
            floor_to_floor=3,
            zoning=ZoningScheme.CORE_PERIMETER,
        )
        # With 4.57m depth on 50x30: core = (50-2*4.57)x(30-2*4.57)
        core_floors = [
            s
            for s in doc["BuildingSurface:Detailed"]
            if (getattr(s, "zone_name", "") or "") == "B Core"
            and (getattr(s, "surface_type", "") or "").upper() == "FLOOR"
        ]
        assert len(core_floors) == 1
        core_area = calculate_surface_area(core_floors[0])
        expected = (50 - 2 * 4.57) * (30 - 2 * 4.57)
        assert _close(core_area, expected, tol=1.0)


# =========================================================================
# Wall geometry correctness
# =========================================================================


class TestWallGeometry:
    def test_exterior_wall_area(self) -> None:
        doc = new_document()
        create_building(
            doc,
            "B",
            footprint_rectangle(10, 8),
            floor_to_floor=3,
        )
        south_wall = doc.getobject("BuildingSurface:Detailed", "B Wall 1")
        assert south_wall is not None
        area = calculate_surface_area(south_wall)
        # Edge (0,0)→(10,0), height 3 → 30 m²
        assert _close(area, 30.0, tol=0.1)

    def test_wall_height(self) -> None:
        doc = new_document()
        create_building(
            doc,
            "B",
            footprint_rectangle(10, 8),
            floor_to_floor=4.2,
        )
        wall = doc.getobject("BuildingSurface:Detailed", "B Wall 1")
        assert wall is not None
        coords = get_surface_coords(wall)
        assert coords is not None
        z_values = sorted({v.z for v in coords.vertices})
        assert _close(z_values[0], 0.0)
        assert _close(z_values[1], 4.2)

    def test_core_perimeter_wall_heights(self) -> None:
        """All walls in core-perimeter mode should have correct height."""
        doc = new_document()
        create_building(
            doc,
            "B",
            footprint_rectangle(50, 30),
            floor_to_floor=3,
            zoning=ZoningScheme.CORE_PERIMETER,
        )
        for s in doc["BuildingSurface:Detailed"]:
            st = (getattr(s, "surface_type", "") or "").upper()
            if st != "WALL":
                continue
            coords = get_surface_coords(s)
            assert coords is not None
            z_vals = sorted({v.z for v in coords.vertices})
            assert len(z_vals) == 2
            assert _close(z_vals[1] - z_vals[0], 3.0, tol=0.01)


# =========================================================================
# Footprint generator origin support
# =========================================================================


class TestOriginSupport:
    def test_rectangle_origin(self) -> None:
        fp = footprint_rectangle(10, 5, origin=(100, 200))
        assert fp[0] == (100.0, 200.0)
        assert fp[2] == (110.0, 205.0)

    def test_l_shape_origin(self) -> None:
        fp = footprint_l_shape(20, 10, 8, 5, origin=(50, 50))
        assert fp[0] == (50, 50)
