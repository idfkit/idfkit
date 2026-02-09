"""
epJSON parser - parses EnergyPlus epJSON files into IDFDocument.

The epJSON format is the native JSON representation of EnergyPlus models.
Parsing is straightforward since it's already structured JSON.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from .document import IDFDocument
from .exceptions import VersionNotFoundError
from .objects import IDFObject

if TYPE_CHECKING:
    from .schema import EpJSONSchema


def parse_epjson(
    filepath: Path | str,
    schema: EpJSONSchema | None = None,
    version: tuple[int, int, int] | None = None,
) -> IDFDocument:
    """
    Parse an epJSON file into an IDFDocument.

    Args:
        filepath: Path to the epJSON file
        schema: Optional EpJSONSchema for validation
        version: Optional version override (auto-detected if not provided)

    Returns:
        Parsed IDFDocument

    Raises:
        VersionNotFoundError: If version cannot be detected
        IdfKitError: If parsing fails
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"epJSON file not found: {filepath}")  # noqa: TRY003

    parser = EpJSONParser(filepath, schema)
    return parser.parse(version)


class EpJSONParser:
    """
    Parser for epJSON files.

    epJSON is the native JSON format for EnergyPlus models, making
    parsing straightforward - just json.load() and transform.
    """

    __slots__ = ("_filepath", "_schema")

    def __init__(
        self,
        filepath: Path,
        schema: EpJSONSchema | None = None,
    ):
        self._filepath = filepath
        self._schema = schema

    def parse(self, version: tuple[int, int, int] | None = None) -> IDFDocument:
        """
        Parse the epJSON file into an IDFDocument.

        Args:
            version: Optional version override

        Returns:
            Parsed IDFDocument
        """
        # Load JSON
        with open(self._filepath, encoding="utf-8") as f:
            data = json.load(f)

        # Detect version if not provided
        if version is None:
            version = self._detect_version(data)

        # Load schema if not provided
        schema = self._schema
        if schema is None:
            from .schema import get_schema

            schema = get_schema(version)

        # Create document
        doc = IDFDocument(version=version, schema=schema, filepath=self._filepath)

        # Parse objects
        self._parse_objects(data, doc, schema)

        return doc

    def _detect_version(self, data: dict[str, Any]) -> tuple[int, int, int]:
        """Detect EnergyPlus version from epJSON data."""
        # Version is in the "Version" object
        version_obj = data.get("Version")

        if version_obj:
            # epJSON format: {"Version": {"Version 1": {"version_identifier": "23.2"}}}
            for _name, fields in version_obj.items():
                version_str: str = fields.get("version_identifier", "")
                if version_str:
                    return self._parse_version_string(version_str)

        raise VersionNotFoundError(str(self._filepath))

    @staticmethod
    def _parse_version_string(version_str: str) -> tuple[int, int, int]:
        """Parse version string like '23.2' or '9.2.0'."""
        parts = version_str.split(".")
        major = int(parts[0]) if len(parts) > 0 else 0
        minor = int(parts[1]) if len(parts) > 1 else 0
        patch = int(parts[2]) if len(parts) > 2 else 0
        return (major, minor, patch)

    def _parse_objects(
        self,
        data: dict[str, Any],
        doc: IDFDocument,
        schema: EpJSONSchema | None,
    ) -> None:
        """Parse all objects from epJSON data into document."""
        for obj_type, objects in data.items():
            # Skip Version (handled separately)
            if obj_type == "Version":
                continue

            if not isinstance(objects, dict):
                continue

            # Get schema info for this type
            obj_schema: dict[str, Any] | None = None
            base_field_names: list[str] | None = None
            has_name = True
            if schema:
                obj_schema = schema.get_object_schema(obj_type)
                has_name = schema.has_name(obj_type)
                base_field_names = (
                    schema.get_field_names(obj_type) if has_name else schema.get_all_field_names(obj_type)
                )

            # epJSON format: {"ObjectType": {"obj_name": {fields...}, ...}}
            objects_dict = cast(dict[str, Any], objects)
            for obj_name, fields in objects_dict.items():
                if not isinstance(fields, dict):
                    continue

                # Nameless objects: use empty string instead of epJSON dict key
                name = obj_name if has_name else ""

                # Create per-object field_order copy so extensible fields can be added
                fields_dict = cast(dict[str, Any], fields)
                field_order = self._build_field_order(obj_type, base_field_names, fields_dict, schema)

                obj = IDFObject(
                    obj_type=obj_type,
                    name=name,
                    data=dict(fields_dict),  # Copy the fields dict
                    schema=obj_schema,
                    field_order=field_order,
                )

                doc.addidfobject(obj)

    def _build_field_order(
        self,
        obj_type: str,
        base_field_names: list[str] | None,
        fields_dict: dict[str, Any],
        schema: EpJSONSchema | None,
    ) -> list[str] | None:
        """Build field_order including extensible fields present in the data."""
        if base_field_names is None:
            return None

        # Start with a copy of the base schema field names
        field_order = list(base_field_names)
        base_set = set(base_field_names)

        # Find extensible fields in the data that aren't in the base field list
        if schema and schema.is_extensible(obj_type):
            ext_names = schema.get_extensible_field_names(obj_type)

            if ext_names:
                # Collect extensible fields from data, grouped and ordered
                group_idx = 0
                while True:
                    suffix = "" if group_idx == 0 else f"_{group_idx + 1}"
                    group_fields = [f"{name}{suffix}" for name in ext_names]

                    # Check if any field from this group exists in the data
                    if not any(f in fields_dict for f in group_fields):
                        break

                    for f in group_fields:
                        if f not in base_set:
                            field_order.append(f)

                    group_idx += 1

        return field_order


def load_epjson(filepath: Path | str) -> dict[str, Any]:
    """
    Load raw epJSON data without parsing into document.

    Useful for quick inspection or manipulation.
    """
    filepath = Path(filepath)
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def get_epjson_version(filepath: Path | str) -> tuple[int, int, int]:
    """
    Quick version detection from epJSON file.

    Args:
        filepath: Path to epJSON file

    Returns:
        Version tuple (major, minor, patch)

    Raises:
        VersionNotFoundError: If version cannot be detected
    """
    filepath = Path(filepath)

    with open(filepath, encoding="utf-8") as f:
        # Parse just enough to get version
        data = json.load(f)

    version_obj = data.get("Version")
    if version_obj:
        for _name, fields in version_obj.items():
            version_str: str = fields.get("version_identifier", "")
            if version_str:
                parts = version_str.split(".")
                major = int(parts[0]) if len(parts) > 0 else 0
                minor = int(parts[1]) if len(parts) > 1 else 0
                patch = int(parts[2]) if len(parts) > 2 else 0
                return (major, minor, patch)

    raise VersionNotFoundError(str(filepath))
