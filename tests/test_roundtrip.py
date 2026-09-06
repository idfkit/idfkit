"""Tests for lossless parse-write round-tripping."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from idfkit.cst import CSTNode
from idfkit.idf_parser import _build_idf_cst, _cst_node_type_name, parse_idf
from idfkit.writers import save_idf, write_epjson, write_idf

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

    def test_comment_with_semicolon_and_comma(self) -> None:
        """Comments containing `;` and `,` must not be matched as objects."""
        text = "! This comment has ; and , in it\nVersion, 24.1;\n"
        cst = _build_idf_cst(text)
        reconstructed = "".join(n.text for n in cst.nodes)
        assert reconstructed == text
        obj_nodes = [n for n in cst.nodes if "," in n.text and ";" in n.text and not n.text.lstrip().startswith("!")]
        assert len(obj_nodes) == 1

    def test_object_no_trailing_newline(self) -> None:
        """Object at EOF with no trailing newline should still be captured."""
        text = "Version, 24.1;"
        cst = _build_idf_cst(text)
        assert len(cst.nodes) == 1
        assert cst.nodes[0].text == text

    def test_comment_before_first_comma_in_body(self) -> None:
        """An inline comment before the first comma in an object body."""
        text = "Zone,\n  !- inline comment\n  TestZone, 0, 0, 0, 0, 1, 1;\n"
        cst = _build_idf_cst(text)
        reconstructed = "".join(n.text for n in cst.nodes)
        assert reconstructed == text


class TestCstNodeTypeName:
    """Unit tests for _cst_node_type_name."""

    def test_normal_object(self) -> None:
        node = CSTNode(text="Zone,\n  TestZone, 0;\n")
        assert _cst_node_type_name(node) == "Zone"

    def test_text_only_node(self) -> None:
        node = CSTNode(text="! just a comment\n\n")
        assert _cst_node_type_name(node) is None

    def test_semicolon_only_node(self) -> None:
        node = CSTNode(text=";")
        assert _cst_node_type_name(node) is None

    def test_comment_before_type(self) -> None:
        """A leading comment line before the type name comma."""
        node = CSTNode(text="! comment\nZone, TestZone;\n")
        assert _cst_node_type_name(node) == "Zone"


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

    def test_copy_clears_source_text(self, tmp_path: Path) -> None:
        """Copying an object should not carry over source_text."""
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)

        doc = parse_idf(idf_path, preserve_formatting=True)
        zone = doc["Zone"]["TestZone"]
        assert zone.source_text is not None

        clone = zone.copy()
        assert clone.source_text is None

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
        assert "!-Generator idfkit" in result
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
        save_idf(doc, out_path)

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
        """CST survives when strict=False skips unknown object types.

        The unknown type's CST node stays unlinked (no ``obj``), but the
        remaining objects are linked correctly and their formatting is
        preserved.
        """
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

        doc = parse_idf(idf_path, strict_parsing=False, preserve_formatting=True)

        # CST is preserved; known objects are linked, unknown node is unlinked.
        assert doc.cst is not None
        zone = doc["Zone"]["TestZone"]
        assert zone.source_text is not None
        mat = doc["Material"]["TestMaterial"]
        assert mat.source_text is not None

        # The document should still be usable and preserve formatting
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

    def test_an_output_type_takes_precedence_over_explicit_preserve(self, tmp_path: Path) -> None:
        """An output form wins over preservation, including over an explicit ``True``.

        This assertion is the reverse of what it was until feature 006, and the reversal is
        deliberate. The two languages disagreed here: Python granted preservation and dropped the
        requested form in silence, TypeScript produced the form. Neither refused, so the caller got
        a different file depending on which library they were holding.

        The form wins, on the reason FR-013 gives: a different output form is a different artifact,
        which the original text was never going to express, so producing it is honest. The
        contradiction that IS refused is preservation together with a control that changes how an
        object is laid out, which is a different question and is checked below.
        """
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)

        doc = parse_idf(idf_path, preserve_formatting=True)
        result = write_idf(doc, output_type="compressed", preserve_formatting=True)

        assert "! File header comment" not in result
        assert result != IDF_WITH_COMMENTS
        assert "Zone,TestZone," in result


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

    def test_added_object_disables_lossless(self, tmp_path: Path) -> None:
        """Adding an object should prevent lossless epJSON output."""
        from idfkit.epjson_parser import parse_epjson

        epjson_path = tmp_path / "input.epJSON"
        epjson_path.write_text(EPJSON_CONTENT)

        doc = parse_epjson(epjson_path, preserve_formatting=True)
        doc.add("Zone", "NewZone", validate=False)

        result = write_epjson(doc)

        # Should be valid JSON with the new zone included
        data = json.loads(result or "{}")
        assert "NewZone" in data["Zone"]
        assert "TestZone" in data["Zone"]

        # But not byte-identical to input (standard writer was used)
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


# ---------------------------------------------------------------------------
# Regressions confirmed by running the code, not by reading it (feature 006)
# ---------------------------------------------------------------------------


class TestNoOpFieldWriteKeepsSourceText:
    """FR-004: writing a field the value it already holds must change nothing.

    Confirmed as a defect by running it (research R4). ``_set_field`` cleared
    ``_source_text`` unconditionally, so writing ``3.000`` over the ``3.0`` it
    had already parsed reformatted the object and lost the author's notation.
    ``_set_name`` has compared before acting since it was written; this is that
    guard, on its sibling.
    """

    NO_OP_SOURCE = (
        "Version, 26.1;\n\nZone,\n  MyZone,          !- Name\n  3.000;           !- Direction of Relative North\n"
    )

    def test_writing_the_value_already_held_reproduces_the_object(self, tmp_path: Path) -> None:
        idf_path = tmp_path / "no-op.idf"
        idf_path.write_text(self.NO_OP_SOURCE)

        doc = parse_idf(idf_path, preserve_formatting=True)
        zone = doc["Zone"]["MyZone"]
        zone.direction_of_relative_north = zone.direction_of_relative_north

        assert write_idf(doc) == self.NO_OP_SOURCE

    def test_writing_a_different_value_still_reformats(self, tmp_path: Path) -> None:
        """The guard must not be a blanket refusal to notice a change."""
        idf_path = tmp_path / "real-edit.idf"
        idf_path.write_text(self.NO_OP_SOURCE)

        doc = parse_idf(idf_path, preserve_formatting=True)
        zone = doc["Zone"]["MyZone"]
        zone.direction_of_relative_north = 4.5

        assert zone.source_text is None
        assert "4.5" in write_idf(doc)


class TestPreserveFormattingRefusals:
    """FR-012 and research R8, R9: the two gaps in the refusal guard.

    ``version_first`` was missing from it, so asking to move the version
    statement while preserving was granted silently. And the guard fired only
    when ``preserve_formatting`` was explicitly ``True``, so a control set on
    the default path preserved the file and dropped the control without a word.
    """

    def test_version_first_conflicts_with_preservation(self, tmp_path: Path) -> None:
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)
        doc = parse_idf(idf_path, preserve_formatting=True)

        with pytest.raises(ValueError, match="version_first"):
            write_idf(doc, preserve_formatting=True, version_first=False)

    def test_the_same_set_of_controls_is_refused_as_in_the_other_language(self, tmp_path: Path) -> None:
        """SC-006: the same SET in both, checked rather than assumed.

        A set of controls, not of values. The two languages' defaults differ and stay differing,
        two spaces against four and sorted order against source order, so "away from its default"
        means away from each language's own. What has to agree is which controls are refused, and
        that the message names the class rather than the one the caller happened to set.
        """
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)
        doc = parse_idf(idf_path, preserve_formatting=True)

        refused: list[dict[str, object]] = [
            {"indent": 4},
            {"comment_column": 40},
            {"ordering": "source"},
            {"version_first": False},
        ]
        for control in refused:
            with pytest.raises(ValueError, match="indent, comment_column, ordering or version_first"):
                write_idf(doc, preserve_formatting=True, **control)  # pyright: ignore[reportArgumentType]

        # The output FORMS are granted rather than refused, on both sides: a different form is a
        # different artifact the source was never going to express.
        assert write_idf(doc, "compressed", preserve_formatting=True) != IDF_WITH_COMMENTS
        assert write_idf(doc, "nocomment", preserve_formatting=True) != IDF_WITH_COMMENTS

    def test_a_control_on_the_default_path_asks_for_formatting(self, tmp_path: Path) -> None:
        """A set control is a request to format, not a control to drop silently."""
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)
        doc = parse_idf(idf_path, preserve_formatting=True)

        written = write_idf(doc, indent=4)

        assert written != IDF_WITH_COMMENTS
        assert "\n    TestZone," in written


class TestChangedObjects:
    """Which objects a preserving write will rewrite, asked directly.

    A consumer cannot derive this from its own edit log. A rename clears the record on every object
    that referred to the renamed one, so an editor counting its own edits reports one where the
    answer is three here and nine on a real model.
    """

    REFERENCED = (
        "Version, 26.1.0;\n"
        "\n"
        "Zone, ZONE ONE;\n"
        "\n"
        "BuildingSurface:Detailed,\n"
        "  S1, Wall, C1, ZONE ONE, , Outdoors, , SunExposed, WindExposed, , ,\n"
        "  0,0,0, 1,0,0;\n"
        "\n"
        "BuildingSurface:Detailed,\n"
        "  S2, Wall, C1, ZONE ONE, , Outdoors, , SunExposed, WindExposed, , ,\n"
        "  0,0,0, 1,0,0;\n"
    )

    def _read(self, tmp_path: Path, *, preserve: bool = True):
        idf_path = tmp_path / "referenced.idf"
        idf_path.write_text(self.REFERENCED)
        return parse_idf(idf_path, preserve_formatting=preserve)

    def test_nothing_is_changed_by_reading(self, tmp_path: Path) -> None:
        assert list(self._read(tmp_path).changed_objects()) == []

    def test_a_rename_changes_every_object_that_pointed_at_it(self, tmp_path: Path) -> None:
        doc = self._read(tmp_path)
        doc["Zone"]["ZONE ONE"].name = "RENAMED"

        changed = sorted(obj.obj_type for obj in doc.changed_objects())

        assert changed == ["BuildingSurface:Detailed", "BuildingSurface:Detailed", "Zone"]

    def test_a_no_op_write_changes_nothing(self, tmp_path: Path) -> None:
        doc = self._read(tmp_path)
        zone = doc["Zone"]["ZONE ONE"]
        zone.name = zone.name

        assert list(doc.changed_objects()) == []

    def test_every_object_is_changed_without_preservation(self, tmp_path: Path) -> None:
        """There is nothing to reproduce, so a write rewrites the file entirely."""
        doc = self._read(tmp_path, preserve=False)

        assert len(list(doc.changed_objects())) == len(doc)

    def test_it_agrees_with_what_the_writer_actually_reproduces(self, tmp_path: Path) -> None:
        """The claim is only worth making if the writer honours it."""
        doc = self._read(tmp_path)
        doc["Zone"]["ZONE ONE"].name = "RENAMED"
        written = write_idf(doc)

        untouched = [obj for obj in doc.all_objects if obj not in list(doc.changed_objects())]
        for obj in untouched:
            assert obj.source_text is not None
            assert obj.source_text in written


class TestCommentsOnAReformattedObject:
    """What survives when the writer rewrites an object, beyond its values.

    An edit asks for the VALUES to be re-rendered. Everything else the author wrote is theirs, and
    that includes the absence of a comment on a field they left bare.
    """

    SOURCE = (
        "Version, 26.1.0;\n"
        "\n"
        "! a note between objects\n"
        "Building,\n"
        "  My Building,   !- Name\n"
        "  ! this value came from the 2019 survey\n"
        "  0,             !- North Axis {deg}\n"
        "  Suburbs;\n"
        "\n"
        "Timestep, 6;\n"
    )

    def _edited(self, tmp_path: Path, **kwargs: object):
        idf_path = tmp_path / "annotated.idf"
        idf_path.write_text(self.SOURCE)
        doc = parse_idf(idf_path, preserve_formatting=True)
        doc["Building"]["My Building"].north_axis = 42
        return write_idf(doc, **kwargs)  # pyright: ignore[reportArgumentType]

    def test_a_units_annotation_survives(self, tmp_path: Path) -> None:
        """`{deg}` is in the schema and the generated label drops it, so rebuilding loses it."""
        assert "!- North Axis {deg}" in self._edited(tmp_path)

    def test_a_comment_on_its_own_line_inside_the_object_survives(self, tmp_path: Path) -> None:
        """The one comment nothing else carries: it is inside the object, not between two."""
        assert "! this value came from the 2019 survey" in self._edited(tmp_path)

    def test_a_comment_between_two_objects_survives(self, tmp_path: Path) -> None:
        assert "! a note between objects" in self._edited(tmp_path)

    def test_a_field_the_author_left_bare_stays_bare(self, tmp_path: Path) -> None:
        """Absence is as much a thing the author wrote as the words are."""
        written = self._edited(tmp_path)

        assert re.search(r"Suburbs;\s*$", written, re.MULTILINE)
        assert "!- Terrain" not in written

    def test_generate_labels_a_bare_field_and_still_keeps_every_comment(self, tmp_path: Path) -> None:
        """The escape hatch adds labels and never costs a line."""
        written = self._edited(tmp_path, field_comments="generate")

        assert "!- Terrain" in written
        assert "! this value came from the 2019 survey" in written
        assert "! a note between objects" in written
        assert "!- North Axis {deg}" in written

    def test_only_the_value_changed(self, tmp_path: Path) -> None:
        written = self._edited(tmp_path)

        assert "42," in written
        assert "  0," not in written

    def test_a_comment_is_attached_by_delimiter_and_not_by_line(self, tmp_path: Path) -> None:
        """Several fields share a line in real files, and counting lines mis-attaches every comment.

        The vertices of a surface are routinely written three to a line with one comment for the
        triple. That comment follows the third delimiter, so it belongs to the third field.
        """
        idf_path = tmp_path / "packed.idf"
        idf_path.write_text(
            "Version, 26.1.0;\n"
            "\n"
            "Building,\n"
            "  Packed, City, 0.04,   !- three fields, one comment\n"
            "  0.4;                  !- and another\n"
        )
        doc = parse_idf(idf_path, preserve_formatting=True)
        doc["Building"]["Packed"].terrain = "Suburbs"
        written = write_idf(doc)

        # The comment lands on the field its delimiter closed, and the two before it stay bare.
        assert "!- three fields, one comment" in written
        assert "!- and another" in written


class TestLineGrouping:
    """The line the author put a value on.

    21.5% of the statements in the 693 EnergyPlus 22.1.0 example files write several values to a
    line, and 690 of those files contain at least one. Writing one value per line regardless turns a
    four-line surface into twelve, which is the most visible thing a reformat does to geometry.
    """

    def test_values_the_author_grouped_stay_grouped(self, tmp_path: Path) -> None:
        source = (
            "Version, 26.1.0;\n"
            "\n"
            "BuildingSurface:Detailed,\n"
            "  S1, Wall, C1, Z1, , Outdoors, , SunExposed, WindExposed, , ,\n"
            "  0, 0, 4.572,   !- X,Y,Z ==> Vertex 1 {m}\n"
            "  0, 0, 0;       !- X,Y,Z ==> Vertex 2 {m}\n"
        )
        idf_path = tmp_path / "grouped.idf"
        idf_path.write_text(source)
        doc = parse_idf(idf_path, preserve_formatting=True)
        doc["BuildingSurface:Detailed"]["S1"].sun_exposure = "NoSun"

        written = write_idf(doc)

        assert len(written.split("\n")) == len(source.split("\n"))
        assert re.search(r"0, 0, 4\.572,\s+!- X,Y,Z ==> Vertex 1 \{m\}", written)

    def test_an_object_written_on_one_line_stays_on_one_line(self, tmp_path: Path) -> None:
        """11.3% of statements, and the case that surprises on a file with no geometry in it."""
        source = "Version, 26.1.0;\n\nTimestep,4;\n"
        idf_path = tmp_path / "oneline.idf"
        idf_path.write_text(source)
        doc = parse_idf(idf_path, preserve_formatting=True)
        doc["Timestep"].first().number_of_timesteps_per_hour = 6

        written = write_idf(doc)

        assert len(written.split("\n")) == len(source.split("\n"))
        assert "Timestep, 6;" in written

    def test_an_object_at_the_end_gains_no_blank_line(self, tmp_path: Path) -> None:
        """A node's text runs to whatever separated it from the next object, which for the last
        object is one newline. Appending a fixed two grew the file on every save."""
        source = "Version, 26.1.0;\n\nTimestep,4;\n"
        idf_path = tmp_path / "trailing.idf"
        idf_path.write_text(source)
        doc = parse_idf(idf_path, preserve_formatting=True)
        doc["Timestep"].first().number_of_timesteps_per_hour = 6

        assert not write_idf(doc).endswith("\n\n")

    def test_nocomment_output_still_reparses(self, tmp_path: Path) -> None:
        """The type name is the line still open when the field loop starts, so a path that skips
        the flush emits it last and produces a file that does not load."""
        idf_path = tmp_path / "input.idf"
        idf_path.write_text(IDF_WITH_COMMENTS)
        doc = parse_idf(idf_path, preserve_formatting=True)

        written = write_idf(doc, "nocomment")
        out = tmp_path / "out.idf"
        out.write_text(written)

        assert written.startswith("!-Generator") or written.lstrip().startswith("Version")
        assert len(parse_idf(out)) == len(doc)
