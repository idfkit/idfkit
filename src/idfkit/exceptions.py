"""Custom exceptions for idfkit."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from .objects import IDFObject


class IdfKitError(Exception):
    """Base exception for all idfkit errors."""

    pass


def _format_subprocess_failure(
    message: str,
    *,
    exit_code: int | None = None,
    stderr: str | None = None,
) -> str:
    """Shared subprocess-failure message formatter.

    Appends ``(exit code N)`` and a 500-char-truncated stderr tail to *message*.
    """
    msg = message
    if exit_code is not None:
        msg += f" (exit code {exit_code})"
    if stderr:
        msg += f"\nstderr: {stderr.strip()[:500]}"
    return msg


@dataclass(frozen=True, slots=True)
class ParseDiagnostic:
    """Structured parse diagnostic with best-effort source context."""

    message: str
    filepath: str | None = None
    obj_type: str | None = None
    obj_name: str | None = None
    line: int | None = None
    column: int | None = None


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
    for missing object types continues to work.
    """

    def __init__(self, obj_type: str, version: tuple[int, int, int] | None = None) -> None:
        self.obj_type = obj_type
        self.version = version
        msg = f"Unknown object type: '{obj_type}'"
        if version:
            from .docs import search_url

            s_url = search_url(obj_type, version)
            if s_url:
                msg += f"\n  Search docs: {s_url.url}"
        super().__init__(msg)


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
    ) -> None:
        self.obj_type = obj_type
        self.field_name = field_name
        self.available_fields = available_fields
        self.version = version
        self.extensible_fields = extensible_fields
        msg = f"Invalid field '{field_name}' for object type '{obj_type}'"
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


class VersionNotFoundError(IdfKitError):
    """Raised when version cannot be detected from file."""

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        super().__init__(f"Could not detect EnergyPlus version in file: {filepath}")


class DanglingReferenceError(IdfKitError):
    """Raised when an object references a non-existent object."""

    def __init__(self, source: IDFObject, field: str, target: str) -> None:
        self.source = source
        self.field = field
        self.target = target
        super().__init__(
            f"Object {source.obj_type}:'{source.name}' field '{field}' references non-existent object '{target}'"
        )


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
        msg = f"Validation failed with {len(errors)} error(s):\n"
        for i, err in enumerate(list(errors)[:5], 1):
            msg += f"  {i}. {err}\n"
        if len(errors) > 5:
            msg += f"  ... and {len(errors) - 5} more errors"
        super().__init__(msg)


class EnergyPlusNotFoundError(IdfKitError):
    """Raised when EnergyPlus installation cannot be found."""

    def __init__(self, searched_locations: list[str] | None = None) -> None:
        self.searched_locations = searched_locations or []
        msg = "Could not find an EnergyPlus installation."
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
    """Raised when an EnergyPlus simulation fails."""

    def __init__(
        self,
        message: str,
        *,
        exit_code: int | None = None,
        stderr: str | None = None,
    ) -> None:
        self.exit_code = exit_code
        self.stderr = stderr
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
            msg += "\nBackward migration is not supported: EnergyPlus ships no reverse transition binaries."
        elif self.migration_chain:
            steps = " -> ".join(f"{a[0]}.{a[1]}.{a[2]}->{b[0]}.{b[1]}.{b[2]}" for a, b in self.migration_chain)
            msg += f"\nMigration chain: {steps}"
            msg += "\nCall idfkit.migrate(model, target_version=...) to migrate explicitly."
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
