"""
Streaming IDF parser - parses EnergyPlus IDF files into IDFDocument.

Features:
- Memory-efficient streaming for large files
- Regex-based tokenization
- Direct parsing into IDFDocument (no intermediate structures)
- Type coercion based on schema
"""

from __future__ import annotations

import logging
import mmap
import re
import time
from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .document import IDFDocument
from .exceptions import IDFParseError, ParseDiagnostic, VersionNotFoundError
from .objects import IDFObject

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .schema import EpJSONSchema, ParsingCache

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


def _coerce_value_fast(field_type: str | None, value: str) -> Any:
    """Coerce a field value using a pre-resolved type string."""
    if field_type == "number":
        try:
            return float(value)
        except ValueError:
            return value
    if field_type == "integer":
        try:
            return int(float(value))
        except ValueError:
            return value
    return value


def parse_idf(
    filepath: Path | str,
    schema: EpJSONSchema | None = None,
    version: tuple[int, int, int] | None = None,
    encoding: str = "latin-1",
    strict: bool = True,
) -> IDFDocument:
    """
    Parse an IDF file into an IDFDocument.

    Args:
        filepath: Path to the IDF file
        schema: Optional EpJSONSchema for field ordering and type coercion
        version: Optional version override (auto-detected if not provided)
        encoding: File encoding (default: latin-1 for compatibility)
        strict: If True, fail fast on malformed objects (default: True)

    Returns:
        Parsed IDFDocument

    Raises:
        VersionNotFoundError: If version cannot be detected
        IdfKitError: If parsing fails

    Examples:
        Load and inspect a DOE reference building:

            ```python
            from idfkit import parse_idf

            model = parse_idf("RefBldgSmallOfficeNew2004.idf")
            for zone in model["Zone"]:
                print(zone.name, zone.x_origin)
            ```

        Force a specific EnergyPlus version when auto-detection fails
        (e.g., a pre-v8.9 file that was manually upgraded):

            ```python
            model = parse_idf("legacy_building.idf", version=(9, 6, 0))
            ```
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"IDF file not found: {filepath}")  # noqa: TRY003

    parser = IDFParser(filepath, schema, encoding, strict=strict)
    return parser.parse(version)


class IDFParser:
    """
    Streaming parser for IDF files.

    Uses memory mapping for large files and regex for tokenization.
    """

    __slots__ = ("_content", "_encoding", "_filepath", "_schema", "_strict")

    _filepath: Path
    _schema: EpJSONSchema | None
    _encoding: str
    _content: bytes | None
    _strict: bool

    def __init__(
        self,
        filepath: Path,
        schema: EpJSONSchema | None = None,
        encoding: str = "latin-1",
        strict: bool = True,
    ):
        self._filepath = filepath
        self._schema = schema
        self._encoding = encoding
        self._strict = strict
        self._content: bytes | None = None

    def parse(self, version: tuple[int, int, int] | None = None) -> IDFDocument:
        """
        Parse the IDF file into an IDFDocument.

        Args:
            version: Optional version override

        Returns:
            Parsed IDFDocument
        """
        t0 = time.perf_counter()
        logger.debug("Parsing IDF file %s", self._filepath)

        # Load content (with mmap for large files)
        content = self._load_content()

        # Detect version if not provided
        if version is None:
            version = self._detect_version(content)
            logger.debug("Detected version %d.%d.%d", *version)

        # Load schema if not provided
        schema = self._schema
        if schema is None:
            from .schema import get_schema

            schema = get_schema(version)

        # Create document
        doc = IDFDocument(version=version, schema=schema, filepath=self._filepath)

        # Parse objects
        self._parse_objects(content, doc, schema)

        elapsed = time.perf_counter() - t0
        logger.info("Parsed %d objects from %s in %.3fs", len(doc), self._filepath, elapsed)

        return doc

    def _load_content(self) -> bytes:
        """Load file content, using mmap for large files."""
        file_size = self._filepath.stat().st_size
        use_mmap = file_size > _MMAP_THRESHOLD

        if use_mmap:
            logger.debug("Using mmap for large file (%d bytes)", file_size)
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

        # Local per-type cache avoids repeated schema lookups
        type_cache: dict[str, ParsingCache | None] = {}
        encoding = self._encoding
        addidfobject = doc.addidfobject
        skipped_types: set[str] = set()

        for match in _OBJECT_PATTERN.finditer(content):
            match_offset = match.start(1)
            obj_type: str | None = None
            obj_name: str | None = None

            try:
                decoded_obj_type = match.group(1).decode(encoding).strip()
                obj_type = decoded_obj_type

                # Skip version object (handled separately)
                if decoded_obj_type.upper() == "VERSION":
                    continue

                obj_name = self._extract_object_name(match, encoding)

                pc, should_skip = self._resolve_type_cache(
                    content=content,
                    schema=schema,
                    type_cache=type_cache,
                    skipped_types=skipped_types,
                    obj_type=decoded_obj_type,
                    obj_name=obj_name,
                    match_offset=match_offset,
                )
                if should_skip:
                    continue

                obj = self._parse_object_cached(match, pc, encoding)
                if obj:
                    addidfobject(obj)
            except IDFParseError:
                raise
            except Exception as exc:
                if self._strict:
                    self._raise_parse_error(
                        content,
                        match_offset,
                        f"Failed to parse object: {exc}",
                        obj_type=obj_type,
                        obj_name=obj_name,
                    )
                logger.warning("Skipping malformed object %r: %s", obj_type or "<decode_error>", exc)

        if skipped_types:
            logger.warning(
                "Skipped %d unknown object type(s): %s", len(skipped_types), ", ".join(sorted(skipped_types))
            )

    def _parse_object_cached(
        self,
        match: re.Match[bytes],
        pc: ParsingCache | None,
        encoding: str,
    ) -> IDFObject | None:
        """Parse a single object from regex match using cached metadata."""
        obj_type = match.group(1).decode(encoding).strip()
        fields_raw = match.group(2).decode(encoding)

        fields = self._parse_fields(fields_raw)
        if not fields:
            return None

        if pc is not None:
            has_name = pc.has_name
            # Mutable copy since extensible parsing appends to it
            field_names: list[str] = list(pc.field_names) if has_name else list(pc.all_field_names)

            name, remaining_fields = (fields[0], fields[1:]) if has_name else ("", fields)

            data = self._build_data_dict_cached(remaining_fields, field_names, pc)

            return IDFObject(
                obj_type=obj_type,
                name=name,
                data=data,
                schema=pc.obj_schema,
                field_order=field_names,
                ref_fields=pc.ref_fields,
            )

        # No-schema fallback
        name = fields[0] if fields else ""
        remaining = fields[1:]
        data: dict[str, Any] = {}
        for i, value in enumerate(remaining):
            if value:
                data[f"field_{i + 1}"] = value
        return IDFObject(obj_type=obj_type, name=name, data=data)

    def _build_data_dict_cached(
        self,
        remaining_fields: list[str],
        field_names: list[str],
        pc: ParsingCache,
    ) -> dict[str, Any]:
        """Build the data dict using pre-computed field types from the cache."""
        data: dict[str, Any] = {}
        field_types = pc.field_types
        num_named = len(field_names)

        for i, value in enumerate(remaining_fields):
            if i < num_named:
                field_name = field_names[i]
                if value:
                    data[field_name] = _coerce_value_fast(field_types.get(field_name), value)
                else:
                    data[field_name] = ""

        if not pc.extensible and len(remaining_fields) > num_named and self._strict:
            overflow = len(remaining_fields) - num_named
            msg = (
                f"Object has {overflow} extra field(s) but type is not extensible "
                f"(expected at most {num_named}, got {len(remaining_fields)})"
            )
            raise ValueError(msg)

        if pc.extensible and num_named < len(remaining_fields):
            extra = remaining_fields[num_named:]
            self._append_extensible_fields(
                data=data,
                extra=extra,
                field_names=field_names,
                field_types=field_types,
                pc=pc,
            )

        return data

    def _append_extensible_fields(
        self,
        *,
        data: dict[str, Any],
        extra: list[str],
        field_names: list[str],
        field_types: dict[str, str | None],
        pc: ParsingCache,
    ) -> None:
        """Append extensible field groups to parsed data."""
        ext_size = pc.ext_size
        if ext_size <= 0:
            if self._strict:
                msg = "Object is marked extensible but extensible group size is invalid"
                raise ValueError(msg)
            return

        ext_names = pc.ext_field_names
        num_ext = len(ext_names)
        for group_idx in range(0, len(extra), ext_size):
            group = extra[group_idx : group_idx + ext_size]
            suffix = "" if group_idx == 0 else f"_{group_idx // ext_size + 1}"
            for j, value in enumerate(group):
                if j >= num_ext:
                    continue
                ext_field = f"{ext_names[j]}{suffix}"
                if value:
                    data[ext_field] = _coerce_value_fast(field_types.get(ext_names[j]), value)
                else:
                    data[ext_field] = ""
                field_names.append(ext_field)

    def _parse_fields(self, fields_raw: str) -> list[str]:
        """Parse and clean field values from raw string."""
        # Fast path: comments already stripped by _COMMENT_PATTERN in _parse_objects
        if "!" not in fields_raw:
            return [part.strip() for part in fields_raw.split(",")]

        # Slow path: strip inline comments (safety fallback)
        lines: list[str] = []
        for line in fields_raw.split("\n"):
            idx = line.find("!")
            if idx >= 0:
                line = line[:idx]
            lines.append(line)
        clean_text = " ".join(lines)
        return [part.strip() for part in clean_text.split(",")]

    @staticmethod
    def _line_and_column(content: bytes, offset: int) -> tuple[int, int]:
        """Convert a byte offset to 1-based (line, column)."""
        line = content.count(b"\n", 0, offset) + 1
        previous_newline = content.rfind(b"\n", 0, offset)
        if previous_newline < 0:
            return (line, offset + 1)
        return (line, offset - previous_newline)

    @staticmethod
    def _extract_object_name(match: re.Match[bytes], encoding: str) -> str | None:
        """Best-effort extraction of the raw first field (typically object name)."""
        fields_raw = match.group(2).decode(encoding)
        first = fields_raw.split(",", maxsplit=1)[0].strip()
        return first or None

    def _raise_parse_error(
        self,
        content: bytes,
        offset: int,
        message: str,
        *,
        obj_type: str | None = None,
        obj_name: str | None = None,
    ) -> None:
        """Raise a ParseError with contextual diagnostics."""
        line, column = self._line_and_column(content, offset)
        diagnostic = ParseDiagnostic(
            message=message,
            filepath=str(self._filepath),
            obj_type=obj_type,
            obj_name=obj_name,
            line=line,
            column=column,
        )
        summary = "Failed to parse IDF"
        raise IDFParseError(summary, diagnostics=[diagnostic])

    def _resolve_type_cache(
        self,
        *,
        content: bytes,
        schema: EpJSONSchema | None,
        type_cache: dict[str, ParsingCache | None],
        skipped_types: set[str],
        obj_type: str,
        obj_name: str | None,
        match_offset: int,
    ) -> tuple[ParsingCache | None, bool]:
        """Resolve and cache parsing metadata for an object type."""
        if schema is None:
            return (None, False)

        pc = type_cache.get(obj_type)
        if pc is None and obj_type not in type_cache:
            pc = schema.get_parsing_cache(obj_type)
            type_cache[obj_type] = pc

        if pc is not None:
            return (pc, False)

        if self._strict:
            msg = f"Unknown object type '{obj_type}'"
            self._raise_parse_error(content, match_offset, msg, obj_type=obj_type, obj_name=obj_name)
        skipped_types.add(obj_type)
        return (None, True)


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
        (useful for quickly sizing batch runs):

            ```python
            from idfkit import iter_idf_objects

            zone_count = sum(
                1 for obj_type, name, _
                in iter_idf_objects("5ZoneAirCooled.idf")
                if obj_type == "Zone"
            )
            ```

        Collect all material names for an audit report:

            ```python
            materials = [
                name for obj_type, name, _
                in iter_idf_objects("LargeOffice.idf")
                if obj_type == "Material"
            ]
            ```
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
        (reads only the first 10 KB for speed):

            ```python
            from idfkit import get_idf_version

            version = get_idf_version("5ZoneAirCooled.idf")
            print(f"EnergyPlus v{version[0]}.{version[1]}.{version[2]}")
            ```
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
