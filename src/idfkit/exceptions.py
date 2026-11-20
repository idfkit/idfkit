"""Custom exceptions for idfkit."""

from __future__ import annotations

import difflib
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from .objects import IDFObject
    from .simulation.result import SimulationResult


class IdfKitError(Exception):
    """Base exception for all idfkit errors."""

    pass


def closest_names(name: str, candidates: Iterable[str], n: int = 1) -> list[str]:
    """Up to *n* candidates closest to *name*, ignoring case, closest first.

    The one "did you mean" matcher: the unknown-type and unknown-field errors, attribute access
    on a document and ``idfkit check`` all suggest through it, so they agree on a typo.

    Examples:
        >>> closest_names("zoens", ["zones", "zone_lists", "materials"], n=2)
        ['zones']
    """
    by_folded = {candidate.casefold(): candidate for candidate in candidates}
    return [by_folded[close] for close in difflib.get_close_matches(name.casefold(), by_folded.keys(), n=n, cutoff=0.6)]


def closest_name(name: str, candidates: Iterable[str]) -> str | None:
    """The candidate closest to *name*, ignoring case, or ``None`` if none is close.

    The "did you mean" of the unknown-type and unknown-field errors; see `closest_names`.

    Examples:
        >>> closest_name("Zoen", ["Zone", "Material"])
        'Zone'
        >>> closest_name("ceiling_heigth", ["x_origin", "ceiling_height"])
        'ceiling_height'
        >>> closest_name("qwerty", ["Zone"]) is None
        True
    """
    close = closest_names(name, candidates)
    return close[0] if close else None


def _format_subprocess_failure(
    message: str,
    *,
    exit_code: int | None = None,
    stderr: str | None = None,
) -> str:
    """Shared subprocess-failure message formatter.

    Appends ``(exit code N)`` to the first line of *message* and a 500-char-truncated stderr tail
    to the whole.
    """
    msg = message
    if exit_code is not None:
        head, sep, rest = msg.partition("\n")
        msg = f"{head} (exit code {exit_code}){sep}{rest}"
    if stderr:
        msg += f"\nstderr: {stderr.strip()[:500]}"
    return msg


#: The shared diagnostic vocabulary, derived from the exception hierarchy below by dropping the
#: `Error` suffix. Both libraries use these exact spellings, because the conformance corpus compares
#: a parse finding on `(code, line, obj_type)` and never on message text: wording is a presentation
#: choice each library should stay free to improve, and pinning it would turn every improvement into
#: a conformance failure.
#:
#: The table lives in `idfkit-conformance/runners/compare.md`. A code outside it is a difference,
#: not a near match.
ParseDiagnosticCode = Literal[
    "UnknownObjectType",
    "InvalidField",
    "Range",
    "DuplicateObject",
    "ParseError",
    "VersionMismatch",
    "UnsupportedVersion",
    "SchemaNotFound",
]


@dataclass(frozen=True, slots=True)
class ParseDiagnostic:
    """One finding from a parse: what happened, and as much location as was available.

    There is no severity, and there never has been. Whether a finding stopped the parse is told by
    the path it arrives on, `IDFParseError.diagnostics` for the ones that did and
    `ParseResult.diagnostics` for the ones that did not, rather than by a field on the finding.

    `code` is added last so that every existing positional construction keeps working. It reads
    better beside `message` and is not there, deliberately.
    """

    message: str
    filepath: str | None = None
    obj_type: str | None = None
    obj_name: str | None = None
    line: int | None = None
    column: int | None = None
    code: ParseDiagnosticCode = "ParseError"


class IDFParseError(IdfKitError):
    """Raised when parsing IDF/epJSON content fails."""

    diagnostics: tuple[ParseDiagnostic, ...]

    def __init__(self, message: str, diagnostics: Sequence[ParseDiagnostic] | None = None) -> None:
        self.diagnostics = tuple(diagnostics or ())
        if self.diagnostics:
            first = self.diagnostics[0]
            location = "unknown location"
            if first.filepath is not None and first.line is not None and first.column is not None:
                location = f"{first.filepath}:{first.line}:{first.column}"
            elif first.filepath is not None and first.line is not None:
                location = f"{first.filepath}:{first.line}"
            elif first.filepath is not None:
                location = first.filepath
            detail = f"{first.message} ({location})"
            if first.obj_type:
                detail += f" [object: {first.obj_type}]"
            if first.obj_name:
                detail += f" [name: {first.obj_name}]"
            super().__init__(f"{message}: {detail}")
            return
        super().__init__(message)


# Alias for backwards compatibility
ParseError = IdfKitError


class FileFormatError(IDFParseError, ValueError):
    """Raised when a loader is given a file in the other format: epJSON to ``load_idf``, or IDF to ``load_epjson``.

    It is a ``ValueError`` too, as the ``json.JSONDecodeError`` that ``load_epjson`` raised for an
    IDF file was.

    Attributes:
        filepath: The file that was read.
        detected_format: The format the file's content is in, ``"idf"`` or ``"epjson"``.
    """

    def __init__(self, filepath: str, detected_format: Literal["idf", "epjson"]) -> None:
        self.filepath = filepath
        self.detected_format: Literal["idf", "epjson"] = detected_format
        if detected_format == "epjson":
            msg = f"{filepath} looks like an epJSON file (it starts with '{{'), not IDF; use load_epjson() to read it"
        else:
            msg = f"{filepath} looks like an IDF file (it does not start with '{{'), not epJSON; use load_idf() to read it"
        super().__init__(msg)

    def __reduce__(self) -> tuple[type[FileFormatError], tuple[str, Literal["idf", "epjson"]]]:
        # BaseException pickles only self.args, the message; rebuild from the parts instead.
        return (type(self), (self.filepath, self.detected_format))


class UnsupportedVersionError(IdfKitError):
    """Raised when a non-existent EnergyPlus version is requested.

    Attributes:
        version: The requested version tuple.
        supported_versions: Tuple of all supported version tuples.
    """

    def __init__(self, version: tuple[int, int, int], supported_versions: Sequence[tuple[int, int, int]]) -> None:
        self.version = version
        self.supported_versions = tuple(supported_versions)
        version_str = f"{version[0]}.{version[1]}.{version[2]}"
        supported_strs = ", ".join(f"{v[0]}.{v[1]}.{v[2]}" for v in self.supported_versions)
        super().__init__(f"EnergyPlus version {version_str} is not supported.\nSupported versions: {supported_strs}")


class SchemaNotFoundError(IdfKitError):
    """Raised when the EpJSON schema file cannot be found."""

    def __init__(self, version: tuple[int, int, int], searched_paths: list[str] | None = None) -> None:
        self.version = version
        self.searched_paths = searched_paths or []
        version_str = f"{version[0]}.{version[1]}.{version[2]}"
        msg = f"Could not find Energy+.schema.epJSON for EnergyPlus {version_str}"
        if searched_paths:
            msg += f"\nSearched in: {', '.join(searched_paths)}"
        super().__init__(msg)


class DuplicateObjectError(IdfKitError):
    """Raised when attempting to add an object with a duplicate name."""

    def __init__(self, obj_type: str, name: str) -> None:
        self.obj_type = obj_type
        self.name = name
        super().__init__(f"Duplicate {obj_type} object with name '{name}'")


class UnknownObjectTypeError(IdfKitError, KeyError):
    """Raised when an unknown object type is encountered.

    Inherits from ``KeyError`` so that existing code catching ``KeyError``
    for missing object types continues to work. Unlike a plain ``KeyError``,
    ``str()`` gives the message as written, not its ``repr()``.

    Attributes:
        obj_type: The type name that was not found.
        version: The EnergyPlus release it was looked up in, if known.
        suggestion: The closest type name of that release, if one is close.
    """

    def __init__(
        self, obj_type: str, version: tuple[int, int, int] | None = None, suggestion: str | None = None
    ) -> None:
        self.obj_type = obj_type
        self.version = version
        self.suggestion = suggestion
        msg = f"Unknown object type: '{obj_type}'"
        if suggestion is not None:
            msg += f". Did you mean '{suggestion}'?"
        if version:
            from .docs import search_url

            s_url = search_url(obj_type, version)
            if s_url:
                msg += f"\n  Search docs: {s_url.url}"
        self.message = msg
        super().__init__(msg)

    def __str__(self) -> str:
        # KeyError.__str__ gives repr() of its argument: quoted, with a literal "\n".
        return self.message

    def __reduce__(self) -> tuple[type[UnknownObjectTypeError], tuple[str, tuple[int, int, int] | None, str | None]]:
        return (type(self), (self.obj_type, self.version, self.suggestion))


class ObjectNotFoundError(IdfKitError, KeyError):
    """Raised when a document has no object of a type by the name looked up.

    Raised by ``doc["Zone"]["name"]``, ``doc.rename()`` and the dotted ``doc.update()``. Inherits
    from ``KeyError`` so code catching ``KeyError`` keeps working; unlike a plain ``KeyError``,
    ``str()`` gives the message as written, not its ``repr()``.

    Attributes:
        obj_type: The object type that was searched.
        name: The name that was not found.
        suggestions: The closest existing names of that type ("did you mean"), closest first.
        available: The existing names of that type, in document order.
        object_count: How many objects of that type the document has, named or not, if known.

    Examples:
        >>> err = ObjectNotFoundError("Zone", "SPACE1_1", available=["SPACE1-1", "SPACE2-1", "PLENUM-1"])
        >>> print(err)
        No Zone named 'SPACE1_1'. Did you mean 'SPACE1-1'?
          Zone names: SPACE1-1, SPACE2-1, PLENUM-1
        >>> isinstance(err, KeyError)
        True
    """

    #: How many existing names the message lists before it summarises the rest.
    _LISTED_NAMES = 10

    def __init__(
        self,
        obj_type: str,
        name: str,
        available: Sequence[str] | Callable[[], Iterable[str]] = (),
        *,
        object_count: int | None = None,
    ) -> None:
        """Build the error. Nothing is computed until the names or the message are read.

        Args:
            obj_type: The object type that was searched.
            name: The name that was not found.
            available: The existing names of that type, or a callable returning them. A callable
                is only called when ``available``, ``suggestions`` or the message is read, so a
                lookup miss caught as ``KeyError`` costs no more than it did.
            object_count: How many objects of that type the document has, named or not. Defaults
                to the number of names; pass it for types whose objects have no names.
        """
        super().__init__(name)
        self.obj_type = obj_type
        self.name = name
        self._available_source = available
        self._available: tuple[str, ...] | None = None
        self._suggestions: tuple[str, ...] | None = None
        self._message: str | None = None
        self.object_count = object_count

    @property
    def available(self) -> tuple[str, ...]:
        """The existing names of that type, in document order."""
        if self._available is None:
            source = self._available_source
            self._available = tuple(source() if callable(source) else source)
            self._available_source = ()
        return self._available

    @property
    def suggestions(self) -> tuple[str, ...]:
        """The closest existing names of that type ("did you mean"), closest first."""
        if self._suggestions is None:
            self._suggestions = tuple(closest_names(self.name, self.available, n=3)) if self.name else ()
        return self._suggestions

    @property
    def message(self) -> str:
        """The full message ``str()`` gives."""
        if self._message is None:
            self._message = self._build_message()
        return self._message

    def _build_message(self) -> str:
        obj_type, name, available = self.obj_type, self.name, self.available
        msg = f"No {obj_type} named '{name}'" if name else f"No {obj_type} object in the document"
        if self.suggestions:
            msg += f". Did you mean '{self.suggestions[0]}'?"
        count = len(available) if self.object_count is None else self.object_count
        if available:
            listed = ", ".join(available[: self._LISTED_NAMES])
            more = len(available) - self._LISTED_NAMES
            if more > 0:
                listed += f", ... ({more} more)"
            msg += f"\n  {obj_type} names: {listed}"
        elif count:
            plural = "object has" if count == 1 else "objects have"
            msg += f"\n  The document's {count} {obj_type} {plural} no name to look up by."
        elif name:
            msg += f"\n  The document has no {obj_type} objects."
        return msg

    def __str__(self) -> str:
        # KeyError.__str__ gives repr() of its argument: quoted, with a literal "\n".
        return self.message

    def __reduce__(
        self,
    ) -> tuple[type[ObjectNotFoundError], tuple[str, str, tuple[str, ...]], dict[str, int | None]]:
        # The names are materialised here: a callable source need not pickle.
        return (type(self), (self.obj_type, self.name, self.available), {"object_count": self.object_count})


class ResultLookupError(IdfKitError, KeyError):
    """Raised when a simulation-result lookup finds no output, or several where it needs one.

    Raised by [SQLResult.get_timeseries][idfkit.simulation.parsers.sql.SQLResult.get_timeseries],
    [SQLResult.get_tabular_value][idfkit.simulation.parsers.sql.SQLResult.get_tabular_value],
    [ESOResult.get_column][idfkit.simulation.parsers.eso.ESOResult.get_column] and
    [CSVResult.get_column][idfkit.simulation.parsers.csv.CSVResult.get_column].
    Inherits from ``KeyError`` so code catching ``KeyError`` keeps working; unlike a plain
    ``KeyError``, ``str()`` gives the message as written, not its ``repr()``.

    Attributes:
        suggestions: The closest names the database does have ("did you mean"), closest first.
        available: The keys, frequencies or names that matched or could be passed instead.
    """

    def __init__(self, message: str, *, suggestions: Sequence[str] = (), available: Sequence[str] = ()) -> None:
        super().__init__(message)
        self.message = message
        self.suggestions = tuple(suggestions)
        self.available = tuple(available)

    def __str__(self) -> str:
        # KeyError.__str__ gives repr() of its argument: quoted, with a literal "\n".
        return self.message


class UnknownObjectTypeWarning(UserWarning):
    """Warned when a document is read by an object type name no bundled EnergyPlus release has.

    ``model["Zoen"]`` and ``model.get_collection("Zoen")`` return an empty collection rather than
    raising (see the note on ``IDFDocument.__getitem__``), so a misspelt name would otherwise go
    unnoticed. A name some bundled release has, even one the document's own release lacks, is not
    warned about. Filter it like any warning:

        warnings.filterwarnings("ignore", category=UnknownObjectTypeWarning)
    """

    def __init__(self, obj_type: str, suggestion: str | None = None) -> None:
        # ``args`` holds the constructor's arguments, not the message, so ``cls(*args)`` rebuilds
        # the warning as pickle, ``copy`` and pytest-xdist's warning transport all do.
        super().__init__(obj_type, suggestion)
        self.obj_type = obj_type
        self.suggestion = suggestion

    def __str__(self) -> str:
        msg = f"Object type '{self.obj_type}' is in no bundled EnergyPlus release; the collection is empty"
        if self.suggestion is not None:
            msg += f". Did you mean '{self.suggestion}'?"
        return msg


@dataclass(frozen=True, slots=True)
class RefusedEntry:
    """One entry of an ``IDFObject.update`` group, or ``IDFDocument.add`` call, that will not be applied.

    ``reason`` is ``"unknown"`` (not a field of the type), ``"name"`` (renaming has its own
    operation), ``"legacy-flat"`` (an eppy-style flat extensible name) or ``"wrapper-value"``
    (the extensible wrapper key given a value single assignment rejects: not a list, or a list
    with an item that is not a dict or group, or a group with an unknown field).
    """

    name: str
    reason: Literal["unknown", "name", "legacy-flat", "wrapper-value"]
    detail: str


def format_refused(
    obj_type: str, refused: Sequence[RefusedEntry], operation: Literal["update", "add"] = "update"
) -> str:
    """Message for a refused ``IDFObject.update`` group or ``IDFDocument.add`` call: the type, then one line per entry."""
    if operation == "add":
        lines = [f"add() of object type '{obj_type}' refused; nothing was added:"]
    else:
        lines = [f"Update of object type '{obj_type}' refused; no field was changed:"]
    lines.extend(f"  - {entry.name}: {entry.reason} ({entry.detail})" for entry in refused)
    return "\n".join(lines)


def _closest_fields(names: Sequence[str], available_fields: Sequence[str], hints: dict[str, str]) -> dict[str, str]:
    """The closest of *available_fields* to each of *names*, for the names that have one.

    A name whose refusal line already quotes that field, as ``spell it 'x_origin'`` does, is left
    out, so the same hint is not given twice. *hints* maps a name to its refusal detail.
    """
    suggestions: dict[str, str] = {}
    for name in names:
        close = closest_name(name, available_fields)
        if close is not None and close != name and f"'{close}'" not in hints.get(name, ""):
            suggestions[name] = close
    return suggestions


def _did_you_mean(names: Sequence[str], suggestions: dict[str, str]) -> str:
    """The "Did you mean" line for *suggestions*, naming each unknown name when there are several."""
    if not suggestions:
        return ""
    if len(names) == 1:
        return f"\nDid you mean '{suggestions[names[0]]}'?"
    pairs = ", ".join(f"'{close}' for '{name}'" for name, close in suggestions.items())
    return f"\nDid you mean {pairs}?"


class InvalidFieldError(IdfKitError, AttributeError):
    """Raised when an invalid field is accessed or set.

    Inherits from ``AttributeError`` so that Python's attribute access
    protocol (``hasattr``, ``getattr`` with default) continues to work
    correctly when this is raised from ``__getattr__``.
    """

    def __init__(
        self,
        obj_type: str,
        field_name: str,
        available_fields: list[str] | None = None,
        version: tuple[int, int, int] | None = None,
        extensible_fields: frozenset[str] | None = None,
        *,
        refused: Sequence[RefusedEntry] | None = None,
        operation: Literal["update", "add"] = "update",
        message: str | None = None,
    ) -> None:
        self.obj_type = obj_type
        self.field_name = field_name
        self.available_fields = available_fields
        self.version = version
        self.extensible_fields = extensible_fields
        self.refused = tuple(refused) if refused else ()
        if message is not None:
            msg = message
        elif refused:
            msg = format_refused(obj_type, refused, operation)
        else:
            msg = f"Invalid field '{field_name}' for object type '{obj_type}'"
        unknown_entries = [entry for entry in refused if entry.reason == "unknown"] if refused else []
        unknown = [entry.name for entry in unknown_entries] if refused else [field_name]
        hints = {entry.name: entry.detail for entry in unknown_entries}
        #: The closest field of the type to each unknown name, for the names that have one and whose
        #: refusal line does not already name it.
        self.suggestions = _closest_fields(unknown, available_fields or [], hints)
        msg += _did_you_mean(unknown, self.suggestions)
        if available_fields:
            msg += f"\nAvailable fields: {', '.join(available_fields[:10])}"
            if len(available_fields) > 10:
                msg += f" ... and {len(available_fields) - 10} more"
        if extensible_fields:
            sorted_ext = sorted(extensible_fields)
            group = ", ".join(sorted_ext)
            msg += f"\n  (extensible: additional groups of ({group}) are allowed)"
        if version:
            from .docs import io_reference_url

            doc_url = io_reference_url(obj_type, version)
            if doc_url:
                msg += f"\n  Docs: {doc_url.url}"
        super().__init__(msg)


class MissingRequiredFieldError(IdfKitError, AttributeError):
    """Raised when reading a required field that the object does not hold.

    A field every EnergyPlus release requires with no default reads as its value type, never
    ``None``: ``add()`` refuses to create an object without it, and assigning ``None`` to it is a
    type error. An object can still lack one when it was loaded from a file that omits it, created
    with ``IDFDocument.add(..., validate=False)``, or cleared through an untyped path. Reading the
    field then raises this rather than returning a ``None`` the type said could not occur.

    It inherits from ``AttributeError``, so ``getattr(obj, field, None)`` and ``hasattr`` keep
    working as the untyped way to ask whether the field is set, as does ``obj.get(field)``.

    The same holds for a key of an extensible group that every release requires
    (``vertex_x_coordinate``): reading it from a group that lacks it, or snapshotting that group with
    ``as_dict()`` or ``as_list()``, raises this with :attr:`wrapper_key` and :attr:`group_index` set;
    ``group.get(key)`` gives ``None`` instead.

    Attributes:
        obj_type: The object's type.
        obj_name: The object's name, ``""`` for a type without one.
        field_name: The field, or the group key, that has no value.
        wrapper_key: The extensible group's wrapper (``vertices``), or ``None`` for a field.
        group_index: The group's 1-based position in the wrapper, or ``None`` for a field.
    """

    def __init__(self, obj_type: str, obj_name: str, field_name: str, *, group: tuple[str, int] | None = None) -> None:
        self.obj_type = obj_type
        self.obj_name = obj_name
        self.field_name = field_name
        self.wrapper_key, self.group_index = group if group is not None else (None, None)
        label = f"{obj_type} {obj_name!r}" if obj_name else obj_type
        if group is None:
            message = (
                f"{label} has no value for its required field {field_name!r}. EnergyPlus refuses an object "
                f"without it; set it, or read it with obj.get({field_name!r}) to get None when it is missing."
            )
        else:
            where = f"{group[0]}[{group[1] - 1}]"
            message = (
                f"{label} has no value for the required key {field_name!r} of {where}. EnergyPlus refuses an "
                f"object without it; set it, or read it with {where}.get({field_name!r}) to get None when it is "
                "missing."
            )
        super().__init__(message)

    def __reduce__(self) -> tuple[Any, ...]:
        # BaseException pickles only self.args, the message; rebuild from the parts instead, so the
        # error survives a process boundary (multiprocessing) with its attributes.
        group = None if self.wrapper_key is None or self.group_index is None else (self.wrapper_key, self.group_index)
        return (_rebuild_missing_required_field_error, (self.obj_type, self.obj_name, self.field_name, group))


def _rebuild_missing_required_field_error(
    obj_type: str, obj_name: str, field_name: str, group: tuple[str, int] | None
) -> MissingRequiredFieldError:
    """Unpickle a :class:`MissingRequiredFieldError` (see its ``__reduce__``)."""
    return MissingRequiredFieldError(obj_type, obj_name, field_name, group=group)


class VersionNotFoundError(IdfKitError):
    """Raised when version cannot be detected from file."""

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        super().__init__(f"Could not detect EnergyPlus version in file: {filepath}")


class DanglingReferenceError(IdfKitError):
    """Raised when an object references a non-existent object.

    Attributes:
        source: The object holding the reference.
        field: The field holding the reference.
        target: The name that resolves to no object.
        suggestion: The closest existing name the field could reference, if one is close.
    """

    def __init__(self, source: IDFObject, field: str, target: str, *, suggestion: str | None = None) -> None:
        self.source = source
        self.field = field
        self.target = target
        self.suggestion = suggestion
        msg = f"Object {source.obj_type}:'{source.name}' field '{field}' references non-existent object '{target}'"
        if suggestion is not None:
            msg += f". Did you mean '{suggestion}'?"
        super().__init__(msg)


class RangeError(IdfKitError):
    """Raised when a field value is outside the valid range (eppy compatibility).

    Attributes:
        obj_type: The object type.
        obj_name: The object name.
        field_name: The field that failed range checking.
    """

    def __init__(self, obj_type: str, obj_name: str, field_name: str, message: str) -> None:
        self.obj_type = obj_type
        self.obj_name = obj_name
        self.field_name = field_name
        super().__init__(message)


class ValidationFailedError(IdfKitError):
    """Raised when validation fails."""

    def __init__(self, errors: Sequence[object]) -> None:
        self.errors = list(errors)
        # Count by severity, so a warning is not called an error. Items without one count as errors.
        counts: dict[str, int] = {}
        for err in self.errors:
            severity = getattr(getattr(err, "severity", None), "value", "error")
            counts[severity] = counts.get(severity, 0) + 1
        parts = [f"{counts[s]} {s}(s)" for s in ("error", "warning", "info") if counts.get(s)]
        msg = f"Validation failed with {', '.join(parts) or '0 error(s)'}:\n"
        for i, err in enumerate(self.errors[:5], 1):
            msg += f"  {i}. {err}\n"
        if len(self.errors) > 5:
            msg += f"  ... and {len(self.errors) - 5} more"
        super().__init__(msg)


class EnergyPlusNotFoundError(IdfKitError):
    """Raised when EnergyPlus installation cannot be found.

    Attributes:
        searched_locations: The paths that were tried, each once, in the order tried.
        requested_version: The release asked for with ``version=``, or ``None`` for any.
        found: The installations discovery did find, as ``(version, install_dir)`` pairs,
            when none of them is *requested_version*.
    """

    def __init__(
        self,
        searched_locations: list[str] | None = None,
        *,
        requested_version: tuple[int, int, int] | None = None,
        found: Sequence[tuple[tuple[int, int, int], str]] = (),
    ) -> None:
        self.searched_locations = list(dict.fromkeys(searched_locations or []))
        self.requested_version = requested_version
        self.found = list(found)
        if requested_version is not None and self.found:
            msg = self._version_mismatch_message(requested_version, self.found)
        else:
            msg = "Could not find an EnergyPlus installation"
            if requested_version is not None:
                msg += f" of version {_dotted(requested_version)}"
            msg += "."
            if self.searched_locations:
                msg += "\nSearched in:\n"
                for loc in self.searched_locations:
                    msg += f"  - {loc}\n"
            msg += (
                "\nTo fix this, either:\n"
                "  1. Set the ENERGYPLUS_DIR environment variable to your EnergyPlus install directory\n"
                "  2. Pass an explicit path: find_energyplus(path='/path/to/EnergyPlus')\n"
                "  3. Ensure 'energyplus' is on your PATH"
            )
        super().__init__(msg)

    @staticmethod
    def _version_mismatch_message(
        requested: tuple[int, int, int], found: list[tuple[tuple[int, int, int], str]]
    ) -> str:
        """The message for an installation that exists, but not at the version asked for."""
        req = _dotted(requested)
        installs = ", ".join(f"{_dotted(v)} at {d}" for v, d in found)
        msg = f"No EnergyPlus {req} found; found {installs}.\nTo fix this, either:\n"
        msg += f"  1. Install EnergyPlus {req}, or point ENERGYPLUS_DIR or path= at an install of it\n"
        msg += "  2. Drop version= to use an installed release: find_energyplus()"
        newer = sorted({v for v, _ in found if v > requested})
        if newer:
            target = newer[-1]
            msg += (
                f"\n  3. Migrate the model to {_dotted(target)}: simulate(..., auto_migrate=True),"
                f" or idfkit.migrate(model, target_version=({target[0]}, {target[1]}, {target[2]}))"
            )
        return msg

    def __reduce__(self) -> tuple[Any, ...]:
        # BaseException pickles only self.args, the message; rebuild from the parts instead, so the
        # error survives a process boundary (multiprocessing) with its message and attributes.
        return (
            _rebuild_energyplus_not_found_error,
            (self.searched_locations, self.requested_version, tuple(self.found)),
        )


def _rebuild_energyplus_not_found_error(
    searched_locations: list[str],
    requested_version: tuple[int, int, int] | None,
    found: tuple[tuple[tuple[int, int, int], str], ...],
) -> EnergyPlusNotFoundError:
    """Unpickle an :class:`EnergyPlusNotFoundError` (see its ``__reduce__``)."""
    return EnergyPlusNotFoundError(searched_locations, requested_version=requested_version, found=found)


def _dotted(version: tuple[int, int, int]) -> str:
    """``(24, 1, 0)`` as ``"24.1.0"``."""
    return f"{version[0]}.{version[1]}.{version[2]}"


class ExpandObjectsError(IdfKitError):
    """Raised when an EnergyPlus preprocessor fails.

    Attributes:
        preprocessor: Name of the preprocessor that failed (e.g.
            ``"ExpandObjects"``, ``"Slab"``, ``"Basement"``).
        exit_code: Process exit code (``None`` if timed out or not started).
        stderr: Captured standard error output (truncated to 500 chars).
    """

    def __init__(
        self,
        message: str,
        *,
        preprocessor: str | None = None,
        exit_code: int | None = None,
        stderr: str | None = None,
    ) -> None:
        self.preprocessor = preprocessor
        self.exit_code = exit_code
        self.stderr = stderr
        super().__init__(_format_subprocess_failure(message, exit_code=exit_code, stderr=stderr))


class SimulationError(IdfKitError):
    """Raised when an EnergyPlus simulation fails.

    Attributes:
        exit_code: EnergyPlus's exit code, if it ran and exited.
        stderr: Its standard error, if any.
        result: The failed run's result, when raised by
            [SimulationResult.raise_for_status][idfkit.simulation.result.SimulationResult.raise_for_status];
            read its ``errors`` for every message.
    """

    def __init__(
        self,
        message: str,
        *,
        exit_code: int | None = None,
        stderr: str | None = None,
        result: SimulationResult | None = None,
    ) -> None:
        self.exit_code = exit_code
        self.stderr = stderr
        self.result = result
        super().__init__(_format_subprocess_failure(message, exit_code=exit_code, stderr=stderr))


class VersionMismatchError(IdfKitError):
    """Raised when an IDF model's version differs from the installed EnergyPlus version.

    Carries structured context so callers (including MCP tools and LSP clients) can
    decide whether to migrate the model or surface the mismatch to the user.

    Attributes:
        current: The model's version tuple.
        target: The installed EnergyPlus version tuple.
        migration_chain: Ordered pairs ``((from, to), ...)`` describing the transition
            steps that would be run to forward-migrate ``current`` to ``target``.
            Empty when migration is not possible (e.g. target is older than current).
        direction: ``"forward"`` when ``current < target``, ``"backward"`` otherwise.
    """

    def __init__(
        self,
        *,
        current: tuple[int, int, int],
        target: tuple[int, int, int],
        migration_chain: Sequence[tuple[tuple[int, int, int], tuple[int, int, int]]] = (),
    ) -> None:
        self.current = current
        self.target = target
        self.migration_chain = tuple(migration_chain)
        self.direction: Literal["forward", "backward"] = "forward" if current < target else "backward"
        current_str = f"{current[0]}.{current[1]}.{current[2]}"
        target_str = f"{target[0]}.{target[1]}.{target[2]}"
        msg = f"Model version {current_str} does not match target EnergyPlus version {target_str}."
        if self.direction == "backward":
            msg += (
                "\nBackward migration is not supported: EnergyPlus ships no reverse transition binaries."
                f"\nTo fix it, either build the model at {target_str}"
                f" (new_document(version=({target[0]}, {target[1]}, {target[2]})),"
                " or version=idfkit.simulation.find_energyplus().version for whatever is installed),"
                f" or install EnergyPlus {current_str} and pass"
                f' energyplus=idfkit.simulation.find_energyplus(version="{current_str}").'
            )
        else:
            if self.migration_chain:
                steps = " -> ".join(f"{a[0]}.{a[1]}.{a[2]}->{b[0]}.{b[1]}.{b[2]}" for a, b in self.migration_chain)
                msg += f"\nMigration chain: {steps}"
            msg += (
                "\nTo fix it, pass auto_migrate=True to simulate() (or to each SimulationJob in a batch)"
                " to migrate a copy before the run,"
                f" or call idfkit.migrate(model, target_version=({target[0]}, {target[1]}, {target[2]}))"
                " to migrate it once and keep the result."
            )
        super().__init__(msg)


class MigrationError(IdfKitError):
    """Raised when an IDF migration step fails.

    Attributes:
        from_version: Version the failing step started from (if known).
        to_version: Version the failing step targeted (if known).
        exit_code: Process exit code of the transition binary (if available).
        stderr: Captured stderr of the transition binary (truncated to 500 chars).
        completed_steps: Ordered ``(from, to)`` pairs that ran successfully before
            the failure. Empty when the chain failed on its first step.
        reason: The message as given, without the step, the process output or the
            step count the full message adds, so the error can be re-raised for
            another step without repeating them.
    """

    def __init__(
        self,
        message: str,
        *,
        from_version: tuple[int, int, int] | None = None,
        to_version: tuple[int, int, int] | None = None,
        exit_code: int | None = None,
        stderr: str | None = None,
        completed_steps: Sequence[tuple[tuple[int, int, int], tuple[int, int, int]]] = (),
    ) -> None:
        self.from_version = from_version
        self.to_version = to_version
        self.exit_code = exit_code
        self.stderr = stderr
        self.completed_steps = tuple(completed_steps)
        self.reason = message
        head = message
        if from_version is not None and to_version is not None:
            a, b = from_version, to_version
            head += f" ({a[0]}.{a[1]}.{a[2]} -> {b[0]}.{b[1]}.{b[2]})"
        msg = _format_subprocess_failure(head, exit_code=exit_code, stderr=stderr)
        if self.completed_steps:
            msg += f"\nCompleted steps before failure: {len(self.completed_steps)}"
        super().__init__(msg)


class NoDesignDaysError(IdfKitError):
    """Raised when a DDY file contains no SizingPeriod:DesignDay objects.

    This typically occurs for weather stations that lack ASHRAE design
    conditions data in the climate.onebuilding.org database.

    Attributes:
        station_name: Display name of the station (if available).
        ddy_path: Path to the DDY file that was parsed.
        nearby_suggestions: List of nearby stations that may have design days.
    """

    def __init__(
        self,
        station_name: str | None = None,
        ddy_path: str | None = None,
        nearby_suggestions: list[str] | None = None,
    ) -> None:
        self.station_name = station_name
        self.ddy_path = ddy_path
        self.nearby_suggestions = nearby_suggestions or []

        if station_name:
            msg = f"DDY file for '{station_name}' contains no SizingPeriod:DesignDay objects."
        elif ddy_path:
            msg = f"DDY file '{ddy_path}' contains no SizingPeriod:DesignDay objects."
        else:
            msg = "DDY file contains no SizingPeriod:DesignDay objects."

        msg += "\nThis station may lack ASHRAE design conditions data."

        if self.nearby_suggestions:
            msg += "\n\nNearby stations that may have design days:"
            for suggestion in self.nearby_suggestions[:5]:
                msg += f"\n  - {suggestion}"

        super().__init__(msg)
