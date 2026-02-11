"""Tests for eppy feature parity additions.

Tests cover:
- Surface tilt & azimuth
- Zone height, ceiling area
- get_referenced_object / getreferingobjs
- getrange / checkrange
- popidfobject
- saveas / savecopy / save
- Building-level translate / rotate
- IDF output formatting modes (nocomment, compressed)
- JSON batch updates (doc.update)
- HTML tabular output parser
"""

from __future__ import annotations

from pathlib import Path

import pytest

from idfkit import IDFDocument, new_document
from idfkit.exceptions import RangeError
from idfkit.geometry import (
    Polygon3D,
    Vector3D,
    calculate_surface_azimuth,
    calculate_surface_tilt,
    calculate_zone_ceiling_area,
    calculate_zone_height,
    rotate_building,
    translate_building,
)
from idfkit.objects import IDFObject
from idfkit.writers import write_idf

_TOL = 1e-6


def _close(a: float, b: float, tol: float = _TOL) -> bool:
    return abs(a - b) < tol


# ---------------------------------------------------------------------------
# Polygon3D tilt & azimuth
# ---------------------------------------------------------------------------


class TestTiltAzimuth:
    def test_horizontal_ceiling_tilt_zero(self) -> None:
        """Horizontal roof/ceiling (normal pointing up) -> tilt 0."""
        # CCW winding viewed from above produces upward normal
        poly = Polygon3D([
            Vector3D(0, 0, 3),
            Vector3D(10, 0, 3),
            Vector3D(10, 10, 3),
            Vector3D(0, 10, 3),
        ])
        assert _close(poly.tilt, 0.0)

    def test_vertical_wall_tilt_90(self) -> None:
        """Vertical wall -> tilt ~90."""
        # Wall in XZ plane, normal pointing in -Y direction
        poly = Polygon3D([
            Vector3D(0, 0, 3),
            Vector3D(0, 0, 0),
            Vector3D(10, 0, 0),
            Vector3D(10, 0, 3),
        ])
        assert _close(poly.tilt, 90.0)

    def test_floor_tilt_180(self) -> None:
        """Floor (normal pointing down) -> tilt 180."""
        # EnergyPlus floor winding: vertices go counter-clockwise when
        # viewed from above, so normal points downward.
        poly = Polygon3D([
            Vector3D(0, 0, 0),
            Vector3D(0, 10, 0),
            Vector3D(10, 10, 0),
            Vector3D(10, 0, 0),
        ])
        assert _close(poly.tilt, 180.0)

    def test_south_wall_azimuth_180(self) -> None:
        """South-facing wall -> azimuth 180."""
        # Normal points in -Y direction (south in E+ convention)
        poly = Polygon3D([
            Vector3D(0, 0, 3),
            Vector3D(0, 0, 0),
            Vector3D(10, 0, 0),
            Vector3D(10, 0, 3),
        ])
        assert _close(poly.azimuth, 180.0)

    def test_north_wall_azimuth_0(self) -> None:
        """North-facing wall -> azimuth 0."""
        poly = Polygon3D([
            Vector3D(10, 10, 3),
            Vector3D(10, 10, 0),
            Vector3D(0, 10, 0),
            Vector3D(0, 10, 3),
        ])
        assert _close(poly.azimuth, 0.0, tol=0.1)

    def test_east_wall_azimuth_90(self) -> None:
        """East-facing wall (normal in +X direction) -> azimuth 90."""
        poly = Polygon3D([
            Vector3D(10, 0, 3),
            Vector3D(10, 0, 0),
            Vector3D(10, 10, 0),
            Vector3D(10, 10, 3),
        ])
        assert _close(poly.azimuth, 90.0)

    def test_west_wall_azimuth_270(self) -> None:
        """West-facing wall (normal in -X direction) -> azimuth 270."""
        poly = Polygon3D([
            Vector3D(0, 10, 3),
            Vector3D(0, 10, 0),
            Vector3D(0, 0, 0),
            Vector3D(0, 0, 3),
        ])
        assert _close(poly.azimuth, 270.0)

    def test_horizontal_surface_azimuth_zero(self) -> None:
        """Horizontal surface -> azimuth 0 (by convention)."""
        poly = Polygon3D([
            Vector3D(0, 0, 3),
            Vector3D(10, 0, 3),
            Vector3D(10, 10, 3),
            Vector3D(0, 10, 3),
        ])
        assert _close(poly.azimuth, 0.0)


class TestSurfaceTiltAzimuthHelpers:
    def test_calculate_surface_tilt(self) -> None:
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
        assert _close(calculate_surface_tilt(surface), 90.0)

    def test_calculate_surface_azimuth(self) -> None:
        surface = IDFObject(
            obj_type="BuildingSurface:Detailed",
            name="SouthWall",
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
        assert _close(calculate_surface_azimuth(surface), 180.0)

    def test_no_coords_returns_zero(self) -> None:
        surface = IDFObject(obj_type="BuildingSurface:Detailed", name="Empty", data={})
        assert calculate_surface_tilt(surface) == 0.0
        assert calculate_surface_azimuth(surface) == 0.0


# ---------------------------------------------------------------------------
# Zone height & ceiling area
# ---------------------------------------------------------------------------


class TestZoneHeight:
    def test_zone_height(self, simple_doc: IDFDocument) -> None:
        height = calculate_zone_height(simple_doc, "TestZone")
        assert _close(height, 3.0)

    def test_zone_height_no_surfaces(self, empty_doc: IDFDocument) -> None:
        empty_doc.add("Zone", "EmptyZone")
        height = calculate_zone_height(empty_doc, "EmptyZone")
        assert height == 0.0


class TestZoneCeilingArea:
    def test_ceiling_area(self) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1")
        doc.add("Construction", "C1", validate=False)
        doc.add(
            "BuildingSurface:Detailed",
            "Roof1",
            {
                "surface_type": "Roof",
                "construction_name": "C1",
                "zone_name": "Z1",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertex_1_x_coordinate": 0.0,
                "vertex_1_y_coordinate": 0.0,
                "vertex_1_z_coordinate": 3.0,
                "vertex_2_x_coordinate": 10.0,
                "vertex_2_y_coordinate": 0.0,
                "vertex_2_z_coordinate": 3.0,
                "vertex_3_x_coordinate": 10.0,
                "vertex_3_y_coordinate": 5.0,
                "vertex_3_z_coordinate": 3.0,
                "vertex_4_x_coordinate": 0.0,
                "vertex_4_y_coordinate": 5.0,
                "vertex_4_z_coordinate": 3.0,
            },
        )
        area = calculate_zone_ceiling_area(doc, "Z1")
        assert _close(area, 50.0)

    def test_ceiling_area_no_ceilings(self, simple_doc: IDFDocument) -> None:
        # simple_doc has a floor and wall but no ceiling
        area = calculate_zone_ceiling_area(simple_doc, "TestZone")
        assert area == 0.0


# ---------------------------------------------------------------------------
# get_referenced_object
# ---------------------------------------------------------------------------


class TestGetReferencedObject:
    def test_follow_reference(self, simple_doc: IDFDocument) -> None:
        wall = simple_doc.getobject("BuildingSurface:Detailed", "TestWall")
        assert wall is not None
        zone = wall.get_referenced_object("zone_name")
        assert zone is not None
        assert zone.name == "TestZone"

    def test_follow_construction_reference(self, simple_doc: IDFDocument) -> None:
        wall = simple_doc.getobject("BuildingSurface:Detailed", "TestWall")
        assert wall is not None
        construction = wall.get_referenced_object("construction_name")
        assert construction is not None
        assert construction.name == "TestConstruction"

    def test_missing_reference_returns_none(self, simple_doc: IDFDocument) -> None:
        zone = simple_doc.getobject("Zone", "TestZone")
        assert zone is not None
        # Zone has no reference field called "nonexistent"
        assert zone.get_referenced_object("nonexistent") is None

    def test_no_document_returns_none(self) -> None:
        obj = IDFObject(obj_type="Zone", name="Z", data={"zone_name": "Foo"})
        assert obj.get_referenced_object("zone_name") is None


# ---------------------------------------------------------------------------
# getreferingobjs
# ---------------------------------------------------------------------------


class TestGetReferingObjs:
    def test_find_referencing_objects(self, simple_doc: IDFDocument) -> None:
        zone = simple_doc.getobject("Zone", "TestZone")
        assert zone is not None
        refs = zone.getreferingobjs()
        # Should find TestWall and TestFloor (both reference TestZone)
        ref_names = {obj.name for obj in refs}
        assert "TestWall" in ref_names
        assert "TestFloor" in ref_names

    def test_filter_by_fields(self, simple_doc: IDFDocument) -> None:
        zone = simple_doc.getobject("Zone", "TestZone")
        assert zone is not None
        refs = zone.getreferingobjs(fields=["zone_name"])
        assert len(refs) >= 2

    def test_no_references(self, simple_doc: IDFDocument) -> None:
        floor = simple_doc.getobject("BuildingSurface:Detailed", "TestFloor")
        assert floor is not None
        refs = floor.getreferingobjs()
        assert len(refs) == 0

    def test_no_document(self) -> None:
        obj = IDFObject(obj_type="Zone", name="Z")
        assert obj.getreferingobjs() == []


# ---------------------------------------------------------------------------
# getrange / checkrange
# ---------------------------------------------------------------------------


class TestRangeChecking:
    def test_getrange_returns_constraints(self, simple_doc: IDFDocument) -> None:
        mat = simple_doc.getobject("Material", "TestMaterial")
        assert mat is not None
        rng = mat.getrange("thickness")
        # Thickness has exclusiveMinimum of 0 in the schema
        assert "exclusiveMinimum" in rng or "minimum" in rng

    def test_getrange_no_constraints(self) -> None:
        obj = IDFObject(obj_type="Zone", name="Z", data={})
        assert obj.getrange("nonexistent") == {}

    def test_checkrange_valid(self, simple_doc: IDFDocument) -> None:
        mat = simple_doc.getobject("Material", "TestMaterial")
        assert mat is not None
        assert mat.checkrange("thickness") is True

    def test_checkrange_raises_on_violation(self, simple_doc: IDFDocument) -> None:
        mat = simple_doc.getobject("Material", "TestMaterial")
        assert mat is not None
        mat.thickness = -1.0
        with pytest.raises(RangeError):
            mat.checkrange("thickness")

    def test_checkrange_non_numeric_returns_true(self, simple_doc: IDFDocument) -> None:
        mat = simple_doc.getobject("Material", "TestMaterial")
        assert mat is not None
        assert mat.checkrange("roughness") is True


# ---------------------------------------------------------------------------
# popidfobject
# ---------------------------------------------------------------------------


class TestPopIdfObject:
    def test_pop_by_index(self, simple_doc: IDFDocument) -> None:
        initial_count = len(simple_doc["BuildingSurface:Detailed"])
        obj = simple_doc.popidfobject("BuildingSurface:Detailed", 0)
        assert obj.name == "TestWall"
        assert len(simple_doc["BuildingSurface:Detailed"]) == initial_count - 1

    def test_pop_out_of_range(self, simple_doc: IDFDocument) -> None:
        with pytest.raises(IndexError):
            simple_doc.popidfobject("BuildingSurface:Detailed", 999)


# ---------------------------------------------------------------------------
# saveas / savecopy / save
# ---------------------------------------------------------------------------


class TestSaveMethods:
    def test_saveas(self, simple_doc: IDFDocument, tmp_path: Path) -> None:
        target = tmp_path / "out.idf"
        simple_doc.saveas(target)
        assert target.exists()
        assert simple_doc.filepath == target

    def test_savecopy(self, simple_doc: IDFDocument, tmp_path: Path) -> None:
        original = simple_doc.filepath
        target = tmp_path / "copy.idf"
        simple_doc.savecopy(target)
        assert target.exists()
        assert simple_doc.filepath == original  # unchanged

    def test_save_with_filepath(self, simple_doc: IDFDocument, tmp_path: Path) -> None:
        target = tmp_path / "saved.idf"
        simple_doc.save(target)
        assert target.exists()

    def test_save_no_filepath_raises(self) -> None:
        doc = new_document()
        with pytest.raises(ValueError, match="No filepath"):
            doc.save()


# ---------------------------------------------------------------------------
# Building-level translate / rotate
# ---------------------------------------------------------------------------


class TestBuildingTransform:
    def test_translate_building(self, simple_doc: IDFDocument) -> None:
        wall = simple_doc.getobject("BuildingSurface:Detailed", "TestWall")
        assert wall is not None
        orig_x = wall.vertex_1_x_coordinate

        translate_building(simple_doc, Vector3D(100, 0, 0))

        assert _close(wall.vertex_1_x_coordinate, orig_x + 100)

    def test_rotate_building(self) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1")
        doc.add("Construction", "C1", validate=False)
        doc.add(
            "BuildingSurface:Detailed",
            "Wall",
            {
                "surface_type": "Wall",
                "construction_name": "C1",
                "zone_name": "Z1",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertex_1_x_coordinate": 10.0,
                "vertex_1_y_coordinate": 0.0,
                "vertex_1_z_coordinate": 3.0,
                "vertex_2_x_coordinate": 10.0,
                "vertex_2_y_coordinate": 0.0,
                "vertex_2_z_coordinate": 0.0,
                "vertex_3_x_coordinate": 0.0,
                "vertex_3_y_coordinate": 0.0,
                "vertex_3_z_coordinate": 0.0,
                "vertex_4_x_coordinate": 0.0,
                "vertex_4_y_coordinate": 0.0,
                "vertex_4_z_coordinate": 3.0,
            },
        )
        rotate_building(doc, 90)
        wall = doc.getobject("BuildingSurface:Detailed", "Wall")
        assert wall is not None
        # After 90 degree rotation around origin, (10,0) -> (0,10)
        assert _close(wall.vertex_1_x_coordinate, 0.0, tol=1e-5)
        assert _close(wall.vertex_1_y_coordinate, 10.0, tol=1e-5)


# ---------------------------------------------------------------------------
# IDF output formatting modes
# ---------------------------------------------------------------------------


class TestOutputFormattingModes:
    def test_nocomment_mode(self, simple_doc: IDFDocument) -> None:
        content = write_idf(simple_doc, output_type="nocomment")
        assert content is not None
        assert "!-" not in content.split("\n")[3]  # No field comments

    def test_compressed_mode(self, simple_doc: IDFDocument) -> None:
        content = write_idf(simple_doc, output_type="compressed")
        assert content is not None
        # Compressed: no "!-" comments, and objects on single lines
        for line in content.split("\n"):
            if line.strip() and not line.startswith("!"):
                assert "!-" not in line

    def test_standard_mode_default(self, simple_doc: IDFDocument) -> None:
        content = write_idf(simple_doc)
        assert content is not None
        assert "!-" in content


# ---------------------------------------------------------------------------
# JSON batch updates
# ---------------------------------------------------------------------------


class TestBatchUpdate:
    def test_update_single_field(self, simple_doc: IDFDocument) -> None:
        simple_doc.update({"Zone.TestZone.x_origin": 42.0})
        zone = simple_doc.getobject("Zone", "TestZone")
        assert zone is not None
        assert zone.x_origin == 42.0

    def test_update_multiple_fields(self, simple_doc: IDFDocument) -> None:
        simple_doc.update({
            "Zone.TestZone.x_origin": 1.0,
            "Zone.TestZone.y_origin": 2.0,
        })
        zone = simple_doc.getobject("Zone", "TestZone")
        assert zone is not None
        assert zone.x_origin == 1.0
        assert zone.y_origin == 2.0

    def test_update_missing_object_raises(self, simple_doc: IDFDocument) -> None:
        with pytest.raises(KeyError, match="NonExistent"):
            simple_doc.update({"Zone.NonExistent.x_origin": 0.0})

    def test_update_bad_key_format(self, simple_doc: IDFDocument) -> None:
        with pytest.raises(KeyError, match="Expected"):
            simple_doc.update({"bad_key": 0.0})


# ---------------------------------------------------------------------------
# HTML tabular output parser
# ---------------------------------------------------------------------------


class TestHTMLParser:
    SAMPLE_HTML = """<html><body>
    <b>Annual Building Utility Performance Summary</b>
    <p><b>For: Entire Facility</b></p>
    <b>Site and Source Energy</b>
    <table>
      <tr><th></th><th>Total Energy [GJ]</th><th>Energy Per Total Building Area [MJ/m2]</th></tr>
      <tr><td>Total Site Energy</td><td>100.50</td><td>50.25</td></tr>
      <tr><td>Net Site Energy</td><td>90.00</td><td>45.00</td></tr>
    </table>
    <b>End Uses</b>
    <table>
      <tr><th></th><th>Electricity [GJ]</th><th>Natural Gas [GJ]</th></tr>
      <tr><td>Heating</td><td>10.0</td><td>20.0</td></tr>
      <tr><td>Cooling</td><td>30.0</td><td>0.0</td></tr>
    </table>
    </body></html>"""

    def test_parse_tables(self) -> None:
        from idfkit.simulation.parsers.html import HTMLResult

        result = HTMLResult.from_string(self.SAMPLE_HTML)
        assert len(result) == 2

    def test_table_titles(self) -> None:
        from idfkit.simulation.parsers.html import HTMLResult

        result = HTMLResult.from_string(self.SAMPLE_HTML)
        assert result[0].title == "Site and Source Energy"
        assert result[1].title == "End Uses"

    def test_table_headers(self) -> None:
        from idfkit.simulation.parsers.html import HTMLResult

        result = HTMLResult.from_string(self.SAMPLE_HTML)
        assert "Total Energy [GJ]" in result[0].header

    def test_table_rows(self) -> None:
        from idfkit.simulation.parsers.html import HTMLResult

        result = HTMLResult.from_string(self.SAMPLE_HTML)
        assert result[0].rows[0][0] == "Total Site Energy"
        assert result[0].rows[0][1] == "100.50"

    def test_to_dict(self) -> None:
        from idfkit.simulation.parsers.html import HTMLResult

        result = HTMLResult.from_string(self.SAMPLE_HTML)
        d = result[0].to_dict()
        assert "Total Site Energy" in d
        assert d["Total Site Energy"]["Total Energy [GJ]"] == "100.50"

    def test_titletable(self) -> None:
        from idfkit.simulation.parsers.html import HTMLResult

        result = HTMLResult.from_string(self.SAMPLE_HTML)
        pairs = result.titletable()
        assert len(pairs) == 2
        assert pairs[0][0] == "Site and Source Energy"

    def test_tablebyname(self) -> None:
        from idfkit.simulation.parsers.html import HTMLResult

        result = HTMLResult.from_string(self.SAMPLE_HTML)
        table = result.tablebyname("End Uses")
        assert table is not None
        assert table.title == "End Uses"

    def test_tablebyname_not_found(self) -> None:
        from idfkit.simulation.parsers.html import HTMLResult

        result = HTMLResult.from_string(self.SAMPLE_HTML)
        assert result.tablebyname("Nonexistent") is None

    def test_tablebyindex(self) -> None:
        from idfkit.simulation.parsers.html import HTMLResult

        result = HTMLResult.from_string(self.SAMPLE_HTML)
        assert result.tablebyindex(0) is not None
        assert result.tablebyindex(999) is None

    def test_from_file(self, tmp_path: Path) -> None:
        from idfkit.simulation.parsers.html import HTMLResult

        p = tmp_path / "test.html"
        p.write_text(self.SAMPLE_HTML, encoding="latin-1")
        result = HTMLResult.from_file(p)
        assert len(result) == 2

    def test_report_name(self) -> None:
        from idfkit.simulation.parsers.html import HTMLResult

        result = HTMLResult.from_string(self.SAMPLE_HTML)
        assert result[0].report_name == "Annual Building Utility Performance Summary"

    def test_empty_html(self) -> None:
        from idfkit.simulation.parsers.html import HTMLResult

        result = HTMLResult.from_string("<html><body></body></html>")
        assert len(result) == 0

    def test_to_dict_excludes_row_key_column(self) -> None:
        from idfkit.simulation.parsers.html import HTMLResult

        result = HTMLResult.from_string(self.SAMPLE_HTML)
        d = result[0].to_dict()
        # The first header (empty string) should NOT appear as a value key
        assert "" not in d["Total Site Energy"]
        # But the data columns should be present
        assert "Total Energy [GJ]" in d["Total Site Energy"]

    def test_tablesbyreport(self) -> None:
        from idfkit.simulation.parsers.html import HTMLResult

        result = HTMLResult.from_string(self.SAMPLE_HTML)
        tables = result.tablesbyreport("Annual Building Utility Performance Summary")
        assert len(tables) == 2


# ---------------------------------------------------------------------------
# Additional edge-case coverage
# ---------------------------------------------------------------------------


class TestGetReferencedObjectFallback:
    """Test the fallback path in get_referenced_object (no schema match)."""

    def test_fallback_scan_finds_object(self) -> None:
        """When schema lookup fails, collection scan should still find the target."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "TargetZone")
        # Create a standalone object with a reference-like field
        obj = IDFObject(
            obj_type="People",
            name="P1",
            data={"zone_or_zonelist_or_space_or_spacelist_name": "TargetZone"},
        )
        doc.addidfobject(obj)
        found = obj.get_referenced_object("zone_or_zonelist_or_space_or_spacelist_name")
        assert found is not None
        assert found.name == "TargetZone"


class TestGetReferingObjsIddGroups:
    def test_filter_by_iddgroups(self, simple_doc: IDFDocument) -> None:
        zone = simple_doc.getobject("Zone", "TestZone")
        assert zone is not None
        # Filter to a group that should contain BuildingSurface:Detailed
        refs = zone.getreferingobjs(iddgroups=["Thermal Zones and Surfaces"])
        ref_types = {obj.obj_type for obj in refs}
        assert "BuildingSurface:Detailed" in ref_types

    def test_filter_by_iddgroups_excludes(self, simple_doc: IDFDocument) -> None:
        zone = simple_doc.getobject("Zone", "TestZone")
        assert zone is not None
        # Filter to a group that should NOT contain surfaces
        refs = zone.getreferingobjs(iddgroups=["Schedules"])
        assert len(refs) == 0


class TestGetReferringObjectsAlias:
    def test_alias_works(self, simple_doc: IDFDocument) -> None:
        zone = simple_doc.getobject("Zone", "TestZone")
        assert zone is not None
        refs1 = zone.getreferingobjs()
        refs2 = zone.get_referring_objects()
        assert {id(o) for o in refs1} == {id(o) for o in refs2}


class TestCheckRangeEdgeCases:
    def test_checkrange_maximum_violation(self) -> None:
        doc = new_document(version=(24, 1, 0))
        zone = doc.add("Zone", "Z1", {"direction_of_relative_north": 500.0}, validate=False)
        rng = zone.getrange("direction_of_relative_north")
        if "maximum" in rng:
            with pytest.raises(RangeError):
                zone.checkrange("direction_of_relative_north")

    def test_checkrange_passes_within_range(self) -> None:
        doc = new_document(version=(24, 1, 0))
        zone = doc.add("Zone", "Z1", {"direction_of_relative_north": 45.0})
        assert zone.checkrange("direction_of_relative_north") is True


class TestRotateBuildingAnchor:
    def test_rotate_with_custom_anchor(self) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1")
        doc.add("Construction", "C1", validate=False)
        doc.add(
            "BuildingSurface:Detailed",
            "Wall",
            {
                "surface_type": "Wall",
                "construction_name": "C1",
                "zone_name": "Z1",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertex_1_x_coordinate": 10.0,
                "vertex_1_y_coordinate": 0.0,
                "vertex_1_z_coordinate": 3.0,
                "vertex_2_x_coordinate": 10.0,
                "vertex_2_y_coordinate": 0.0,
                "vertex_2_z_coordinate": 0.0,
                "vertex_3_x_coordinate": 0.0,
                "vertex_3_y_coordinate": 0.0,
                "vertex_3_z_coordinate": 0.0,
                "vertex_4_x_coordinate": 0.0,
                "vertex_4_y_coordinate": 0.0,
                "vertex_4_z_coordinate": 3.0,
            },
        )
        # Rotate 180 degrees around (5, 0, 0) -> vertex (10,0,z) becomes (0,0,z)
        rotate_building(doc, 180, anchor=Vector3D(5, 0, 0))
        wall = doc.getobject("BuildingSurface:Detailed", "Wall")
        assert wall is not None
        assert _close(wall.vertex_1_x_coordinate, 0.0, tol=1e-5)
        assert _close(wall.vertex_4_x_coordinate, 10.0, tol=1e-5)
