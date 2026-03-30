"""Unit tests for idfkit.compat._diff (schema indexing and diffing)."""

from __future__ import annotations

import pytest

from idfkit.compat._diff import SchemaDiff, SchemaIndex, build_schema_index, diff_schemas
from idfkit.schema import get_schema


@pytest.fixture
def index_24_1() -> SchemaIndex:
    """Schema index for v24.1.0."""
    return build_schema_index(get_schema((24, 1, 0)))


@pytest.fixture
def index_24_2() -> SchemaIndex:
    """Schema index for v24.2.0."""
    return build_schema_index(get_schema((24, 2, 0)))


class TestBuildSchemaIndex:
    """Tests for build_schema_index."""

    def test_object_types_populated(self, index_24_1: SchemaIndex) -> None:
        assert len(index_24_1.object_types) > 100
        assert "Zone" in index_24_1.object_types
        assert "Material" in index_24_1.object_types
        assert "Construction" in index_24_1.object_types

    def test_version_stored(self, index_24_1: SchemaIndex) -> None:
        assert index_24_1.version == (24, 1, 0)

    def test_choices_populated(self, index_24_1: SchemaIndex) -> None:
        # Material.roughness should have enum choices
        key = ("Material", "roughness")
        assert key in index_24_1.choices
        roughness_choices = index_24_1.choices[key]
        assert "MediumSmooth" in roughness_choices
        assert "Smooth" in roughness_choices
        assert "VerySmooth" in roughness_choices

    def test_non_enum_field_not_in_choices(self, index_24_1: SchemaIndex) -> None:
        # Material.thickness is a number, not an enum
        key = ("Material", "thickness")
        assert key not in index_24_1.choices

    def test_frozen_types(self, index_24_1: SchemaIndex) -> None:
        assert isinstance(index_24_1.object_types, frozenset)
        for choices in index_24_1.choices.values():
            assert isinstance(choices, frozenset)

    def test_two_versions_have_different_counts(self, index_24_1: SchemaIndex, index_24_2: SchemaIndex) -> None:
        # Versions should have slightly different object type counts
        # (this verifies they are independently loaded)
        assert index_24_1.version != index_24_2.version

    def test_groups_populated(self, index_24_1: SchemaIndex) -> None:
        assert "Zone" in index_24_1.groups
        assert index_24_1.groups["Zone"] == "Thermal Zones and Surfaces"
        assert "Material" in index_24_1.groups
        assert index_24_1.groups["Material"] == "Surface Construction Elements"

    def test_groups_cover_all_types(self, index_24_1: SchemaIndex) -> None:
        # Every object type should have a group mapping
        for obj_type in index_24_1.object_types:
            assert obj_type in index_24_1.groups, f"{obj_type} missing from groups"


class TestDiffSchemas:
    """Tests for diff_schemas."""

    def test_diff_same_version_is_empty(self, index_24_1: SchemaIndex) -> None:
        diff = diff_schemas(index_24_1, index_24_1)
        assert len(diff.removed_types) == 0
        assert len(diff.added_types) == 0
        assert len(diff.removed_choices) == 0
        assert len(diff.added_choices) == 0

    def test_diff_versions_stored(self, index_24_1: SchemaIndex, index_24_2: SchemaIndex) -> None:
        diff = diff_schemas(index_24_1, index_24_2)
        assert diff.from_version == (24, 1, 0)
        assert diff.to_version == (24, 2, 0)

    def test_diff_returns_schema_diff_type(self, index_24_1: SchemaIndex, index_24_2: SchemaIndex) -> None:
        diff = diff_schemas(index_24_1, index_24_2)
        assert isinstance(diff, SchemaDiff)
        assert isinstance(diff.removed_types, frozenset)
        assert isinstance(diff.added_types, frozenset)

    def test_synthetic_removed_type(self) -> None:
        """Test diffing with a synthetic index that has a removed type."""
        idx_a = SchemaIndex(
            version=(1, 0, 0),
            object_types=frozenset({"Zone", "Material", "OldType"}),
            choices={},
        )
        idx_b = SchemaIndex(
            version=(2, 0, 0),
            object_types=frozenset({"Zone", "Material", "NewType"}),
            choices={},
        )
        diff = diff_schemas(idx_a, idx_b)
        assert "OldType" in diff.removed_types
        assert "NewType" in diff.added_types
        assert "Zone" not in diff.removed_types
        assert "Zone" not in diff.added_types

    def test_synthetic_choice_diff(self) -> None:
        """Test diffing with synthetic choice changes."""
        idx_a = SchemaIndex(
            version=(1, 0, 0),
            object_types=frozenset({"Material"}),
            choices={("Material", "roughness"): frozenset({"Smooth", "MediumSmooth", "OldChoice"})},
        )
        idx_b = SchemaIndex(
            version=(2, 0, 0),
            object_types=frozenset({"Material"}),
            choices={("Material", "roughness"): frozenset({"Smooth", "MediumSmooth", "NewChoice"})},
        )
        diff = diff_schemas(idx_a, idx_b)
        assert ("Material", "roughness") in diff.removed_choices
        assert "OldChoice" in diff.removed_choices[("Material", "roughness")]
        assert ("Material", "roughness") in diff.added_choices
        assert "NewChoice" in diff.added_choices[("Material", "roughness")]

    def test_diff_across_major_versions(self) -> None:
        """Test diffing between substantially different versions (8.9 vs 25.2)."""
        idx_old = build_schema_index(get_schema((8, 9, 0)))
        idx_new = build_schema_index(get_schema((25, 2, 0)))
        diff = diff_schemas(idx_old, idx_new)
        # There should be some types added in newer versions
        assert len(diff.added_types) > 0
        # Both should still have Zone
        assert "Zone" not in diff.removed_types
        assert "Zone" not in diff.added_types


# ---------------------------------------------------------------------------
# Additional tests for uncovered branches in _diff.py
# ---------------------------------------------------------------------------


class TestExtractEnumValues:
    """Tests for _extract_enum_values edge cases."""

    def test_non_string_enum_value_ignored(self) -> None:
        """Non-string values in an ``enum`` array are silently skipped."""
        from idfkit.compat._diff import _extract_enum_values  # pyright: ignore[reportPrivateUsage]

        result = _extract_enum_values({"enum": [1, 2, "ValidString", None]})
        assert result == {"ValidString"}

    def test_anyof_with_non_string_values(self) -> None:
        """Non-string values in anyOf enum branches are silently skipped."""
        from idfkit.compat._diff import _extract_enum_values  # pyright: ignore[reportPrivateUsage]

        field_schema = {"anyOf": [{"enum": [1, "Choice1"]}, {"enum": ["Choice2", 3.14]}]}
        result = _extract_enum_values(field_schema)
        assert result == {"Choice1", "Choice2"}


class TestBuildSchemaIndexEdgeCases:
    """Edge-case tests for build_schema_index."""

    def test_object_type_with_none_inner_schema(self) -> None:
        """Object types whose inner schema is None are added to object_types but skipped for choices."""
        from unittest.mock import MagicMock

        from idfkit.compat._diff import build_schema_index  # pyright: ignore[reportPrivateUsage]

        mock_schema = MagicMock()
        mock_schema.version = (24, 1, 0)
        mock_schema.object_types = ["Zone", "FakeType"]
        mock_schema.get_group.return_value = "Some Group"
        # FakeType returns None inner schema
        mock_schema.get_inner_schema.side_effect = lambda t: None if t == "FakeType" else {"properties": {}}  # pyright: ignore[reportUnknownLambdaType]

        index = build_schema_index(mock_schema)
        assert "Zone" in index.object_types
        assert "FakeType" in index.object_types
        # No choices since neither has enum fields
        assert len(index.choices) == 0

    def test_field_with_non_dict_value_skipped(self) -> None:
        """A properties entry that is not a dict is skipped without error."""
        from unittest.mock import MagicMock

        from idfkit.compat._diff import build_schema_index  # pyright: ignore[reportPrivateUsage]

        mock_schema = MagicMock()
        mock_schema.version = (24, 1, 0)
        mock_schema.object_types = ["Zone"]
        mock_schema.get_group.return_value = "Thermal Zones and Surfaces"
        # properties contains a non-dict value for one field
        mock_schema.get_inner_schema.return_value = {"properties": {"name": "not-a-dict", "area": {"type": "number"}}}

        index = build_schema_index(mock_schema)
        assert "Zone" in index.object_types
        # "not-a-dict" string field should be skipped; "area" has no enum, so no choices
        assert len(index.choices) == 0

    def test_object_type_with_no_group(self) -> None:
        """Object types where get_group returns None are added without a group mapping."""
        from unittest.mock import MagicMock

        from idfkit.compat._diff import build_schema_index  # pyright: ignore[reportPrivateUsage]

        mock_schema = MagicMock()
        mock_schema.version = (24, 1, 0)
        mock_schema.object_types = ["UngroupedType"]
        mock_schema.get_group.return_value = None
        mock_schema.get_inner_schema.return_value = {"properties": {}}

        index = build_schema_index(mock_schema)
        assert "UngroupedType" in index.object_types
        assert "UngroupedType" not in index.groups
