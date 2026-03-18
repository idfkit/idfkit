"""Tests for lossless parse-write round-tripping."""

from __future__ import annotations

import json
from pathlib import Path

from idfkit.idf_parser import _build_idf_cst, parse_idf
from idfkit.writers import write_epjson, write_idf

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

IDF_WITH_COMMENTS = """\
! File header comment
! Another header line

Version, 24.1;

! *** Zones ***

Zone,
  TestZone,              !- Name
  0,                     !- Direction of Relative North
  0, 0, 0,               !- X,Y,Z Origin
  1,                     !- Type
  1;                     !- Multiplier

Material,
  TestMaterial,           !- Name
  MediumSmooth,           !- Roughness
  0.1,                    !- Thickness
  1.0,                    !- Conductivity
  2000,                   !- Density
  1000;                   !- Specific Heat

Construction,
  TestConstruction,       !- Name
  TestMaterial;           !- Outside Layer
"""


# ---------------------------------------------------------------------------
# CST builder tests
# ---------------------------------------------------------------------------


class TestBuildIdfCst:
    """Unit tests for _build_idf_cst."""

    def test_concatenation_reproduces_original(self) -> None:
        """Concatenating all CST node texts must reproduce the input exactly."""
        cst = _build_idf_cst(IDF_WITH_COMMENTS)
        reconstructed = "".join(node.text for node in cst.nodes)
        assert reconstructed == IDF_WITH_COMMENTS

    def test_object_nodes_detected(self) -> None:
        """Object nodes should be created for Version, Zone, Material, Construction."""
        cst = _build_idf_cst(IDF_WITH_COMMENTS)
        # Count nodes that look like objects (contain comma+semicolon)
        obj_nodes = [n for n in cst.nodes if "," in n.text and ";" in n.text]
        assert len(obj_nodes) == 4  # Version, Zone, Material, Construction

    def test_comment_only_file(self) -> None:
        """A file with only comments should produce a single text node."""
        text = "! Just a comment\n! Another one\n"
        cst = _build_idf_cst(text)
        assert len(cst.nodes) == 1
        assert cst.nodes[0].text == text

    def test_empty_file(self) -> None:
        """An empty file should produce no nodes."""
        cst = _build_idf_cst("")
        assert len(cst.nodes) == 0


# ---------------------------------------------------------------------------
# IDF round-trip tests
# ---------------------------------------------------------------------------


class TestIdfRoundTrip:
    """Integration tests for IDF lossless round-tripping."""

    def test_basic_roundtrip(self, tmp_path: Path) -> None:
        """Parse with preserve_formatting → write should reproduce exactly."""
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)

        doc = parse_idf(idf_path, preserve_formatting=True)
        result = write_idf(doc)

        assert result == IDF_WITH_COMMENTS

    def test_roundtrip_preserves_comments(self, tmp_path: Path) -> None:
        """Comments should survive a round-trip."""
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)

        doc = parse_idf(idf_path, preserve_formatting=True)
        result = write_idf(doc)

        assert "! File header comment" in result
        assert "! *** Zones ***" in result
        assert "!- Name" in result

    def test_roundtrip_preserves_blank_lines(self, tmp_path: Path) -> None:
        """Blank lines between objects should be preserved."""
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)

        doc = parse_idf(idf_path, preserve_formatting=True)
        result = write_idf(doc)

        # The blank line after the header comments
        assert "\n\n" in result

    def test_modified_object_gets_reformatted(self, tmp_path: Path) -> None:
        """A mutated object should be re-serialized (not use original text)."""
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)

        doc = parse_idf(idf_path, preserve_formatting=True)
        zone = doc["Zone"]["TestZone"]
        zone.direction_of_relative_north = 45.0

        result = write_idf(doc)

        # The zone should now be reformatted (standard writer)
        assert "45" in result
        # But the comments between objects should still be there
        assert "! File header comment" in result
        assert "! *** Zones ***" in result

    def test_source_text_cleared_on_name_change(self, tmp_path: Path) -> None:
        """Renaming an object should clear its source_text."""
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)

        doc = parse_idf(idf_path, preserve_formatting=True)
        zone = doc["Zone"]["TestZone"]
        assert zone.source_text is not None

        zone.name = "RenamedZone"
        assert zone.source_text is None

    def test_source_text_cleared_on_field_change(self, tmp_path: Path) -> None:
        """Modifying a field should clear source_text."""
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)

        doc = parse_idf(idf_path, preserve_formatting=True)
        mat = doc["Material"]["TestMaterial"]
        assert mat.source_text is not None

        mat.thickness = 0.2
        assert mat.source_text is None

    def test_new_object_appended(self, tmp_path: Path) -> None:
        """Objects added after parsing should appear at the end."""
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)

        doc = parse_idf(idf_path, preserve_formatting=True)
        doc.add("Zone", "NewZone", validate=False)

        result = write_idf(doc)

        # Original content preserved at the start
        assert result.startswith("! File header comment")
        # New zone at the end
        assert "NewZone" in result

    def test_removed_object_excluded(self, tmp_path: Path) -> None:
        """Removed objects should not appear in the output."""
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)

        doc = parse_idf(idf_path, preserve_formatting=True)
        constr = doc["Construction"]["TestConstruction"]
        doc.removeidfobject(constr)

        result = write_idf(doc)

        # The Construction object text should be gone
        assert "TestConstruction" not in result
        # Other objects still present
        assert "TestZone" in result
        assert "TestMaterial" in result

    def test_preserve_false_gives_standard_output(self, tmp_path: Path) -> None:
        """Explicitly setting preserve_formatting=False should give standard output."""
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)

        doc = parse_idf(idf_path, preserve_formatting=True)
        result = write_idf(doc, preserve_formatting=False)

        # Standard writer adds its own header
        assert "!-Generator archetypal" in result
        # Original comments are NOT preserved in standard mode
        assert "! File header comment" not in result

    def test_no_cst_when_preserve_false(self, tmp_path: Path) -> None:
        """Default parsing should not build a CST."""
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)

        doc = parse_idf(idf_path)
        assert doc.cst is None

    def test_write_to_file(self, tmp_path: Path) -> None:
        """Round-trip to file should produce identical content."""
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)

        doc = parse_idf(idf_path, preserve_formatting=True)
        out_path = tmp_path / "output.idf"
        write_idf(doc, out_path)

        assert out_path.read_text(encoding="latin-1") == IDF_WITH_COMMENTS

    def test_idempotent(self, tmp_path: Path) -> None:
        """Two consecutive round-trips should produce identical output."""
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)

        # First round-trip
        doc1 = parse_idf(idf_path, preserve_formatting=True)
        result1 = write_idf(doc1)

        # Write to file and parse again
        path2 = tmp_path / "round2.idf"
        path2.write_text(result1 or "")
        doc2 = parse_idf(path2, preserve_formatting=True)
        result2 = write_idf(doc2)

        assert result1 == result2

    def test_rename_invalidates_referencing_objects(self, tmp_path: Path) -> None:
        """Renaming a referenced object should update referencing objects' output."""
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)

        doc = parse_idf(idf_path, preserve_formatting=True)

        # Construction references TestMaterial — verify source_text is set
        constr = doc["Construction"]["TestConstruction"]
        assert constr.source_text is not None

        # Rename the material
        mat = doc["Material"]["TestMaterial"]
        mat.name = "RenamedMaterial"

        # The construction's source_text should be invalidated
        assert constr.source_text is None

        result = write_idf(doc)

        # The construction must use the new name, not the old one
        assert "RenamedMaterial" in result
        assert "TestMaterial" not in result

    def test_strict_false_with_unknown_type(self, tmp_path: Path) -> None:
        """CST should be discarded when strict=False skips unknown object types."""
        idf_content = """\
Version, 24.1;

Zone,
  TestZone,              !- Name
  0,                     !- Direction of Relative North
  0, 0, 0,               !- X,Y,Z Origin
  1,                     !- Type
  1;                     !- Multiplier

UnknownFakeObject,
  SomeName,
  SomeValue;

Material,
  TestMaterial,           !- Name
  MediumSmooth,           !- Roughness
  0.1,                    !- Thickness
  1.0,                    !- Conductivity
  2000,                   !- Density
  1000;                   !- Specific Heat
"""
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(idf_content)

        doc = parse_idf(idf_path, strict=False, preserve_formatting=True)

        # CST should be discarded because the unknown type causes a mismatch
        assert doc.cst is None

        # The document should still be usable (standard formatting)
        result = write_idf(doc)
        assert "TestZone" in result
        assert "TestMaterial" in result

    def test_removed_object_cst_reference_cleared(self, tmp_path: Path) -> None:
        """Removing an object should clear its CST node reference for GC."""
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)

        doc = parse_idf(idf_path, preserve_formatting=True)
        constr = doc["Construction"]["TestConstruction"]

        # Before removal, CST should reference this object
        assert doc.cst is not None
        cst_refs = [n for n in doc.cst.nodes if n.obj is constr]
        assert len(cst_refs) == 1

        doc.removeidfobject(constr)

        # After removal, no CST node should reference the object
        cst_refs_after = [n for n in doc.cst.nodes if n.obj is constr]
        assert len(cst_refs_after) == 0

        # Output should still be correct
        result = write_idf(doc)
        assert "TestConstruction" not in result
        assert "TestZone" in result

    def test_output_type_overrides_auto_detect(self, tmp_path: Path) -> None:
        """Explicit output_type should disable lossless auto-detection."""
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)

        doc = parse_idf(idf_path, preserve_formatting=True)
        assert doc.cst is not None

        # Request compressed output without explicit preserve_formatting
        result = write_idf(doc, output_type="compressed")

        # Should use compressed format, not lossless
        assert "! File header comment" not in result
        assert "Zone," in result

    def test_nocomment_overrides_auto_detect(self, tmp_path: Path) -> None:
        """output_type='nocomment' should also disable lossless auto-detection."""
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)

        doc = parse_idf(idf_path, preserve_formatting=True)
        result = write_idf(doc, output_type="nocomment")

        # Original comments should not be preserved
        assert "! File header comment" not in result

    def test_explicit_preserve_ignores_output_type(self, tmp_path: Path) -> None:
        """Explicit preserve_formatting=True should take precedence over output_type."""
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)

        doc = parse_idf(idf_path, preserve_formatting=True)
        result = write_idf(doc, output_type="compressed", preserve_formatting=True)

        # Lossless mode should win
        assert "! File header comment" in result
        assert result == IDF_WITH_COMMENTS


# ---------------------------------------------------------------------------
# epJSON round-trip tests
# ---------------------------------------------------------------------------


EPJSON_CONTENT = """{
  "Version": {
    "Version 1": {
      "version_identifier": "24.1"
    }
  },
  "Zone": {
    "TestZone": {
      "direction_of_relative_north": 0,
      "x_origin": 0,
      "y_origin": 0,
      "z_origin": 0,
      "type": 1,
      "multiplier": 1
    }
  },
  "Material": {
    "TestMaterial": {
      "roughness": "MediumSmooth",
      "thickness": 0.1,
      "conductivity": 1.0,
      "density": 2000,
      "specific_heat": 1000
    }
  }
}"""


class TestEpJsonRoundTrip:
    """Integration tests for epJSON lossless round-tripping."""

    def test_basic_roundtrip(self, tmp_path: Path) -> None:
        """Parse with preserve_formatting → write should reproduce exactly."""
        from idfkit.epjson_parser import parse_epjson

        epjson_path = tmp_path / "input.epJSON"
        epjson_path.write_text(EPJSON_CONTENT)

        doc = parse_epjson(epjson_path, preserve_formatting=True)
        result = write_epjson(doc)

        assert result == EPJSON_CONTENT

    def test_modified_object_falls_back(self, tmp_path: Path) -> None:
        """After modification, standard JSON writer is used."""
        from idfkit.epjson_parser import parse_epjson

        epjson_path = tmp_path / "input.epJSON"
        epjson_path.write_text(EPJSON_CONTENT)

        doc = parse_epjson(epjson_path, preserve_formatting=True)
        doc["Zone"]["TestZone"].x_origin = 10.0

        result = write_epjson(doc)

        # Should still be valid JSON
        data = json.loads(result or "{}")
        assert data["Zone"]["TestZone"]["x_origin"] == 10.0

        # But it won't be byte-identical to input
        assert result != EPJSON_CONTENT

    def test_no_raw_text_when_preserve_false(self, tmp_path: Path) -> None:
        """Default parsing should not store raw text."""
        from idfkit.epjson_parser import parse_epjson

        epjson_path = tmp_path / "input.epJSON"
        epjson_path.write_text(EPJSON_CONTENT)

        doc = parse_epjson(epjson_path)
        assert doc.raw_text is None


# ---------------------------------------------------------------------------
# Performance: ensure default path is not affected
# ---------------------------------------------------------------------------


class TestPreserveFormattingPerformance:
    """Verify the default (non-preserving) path is not penalized."""

    def test_default_parse_has_no_cst(self, tmp_path: Path) -> None:
        """Objects parsed without preserve_formatting have no source_text."""
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)

        doc = parse_idf(idf_path)

        assert doc.cst is None
        assert doc.raw_text is None
        for obj in doc.all_objects:
            assert obj.source_text is None
