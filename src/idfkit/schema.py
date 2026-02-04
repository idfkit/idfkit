"""
EpJSON Schema loader and manager.

Handles loading and caching of Energy+.schema.epJSON files
for different EnergyPlus versions. Supports both uncompressed
and gzip-compressed schema files.
"""

from __future__ import annotations

import gzip
import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, ClassVar

from .exceptions import SchemaNotFoundError
from .versions import (
    ENERGYPLUS_VERSIONS,
    find_closest_version,
    version_dirname,
)


class EpJSONSchema:
    """
    Wrapper around Energy+.schema.epJSON providing easy access to object definitions.

    The schema contains:
    - Object definitions with field types, defaults, constraints
    - Reference lists (object-list) for cross-object validation
    - Legacy IDD info for IDF field ordering

    Attributes:
        version: The EnergyPlus version tuple
        _raw: The raw schema dict
        _properties: Object definitions
    """

    __slots__ = ("_object_lists", "_properties", "_raw", "_reference_lists", "version")

    version: tuple[int, int, int]
    _raw: dict[str, Any]
    _properties: dict[str, Any]
    _reference_lists: dict[str, list[str]]
    _object_lists: dict[str, set[str]]

    def __init__(self, version: tuple[int, int, int], schema_data: dict[str, Any]) -> None:
        self.version = version
        self._raw = schema_data
        self._properties: dict[str, Any] = schema_data.get("properties", {})

        # Build reference indexes
        self._reference_lists: dict[str, list[str]] = {}
        self._object_lists: dict[str, set[str]] = {}
        self._build_reference_indexes()

    def _build_reference_indexes(self) -> None:
        """Build indexes for reference and object lists."""
        for obj_type, obj_schema in self._properties.items():
            # Check if this object provides names for any reference lists
            name_info = obj_schema.get("name", {})
            if "reference" in name_info:
                for ref_list in name_info["reference"]:
                    if ref_list not in self._reference_lists:
                        self._reference_lists[ref_list] = []
                    self._reference_lists[ref_list].append(obj_type)

            # Find fields that reference object lists
            pattern_props: dict[str, Any] = obj_schema.get("patternProperties", {})
            default_dict: dict[str, Any] = {}
            inner: dict[str, Any] = next(iter(pattern_props.values()), default_dict) if pattern_props else default_dict
            props: dict[str, Any] = inner.get("properties", {})
            for field_name, field_schema in props.items():
                field_schema_dict: dict[str, Any] = field_schema
                if "object_list" in field_schema_dict:
                    for obj_list in field_schema_dict["object_list"]:
                        if obj_list not in self._object_lists:
                            self._object_lists[obj_list] = set()
                        self._object_lists[obj_list].add(f"{obj_type}.{field_name}")

    def get_object_schema(self, obj_type: str) -> dict[str, Any] | None:
        """Get the full schema for an object type."""
        return self._properties.get(obj_type)

    def get_inner_schema(self, obj_type: str) -> dict[str, Any] | None:
        """Get the inner schema (inside patternProperties) for an object type."""
        obj_schema = self.get_object_schema(obj_type)
        if not obj_schema:
            return None
        pattern_props = obj_schema.get("patternProperties", {})
        # The pattern key varies (e.g., ".*", "^.*\\S.*$") - get the first one
        for key in pattern_props:
            return pattern_props[key]
        return None

    def get_field_schema(self, obj_type: str, field_name: str) -> dict[str, Any] | None:
        """Get schema for a specific field of an object type."""
        inner = self.get_inner_schema(obj_type)
        if not inner:
            return None
        return inner.get("properties", {}).get(field_name)

    def get_field_names(self, obj_type: str) -> list[str]:
        """Get ordered list of field names for an object type (from legacy_idd)."""
        obj_schema = self.get_object_schema(obj_type)
        if not obj_schema:
            return []
        legacy = obj_schema.get("legacy_idd", {})
        fields = legacy.get("fields", [])
        # First field is 'name', return the rest
        return fields[1:] if fields else []

    def get_all_field_names(self, obj_type: str) -> list[str]:
        """Get all field names including 'name'."""
        obj_schema = self.get_object_schema(obj_type)
        if not obj_schema:
            return []
        legacy = obj_schema.get("legacy_idd", {})
        return legacy.get("fields", [])

    def get_required_fields(self, obj_type: str) -> list[str]:
        """Get list of required field names for an object type."""
        inner = self.get_inner_schema(obj_type)
        if not inner:
            return []
        return inner.get("required", [])

    def get_field_default(self, obj_type: str, field_name: str) -> Any:
        """Get default value for a field."""
        field_schema = self.get_field_schema(obj_type, field_name)
        if field_schema:
            return field_schema.get("default")
        return None

    def get_field_type(self, obj_type: str, field_name: str) -> str | None:
        """Get the type of a field ('number', 'string', 'integer', 'array')."""
        field_schema = self.get_field_schema(obj_type, field_name)
        if not field_schema:
            return None

        # Handle anyOf (e.g., number OR "Autocalculate")
        if "anyOf" in field_schema:
            for sub in field_schema["anyOf"]:
                if sub.get("type") in ("number", "integer"):
                    return sub["type"]
            return "string"

        return field_schema.get("type")

    def get_field_object_list(self, obj_type: str, field_name: str) -> list[str] | None:
        """Get the object_list(s) that a field references."""
        field_schema = self.get_field_schema(obj_type, field_name)
        if field_schema:
            return field_schema.get("object_list")
        return None

    def is_reference_field(self, obj_type: str, field_name: str) -> bool:
        """Check if a field is a reference to another object."""
        return self.get_field_object_list(obj_type, field_name) is not None

    def get_types_providing_reference(self, ref_list: str) -> list[str]:
        """Get object types that provide names for a reference list."""
        return self._reference_lists.get(ref_list, [])

    def get_object_memo(self, obj_type: str) -> str | None:
        """Get the memo/description for an object type."""
        obj_schema = self.get_object_schema(obj_type)
        if obj_schema:
            return obj_schema.get("memo")
        return None

    def is_extensible(self, obj_type: str) -> bool:
        """Check if an object type has extensible fields."""
        obj_schema = self.get_object_schema(obj_type)
        if obj_schema:
            return "extensible_size" in obj_schema
        return False

    def get_extensible_size(self, obj_type: str) -> int | None:
        """Get the extensible group size for an object type."""
        obj_schema = self.get_object_schema(obj_type)
        if obj_schema:
            return obj_schema.get("extensible_size")
        return None

    @property
    def object_types(self) -> list[str]:
        """Get list of all object types in the schema."""
        return list(self._properties.keys())

    def __contains__(self, obj_type: str) -> bool:
        """Check if an object type exists in the schema."""
        return obj_type in self._properties

    def __len__(self) -> int:
        """Return number of object types."""
        return len(self._properties)


_SCHEMA_FILENAME = "Energy+.schema.epJSON"
_SCHEMA_FILENAME_GZ = "Energy+.schema.epJSON.gz"


def load_schema_json(path: Path) -> dict[str, Any]:
    """Load a schema JSON file, handling both plain and gzip-compressed files."""
    if path.suffix == ".gz" or path.name.endswith(".epJSON.gz"):
        with gzip.open(path, "rt", encoding="utf-8") as f:
            return json.load(f)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class SchemaManager:
    """
    Manages loading and caching of EpJSON schemas for different versions.

    Searches for schemas in the following order:
    1. Bundled schemas directory (shipped with idfkit) - both .gz and plain
    2. User cache directory (~/.idfkit/schemas/)
    3. EnergyPlus installation directories

    Supports gzip-compressed schema files (.epJSON.gz) to reduce package size.
    """

    # Common EnergyPlus installation paths by platform
    _INSTALL_PATHS: ClassVar[dict[str, list[str]]] = {
        "linux": ["/usr/local/EnergyPlus-{v}", "/opt/EnergyPlus-{v}"],
        "darwin": ["/Applications/EnergyPlus-{v}"],
        "win32": [
            "C:\\EnergyPlusV{v}",
            "C:\\EnergyPlus-{v}",
            os.path.expandvars("$LOCALAPPDATA\\EnergyPlusV{v}"),
        ],
    }

    def __init__(
        self,
        bundled_schema_dir: Path | None = None,
        cache_dir: Path | None = None,
    ):
        """
        Initialize the schema manager.

        Args:
            bundled_schema_dir: Path to directory with bundled schema files.
                               If None, uses default location next to this file.
            cache_dir: Path to user cache directory for downloaded schemas.
                       If None, uses ~/.idfkit/schemas/.
        """
        if bundled_schema_dir is None:
            bundled_schema_dir = Path(__file__).parent / "schemas"

        if cache_dir is None:
            cache_dir = Path.home() / ".idfkit" / "schemas"

        self._bundled_dir = bundled_schema_dir
        self._cache_dir = cache_dir
        self._cache: dict[tuple[int, int, int], EpJSONSchema] = {}

    @property
    def bundled_dir(self) -> Path:
        """Path to the bundled schemas directory."""
        return self._bundled_dir

    @property
    def cache_dir(self) -> Path:
        """Path to the user cache directory for schemas."""
        return self._cache_dir

    @lru_cache(maxsize=8)  # noqa: B019
    def get_schema(self, version: tuple[int, int, int]) -> EpJSONSchema:
        """
        Load and return schema for a specific version.

        If the exact version is not found, attempts to find the closest
        supported version that is <= the requested version.

        Args:
            version: EnergyPlus version tuple (major, minor, patch)

        Returns:
            EpJSONSchema for the requested version

        Raises:
            SchemaNotFoundError: If schema cannot be found
        """
        if version in self._cache:
            return self._cache[version]

        # Try exact version first
        schema_path = self._find_schema_file(version)
        if schema_path is None:
            # Try closest supported version
            closest = find_closest_version(version)
            if closest is not None and closest != version:
                schema_path = self._find_schema_file(closest)

        if schema_path is None:
            searched = self._get_searched_paths(version)
            raise SchemaNotFoundError(version, searched)

        data = load_schema_json(schema_path)

        schema = EpJSONSchema(version, data)
        self._cache[version] = schema
        return schema

    def _find_schema_file(self, version: tuple[int, int, int]) -> Path | None:
        """
        Find the schema file for a version.

        Searches bundled directory first (both compressed and plain),
        then user cache, then EnergyPlus installations.
        """
        # Try bundled schemas first
        for path in self._get_bundled_paths(version):
            if path.exists():
                return path

        # Try user cache
        for path in self._get_cache_paths(version):
            if path.exists():
                return path

        # Try EnergyPlus installation
        for path in self._get_install_paths(version):
            if path.exists():
                return path

        return None

    def _get_searched_paths(self, version: tuple[int, int, int]) -> list[str]:
        """Get all paths that would be searched for a version (for error messages)."""
        paths: list[str] = []
        for p in self._get_bundled_paths(version):
            paths.append(str(p))
        for p in self._get_cache_paths(version):
            paths.append(str(p))
        for p in self._get_install_paths(version):
            paths.append(str(p))
        return paths

    def _get_bundled_paths(self, version: tuple[int, int, int]) -> list[Path]:
        """Get potential bundled schema paths for a version."""
        paths: list[Path] = []
        dirname = version_dirname(version)

        # Compressed first (preferred for bundled), then plain
        paths.append(self._bundled_dir / dirname / _SCHEMA_FILENAME_GZ)
        paths.append(self._bundled_dir / dirname / _SCHEMA_FILENAME)

        return paths

    def _get_cache_paths(self, version: tuple[int, int, int]) -> list[Path]:
        """Get potential user cache schema paths for a version."""
        paths: list[Path] = []
        dirname = version_dirname(version)

        paths.append(self._cache_dir / dirname / _SCHEMA_FILENAME_GZ)
        paths.append(self._cache_dir / dirname / _SCHEMA_FILENAME)

        return paths

    def _get_install_paths(self, version: tuple[int, int, int]) -> list[Path]:
        """Get potential EnergyPlus installation schema paths."""
        import sys

        platform = sys.platform
        paths: list[Path] = []
        v = version

        # Get base paths for this platform
        base_patterns: list[str] = self._INSTALL_PATHS.get(platform, self._INSTALL_PATHS.get("linux", []))

        version_formats = [
            f"{v[0]}-{v[1]}-{v[2]}",
            f"{v[0]}.{v[1]}.{v[2]}",
            f"{v[0]}-{v[1]}",
        ]

        for base_pattern in base_patterns:
            for v_fmt in version_formats:
                base_path = Path(base_pattern.format(v=v_fmt))
                paths.append(base_path / _SCHEMA_FILENAME)

        return paths

    def get_available_versions(self) -> list[tuple[int, int, int]]:  # noqa: C901
        """
        Get list of versions with available schemas.

        Checks bundled schemas, user cache, and installed EnergyPlus versions.
        """
        versions: set[tuple[int, int, int]] = set()

        # Check bundled
        if self._bundled_dir.exists():
            for item in self._bundled_dir.iterdir():
                if item.is_dir():
                    version = self._parse_version_from_dirname(item.name)
                    if version and self._dir_has_schema(item):
                        versions.add(version)

        # Check user cache
        if self._cache_dir.exists():
            for item in self._cache_dir.iterdir():
                if item.is_dir():
                    version = self._parse_version_from_dirname(item.name)
                    if version and self._dir_has_schema(item):
                        versions.add(version)

        # Check installed EnergyPlus versions
        import sys

        platform = sys.platform
        base_patterns: list[str] = self._INSTALL_PATHS.get(platform, self._INSTALL_PATHS.get("linux", []))

        for pattern in base_patterns:
            # Look for existing directories matching the pattern
            parent = Path(pattern.split("{v}")[0])
            if parent.exists():
                for item in parent.iterdir():
                    if item.is_dir() and "EnergyPlus" in item.name:
                        version = self._parse_version_from_dirname(item.name)
                        if version:
                            schema_path = item / _SCHEMA_FILENAME
                            if schema_path.exists():
                                versions.add(version)

        return sorted(versions)

    @staticmethod
    def _dir_has_schema(directory: Path) -> bool:
        """Check if a directory contains a schema file (plain or compressed)."""
        return (directory / _SCHEMA_FILENAME).exists() or (directory / _SCHEMA_FILENAME_GZ).exists()

    @staticmethod
    def _parse_version_from_dirname(dirname: str) -> tuple[int, int, int] | None:
        """Parse version tuple from directory name."""
        import re

        # Match patterns like "9-2-0", "9.2.0", "V9-2-0", "EnergyPlus-9-2-0"
        match = re.search(r"(\d+)[-._](\d+)[-._]?(\d+)?", dirname)
        if match:
            major = int(match.group(1))
            minor = int(match.group(2))
            patch = int(match.group(3)) if match.group(3) else 0
            return (major, minor, patch)
        return None

    def clear_cache(self) -> None:
        """Clear the schema cache."""
        self._cache.clear()
        self.get_schema.cache_clear()

    def get_supported_versions(self) -> list[tuple[int, int, int]]:
        """Get list of all EnergyPlus versions that idfkit supports.

        This returns all versions in the registry, regardless of whether
        schema files are currently available locally.
        """
        return list(ENERGYPLUS_VERSIONS)


# Global schema manager instance
_schema_manager: SchemaManager | None = None


def get_schema_manager() -> SchemaManager:
    """Get the global schema manager instance."""
    global _schema_manager
    if _schema_manager is None:
        _schema_manager = SchemaManager()
    return _schema_manager


def get_schema(version: tuple[int, int, int]) -> EpJSONSchema:
    """Convenience function to get schema for a version."""
    return get_schema_manager().get_schema(version)
