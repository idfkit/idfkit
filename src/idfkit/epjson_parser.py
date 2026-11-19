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

from .document import AnyIDFDocument, IDFDocument
from .exceptions import FileFormatError, IDFParseError, ParseDiagnostic, VersionNotFoundError, closest_name
from .objects import IDFObject, drop_blank_group_slots, is_blank_slot
from .schema import canonicalize_choices, get_schema_manager

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from collections.abc import Callable

    from .schema import EpJSONSchema, ParsingCache


def parse_epjson(
    filepath: Path | str,
    schema: EpJSONSchema | None = None,
    version: tuple[int, int, int] | None = None,
    strict: bool = True,
    *,
    strict_parsing: bool = True,
    preserve_formatting: bool = False,
    normalize_choices: bool = True,
) -> IDFDocument:
    """
    Parse an epJSON file into an IDFDocument.

    Args:
        filepath: Path to the epJSON file
        schema: Optional EpJSONSchema for validation
        version: Optional version override (auto-detected if not provided)
        strict: When ``True``, accessing or setting an unknown field name on any
            IDFObject raises :class:`~idfkit.exceptions.InvalidFieldError` instead
            of returning ``None``, and assigning a value the schema refuses raises
            :class:`~idfkit.exceptions.ValidationFailedError`, as ``add()`` does.
        strict_parsing: When ``True`` (the default), an object type the schema does not
            have raises :class:`~idfkit.exceptions.IDFParseError`, as :func:`~idfkit.load_idf`
            does, and the message suggests the closest type; EnergyPlus refuses such a file.
            ``False`` skips it with a logged warning.
        preserve_formatting: If ``True``, store the raw JSON text so that
            :func:`~idfkit.writers.write_epjson` and
            :func:`~idfkit.writers.save_epjson` can reproduce it
            byte-for-byte when no objects have been modified.
        normalize_choices: When ``True`` (the default), each choice value is stored in the
            spelling its schema declares, whatever case the file used, as the field's
            ``Literal`` type says. ``False`` keeps the file's text.

    Returns:
        Parsed IDFDocument

    Raises:
        VersionNotFoundError: If version cannot be detected
        IDFParseError: For an object type the schema does not have, with *strict_parsing*
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
    return parser.parse(
        version,
        strict=strict,
        strict_parsing=strict_parsing,
        preserve_formatting=preserve_formatting,
        normalize_choices=normalize_choices,
    )


def _bucket_flat_extensibles(fields_dict: dict[str, Any], pc: ParsingCache) -> dict[str, Any]:
    """Translate flat suffixed extensible keys into the canonical wrapper array.

    Real EnergyPlus epJSON output is canonical, but hand-authored / legacy
    epJSON sometimes uses ``vertex_x_coordinate_2``-style flat keys. This
    helper buckets every flat extensible key it finds into a list of dicts
    under the schema's wrapper key. If the wrapper is already present
    (and is a list), the flat keys are merged into it.
    """
    from .objects import is_blank_slot, parse_extensible_index

    ext_set = frozenset(pc.ext_field_names)
    fixed = frozenset(pc.all_field_names)
    wrapper_key = pc.ext_wrapper_key
    assert wrapper_key is not None  # caller checked  # noqa: S101

    flat_groups: dict[int, dict[str, Any]] = {}
    flat_keys: list[str] = []
    for key in fields_dict:
        if key == wrapper_key:
            continue
        base, idx = parse_extensible_index(key, ext_set, fixed)
        if base is not None:
            if not is_blank_slot(fields_dict[key]):
                flat_groups.setdefault(idx, {})[base] = fields_dict[key]
            flat_keys.append(key)

    if not flat_keys:
        return fields_dict

    out = dict(fields_dict)
    for k in flat_keys:
        del out[k]
    flat_list = [flat_groups[i] for i in sorted(flat_groups)]
    existing = out.get(wrapper_key)
    if isinstance(existing, list):
        # Wrapper present alongside flat keys — append; keeps user-authored
        # mixes deterministic.
        out[wrapper_key] = list(cast("list[Any]", existing)) + flat_list
    else:
        out[wrapper_key] = flat_list
    return out


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

    def parse(
        self,
        version: tuple[int, int, int] | None = None,
        *,
        strict: bool = True,
        strict_parsing: bool = True,
        preserve_formatting: bool = False,
        normalize_choices: bool = True,
    ) -> IDFDocument:
        """
        Parse the epJSON file into an IDFDocument.

        Args:
            version: Optional version override
            strict: Enforce strict field access on the resulting document.
            strict_parsing: Raise on an object type the schema does not have, rather than skip it.
            preserve_formatting: Store raw JSON text for lossless round-tripping.
            normalize_choices: Store each choice value in the spelling its schema declares.

        Returns:
            Parsed IDFDocument
        """
        t0 = time.perf_counter()
        logger.debug("Parsing epJSON file %s", self._filepath)

        # Load JSON
        try:
            with open(self._filepath, encoding="utf-8") as f:
                raw_text = f.read()
            data: dict[str, Any] = json.loads(raw_text, parse_constant=_constant_refuser(self._filepath))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            # IDF text starts with a comment or an object type, never with '{'. An IDF file is often
            # latin-1 (save_idf's default) and so not UTF-8 at all: look at the bytes, not the text.
            with open(self._filepath, "rb") as f:
                head = f.read(4096)
            first = head.removeprefix(b"\xef\xbb\xbf").lstrip(b" \t\r\n")[:1]
            if first == b"!" or first.isalpha():
                raise FileFormatError(str(self._filepath), "idf") from exc
            raise

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
        doc = IDFDocument(
            version=version,
            schema=schema,
            filepath=self._filepath,
            strict=strict,
            normalize_choices=normalize_choices,
        )

        # Parse objects
        self._parse_objects(data, doc, schema, strict_parsing=strict_parsing, normalize_choices=normalize_choices)

        # Store raw text for lossless round-tripping (opt-in).
        if preserve_formatting:
            doc._raw_text = raw_text  # pyright: ignore[reportAttributeAccessIssue]
            # Mark all objects as "pristine" with a sentinel source_text so
            # that the writer can detect mutations.
            for obj in doc.all_objects:
                object.__setattr__(obj, "_source_text", "")
            # How many there were, so that a removal is visible to the writer.
            # The sentinel above only marks the objects that are still here, and
            # a removed one is not among them to ask.
            doc._count_at_read = len(doc)

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
        doc: AnyIDFDocument,
        schema: EpJSONSchema | None,
        *,
        strict_parsing: bool = True,
        normalize_choices: bool = True,
    ) -> None:
        """Parse all objects from epJSON data into document.

        An object type *schema* does not have raises with *strict_parsing*, and is skipped
        without, as the IDF parser treats one.

        With *normalize_choices*, each choice is stored in the spelling its schema declares, as the
        IDF parser stores it. EnergyPlus's own epJSON is already canonical; a hand-written or
        converted file need not be.
        """
        # Values are normalized below while each object is built, so objects are filed as they are.
        addidfobject = doc._adopt  # pyright: ignore[reportPrivateUsage]
        unknown_fields: list[ParseDiagnostic] = []

        for obj_type, objects in data.items():
            if not isinstance(objects, dict):
                continue

            # Get schema info from parsing cache
            pc: ParsingCache | None = None
            obj_schema: dict[str, Any] | None = None
            base_field_names: tuple[str, ...] | None = None
            ref_fields: frozenset[str] | None = None
            has_name = True
            # epJSON format: {"ObjectType": {"obj_name": {fields...}, ...}}
            objects_dict = cast(dict[str, Any], objects)
            if schema:
                pc = schema.get_parsing_cache(obj_type)
                if pc is None:
                    self._unknown_type(obj_type, objects_dict, schema, strict_parsing=strict_parsing)
                    continue
                obj_schema = pc.obj_schema
                has_name = pc.has_name
                base_field_names = pc.field_names if has_name else pc.all_field_names
                ref_fields = pc.ref_fields

            for obj_name, fields in objects_dict.items():
                if not isinstance(fields, dict):
                    continue

                # Nameless objects: use empty string instead of epJSON dict key
                name = obj_name if has_name else ""

                fields_dict = cast(dict[str, Any], fields)

                # Real EnergyPlus epJSON is canonical for extensible types, but
                # hand-authored or legacy epJSON sometimes uses flat suffixed
                # keys (vertex_x_coordinate_2, time_3, ...). Coerce them into
                # the canonical wrapper-array shape so downstream consumers see
                # uniform storage.
                if pc and pc.extensible and pc.ext_wrapper_key and pc.ext_field_names:
                    fields_dict = drop_blank_group_slots(_bucket_flat_extensibles(fields_dict, pc), pc.ext_wrapper_key)

                field_order = list(base_field_names) if base_field_names is not None else None
                # A copy, without blank values ("" or null): a blank field is unset, as in IDF (idfkit#183).
                obj_data = {key: value for key, value in fields_dict.items() if not is_blank_slot(value)}
                if normalize_choices and pc is not None:
                    canonicalize_choices(obj_data, pc)
                if has_name and pc is not None and "name" in obj_data:
                    self._drop_body_name(obj_type, obj_name, obj_data)
                unknown_fields.extend(
                    self._unknown_fields(obj_type, obj_name, obj_data, pc, strict_parsing=strict_parsing)
                )

                obj = IDFObject(
                    obj_type=obj_type,
                    name=name,
                    data=obj_data,
                    schema=obj_schema,
                    field_order=field_order,
                    ref_fields=ref_fields,
                    extensibles=frozenset(pc.ext_field_names) if pc else None,
                    wrapper_key=pc.ext_wrapper_key if pc else None,
                    ext_inner_names=tuple(pc.ext_inner_props.keys()) if pc else (),
                    aliases=pc.field_aliases if pc else None,
                )

                addidfobject(obj)

        _raise_unknown_fields(unknown_fields)

    def _drop_body_name(self, obj_type: str, obj_name: str, obj_data: dict[str, Any]) -> None:
        """Drop a ``name`` key repeated inside a named object's body.

        The object's key is its name; some writers repeat it in the body as well. EnergyPlus reads
        the key, so a body name that differs from it is logged and dropped too.
        """
        body_name = obj_data.pop("name")
        if not isinstance(body_name, str) or body_name.upper() != obj_name.upper():
            logger.warning(
                "%s '%s' in %s repeats a different name, %r, in its body; the key is the name",
                obj_type,
                obj_name,
                self._filepath,
                body_name,
            )

    def _unknown_fields(
        self, obj_type: str, obj_name: str, obj_data: dict[str, Any], pc: ParsingCache | None, *, strict_parsing: bool
    ) -> list[ParseDiagnostic]:
        """The keys of *obj_data* that no release ever had as fields of *obj_type*, one diagnostic each.

        EnergyPlus ignores a key that is not a field, so a misspelt field's value is silently
        lost and the field takes its default. With *strict_parsing* those are returned, to be
        raised; without, each is logged and kept, as before. A field an earlier release had, and
        this one removed, is logged and kept either way: EnergyPlus's own example files carry
        some, and EnergyPlus runs them.
        """
        if pc is None:
            return []
        unknown = [key for key in obj_data if key not in pc.known_keys]
        if not unknown:
            return []
        candidates = (*pc.known_keys, *pc.ext_field_names)
        diagnostics: list[ParseDiagnostic] = []
        for key in unknown:
            if key in get_schema_manager().field_names_in_any_release(obj_type):
                logger.warning(
                    "Field '%s' of %s '%s' in %s is not in this release's schema; EnergyPlus ignores it",
                    key,
                    obj_type,
                    obj_name,
                    self._filepath,
                )
                continue
            message = f"Unknown field '{key}' for {obj_type}"
            suggestion = closest_name(key, candidates)
            if suggestion is not None:
                message += f". Did you mean '{suggestion}'?"
            if not strict_parsing:
                logger.warning("%s in %s [name: %s]; kept as is", message, self._filepath, obj_name)
                continue
            diagnostics.append(
                ParseDiagnostic(
                    message=message,
                    filepath=str(self._filepath),
                    obj_type=obj_type,
                    obj_name=obj_name,
                    code="InvalidField",
                )
            )
        return diagnostics

    def _unknown_type(
        self, obj_type: str, objects: dict[str, Any], schema: EpJSONSchema, *, strict_parsing: bool
    ) -> None:
        """Raise for an object type *schema* does not have, or, without *strict_parsing*, log it."""
        suggestion = closest_name(obj_type, schema.object_types)
        message = f"Unknown object type '{obj_type}'"
        if suggestion is not None:
            message += f". Did you mean '{suggestion}'?"
        if not strict_parsing:
            logger.warning("%s in %s; skipped %d object(s)", message, self._filepath, len(objects))
            return
        diagnostic = ParseDiagnostic(
            message=message,
            filepath=str(self._filepath),
            obj_type=obj_type,
            obj_name=next(iter(objects), None),
            code="UnknownObjectType",
        )
        summary = "Failed to parse epJSON"
        raise IDFParseError(summary, diagnostics=[diagnostic])


def _raise_unknown_fields(diagnostics: list[ParseDiagnostic]) -> None:
    """Raise one [IDFParseError][idfkit.exceptions.IDFParseError] carrying every unknown-field diagnostic, if any."""
    if diagnostics:
        summary = "Failed to parse epJSON"
        raise IDFParseError(summary, diagnostics=diagnostics)


def _constant_refuser(filepath: Path) -> Callable[[str], Any]:
    """A ``parse_constant`` hook refusing ``NaN``, ``Infinity`` and ``-Infinity`` in *filepath*.

    ``json`` reads them, but JSON does not have them and EnergyPlus's epJSON reader stops on them
    with a parse error, so a file holding one would load here and fail there.
    """

    def refuse(constant: str) -> Any:
        msg = (
            f"{filepath}: {constant} is not valid JSON and EnergyPlus refuses it. "
            "Replace it with a number (or remove the field) and load the file again."
        )
        raise ValueError(msg)

    return refuse


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
        return json.load(f, parse_constant=_constant_refuser(filepath))


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
        data = json.load(f, parse_constant=_constant_refuser(filepath))

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
