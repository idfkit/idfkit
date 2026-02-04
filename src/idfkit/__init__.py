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

__version__ = "0.1.0"

# Core classes
from .document import IDFDocument
from .epjson_parser import parse_epjson

# Exceptions
from .exceptions import (
    DuplicateObjectError,
    IdfKitError,
    ParseError,
    SchemaNotFoundError,
    UnknownObjectTypeError,
    ValidationFailedError,
    VersionNotFoundError,
)

# Geometry utilities
from .geometry import Polygon3D, Vector3D

# Parsing functions
from .idf_parser import IDFParser, get_idf_version, parse_idf
from .objects import IDFCollection, IDFObject

# Reference graph
from .references import ReferenceGraph

# Schema access
from .schema import EpJSONSchema, SchemaManager, get_schema, get_schema_manager

# Validation
from .validation import ValidationError, ValidationResult, validate_document

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


def load_idf(path: str, version: tuple[int, int, int] | None = None) -> IDFDocument:
    """
    Load an IDF file and return an IDFDocument.

    Args:
        path: Path to the IDF file
        version: Optional version override (major, minor, patch)

    Returns:
        Parsed IDFDocument

    Example:
        model = load_idf("building.idf")
        print(f"Loaded {len(model)} objects")
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

    Example:
        model = load_epjson("building.epJSON")
        print(f"Loaded {len(model)} objects")
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

    Example:
        model = new_document()
        model.add("Zone", "MyZone", {"x_origin": 0, "y_origin": 0})
    """
    schema = get_schema(version)
    return IDFDocument(version=version, schema=schema)


__all__ = [
    "ENERGYPLUS_VERSIONS",
    "LATEST_VERSION",
    "MINIMUM_VERSION",
    "DuplicateObjectError",
    "EpJSONSchema",
    "IDFCollection",
    "IDFDocument",
    "IDFObject",
    "IDFParser",
    "IdfKitError",
    "ParseError",
    "Polygon3D",
    "ReferenceGraph",
    "SchemaManager",
    "SchemaNotFoundError",
    "UnknownObjectTypeError",
    "ValidationError",
    "ValidationFailedError",
    "ValidationResult",
    "Vector3D",
    "VersionNotFoundError",
    "__version__",
    "find_closest_version",
    "get_idf_version",
    "get_schema",
    "get_schema_manager",
    "is_supported_version",
    "load_epjson",
    "load_idf",
    "new_document",
    "parse_epjson",
    "parse_idf",
    "validate_document",
    "version_string",
    "write_epjson",
    "write_idf",
]
