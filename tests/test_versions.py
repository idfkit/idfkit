"""Tests for EnergyPlus version registry and schema loading."""

from __future__ import annotations

import gzip
import json
import tempfile
from pathlib import Path
from typing import Any

from idfkit.exceptions import SchemaNotFoundError
from idfkit.schema import EpJSONSchema, SchemaManager, load_schema_json
from idfkit.versions import (
    ENERGYPLUS_VERSIONS,
    LATEST_VERSION,
    MINIMUM_VERSION,
    find_closest_version,
    github_release_tag,
    is_supported_version,
    version_dirname,
    version_string,
)


class TestVersionRegistry:
    """Tests for the version registry module."""

    def test_versions_tuple_is_sorted(self) -> None:
        """Versions should be in ascending order."""
        for i in range(len(ENERGYPLUS_VERSIONS) - 1):
            assert ENERGYPLUS_VERSIONS[i] < ENERGYPLUS_VERSIONS[i + 1]

    def test_minimum_version_is_8_9(self) -> None:
        """The minimum supported version should be 8.9.0."""
        assert MINIMUM_VERSION == (8, 9, 0)

    def test_latest_version_is_last(self) -> None:
        """LATEST_VERSION should be the last in the tuple."""
        assert ENERGYPLUS_VERSIONS[-1] == LATEST_VERSION

    def test_all_versions_have_three_parts(self) -> None:
        """All version tuples should have exactly 3 parts."""
        for v in ENERGYPLUS_VERSIONS:
            assert len(v) == 3

    def test_known_versions_present(self) -> None:
        """Check that known versions are in the registry."""
        known = [(8, 9, 0), (9, 0, 1), (9, 6, 0), (22, 1, 0), (24, 1, 0)]
        for v in known:
            assert v in ENERGYPLUS_VERSIONS

    def test_is_supported_version(self) -> None:
        assert is_supported_version((24, 1, 0))
        assert is_supported_version((8, 9, 0))
        assert not is_supported_version((7, 0, 0))
        assert not is_supported_version((99, 0, 0))

    def test_version_string(self) -> None:
        assert version_string((24, 1, 0)) == "24.1.0"
        assert version_string((8, 9, 0)) == "8.9.0"

    def test_version_dirname(self) -> None:
        assert version_dirname((24, 1, 0)) == "V24-1-0"
        assert version_dirname((8, 9, 0)) == "V8-9-0"
        assert version_dirname((9, 0, 1)) == "V9-0-1"

    def test_github_release_tag(self) -> None:
        assert github_release_tag((24, 1, 0)) == "v24.1.0"
        assert github_release_tag((8, 9, 0)) == "v8.9.0"


class TestFindClosestVersion:
    """Tests for find_closest_version."""

    def test_exact_match(self) -> None:
        assert find_closest_version((24, 1, 0)) == (24, 1, 0)

    def test_patch_fallback(self) -> None:
        """Version 9.0.0 should fall back to 8.9.0 (9.0.1 is in the registry)."""
        result = find_closest_version((9, 0, 0))
        assert result == (8, 9, 0)

    def test_too_old(self) -> None:
        """Version older than minimum should return None."""
        assert find_closest_version((7, 0, 0)) is None

    def test_future_version(self) -> None:
        """Version beyond latest should return latest."""
        result = find_closest_version((99, 0, 0))
        assert result == LATEST_VERSION

    def test_between_versions(self) -> None:
        """Version between supported versions should fall back to lower."""
        result = find_closest_version((10, 0, 0))
        assert result == (9, 6, 0)


class TestCompressedSchemaLoading:
    """Tests for loading compressed schema files."""

    def test_load_gzipped_schema(self) -> None:
        """Should load a gzip-compressed schema file."""
        schema_data: dict[str, Any] = {"properties": {"Zone": {"patternProperties": {}}}}

        with tempfile.NamedTemporaryFile(suffix=".epJSON.gz", delete=False) as f:
            with gzip.open(f, "wt", encoding="utf-8") as gz:
                json.dump(schema_data, gz)
            tmp_path = Path(f.name)

        try:
            loaded = load_schema_json(tmp_path)
            assert loaded == schema_data
        finally:
            tmp_path.unlink()

    def test_load_plain_schema(self) -> None:
        """Should load a plain (uncompressed) schema file."""
        schema_data: dict[str, Any] = {"properties": {"Zone": {"patternProperties": {}}}}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".epJSON", delete=False) as f:
            json.dump(schema_data, f)
            tmp_path = Path(f.name)

        try:
            loaded = load_schema_json(tmp_path)
            assert loaded == schema_data
        finally:
            tmp_path.unlink()


class TestSchemaManager:
    """Tests for SchemaManager with version support."""

    def _create_test_schema(self, directory: Path, version: tuple[int, int, int], compressed: bool = True) -> None:
        """Create a minimal test schema file."""
        dirname = version_dirname(version)
        schema_dir = directory / dirname
        schema_dir.mkdir(parents=True, exist_ok=True)

        schema_data: dict[str, Any] = {
            "properties": {
                "Version": {
                    "patternProperties": {".*": {"type": "object", "properties": {}}},
                    "legacy_idd": {"fields": ["version_identifier"]},
                },
                "Zone": {
                    "patternProperties": {
                        ".*": {
                            "type": "object",
                            "properties": {
                                "direction_of_relative_north": {"type": "number"},
                                "x_origin": {"type": "number"},
                                "y_origin": {"type": "number"},
                                "z_origin": {"type": "number"},
                            },
                        }
                    },
                    "name": {"reference": ["ZoneNames"]},
                    "legacy_idd": {
                        "fields": ["name", "direction_of_relative_north", "x_origin", "y_origin", "z_origin"]
                    },
                },
            }
        }

        if compressed:
            with gzip.open(schema_dir / "Energy+.schema.epJSON.gz", "wt", encoding="utf-8") as f:
                json.dump(schema_data, f)
        else:
            with open(schema_dir / "Energy+.schema.epJSON", "w") as f:
                json.dump(schema_data, f)

    def test_load_compressed_bundled_schema(self) -> None:
        """Should find and load a compressed bundled schema."""
        with tempfile.TemporaryDirectory() as tmpdir:
            bundled = Path(tmpdir) / "bundled"
            self._create_test_schema(bundled, (9, 2, 0), compressed=True)

            manager = SchemaManager(bundled_schema_dir=bundled, cache_dir=Path(tmpdir) / "cache")
            schema = manager.get_schema((9, 2, 0))

            assert isinstance(schema, EpJSONSchema)
            assert schema.version == (9, 2, 0)
            assert "Zone" in schema

    def test_load_plain_bundled_schema(self) -> None:
        """Should find and load a plain bundled schema."""
        with tempfile.TemporaryDirectory() as tmpdir:
            bundled = Path(tmpdir) / "bundled"
            self._create_test_schema(bundled, (9, 2, 0), compressed=False)

            manager = SchemaManager(bundled_schema_dir=bundled, cache_dir=Path(tmpdir) / "cache")
            schema = manager.get_schema((9, 2, 0))

            assert isinstance(schema, EpJSONSchema)
            assert "Zone" in schema

    def test_load_from_cache_dir(self) -> None:
        """Should find schema in user cache directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = Path(tmpdir) / "cache"
            self._create_test_schema(cache, (9, 3, 0), compressed=True)

            manager = SchemaManager(
                bundled_schema_dir=Path(tmpdir) / "empty_bundled",
                cache_dir=cache,
            )
            schema = manager.get_schema((9, 3, 0))

            assert isinstance(schema, EpJSONSchema)
            assert schema.version == (9, 3, 0)

    def test_closest_version_fallback(self) -> None:
        """Should fall back to closest supported version when exact not found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            bundled = Path(tmpdir) / "bundled"
            # Create schema for 9.2.0
            self._create_test_schema(bundled, (9, 2, 0), compressed=True)

            manager = SchemaManager(bundled_schema_dir=bundled, cache_dir=Path(tmpdir) / "cache")
            # Request 9.2.5 (not exact), should fall back to 9.2.0
            schema = manager.get_schema((9, 2, 5))

            assert isinstance(schema, EpJSONSchema)
            # Version is what was requested
            assert schema.version == (9, 2, 5)

    def test_get_available_versions(self) -> None:
        """Should list available versions from both bundled and cache."""
        with tempfile.TemporaryDirectory() as tmpdir:
            bundled = Path(tmpdir) / "bundled"
            cache = Path(tmpdir) / "cache"

            self._create_test_schema(bundled, (9, 2, 0))
            self._create_test_schema(bundled, (24, 1, 0))
            self._create_test_schema(cache, (9, 3, 0))

            manager = SchemaManager(bundled_schema_dir=bundled, cache_dir=cache)
            versions = manager.get_available_versions()

            assert (9, 2, 0) in versions
            assert (9, 3, 0) in versions
            assert (24, 1, 0) in versions

    def test_get_supported_versions(self) -> None:
        """Should return all versions in the registry."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SchemaManager(
                bundled_schema_dir=Path(tmpdir) / "bundled",
                cache_dir=Path(tmpdir) / "cache",
            )
            supported = manager.get_supported_versions()
            assert supported == list(ENERGYPLUS_VERSIONS)

    def test_prefers_compressed_over_plain(self) -> None:
        """When both compressed and plain exist, compressed should be used."""
        with tempfile.TemporaryDirectory() as tmpdir:
            bundled = Path(tmpdir) / "bundled"
            # Create both plain and compressed
            self._create_test_schema(bundled, (9, 4, 0), compressed=True)
            self._create_test_schema(bundled, (9, 4, 0), compressed=False)

            manager = SchemaManager(bundled_schema_dir=bundled, cache_dir=Path(tmpdir) / "cache")
            schema = manager.get_schema((9, 4, 0))

            assert isinstance(schema, EpJSONSchema)

    def test_schema_not_found_error(self) -> None:
        """Should raise SchemaNotFoundError for unavailable version."""
        import pytest

        from idfkit.exceptions import SchemaNotFoundError

        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SchemaManager(
                bundled_schema_dir=Path(tmpdir) / "empty",
                cache_dir=Path(tmpdir) / "empty_cache",
            )
            with pytest.raises(SchemaNotFoundError):
                manager.get_schema((99, 0, 0))


class TestBundledSchemas:
    """Tests that verify bundled schemas load correctly."""

    def test_bundled_v24_1_0_loads(self) -> None:
        """The bundled V24-1-0 schema should load successfully."""
        manager = SchemaManager()
        schema = manager.get_schema((24, 1, 0))
        assert isinstance(schema, EpJSONSchema)
        assert "Zone" in schema
        assert len(schema) > 100  # Should have many object types

    def test_available_versions_nonempty(self) -> None:
        """At least one version should be available from bundled schemas."""
        manager = SchemaManager()
        versions = manager.get_available_versions()
        assert len(versions) >= 1
        assert (24, 1, 0) in versions

    def test_all_bundled_schemas_load(self) -> None:
        """All bundled schemas should load and contain Zone objects."""
        manager = SchemaManager()
        available = manager.get_available_versions()

        for version in available:
            manager.clear_cache()
            schema = manager.get_schema(version)
            assert isinstance(schema, EpJSONSchema), f"Failed for {version}"
            assert "Zone" in schema, f"Zone not in schema for {version}"

    def test_new_document_with_latest_version(self) -> None:
        """new_document() with LATEST_VERSION should work if schema is bundled."""
        import pytest

        from idfkit import new_document
        from idfkit.versions import LATEST_VERSION

        manager = SchemaManager()
        available = manager.get_available_versions()

        if LATEST_VERSION in available:
            model = new_document()
            assert model.version == LATEST_VERSION
        else:
            with pytest.raises(SchemaNotFoundError):
                new_document()
