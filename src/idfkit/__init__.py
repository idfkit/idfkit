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

__version__ = "0.1.0"

# Core classes
from .document import IDFDocument
from .epjson_parser import parse_epjson

# Exceptions
from .exceptions import (
    DuplicateObjectError,
    EnergyPlusNotFoundError,
    ExpandObjectsError,
    IdfKitError,
    NoDesignDaysError,
    ParseError,
    RangeError,
    SchemaNotFoundError,
    SimulationError,
    UnknownObjectTypeError,
    ValidationFailedError,
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
    rotate_building,
    set_wwr,
    translate_building,
)

# Geometry builders
from .geometry_builders import (
    Shoebox,
    add_block,
    add_shading_block,
    bounding_box,
    scale_building,
    set_default_constructions,
)

# Parsing functions
from .idf_parser import IDFParser, get_idf_version, parse_idf

# Introspection
from .introspection import FieldDescription, ObjectDescription
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
    ZoningScheme,
    create_building,
    footprint_courtyard,
    footprint_h_shape,
    footprint_l_shape,
    footprint_rectangle,
    footprint_t_shape,
    footprint_u_shape,
)

logging.getLogger(__name__).addHandler(logging.NullHandler())


def load_idf(path: str, version: tuple[int, int, int] | None = None) -> IDFDocument:
    """
    Load an IDF file and return an IDFDocument.

    Args:
        path: Path to the IDF file
        version: Optional version override (major, minor, patch)

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
    """
    from pathlib import Path

    return parse_idf(Path(path), version=version)


def load_epjson(path: str, version: tuple[int, int, int] | None = None) -> IDFDocument:
    """
    Load an epJSON file and return an IDFDocument.

    Args:
        path: Path to the epJSON file
        version: Optional version override (major, minor, patch)

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

    return parse_epjson(Path(path), version=version)


def new_document(version: tuple[int, int, int] = LATEST_VERSION) -> IDFDocument:
    """
    Create a new empty IDFDocument.

    Args:
        version: EnergyPlus version (default: latest supported version)

    Returns:
        Empty IDFDocument with schema loaded

    Examples:
        >>> model = new_document()
        >>> len(model)
        0

        Add objects to the model:

        >>> zone = model.add("Zone", "Office", x_origin=0.0, y_origin=0.0)
        >>> zone.name
        'Office'
        >>> len(model)
        1

        Create a model for a specific EnergyPlus version:

        >>> model_v24 = new_document(version=(24, 1, 0))
        >>> model_v24.version
        (24, 1, 0)
    """
    schema = get_schema(version)
    return IDFDocument(version=version, schema=schema)


__all__ = [
    "ASHRAE_PERIMETER_DEPTH",
    "ENERGYPLUS_VERSIONS",
    "LATEST_VERSION",
    "MINIMUM_VERSION",
    "DuplicateObjectError",
    "EnergyPlusNotFoundError",
    "EpJSONSchema",
    "ExpandObjectsError",
    "FieldDescription",
    "IDFCollection",
    "IDFDocument",
    "IDFObject",
    "IDFParser",
    "IdfKitError",
    "NoDesignDaysError",
    "ObjectDescription",
    "ParseError",
    "Polygon3D",
    "RangeError",
    "ReferenceGraph",
    "SchemaManager",
    "SchemaNotFoundError",
    "Shoebox",
    "SimulationError",
    "UnknownObjectTypeError",
    "ValidationError",
    "ValidationFailedError",
    "ValidationResult",
    "Vector3D",
    "VersionNotFoundError",
    "ZonedBlock",
    "ZoningScheme",
    "__version__",
    "add_block",
    "add_shading_block",
    "bounding_box",
    "calculate_surface_area",
    "calculate_surface_azimuth",
    "calculate_surface_tilt",
    "calculate_zone_ceiling_area",
    "calculate_zone_floor_area",
    "calculate_zone_height",
    "calculate_zone_volume",
    "create_building",
    "create_compact_schedule_from_values",
    "create_constant_schedule",
    "create_schedule_type_limits",
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
    "is_supported_version",
    "load_epjson",
    "load_idf",
    "new_document",
    "parse_epjson",
    "parse_idf",
    "rotate_building",
    "scale_building",
    "set_default_constructions",
    "set_wwr",
    "translate_building",
    "validate_document",
    "validate_object",
    "version_string",
    "write_epjson",
    "write_idf",
]
