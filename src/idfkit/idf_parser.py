"""
Streaming IDF parser - parses EnergyPlus IDF files into IDFDocument.

Features:
- Memory-efficient streaming for large files
- Regex-based tokenization
- Direct parsing into IDFDocument (no intermediate structures)
- Type coercion based on schema
"""

from __future__ import annotations

import mmap
import re
from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .document import IDFDocument
from .exceptions import VersionNotFoundError
from .objects import IDFObject

if TYPE_CHECKING:
    from .schema import EpJSONSchema

# Regex patterns for parsing
_VERSION_PATTERN = re.compile(
    rb"VERSION\s*,\s*(\d+)\.(\d+)(?:\.(\d+))?\s*;",
    re.IGNORECASE,
)

_COMMENT_PATTERN = re.compile(rb"!.*$", re.MULTILINE)

# Pattern to match IDF objects: "ObjectType, field1, field2, ..., fieldN;"
# Handles multi-line objects and comments
_OBJECT_PATTERN = re.compile(
    rb"([A-Za-z][A-Za-z0-9:_ \-]*?)\s*,\s*"  # Object type (group 1)
    rb"((?:[^;!]*(?:![^\n]*\n)?)*?)"  # Fields with optional comments (group 2)
    rb"\s*;",  # Terminating semicolon
    re.DOTALL,
)

# Pattern to split fields (handles inline comments)
_FIELD_SPLIT_PATTERN = re.compile(rb"\s*,\s*")

# Memory map threshold (10 MB)
_MMAP_THRESHOLD = 10 * 1024 * 1024


def parse_idf(
    filepath: Path | str,
    schema: EpJSONSchema | None = None,
    version: tuple[int, int, int] | None = None,
    encoding: str = "latin-1",
) -> IDFDocument:
    """
    Parse an IDF file into an IDFDocument.

    Args:
        filepath: Path to the IDF file
        schema: Optional EpJSONSchema for field ordering and type coercion
        version: Optional version override (auto-detected if not provided)
        encoding: File encoding (default: latin-1 for compatibility)

    Returns:
        Parsed IDFDocument

    Raises:
        VersionNotFoundError: If version cannot be detected
        IdfKitError: If parsing fails

    Examples:
        Load and inspect a DOE reference building::

            from idfkit import parse_idf

            model = parse_idf("RefBldgSmallOfficeNew2004.idf")
            for zone in model["Zone"]:
                print(zone.name, zone.x_origin)

        Force a specific EnergyPlus version when auto-detection fails
        (e.g., a pre-v8.9 file that was manually upgraded)::

            model = parse_idf("legacy_building.idf", version=(9, 6, 0))
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"IDF file not found: {filepath}")  # noqa: TRY003

    parser = IDFParser(filepath, schema, encoding)
    return parser.parse(version)


class IDFParser:
    """
    Streaming parser for IDF files.

    Uses memory mapping for large files and regex for tokenization.
    """

    __slots__ = ("_content", "_encoding", "_filepath", "_schema")

    _filepath: Path
    _schema: EpJSONSchema | None
    _encoding: str
    _content: bytes | None

    def __init__(
        self,
        filepath: Path,
        schema: EpJSONSchema | None = None,
        encoding: str = "latin-1",
    ):
        self._filepath = filepath
        self._schema = schema
        self._encoding = encoding
        self._content: bytes | None = None

    def parse(self, version: tuple[int, int, int] | None = None) -> IDFDocument:
        """
        Parse the IDF file into an IDFDocument.

        Args:
            version: Optional version override

        Returns:
            Parsed IDFDocument
        """
        # Load content (with mmap for large files)
        content = self._load_content()

        # Detect version if not provided
        if version is None:
            version = self._detect_version(content)

        # Load schema if not provided
        schema = self._schema
        if schema is None:
            from .schema import get_schema

            schema = get_schema(version)

        # Create document
        doc = IDFDocument(version=version, schema=schema, filepath=self._filepath)

        # Parse objects
        self._parse_objects(content, doc, schema)

        return doc

    def _load_content(self) -> bytes:
        """Load file content, using mmap for large files."""
        file_size = self._filepath.stat().st_size

        if file_size > _MMAP_THRESHOLD:
            # Use memory mapping for large files
            with open(self._filepath, "rb") as f:
                mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
                content = bytes(mm)
                mm.close()
        else:
            with open(self._filepath, "rb") as f:
                content = f.read()

        return content

    def _detect_version(self, content: bytes) -> tuple[int, int, int]:
        """Detect EnergyPlus version from file content."""
        # Only search first 10KB for version
        header = content[:10240]

        match = _VERSION_PATTERN.search(header)
        if match:
            major = int(match.group(1))
            minor = int(match.group(2))
            patch = int(match.group(3)) if match.group(3) else 0
            return (major, minor, patch)

        raise VersionNotFoundError(str(self._filepath))

    def _parse_objects(
        self,
        content: bytes,
        doc: IDFDocument,
        schema: EpJSONSchema | None,
    ) -> None:
        """Parse all objects from content into document."""
        # Strip comments before matching to prevent phantom objects
        # (e.g. "!- X,Y,Z Origin" matching "X," as an object type)
        content = _COMMENT_PATTERN.sub(b"", content)
        for match in _OBJECT_PATTERN.finditer(content):
            try:
                obj = self._parse_object(match, schema)
                if obj:
                    doc.addidfobject(obj)
            except Exception:  # noqa: S110
                # Log parse errors but continue
                pass

    def _parse_object(
        self,
        match: re.Match[bytes],
        schema: EpJSONSchema | None,
    ) -> IDFObject | None:
        """Parse a single object from regex match."""
        obj_type = match.group(1).decode(self._encoding).strip()
        fields_raw = match.group(2).decode(self._encoding)

        # Skip version object (handled separately)
        if obj_type.upper() == "VERSION":
            return None

        # Skip unknown object types (filters phantom objects from non-EnergyPlus text)
        if schema and schema.get_object_schema(obj_type) is None:
            return None

        # Split and clean fields
        fields = self._parse_fields(fields_raw)
        if not fields:
            return None

        # Get schema info
        obj_schema: dict[str, Any] | None = None
        field_names: list[str] | None = None
        has_name = True  # default for no-schema fallback

        if schema:
            obj_schema = schema.get_object_schema(obj_type)
            has_name = schema.has_name(obj_type)
            field_names = schema.get_field_names(obj_type) if has_name else schema.get_all_field_names(obj_type)

        # Name handling: named objects use fields[0] as name, nameless use ""
        name, remaining_fields = (fields[0], fields[1:]) if has_name else ("", fields)

        # Build data dict
        data = self._build_data_dict(obj_type, remaining_fields, field_names, schema)

        return IDFObject(
            obj_type=obj_type,
            name=name,
            data=data,
            schema=obj_schema,
            field_order=field_names,
        )

    def _build_data_dict(
        self,
        obj_type: str,
        remaining_fields: list[str],
        field_names: list[str] | None,
        schema: EpJSONSchema | None,
    ) -> dict[str, Any]:
        """Build the data dict from parsed fields using schema field ordering."""
        data: dict[str, Any] = {}

        if field_names is not None:
            # Schema-based: map fields by name, then parse extensibles
            for i, value in enumerate(remaining_fields):
                if i < len(field_names):
                    field_name = field_names[i]
                    # Always store values to preserve field positions
                    # Empty strings are stored as empty strings
                    if value:
                        data[field_name] = self._coerce_value(obj_type, field_name, value, schema)
                    else:
                        data[field_name] = ""
            self._parse_extensible_fields(obj_type, remaining_fields, field_names, data, schema)
        else:
            # No schema — use generic field names
            for i, value in enumerate(remaining_fields):
                if value:
                    data[f"field_{i + 1}"] = value

        return data

    def _parse_extensible_fields(
        self,
        obj_type: str,
        remaining_fields: list[str],
        field_names: list[str],
        data: dict[str, Any],
        schema: EpJSONSchema | None,
    ) -> None:
        """Parse extensible fields (e.g. vertices) beyond the schema-defined field count."""
        extra_start = len(field_names)
        if not schema or not schema.is_extensible(obj_type) or extra_start >= len(remaining_fields):
            return

        ext_size = int(schema.get_extensible_size(obj_type) or 1)
        ext_names = schema.get_extensible_field_names(obj_type)
        extra = remaining_fields[extra_start:]
        for group_idx in range(0, len(extra), ext_size):
            group = extra[group_idx : group_idx + ext_size]
            suffix = "" if group_idx == 0 else f"_{group_idx // ext_size + 1}"
            for j, value in enumerate(group):
                if j < len(ext_names):
                    ext_field = f"{ext_names[j]}{suffix}"
                    # Always store values to preserve field positions in extensible groups
                    # Empty strings are stored as empty strings
                    if value:
                        data[ext_field] = self._coerce_value(obj_type, ext_names[j], value, schema)
                    else:
                        data[ext_field] = ""
                    field_names.append(ext_field)  # extend field_order

    def _parse_fields(self, fields_raw: str) -> list[str]:
        """Parse and clean field values from raw string."""
        # First, strip comments from each line (comments may contain commas)
        lines: list[str] = []
        for line in fields_raw.split("\n"):
            if "!" in line:
                line = line[: line.index("!")]
            lines.append(line)

        # Join lines and split by comma
        clean_text = " ".join(lines)
        fields: list[str] = []
        for part in clean_text.split(","):
            value = part.strip()
            fields.append(value)

        return fields

    def _coerce_value(
        self,
        obj_type: str,
        field_name: str,
        value: str,
        schema: EpJSONSchema | None,
    ) -> Any:
        """Coerce a field value to the appropriate type."""
        if not schema or not value:
            return value

        field_type = schema.get_field_type(obj_type, field_name)

        if field_type == "number":
            try:
                # Handle scientific notation
                return float(value)
            except ValueError:
                # Might be "Autocalculate", "Autosize", etc. — preserve original casing
                return value

        elif field_type == "integer":
            try:
                return int(float(value))
            except ValueError:
                return value

        # Default: return as string
        return value


def iter_idf_objects(
    filepath: Path | str,
    encoding: str = "latin-1",
) -> Iterator[tuple[str, str, list[str]]]:
    """
    Iterate over objects in an IDF file without loading into document.

    Yields:
        Tuples of (object_type, name, [field_values])

    This is useful for quick scanning or filtering without full parsing.

    Examples:
        Count thermal zones without loading the full document
        (useful for quickly sizing batch runs)::

            from idfkit import iter_idf_objects

            zone_count = sum(
                1 for obj_type, name, _
                in iter_idf_objects("5ZoneAirCooled.idf")
                if obj_type == "Zone"
            )

        Collect all material names for an audit report::

            materials = [
                name for obj_type, name, _
                in iter_idf_objects("LargeOffice.idf")
                if obj_type == "Material"
            ]
    """
    filepath = Path(filepath)

    with open(filepath, "rb") as f:
        content = f.read()

    # Strip comments before matching to prevent phantom objects
    content = _COMMENT_PATTERN.sub(b"", content)

    for match in _OBJECT_PATTERN.finditer(content):
        obj_type = match.group(1).decode(encoding).strip()
        fields_raw = match.group(2).decode(encoding)

        # Split and clean fields
        fields: list[str] = []
        for part in fields_raw.split(","):
            if "!" in part:
                part = part[: part.index("!")]
            fields.append(part.strip())

        obj_name = fields[0] if fields else ""
        yield (obj_type, obj_name, fields[1:])


def get_idf_version(filepath: Path | str) -> tuple[int, int, int]:
    """
    Quick version detection without full parsing.

    Only reads the first 10 KB of the file, making it very fast
    even for large models.

    Args:
        filepath: Path to IDF file

    Returns:
        Version tuple (major, minor, patch)

    Raises:
        VersionNotFoundError: If version cannot be detected

    Examples:
        Check which EnergyPlus version a model was created for
        (reads only the first 10 KB for speed)::

            from idfkit import get_idf_version

            version = get_idf_version("5ZoneAirCooled.idf")
            print(f"EnergyPlus v{version[0]}.{version[1]}.{version[2]}")
    """
    filepath = Path(filepath)

    with open(filepath, "rb") as f:
        header = f.read(10240)

    match = _VERSION_PATTERN.search(header)
    if match:
        major = int(match.group(1))
        minor = int(match.group(2))
        patch = int(match.group(3)) if match.group(3) else 0
        return (major, minor, patch)

    raise VersionNotFoundError(str(filepath))
