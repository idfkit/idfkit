"""Tests for schema module: EpJSONSchema and SchemaManager."""

from __future__ import annotations

import gzip
import json
from pathlib import Path
from typing import Any

import pytest

from idfkit.exceptions import SchemaNotFoundError
from idfkit.schema import (  # pyright: ignore[reportPrivateUsage]
    EpJSONSchema,
    SchemaManager,
    _resolve_field_type,
    get_schema,
    get_schema_manager,
    load_schema_json,
)

# ---------------------------------------------------------------------------
# EpJSONSchema
# ---------------------------------------------------------------------------


class TestEpJSONSchema:
    def test_version(self, schema: EpJSONSchema) -> None:
        assert schema.version == (24, 1, 0)

    def test_object_types_not_empty(self, schema: EpJSONSchema) -> None:
        types = schema.object_types
        assert len(types) > 0

    def test_contains_zone(self, schema: EpJSONSchema) -> None:
        assert "Zone" in schema

    def test_contains_missing(self, schema: EpJSONSchema) -> None:
        assert "TotallyFakeObject" not in schema

    def test_len(self, schema: EpJSONSchema) -> None:
        assert len(schema) > 100  # EnergyPlus has hundreds of object types

    def test_get_object_schema(self, schema: EpJSONSchema) -> None:
        zone_schema = schema.get_object_schema("Zone")
        assert zone_schema is not None
        assert isinstance(zone_schema, dict)

    def test_get_object_schema_missing(self, schema: EpJSONSchema) -> None:
        assert schema.get_object_schema("FakeType") is None

    def test_get_inner_schema(self, schema: EpJSONSchema) -> None:
        inner = schema.get_inner_schema("Zone")
        assert inner is not None
        assert "properties" in inner

    def test_get_inner_schema_missing(self, schema: EpJSONSchema) -> None:
        assert schema.get_inner_schema("FakeType") is None

    def test_get_field_schema(self, schema: EpJSONSchema) -> None:
        field = schema.get_field_schema("Zone", "x_origin")
        assert field is not None

    def test_get_field_schema_missing_field(self, schema: EpJSONSchema) -> None:
        field = schema.get_field_schema("Zone", "nonexistent_field")
        assert field is None

    def test_get_field_schema_missing_type(self, schema: EpJSONSchema) -> None:
        assert schema.get_field_schema("FakeType", "x") is None

    def test_get_field_names(self, schema: EpJSONSchema) -> None:
        fields = schema.get_field_names("Zone")
        assert isinstance(fields, list)
        assert len(fields) > 0
        # 'name' should NOT be in the returned list (it's excluded)
        assert "name" not in fields

    def test_get_field_names_missing_type(self, schema: EpJSONSchema) -> None:
        assert schema.get_field_names("FakeType") == []

    def test_get_all_field_names(self, schema: EpJSONSchema) -> None:
        fields = schema.get_all_field_names("Zone")
        assert isinstance(fields, list)
        # Should include 'name' as first entry
        assert "name" in fields

    def test_get_all_field_names_missing_type(self, schema: EpJSONSchema) -> None:
        assert schema.get_all_field_names("FakeType") == []

    def test_get_required_fields(self, schema: EpJSONSchema) -> None:
        required = schema.get_required_fields("Zone")
        assert isinstance(required, list)

    def test_get_required_fields_missing_type(self, schema: EpJSONSchema) -> None:
        assert schema.get_required_fields("FakeType") == []

    def test_get_field_default(self, schema: EpJSONSchema) -> None:
        # Many fields have defaults
        default = schema.get_field_default("Zone", "multiplier")
        # May be None or a value depending on schema
        # Just check it doesn't crash
        assert default is None or isinstance(default, (int, float, str))

    def test_get_field_default_missing(self, schema: EpJSONSchema) -> None:
        assert schema.get_field_default("FakeType", "x") is None

    def test_get_field_type(self, schema: EpJSONSchema) -> None:
        ft = schema.get_field_type("Zone", "x_origin")
        assert ft is not None
        assert ft in ("number", "integer", "string")

    def test_get_field_type_missing(self, schema: EpJSONSchema) -> None:
        assert schema.get_field_type("FakeType", "x") is None

    def test_is_reference_field(self, schema: EpJSONSchema) -> None:
        # Construction's "outside_layer" references a material
        assert schema.is_reference_field("Construction", "outside_layer") is True

    def test_is_not_reference_field(self, schema: EpJSONSchema) -> None:
        # Zone's x_origin is not a reference
        assert schema.is_reference_field("Zone", "x_origin") is False

    def test_get_field_object_list(self, schema: EpJSONSchema) -> None:
        obj_list = schema.get_field_object_list("Construction", "outside_layer")
        assert obj_list is not None
        assert isinstance(obj_list, list)
        assert len(obj_list) > 0

    def test_get_field_object_list_none(self, schema: EpJSONSchema) -> None:
        assert schema.get_field_object_list("Zone", "x_origin") is None

    def test_get_types_providing_reference(self, schema: EpJSONSchema) -> None:
        # There should be some reference lists populated
        # Test that at least one can be queried
        types = schema.get_types_providing_reference("SomeUnknownList")
        assert isinstance(types, list)

    def test_get_group(self, schema: EpJSONSchema) -> None:
        assert schema.get_group("Zone") == "Thermal Zones and Surfaces"

    def test_get_group_hvac_template(self, schema: EpJSONSchema) -> None:
        assert schema.get_group("HVACTemplate:Zone:IdealLoadsAirSystem") == "HVAC Templates"

    def test_get_group_missing(self, schema: EpJSONSchema) -> None:
        assert schema.get_group("FakeType") is None

    def test_get_object_memo(self, schema: EpJSONSchema) -> None:
        memo = schema.get_object_memo("Zone")
        # May be None or a string depending on schema
        assert memo is None or isinstance(memo, str)

    def test_get_object_memo_missing(self, schema: EpJSONSchema) -> None:
        assert schema.get_object_memo("FakeType") is None

    def test_is_extensible(self, schema: EpJSONSchema) -> None:
        # Schedule:Day:Interval is extensible
        assert schema.is_extensible("Schedule:Day:Interval") is True

    def test_is_not_extensible(self, schema: EpJSONSchema) -> None:
        # Zone is not extensible
        assert schema.is_extensible("Zone") is False

    def test_is_extensible_missing(self, schema: EpJSONSchema) -> None:
        assert schema.is_extensible("FakeType") is False

    def test_get_extensible_size(self, schema: EpJSONSchema) -> None:
        size = schema.get_extensible_size("Schedule:Day:Interval")
        assert size is not None
        assert isinstance(size, (int, float))

    def test_get_extensible_size_missing(self, schema: EpJSONSchema) -> None:
        assert schema.get_extensible_size("FakeType") is None


# ---------------------------------------------------------------------------
# Case-insensitive type resolution
# ---------------------------------------------------------------------------


class TestResolveTypeName:
    def test_canonical_name(self, schema: EpJSONSchema) -> None:
        assert schema.resolve_type_name("Zone") == "Zone"

    def test_uppercase(self, schema: EpJSONSchema) -> None:
        assert schema.resolve_type_name("ZONE") == "Zone"

    def test_lowercase(self, schema: EpJSONSchema) -> None:
        assert schema.resolve_type_name("zone") == "Zone"

    def test_mixed_case_with_colon(self, schema: EpJSONSchema) -> None:
        assert schema.resolve_type_name("SCHEDULE:COMPACT") == "Schedule:Compact"

    def test_unknown_type(self, schema: EpJSONSchema) -> None:
        assert schema.resolve_type_name("FakeType") is None

    def test_extensible_field_types_in_parsing_cache(self, schema: EpJSONSchema) -> None:
        """Extensible field types should be resolved from JSON schema, not just legacy_idd."""
        pc = schema.get_parsing_cache("Foundation:Kiva")
        assert pc is not None
        assert pc.field_types.get("custom_block_material_name") == "string"
        assert pc.field_types.get("custom_block_depth") == "number"

    def test_extensible_ref_fields_in_parsing_cache(self, schema: EpJSONSchema) -> None:
        """Extensible reference fields must appear in ref_fields (GH-92)."""
        pc = schema.get_parsing_cache("Foundation:Kiva")
        assert pc is not None
        assert "custom_block_material_name" in pc.ref_fields

    def test_parsing_cache_case_insensitive(self, schema: EpJSONSchema) -> None:
        """get_parsing_cache should resolve miscased type names."""
        pc_canonical = schema.get_parsing_cache("Zone")
        pc_upper = schema.get_parsing_cache("ZONE")
        pc_lower = schema.get_parsing_cache("zone")
        assert pc_canonical is not None
        assert pc_canonical is pc_upper
        assert pc_canonical is pc_lower


# ---------------------------------------------------------------------------
# SchemaManager
# ---------------------------------------------------------------------------


class TestSchemaManager:
    def test_get_schema(self) -> None:
        manager = SchemaManager()
        schema = manager.get_schema((24, 1, 0))
        assert schema is not None
        assert schema.version == (24, 1, 0)

    def test_get_schema_cached(self) -> None:
        manager = SchemaManager()
        s1 = manager.get_schema((24, 1, 0))
        s2 = manager.get_schema((24, 1, 0))
        assert s1 is s2

    def test_get_schema_not_found(self) -> None:
        manager = SchemaManager()
        with pytest.raises(SchemaNotFoundError):
            manager.get_schema((1, 0, 0))

    def test_get_available_versions(self) -> None:
        manager = SchemaManager()
        versions = manager.get_available_versions()
        assert isinstance(versions, list)
        assert (24, 1, 0) in versions

    def test_clear_cache(self) -> None:
        manager = SchemaManager()
        _ = manager.get_schema((24, 1, 0))
        manager.clear_cache()
        # Should still work after clearing
        schema = manager.get_schema((24, 1, 0))
        assert schema is not None

    def test_available_versions_sorted(self) -> None:
        manager = SchemaManager()
        versions = manager.get_available_versions()
        assert versions == sorted(versions)


# ---------------------------------------------------------------------------
# Module-level functions
# ---------------------------------------------------------------------------


class TestModuleFunctions:
    def test_get_schema_manager(self) -> None:
        manager = get_schema_manager()
        assert isinstance(manager, SchemaManager)
        # Should return same instance
        assert get_schema_manager() is manager

    def test_get_schema(self) -> None:
        schema = get_schema((24, 1, 0))
        assert isinstance(schema, EpJSONSchema)
        assert schema.version == (24, 1, 0)


# ---------------------------------------------------------------------------
# _resolve_field_type helper
# ---------------------------------------------------------------------------


class TestResolveFieldTypeHelper:
    def test_field_not_in_props_not_in_field_info(self) -> None:
        result = _resolve_field_type("missing", {}, {})
        assert result is None

    def test_field_in_field_info_type_n(self) -> None:
        result = _resolve_field_type("myfield", {}, {"myfield": {"field_type": "n"}})
        assert result == "number"

    def test_field_in_field_info_type_a(self) -> None:
        result = _resolve_field_type("myfield", {}, {"myfield": {"field_type": "a"}})
        assert result == "string"

    def test_field_in_props_anyof_no_numeric(self) -> None:
        props: dict[str, Any] = {"myfield": {"anyOf": [{"type": "string"}, {"enum": ["Auto"]}]}}
        result = _resolve_field_type("myfield", props, {})
        assert result == "string"


# ---------------------------------------------------------------------------
# EpJSONSchema edge cases
# ---------------------------------------------------------------------------


class TestEpJSONSchemaEdgeCases:
    def test_get_inner_schema_returns_none_for_empty_pattern_props(self) -> None:
        schema = EpJSONSchema((24, 1, 0), {"properties": {"EmptyType": {"patternProperties": {}}}})
        assert schema.get_inner_schema("EmptyType") is None

    def test_has_name_returns_true_for_unknown_type(self, schema: EpJSONSchema) -> None:
        # Default backward-compat: assume named
        assert schema.has_name("FakeTypeXYZ") is True

    def test_get_extensible_field_names_missing_type(self, schema: EpJSONSchema) -> None:
        result = schema.get_extensible_field_names("FakeTypeXYZ")
        assert result == []

    def test_get_extensible_field_names_valid_type(self, schema: EpJSONSchema) -> None:
        result = schema.get_extensible_field_names("BuildingSurface:Detailed")
        assert len(result) > 0
        assert "vertex_x_coordinate" in result

    def test_get_field_type_extensible_field_via_legacy_fallback(self, schema: EpJSONSchema) -> None:
        # 'time' and 'value_until_time' are extensible in Schedule:Day:Interval
        # They are NOT in patternProperties.props but ARE in legacy_idd.field_info
        ft_time = schema.get_field_type("Schedule:Day:Interval", "time")
        assert ft_time == "string"

        ft_value = schema.get_field_type("Schedule:Day:Interval", "value_until_time")
        assert ft_value == "number"

    def test_get_field_type_anyof_string_only(self) -> None:
        schema = EpJSONSchema(
            (24, 1, 0),
            {
                "properties": {
                    "FakeObj": {
                        "patternProperties": {
                            ".*": {
                                "properties": {"myfield": {"anyOf": [{"type": "string"}, {"enum": ["Autocalculate"]}]}}
                            }
                        }
                    }
                }
            },
        )
        result = schema.get_field_type("FakeObj", "myfield")
        assert result == "string"

    def test_get_parsing_cache_canonical_already_cached(self, schema: EpJSONSchema) -> None:
        # Pre-populate canonical cache then delete non-canonical entry
        pc_canonical = schema.get_parsing_cache("Zone")
        assert pc_canonical is not None
        # Remove the ZONE entry (if present) to force canonical-already-cached path
        schema._parsing_cache.pop("ZONE", None)  # pyright: ignore[reportPrivateUsage]
        pc_upper = schema.get_parsing_cache("ZONE")
        assert pc_upper is pc_canonical


# ---------------------------------------------------------------------------
# load_schema_json
# ---------------------------------------------------------------------------


class TestLoadSchemaJson:
    def test_load_plain_json(self, tmp_path: Path) -> None:
        path = tmp_path / "schema.json"
        path.write_text(json.dumps({"key": "value"}))
        result = load_schema_json(path)
        assert result == {"key": "value"}

    def test_load_gzipped_json(self, tmp_path: Path) -> None:
        data = {"key": "gzipped"}
        path = tmp_path / "schema.json.gz"
        with gzip.open(path, "wt", encoding="utf-8") as gz:
            json.dump(data, gz)
        result = load_schema_json(path)
        assert result == data


# ---------------------------------------------------------------------------
# SchemaManager additional tests
# ---------------------------------------------------------------------------


class TestSchemaManagerAdditional:
    def test_bundled_dir_property(self) -> None:
        manager = SchemaManager()
        assert isinstance(manager.bundled_dir, Path)

    def test_cache_dir_property(self) -> None:
        manager = SchemaManager()
        assert isinstance(manager.cache_dir, Path)

    def test_custom_bundled_and_cache_dirs(self, tmp_path: Path) -> None:
        bundled = tmp_path / "bundled"
        cache = tmp_path / "cache"
        manager = SchemaManager(bundled_schema_dir=bundled, cache_dir=cache)
        assert manager.bundled_dir == bundled
        assert manager.cache_dir == cache

    def test_get_schema_dict_cache_hit(self) -> None:
        manager = SchemaManager()
        s1 = manager.get_schema((24, 1, 0))
        # Clear the lru_cache but keep _cache — should return same object
        manager.get_schema.cache_clear()
        s2 = manager.get_schema((24, 1, 0))
        assert s1 is s2

    def test_get_schema_fallback_to_closest_version(self) -> None:
        # A patch version that doesn't exist but has a close match
        manager = SchemaManager()
        schema = manager.get_schema((24, 1, 99))
        assert schema.version == (24, 1, 99)

    def test_find_schema_from_cache_dir(self, tmp_path: Path) -> None:
        cache_dir = tmp_path / "cache"
        version_dir = cache_dir / "V24-1-0"
        version_dir.mkdir(parents=True)
        # Write a minimal plain schema file
        schema_file = version_dir / "Energy+.schema.epJSON"
        schema_file.write_text(json.dumps({"properties": {"Zone": {}}}))

        manager = SchemaManager(bundled_schema_dir=tmp_path / "nonexistent", cache_dir=cache_dir)
        found = manager._find_schema_file((24, 1, 0))  # pyright: ignore[reportPrivateUsage]
        assert found == schema_file

    def test_get_available_versions_with_user_cache(self, tmp_path: Path) -> None:
        cache_dir = tmp_path / "cache"
        version_dir = cache_dir / "V99-0-0"
        version_dir.mkdir(parents=True)
        (version_dir / "Energy+.schema.epJSON").write_text("{}")

        # Non-version dir should be skipped
        (cache_dir / "noversion").mkdir()

        manager = SchemaManager(cache_dir=cache_dir)
        versions = manager.get_available_versions()
        assert (99, 0, 0) in versions

    def test_get_available_versions_user_cache_dir_missing(self, tmp_path: Path) -> None:
        manager = SchemaManager(cache_dir=tmp_path / "nonexistent")
        # Should not raise, just skip the missing cache dir
        versions = manager.get_available_versions()
        assert isinstance(versions, list)

    def test_parse_version_from_dirname_no_match(self) -> None:
        result = SchemaManager._parse_version_from_dirname("noversion")
        assert result is None

    def test_parse_version_from_dirname_no_patch(self) -> None:
        result = SchemaManager._parse_version_from_dirname("EnergyPlus-24-2")
        assert result is not None
        assert result[0] == 24
        assert result[1] == 2
        assert result[2] == 0

    def test_get_supported_versions(self) -> None:
        manager = SchemaManager()
        supported = manager.get_supported_versions()
        assert isinstance(supported, list)
        assert len(supported) > 10
        assert (24, 1, 0) in supported

    def test_get_available_versions_user_cache_version_without_schema(self, tmp_path: Path) -> None:
        cache_dir = tmp_path / "cache"
        # Dir with parseable version name but no schema file
        (cache_dir / "V99-0-0").mkdir(parents=True)
        manager = SchemaManager(cache_dir=cache_dir)
        versions = manager.get_available_versions()
        assert (99, 0, 0) not in versions

    def test_get_available_versions_user_cache_unparseable_dir(self, tmp_path: Path) -> None:
        cache_dir = tmp_path / "cache"
        # Dir whose name can't be parsed as a version -> should be ignored
        (cache_dir / "noversion").mkdir(parents=True)
        manager = SchemaManager(cache_dir=cache_dir)
        versions = manager.get_available_versions()
        assert isinstance(versions, list)

    def test_find_schema_from_install_path(self, tmp_path: Path) -> None:
        # Simulate an EnergyPlus installation directory containing a schema file
        install_base = tmp_path / "Applications" / "EnergyPlus-24-1-0"
        install_base.mkdir(parents=True)
        schema_file = install_base / "Energy+.schema.epJSON"
        schema_file.write_text(json.dumps({"properties": {"Zone": {}}}))

        # Use a custom bundled dir (no schemas) so install path is reached
        manager = SchemaManager(
            bundled_schema_dir=tmp_path / "no_bundled",
            cache_dir=tmp_path / "no_cache",
        )
        # Patch the install paths to use our tmp dir
        old_paths = manager._INSTALL_PATHS.copy()
        manager._INSTALL_PATHS["darwin"] = [str(tmp_path / "Applications" / "EnergyPlus-{v}")]
        manager._INSTALL_PATHS["linux"] = [str(tmp_path / "Applications" / "EnergyPlus-{v}")]
        manager._INSTALL_PATHS["win32"] = [str(tmp_path / "Applications" / "EnergyPlus-{v}")]
        try:
            found = manager._find_schema_file((24, 1, 0))  # pyright: ignore[reportPrivateUsage]
            assert found == schema_file
        finally:
            manager._INSTALL_PATHS.clear()
            manager._INSTALL_PATHS.update(old_paths)


class TestGetFieldTypeEdgeCases:
    """Test get_field_type legacy fallback edge cases."""

    def test_field_in_field_info_unknown_type(self) -> None:
        schema = EpJSONSchema(
            (24, 1, 0),
            {
                "properties": {
                    "MyType": {
                        "legacy_idd": {
                            "fields": ["name"],
                            "field_info": {"myfield": {"field_type": "x"}},  # unknown -> None
                        }
                    }
                }
            },
        )
        result = schema.get_field_type("MyType", "myfield")
        assert result is None

    def test_anyof_with_integer_type(self) -> None:
        schema = EpJSONSchema(
            (24, 1, 0),
            {
                "properties": {
                    "MyType": {
                        "patternProperties": {
                            ".*": {"properties": {"myfield": {"anyOf": [{"type": "integer"}, {"type": "string"}]}}}
                        }
                    }
                }
            },
        )
        result = schema.get_field_type("MyType", "myfield")
        assert result == "integer"

    def test_field_not_in_field_info_either(self) -> None:
        # Field that's not in patternProperties and not in field_info -> None
        schema = EpJSONSchema(
            (24, 1, 0),
            {
                "properties": {
                    "MyType": {"legacy_idd": {"fields": ["name"], "field_info": {"other": {"field_type": "n"}}}}
                }
            },
        )
        result = schema.get_field_type("MyType", "missing_field")
        assert result is None


class TestParsingCacheEdgeCases:
    """Test _build_parsing_cache edge cases."""

    def test_array_without_items_builds_cache(self) -> None:
        schema = EpJSONSchema(
            (24, 1, 0),
            {"properties": {"MyType": {"patternProperties": {".*": {"properties": {"myarray": {"type": "array"}}}}}}},
        )
        pc = schema.get_parsing_cache("MyType")
        assert pc is not None

    def test_canonical_already_cached_path(self, schema: EpJSONSchema) -> None:
        # Ensure canonical is cached first
        pc_canonical = schema.get_parsing_cache("Zone")
        assert pc_canonical is not None
        # Remove the non-canonical entry
        schema._parsing_cache.pop("ZONE", None)  # pyright: ignore[reportPrivateUsage]
        # Now requesting ZONE: canonical cached, non-canonical not -> line 323 path
        pc_upper = schema.get_parsing_cache("ZONE")
        assert pc_upper is pc_canonical

    def test_build_parsing_cache_extensible_ref_field_in_ext_props(self, schema: EpJSONSchema) -> None:
        """Extensible fields with object_list in ext_props add to ref_fields."""
        pc = schema.get_parsing_cache("Foundation:Kiva")
        assert pc is not None
        # custom_block_material_name should be in ref_fields (comes from ext_props)
        assert "custom_block_material_name" in pc.ref_fields

    def test_resolve_field_type_field_info_field_not_found(self) -> None:
        """_resolve_field_type returns None when field not in field_info."""
        result = _resolve_field_type("missing", {}, {"other_field": {"field_type": "n"}})
        assert result is None

    def test_resolve_field_type_field_info_unknown_type_goes_to_none(self) -> None:
        """_resolve_field_type line 63->65: ft is not 'a', returns None."""
        result = _resolve_field_type("myfield", {}, {"myfield": {"field_type": "x"}})
        assert result is None

    def test_build_parsing_cache_items_dict_but_no_properties(self) -> None:
        """Line 358->353: _items is a dict but _ep is not a dict."""
        schema = EpJSONSchema(
            (24, 1, 0),
            {
                "properties": {
                    "MyType": {
                        "patternProperties": {
                            ".*": {"properties": {"myarray": {"type": "array", "items": {"no_properties_key": True}}}}
                        }
                    }
                }
            },
        )
        pc = schema.get_parsing_cache("MyType")
        assert pc is not None

    def test_build_parsing_cache_ext_fname_already_in_field_types(self) -> None:
        """Line 380->382: ext_fname already in field_types, skip re-resolve."""
        schema = EpJSONSchema(
            (24, 1, 0),
            {
                "properties": {
                    "ExtType": {
                        "extensible_size": 1,
                        "legacy_idd": {
                            "fields": ["name", "myfield"],
                            "extensibles": ["myfield"],
                            "field_info": {},
                        },
                        "patternProperties": {".*": {"properties": {"myfield": {"type": "number"}}}},
                    }
                }
            },
        )
        pc = schema.get_parsing_cache("ExtType")
        assert pc is not None
        assert pc.field_types.get("myfield") == "number"

    def test_get_field_object_list_no_field_schema(self, schema: EpJSONSchema) -> None:
        """Line 292: get_field_object_list returns None when no field schema."""
        result = schema.get_field_object_list("Zone", "nonexistent_field")
        assert result is None


class TestGetAvailableVersionsEdgeCases:
    """Additional edge cases for get_available_versions."""

    def test_cache_dir_has_files_not_dirs(self, tmp_path: Path) -> None:
        cache_dir = tmp_path / "cache"
        cache_dir.mkdir()
        # Put files (not dirs) in cache_dir — they should be skipped (727->726)
        (cache_dir / "somefile.txt").write_text("hello")

        manager = SchemaManager(cache_dir=cache_dir)
        versions = manager.get_available_versions()
        assert isinstance(versions, list)

    def test_bundled_dir_version_without_schema(self, tmp_path: Path) -> None:
        bundled_dir = tmp_path / "bundled"
        # Dir with parseable version but no schema file (721->718 False branch)
        (bundled_dir / "V99-0-0").mkdir(parents=True)

        manager = SchemaManager(bundled_schema_dir=bundled_dir, cache_dir=tmp_path / "no_cache")
        versions = manager.get_available_versions()
        assert (99, 0, 0) not in versions

    def test_install_dir_energyplus_no_version_parseable(self, tmp_path: Path) -> None:
        install_base = tmp_path / "ep"
        install_base.mkdir()
        # A file (not a dir) — hits the 743->742 False branch
        (install_base / "EnergyPlus-98-0-0.txt").write_text("file")
        # Dir with 'EnergyPlus' in name but no parseable version (743 True, version None)
        (install_base / "EnergyPlus-invalid").mkdir()
        # Dir with parseable version but no schema (745 True, 747 False -> loop back)
        (install_base / "EnergyPlus-99-0-0").mkdir()

        manager = SchemaManager(
            bundled_schema_dir=tmp_path / "none",
            cache_dir=tmp_path / "cache",
        )
        old_paths = dict(manager._INSTALL_PATHS)
        install_pattern = str(install_base / "{v}")
        manager._INSTALL_PATHS["darwin"] = [install_pattern]
        manager._INSTALL_PATHS["linux"] = [install_pattern]
        manager._INSTALL_PATHS["win32"] = [install_pattern]
        try:
            versions = manager.get_available_versions()
            assert (99, 0, 0) not in versions
        finally:
            manager._INSTALL_PATHS.clear()
            manager._INSTALL_PATHS.update(old_paths)


class TestGetAvailableVersionsInstallPath:
    """Test get_available_versions for installed EnergyPlus directories."""

    def test_installed_energyplus_dir_with_schema(self, tmp_path: Path) -> None:
        # Simulate an installed EnergyPlus directory structure.
        # The pattern is "parent/{v}" where parent is an existing directory.
        # get_available_versions splits on "{v}" to find the parent.
        install_base = tmp_path / "ep"
        ep_dir = install_base / "EnergyPlus-24-1-0"
        ep_dir.mkdir(parents=True)
        schema_file = ep_dir / "Energy+.schema.epJSON"
        schema_file.write_text(json.dumps({"properties": {}}))

        manager = SchemaManager(
            bundled_schema_dir=tmp_path / "no_bundled",
            cache_dir=tmp_path / "no_cache",
        )
        # Patch install paths — use pattern where parent directory exists
        old_paths = dict(manager._INSTALL_PATHS)
        install_pattern = str(install_base / "{v}")
        manager._INSTALL_PATHS["darwin"] = [install_pattern]
        manager._INSTALL_PATHS["linux"] = [install_pattern]
        manager._INSTALL_PATHS["win32"] = [install_pattern]
        try:
            versions = manager.get_available_versions()
            assert (24, 1, 0) in versions
        finally:
            manager._INSTALL_PATHS.clear()
            manager._INSTALL_PATHS.update(old_paths)
