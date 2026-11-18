"""Tests for idfkit.codegen — code generation utilities."""

from __future__ import annotations

import ast
import json
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from idfkit.codegen import generate_stubs as gen
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
    _generate_getitem,  # pyright: ignore[reportPrivateUsage]
    _generate_not_an_object_type,  # pyright: ignore[reportPrivateUsage]
    _generate_object_class,  # pyright: ignore[reportPrivateUsage]
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
from idfkit.schema import EpJSONSchema, get_schema
from idfkit.versions import LATEST_VERSION

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
        """Cover branch 89: duplicate object type keeps the first location.

        generate() iterates HTML files via sorted(rglob(...)), so "aaa" comes
        before "bbb" alphabetically — the winner is deterministic regardless of
        filesystem iteration order.
        """
        version_dir = tmp_path / "v25.2"
        # Directory names are chosen so that sorted order is aaa < bbb
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

    @pytest.mark.filterwarnings("ignore::RuntimeWarning")
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
        # A blank choice is stored as absent and reads None, so it is not a value of the field.
        assert _enum_to_literal(["", "X"]) == 'Literal["X"]'
        assert _enum_to_literal([""]) == "str"

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
        # _truncate_text caps at max_len=120: first 117 chars + "..."
        assert len(result) == 120
        assert result.endswith("...")


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
        assert "class Zone(_TypedIDFObject):" in text

    def test_class_with_version_info(self, schema: EpJSONSchema) -> None:
        type_since = {"Zone": (8, 9, 0)}
        field_since: dict[tuple[str, str], tuple[int, int, int]] = {}
        lines = _generate_object_class(schema, "Zone", type_since=type_since, field_since=field_since)
        text = "\n".join(lines)
        assert "class Zone(_TypedIDFObject):" in text

    def test_class_with_no_fields_no_docstring(self) -> None:
        """Cover line 302: object type with no fields and no docstring."""
        mock_schema = MagicMock()
        mock_schema.get_field_names.return_value = []
        mock_schema.is_extensible.return_value = False
        mock_schema.get_object_memo.return_value = None
        lines = _generate_object_class(mock_schema, "FakeEmpty", emit_update=False)
        assert lines == ["class FakeEmpty(_TypedIDFObject): ..."]

    def test_class_with_no_fields_declares_its_creation_signature(self, schema: EpJSONSchema) -> None:
        # A type with no field at all still says what add() takes: here nothing, not even a name.
        mock_schema = MagicMock()
        mock_schema.get_field_names.return_value = []
        mock_schema.get_object_memo.return_value = None
        mock_schema.get_inner_schema.return_value = {}
        mock_schema.has_name.return_value = False
        lines = _generate_object_class(mock_schema, "FakeEmpty")
        assert lines[0] == "class FakeEmpty(_TypedIDFObject):"
        assert lines[-1].startswith("    _creation_signature: _c")

    def test_class_with_no_fields_but_docstring(self, schema: EpJSONSchema) -> None:
        """Cover line 304: no-fields type that has a docstring."""
        # Version (real type with memo but no fields)
        lines = _generate_object_class(schema, "Version")
        text = "\n".join(lines)
        assert "class Version(_TypedIDFObject):" in text

    def test_extensible_type(self, schema: EpJSONSchema) -> None:
        lines = _generate_object_class(schema, "BuildingSurface:Detailed")
        text = "\n".join(lines)
        assert "class BuildingSurfaceDetailed(_TypedIDFObject):" in text
        assert "class BuildingSurfaceDetailedVerticesGroup(_TypedExtensibleGroup):" in text


class TestGenerateGetitem:
    def test_one_overload_per_object_type_then_one_matching_nothing(self) -> None:
        lines = _generate_getitem([("Zone", "Zone"), ("Material", "Material")], "EnergyPlus24_1")
        text = "\n".join(lines)
        assert 'def __getitem__(self, obj_type: Literal["Zone"], /) -> IDFCollection[Zone]: ...' in text
        assert text.count("@overload") == 3
        assert lines[-1] == (
            "    def __getitem__(self, obj_type: _NotAnObjectTypeOfEnergyPlus24_1, /) -> IDFCollection[IDFObject]: ..."
        )
        assert "TypedDict" not in text

    def test_the_type_matching_nothing_is_a_sequence_so_mypy_reports_one_overload(self) -> None:
        # mypy reports a call no overload matches against the one overload whose parameter is a
        # generic class in str's MRO, whatever its argument; finding none, it lists every overload.
        text = "\n".join(_generate_not_an_object_type("EnergyPlus24_1", "EnergyPlus 24.1.0 has"))
        assert "class _NotAnObjectTypeNameOfEnergyPlus24_1:" in text
        assert "_NotAnObjectTypeOfEnergyPlus24_1: TypeAlias = Sequence[_NotAnObjectTypeNameOfEnergyPlus24_1]" in text


class TestGenerateAttrProperties:
    def test_generates_properties(self) -> None:
        from idfkit.schema import get_schema

        schema = get_schema((24, 1, 0))
        mapping = {"zones": "Zone", "materials": "Material"}
        lines = _generate_attr_properties(mapping, schema)
        text = "\n".join(lines)
        assert "@property" in text
        # The signature is now followed by a docstring instead of `: ...`
        assert "def zones(self) -> IDFCollection[Zone]:" in text
        assert '"""All ``Zone`` objects in the document.' in text

    def test_skips_reserved(self) -> None:
        from idfkit.schema import get_schema

        schema = get_schema((24, 1, 0))
        mapping = {"version": "Version", "zones": "Zone"}
        lines = _generate_attr_properties(mapping, schema)
        text = "\n".join(lines)
        assert "def version" not in text
        assert "def zones" in text

    def test_skips_every_real_member_of_the_document(self) -> None:
        """The skip set is the document's own reserved set, not a second hand-written list.

        Covers members the old list never named, such as ``add`` and ``all_objects``,
        so a shorthand colliding with any future member is skipped here exactly as the
        resolver drops it at runtime.
        """
        from idfkit.document import _RESERVED  # pyright: ignore[reportPrivateUsage]
        from idfkit.schema import get_schema

        schema = get_schema((24, 1, 0))
        assert {"add", "all_objects", "version"} <= _RESERVED
        lines = _generate_attr_properties(dict.fromkeys(_RESERVED, "Zone"), schema)
        assert lines == []


class TestBuildVersionAvailability:
    def test_returns_type_and_field_since(self) -> None:
        # Patch ENERGYPLUS_VERSIONS to a small subset to keep this test fast
        patched_versions = [(24, 1, 0), (24, 2, 0)]
        with patch("idfkit.codegen.generate_stubs.ENERGYPLUS_VERSIONS", patched_versions):
            type_since, field_since = _build_version_availability()
        # Both dicts must be non-empty
        assert len(type_since) > 0
        assert len(field_since) > 0
        # "Zone" is a well-known type present in every EnergyPlus version
        assert "Zone" in type_since
        assert type_since["Zone"] == min(patched_versions)
        # At least one well-known Zone field should be present in field_since
        assert any(obj_type == "Zone" for obj_type, _ in field_since)


class TestGenerateStubs:
    def test_generates_valid_output(self) -> None:
        # Use a specific version to keep it fast
        content = generate_stubs((24, 1, 0))
        assert "Auto-generated type stubs" in content
        # Zone's declaration changed between releases, so it derives from its shared base.
        assert "class Zone(AnyZone):" in content
        assert "class AnyZone(_TypedIDFObject):" in content
        # The stub-only bases switch off the catch-all attribute access with a name type no string is,
        # a class named for the mistake, which pyright prints for the name and mypy for the value.
        assert "class _NotAFieldOfThisObjectType:" in content
        assert "class _NotAFieldOfThisExtensibleGroup:" in content
        assert "TypeAlias = Never" not in content
        assert "class _TypedIDFObject(IDFObject):" in content
        assert "def __getattr__(self, key: _NotAFieldOfThisObjectType) -> object: ..." in content
        assert "class _TypedExtensibleGroup(ExtensibleGroup):" in content
        assert (
            "def __setattr__(self, name: _NotAFieldOfThisExtensibleGroup, value: _NotAFieldOfThisExtensibleGroup)"
            " -> None: ..." in content
        )
        # ReadOnly typed the entries of the TypedDict maps, which are gone; nothing else uses it.
        assert "from typing_extensions import Unpack" in content
        # A trailing-underscore field is declared under both spellings the runtime accepts.
        assert "    cond_flag_is_the_basement_conditioned_: " in content
        assert "    cond_flag_is_the_basement_conditioned: " in content
        # The document types are not TypedDicts (see TestGenerateGetitem), so no map is generated.
        assert "_ObjectTypeMap" not in content
        assert "from __future__ import annotations" in content
        # Validate that the output is syntactically valid Python
        ast.parse(content)

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
        # Validate that the output is syntactically valid Python
        ast.parse(content)


@pytest.fixture
def _preserve_generated_stubs() -> Iterator[tuple[Path, Path]]:
    """Back up and restore generated stub files around a test."""
    import idfkit.codegen.generate_stubs as stubs_mod

    real_base = Path(stubs_mod.__file__).resolve().parent.parent
    types_file = real_base / "_generated_types.pyi"
    doc_file = real_base / "document.pyi"
    documents_dir = real_base / "_versioned"
    creation_dir = real_base / "_creation"
    generated = [
        types_file,
        doc_file,
        real_base / "versioned.pyi",
        real_base / "versioned.py",
        real_base / "_read_required.py",
    ]
    generated += sorted(documents_dir.glob("*.pyi"))
    generated += sorted(creation_dir.glob("*.pyi"))
    backups = {path: path.read_text(encoding="utf-8") if path.exists() else None for path in generated}

    yield types_file, doc_file

    for path, backup in backups.items():
        if backup is not None:
            path.write_text(backup, encoding="utf-8")
        elif path.exists():
            path.unlink()
    # A generation for an older release writes modules the committed set does not have.
    for path in [*documents_dir.glob("*.pyi"), *creation_dir.glob("*.pyi")]:
        if path not in backups:
            path.unlink()


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
        # One module per release older than the one generated for.
        assert (tmp_path / "_versioned" / "__init__.pyi").exists()
        assert (tmp_path / "_versioned" / "v23_2.pyi").exists()
        assert not (tmp_path / "_versioned" / "v24_1.pyi").exists()

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

    @pytest.mark.filterwarnings("ignore::RuntimeWarning")
    @pytest.mark.usefixtures("_preserve_generated_stubs")
    def test_main_via_module_execution(self, tmp_path: Path) -> None:
        """Cover line 620: if __name__ == '__main__'.

        ``runpy.run_module(run_name="__main__")`` re-imports the module fresh
        and resets ``__file__`` to the real on-disk path, so the
        ``patch.object(stubs_mod, "__file__", ...)`` does *not* take effect for
        this test.  The ``_preserve_generated_stubs`` fixture backs up and
        restores the real stub files so this test does not corrupt them.
        """
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


# =========================================================================
# The creation signature: what IDFCollection.add() takes
# =========================================================================


_LATEST = get_schema(LATEST_VERSION)


def _signature_of(sink: gen._CreationModules, cls_name: str) -> str:  # pyright: ignore[reportPrivateUsage]
    """The ``__call__`` line *sink* filed for *cls_name*."""
    for lines in sink.classes.values():
        for i, line in enumerate(lines):
            if line == f"class {cls_name}:":
                return lines[i + 1]
    pytest.fail(f"no creation signature for {cls_name}")


class TestCreationSignature:
    @pytest.mark.parametrize(
        ("value", "rendered"),
        [
            (0.9, "0.9"),
            (-1.5, "-1.5"),
            (2.0, "2"),  # some releases give an integer field's default as a float
            (6, "6"),
            ("Rough", '"Rough"'),
            ("", '""'),
            (True, None),  # booleans are not shown
            (1e-05, None),  # exponent notation is not shown
            ([1, 2], None),
            ("x" * 41, None),  # long strings are not shown
            ('say "hi"', None),
            ("back\\slash", None),
        ],
    )
    def test_render_default(self, value: object, rendered: str | None) -> None:
        assert gen._render_default(value) == rendered  # pyright: ignore[reportPrivateUsage]

    def test_required_fields_are_those_the_schema_requires_without_default(self) -> None:
        info = gen._creation_info(get_schema(LATEST_VERSION), "Material")  # pyright: ignore[reportPrivateUsage]
        assert info.name == "required"
        assert info.required == {"roughness", "thickness", "conductivity", "density", "specific_heat"}
        assert ("thermal_absorptance", "0.9") in info.defaults

    @pytest.mark.parametrize(
        ("obj_type", "kind"), [("Zone", "required"), ("Building", "optional"), ("Output:SQLite", "none")]
    )
    def test_name_kind(self, obj_type: str, kind: str) -> None:
        assert gen._creation_info(get_schema(LATEST_VERSION), obj_type).name == kind  # pyright: ignore[reportPrivateUsage]

    def test_rendering(self) -> None:
        sink = gen._CreationModules()  # pyright: ignore[reportPrivateUsage]
        creation = gen._Creation(  # pyright: ignore[reportPrivateUsage]
            "required",
            frozenset({"a"}),
            (("b", '"X"'), ("c", "0.5"), ("d", '"Z"')),
        )
        fields = [
            ("a", "float | None"),
            ("b", 'Literal["X", "Y"] | None'),
            ("c", "float | None"),
            ("d", 'Literal["X", "Y"] | None'),  # its default is not one of its values: "..."
        ]
        lines = gen._creation_lines("Cls", fields, creation, "    ", sink, _LATEST, "Zone")  # pyright: ignore[reportPrivateUsage]
        assert len(lines) == 1
        assert lines[0].startswith("    _creation_signature: _c")
        assert lines[0].endswith(".Cls  # type: ignore[assignment]")
        assert _signature_of(sink, "Cls") == (
            '    def __call__(self, name: str, /, *, a: float, b: Literal["X", "Y"] | None = "X", '
            'c: float | None = 0.5, d: Literal["X", "Y"] | None = ...) -> None:'
        )

    @pytest.mark.parametrize(
        "fields",
        [
            [("a", "float | None")],  # "e" is required but not declared (renamed in some release)
            [("a", "float | None"), ("e", "None")],  # declared, but only None is safe to write
        ],
    )
    def test_a_required_field_no_value_can_be_given_for_asks_to_narrow(self, fields: list[tuple[str, str]]) -> None:
        sink = gen._CreationModules()  # pyright: ignore[reportPrivateUsage]
        creation = gen._Creation("none", frozenset({"a", "e"}), ())  # pyright: ignore[reportPrivateUsage]
        gen._creation_lines("Cls", fields, creation, "    ", sink, _LATEST, "Zone")  # pyright: ignore[reportPrivateUsage]
        assert _signature_of(sink, "Cls").startswith(
            "    def __call__(self, this_type_has_no_name_field: _g._PassFieldsAsKeywords = ..., /, *, narrow_with_as_version_first: Never, a: float"
        )

    def test_the_alias_of_a_required_key_is_not_offered(self) -> None:
        # The run time takes either spelling of gas_or_gas_mixture_, but not both: offering the
        # alias beside the required key would type-check a call the run time refuses.
        sink = gen._CreationModules()  # pyright: ignore[reportPrivateUsage]
        lines = _generate_object_class(get_schema(LATEST_VERSION), "WindowMaterial:Gap", sink=sink)
        assert any(line.strip() == "gas_or_gas_mixture: str" for line in lines)  # still an attribute, required on read
        signature = _signature_of(sink, "WindowMaterialGap")
        assert "gas_or_gas_mixture_: str," in signature
        assert "gas_or_gas_mixture:" not in signature

    def test_nameless_type_without_fields(self) -> None:
        sink = gen._CreationModules()  # pyright: ignore[reportPrivateUsage]
        creation = gen._Creation("none", frozenset(), ())  # pyright: ignore[reportPrivateUsage]
        gen._creation_lines("Bare", [], creation, "    ", sink, _LATEST, "Output:SQLite")  # pyright: ignore[reportPrivateUsage]
        # The guard takes the place of the name, so a name passed by mistake is reported as such.
        assert _signature_of(sink, "Bare") == (
            "    def __call__(self, this_type_has_no_name_field: _g._PassFieldsAsKeywords = ..., /) -> None:"
        )
        module = next(source for source in sink.sources().values() if "class Bare:" in source)
        assert "from .. import _generated_types as _g" in module

    def test_the_class_declares_the_signature_its_update_keywords_make(self) -> None:
        sink = gen._CreationModules()  # pyright: ignore[reportPrivateUsage]
        lines = _generate_object_class(get_schema(LATEST_VERSION), "Material", sink=sink)
        assert any(line.startswith("    _creation_signature: _c") for line in lines)
        signature = _signature_of(sink, "Material")
        assert "self, name: str, /, *, roughness: Literal[" in signature
        assert "thickness: float, conductivity: float, density: float, specific_heat: float," in signature
        assert "thermal_absorptance: float | None = 0.9" in signature

    def test_modules_import_only_what_they_use(self) -> None:
        sink = gen._CreationModules()  # pyright: ignore[reportPrivateUsage]
        sources = sink.sources()
        assert len(sources) == gen._CREATION_BUCKETS  # pyright: ignore[reportPrivateUsage]
        assert not any("from typing" in source for source in sources.values())
        gen._creation_lines(  # pyright: ignore[reportPrivateUsage]
            "Cls",
            [("a", 'Literal["X"] | None')],
            gen._Creation("none", frozenset(), ()),  # pyright: ignore[reportPrivateUsage]
            "    ",
            sink,
            _LATEST,
            "Zone",
        )
        module = next(source for source in sink.sources().values() if "class Cls:" in source)
        assert "from typing import Literal\n" in module
        ast.parse(module)

    def test_a_docstring_imports_nothing(self) -> None:
        # A schema memo can say "Any", "Never" or "_g."; only what the signature uses is imported.
        sink = gen._CreationModules()  # pyright: ignore[reportPrivateUsage]
        sink.add("Cls", "self, /", "Any number of things. Never _g.Zone.")
        module = next(source for source in sink.sources().values() if "class Cls:" in source)
        assert "from typing" not in module
        assert "typing_extensions" not in module
        assert "_generated_types" not in module


def _docstring_of(sink: gen._CreationModules, cls_name: str) -> str:  # pyright: ignore[reportPrivateUsage]
    """The docstring of the ``__call__`` *sink* filed for *cls_name*: what an editor shows for ``add()``."""
    for source in sink.sources().values():
        for node in ast.parse(source).body:
            if isinstance(node, ast.ClassDef) and node.name == cls_name:
                call = node.body[0]
                assert isinstance(call, ast.FunctionDef)
                doc = ast.get_docstring(call)
                assert doc is not None
                return doc
    pytest.fail(f"no creation signature for {cls_name}")


class TestCreationDocstring:
    """The creation signature's docstring is the one an editor shows for ``add()`` on the type."""

    def test_names_the_type_gives_its_memo_whole_and_links_its_page(self) -> None:
        sink = gen._CreationModules()  # pyright: ignore[reportPrivateUsage]
        _generate_object_class(_LATEST, "Schedule:Constant", sink=sink)
        assert _docstring_of(sink, "ScheduleConstant") == (
            "Create a new ``Schedule:Constant`` and add it to the document.\n\n"
            "Constant hourly value for entire year.\n\n"
            "EnergyPlus I/O Reference: "
            "https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#scheduleconstant"
        )

    def test_the_memo_is_not_truncated(self) -> None:
        memo = _LATEST.get_object_memo("Material:NoMass")
        assert memo is not None
        sink = gen._CreationModules()  # pyright: ignore[reportPrivateUsage]
        _generate_object_class(_LATEST, "Material:NoMass", sink=sink)
        assert " ".join(memo.split()) in _docstring_of(sink, "MaterialNoMass")

    def test_a_name_one_release_requires_and_another_refuses_is_a_conflict(self) -> None:
        # Output:Table:ReportPeriod has no Name field before 25.2 and requires one from it on.
        sink = gen._CreationModules()  # pyright: ignore[reportPrivateUsage]
        versions = gen._versions_with("Output:Table:ReportPeriod")  # pyright: ignore[reportPrivateUsage]
        creation = gen._creation_for("Output:Table:ReportPeriod", versions)  # pyright: ignore[reportPrivateUsage]
        assert creation.name_conflict
        gen._creation_lines(
            "Cls", [("a", "float | None")], creation, "    ", sink, _LATEST, "Output:Table:ReportPeriod"
        )  # pyright: ignore[reportPrivateUsage]
        assert "narrow_with_as_version_first: Never" in _signature_of(sink, "Cls")

    def test_says_to_narrow_where_no_call_suits_every_release(self) -> None:
        sink = gen._CreationModules()  # pyright: ignore[reportPrivateUsage]
        generate_stubs(sink=sink)
        assert "narrow the document with ``as_version`` first" in _docstring_of(sink, "AnyPeople")
        assert "narrow the document" not in _docstring_of(sink, "People")

    def test_an_older_release_links_its_own_documentation(self) -> None:
        sink = gen._CreationModules("_v", "_cv")  # pyright: ignore[reportPrivateUsage]
        gen.generate_versioned_pyi(sink)
        doc = _docstring_of(sink, "InternalMass_v9_2_to_v9_5")
        assert doc.startswith("Create a new ``InternalMass`` and add it to the document.")
        assert "https://docs.idfkit.com/v9.5/" in doc

    def test_a_docstring_survives_quotes_and_backslashes(self) -> None:
        schema = MagicMock(spec=EpJSONSchema)
        schema.version = LATEST_VERSION
        schema.get_object_memo.return_value = 'A "quoted" C:\\path memo'
        schema.get_group.return_value = None
        doc = gen._creation_docstring(schema, "Not:AType", narrow_first=False)  # pyright: ignore[reportPrivateUsage]
        sink = gen._CreationModules()  # pyright: ignore[reportPrivateUsage]
        sink.add("Cls", "self, /", doc)
        assert (
            _docstring_of(sink, "Cls")
            == "Create a new ``Not:AType`` and add it to the document.\n\nA 'quoted' C:\\path memo"
        )


class TestCreationAcrossReleases:
    """Any<Class> requires what any release requires; each release's class requires its own."""

    def test_no_subclass_requires_more_than_its_base(self) -> None:
        # IDFCollection is covariant: a subclass's collection passes for its base's, whose add()
        # would then accept a call the subclass's releases refuse.
        runs = gen._build_type_runs()  # pyright: ignore[reportPrivateUsage]
        for obj_type, run, piece, cls_name, base in gen._piece_classes():  # pyright: ignore[reportPrivateUsage]
            sub = gen._creation_for(obj_type, piece)  # pyright: ignore[reportPrivateUsage]
            if base.startswith("_g.Any"):
                assert not gen._relaxes(sub, gen._class_creation(obj_type, run)), cls_name  # pyright: ignore[reportPrivateUsage]
                assert obj_type in gen._shared_layout(), cls_name  # pyright: ignore[reportPrivateUsage]
            else:
                assert gen._relaxes(sub, gen._class_creation(obj_type, run)), cls_name  # pyright: ignore[reportPrivateUsage]
        stricter = {cls for _, _, _, cls, base in gen._piece_classes() if base.startswith("_g.Any")}  # pyright: ignore[reportPrivateUsage]
        assert "BuildingSurfaceDetailed_v25_1_to_v26_1" in stricter
        assert runs

    def test_any_class_requires_what_any_release_requires(self) -> None:
        # EnergyManagementSystem:Program: 8.9 requires no lines, every later release does.
        versions = gen._versions_with("EnergyManagementSystem:Program")  # pyright: ignore[reportPrivateUsage]
        creation = gen._creation_for("EnergyManagementSystem:Program", versions)  # pyright: ignore[reportPrivateUsage]
        assert creation.required == {"lines"}
        sink = gen._CreationModules()  # pyright: ignore[reportPrivateUsage]
        stub = generate_stubs(sink=sink)
        # 26.2 requires them too, so the latest class serves every release: Any<Class> is an alias.
        assert "AnyEnergyManagementSystemProgram: TypeAlias = EnergyManagementSystemProgram" in stub
        assert (
            "lines: Sequence[_g.EnergyManagementSystemProgramLinesItem | _g.EnergyManagementSystemProgramLinesGroup])"
            in _signature_of(sink, "EnergyManagementSystemProgram")
        )
        # BuildingSurface:Detailed: 8.9 to 26.1 require the construction, 26.2 does not.
        assert "construction_name: str," in _signature_of(sink, "AnyBuildingSurfaceDetailed")
        assert "construction_name: str | None = ..." in _signature_of(sink, "BuildingSurfaceDetailed")

    def test_any_class_asks_to_narrow_when_no_call_suits_every_release(self) -> None:
        # People's zone is required everywhere but renamed in 9.6, so AnyPeople does not declare it.
        sink = gen._CreationModules()  # pyright: ignore[reportPrivateUsage]
        generate_stubs(sink=sink)
        assert "narrow_with_as_version_first: Never" in _signature_of(sink, "AnyPeople")
        assert "narrow_with_as_version_first" not in _signature_of(sink, "People")
        assert "narrow_with_as_version_first" not in _signature_of(sink, "AnyMaterial")

    def test_any_class_shows_a_default_only_where_every_release_agrees(self) -> None:
        obj_type = "HeatExchanger:Desiccant:BalancedFlow"
        versions = gen._versions_with(obj_type)  # pyright: ignore[reportPrivateUsage]
        defaults = {
            dict(gen._creation_info(get_schema(v), obj_type).defaults).get("economizer_lockout")  # pyright: ignore[reportPrivateUsage]
            for v in versions
        }
        assert len(defaults) > 1
        assert "economizer_lockout" not in dict(gen._creation_for(obj_type, versions).defaults)  # pyright: ignore[reportPrivateUsage]

    def test_a_default_alone_does_not_make_a_class(self) -> None:
        # Version's default differs in every release; its fields and required fields do not.
        class_for, _ = gen._class_assignment()  # pyright: ignore[reportPrivateUsage]
        assert {class_for["Version", v] for v in gen._versions_with("Version")} == {"_g.Version"}  # pyright: ignore[reportPrivateUsage]
        assert "AnyVersion: TypeAlias = Version" in generate_stubs()

    def test_a_release_that_requires_other_fields_gets_a_subclass_of_its_range_class(self) -> None:
        # ZoneControl:ContaminantController's fields are typed alike in every release, but 26.2
        # alone requires the CO2 schedule: the older releases get a subclass of the latest class.
        class_for, _ = gen._class_assignment()  # pyright: ignore[reportPrivateUsage]
        obj_type = "ZoneControl:ContaminantController"
        assert class_for[obj_type, LATEST_VERSION] == "_g.ZoneControlContaminantController"
        older = class_for[obj_type, (26, 1, 0)]
        assert older == "ZoneControlContaminantController_v8_9_to_v26_1"
        stub = gen.generate_versioned_pyi()
        assert f"class {older}(_g.ZoneControlContaminantController):" in stub

    @pytest.mark.parametrize(
        "name",
        [
            # Classes of ranges that ended before the latest release keep their names: these split
            # into pieces with other required fields or name, and stay their pieces' base.
            "RunPeriod_v9_0_to_v9_5",
            "AirLoopHVACOutdoorAirSystem_v8_9_to_v9_5",
            "EvaporativeFluidCoolerSingleSpeed_v8_9_to_v25_1",
            "TableTwoIndependentVariables_v8_9_to_v9_1",
        ],
    )
    def test_a_range_class_keeps_its_name(self, name: str) -> None:
        assert f"class {name}(" in gen.generate_versioned_pyi()

    def test_the_release_class_signature_requires_its_release_fields(self) -> None:
        sink = gen._CreationModules("_v", "_cv")  # pyright: ignore[reportPrivateUsage]
        gen.generate_versioned_pyi(sink)
        class_for, _ = gen._class_assignment()  # pyright: ignore[reportPrivateUsage]
        signature = _signature_of(sink, class_for["InternalMass", (9, 4, 0)])
        assert "zone_or_zonelist_name: str," in signature
        assert "construction_name: str," in signature
        latest_sink = gen._CreationModules()  # pyright: ignore[reportPrivateUsage]
        generate_stubs(sink=latest_sink)
        latest = _signature_of(latest_sink, "InternalMass")
        assert "surface_area: float" in latest
        assert "construction_name: str | None = ..." in latest


class TestExtensibleGroupItems:
    """Every extensible group is taken as a list of dicts typed by the group's item TypedDict."""

    def test_item_name(self) -> None:
        assert gen._group_item_name("BuildingSurfaceDetailedVerticesGroup") == "BuildingSurfaceDetailedVerticesItem"  # pyright: ignore[reportPrivateUsage]
        assert (
            gen._group_item_name("ScheduleWeekCompactDataGroup_v8_9_to_v9_4")  # pyright: ignore[reportPrivateUsage]
            == "ScheduleWeekCompactDataItem_v8_9_to_v9_4"
        )

    def test_group_class_comes_with_its_item_and_a_typed_as_dict(self) -> None:
        sink = gen._CreationModules()  # pyright: ignore[reportPrivateUsage]
        text = "\n".join(_generate_object_class(get_schema(LATEST_VERSION), "BuildingSurface:Detailed", sink=sink))
        assert "class BuildingSurfaceDetailedVerticesItem(TypedDict, total=False):" in text
        assert "    vertex_x_coordinate: float | None" in text
        assert "    def as_dict(self) -> BuildingSurfaceDetailedVerticesItem: ..." in text
        # The update keyword: dicts or groups, in any sequence.
        assert (
            "    vertices: Sequence[BuildingSurfaceDetailedVerticesItem | BuildingSurfaceDetailedVerticesGroup]" in text
        )
        signature = _signature_of(sink, "BuildingSurfaceDetailed")
        assert (
            "vertices: Sequence[_g.BuildingSurfaceDetailedVerticesItem | _g.BuildingSurfaceDetailedVerticesGroup] = ..."
            in signature
        )

    def test_creation_modules_import_the_stub_their_items_live_in(self) -> None:
        sink = gen._CreationModules("_v", "_cv")  # pyright: ignore[reportPrivateUsage]
        gen.generate_versioned_pyi(sink)
        sources = "\n".join(sink.sources().values())
        assert "from .. import versioned as _vd" in sources
        assert "from .. import _generated_types as _g" in sources
        assert "_vd._" not in sources  # private names stay private: items are public
