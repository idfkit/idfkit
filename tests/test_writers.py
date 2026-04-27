"""Tests for IDF and epJSON writers."""

from __future__ import annotations

import json
import logging
from pathlib import Path

import pytest

from idfkit import IDFDocument, new_document, parse_idf, write_epjson, write_idf
from idfkit.epjson_parser import parse_epjson  # pyright: ignore[reportPrivateUsage]
from idfkit.writers import (
    EpJSONWriter,
    IDFWriter,
    _resolve_version_identifier,  # pyright: ignore[reportPrivateUsage]
    _write_idf_lossless,  # pyright: ignore[reportPrivateUsage]
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
        assert wall.data["vertices"][3]["vertex_x_coordinate"] == 10.0
        assert wall.data["vertices"][3]["vertex_z_coordinate"] == 3.0

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
        assert wall.data["vertices"][3]["vertex_x_coordinate"] == 10.0
        assert wall.data["vertices"][3]["vertex_z_coordinate"] == 3.0

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
        assert schedule.data["data"][0]["field"] == "Through: 12/31"
        assert schedule.data["data"][3]["field"] == "1.0"


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


# ---------------------------------------------------------------------------
# Coverage gap tests: writers.py uncovered lines
# ---------------------------------------------------------------------------


class TestResolveVersionIdentifier:
    """_resolve_version_identifier edge cases (L38, L42->33, L44-45)."""

    def test_empty_version_identifier_string_falls_back_to_doc_version(self) -> None:
        """version_identifier is a whitespace-only string → fall back to doc.version (L42->33)."""
        doc = new_document(version=(24, 1, 0))
        version_obj = doc["Version"].first()
        assert version_obj is not None
        # Set version_identifier to empty string so strip() returns ""
        version_obj.data["version_identifier"] = "   "
        result = _resolve_version_identifier(doc)
        assert result == "24.1"

    def test_numeric_version_identifier_falls_back_to_doc_version(self) -> None:
        """version_identifier is a non-string (e.g. float) → isinstance guard fails, falls back to doc.version."""
        doc = new_document(version=(24, 1, 0))
        version_obj = doc["Version"].first()
        assert version_obj is not None
        # Store a numeric value directly; the function only accepts str, so this falls back
        version_obj.data["version_identifier"] = 23.2
        result = _resolve_version_identifier(doc)
        assert result == "24.1"

    def test_version_identifier_none_falls_back_to_doc_version(self) -> None:
        """version_identifier key absent: data.get() returns None, elif skipped (L44->33)."""
        doc = new_document(version=(24, 1, 0))
        version_obj = doc["Version"].first()
        assert version_obj is not None
        version_obj.data.pop("version_identifier", None)
        result = _resolve_version_identifier(doc)
        assert result == "24.1"

    def test_no_version_collection_falls_back(self) -> None:
        """No VERSION collection: loop finds nothing, falls back to doc.version (L47-48)."""
        from idfkit import IDFDocument
        from idfkit.schema import get_schema

        doc = IDFDocument(version=(24, 1, 0), schema=get_schema((24, 1, 0)))
        result = _resolve_version_identifier(doc)
        assert result == "24.1"


class TestIDFValueFormattingEdgeCases:
    """IDFWriter._format_value edge cases (L402, L408, L412-413, L416)."""

    def test_bool_true_written_as_yes(self) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {"x_origin": True}, validate=False)
        output = write_idf(doc)
        assert output is not None
        assert "Yes" in output

    def test_bool_false_written_as_no(self) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {"x_origin": False}, validate=False)
        output = write_idf(doc)
        assert output is not None
        assert "No" in output

    def test_float_scientific_notation_large(self) -> None:
        """Floats >= 1e10 use scientific notation (L408)."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {"x_origin": 1.5e12}, validate=False)
        output = write_idf(doc)
        assert output is not None
        assert "e" in output.lower()

    def test_float_scientific_notation_small(self) -> None:
        """Floats < 0.0001 use scientific notation (L408)."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {"x_origin": 0.00001}, validate=False)
        output = write_idf(doc)
        assert output is not None
        assert "e" in output.lower()

    def test_list_value_written_as_csv(self) -> None:
        """List values are joined with ', ' (L412-413)."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {"x_origin": [1, 2, 3]}, validate=False)
        output = write_idf(doc)
        assert output is not None
        assert "1, 2, 3" in output

    def test_delimiter_in_string_logs_warning(self, caplog: pytest.LogCaptureFixture) -> None:
        """String with IDF delimiter characters logs a warning (L416)."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {"x_origin": "bad,value"}, validate=False)
        with caplog.at_level(logging.WARNING, logger="idfkit.writers"):
            write_idf(doc)
        assert any("delimiter" in r.message for r in caplog.records)


class TestIDFWriterNocommentMode:
    """IDFWriter nocomment mode (L322, L338->341, L346-349)."""

    def test_nocomment_output_has_no_field_comments(self) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {"x_origin": 1.0})
        output = write_idf(doc, output_type="nocomment")
        assert output is not None
        # nocomment mode omits per-field "!- Field Name" annotations
        assert "!- X Origin" not in output
        assert "Z1" in output

    def test_schema_based_field_names_when_no_field_order(self) -> None:
        """Objects without field_order fall back to schema.get_all_field_names (L338->341)."""
        from idfkit import IDFDocument
        from idfkit.objects import IDFObject
        from idfkit.schema import get_schema

        schema = get_schema((24, 1, 0))
        doc = IDFDocument(version=(24, 1, 0), schema=schema)
        # Create object with no field_order (field_order=None by default in IDFObject)
        obj = IDFObject(obj_type="Zone", name="Z1", data={"x_origin": 2.0})
        doc.addidfobject(obj)

        output = write_idf(doc)
        assert output is not None
        assert "Z1" in output

    def test_no_schema_no_field_order_uses_data_keys(self) -> None:
        """Objects without field_order and no schema fall back to data.keys (L346-349)."""
        from idfkit import IDFDocument
        from idfkit.objects import IDFObject

        doc = IDFDocument(version=(24, 1, 0), schema=None)
        obj = IDFObject(obj_type="Zone", name="Z1", data={"x_origin": 3.0})
        doc.addidfobject(obj)

        output = write_idf(doc)
        assert output is not None
        assert "Z1" in output


class TestIDFWriterWriteToFile:
    """IDFWriter.write_to_file (L425-427)."""

    def test_write_to_file(self, tmp_path: Path) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {"x_origin": 0.0})
        writer = IDFWriter(doc)
        out_path = tmp_path / "out.idf"
        writer.write_to_file(out_path)
        content = out_path.read_text(encoding="latin-1")
        assert "Zone," in content


class TestEpJSONWriterWriteToFile:
    """EpJSONWriter.write_to_file (L511-513)."""

    def test_write_to_file(self, tmp_path: Path) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {"x_origin": 0.0})
        writer = EpJSONWriter(doc)
        out_path = tmp_path / "out.epJSON"
        writer.write_to_file(out_path)
        data = json.loads(out_path.read_text())
        assert "Zone" in data


class TestIDFWriterEmptyCollection:
    """IDFWriter.to_string skips empty collections (L322)."""

    def test_empty_collection_skipped_in_idf(self) -> None:
        from idfkit import IDFDocument
        from idfkit.schema import get_schema

        doc = IDFDocument(version=(24, 1, 0), schema=get_schema((24, 1, 0)))
        # Access (and thus create) an empty Zone collection
        _ = doc["Zone"]
        output = write_idf(doc)
        assert output is not None
        # Empty Zone collection should not appear in IDF output
        assert "Zone," not in output


class TestEpJSONWriterEmptyCollection:
    """EpJSONWriter skips empty collections (L467)."""

    def test_empty_collection_skipped(self) -> None:
        from idfkit import IDFDocument
        from idfkit.schema import get_schema

        # Create doc with an empty collection (no objects of a type that exists in schema)
        doc = IDFDocument(version=(24, 1, 0), schema=get_schema((24, 1, 0)))
        # Ensure there is a collection entry but with no objects
        _ = doc["Zone"]  # accessing creates an empty collection
        output = write_epjson(doc)
        assert output is not None
        data = json.loads(output)
        # Empty Zone collection should not appear in epJSON
        assert "Zone" not in data


class TestWriteIdfLossless:
    """_write_idf_lossless edge cases (L227, L246-247, L262)."""

    def test_write_idf_lossless_no_cst_raises(self) -> None:
        """_write_idf_lossless raises ValueError when doc has no CST (L246-247)."""
        doc = new_document(version=(24, 1, 0))
        with pytest.raises(ValueError, match="no CST"):
            _write_idf_lossless(doc)

    def test_removed_object_skipped_in_lossless_output(self, tmp_path: Path) -> None:
        """Object removed via collection.remove bypasses CST clearing (L227)."""
        content = """\
Version, 24.1;

Zone,
  ZoneKeep,
  0, 0, 0, 0, 1, 1;

Zone,
  ZoneRemove,
  0, 0, 0, 0, 1, 1;
"""
        idf_path = tmp_path / "remove.idf"
        idf_path.write_bytes(content.encode("latin-1"))
        doc = parse_idf(idf_path, preserve_formatting=True)

        # Remove via the collection directly so CST node.obj is NOT cleared.
        # This means _emit_cst_node will see node.obj set but id not in live_ids (L227).
        zone_remove = doc["Zone"]["ZoneRemove"]
        assert zone_remove is not None
        doc["Zone"].remove(zone_remove)  # pyright: ignore[reportArgumentType]

        output = write_idf(doc)
        assert output is not None
        assert "ZoneKeep" in output
        assert "ZoneRemove" not in output

    def test_new_object_appended_when_tail_has_no_newline(self, tmp_path: Path) -> None:
        """New objects added after parse are appended; handles tail without trailing newline (L262)."""
        content = "Version, 24.1;\nZone, ExistingZone, 0, 0, 0, 0, 1, 1;"
        idf_path = tmp_path / "notail.idf"
        idf_path.write_bytes(content.encode("latin-1"))
        doc = parse_idf(idf_path, preserve_formatting=True)

        # Add a new Zone after parsing — it won't be in any CST node
        doc.add("Zone", "NewZone", {"x_origin": 5.0})

        output = write_idf(doc)
        assert output is not None
        assert "ExistingZone" in output
        assert "NewZone" in output


_LOSSLESS_EPJSON = {
    "Version": {"Version 1": {"version_identifier": "24.1"}},
    "Zone": {"Z1": {"x_origin": 0.0}},
}


class TestWriteEpJSONLossless:
    """write_epjson lossless path: write to file (L190-194) and return string (L195-196)."""

    def test_lossless_to_file(self, tmp_path: Path) -> None:
        epjson_path = tmp_path / "source.epJSON"
        epjson_path.write_text(json.dumps(_LOSSLESS_EPJSON))

        doc = parse_epjson(epjson_path, preserve_formatting=True)
        out_path = tmp_path / "lossless_out.epJSON"
        result = write_epjson(doc, out_path)
        assert result is None
        assert out_path.exists()
        assert "Zone" in json.loads(out_path.read_text())

    def test_lossless_to_string(self, tmp_path: Path) -> None:
        epjson_path = tmp_path / "source.epJSON"
        epjson_path.write_text(json.dumps(_LOSSLESS_EPJSON))

        doc = parse_epjson(epjson_path, preserve_formatting=True)
        result = write_epjson(doc)
        assert result is not None
        assert "Zone" in json.loads(result)


class TestWriteIDFLosslessEmittedDirtyObject:
    """_emit_cst_node: mutated object uses formatter (L234-235)."""

    def test_mutated_object_reformatted_in_lossless_output(self, tmp_path: Path) -> None:
        content = """\
Version, 24.1;

Zone,
  MutableZone,
  0, 0, 0, 0, 1, 1;
"""
        idf_path = tmp_path / "mutable.idf"
        idf_path.write_bytes(content.encode("latin-1"))
        doc = parse_idf(idf_path, preserve_formatting=True)

        zone = doc["Zone"]["MutableZone"]
        assert zone is not None
        # Mutate the object so source_text is cleared
        zone.x_origin = 99.0

        output = write_idf(doc)
        assert output is not None
        assert "MutableZone" in output
