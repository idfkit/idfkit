"""Tests for idfkit.codegen — code generation utilities."""

from __future__ import annotations

import json
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from idfkit.codegen.generate_doc_locations import (
    _ANCHOR_RE,  # pyright: ignore[reportPrivateUsage]
    _ANCHOR_STRIP_RE,  # pyright: ignore[reportPrivateUsage]
    _build_anchor_to_object_map,  # pyright: ignore[reportPrivateUsage]
    _find_latest_version_dir,  # pyright: ignore[reportPrivateUsage]
    generate,
)
from idfkit.codegen.generate_doc_locations import (
    main as doc_locations_main,
)
from idfkit.codegen.generate_stubs import (
    _anyof_to_python,  # pyright: ignore[reportPrivateUsage]
    _build_version_availability,  # pyright: ignore[reportPrivateUsage]
    _class_docstring,  # pyright: ignore[reportPrivateUsage]
    _enum_to_literal,  # pyright: ignore[reportPrivateUsage]
    _field_docstring,  # pyright: ignore[reportPrivateUsage]
    _format_constraints,  # pyright: ignore[reportPrivateUsage]
    _generate_attr_properties,  # pyright: ignore[reportPrivateUsage]
    _generate_object_class,  # pyright: ignore[reportPrivateUsage]
    _generate_object_type_map,  # pyright: ignore[reportPrivateUsage]
    _sanitize_docstring,  # pyright: ignore[reportPrivateUsage]
    _schema_type_to_python,  # pyright: ignore[reportPrivateUsage]
    _to_class_name,  # pyright: ignore[reportPrivateUsage]
    _truncate_text,  # pyright: ignore[reportPrivateUsage]
    generate_document_pyi,
    generate_stubs,
)
from idfkit.codegen.generate_stubs import (
    main as stubs_main,
)
from idfkit.schema import EpJSONSchema

# =========================================================================
# generate_doc_locations tests
# =========================================================================


class TestAnchorRegex:
    def test_anchor_re_matches_id_attributes(self) -> None:
        html = '<h2 id="zone-hvac-equipment">Zone HVAC Equipment</h2>'
        matches = _ANCHOR_RE.findall(html)
        assert matches == ["zone-hvac-equipment"]

    def test_anchor_re_multiple_ids(self) -> None:
        html = '<div id="abc"><span id="def-123"></span></div>'
        assert _ANCHOR_RE.findall(html) == ["abc", "def-123"]

    def test_anchor_strip_re(self) -> None:
        assert _ANCHOR_STRIP_RE.sub("", "OS:Zone") == "OSZone"
        assert _ANCHOR_STRIP_RE.sub("", "Material:AirGap") == "MaterialAirGap"
        assert _ANCHOR_STRIP_RE.sub("", "Pipe (Steam)") == "PipeSteam"


class TestBuildAnchorToObjectMap:
    def test_returns_mapping(self) -> None:
        mapping = _build_anchor_to_object_map()
        assert isinstance(mapping, dict)
        assert len(mapping) > 0
        # "Zone" object type should map from anchor "zone"
        assert mapping.get("zone") == "Zone"

    def test_mapping_contains_colon_types(self) -> None:
        mapping = _build_anchor_to_object_map()
        # "BuildingSurface:Detailed" -> anchor "buildingsurfacedetailed"
        assert mapping.get("buildingsurfacedetailed") == "BuildingSurface:Detailed"


class TestFindLatestVersionDir:
    def test_finds_latest(self, tmp_path: Path) -> None:
        (tmp_path / "v24.1").mkdir()
        (tmp_path / "v25.2").mkdir()
        (tmp_path / "v23.0").mkdir()
        result = _find_latest_version_dir(tmp_path)
        assert result is not None
        assert result.name == "v25.2"

    def test_returns_none_for_empty(self, tmp_path: Path) -> None:
        result = _find_latest_version_dir(tmp_path)
        assert result is None

    def test_ignores_non_versioned_dirs(self, tmp_path: Path) -> None:
        (tmp_path / "assets").mkdir()
        (tmp_path / "v10.0").mkdir()
        result = _find_latest_version_dir(tmp_path)
        assert result is not None
        assert result.name == "v10.0"


class TestGenerate:
    def test_generate_scans_html_files(self, tmp_path: Path) -> None:
        # Create a minimal dist structure
        version_dir = tmp_path / "v25.2"
        io_ref = version_dir / "io-reference" / "group-something"
        io_ref.mkdir(parents=True)
        html = io_ref / "index.html"
        html.write_text('<h2 id="zone">Zone</h2><h2 id="material">Material</h2>')

        result = generate(tmp_path)
        assert isinstance(result, dict)
        # Should find "Zone" and "Material" mapped to their paths
        assert "Zone" in result
        assert "Material" in result
        assert result["Zone"] == "io-reference/group-something/#zone"

    def test_generate_exits_when_no_version_dir(self, tmp_path: Path) -> None:
        with pytest.raises(SystemExit):
            generate(tmp_path)

    def test_generate_exits_when_no_io_reference(self, tmp_path: Path) -> None:
        (tmp_path / "v25.2").mkdir()
        with pytest.raises(SystemExit):
            generate(tmp_path)

    def test_generate_sorted_output(self, tmp_path: Path) -> None:
        version_dir = tmp_path / "v25.2"
        io_ref = version_dir / "io-reference" / "page"
        io_ref.mkdir(parents=True)
        (io_ref / "index.html").write_text('<h2 id="zone">Zone</h2><h2 id="material">Material</h2>')

        result = generate(tmp_path)
        keys = list(result.keys())
        assert keys == sorted(keys)

    def test_generate_skips_unmatched_anchors(self, tmp_path: Path) -> None:
        """Cover branch 89->87: anchor not matching any known object type."""
        version_dir = tmp_path / "v25.2"
        io_ref = version_dir / "io-reference" / "page"
        io_ref.mkdir(parents=True)
        # "not-a-real-object" won't match any EnergyPlus type
        (io_ref / "index.html").write_text('<h2 id="not-a-real-object">Nope</h2><h2 id="zone">Zone</h2>')

        result = generate(tmp_path)
        # Only the real "Zone" object should be present; the fake anchor is skipped
        assert set(result.keys()) == {"Zone"}
        assert all("#not-a-real-object" not in v for v in result.values())

    def test_generate_first_match_wins(self, tmp_path: Path) -> None:
        """Cover branch 89: duplicate object type keeps the first location."""
        version_dir = tmp_path / "v25.2"
        page1 = version_dir / "io-reference" / "aaa"
        page2 = version_dir / "io-reference" / "bbb"
        page1.mkdir(parents=True)
        page2.mkdir(parents=True)
        (page1 / "index.html").write_text('<h2 id="zone">Zone</h2>')
        (page2 / "index.html").write_text('<h2 id="zone">Zone again</h2>')

        result = generate(tmp_path)
        assert "Zone" in result
        assert result["Zone"] == "io-reference/aaa/#zone"


class TestDocLocationsMain:
    def test_main_with_valid_dist(self, tmp_path: Path) -> None:
        version_dir = tmp_path / "v25.2"
        io_ref = version_dir / "io-reference" / "page"
        io_ref.mkdir(parents=True)
        (io_ref / "index.html").write_text('<h2 id="zone">Zone</h2>')

        output_path = tmp_path / "doc_locations.json"
        with (
            patch("idfkit.codegen.generate_doc_locations._OUTPUT_PATH", output_path),
            patch.object(sys, "argv", ["prog", str(tmp_path)]),
        ):
            doc_locations_main()

        assert output_path.exists()
        data = json.loads(output_path.read_text())
        assert "Zone" in data

    def test_main_default_argv(self, tmp_path: Path) -> None:
        # Patch _DEFAULT_DOCS_DIST to a guaranteed-missing path so SystemExit is deterministic
        missing_dir = tmp_path / "missing"
        with (
            patch("idfkit.codegen.generate_doc_locations._DEFAULT_DOCS_DIST", missing_dir),
            patch.object(sys, "argv", ["prog"]),
            pytest.raises(SystemExit),
        ):
            doc_locations_main()

    def test_main_nonexistent_dir(self, tmp_path: Path) -> None:
        missing_dir = tmp_path / "missing"
        with (
            patch.object(sys, "argv", ["prog", str(missing_dir)]),
            pytest.raises(SystemExit),
        ):
            doc_locations_main()

    def test_main_via_module_execution(self, tmp_path: Path) -> None:
        """Cover line 111: if __name__ == '__main__'."""
        import runpy

        missing_dir = tmp_path / "missing"
        with (
            patch.object(sys, "argv", ["prog", str(missing_dir)]),
            pytest.raises(SystemExit),
        ):
            runpy.run_module("idfkit.codegen.generate_doc_locations", run_name="__main__")


# =========================================================================
# generate_stubs tests
# =========================================================================


class TestToClassName:
    def test_simple(self) -> None:
        assert _to_class_name("Zone") == "Zone"

    def test_colon_separated(self) -> None:
        assert _to_class_name("BuildingSurface:Detailed") == "BuildingSurfaceDetailed"

    def test_special_chars(self) -> None:
        assert _to_class_name("OS:Zone") == "OSZone"
        assert _to_class_name("Material:AirGap") == "MaterialAirGap"


class TestSchemaTypeToPython:
    def test_with_enum(self) -> None:
        field_schema: dict[str, Any] = {"enum": ["Option1", "Option2"]}
        result = _schema_type_to_python(field_schema, "string")
        assert "Literal" in result
        assert "Option1" in result

    def test_with_anyof(self) -> None:
        field_schema: dict[str, Any] = {
            "anyOf": [{"type": "number"}, {"type": "string", "enum": ["Autosize"]}],
        }
        result = _schema_type_to_python(field_schema, None, has_any_of=True)
        assert "float" in result
        assert "Autosize" in result

    def test_simple_types(self) -> None:
        assert _schema_type_to_python(None, "number") == "float"
        assert _schema_type_to_python(None, "integer") == "int"
        assert _schema_type_to_python(None, "string") == "str"
        assert _schema_type_to_python(None, "array") == "list[Any]"

    def test_unknown_type(self) -> None:
        assert _schema_type_to_python(None, None) == "str | float"

    def test_has_any_of_with_no_field_schema(self) -> None:
        """Cover line 73: has_any_of=True but field_schema is None."""
        result = _schema_type_to_python(None, None, has_any_of=True)
        assert result == "str | float"


class TestEnumToLiteral:
    def test_string_values(self) -> None:
        result = _enum_to_literal(["A", "B", "C"])
        assert result == 'Literal["A", "B", "C"]'

    def test_empty_string(self) -> None:
        result = _enum_to_literal(["", "X"])
        assert result == 'Literal["", "X"]'

    def test_non_string_values(self) -> None:
        """Cover line 88: non-string enum value."""
        result = _enum_to_literal([1, 2.5, "text"])
        assert result == 'Literal[1, 2.5, "text"]'


class TestAnyOfToPython:
    def test_numeric_with_enum(self) -> None:
        schema: dict[str, Any] = {
            "anyOf": [
                {"type": "number"},
                {"type": "string", "enum": ["Autosize"]},
            ],
        }
        result = _anyof_to_python(schema)
        assert "float" in result
        assert "Autosize" in result

    def test_empty_anyof(self) -> None:
        """Cover line 101->99: sub_type not in _ANY_OF_TYPE_MAP."""
        schema: dict[str, Any] = {"anyOf": [{"type": "object"}]}
        result = _anyof_to_python(schema)
        assert result == "str | float"

    def test_no_anyof_key(self) -> None:
        schema: dict[str, Any] = {}
        result = _anyof_to_python(schema)
        assert result == "str | float"

    def test_numeric_enum_with_non_string_values(self) -> None:
        """Cover line 108: non-string value within an anyOf enum."""
        schema: dict[str, Any] = {
            "anyOf": [
                {"type": "number", "enum": [0, 1]},
                {"type": "string", "enum": ["", "Auto"]},
            ],
        }
        result = _anyof_to_python(schema)
        assert "0" in result
        assert "1" in result
        assert "Auto" in result


class TestFormatConstraints:
    def test_minimum(self) -> None:
        assert _format_constraints({"minimum": 0}) == "Range: >= 0"

    def test_exclusive_minimum(self) -> None:
        assert _format_constraints({"exclusiveMinimum": 0}) == "Range: > 0"

    def test_maximum(self) -> None:
        assert _format_constraints({"maximum": 100}) == "Range: <= 100"

    def test_exclusive_maximum(self) -> None:
        assert _format_constraints({"exclusiveMaximum": 100}) == "Range: < 100"

    def test_combined(self) -> None:
        result = _format_constraints({"minimum": 0, "maximum": 1})
        assert result == "Range: >= 0, <= 1"

    def test_unconstrained(self) -> None:
        assert _format_constraints({}) is None


class TestFieldDocstring:
    def test_with_note(self) -> None:
        result = _field_docstring({"note": "Some useful note"})
        assert result is not None
        assert "Some useful note" in result

    def test_with_units(self) -> None:
        result = _field_docstring({"units": "W/m2"})
        assert result is not None
        assert "[W/m2]" in result

    def test_with_ip_units(self) -> None:
        result = _field_docstring({"units": "W/m2", "ip-units": "Btu/h-ft2"})
        assert result is not None
        assert "(Btu/h-ft2)" in result

    def test_with_default(self) -> None:
        result = _field_docstring({"default": 0.5})
        assert result is not None
        assert "Default: 0.5" in result

    def test_with_since(self) -> None:
        result = _field_docstring(None, since_version=(24, 1, 0))
        assert result is not None
        assert "Since: 24.1.0" in result

    def test_none_when_empty(self) -> None:
        assert _field_docstring(None) is None

    def test_none_when_no_useful_metadata(self) -> None:
        assert _field_docstring({}) is None

    def test_long_note_truncated(self) -> None:
        long_note = "A" * 200
        result = _field_docstring({"note": long_note})
        assert result is not None
        assert len(result) <= 130  # truncated + other fields


class TestSanitizeDocstring:
    def test_replaces_double_quotes(self) -> None:
        assert _sanitize_docstring('say "hello"') == "say 'hello'"

    def test_replaces_unicode_quotes(self) -> None:
        assert _sanitize_docstring("it\u2019s") == "it's"
        assert _sanitize_docstring("\u201cquote\u201d") == "'quote'"

    def test_replaces_unicode_dashes(self) -> None:
        assert _sanitize_docstring("a\u2013b") == "a-b"
        assert _sanitize_docstring("a\u2014b") == "a-b"


class TestTruncateText:
    def test_short_text(self) -> None:
        assert _truncate_text("hello world") == "hello world"

    def test_collapses_whitespace(self) -> None:
        assert _truncate_text("hello   world\n\tnext") == "hello world next"

    def test_truncates_long_text(self) -> None:
        result = _truncate_text("A" * 200, max_len=50)
        assert len(result) == 50
        assert result.endswith("...")


class TestClassDocstring:
    def test_with_memo(self) -> None:
        result = _class_docstring("A test memo", None)
        assert result is not None
        assert "A test memo" in result

    def test_with_since(self) -> None:
        # Only shown if after ENERGYPLUS_VERSIONS[0]
        result = _class_docstring(None, (25, 2, 0))
        assert result is not None
        assert "Since: 25.2.0" in result

    def test_none_when_empty(self) -> None:
        assert _class_docstring(None, None) is None

    def test_earliest_version_not_shown(self) -> None:
        from idfkit.versions import ENERGYPLUS_VERSIONS

        result = _class_docstring(None, ENERGYPLUS_VERSIONS[0])
        assert result is None


class TestGenerateObjectClass:
    def test_basic_class(self, schema: EpJSONSchema) -> None:
        lines = _generate_object_class(schema, "Zone")
        text = "\n".join(lines)
        assert "class Zone(IDFObject):" in text

    def test_class_with_version_info(self, schema: EpJSONSchema) -> None:
        type_since = {"Zone": (8, 9, 0)}
        field_since: dict[tuple[str, str], tuple[int, int, int]] = {}
        lines = _generate_object_class(schema, "Zone", type_since=type_since, field_since=field_since)
        text = "\n".join(lines)
        assert "class Zone(IDFObject):" in text

    def test_class_with_no_fields_no_docstring(self) -> None:
        """Cover line 302: object type with no fields and no docstring."""
        mock_schema = MagicMock()
        mock_schema.get_field_names.return_value = []
        mock_schema.is_extensible.return_value = False
        mock_schema.get_object_memo.return_value = None
        lines = _generate_object_class(mock_schema, "FakeEmpty")
        assert lines == ["class FakeEmpty(IDFObject): ..."]

    def test_class_with_no_fields_but_docstring(self, schema: EpJSONSchema) -> None:
        """Cover line 304: no-fields type that has a docstring."""
        # Version (real type with memo but no fields)
        lines = _generate_object_class(schema, "Version")
        text = "\n".join(lines)
        assert "class Version(IDFObject):" in text

    def test_extensible_type(self, schema: EpJSONSchema) -> None:
        lines = _generate_object_class(schema, "BuildingSurface:Detailed")
        text = "\n".join(lines)
        assert "class BuildingSurfaceDetailed(IDFObject):" in text


class TestGenerateObjectTypeMap:
    def test_generates_typed_dict(self, schema: EpJSONSchema) -> None:
        lines = _generate_object_type_map(schema)
        text = "\n".join(lines)
        assert "_ObjectTypeMap" in text
        assert "TypedDict" in text
        assert '"Zone": IDFCollection[Zone]' in text


class TestGenerateAttrProperties:
    def test_generates_properties(self) -> None:
        mapping = {"zones": "Zone", "materials": "Material"}
        lines = _generate_attr_properties(mapping)
        text = "\n".join(lines)
        assert "@property" in text
        assert "def zones(self) -> IDFCollection[Zone]: ..." in text

    def test_skips_reserved(self) -> None:
        mapping = {"version": "Version", "zones": "Zone"}
        lines = _generate_attr_properties(mapping)
        text = "\n".join(lines)
        assert "def version" not in text
        assert "def zones" in text


class TestBuildVersionAvailability:
    def test_returns_type_and_field_since(self) -> None:
        # Patch ENERGYPLUS_VERSIONS to a small subset to keep this test fast
        patched_versions = [(24, 1, 0), (24, 2, 0)]
        with patch("idfkit.codegen.generate_stubs.ENERGYPLUS_VERSIONS", patched_versions):
            type_since, field_since = _build_version_availability()
        assert isinstance(type_since, dict)
        assert isinstance(field_since, dict)
        # Zone should exist and be associated with the earliest patched version
        assert "Zone" in type_since
        assert type_since["Zone"] == min(patched_versions)


class TestGenerateStubs:
    def test_generates_valid_output(self) -> None:
        # Use a specific version to keep it fast
        content = generate_stubs((24, 1, 0))
        assert "Auto-generated type stubs" in content
        assert "class Zone(IDFObject):" in content
        assert "_ObjectTypeMap" in content
        assert "from __future__ import annotations" in content

    def test_default_version(self) -> None:
        content = generate_stubs()
        assert "Auto-generated type stubs" in content


class TestGenerateDocumentPyi:
    def test_generates_valid_output(self) -> None:
        content = generate_document_pyi((24, 1, 0))
        assert "class IDFDocument" in content
        assert "def __init__" in content
        assert "@property" in content
        assert "from __future__ import annotations" in content


@pytest.fixture
def _preserve_generated_stubs() -> Iterator[tuple[Path, Path]]:
    """Back up and restore generated stub files around a test."""
    import idfkit.codegen.generate_stubs as stubs_mod

    real_base = Path(stubs_mod.__file__).resolve().parent.parent
    types_file = real_base / "_generated_types.pyi"
    doc_file = real_base / "document.pyi"

    types_backup = types_file.read_text() if types_file.exists() else None
    doc_backup = doc_file.read_text() if doc_file.exists() else None

    yield types_file, doc_file

    if types_backup is not None:
        types_file.write_text(types_backup)
    elif types_file.exists():
        types_file.unlink()
    if doc_backup is not None:
        doc_file.write_text(doc_backup)
    elif doc_file.exists():
        doc_file.unlink()


class TestStubsMain:
    def test_main_writes_files(self, tmp_path: Path) -> None:
        """Cover lines 589-616: main() function."""
        import idfkit.codegen.generate_stubs as stubs_mod

        fake_file = str(tmp_path / "codegen" / "generate_stubs.py")
        with (
            patch.object(stubs_mod, "__file__", fake_file),
            patch("subprocess.run"),
            patch.object(sys, "argv", ["prog", "24.1.0"]),
        ):
            stubs_main()
        types_file = tmp_path / "_generated_types.pyi"
        doc_file = tmp_path / "document.pyi"
        assert types_file.exists()
        assert doc_file.exists()
        assert types_file.stat().st_size > 0
        assert doc_file.stat().st_size > 0

    def test_main_default_version(self, tmp_path: Path) -> None:
        """Cover main() with no version argument."""
        import idfkit.codegen.generate_stubs as stubs_mod

        fake_file = str(tmp_path / "codegen" / "generate_stubs.py")
        with (
            patch.object(stubs_mod, "__file__", fake_file),
            patch("subprocess.run"),
            patch.object(sys, "argv", ["prog"]),
        ):
            stubs_main()
        assert (tmp_path / "_generated_types.pyi").exists()

    def test_main_via_module_execution(self, tmp_path: Path) -> None:
        """Cover line 620: if __name__ == '__main__'."""
        import runpy

        import idfkit.codegen.generate_stubs as stubs_mod

        fake_file = str(tmp_path / "codegen" / "generate_stubs.py")
        with (
            patch.object(stubs_mod, "__file__", fake_file),
            patch("subprocess.run"),
            patch.object(sys, "argv", ["prog", "24.1.0"]),
        ):
            runpy.run_module("idfkit.codegen.generate_stubs", run_name="__main__")


class TestGenerateFieldsWithSinceVersion:
    """Test field_since logic in _generate_fields (line 338->343)."""

    def test_field_since_shown_when_newer_than_type(self, schema: EpJSONSchema) -> None:
        type_since = {"Zone": (8, 9, 0)}
        # Set a field to appear in a later version
        field_since: dict[tuple[str, str], tuple[int, int, int]] = {
            ("Zone", "direction_of_relative_north"): (24, 1, 0),
        }
        lines = _generate_object_class(
            schema,
            "Zone",
            type_since=type_since,
            field_since=field_since,
        )
        text = "\n".join(lines)
        assert "Since: 24.1.0" in text

    def test_field_since_not_shown_when_same_as_type(self, schema: EpJSONSchema) -> None:
        """Cover branch 338->343: field appeared same version as type."""
        type_since = {"Zone": (8, 9, 0)}
        field_since: dict[tuple[str, str], tuple[int, int, int]] = {
            ("Zone", "direction_of_relative_north"): (8, 9, 0),
        }
        lines = _generate_object_class(
            schema,
            "Zone",
            type_since=type_since,
            field_since=field_since,
        )
        # "Since:" should NOT appear for this field (same version as type)
        assert not any("Since: 8.9.0" in line for line in lines)
