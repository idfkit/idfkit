"""Tests for IDF and epJSON writers."""

from __future__ import annotations

import json
from pathlib import Path

from idfkit import IDFDocument, new_document, write_epjson, write_idf
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
        doc.add("Material", "Mat1", {"roughness": "MediumSmooth"})
        output = write_idf(doc, None)
        assert output is not None
        assert "MediumSmooth" in output


# ---------------------------------------------------------------------------
# epJSON value formatting (tested via public write_epjson output)
# ---------------------------------------------------------------------------


class TestEpJSONValueFormatting:
    def test_autosize_normalized(self) -> None:
        doc = new_document()
        doc.add("Zone", "Z1", {"x_origin": "autosize"})
        output = write_epjson(doc, None)
        assert output is not None
        data = json.loads(output)
        zone_data = data["Zone"]["Z1"]
        assert zone_data["x_origin"] == "Autosize"

    def test_yes_no_normalized(self) -> None:
        doc = new_document()
        doc.add("Zone", "Z1", {"x_origin": "yes"})
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
