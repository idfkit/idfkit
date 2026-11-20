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
    from idfkit import save_idf
    save_idf(model, "modified.idf")
"""

from __future__ import annotations

import logging
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version
from typing import TYPE_CHECKING, Literal, overload

if TYPE_CHECKING:
    from typing import TypeVar

    from ._compat import EppyDocumentMixin
    from ._generated_types import *

    # Bound to a plain base every document type inherits, so the check is nominal. AnyIDFDocument, a union
    # of two TypedDict-backed classes, would make pyright build both, and compare them key by key at each
    # call, in every file that calls new_document, new_document() included.
    _D = TypeVar("_D", bound=EppyDocumentMixin)

try:
    __version__ = _pkg_version("idfkit")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"

# The conformance corpus level this release declares (FR-024), generated from
# [tool.idfkit.conformance] in pyproject.toml so the claim and the pin stay one fact.
from ._conformance import CONFORMANCE_LEVEL

# Loading functions: typed for any release unless the caller names one (see _loaders.pyi)
from ._loaders import check_supported_version as _check_version
from ._loaders import load_epjson, load_idf, load_idf_with_diagnostics
from .cst import SourceSpan

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
    FileFormatError,
    IdfKitError,
    IDFParseError,
    InvalidFieldError,
    MigrationError,
    MissingRequiredFieldError,
    NoDesignDaysError,
    ObjectNotFoundError,
    ParseError,
    RangeError,
    ResultLookupError,
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
    counter_clockwise_footprint,
    detect_horizontal_adjacencies,
    link_horizontal_surfaces,
    scale_building,
    set_default_constructions,
    split_horizontal_surface,
)

# Parsing functions
from .idf_parser import IDFParser, ParseResult, get_idf_version, parse_idf

# Introspection
from .introspection import FieldDescription, ObjectDescription

# Migration
from .migration import MigrationReport, async_migrate, migrate
from .objects import IDFCollection, IDFObject

# Reference graph
from .references import ReferenceGraph

# Geometry extraction: the read-only half, which resolves rather than authors
from .scene import (
    AppliedRules,
    ResolvedSurface,
    Scene,
    SceneBounds,
    UnattemptedType,
    UnresolvedObject,
    get_scene,
)

# Schedule builders
from .schedules.builder import (
    create_compact_schedule_from_values,
    create_constant_schedule,
    create_schedule_type_limits,
)

# Schema access
from .schema import EpJSONSchema, SchemaManager, get_schema, get_schema_manager

# Surface intersect-and-match
from .surface_matching import (
    MatchOptions,
    MatchReport,
    intersect_and_match,
)

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
from .writers import save_epjson, save_idf, write_epjson, write_idf

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


@overload
def new_document(
    version: tuple[int, int, int] = ...,
    *,
    strict: Literal[True] = ...,
    normalize_choices: bool = ...,
) -> IDFDocument[Literal[True]]: ...


@overload
def new_document(
    version: tuple[int, int, int] = ...,
    *,
    strict: Literal[False],
    normalize_choices: bool = ...,
) -> IDFDocument[Literal[False]]: ...


# Last, so that an argument typed Any, or new_document passed as a callable, keeps the tuple overloads'
# types: first, it would make the one a union of both returns, so Any, and the other a bare _D. Without
# `strict`, so that the type is the one way to state it: IDFDocumentV9_4[Literal[False]].
@overload
def new_document(version: type[_D], *, normalize_choices: bool = ...) -> _D: ...


# The overloads carry the types; these annotations stay built-in, which costs pyright nothing at each call
# and keeps typing.get_type_hints working at run time.
def new_document(
    version: tuple[int, int, int] | type[object] = LATEST_VERSION,
    *,
    strict: bool = True,
    normalize_choices: bool = True,
) -> object:
    """
    Create a new IDFDocument with baseline singleton objects populated.

    Args:
        version: The EnergyPlus release, as a version tuple (default: the latest
            supported release) or as a release's document type from
            :mod:`idfkit.versioned`. Given a type, such as ``IDFDocumentV9_4``, the
            document is created for the release the type stands for and typed as
            that type; a non-strict one is asked for by the type,
            ``IDFDocumentV9_4[Literal[False]]``. Given a tuple, it is typed for the
            latest release whatever the version, since a type checker does not read
            the tuple. ``IDFDocument`` is refused, and so is the latest release's
            type in :mod:`idfkit.versioned`, which is ``IDFDocument``: it is the
            run-time class of every document, so ``new_document(type(doc))`` would
            create a document of the latest release whatever ``doc``'s. Call
            ``new_document()`` for the latest release. ``simulate()`` runs a model
            only on an EnergyPlus of its release (or a newer one, with
            ``auto_migrate=True``), so to simulate on an older installed EnergyPlus,
            create the model at its release: ``new_document(version=idfkit.simulation.find_energyplus().version)``.
        strict: When ``True``, accessing or setting an unknown field name on any
            IDFObject raises :class:`~idfkit.exceptions.InvalidFieldError` instead
            of returning ``None``.
        normalize_choices: When ``True`` (the default), a choice value passed to ``add()``
            or assigned to a field is stored in the spelling its schema declares:
            ``roughness="ROUGH"`` reads back ``"Rough"``. ``False`` stores it as given.

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

        Create a model typed for an older release, naming the release once:

        >>> from typing import Literal
        >>> from idfkit.versioned import IDFDocumentV9_4
        >>> legacy = new_document(IDFDocumentV9_4)
        >>> legacy.version
        (9, 4, 0)
        >>> new_document(IDFDocumentV9_4[Literal[False]]).strict
        False
    """
    if not isinstance(version, tuple):
        from ._document_types import is_type_form, release_for_new_document

        # Anything else is left to the version check, which raises TypeError for a non-tuple such as "26.1".
        if is_type_form(version):
            version, strict = release_for_new_document(version, strict)
    _check_version(version)
    schema = get_schema(version)
    doc = IDFDocument(version=version, schema=schema, strict=strict, normalize_choices=normalize_choices)

    # Seed core singleton objects for a minimal baseline model.
    version_identifier = f"{version[0]}.{version[1]}"
    doc["Version"].add(version_identifier=version_identifier)
    doc["Building"].add("Building")
    doc["SimulationControl"].add()
    doc["GlobalGeometryRules"].add(
        starting_vertex_position="UpperLeftCorner",
        vertex_entry_direction="Counterclockwise",
        coordinate_system="Relative",
    )
    return doc


__all__ = [
    "ASHRAE_PERIMETER_DEPTH",
    "CONFORMANCE_LEVEL",
    "ENERGYPLUS_VERSIONS",
    "LATEST_VERSION",
    "MINIMUM_VERSION",
    "AppliedRules",
    "DocsUrl",
    "DuplicateObjectError",
    "EnergyPlusNotFoundError",
    "EpJSONSchema",
    "ExpandObjectsError",
    "FieldDescription",
    "FileFormatError",
    "HorizontalAdjacency",
    "IDFCollection",
    "IDFDocument",
    "IDFObject",
    "IDFParseError",
    "IDFParser",
    "IdfKitError",
    "InvalidFieldError",
    "MatchOptions",
    "MatchReport",
    "MigrationError",
    "MigrationReport",
    "MissingRequiredFieldError",
    "NoDesignDaysError",
    "ObjectDescription",
    "ObjectNotFoundError",
    "ParseError",
    "ParseResult",
    "Polygon3D",
    "RangeError",
    "ReferenceGraph",
    "ResolvedSurface",
    "ResultLookupError",
    "Scene",
    "SceneBounds",
    "SchemaManager",
    "SchemaNotFoundError",
    "SimulationError",
    "SourceSpan",
    "UnattemptedType",
    "UnknownObjectTypeError",
    "UnresolvedObject",
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
    "counter_clockwise_footprint",
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
    "get_scene",
    "get_schema",
    "get_schema_manager",
    "intersect_and_match",
    "intersect_match",
    "io_reference_url",
    "is_supported_version",
    "link_blocks",
    "link_horizontal_surfaces",
    "load_epjson",
    "load_idf",
    "load_idf_with_diagnostics",
    "migrate",
    "new_document",
    "parse_epjson",
    "parse_idf",
    "polygon_area_2d",
    "polygon_contains_2d",
    "polygon_difference_2d",
    "polygon_intersection_2d",
    "rotate_building",
    "save_epjson",
    "save_idf",
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

# FR-008: assembly artefacts are deleted, not registered. These names are bound at module scope
# only so that the module can be assembled, they are absent from ``__all__``, and leaving them
# bound leaks them into ``dir(idfkit)`` and into editor completion on ``idfkit.``. The unbinding
# goes through ``globals()`` rather than a plain ``del``: a plain ``del`` at module scope makes
# every static analyser treat the name as unbound for the whole module, so the ``Literal`` and
# ``overload`` annotations above stop resolving. Deleting through the namespace dict removes the
# names at runtime, which is where the leak is, and leaves the annotations intact.
for _assembly_artefact in ("PackageNotFoundError", "TYPE_CHECKING", "Literal", "annotations", "logging", "overload"):
    globals().pop(_assembly_artefact, None)
globals().pop("_assembly_artefact", None)
