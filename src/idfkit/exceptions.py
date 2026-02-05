"""Custom exceptions for idfkit."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .objects import IDFObject


class IdfKitError(Exception):
    """Base exception for all idfkit errors."""

    pass


# Alias for backwards compatibility
ParseError = IdfKitError


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


class UnknownObjectTypeError(IdfKitError):
    """Raised when an unknown object type is encountered."""

    def __init__(self, obj_type: str) -> None:
        self.obj_type = obj_type
        super().__init__(f"Unknown object type: '{obj_type}'")


class InvalidFieldError(IdfKitError):
    """Raised when an invalid field is accessed or set."""

    def __init__(self, obj_type: str, field_name: str, available_fields: list[str] | None = None) -> None:
        self.obj_type = obj_type
        self.field_name = field_name
        self.available_fields = available_fields
        msg = f"Invalid field '{field_name}' for object type '{obj_type}'"
        if available_fields:
            msg += f"\nAvailable fields: {', '.join(available_fields[:10])}"
            if len(available_fields) > 10:
                msg += f" ... and {len(available_fields) - 10} more"
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


class ValidationFailedError(IdfKitError):
    """Raised when validation fails."""

    def __init__(self, errors: list[object]) -> None:
        self.errors = errors
        msg = f"Validation failed with {len(errors)} error(s):\n"
        for i, err in enumerate(errors[:5], 1):
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
        msg = message
        if exit_code is not None:
            msg += f" (exit code {exit_code})"
        if stderr:
            trimmed = stderr.strip()[:500]
            msg += f"\nstderr: {trimmed}"
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
