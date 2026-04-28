"""
idfkit: A fast, modern EnergyPlus IDF/epJSON parser.

This package provides high-performance parsing and manipulation of EnergyPlus
input files (IDF and epJSON formats), with O(1) lookups and reference tracking.

Basic usage:
    from idfkit import load_idf, load_epjson

    # Load an IDF file
    model = load_idf("building.idf")

    # Access objects
    zones = model["Zone"]
    zone = zones["MyZone"]

    # Find references
    surfaces = model.get_referencing("MyZone")

    # Write back
    from idfkit import write_idf
    write_idf(model, "modified.idf")
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Literal, overload

if TYPE_CHECKING:
    from ._generated_types import *

__version__ = "0.1.0"

# Core classes
# Documentation URL builder
from .docs import DocsUrl, docs_url_for_object, engineering_reference_url, io_reference_url, search_url
from .document import IDFDocument
from .epjson_parser import parse_epjson

# Exceptions
from .exceptions import (
    DuplicateObjectError,
    EnergyPlusNotFoundError,
    ExpandObjectsError,
    IdfKitError,
    IDFParseError,
    InvalidFieldError,
    MigrationError,
    NoDesignDaysError,
    ParseError,
    RangeError,
    SchemaNotFoundError,
    SimulationError,
    UnknownObjectTypeError,
    UnsupportedVersionError,
    ValidationFailedError,
    VersionMismatchError,
    VersionNotFoundError,
)

# Geometry utilities
from .geometry import (
    Polygon3D,
    Vector3D,
    calculate_surface_area,
    calculate_surface_azimuth,
    calculate_surface_tilt,
    calculate_zone_ceiling_area,
    calculate_zone_floor_area,
    calculate_zone_height,
    calculate_zone_volume,
    intersect_match,
    polygon_area_2d,
    polygon_contains_2d,
    polygon_difference_2d,
    polygon_intersection_2d,
    rotate_building,
    set_wwr,
    translate_building,
)

# Geometry builders
from .geometry_builders import (
    HorizontalAdjacency,
    add_shading_block,
    bounding_box,
    detect_horizontal_adjacencies,
    link_horizontal_surfaces,
    scale_building,
    set_default_constructions,
    split_horizontal_surface,
)

# Parsing functions
from .idf_parser import IDFParser, get_idf_version, parse_idf

# Introspection
from .introspection import FieldDescription, ObjectDescription

# Migration
from .migration import MigrationReport, async_migrate, migrate
from .objects import IDFCollection, IDFObject

# Reference graph
from .references import ReferenceGraph

# Schedule builders
from .schedules.builder import (
    create_compact_schedule_from_values,
    create_constant_schedule,
    create_schedule_type_limits,
)

# Schema access
from .schema import EpJSONSchema, SchemaManager, get_schema, get_schema_manager

# Validation
from .validation import (
    ValidationError,
    ValidationResult,
    validate_document,
    validate_object,
)

# Version registry
from .versions import (
    ENERGYPLUS_VERSIONS,
    LATEST_VERSION,
    MINIMUM_VERSION,
    find_closest_version,
    is_supported_version,
    version_string,
)

# Writing functions
from .writers import write_epjson, write_idf

# Zoning
from .zoning import (
    ASHRAE_PERIMETER_DEPTH,
    ZonedBlock,
    ZoneFootprint,
    ZoningScheme,
    create_block,
    footprint_courtyard,
    footprint_h_shape,
    footprint_l_shape,
    footprint_rectangle,
    footprint_t_shape,
    footprint_u_shape,
    link_blocks,
)

logging.getLogger(__name__).addHandler(logging.NullHandler())


def _check_version(version: tuple[int, int, int]) -> None:
    """Raise UnsupportedVersionError if *version* is not a known EnergyPlus release."""
    if not is_supported_version(version):
        raise UnsupportedVersionError(version, ENERGYPLUS_VERSIONS)


@overload
def load_idf(
    path: str,
    version: tuple[int, int, int] | None = ...,
    *,
    strict_parsing: bool = ...,
    strict: Literal[True] = ...,
    preserve_formatting: bool = ...,
) -> IDFDocument[Literal[True]]: ...


@overload
def load_idf(
    path: str,
    version: tuple[int, int, int] | None = ...,
    *,
    strict_parsing: bool = ...,
    strict: Literal[False],
    preserve_formatting: bool = ...,
) -> IDFDocument[Literal[False]]: ...


def load_idf(
    path: str,
    version: tuple[int, int, int] | None = None,
    *,
    strict_parsing: bool = True,
    strict: bool = True,
    preserve_formatting: bool = False,
) -> IDFDocument[bool]:
    """
    Load an IDF file and return an IDFDocument.

    Args:
        path: Path to the IDF file
        version: Optional version override (major, minor, patch)
        strict_parsing: If True, fail fast on malformed IDF objects (default: True)
        strict: When ``True``, accessing or setting an unknown field name on any
            IDFObject raises :class:`~idfkit.exceptions.InvalidFieldError` instead
            of returning ``None``.
        preserve_formatting: When ``True``, build a Concrete Syntax Tree
            (CST) so that :func:`write_idf` reproduces the original
            formatting, comments, and whitespace for unmodified objects.

    Returns:
        Parsed IDFDocument

    Examples:
        Load a DOE reference building and list its zones:

            ```python
            model = load_idf("RefBldgSmallOfficeNew2004.idf")
            print(f"Loaded {len(model)} objects")
            for zone in model["Zone"]:
                print(zone.name)
            ```

        Override the version for a legacy model:

            ```python
            model = load_idf("pre_v9_building.idf", version=(9, 6, 0))
            ```

        Lossless round-trip:

            ```python
            model = load_idf("building.idf", preserve_formatting=True)
            write_idf(model, "building_copy.idf")  # byte-identical
            ```
    """
    from pathlib import Path

    if version is not None:
        _check_version(version)
    return parse_idf(
        Path(path),
        version=version,
        strict_parsing=strict_parsing,
        strict=strict,
        preserve_formatting=preserve_formatting,
    )


@overload
def load_epjson(
    path: str,
    version: tuple[int, int, int] | None = ...,
    *,
    strict: Literal[True] = ...,
    preserve_formatting: bool = ...,
) -> IDFDocument[Literal[True]]: ...


@overload
def load_epjson(
    path: str,
    version: tuple[int, int, int] | None = ...,
    *,
    strict: Literal[False],
    preserve_formatting: bool = ...,
) -> IDFDocument[Literal[False]]: ...


def load_epjson(
    path: str,
    version: tuple[int, int, int] | None = None,
    *,
    strict: bool = True,
    preserve_formatting: bool = False,
) -> IDFDocument[bool]:
    """
    Load an epJSON file and return an IDFDocument.

    Args:
        path: Path to the epJSON file
        version: Optional version override (major, minor, patch)
        strict: When ``True``, accessing or setting an unknown field name on any
            IDFObject raises :class:`~idfkit.exceptions.InvalidFieldError` instead
            of returning ``None``.
        preserve_formatting: When ``True``, store the raw JSON text so
            that :func:`write_epjson` can reproduce it byte-for-byte
            when no objects have been modified.

    Returns:
        Parsed IDFDocument

    Examples:
        Load an epJSON model and iterate over zones:

            ```python
            model = load_epjson("SmallOffice.epJSON")
            for zone in model["Zone"]:
                print(zone.name, zone.x_origin)
            ```

        Specify an explicit EnergyPlus version:

            ```python
            model = load_epjson("SmallOffice.epJSON", version=(24, 1, 0))
            ```
    """
    from pathlib import Path

    if version is not None:
        _check_version(version)
    return parse_epjson(Path(path), version=version, strict=strict, preserve_formatting=preserve_formatting)


@overload
def new_document(
    version: tuple[int, int, int] = ...,
    *,
    strict: Literal[True] = ...,
) -> IDFDocument[Literal[True]]: ...


@overload
def new_document(
    version: tuple[int, int, int] = ...,
    *,
    strict: Literal[False],
) -> IDFDocument[Literal[False]]: ...


def new_document(
    version: tuple[int, int, int] = LATEST_VERSION,
    *,
    strict: bool = True,
) -> IDFDocument[bool]:
    """
    Create a new IDFDocument with baseline singleton objects populated.

    Args:
        version: EnergyPlus version (default: latest supported version)
        strict: When ``True``, accessing or setting an unknown field name on any
            IDFObject raises :class:`~idfkit.exceptions.InvalidFieldError` instead
            of returning ``None``.

    Returns:
        IDFDocument with schema loaded and baseline objects seeded

    Examples:
        >>> model = new_document()
        >>> len(model)
        4

        Baseline singleton objects are present by default:

        >>> model["Building"].first().name
        'Building'

        Add objects to the model:

        >>> zone = model.add("Zone", "Office", x_origin=0.0, y_origin=0.0)
        >>> zone.name
        'Office'
        >>> len(model)
        5

        Create a model for a specific EnergyPlus version:

        >>> model_v24 = new_document(version=(24, 1, 0))
        >>> model_v24.version
        (24, 1, 0)
    """
    _check_version(version)
    schema = get_schema(version)
    doc = IDFDocument(version=version, schema=schema, strict=strict)  # type: ignore[reportCallIssue]  # .pyi uses covariant Strict

    # Seed core singleton objects for a minimal baseline model.
    version_identifier = f"{version[0]}.{version[1]}"
    doc.add("Version", version_identifier=version_identifier)
    doc.add("Building", "Building")
    doc.add("SimulationControl")
    doc.add(
        "GlobalGeometryRules",
        starting_vertex_position="UpperLeftCorner",
        vertex_entry_direction="Counterclockwise",
        coordinate_system="Relative",
    )
    return doc


__all__ = [
    "ASHRAE_PERIMETER_DEPTH",
    "ENERGYPLUS_VERSIONS",
    "LATEST_VERSION",
    "MINIMUM_VERSION",
    "DocsUrl",
    "DuplicateObjectError",
    "EnergyPlusNotFoundError",
    "EpJSONSchema",
    "ExpandObjectsError",
    "FieldDescription",
    "HorizontalAdjacency",
    "IDFCollection",
    "IDFDocument",
    "IDFObject",
    "IDFParseError",
    "IDFParser",
    "IdfKitError",
    "InvalidFieldError",
    "MigrationError",
    "MigrationReport",
    "NoDesignDaysError",
    "ObjectDescription",
    "ParseError",
    "Polygon3D",
    "RangeError",
    "ReferenceGraph",
    "SchemaManager",
    "SchemaNotFoundError",
    "SimulationError",
    "UnknownObjectTypeError",
    "UnsupportedVersionError",
    "ValidationError",
    "ValidationFailedError",
    "ValidationResult",
    "Vector3D",
    "VersionMismatchError",
    "VersionNotFoundError",
    "ZoneFootprint",
    "ZonedBlock",
    "ZoningScheme",
    "__version__",
    "add_shading_block",
    "async_migrate",
    "bounding_box",
    "calculate_surface_area",
    "calculate_surface_azimuth",
    "calculate_surface_tilt",
    "calculate_zone_ceiling_area",
    "calculate_zone_floor_area",
    "calculate_zone_height",
    "calculate_zone_volume",
    "create_block",
    "create_compact_schedule_from_values",
    "create_constant_schedule",
    "create_schedule_type_limits",
    "detect_horizontal_adjacencies",
    "docs_url_for_object",
    "engineering_reference_url",
    "find_closest_version",
    "footprint_courtyard",
    "footprint_h_shape",
    "footprint_l_shape",
    "footprint_rectangle",
    "footprint_t_shape",
    "footprint_u_shape",
    "get_idf_version",
    "get_schema",
    "get_schema_manager",
    "intersect_match",
    "io_reference_url",
    "is_supported_version",
    "link_blocks",
    "link_horizontal_surfaces",
    "load_epjson",
    "load_idf",
    "migrate",
    "new_document",
    "parse_epjson",
    "parse_idf",
    "polygon_area_2d",
    "polygon_contains_2d",
    "polygon_difference_2d",
    "polygon_intersection_2d",
    "rotate_building",
    "scale_building",
    "search_url",
    "set_default_constructions",
    "set_wwr",
    "split_horizontal_surface",
    "translate_building",
    "validate_document",
    "validate_object",
    "version_string",
    "write_epjson",
    "write_idf",
]
