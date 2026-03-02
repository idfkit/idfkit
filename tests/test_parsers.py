"""Tests for IDF and epJSON parsers."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from idfkit import load_epjson, load_idf
from idfkit.epjson_parser import get_epjson_version, parse_epjson
from idfkit.epjson_parser import load_epjson as raw_load_epjson
from idfkit.exceptions import IDFParseError, VersionNotFoundError
from idfkit.idf_parser import get_idf_version, iter_idf_objects, parse_idf

# ---------------------------------------------------------------------------
# IDF Parser
# ---------------------------------------------------------------------------


class TestParseIDF:
    def test_basic_load(self, idf_file: Path) -> None:
        doc = parse_idf(idf_file)
        assert doc.version == (24, 1, 0)
        assert len(doc["Zone"]) == 1

    def test_load_with_version_override(self, idf_file: Path) -> None:
        doc = parse_idf(idf_file, version=(24, 1, 0))
        assert doc.version == (24, 1, 0)

    def test_load_sets_filepath(self, idf_file: Path) -> None:
        doc = parse_idf(idf_file)
        assert doc.filepath is not None
        assert doc.filepath.name == idf_file.name

    def test_load_missing_file_raises(self) -> None:
        with pytest.raises(FileNotFoundError):
            parse_idf(Path("/nonexistent/file.idf"))

    def test_zone_object_fields(self, idf_file: Path) -> None:
        doc = parse_idf(idf_file)
        zone = doc["Zone"]["TestZone"]
        assert zone.name == "TestZone"

    def test_multiple_object_types(self, idf_file: Path) -> None:
        doc = parse_idf(idf_file)
        assert "Zone" in doc
        assert "Material" in doc
        assert "Construction" in doc

    def test_people_schedule_reference(self, idf_file: Path) -> None:
        doc = parse_idf(idf_file)
        assert "People" in doc
        people = doc["People"]["TestPeople"]
        assert people is not None


class TestIDFParserVersionDetection:
    def test_version_detected_from_file(self, idf_file: Path) -> None:
        doc = parse_idf(idf_file)
        assert doc.version == (24, 1, 0)

    def test_version_detection_no_version_raises(self, tmp_path: Path) -> None:
        filepath = tmp_path / "no_version.idf"
        filepath.write_text("Zone, MyZone, 0, 0, 0, 0, 1, 1;")
        with pytest.raises(VersionNotFoundError):
            parse_idf(filepath)


class TestIDFParserTypeCoercion:
    def test_numeric_fields_coerced(self, idf_file: Path) -> None:
        """Numeric fields should be coerced to float/int during parsing."""
        doc = parse_idf(idf_file)
        zone = doc["Zone"]["TestZone"]
        # Direction of relative north should be numeric
        direction = zone.direction_of_relative_north
        assert isinstance(direction, (int, float))

    def test_integer_fields_coerced(self, idf_file: Path) -> None:
        """Integer fields should be coerced to int during parsing."""
        doc = parse_idf(idf_file)
        zone = doc["Zone"]["TestZone"]
        multiplier = zone.multiplier
        assert isinstance(multiplier, int)

    def test_string_fields_preserved(self, idf_file: Path) -> None:
        """String fields should remain as strings."""
        doc = parse_idf(idf_file)
        material = doc["Material"]["TestMaterial"]
        assert material.roughness == "MediumSmooth"

    def test_fields_with_comments_parsed(self, tmp_path: Path) -> None:
        """IDF fields with inline comments should be parsed correctly."""
        content = """\
Version, 24.1;
Zone,
  TestZone,              !- Name
  0,                     !- Direction of Relative North
  0, 0, 0,               !- X,Y,Z Origin
  1,                     !- Type
  1;                     !- Multiplier
"""
        filepath = tmp_path / "comments.idf"
        filepath.write_text(content)
        doc = parse_idf(filepath)
        zone = doc["Zone"]["TestZone"]
        assert zone.name == "TestZone"


class TestGetIDFVersion:
    def test_basic(self, idf_file: Path) -> None:
        version = get_idf_version(idf_file)
        assert version == (24, 1, 0)

    def test_no_version_raises(self, tmp_path: Path) -> None:
        filepath = tmp_path / "no_version.idf"
        filepath.write_text("Zone, MyZone;")
        with pytest.raises(VersionNotFoundError):
            get_idf_version(filepath)


class TestIterIDFObjects:
    def test_basic(self, idf_file: Path) -> None:
        objects = list(iter_idf_objects(idf_file))
        types = [obj_type for obj_type, _, _ in objects]
        assert "Zone" in types
        assert "Material" in types

    def test_object_names(self, idf_file: Path) -> None:
        objects = list(iter_idf_objects(idf_file))
        names = {obj_name for _, obj_name, _ in objects}
        assert "TestZone" in names
        assert "TestMaterial" in names

    def test_yields_fields(self, idf_file: Path) -> None:
        for obj_type, _obj_name, fields in iter_idf_objects(idf_file):
            if obj_type == "Zone":
                assert isinstance(fields, list)
                assert len(fields) > 0
                break


# ---------------------------------------------------------------------------
# epJSON Parser
# ---------------------------------------------------------------------------


class TestParseEpJSON:
    def test_basic_load(self, epjson_file: Path) -> None:
        doc = parse_epjson(epjson_file)
        assert doc.version == (24, 1, 0)
        assert len(doc["Zone"]) == 1

    def test_load_with_version_override(self, epjson_file: Path) -> None:
        doc = parse_epjson(epjson_file, version=(24, 1, 0))
        assert doc.version == (24, 1, 0)

    def test_load_sets_filepath(self, epjson_file: Path) -> None:
        doc = parse_epjson(epjson_file)
        assert doc.filepath is not None

    def test_load_missing_file_raises(self) -> None:
        with pytest.raises(FileNotFoundError):
            parse_epjson(Path("/nonexistent/file.epJSON"))

    def test_zone_data(self, epjson_file: Path) -> None:
        doc = parse_epjson(epjson_file)
        zone = doc["Zone"]["TestZone"]
        assert zone.name == "TestZone"

    def test_multiple_types(self, epjson_file: Path) -> None:
        doc = parse_epjson(epjson_file)
        assert "Zone" in doc
        assert "Material" in doc
        assert "Construction" in doc


class TestEpJSONParserVersionDetection:
    def test_version_detected_major_minor(self, tmp_path: Path) -> None:
        """Test that version like '24.1' is parsed correctly."""
        data: dict[str, dict[str, dict[str, str]]] = {
            "Version": {"Version 1": {"version_identifier": "24.1"}},
            "Zone": {"Z1": {}},
        }
        filepath = tmp_path / "v24.epJSON"
        filepath.write_text(json.dumps(data))
        doc = parse_epjson(filepath)
        assert doc.version == (24, 1, 0)

    def test_version_detected_full(self, tmp_path: Path) -> None:
        """Test that version like '9.2.0' is parsed correctly."""
        data = {"Version": {"Version 1": {"version_identifier": "9.2.0"}}}
        filepath = tmp_path / "v9.epJSON"
        filepath.write_text(json.dumps(data))
        doc = parse_epjson(filepath)
        assert doc.version == (9, 2, 0)

    def test_version_detection_missing(self, tmp_path: Path) -> None:
        filepath = tmp_path / "no_version.epJSON"
        filepath.write_text(json.dumps({"Zone": {"Z1": {}}}))
        with pytest.raises(VersionNotFoundError):
            parse_epjson(filepath)


class TestGetEpJSONVersion:
    def test_basic(self, epjson_file: Path) -> None:
        version = get_epjson_version(epjson_file)
        assert version == (24, 1, 0)

    def test_no_version_raises(self, tmp_path: Path) -> None:
        filepath = tmp_path / "no_version.epJSON"
        filepath.write_text(json.dumps({"Zone": {"Z1": {}}}))
        with pytest.raises(VersionNotFoundError):
            get_epjson_version(filepath)


class TestLoadEpJSON:
    def test_raw_load(self, epjson_file: Path) -> None:
        data = raw_load_epjson(epjson_file)
        assert isinstance(data, dict)
        assert "Version" in data
        assert "Zone" in data


# ---------------------------------------------------------------------------
# High-level load functions
# ---------------------------------------------------------------------------


class TestHighLevelLoad:
    def test_load_idf(self, idf_file: Path) -> None:
        doc = load_idf(str(idf_file))
        assert doc.version == (24, 1, 0)
        assert len(doc["Zone"]) == 1

    def test_load_epjson(self, epjson_file: Path) -> None:
        doc = load_epjson(str(epjson_file))
        assert doc.version == (24, 1, 0)
        assert len(doc["Zone"]) == 1


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestParserEdgeCases:
    def test_idf_with_empty_fields(self, tmp_path: Path) -> None:
        content = "Version, 24.1;\nZone, TestZone, , , , , , ;"
        filepath = tmp_path / "empty_fields.idf"
        filepath.write_text(content)
        doc = parse_idf(filepath)
        assert len(doc["Zone"]) == 1

    def test_idf_with_comments_only(self, tmp_path: Path) -> None:
        content = "! This is a comment\nVersion, 24.1;\n! Another comment\n"
        filepath = tmp_path / "comments.idf"
        filepath.write_text(content)
        doc = parse_idf(filepath)
        assert len(doc) == 0  # Only version, no objects

    def test_epjson_with_non_dict_value(self, tmp_path: Path) -> None:
        """Test that non-dict values in the object type are skipped."""
        data = {
            "Version": {"Version 1": {"version_identifier": "24.1"}},
            "Zone": "not a dict",
        }
        filepath = tmp_path / "bad.epJSON"
        filepath.write_text(json.dumps(data))
        doc = parse_epjson(filepath)
        # Zone should be skipped because its value is not a dict
        assert len(doc["Zone"]) == 0

    def test_epjson_with_non_dict_object(self, tmp_path: Path) -> None:
        """Test that non-dict individual objects are skipped."""
        data = {
            "Version": {"Version 1": {"version_identifier": "24.1"}},
            "Zone": {"Z1": "not a dict"},
        }
        filepath = tmp_path / "bad_obj.epJSON"
        filepath.write_text(json.dumps(data))
        doc = parse_epjson(filepath)
        assert len(doc["Zone"]) == 0

    def test_iter_idf_objects_strips_comments(self, tmp_path: Path) -> None:
        """iter_idf_objects should not produce phantom objects from comments."""
        content = "Version, 24.1;\n! Comment with X,Y,Z format:\n! X,\n!   value1;\nZone,\n  TestZone,\n  0, 0, 0, 0;\n"
        filepath = tmp_path / "comments.idf"
        filepath.write_text(content)
        objects = list(iter_idf_objects(filepath))
        obj_types = [t for t, _, _ in objects]
        assert "Zone" in obj_types
        # Comments should NOT produce phantom objects
        assert all(t in ("Version", "Zone") for t in obj_types), (
            f"Phantom objects found: {[t for t in obj_types if t not in ('Version', 'Zone')]}"
        )

    def test_coerce_value_preserves_autosize_casing(self, tmp_path: Path) -> None:
        """Autosize/Autocalculate should not be lowercased by the parser."""
        content = """\
Version, 24.1;
Sizing:Zone,
  TestZone,
  SupplyAirTemperature, 14, ,
  SupplyAirTemperature, 40, ,
  0.0085, 0.008, , , ,
  DesignDay, 0, , , 0,
  DesignDay, 0, , , 0, ,
  No, NeutralSupplyAir,
  Autosize,
  Autosize;
"""
        filepath = tmp_path / "autosize.idf"
        filepath.write_text(content)
        doc = parse_idf(filepath)
        sz = doc["Sizing:Zone"][0]
        low_sp = sz.data.get("dedicated_outdoor_air_low_setpoint_temperature_for_design")
        # Should preserve the original casing, not lowercase it
        assert low_sp == "Autosize", f"Expected 'Autosize' but got {low_sp!r}"

    def test_schema_not_mutated_by_extensible_parsing(self, tmp_path: Path) -> None:
        """Parsing extensible nameless objects must not mutate the schema's field list."""
        from idfkit.schema import get_schema

        schema = get_schema((24, 1, 0))
        original_fields = list(schema.get_all_field_names("Output:Table:SummaryReports"))

        content = "Version, 24.1;\nOutput:Table:SummaryReports, AllSummary, ZoneComponentLoadSummary;\n"
        filepath = tmp_path / "reports.idf"
        filepath.write_text(content)
        parse_idf(filepath, schema=schema)

        after_fields = schema.get_all_field_names("Output:Table:SummaryReports")
        assert after_fields == original_fields, (
            f"Schema was mutated: started with {original_fields}, now {after_fields}"
        )

    def test_non_extensible_overflow_raises(self, tmp_path: Path) -> None:
        """Strict parsing should fail when non-extensible objects overflow fields."""
        content = """\
Version,24.1;
Building,
  My Building,
  0.0,
  Suburbs,
  0.04,
  0.4,
  FullExterior,
  25,
  6,
  UnexpectedTrailingField;
"""
        filepath = tmp_path / "overflow.idf"
        filepath.write_text(content)
        with pytest.raises(IDFParseError, match="not extensible") as exc_info:
            parse_idf(filepath)
        assert exc_info.value.diagnostics
        assert exc_info.value.diagnostics[0].line is not None

    def test_unknown_object_type_raises(self, tmp_path: Path) -> None:
        """Strict parsing should fail on unknown object types instead of silently skipping."""
        content = """\
Version,24.1;
Zone, KnownZone;
TotallyMadeUpObject, Foo;
"""
        filepath = tmp_path / "unknown_type.idf"
        filepath.write_text(content)
        with pytest.raises(IDFParseError, match="Unknown object type") as exc_info:
            parse_idf(filepath)
        assert exc_info.value.diagnostics[0].obj_type == "TotallyMadeUpObject"

    def test_invalid_field_bytes_strict_false_skips(self, tmp_path: Path) -> None:
        """Malformed bytes should be skipped (not leaked as UnicodeDecodeError) when strict=False."""
        content = b"Version,24.1;\nZone,\n  Bad\xffName,\n  0,0,0,0;\n"
        filepath = tmp_path / "bad_bytes.idf"
        filepath.write_bytes(content)

        doc = parse_idf(filepath, encoding="utf-8", strict=False)
        assert len(doc["Zone"]) == 0

    def test_invalid_field_bytes_strict_true_wrapped(self, tmp_path: Path) -> None:
        """Malformed bytes should raise IDFParseError with diagnostics when strict=True."""
        content = b"Version,24.1;\nZone,\n  Bad\xffName,\n  0,0,0,0;\n"
        filepath = tmp_path / "bad_bytes_strict.idf"
        filepath.write_bytes(content)

        with pytest.raises(IDFParseError, match="Failed to parse object") as exc_info:
            parse_idf(filepath, encoding="utf-8", strict=True)
        assert exc_info.value.diagnostics
        assert exc_info.value.diagnostics[0].obj_type == "Zone"
