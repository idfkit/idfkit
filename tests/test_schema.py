"""Tests for schema module: EpJSONSchema and SchemaManager."""

from __future__ import annotations

import pytest

from idfkit.exceptions import SchemaNotFoundError
from idfkit.schema import EpJSONSchema, SchemaManager, get_schema, get_schema_manager

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
            manager.get_schema((99, 99, 99))

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
