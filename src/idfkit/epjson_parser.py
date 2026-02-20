"""
epJSON parser - parses EnergyPlus epJSON files into IDFDocument.

The epJSON format is the native JSON representation of EnergyPlus models.
Parsing is straightforward since it's already structured JSON.
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from .document import IDFDocument
from .exceptions import VersionNotFoundError
from .objects import IDFObject

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .schema import EpJSONSchema, ParsingCache


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

    Examples:
        Load an epJSON model and list its thermal zones:

            ```python
            from idfkit import parse_epjson

            model = parse_epjson("SmallOffice.epJSON")
            for zone in model["Zone"]:
                print(zone.name)
            ```
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
        t0 = time.perf_counter()
        logger.debug("Parsing epJSON file %s", self._filepath)

        # Load JSON
        with open(self._filepath, encoding="utf-8") as f:
            data = json.load(f)

        # Detect version if not provided
        if version is None:
            version = self._detect_version(data)
            logger.debug("Detected version %d.%d.%d", *version)

        # Load schema if not provided
        schema = self._schema
        if schema is None:
            from .schema import get_schema

            schema = get_schema(version)

        # Create document
        doc = IDFDocument(version=version, schema=schema, filepath=self._filepath)

        # Parse objects
        self._parse_objects(data, doc, schema)

        elapsed = time.perf_counter() - t0
        logger.info("Parsed %d objects from %s in %.3fs", len(doc), self._filepath, elapsed)

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
        addidfobject = doc.addidfobject

        for obj_type, objects in data.items():
            # Skip Version (handled separately)
            if obj_type == "Version":
                continue

            if not isinstance(objects, dict):
                continue

            # Get schema info from parsing cache
            pc: ParsingCache | None = None
            obj_schema: dict[str, Any] | None = None
            base_field_names: tuple[str, ...] | None = None
            ref_fields: frozenset[str] | None = None
            has_name = True
            if schema:
                pc = schema.get_parsing_cache(obj_type)
                if pc is not None:
                    obj_schema = pc.obj_schema
                    has_name = pc.has_name
                    base_field_names = pc.field_names if has_name else pc.all_field_names
                    ref_fields = pc.ref_fields

            # epJSON format: {"ObjectType": {"obj_name": {fields...}, ...}}
            objects_dict = cast(dict[str, Any], objects)
            for obj_name, fields in objects_dict.items():
                if not isinstance(fields, dict):
                    continue

                # Nameless objects: use empty string instead of epJSON dict key
                name = obj_name if has_name else ""

                # Create per-object field_order copy so extensible fields can be added
                fields_dict = cast(dict[str, Any], fields)
                field_order = self._build_field_order(base_field_names, fields_dict, pc)

                obj = IDFObject(
                    obj_type=obj_type,
                    name=name,
                    data=dict(fields_dict),  # Copy the fields dict
                    schema=obj_schema,
                    field_order=field_order,
                    ref_fields=ref_fields,
                )

                addidfobject(obj)

    @staticmethod
    def _build_field_order(
        base_field_names: tuple[str, ...] | None,
        fields_dict: dict[str, Any],
        pc: ParsingCache | None,
    ) -> list[str] | None:
        """Build field_order including extensible fields present in the data."""
        if base_field_names is None:
            return None

        # Start with a copy of the base schema field names
        field_order = list(base_field_names)
        base_set = set(base_field_names)

        # Find extensible fields in the data that aren't in the base field list
        if pc is not None and pc.extensible and pc.ext_field_names:
            ext_names = pc.ext_field_names
            group_idx = 0
            while True:
                suffix = "" if group_idx == 0 else f"_{group_idx + 1}"
                group_fields = [f"{name}{suffix}" for name in ext_names]

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

    Useful for quick inspection or manipulation when you need the
    raw JSON dict rather than an [IDFDocument][idfkit.document.IDFDocument].

    Examples:
        Grab the raw JSON dict for custom post-processing:

            ```python
            from idfkit.epjson_parser import load_epjson

            data = load_epjson("SmallOffice.epJSON")
            zone_names = list(data.get("Zone", {}).keys())
            ```
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

    Examples:
        Detect the EnergyPlus version of an epJSON file:

            ```python
            from idfkit.epjson_parser import get_epjson_version

            version = get_epjson_version("SmallOffice.epJSON")
            print(f"EnergyPlus v{version[0]}.{version[1]}")
            ```
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
