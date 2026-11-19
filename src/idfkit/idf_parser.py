"""
Streaming IDF parser - parses EnergyPlus IDF files into IDFDocument.

Features:
- Memory-efficient streaming for large files
- Regex-based tokenization
- Direct parsing into IDFDocument (no intermediate structures)
- Type coercion based on schema
- Optional CST (Concrete Syntax Tree) for lossless round-tripping
"""

from __future__ import annotations

import codecs
import logging
import mmap
import re
import time
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final, Generic, cast

from .cst import CSTNode, DocumentCST
from .document import AnyIDFDocument, IDFDocument
from .exceptions import (
    FileFormatError,
    IDFParseError,
    ParseDiagnostic,
    ParseDiagnosticCode,
    VersionNotFoundError,
)
from .objects import IDFObject
from .schema import SIZING_SENTINELS

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from typing_extensions import TypeVar

    from .schema import EpJSONSchema, ParsingCache

    # The document type a ParseResult carries: what every release has, unless the loader was told the
    # release (load_idf_with_diagnostics(path, as_type=...) or since=/before=).
    _DocT = TypeVar("_DocT", bound=AnyIDFDocument, default=AnyIDFDocument, covariant=True)
else:
    from typing import TypeVar

    _DocT = TypeVar("_DocT", covariant=True)

# Regex patterns for parsing
# Components past the patch are accepted and ignored: DesignBuilder writes
# ``Version, 23.1.0.002;``, which resolves to 23.1.0 (as idfkit-js does).
_VERSION_PATTERN = re.compile(
    rb"VERSION\s*,\s*(\d+)\.(\d+)(?:\.(\d+))?(?:\.\d+)*\s*;",
    re.IGNORECASE,
)

_COMMENT_PATTERN = re.compile(rb"!.*$", re.MULTILINE)

# epJSON is a JSON object, so its first non-space byte is '{'; IDF text never starts with one.
_EPJSON_START = re.compile(rb"(?:\xef\xbb\xbf)?\s*\{")

_UTF8_BOM = b"\xef\xbb\xbf"


def _search_version(content: bytes) -> re.Match[bytes] | None:
    """The first ``Version`` object in *content*, ignoring any that sits inside a ``!`` comment.

    A comment such as ``! Upgraded from Version,9.0;`` must not choose the schema: the document's
    version comes from the real object, and a schema of another release would read its fields at
    the wrong positions.
    """
    # Most files state their version once, outside any comment: accept the first match whose line
    # has no `!` before it, which costs no copy of the file. IDF has no quoting, so a `!` always
    # opens a comment.
    pos = 0
    while (match := _VERSION_PATTERN.search(content, pos)) is not None:
        line_start = content.rfind(b"\n", 0, match.start()) + 1
        if b"!" not in content[line_start : match.start()]:
            return match
        pos = match.end()
    # Every match was commented out, or a comment splits the object (`Version, !- id` then `24.1;`
    # on the next line): search the text without its comments.
    return _VERSION_PATTERN.search(_COMMENT_PATTERN.sub(b"", content))


def _is_utf8(name: str) -> bool:
    """Whether the codec *name* is UTF-8, with or without the byte-order mark."""
    return codecs.lookup(name).name in ("utf-8", "utf-8-sig")


def _resolve_encoding(content: bytes, requested: str | None) -> tuple[bytes, str, str]:
    """The text of an IDF file, the codec to decode it with, and the codec to write it back with.

    With no *requested* codec, the file is read as UTF-8 when its bytes are valid UTF-8 and hold
    more than ASCII, and as latin-1 otherwise, which is what EnergyPlus writes. A leading UTF-8
    byte-order mark is dropped from the text and remembered in the write codec (``utf-8-sig``), so
    a lossless round trip writes it back. A *requested* codec is used as given, except that a UTF-8
    one (``utf-8`` or ``utf-8-sig``) drops a mark the file has and writes one back only then.
    """
    has_bom = content.startswith(_UTF8_BOM)
    if requested is None:
        if has_bom:
            return content[len(_UTF8_BOM) :], "utf-8", "utf-8-sig"
        if content.isascii():
            return content, "latin-1", "latin-1"
        try:
            content.decode("utf-8")
        except UnicodeDecodeError:
            return content, "latin-1", "latin-1"
        return content, "utf-8", "utf-8"
    if _is_utf8(requested):
        # The mark is written back only when the file had one, whichever UTF-8 codec was named.
        if has_bom:
            return content[len(_UTF8_BOM) :], "utf-8", "utf-8-sig"
        return content, "utf-8", "utf-8"
    return content, requested, requested


# Pattern to match IDF objects: "ObjectType, field1, field2, ..., fieldN;"
# Handles multi-line objects and comments
_OBJECT_PATTERN = re.compile(
    # The first character admits `/` and `*` as well as a letter, so that a stray block comment,
    # which IDF has no syntax for, is reported with the text the file actually wrote rather than
    # with the leading `/*` shaved off. Verified against 8,581 example files across twelve
    # EnergyPlus installations: not one of them parses differently (idfkit#190).
    rb"([A-Za-z/*][A-Za-z0-9:_ /*\-]*?)\s*,\s*"  # Object type (group 1)
    # Fields with optional comments (group 2), written as an unrolled loop. The earlier form nested
    # a quantified group inside a quantified group, which backtracked exponentially in the length of
    # an unterminated tail: thirty characters did not finish in one hundred seconds (idfkit#187).
    # Group 2 may now end with the whitespace before the `;`; every field is stripped downstream.
    rb"([^;!]*(?:![^\n]*\n[^;!]*)*)"
    rb"\s*;",  # Terminating semicolon
    re.DOTALL,
)

#: What may follow the last terminated object without it being an unterminated one. ``\x1a`` is the
#: DOS end-of-file marker that some legacy editors appended.
_TRAILING_BLANK = b" \t\r\n\x0b\x0c\x1a"

#: How much of an unterminated tail is quoted in its finding.
_UNTERMINATED_EXCERPT = 40

#: The object type at the start of an unterminated tail, read the way group 1 of `_OBJECT_PATTERN`
#: reads it, so a tail that does not open like an object is reported with no type.
_TAIL_TYPE_PATTERN = re.compile(rb"([A-Za-z/*][A-Za-z0-9:_ /*\-]*?)\s*,")

#: A line break straight after a value, with no `,` before it: the first sign of an object whose `;` is
#: missing, so that the next object's type was read as part of the value (``0\nMaterial``). Rare in a
#: well-formed file, which ends each line with `,` or `;`, so the fields are only examined when it hits.
_VALUE_THEN_LINE_BREAK = re.compile(r"[^,\s][ \t\r]*\n")

# Pattern to split fields (handles inline comments)
_FIELD_SPLIT_PATTERN = re.compile(rb"\s*,\s*")

# Memory map threshold (10 MB)
_MMAP_THRESHOLD = 10 * 1024 * 1024

# How much of a file ``get_idf_version`` reads before falling back to the whole
# of it. A first guess, not a limit: a file stating its version later is read
# in full rather than refused.
_VERSION_SCAN_BYTES = 10240

# ---------------------------------------------------------------------------
# CST regex patterns
# ---------------------------------------------------------------------------

# Matches either a comment line (alt 1, no capture) or an IDF object (alt 2,
# capture group 1).  Comments get priority so that `!`, `,` and `;` inside
# comments are never mistaken for object delimiters.
_CST_OBJECT_RE = re.compile(
    r"(?:![^\n]*\n?)"  # Alt 1: comment line (no capture group)
    r"|"
    r"("  # Alt 2: object (capture group 1)
    r"[A-Za-z][A-Za-z0-9:_ \t-]*\s*,"  #   Type name + first comma
    # Fields with inline comments, then the semicolon, as an unrolled loop. The earlier nested form
    # backtracked exponentially on an unterminated tail, as `_OBJECT_PATTERN` did (idfkit#187). A
    # comment not ending in a newline runs to the end of the text, so no `;` can follow it anyway.
    r"[^;!]*(?:![^\n]*\n[^;!]*)*;"
    r"[^\n]*"  #   Trailing inline comment on semicolon line
    r"[\r\n]*"  #   Trailing newlines
    r")",
)

# Extracts the type name from a CST object node: everything before the first
# comma that is not inside a leading comment.
_CST_TYPE_NAME_RE = re.compile(r"^(?:![^\n]*\n)*([^;!,\n]*),", re.MULTILINE)


def _coerce_value_fast(field_type: str | None, value: str) -> Any:
    """Coerce a field value using a pre-resolved type string."""
    if field_type == "number":
        try:
            return float(value)
        except ValueError:
            return value
    if field_type == "integer":
        try:
            number = float(value)
        except ValueError:
            return value
        # A fractional value is kept as written rather than truncated, so validation can report it.
        return int(number) if number.is_integer() else number
    return value


#: Field types whose value is coerced, and therefore whose coercion can fail.
_NUMERIC_FIELD_TYPES: Final = frozenset({"number", "integer"})


#: The two sizing sentinels, accepted in ANY numeric field.
#:
#: Not read from the field's own enum, deliberately. The schema EnergyPlus ships is NARROWER than
#: the engine it ships with, and its own example files prove it. Both of these declare a string
#: branch naming exactly one sentinel, and the shipped files use the other one:
#:
#:   PlantLoop.plant_loop_volume                                   allows "Autocalculate", 28 files
#:                                                                 write "Autosize"
#:   AirTerminal:SingleDuct:VAV:Reheat                             allows "Autosize", 673 files
#:     .maximum_flow_fraction_during_reheat                        write "Autocalculate"
#:
#: The schema is well formed: measured across all 17 bundled versions, no field declares a
#: non-numeric string default on a numeric type with no string branch. It is simply stricter about
#: WHICH sentinel belongs where than EnergyPlus is. Reading each field's enum literally produced
#: 3,775 findings across the 760 example files of one release, every one against a model EnergyPlus
#: reads without complaint.
#:
#: A parse finding says the value is not of the kind the field takes. Whether the exact sentinel is
#: the one THIS field documents is a schema-conformance question, and `validate_document` already
#: answers it: it reports these as E003. Duplicating that here, less accurately, would make the
#: parse diagnostic noise and teach a reader to ignore it.
_SIZING_SENTINELS: Final = SIZING_SENTINELS


def _string_is_legal(obj_schema: dict[str, Any] | None, field_name: str, value: str) -> bool:
    """Whether *value*, a string the numeric coercion rejected, is legal for this field anyway.

    Two things make a string legal. Either it is a sizing sentinel, which any numeric field takes
    whatever its own enum says (see :data:`_SIZING_SENTINELS`), or the field declares an
    ``anyOf`` whose string branch admits it.

    Consulted only when coercion has already failed, so the parse path pays nothing for it.
    """
    if value.casefold() in _SIZING_SENTINELS:
        return True
    if obj_schema is None:
        return True

    pattern_properties = cast("dict[str, Any]", obj_schema.get("patternProperties") or {})
    empty: dict[str, Any] = {}
    body = cast("dict[str, Any]", next(iter(pattern_properties.values()), empty) or empty)
    properties = cast("dict[str, Any]", body.get("properties") or {})
    field = properties.get(field_name)
    if not isinstance(field, dict):
        # No schema for the field is not evidence against the value.
        return True

    branches = cast("dict[str, Any]", field).get("anyOf")
    if not isinstance(branches, list):
        return False

    folded = value.casefold()
    for raw_branch in cast("list[Any]", branches):
        if not isinstance(raw_branch, dict):
            continue
        branch = cast("dict[str, Any]", raw_branch)
        if branch.get("type") != "string":
            continue
        allowed = branch.get("enum")
        if not isinstance(allowed, list) or not allowed:
            # A string branch with no enum accepts any string.
            return True
        return any(isinstance(a, str) and a.casefold() == folded for a in cast("list[Any]", allowed))

    return False


def _swallowed_field_name(pc: ParsingCache, index: int) -> str:
    """Name the field at *index* in an object's raw values, extensible fields included.

    A value past the fixed fields is named by its extensible field and group, such as
    ``'vertex_z_coordinate (vertices item 4)'``, since that is where a ``;`` most often goes missing.
    """
    if pc.has_name:
        if index == 0:
            return "name"
        index -= 1
    field_names = pc.field_names if pc.has_name else pc.all_field_names
    if index < len(field_names):
        return field_names[index]
    ext_index = index - len(field_names)
    if pc.extensible and pc.ext_size > 0 and pc.ext_field_names:
        group, slot = divmod(ext_index, pc.ext_size)
        if slot < len(pc.ext_field_names):
            return f"{pc.ext_field_names[slot]} ({pc.ext_wrapper_key or 'extensible'} item {group + 1})"
    return f"field {index + 1 + (1 if pc.has_name else 0)}"


def _field_offset(fields_raw: str, index: int) -> int | None:
    """Character offset in *fields_raw* where field *index* begins, or None if it runs out.

    Walks the text the way :meth:`IDFParser._parse_fields` does, stepping over ``!`` comments so a
    comma inside one is not counted as a separator. Only called when a finding is being built, so
    the cost lands on the malformed object rather than on every field of every object.
    """
    position = 0
    length = len(fields_raw)
    offset = 0
    while offset < length:
        char = fields_raw[offset]
        if char == "!":
            newline = fields_raw.find("\n", offset)
            if newline < 0:
                break
            offset = newline + 1
            continue
        if char == ",":
            position += 1
            offset += 1
            if position == index:
                while offset < length and fields_raw[offset].isspace():
                    offset += 1
                return offset
            continue
        offset += 1

    return None if index else 0


# No slots=True, as for MigrationReport: on Python 3.10 a frozen dataclass rebuilt with slots cannot
# be constructed through a subscripted alias (ParseResult[X](...)), because the alias sets
# __orig_class__ and the generated __setattr__'s super() refers to the class before rebuild.
@dataclass(frozen=True)
class ParseResult(Generic[_DocT]):
    """A document, and the recoverable findings from the parse that produced it.

    What `load_idf_with_diagnostics` hands back. The findings here are the ones that did NOT stop
    the parse: a skipped unknown type, a malformed object, a formatting tree that could not be
    linked. The ones that did stop it never reach this type, because there is no document to pair
    them with; they arrive on `IDFParseError.diagnostics` instead.

    Field names match the other language's `ParseResult` exactly, so a reader moving between the
    two reads the same two names in the same order.

    Generic in the document's type: ``ParseResult`` alone carries an ``AnyIDFDocument``, since a
    file's release is known only once it is read, and
    ``load_idf_with_diagnostics(path, as_type=IDFDocumentV9_4)`` returns a
    ``ParseResult[IDFDocumentV9_4]``.
    """

    document: _DocT
    diagnostics: tuple[ParseDiagnostic, ...]


def parse_idf(
    filepath: Path | str,
    schema: EpJSONSchema | None = None,
    version: tuple[int, int, int] | None = None,
    encoding: str | None = None,
    strict_parsing: bool = True,
    strict: bool = True,
    *,
    preserve_formatting: bool = False,
    normalize_choices: bool = True,
) -> IDFDocument:
    """
    Parse an IDF file into an IDFDocument.

    Args:
        filepath: Path to the IDF file
        schema: Optional EpJSONSchema for field ordering and type coercion
        version: Optional version override (auto-detected if not provided)
        encoding: File encoding. ``None`` (the default) reads the file as UTF-8 when its bytes
            are valid UTF-8, and as latin-1 otherwise. A leading UTF-8 byte-order mark is dropped.
            The document remembers the encoding, and :func:`~idfkit.writers.save_idf` writes it
            back unless told otherwise.
        strict_parsing: If True, fail fast on malformed objects (default: True)
        strict: When ``True``, accessing or setting an unknown field name on any
            IDFObject raises :class:`~idfkit.exceptions.InvalidFieldError` instead
            of returning ``None``, and assigning a value the schema refuses raises
            :class:`~idfkit.exceptions.ValidationFailedError`, as ``add()`` does.
        preserve_formatting: If ``True``, build a Concrete Syntax Tree (CST)
            so that writing the document back preserves original formatting,
            comments, and whitespace for unmodified objects.  The default
            code path is unchanged — no performance penalty when ``False``.
        normalize_choices: When ``True`` (the default), each choice value is stored in the
            spelling its schema declares, whatever case the file used: ``WALL`` reads back
            ``"Wall"``, as the field's ``Literal`` type says. ``False`` keeps the file's text.
            Either way, a ``preserve_formatting=True`` write emits unmodified objects verbatim.

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

        Round-trip an IDF file losslessly:

            ```python
            model = parse_idf("building.idf", preserve_formatting=True)
            # write_idf(model) reproduces the original byte-for-byte
            ```
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"IDF file not found: {filepath}")  # noqa: TRY003

    parser = IDFParser(filepath, schema, encoding, strict_parsing=strict_parsing)
    return parser.parse(
        version, strict=strict, preserve_formatting=preserve_formatting, normalize_choices=normalize_choices
    )


def parse_idf_with_diagnostics(
    filepath: Path | str,
    schema: EpJSONSchema | None = None,
    version: tuple[int, int, int] | None = None,
    encoding: str | None = None,
    *,
    strict: bool = True,
    preserve_formatting: bool = False,
    normalize_choices: bool = True,
) -> ParseResult[IDFDocument]:
    """Parse an IDF file, keeping the findings that did not stop the parse.

    The same work `parse_idf(..., strict_parsing=False)` does, handing back the recoverable
    findings alongside the document instead of only announcing them through the logging module.

    `strict_parsing` is not a parameter: a strict parse has no recoverable findings by definition,
    so this function always parses non-strictly. Findings that stop a parse still raise, and still
    arrive on `IDFParseError.diagnostics`.

    Every logging announcement fires exactly as it does today. A caller with a handler installed
    sees no change (FR-014); this is a second way to reach the same findings, not a replacement.

    `encoding` and `normalize_choices` are the parameters of :func:`parse_idf`.
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"IDF file not found: {filepath}")  # noqa: TRY003

    parser = IDFParser(filepath, schema, encoding, strict_parsing=False)
    document = parser.parse(
        version, strict=strict, preserve_formatting=preserve_formatting, normalize_choices=normalize_choices
    )
    return ParseResult(document=document, diagnostics=parser.diagnostics)


class IDFParser:
    """
    Streaming parser for IDF files.

    Uses memory mapping for large files and regex for tokenization.
    """

    __slots__ = (
        "_content",
        "_diagnostics",
        "_encoding",
        "_filepath",
        "_normalize_choices",
        "_requested_encoding",
        "_schema",
        "_strict_parsing",
    )

    _filepath: Path
    _schema: EpJSONSchema | None
    #: The codec the parse in progress decodes with: the requested one, else the detected one.
    _encoding: str
    #: The codec the caller asked for, or ``None`` to detect it from each file's bytes.
    _requested_encoding: str | None
    _content: bytes | None
    _strict_parsing: bool
    _diagnostics: list[ParseDiagnostic]
    #: Whether the parse in progress stores choices in their schema's spelling; set by :meth:`parse`.
    _normalize_choices: bool

    def __init__(
        self,
        filepath: Path,
        schema: EpJSONSchema | None = None,
        encoding: str | None = None,
        strict_parsing: bool = True,
    ):
        self._filepath = filepath
        self._schema = schema
        self._requested_encoding = encoding
        self._encoding = encoding or "latin-1"
        self._strict_parsing = strict_parsing
        self._normalize_choices = True
        self._content: bytes | None = None
        # Recoverable findings from the last parse: the ones that did not stop it.
        #
        # These have always been produced; they went to the logging module and nowhere else, so a
        # caller who wanted them had to install a handler before parsing. They are collected here
        # too, so `load_idf_with_diagnostics` can hand them back in one call. Every logging
        # announcement still fires exactly as it did (FR-014); this adds a second way to reach the
        # same findings and removes none.
        self._diagnostics = []

    @property
    def diagnostics(self) -> tuple[ParseDiagnostic, ...]:
        """Recoverable findings from the most recent parse, in the order they were noticed."""
        return tuple(self._diagnostics)

    def _record(
        self,
        message: str,
        *,
        code: ParseDiagnosticCode,
        obj_type: str | None = None,
        obj_name: str | None = None,
        content: bytes | None = None,
        offset: int | None = None,
    ) -> None:
        """Note a recoverable finding, resolving its position while the offset is still in hand.

        The position has to be captured here rather than recovered later. The aggregate site used
        to reduce its findings to a set of type names before warning, which threw away every offset
        it had, and a finding with no position is not the finding the other language returns.
        """
        line: int | None = None
        column: int | None = None
        if content is not None and offset is not None:
            line, column = self._line_and_column(content, offset)
        self._diagnostics.append(
            ParseDiagnostic(
                message=message,
                filepath=str(self._filepath),
                obj_type=obj_type,
                obj_name=obj_name,
                line=line,
                column=column,
                code=code,
            )
        )

    def parse(
        self,
        version: tuple[int, int, int] | None = None,
        *,
        strict: bool = True,
        preserve_formatting: bool = False,
        normalize_choices: bool = True,
    ) -> IDFDocument:
        """
        Parse the IDF file into an IDFDocument.

        Args:
            version: Optional version override
            strict: Enforce strict field access on the resulting document.
            preserve_formatting: Build a CST for lossless round-tripping.
            normalize_choices: Store each choice value in the spelling its schema declares.

        Returns:
            Parsed IDFDocument
        """
        t0 = time.perf_counter()
        # A parser may be reused, and findings belong to one parse rather than to its whole life.
        self._diagnostics = []
        self._normalize_choices = normalize_choices
        logger.debug("Parsing IDF file %s", self._filepath)

        # Load content (with mmap for large files)
        content, self._encoding, source_encoding = _resolve_encoding(self._load_content(), self._requested_encoding)
        if _EPJSON_START.match(content):
            raise FileFormatError(str(self._filepath), "epjson")

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
        doc = IDFDocument(
            version=version,
            schema=schema,
            filepath=self._filepath,
            strict=strict,
            normalize_choices=normalize_choices,
        )
        doc._source_encoding = source_encoding

        # Parse objects
        self._parse_objects(content, doc, schema)

        # Build CST for lossless round-tripping (opt-in, no cost when False)
        if preserve_formatting:
            original_text = content.decode(self._encoding)
            cst = _build_idf_cst(original_text)
            cst.encoding = source_encoding
            if _link_cst_to_objects(cst, doc, self._diagnostics, str(self._filepath)):
                doc._cst = cst  # pyright: ignore[reportAttributeAccessIssue]
                doc._raw_text = original_text  # pyright: ignore[reportAttributeAccessIssue]
            else:
                logger.warning("CST discarded due to linking failure — lossless round-trip disabled")
                # No position: the failure is a property of the whole tree, not of one place in it.
                self._record(
                    "CST discarded due to linking failure, lossless round-trip disabled",
                    code="ParseError",
                )

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
        # Search the whole file. ``content`` is already in memory, so a window
        # saves nothing here and costs correctness: nothing in the format puts
        # the Version object near the top, and three of the example files
        # shipped with EnergyPlus 26.1.0 carry it past the first 10 KB.
        match = _search_version(content)
        if match:
            major = int(match.group(1))
            minor = int(match.group(2))
            patch = int(match.group(3)) if match.group(3) else 0
            return (major, minor, patch)

        raise VersionNotFoundError(str(self._filepath))

    def _parse_objects(
        self,
        content: bytes,
        doc: AnyIDFDocument,
        schema: EpJSONSchema | None,
    ) -> None:
        """Parse all objects from content into document."""
        # Strip comments before matching to prevent phantom objects
        # (e.g. "!- X,Y,Z Origin" matching "X," as an object type)
        content = _COMMENT_PATTERN.sub(b"", content)

        # Local per-type caches avoid repeated schema lookups
        type_cache: dict[str, ParsingCache | None] = {}
        canonical_cache: dict[str, str] = {}
        encoding = self._encoding
        # Values are normalized while the fields are read, so objects are filed as they are.
        addidfobject = doc._adopt  # pyright: ignore[reportPrivateUsage]
        skipped_types: set[str] = set()

        # Every match ends at a `;`, so nothing past the last one can match. Bounding the scan there
        # keeps the scanner off the unterminated tail, which is reported on its own below.
        end = content.rfind(b";") + 1

        for match in _OBJECT_PATTERN.finditer(content, 0, end):
            match_offset = match.start(1)
            obj_type: str | None = None
            obj_name: str | None = None

            try:
                decoded_obj_type = match.group(1).decode(encoding).strip()
                obj_type = decoded_obj_type

                obj_name = self._extract_object_name(match, encoding)

                pc, should_skip, decoded_obj_type = self._resolve_type_cache(
                    content=content,
                    schema=schema,
                    type_cache=type_cache,
                    canonical_cache=canonical_cache,
                    skipped_types=skipped_types,
                    obj_type=decoded_obj_type,
                    obj_name=obj_name,
                    match_offset=match_offset,
                )
                if should_skip:
                    continue

                obj = self._parse_object_cached(match, pc, encoding, obj_type_override=decoded_obj_type, schema=schema)
                if obj:
                    addidfobject(obj)
            except IDFParseError:
                raise
            except Exception as exc:
                if self._strict_parsing:
                    self._raise_parse_error(
                        content,
                        match_offset,
                        f"Failed to parse object: {exc}",
                        obj_type=obj_type,
                        obj_name=obj_name,
                    )
                logger.warning("Skipping malformed object %r: %s", obj_type or "<decode_error>", exc)
                self._record(
                    f"Skipping malformed object: {exc}",
                    code="ParseError",
                    obj_type=obj_type,
                    obj_name=obj_name,
                    content=content,
                    offset=match_offset,
                )

        if skipped_types:
            logger.warning(
                "Skipped %d unknown object type(s): %s", len(skipped_types), ", ".join(sorted(skipped_types))
            )

        self._check_unterminated_tail(content, end, encoding)

    def _check_unterminated_tail(self, content: bytes, end: int, encoding: str) -> None:
        """Report text after the last ``;`` that is not blank, which is an object missing its ``;``.

        The object pattern only matches text that reaches a semicolon, so such an object used to be
        discarded without a word (idfkit#187). *content* has had its comments stripped already, so
        a trailing comment is blank here, and offsets still give the original line numbers.
        """
        tail = content[end:]
        stripped = tail.lstrip(_TRAILING_BLANK)
        if not stripped.rstrip(_TRAILING_BLANK):
            return

        offset = end + len(tail) - len(stripped)
        # A truncated file can end inside a multibyte character, so decoding must not raise here:
        # that would replace the finding with a UnicodeDecodeError, even on the returning path.
        type_match = _TAIL_TYPE_PATTERN.match(stripped)
        obj_type = type_match.group(1).decode(encoding, errors="replace").strip() if type_match else None
        # Only a few bytes per quoted character are needed; the tail may be most of the file.
        head = stripped[: _UNTERMINATED_EXCERPT * 8].decode(encoding, errors="replace")
        excerpt = " ".join(head.split())
        if len(excerpt) > _UNTERMINATED_EXCERPT or len(stripped) > _UNTERMINATED_EXCERPT * 8:
            excerpt = excerpt[:_UNTERMINATED_EXCERPT] + "..."
        message = f'Unterminated object near "{excerpt}" (missing ";")'

        if self._strict_parsing:
            self._raise_parse_error(content, offset, message, obj_type=obj_type)
        logger.warning("Skipping unterminated object %r: %s", obj_type or "<unknown>", message)
        self._record(message, code="ParseError", obj_type=obj_type, content=content, offset=offset)

    def _parse_object_cached(
        self,
        match: re.Match[bytes],
        pc: ParsingCache | None,
        encoding: str,
        *,
        obj_type_override: str | None = None,
        schema: EpJSONSchema | None = None,
    ) -> IDFObject | None:
        """Parse a single object from regex match using cached metadata.

        *schema* names the object types a value running onto the next line is checked against.
        """
        obj_type = obj_type_override or match.group(1).decode(encoding).strip()
        fields_raw = match.group(2).decode(encoding)

        fields = self._parse_fields(fields_raw)
        if not fields:
            return None

        swallowed: int | None = None
        if pc is not None and schema is not None and _VALUE_THEN_LINE_BREAK.search(fields_raw) is not None:
            swallowed = self._check_swallowed_object(match, fields_raw, encoding, obj_type, fields, pc, schema)

        if pc is not None:
            has_name = pc.has_name
            # Mutable copy since extensible parsing appends to it
            field_names: list[str] = list(pc.field_names) if has_name else list(pc.all_field_names)

            name, remaining_fields = (fields[0], fields[1:]) if has_name else ("", fields)

            invalid: list[tuple[int, str, str]] = []
            data = self._build_data_dict_cached(remaining_fields, field_names, pc, invalid)
            if invalid and swallowed is not None:
                # The values from the swallowed one on are the lost object's, read into this one's
                # fields; the missing ';' was reported once already, so they are not reported again.
                invalid = [entry for entry in invalid if entry[0] + (1 if has_name else 0) < swallowed]
            if invalid:
                self._report_invalid_fields(match, fields_raw, encoding, obj_type, fields, pc, invalid)

            return IDFObject(
                obj_type=obj_type,
                name=name,
                data=data,
                schema=pc.obj_schema,
                field_order=field_names,
                ref_fields=pc.ref_fields,
                extensibles=frozenset(pc.ext_field_names),
                wrapper_key=pc.ext_wrapper_key,
                ext_inner_names=tuple(pc.ext_inner_props.keys()),
                aliases=pc.field_aliases,
            )

        # No-schema fallback
        name = fields[0] if fields else ""
        remaining = fields[1:]
        data: dict[str, Any] = {}
        for i, value in enumerate(remaining):
            if value:
                data[f"field_{i + 1}"] = value
        return IDFObject(obj_type=obj_type, name=name, data=data)

    def _check_swallowed_object(
        self,
        match: re.Match[bytes],
        fields_raw: str,
        encoding: str,
        obj_type: str,
        fields: list[str],
        pc: ParsingCache,
        schema: EpJSONSchema,
    ) -> int | None:
        """Report a value that runs onto a line starting with an object type: a missing ``;``.

        ``Zone, A, 0, 0, 0`` followed by ``Material, M;`` reads as one Zone whose y origin is
        ``"0\nMaterial"``, and the Material is lost. The finding never stops the parse, in either mode:
        a line break inside a value is legal (``My`` then ``Zone,`` is the one name ``"My Zone"``), so
        the object is kept as read, a warning is logged, and a ``ParseError`` diagnostic is recorded,
        which :func:`~idfkit.load_idf_with_diagnostics` returns.

        Returns the index in *fields* of the value reported, or ``None`` when there is none.
        """
        for index, value in enumerate(fields):
            if "\n" not in value:
                continue
            before, _, after = value.partition("\n")
            next_type = next((line.strip() for line in after.split("\n") if line.strip()), "")
            if schema.resolve_type_name(next_type) is None:
                continue
            field_name = _swallowed_field_name(pc, index)
            message = (
                f"Field {field_name!r} runs onto the next line, which starts with {next_type!r}: "
                f"missing ';' after {before.strip()!r}, before {next_type!r}?"
            )
            offset = _field_offset(fields_raw, index)
            prefix = 0 if offset is None else len(fields_raw[:offset].encode(encoding))
            position = match.start(2) + prefix
            # When the name itself ran on, the object's name is the part before the line break.
            obj_name = (before.strip() if index == 0 else fields[0]) if pc.has_name else None
            logger.warning("Possible missing ';' in %s %r: %s", obj_type, obj_name, message)
            self._record(
                message, code="ParseError", obj_type=obj_type, obj_name=obj_name, content=match.string, offset=position
            )
            return index
        return None

    def _report_invalid_fields(
        self,
        match: re.Match[bytes],
        fields_raw: str,
        encoding: str,
        obj_type: str,
        fields: list[str],
        pc: ParsingCache,
        invalid: list[tuple[int, str, str]],
    ) -> None:
        """Report values the schema declares numeric that are neither numeric nor a legal sentinel.

        Never raises, in either mode. A value of the wrong kind does not stop the parse: the object
        is built and the document is returned, so a caller who was reading strictly still gets what
        they got before (FR-014). This adds a finding where there was silence, and nothing else.

        The finding is positioned at the offending FIELD rather than at the object, because that is
        what makes it useful: the shape this catches is a missing semicolon swallowing the object
        below, and the object's own first line is nowhere near the damage.
        """
        name_offset = 1 if pc.has_name else 0
        for index, field_name, value in invalid:
            if _string_is_legal(pc.obj_schema, field_name, value):
                continue

            offset = _field_offset(fields_raw, index + name_offset)
            prefix = 0 if offset is None else len(fields_raw[:offset].encode(encoding))
            position = match.start(2) + prefix

            self._record(
                f"Field {field_name!r} expects a number, got {value!r}",
                code="InvalidField",
                obj_type=obj_type,
                obj_name=fields[0] if pc.has_name and fields else None,
                content=match.string,
                offset=position,
            )

    def _build_data_dict_cached(
        self,
        remaining_fields: list[str],
        field_names: list[str],
        pc: ParsingCache,
        invalid: list[tuple[int, str, str]] | None = None,
    ) -> dict[str, Any]:
        """Build the data dict using pre-computed field types from the cache.

        *invalid* collects ``(index, field name, value)`` for each value the schema declares numeric
        that did not coerce. It is almost always empty, and detecting that costs one identity test
        and one frozenset lookup per field: ``_coerce_value_fast`` returns a NEW object when it
        succeeds and hands back the very string it was given when it fails, so ``is`` separates the
        two without re-parsing anything.

        Whether such a value is actually wrong is not decided here. A numeric field routinely
        accepts ``autosize``; that question needs the schema and is asked on the reporting path.

        A value left a string is, when it folds to one of its field's choices, stored in the
        spelling the schema declares, so the field's ``Literal`` type holds for any file. The
        same identity test confines that lookup to strings: a coerced number never pays for it.
        """
        data: dict[str, Any] = {}
        field_types = pc.field_types
        num_named = len(field_names)
        choices = pc.choice_spellings if self._normalize_choices else None

        # zip stops at the named fields: the extensible tail is bucketed below, not walked here.
        for i, (field_name, value) in enumerate(zip(field_names, remaining_fields, strict=False)):
            # A blank field is unset and stays absent, as in epJSON and as the extensible groups below
            # already do. Holding it as "" made the model disagree with both writers, which drop it,
            # so a re-parse of idfkit's own output was not equal to the original (idfkit#183).
            if value:
                field_type = field_types.get(field_name)
                coerced = _coerce_value_fast(field_type, value)
                if coerced is value:
                    if invalid is not None and field_type in _NUMERIC_FIELD_TYPES:
                        invalid.append((i, field_name, value))
                    if choices and (table := choices.get(field_name)) is not None:
                        coerced = table.get(value.casefold(), value)
                data[field_name] = coerced

        if len(remaining_fields) > num_named:
            extra = remaining_fields[num_named:]
            if pc.extensible:
                self._append_extensible_fields(
                    data=data,
                    extra=extra,
                    field_names=field_names,
                    field_types=field_types,
                    pc=pc,
                )
            elif self._strict_parsing and any(extra):
                # Trailing blanks past the last field are unset, like any other blank field, and are
                # not extra values: EnergyPlus accepts ``Timestep,4,,;`` and refuses ``Timestep,4,5;``.
                # It is also how idfkit writes an object with nothing in it to keep its terminator,
                # ``GroundHeatTransfer:Slab:XFACE,;``. Only the values up to the last non-blank one
                # are counted as extra.
                overflow = len(extra) - next(i for i, value in enumerate(reversed(extra)) if value)
                msg = (
                    f"Object has {overflow} extra field(s) but type is not extensible "
                    f"(expected at most {num_named}, got {num_named + overflow})"
                )
                raise ValueError(msg)

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
        """Bucket extensible-group tokens into a canonical wrapper array.

        Tokens are split into ``ext_size``-wide groups; each group becomes
        a dict keyed by the schema's inner property names, and the resulting
        list is stored under ``data[wrapper_key]`` (e.g. ``data["vertices"]``).
        The wrapper key is *not* added to ``field_names`` — the IDF writer
        handles wrapper expansion separately via the schema cache.
        """
        ext_size = pc.ext_size
        if ext_size <= 0:
            if self._strict_parsing:
                msg = "Object is marked extensible but extensible group size is invalid"
                raise ValueError(msg)
            return

        ext_names = pc.ext_field_names
        num_ext = len(ext_names)
        ext_types = tuple(field_types.get(name) for name in ext_names)
        wrapper_key = pc.ext_wrapper_key
        ext_choices = pc.ext_choice_spellings if self._normalize_choices else None

        items: list[dict[str, Any]] = []
        for group_start in range(0, len(extra), ext_size):
            group = extra[group_start : group_start + ext_size]
            # A blank slot is absent rather than "", as in epJSON; the IDF writer restores it (idfkit#182).
            item: dict[str, Any] = {
                ext_names[j]: _coerce_value_fast(ext_types[j], value)
                for j, value in enumerate(group[:num_ext])
                if value
            }
            # Drop all-empty groups (e.g. an extra "," at the end of the extensible block).
            # Keeping them would emit phantom vertices.
            if item:
                if ext_choices:
                    for name, value in item.items():
                        table = ext_choices.get(name)
                        if table is not None and type(value) is str:
                            item[name] = table.get(value.casefold(), value)
                items.append(item)

        if items and wrapper_key is not None:
            data[wrapper_key] = items

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
        code: ParseDiagnosticCode = "ParseError",
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
            code=code,
        )
        summary = "Failed to parse IDF"
        raise IDFParseError(summary, diagnostics=[diagnostic])

    def _resolve_type_cache(
        self,
        *,
        content: bytes,
        schema: EpJSONSchema | None,
        type_cache: dict[str, ParsingCache | None],
        canonical_cache: dict[str, str],
        skipped_types: set[str],
        obj_type: str,
        obj_name: str | None,
        match_offset: int,
    ) -> tuple[ParsingCache | None, bool, str]:
        """Resolve and cache parsing metadata for an object type.

        Returns ``(cache, should_skip, canonical_type)`` where *canonical_type*
        is the PascalCase schema name (may differ from the raw IDF casing).
        """
        if schema is None:
            return (None, False, obj_type)

        pc = type_cache.get(obj_type)
        if pc is None and obj_type not in type_cache:
            pc = schema.get_parsing_cache(obj_type)
            type_cache[obj_type] = pc

        if pc is not None:
            # Return cached canonical name (resolved once per raw type).
            canonical = canonical_cache.get(obj_type)
            if canonical is None:
                canonical = schema.resolve_type_name(obj_type) or obj_type
                canonical_cache[obj_type] = canonical
            return (pc, False, canonical)

        if self._strict_parsing:
            # The same code the recoverable path below uses, and the same one the other language
            # reports for this input. A finding must not change kind depending on which mode was
            # asked for: it is the same finding, arriving on a different path.
            msg = f"Unknown object type '{obj_type}'"
            self._raise_parse_error(
                content,
                match_offset,
                msg,
                obj_type=obj_type,
                obj_name=obj_name,
                code="UnknownObjectType",
            )

        # One finding per skip, positioned, and recorded HERE rather than after the loop.
        #
        # `skipped_types` is a set and stays one, because the log line it feeds is a summary and
        # changing it would change what an existing caller sees. But a set of type names is not
        # what the other language returns: it collapses four skips of the same type into one and
        # discards every offset. The offset is in hand at exactly this point and nowhere later,
        # which is why the finding is built here.
        self._record(
            f"Unknown object type '{obj_type}'",
            code="UnknownObjectType",
            obj_type=obj_type,
            obj_name=obj_name,
            content=content,
            offset=match_offset,
        )
        skipped_types.add(obj_type)
        return (None, True, obj_type)


def iter_idf_objects(
    filepath: Path | str,
    encoding: str | None = None,
) -> Iterator[tuple[str, str, list[str]]]:
    """
    Iterate over objects in an IDF file without loading into document.

    Yields:
        Tuples of (object_type, name, [field_values])

    This is useful for quick scanning or filtering without full parsing.
    ``encoding`` is read as :func:`parse_idf` reads it: ``None`` detects UTF-8 or latin-1.

    Note:
        Type names are returned exactly as they appear in the IDF file
        (no schema-based case normalization).  Use case-insensitive
        comparisons when filtering: ``obj_type.upper() == "ZONE"``.

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
    content, encoding, _ = _resolve_encoding(content, encoding)

    # Strip comments before matching to prevent phantom objects
    content = _COMMENT_PATTERN.sub(b"", content)

    # As in `IDFParser._parse_objects`: no match reaches past the last `;`, and scanning an
    # unterminated tail costs time quadratic in its length for nothing (idfkit#187).
    end = content.rfind(b";") + 1
    if content[end:].strip(_TRAILING_BLANK):
        logger.warning('Ignoring unterminated object at the end of %s (missing ";")', filepath)

    for match in _OBJECT_PATTERN.finditer(content, 0, end):
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

    Reads the first 10 KB of the file, which holds the ``Version`` object in
    almost every model, and falls back to reading the rest only when it does
    not. The common case costs one small read; no valid file is refused for
    stating its version late. Nothing in the IDF format requires ``Version``
    to appear near the top, and three of the example files shipped with
    EnergyPlus 26.1.0 carry it past 10 KB.

    Args:
        filepath: Path to IDF file

    Returns:
        Version tuple (major, minor, patch)

    Raises:
        VersionNotFoundError: If the file holds no Version object

    Examples:
        Check which EnergyPlus version a model was created for
        (usually reads only the first 10 KB):

            ```python
            from idfkit import get_idf_version

            version = get_idf_version("5ZoneAirCooled.idf")
            print(f"EnergyPlus v{version[0]}.{version[1]}.{version[2]}")
            ```
    """
    filepath = Path(filepath)

    with open(filepath, "rb") as f:
        head = f.read(_VERSION_SCAN_BYTES)
        # A comment's `!` precedes its text, so the window holds it whenever it holds the text.
        match = _search_version(head)
        if match is None:
            # The scan window may have split the Version object, so re-search
            # the whole file rather than only the remainder.
            match = _search_version(head + f.read())

    if match:
        major = int(match.group(1))
        minor = int(match.group(2))
        patch = int(match.group(3)) if match.group(3) else 0
        return (major, minor, patch)

    raise VersionNotFoundError(str(filepath))


# ---------------------------------------------------------------------------
# CST (Concrete Syntax Tree) helpers for lossless round-tripping
# ---------------------------------------------------------------------------


def _build_idf_cst(text: str) -> DocumentCST:
    """Build a :class:`DocumentCST` from the original IDF source text.

    The returned CST is a flat list of :class:`CSTNode` items whose ``text``
    attributes, when concatenated, reproduce *text* exactly.  Nodes that
    correspond to IDF objects are distinguished from pure-text nodes
    (comments, blank lines, preamble) so that the writer can substitute
    freshly formatted output for mutated objects while keeping everything
    else verbatim.

    Performance: single-pass regex scanner using :data:`_CST_OBJECT_RE`.
    """
    nodes: list[CSTNode] = []
    pos = 0
    for m in _CST_OBJECT_RE.finditer(text):
        if m.group(1) is None:
            continue  # Comment match — will be part of surrounding text node
        if m.start() > pos:
            nodes.append(CSTNode(text=text[pos : m.start()]))
        nodes.append(CSTNode(text=m.group(1)))
        pos = m.end()
    if pos < len(text):
        nodes.append(CSTNode(text=text[pos:]))
    return DocumentCST(nodes=nodes)


def _link_cst_to_objects(
    cst: DocumentCST,
    doc: AnyIDFDocument,
    diagnostics: list[ParseDiagnostic] | None = None,
    filepath: str | None = None,
) -> bool:
    """Link object :class:`CSTNode` items to their parsed :class:`IDFObject`.

    The CST preserves file order while ``doc.all_objects`` groups objects by
    type.  Within each type the collection preserves insertion (= file) order,
    so we build a ``type_upper → deque[IDFObject]`` map and pop the next
    object of the matching type for each CST node.

    The ``Version`` object is kept as an unlinked node because the parser
    handles it separately.

    Each linked object also receives its original source text via
    ``_source_text`` for mutation tracking.

    Returns ``True`` if linking succeeded, ``False`` if a CST object node
    could not be matched to any parsed object.
    """
    from collections import deque

    # Build type_upper → deque[IDFObject] from document collections.
    # Each collection's _items list preserves insertion (= file) order.
    obj_by_type: dict[str, deque[IDFObject]] = {}
    for obj_type, collection in doc.collections.items():
        if collection:
            obj_by_type[obj_type.upper()] = deque(collection)

    linked = 0

    for node in cst.nodes:
        type_name = _cst_node_type_name(node)
        if type_name is None:
            continue

        type_upper = type_name.upper()

        bucket = obj_by_type.get(type_upper)
        if bucket:
            obj = bucket.popleft()
            node.obj = obj
            object.__setattr__(obj, "_source_text", node.text)
            linked += 1
            if not bucket:
                del obj_by_type[type_upper]
        else:
            logger.warning(
                "CST linking: no parsed object for CST node type=%r (strict=False may have skipped objects)",
                type_name,
            )
            # The type name is the whole location available here. The CST node knows its text but
            # not its offset in the original content, so there is no line to give and none is
            # invented; the other language reports the same finding with the same gap.
            if diagnostics is not None:
                diagnostics.append(
                    ParseDiagnostic(
                        message=f"CST linking: no parsed object for CST node type {type_name!r}",
                        filepath=filepath,
                        obj_type=type_name,
                        code="ParseError",
                    )
                )

    total = sum(len(c) for c in doc.collections.values())
    logger.debug("CST linking: %d of %d parsed objects linked", linked, total)
    return True


def _cst_node_type_name(node: CSTNode) -> str | None:
    """Extract the object type name from a CST node, or ``None`` for text-only nodes."""
    m = _CST_TYPE_NAME_RE.match(node.text)
    if m is None:
        return None
    name = m.group(1).strip()
    return name or None
