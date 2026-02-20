"""Tests for IDF and epJSON writers."""

from __future__ import annotations

import json
from pathlib import Path

from idfkit import IDFDocument, new_document, parse_idf, write_epjson, write_idf
from idfkit.writers import (
    convert_epjson_to_idf,
    convert_idf_to_epjson,
)

# ---------------------------------------------------------------------------
# write_idf
# ---------------------------------------------------------------------------


class TestWriteIDF:
    def test_write_to_string(self, simple_doc: IDFDocument) -> None:
        output = write_idf(simple_doc, None)
        assert output is not None
        assert isinstance(output, str)
        assert "Zone," in output
        assert "TestZone" in output

    def test_write_to_file(self, simple_doc: IDFDocument, tmp_path: Path) -> None:
        filepath = tmp_path / "output.idf"
        result = write_idf(simple_doc, filepath)
        assert result is None  # returns None when writing to file
        assert filepath.exists()
        content = filepath.read_text(encoding="latin-1")
        assert "Zone," in content

    def test_write_contains_version(self, simple_doc: IDFDocument) -> None:
        output = write_idf(simple_doc, None)
        assert output is not None
        assert "Version," in output
        assert "24.1" in output

    def test_write_contains_all_types(self, simple_doc: IDFDocument) -> None:
        output = write_idf(simple_doc, None)
        assert output is not None
        assert "Zone," in output
        assert "Material," in output
        assert "Construction," in output
        assert "BuildingSurface:Detailed," in output

    def test_write_empty_doc(self, empty_doc: IDFDocument) -> None:
        output = write_idf(empty_doc, None)
        assert output is not None
        assert "Version," in output

    def test_field_comments(self, simple_doc: IDFDocument) -> None:
        output = write_idf(simple_doc, None)
        assert output is not None
        # IDF format should include !- comments
        assert "!-" in output

    def test_version_not_duplicated_when_version_object_exists(self) -> None:
        doc = new_document(version=(24, 1, 0))
        output = write_idf(doc, None)
        assert output is not None
        assert output.count("Version,") == 1

    def test_version_object_is_authoritative_for_idf_output(self) -> None:
        doc = new_document(version=(24, 1, 0))
        version_obj = doc["Version"].first()
        assert version_obj is not None
        version_obj.version_identifier = "99.7"
        output = write_idf(doc, None)
        assert output is not None
        assert "99.7" in output

    def test_programmatic_surface_extensibles_schema_style_are_preserved(self, tmp_path: Path) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add(
            "BuildingSurface:Detailed",
            "W1",
            {
                "surface_type": "Wall",
                "outside_boundary_condition": "Outdoors",
                "sun_exposure": "SunExposed",
                "wind_exposure": "WindExposed",
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
            validate=False,
        )

        path = tmp_path / "surface_schema_style.idf"
        write_idf(doc, path)

        roundtrip = parse_idf(path)
        wall = roundtrip.getobject("BuildingSurface:Detailed", "W1")
        assert wall is not None
        assert wall.data.get("vertex_x_coordinate_4") == 10.0
        assert wall.data.get("vertex_z_coordinate_4") == 3.0

    def test_programmatic_surface_extensibles_classic_style_are_preserved(self, tmp_path: Path) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add(
            "BuildingSurface:Detailed",
            "W1",
            {
                "surface_type": "Wall",
                "outside_boundary_condition": "Outdoors",
                "sun_exposure": "SunExposed",
                "wind_exposure": "WindExposed",
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
            validate=False,
        )

        path = tmp_path / "surface_classic_style.idf"
        write_idf(doc, path)

        roundtrip = parse_idf(path)
        wall = roundtrip.getobject("BuildingSurface:Detailed", "W1")
        assert wall is not None
        assert wall.data.get("vertex_x_coordinate_4") == 10.0
        assert wall.data.get("vertex_z_coordinate_4") == 3.0

    def test_programmatic_schedule_compact_extensibles_are_preserved(self, tmp_path: Path) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add(
            "Schedule:Compact",
            "AlwaysOn",
            {
                "schedule_type_limits_name": "Any Number",
                "field": "Through: 12/31",
                "field_2": "For: AllDays",
                "field_3": "Until: 24:00",
                "field_4": "1.0",
            },
            validate=False,
        )

        path = tmp_path / "schedule_compact.idf"
        write_idf(doc, path)

        roundtrip = parse_idf(path)
        schedule = roundtrip.getobject("Schedule:Compact", "AlwaysOn")
        assert schedule is not None
        assert schedule.data.get("field") == "Through: 12/31"
        assert schedule.data.get("field_4") == "1.0"


# ---------------------------------------------------------------------------
# write_epjson
# ---------------------------------------------------------------------------


class TestWriteEpJSON:
    def test_write_to_string(self, simple_doc: IDFDocument) -> None:
        output = write_epjson(simple_doc, None)
        assert output is not None
        data = json.loads(output)
        assert "Version" in data
        assert "Zone" in data

    def test_write_to_file(self, simple_doc: IDFDocument, tmp_path: Path) -> None:
        filepath = tmp_path / "output.epJSON"
        result = write_epjson(simple_doc, filepath)
        assert result is None
        assert filepath.exists()
        data = json.loads(filepath.read_text())
        assert "Zone" in data

    def test_write_contains_version(self, simple_doc: IDFDocument) -> None:
        output = write_epjson(simple_doc, None)
        assert output is not None
        data = json.loads(output)
        assert "Version" in data
        assert "Version 1" in data["Version"]
        assert data["Version"]["Version 1"]["version_identifier"] == "24.1"

    def test_write_zone_data(self, simple_doc: IDFDocument) -> None:
        output = write_epjson(simple_doc, None)
        assert output is not None
        data = json.loads(output)
        assert "TestZone" in data["Zone"]

    def test_write_empty_doc(self, empty_doc: IDFDocument) -> None:
        output = write_epjson(empty_doc, None)
        assert output is not None
        data = json.loads(output)
        assert "Version" in data

    def test_write_custom_indent(self, empty_doc: IDFDocument) -> None:
        output = write_epjson(empty_doc, None, indent=4)
        assert output is not None
        # 4-space indent should have more spaces than 2-space
        assert "    " in output

    def test_version_not_duplicated_when_version_object_exists(self) -> None:
        doc = new_document(version=(24, 1, 0))
        output = write_epjson(doc, None)
        assert output is not None
        data = json.loads(output)
        assert "Version" in data
        assert len(data["Version"]) == 1

    def test_version_object_is_authoritative_for_epjson_output(self) -> None:
        doc = new_document(version=(24, 1, 0))
        version_obj = doc["Version"].first()
        assert version_obj is not None
        version_obj.version_identifier = "88.4"
        output = write_epjson(doc, None)
        assert output is not None
        data = json.loads(output)
        assert data["Version"]["Version 1"]["version_identifier"] == "88.4"


# ---------------------------------------------------------------------------
# IDF value formatting (tested via public write_idf output)
# ---------------------------------------------------------------------------


class TestIDFValueFormatting:
    def test_none_field_written_as_empty(self) -> None:
        doc = new_document()
        doc.add("Zone", "Z1", {"x_origin": None})
        output = write_idf(doc, None)
        assert output is not None
        # None values should be written as empty strings
        assert "Z1" in output

    def test_float_field_written(self) -> None:
        doc = new_document()
        doc.add("Zone", "Z1", {"x_origin": 3.14})
        output = write_idf(doc, None)
        assert output is not None
        assert "3.14" in output

    def test_string_field_written(self) -> None:
        doc = new_document()
        # Using validate=False since we're only testing IDF output formatting
        doc.add("Material", "Mat1", {"roughness": "MediumSmooth"}, validate=False)
        output = write_idf(doc, None)
        assert output is not None
        assert "MediumSmooth" in output


# ---------------------------------------------------------------------------
# epJSON value formatting (tested via public write_epjson output)
# ---------------------------------------------------------------------------


class TestEpJSONValueFormatting:
    def test_autosize_normalized(self) -> None:
        doc = new_document()
        # Using validate=False since we're testing value normalization, not schema validity
        doc.add("Zone", "Z1", {"x_origin": "autosize"}, validate=False)
        output = write_epjson(doc, None)
        assert output is not None
        data = json.loads(output)
        zone_data = data["Zone"]["Z1"]
        assert zone_data["x_origin"] == "Autosize"

    def test_yes_no_normalized(self) -> None:
        doc = new_document()
        # Using validate=False since we're testing value normalization, not schema validity
        doc.add("Zone", "Z1", {"x_origin": "yes"}, validate=False)
        output = write_epjson(doc, None)
        assert output is not None
        data = json.loads(output)
        assert data["Zone"]["Z1"]["x_origin"] == "Yes"

    def test_numeric_passthrough(self) -> None:
        doc = new_document()
        doc.add("Zone", "Z1", {"x_origin": 42})
        output = write_epjson(doc, None)
        assert output is not None
        data = json.loads(output)
        assert data["Zone"]["Z1"]["x_origin"] == 42


# ---------------------------------------------------------------------------
# Format conversion
# ---------------------------------------------------------------------------


class TestFormatConversion:
    def test_convert_idf_to_epjson(self, idf_file: Path, tmp_path: Path) -> None:
        epjson_path = tmp_path / "output.epJSON"
        result = convert_idf_to_epjson(idf_file, epjson_path)
        assert result == epjson_path
        assert epjson_path.exists()
        data = json.loads(epjson_path.read_text())
        assert "Zone" in data

    def test_convert_idf_to_epjson_default_path(self, idf_file: Path) -> None:
        result = convert_idf_to_epjson(idf_file)
        expected = idf_file.with_suffix(".epJSON")
        assert result == expected
        assert expected.exists()

    def test_convert_epjson_to_idf(self, epjson_file: Path, tmp_path: Path) -> None:
        idf_path = tmp_path / "output.idf"
        result = convert_epjson_to_idf(epjson_file, idf_path)
        assert result == idf_path
        assert idf_path.exists()
        content = idf_path.read_text(encoding="latin-1")
        assert "Zone," in content

    def test_convert_epjson_to_idf_default_path(self, epjson_file: Path) -> None:
        result = convert_epjson_to_idf(epjson_file)
        expected = epjson_file.with_suffix(".idf")
        assert result == expected
        assert expected.exists()

    def test_roundtrip_idf(self, idf_file: Path, tmp_path: Path) -> None:
        """IDF -> epJSON -> IDF should preserve structure."""
        epjson_path = tmp_path / "mid.epJSON"
        idf_out = tmp_path / "roundtrip.idf"
        convert_idf_to_epjson(idf_file, epjson_path)
        convert_epjson_to_idf(epjson_path, idf_out)
        content = idf_out.read_text(encoding="latin-1")
        assert "Zone," in content
        assert "TestZone" in content


# ---------------------------------------------------------------------------
# Bug-fix regression tests
# ---------------------------------------------------------------------------


class TestEpJSONWriterNamelessDuplicates:
    """epJSON writer must preserve all nameless objects (e.g. Output:Variable)."""

    def test_multiple_output_variables_preserved(self, tmp_path: Path) -> None:
        from idfkit.idf_parser import parse_idf

        content = (
            "Version, 24.1;\n"
            "Output:Variable,*,Site Outdoor Air Drybulb Temperature,Timestep;\n"
            "Output:Variable,*,Zone Mean Air Temperature,Timestep;\n"
            "Output:Variable,*,Zone Air System Sensible Heating Energy,Timestep;\n"
        )
        filepath = tmp_path / "output_vars.idf"
        filepath.write_text(content)
        doc = parse_idf(filepath)
        assert len(doc["Output:Variable"]) == 3

        epjson_str = write_epjson(doc)
        assert epjson_str is not None
        data = json.loads(epjson_str)
        # All 3 Output:Variable objects must survive in epJSON
        assert len(data.get("Output:Variable", {})) == 3


class TestEpJSONWriterEmptyStrings:
    """epJSON writer should omit empty string field values."""

    def test_empty_strings_omitted(self) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {"x_origin": 0.0, "type": ""}, validate=False)
        epjson_str = write_epjson(doc)
        assert epjson_str is not None
        data = json.loads(epjson_str)
        zone_data = data["Zone"]["Z1"]
        # Empty string values should not appear in epJSON output
        assert "" not in zone_data.values(), f"Empty strings found: {zone_data}"
