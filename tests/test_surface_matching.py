"""Tests for robust intersect-and-match (idfkit.surface_matching)."""

from __future__ import annotations

import pytest

from idfkit import MatchOptions, MatchReport, intersect_and_match, new_document
from idfkit.document import IDFDocument
from idfkit.geometry import get_surface_coords
from idfkit.objects import IDFObject
from idfkit.surface_matching import (
    _clean_poly,
    _convex_difference,
    _difference_many,
    _is_convex,
    _signed_area,
    _triangulate,
)

# ---------------------------------------------------------------------------
# 2-D kernel unit tests
# ---------------------------------------------------------------------------

Poly = list[tuple[float, float]]


def _area(poly: Poly) -> float:
    return abs(_signed_area(poly))


class TestConvexDifferenceKernel:
    def test_shared_edge(self) -> None:
        """Subtracting an edge-sharing half leaves the complementary half."""
        square: Poly = [(0, 0), (2, 0), (2, 2), (0, 2)]
        left: Poly = [(0, 0), (1, 0), (1, 2), (0, 2)]
        pieces = _convex_difference(square, left)
        assert sum(_area(p) for p in pieces) == pytest.approx(2.0)
        assert all(_is_convex(p) for p in pieces)

    def test_disjoint_bbox_returns_subject(self) -> None:
        square: Poly = [(0, 0), (1, 0), (1, 1), (0, 1)]
        far: Poly = [(5, 5), (6, 5), (6, 6), (5, 6)]
        pieces = _convex_difference(square, far)
        assert len(pieces) == 1
        assert _area(pieces[0]) == pytest.approx(1.0)

    def test_interior_hole_frame(self) -> None:
        """Subtracting a fully-interior cutter yields a convex-tiled frame."""
        big: Poly = [(0, 0), (10, 0), (10, 3), (0, 3)]
        inner: Poly = [(4, 0), (5, 0), (5, 1), (4, 1)]
        pieces = _convex_difference(big, inner)
        assert sum(_area(p) for p in pieces) == pytest.approx(30.0 - 1.0)
        assert all(_is_convex(p) for p in pieces)

    def test_one_to_many_full_coverage(self) -> None:
        host: Poly = [(0, 0), (10, 0), (10, 3), (0, 3)]
        n1: Poly = [(0, 0), (5, 0), (5, 3), (0, 3)]
        n2: Poly = [(5, 0), (10, 0), (10, 3), (5, 3)]
        remainder = _difference_many(host, [n1, n2])
        assert sum(_area(p) for p in remainder) == pytest.approx(0.0, abs=1e-9)

    def test_one_to_many_partial(self) -> None:
        host: Poly = [(0, 0), (10, 0), (10, 3), (0, 3)]
        n1: Poly = [(0, 0), (5, 0), (5, 2), (0, 2)]
        n2: Poly = [(5, 0), (10, 0), (10, 2), (5, 2)]
        remainder = _difference_many(host, [n1, n2])
        assert sum(_area(p) for p in remainder) == pytest.approx(10.0)
        assert all(_is_convex(p) for p in remainder)

    def test_concave_cutter_triangulated(self) -> None:
        """An L-shaped (concave) cutter is handled via triangulation."""
        big: Poly = [(0, 0), (10, 0), (10, 10), (0, 10)]
        ell: Poly = [(0, 0), (6, 0), (6, 4), (4, 4), (4, 8), (0, 8)]
        assert not _is_convex(ell)
        remainder = _difference_many(big, [ell])
        assert sum(_area(p) for p in remainder) == pytest.approx(100.0 - _area(ell))

    def test_triangulate_tiles_polygon(self) -> None:
        ell: Poly = [(0, 0), (6, 0), (6, 4), (4, 4), (4, 8), (0, 8)]
        tris = _triangulate(ell)
        assert sum(_area(t) for t in tris) == pytest.approx(_area(ell))
        assert all(len(t) == 3 for t in tris)

    def test_clean_poly_drops_collinear(self) -> None:
        poly: Poly = [(0, 0), (1, 0), (2, 0), (2, 2), (0, 2)]
        cleaned = _clean_poly(poly)
        assert len(cleaned) == 4


# ---------------------------------------------------------------------------
# Integration helpers
# ---------------------------------------------------------------------------


def _wall(
    doc: IDFDocument,
    name: str,
    zone: str,
    verts: list[tuple[float, float, float]],
    *,
    surface_type: str = "Wall",
    bc: str = "Outdoors",
) -> IDFObject:
    return doc.add(
        "BuildingSurface:Detailed",
        name,
        {
            "surface_type": surface_type,
            "zone_name": zone,
            "construction_name": "",
            "outside_boundary_condition": bc,
            "sun_exposure": "SunExposed",
            "wind_exposure": "WindExposed",
            "number_of_vertices": len(verts),
            "vertices": [
                {"vertex_x_coordinate": x, "vertex_y_coordinate": y, "vertex_z_coordinate": z} for (x, y, z) in verts
            ],
        },
        validate=False,
    )


def _window(doc: IDFDocument, name: str, base: str, verts: list[tuple[float, float, float]]) -> IDFObject:
    return doc.add(
        "FenestrationSurface:Detailed",
        name,
        {
            "surface_type": "Window",
            "building_surface_name": base,
            "number_of_vertices": len(verts),
            "vertices": [
                {"vertex_x_coordinate": x, "vertex_y_coordinate": y, "vertex_z_coordinate": z} for (x, y, z) in verts
            ],
        },
        validate=False,
    )


def _long_wall_two_zones() -> IDFDocument:
    doc = new_document(version=(24, 1, 0))
    for z in ("A", "B", "C"):
        doc.add("Zone", z, {})
    # Zone A long wall on y=0, x 0..10, z 0..3 (normal -Y)
    _wall(doc, "A_east", "A", [(0, 0, 3), (0, 0, 0), (10, 0, 0), (10, 0, 3)])
    # Neighbours on the opposite side (normal +Y), sharing edge x=5
    _wall(doc, "B_west", "B", [(5, 0, 3), (5, 0, 0), (0, 0, 0), (0, 0, 3)])
    _wall(doc, "C_west", "C", [(10, 0, 3), (10, 0, 0), (5, 0, 0), (5, 0, 3)])
    return doc


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------


class TestIntersectAndMatch:
    def test_one_to_many_split(self) -> None:
        doc = _long_wall_two_zones()
        report = intersect_and_match(doc)
        assert isinstance(report, MatchReport)
        assert report.pairs_matched == 2
        assert report.surfaces_split == 1
        assert report.fragments_created == 1

        surfaces = {s.name: s for s in doc["BuildingSurface:Detailed"]}
        assert len(surfaces) == 4  # A_east split into A_east + one new fragment
        # Both neighbours are now interior, each referencing an A-side fragment.
        b, c = surfaces["B_west"], surfaces["C_west"]
        assert b.outside_boundary_condition == "Surface"
        assert c.outside_boundary_condition == "Surface"
        a_side = {surfaces[b.outside_boundary_condition_object], surfaces[c.outside_boundary_condition_object]}
        assert len(a_side) == 2  # two distinct A fragments
        for frag in a_side:
            assert frag.zone_name == "A"
            assert frag.outside_boundary_condition == "Surface"
            assert get_surface_coords(frag).area == pytest.approx(15.0)

    def test_matched_pair_has_reversed_normals(self) -> None:
        doc = _long_wall_two_zones()
        intersect_and_match(doc)
        surfaces = {s.name: s for s in doc["BuildingSurface:Detailed"]}
        b = surfaces["B_west"]
        partner = surfaces[b.outside_boundary_condition_object]
        nb = get_surface_coords(b).normal
        npart = get_surface_coords(partner).normal
        assert nb.dot(npart) == pytest.approx(-1.0, abs=1e-6)

    def test_area_conserved_on_split(self) -> None:
        doc = _long_wall_two_zones()
        intersect_and_match(doc)
        a_area = sum(get_surface_coords(s).area for s in doc["BuildingSurface:Detailed"] if s.zone_name == "A")
        assert a_area == pytest.approx(30.0)

    def test_idempotent(self) -> None:
        doc = _long_wall_two_zones()
        intersect_and_match(doc)
        count_after_first = len(list(doc["BuildingSurface:Detailed"]))
        report2 = intersect_and_match(doc)
        count_after_second = len(list(doc["BuildingSurface:Detailed"]))
        assert count_after_second == count_after_first
        assert report2.surfaces_split == 0
        assert report2.fragments_created == 0

    def test_congruent_match_no_split(self) -> None:
        """Two equal opposing walls match without creating new surfaces."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "A", {})
        doc.add("Zone", "B", {})
        _wall(doc, "A_w", "A", [(0, 0, 3), (0, 0, 0), (5, 0, 0), (5, 0, 3)])
        _wall(doc, "B_w", "B", [(5, 0, 3), (5, 0, 0), (0, 0, 0), (0, 0, 3)])
        report = intersect_and_match(doc)
        assert report.pairs_matched == 1
        assert report.fragments_created == 0
        assert len(list(doc["BuildingSurface:Detailed"])) == 2
        a = doc.getobject("BuildingSurface:Detailed", "A_w")
        assert a.outside_boundary_condition == "Surface"
        assert a.outside_boundary_condition_object == "B_w"

    def test_horizontal_floor_ceiling_match(self) -> None:
        """Stacked zones: a ceiling and the floor above match across z."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Lower", {})
        doc.add("Zone", "Upper", {})
        # Lower zone ceiling at z=3, outward normal +Z
        _wall(
            doc,
            "Lower_ceiling",
            "Lower",
            [(0, 0, 3), (5, 0, 3), (5, 5, 3), (0, 5, 3)],
            surface_type="Ceiling",
        )
        # Upper zone floor at z=3, outward normal -Z (reversed winding)
        _wall(
            doc,
            "Upper_floor",
            "Upper",
            [(0, 0, 3), (0, 5, 3), (5, 5, 3), (5, 0, 3)],
            surface_type="Floor",
        )
        report = intersect_and_match(doc)
        assert report.pairs_matched == 1
        ceiling = doc.getobject("BuildingSurface:Detailed", "Lower_ceiling")
        assert ceiling.outside_boundary_condition == "Surface"
        assert ceiling.outside_boundary_condition_object == "Upper_floor"

    def test_same_zone_not_matched(self) -> None:
        """Opposite-facing surfaces in the same zone are not matched by default."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "A", {})
        _wall(doc, "w1", "A", [(0, 0, 3), (0, 0, 0), (5, 0, 0), (5, 0, 3)])
        _wall(doc, "w2", "A", [(5, 0, 3), (5, 0, 0), (0, 0, 0), (0, 0, 3)])
        report = intersect_and_match(doc)
        assert report.pairs_matched == 0
        w1 = doc.getobject("BuildingSurface:Detailed", "w1")
        assert w1.outside_boundary_condition == "Outdoors"


class TestFenestration:
    def test_window_rehomed_to_correct_fragment(self) -> None:
        doc = _long_wall_two_zones()
        # Window on A_east in the C-side half (x 6..9), inset from edges.
        _window(doc, "A_win", "A_east", [(6, 0, 2.5), (6, 0, 0.5), (9, 0, 0.5), (9, 0, 2.5)])
        intersect_and_match(doc)
        win = doc.getobject("FenestrationSurface:Detailed", "A_win")
        host_name = win.building_surface_name
        host = doc.getobject("BuildingSurface:Detailed", host_name)
        # The window's host fragment is the one matched to C_west (x 5..10).
        assert host.outside_boundary_condition_object == "C_west"

    def test_straddling_window_blocks_split(self) -> None:
        doc = _long_wall_two_zones()
        # Window spanning the x=5 cut line -> straddles two fragments.
        _window(doc, "A_win", "A_east", [(3, 0, 2.5), (3, 0, 0.5), (7, 0, 0.5), (7, 0, 2.5)])
        report = intersect_and_match(doc)
        assert "A_east" in report.fenestration_conflicts
        # A_east left intact and exterior; neighbours not matched to it.
        surfaces = list(doc["BuildingSurface:Detailed"])
        assert len(surfaces) == 3  # no split occurred
        a = doc.getobject("BuildingSurface:Detailed", "A_east")
        assert a.outside_boundary_condition == "Outdoors"


class TestOptions:
    def test_match_same_zone_option(self) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "A", {})
        _wall(doc, "w1", "A", [(0, 0, 3), (0, 0, 0), (5, 0, 0), (5, 0, 3)])
        _wall(doc, "w2", "A", [(5, 0, 3), (5, 0, 0), (0, 0, 0), (0, 0, 3)])
        report = intersect_and_match(doc, MatchOptions(match_same_zone=True))
        assert report.pairs_matched == 1

    def test_surface_classes_filter(self) -> None:
        """Restricting to walls leaves floors/ceilings untouched."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Lower", {})
        doc.add("Zone", "Upper", {})
        _wall(doc, "c", "Lower", [(0, 0, 3), (5, 0, 3), (5, 5, 3), (0, 5, 3)], surface_type="Ceiling")
        _wall(doc, "f", "Upper", [(0, 0, 3), (0, 5, 3), (5, 5, 3), (5, 0, 3)], surface_type="Floor")
        report = intersect_and_match(doc, MatchOptions(surface_classes=("WALL",)))
        assert report.pairs_matched == 0
