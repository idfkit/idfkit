"""
On-demand validation system for IDF documents.

Provides validation against EpJSON schema without requiring
eager validation during parsing.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, cast

from ._finite import NON_FINITE_DETAIL, non_finite_fields
from ._surface_types import is_fenestration_door
from .exceptions import closest_names
from .objects import IDFObject, is_blank_slot

__all__ = [
    "Severity",
    "ValidationError",
    "ValidationResult",
    "validate_document",
    "validate_object",
]

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

    from .document import AnyIDFDocument
    from .schema import EpJSONSchema, ReferenceKin


class Severity(Enum):
    """Validation issue severity levels."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass(init=False)
class ValidationError:
    """
    Represents a validation issue.

    Attributes:
        severity: Issue severity (ERROR, WARNING, INFO)
        obj_type: Object type where issue was found
        obj_name: Object name where issue was found
        field: Field name where issue was found (if applicable)
        message: Human-readable description
        code: Machine-readable error code
        obj: The object the issue was found on, or ``None`` for a document-level
            issue. Types without a Name field (``HVACTemplate:Zone:*``,
            ``Output:Variable``, ...) have an empty ``obj_name``; use ``obj`` to
            find, highlight or fix the object itself. It is a plain attribute,
            not a dataclass field: ``dataclasses.asdict``/``astuple``, equality
            and pickling leave it out (pickling or deep-copying an error drops
            it), so serializing errors never copies the owning document.
    """

    severity: Severity
    obj_type: str
    obj_name: str
    field: str | None
    message: str
    code: str

    def __init__(
        self,
        severity: Severity,
        obj_type: str,
        obj_name: str,
        field: str | None,
        message: str,
        code: str,
        obj: IDFObject | None = None,
    ) -> None:
        self.severity = severity
        self.obj_type = obj_type
        self.obj_name = obj_name
        self.field = field
        self.message = message
        self.code = code
        # Not a dataclass field, so asdict()/astuple()/eq/repr/pickle leave it out (see docstring).
        self.obj: IDFObject | None = obj

    def __getstate__(self) -> dict[str, Any]:
        state = dict(self.__dict__)
        state["obj"] = None
        return state

    def __copy__(self) -> ValidationError:
        return ValidationError(
            self.severity, self.obj_type, self.obj_name, self.field, self.message, self.code, obj=self.obj
        )

    def __str__(self) -> str:
        if not self.obj_name and self.obj is not None:
            # A nameless object reads as its repr, which names it by its first set fields.
            location = repr(self.obj)
        else:
            location = f"{self.obj_type}:'{self.obj_name}'"
        if self.field:
            location += f".{self.field}"
        return f"[{self.severity.value.upper()}] {location}: {self.message}"


@dataclass
class ValidationResult:
    """
    Result of document validation.

    Attributes:
        errors: List of validation errors
        warnings: List of validation warnings
        info: List of informational messages
    """

    errors: list[ValidationError]
    warnings: list[ValidationError]
    info: list[ValidationError]

    @property
    def is_valid(self) -> bool:
        """True if there are no errors."""
        return len(self.errors) == 0

    @property
    def total_issues(self) -> int:
        """Total number of issues found."""
        return len(self.errors) + len(self.warnings) + len(self.info)

    def __str__(self) -> str:
        lines = [f"Validation: {len(self.errors)} errors, {len(self.warnings)} warnings"]
        for err in self.errors[:10]:
            lines.append(f"  {err}")
        if len(self.errors) > 10:
            lines.append(f"  ... and {len(self.errors) - 10} more errors")
        return "\n".join(lines)

    def __bool__(self) -> bool:
        return self.is_valid


def validate_document(  # noqa: C901
    doc: AnyIDFDocument,
    schema: EpJSONSchema | None = None,
    check_references: bool = True,
    check_required: bool = True,
    check_types: bool = True,
    check_ranges: bool = True,
    check_singletons: bool = True,
    object_types: list[str] | None = None,
    check_geometry: bool = True,
) -> ValidationResult:
    """
    Validate an IDF document against schema.

    Args:
        doc: The document to validate
        schema: Schema to validate against (uses doc's schema if not provided)
        check_references: Check reference integrity (``E009``; a missing ``ScheduleTypeLimits``,
            which EnergyPlus only warns about, is ``W006``), and that each window or glass door
            names a window construction rather than an opaque one (``E013``)
        check_required: Check required fields, and report a group-only object such as
            ``OutdoorAir:NodeList`` that has no entries (``W004``)
        check_types: Check field types
        check_ranges: Check numeric ranges
        check_singletons: Check singleton (maxProperties) constraints
        object_types: Only validate these types (None = all)
        check_geometry: Warn about a floor whose vertices make it face up, or a roof or
            ceiling that faces down (``W005``): the surface is upside down, as a clockwise
            footprint extruded into an inside-out zone is, and EnergyPlus runs it with
            only a warning and a wrong zone volume

    Returns:
        ValidationResult with all issues found

    Examples:
        Validate a model before running a simulation:

        >>> from idfkit import new_document, validate_document
        >>> model = new_document()
        >>> model.add("Zone", "Perimeter_ZN_1")  # doctest: +ELLIPSIS
        Zone('Perimeter_ZN_1')
        >>> result = validate_document(model)
        >>> result.is_valid
        True
        >>> result.total_issues
        0

        Validate only material and construction definitions:

        >>> result = validate_document(model, object_types=["Material", "Construction"])
        >>> result.is_valid
        True
    """
    schema = schema or doc.schema

    errors: list[ValidationError] = []
    warnings: list[ValidationError] = []
    info: list[ValidationError] = []

    if schema is None:
        warnings.append(
            ValidationError(
                severity=Severity.WARNING,
                obj_type="Document",
                obj_name="",
                field=None,
                message="No schema available - skipping schema validation",
                code="W001",
            )
        )
        return ValidationResult(errors, warnings, info)

    # Determine which object types to validate
    types_to_check = object_types or list(doc.collections.keys())
    logger.debug("Validating %d object type(s)", len(types_to_check))

    # Check singleton (maxProperties) constraints
    if check_singletons:
        for obj_type in types_to_check:
            if obj_type not in doc.collections:
                continue
            obj_schema = schema.get_object_schema(obj_type)
            if obj_schema and obj_schema.get("maxProperties") == 1:
                coll = doc.get_collection(obj_type)
                count = len(coll)
                if count > 1:
                    first = coll.first()
                    obj_name = first.name if first and first.name else obj_type
                    errors.append(
                        ValidationError(
                            severity=Severity.ERROR,
                            obj_type=obj_type,
                            obj_name=obj_name,
                            obj=first,
                            field=None,
                            message=f"Singleton type '{obj_type}' has {count} instances (maximum 1 allowed)",
                            code="E010",
                        )
                    )

    for obj_type in types_to_check:
        if obj_type not in doc.collections:
            continue

        # W004 is checked here and not in `_validate_object`: `add()` refuses any finding that
        # function makes, and an empty group-only object is a normal step in building one up. Only
        # the finished model is wrong to hold it. Whether the type is group-only is read once.
        group_only = _group_only_type(schema, obj_type) if check_required else None

        for obj in doc.get_collection(obj_type):
            obj_errors = _validate_object(
                obj,
                schema,
                check_required=check_required,
                check_types=check_types,
                check_ranges=check_ranges,
            )
            if group_only is not None:
                empty = _empty_group_only_object(obj, group_only)
                if empty is not None:
                    obj_errors.append(empty)

            for err in obj_errors:
                if err.severity == Severity.ERROR:
                    errors.append(err)
                elif err.severity == Severity.WARNING:
                    warnings.append(err)
                else:
                    info.append(err)

    if check_geometry:
        warnings.extend(_validate_surface_orientation(doc, types_to_check))

    # Schedules EnergyPlus refuses as fatal although every field is valid on its own
    for err in _validate_schedules(doc, types_to_check, check_ranges=check_ranges):
        errors.append(err)

    # Check reference integrity
    if check_references:
        errors.extend(_validate_window_constructions(doc, types_to_check))
        ref_errors = _validate_references(doc, schema)
        for err in ref_errors:
            if err.severity == Severity.ERROR:
                errors.append(err)
            elif err.severity == Severity.WARNING:
                warnings.append(err)

    result = ValidationResult(errors, warnings, info)
    logger.info(
        "Validation complete: %d error(s), %d warning(s), %d info",
        len(errors),
        len(warnings),
        len(info),
    )
    return result


#: Schedule types whose values ``_schedule_values`` reads, for the type-limits check (``E012``).
_LIMITED_SCHEDULE_TYPES = ("Schedule:Compact", "Schedule:Constant")


def _validate_schedules(doc: AnyIDFDocument, types_to_check: list[str], *, check_ranges: bool) -> list[ValidationError]:
    """Report schedules EnergyPlus terminates on although each field is valid on its own.

    ``E011``: a ``Schedule:Compact`` that does not cover the year through ``12/31``, or a day
    through ``Until: 24:00``. ``E012`` (with *check_ranges*): a ``Schedule:Compact`` or
    ``Schedule:Constant`` value outside the lower or upper limit of its ``ScheduleTypeLimits``.
    """
    from .schedules.compact import compact_problems

    findings: list[ValidationError] = []
    if "Schedule:Compact" in types_to_check:
        for obj in doc["Schedule:Compact"]:
            try:
                problems = compact_problems(obj)
            except ValueError as e:
                problems = [f"it cannot be read ({e})"]
            findings.extend(
                ValidationError(
                    severity=Severity.ERROR,
                    obj_type=obj.obj_type,
                    obj_name=obj.name,
                    obj=obj,
                    field="data",
                    message=f"{problem[:1].upper()}{problem[1:]}; EnergyPlus stops on this schedule",
                    code="E011",
                )
                for problem in problems
            )
    if check_ranges:
        for obj_type in _LIMITED_SCHEDULE_TYPES:
            if obj_type not in types_to_check:
                continue
            for obj in doc.get_collection(obj_type):
                finding = _schedule_limit_failure(doc, obj)
                if finding is not None:
                    findings.append(finding)
    return findings


#: Surface types read by the orientation check (``W005``), with the field that holds the surface
#: type (``None``: the type itself says it).
_HORIZONTAL_SURFACE_TYPES: dict[str, str | None] = {
    "BuildingSurface:Detailed": "surface_type",
    "Floor:Detailed": None,
    "RoofCeiling:Detailed": None,
}


def _validate_surface_orientation(doc: AnyIDFDocument, types_to_check: list[str]) -> list[ValidationError]:
    """``W005`` for a floor that faces up, or a roof or ceiling that faces down.

    A floor's outward normal points down (tilt 180) and a roof's or ceiling's up (tilt 0).
    The tilt is read from the vertex order under the document's ``GlobalGeometryRules``
    entry direction; a sloped surface is reported only once it faces the wrong half-space.
    """
    from .geometry import get_surface_coords
    from .geometry_builders import get_geometry_convention

    found: list[ValidationError] = []
    clockwise: bool | None = None
    for obj_type, type_field in _HORIZONTAL_SURFACE_TYPES.items():
        if obj_type not in types_to_check or obj_type not in doc.collections:
            continue
        for obj in doc.get_collection(obj_type):
            kind = str(obj.get(type_field) or "").lower() if type_field else obj_type.split(":")[0].lower()
            if kind not in ("floor", "roof", "ceiling", "roofceiling"):
                continue
            try:
                poly = get_surface_coords(obj)
            except (TypeError, ValueError):
                continue  # a non-numeric vertex is the type check's to report (E003)
            if poly is None or poly.area <= 0:
                continue
            if clockwise is None:
                clockwise = get_geometry_convention(doc)[1]
            tilt = 180.0 - poly.tilt if clockwise else poly.tilt
            if kind == "floor" and tilt < 89.0:
                expected, facing = "down (tilt 180)", "up"
            elif kind != "floor" and tilt > 91.0:
                expected, facing = "up (tilt 0)", "down"
            else:
                continue
            found.append(
                ValidationError(
                    severity=Severity.WARNING,
                    obj_type=obj_type,
                    obj_name=obj.name,
                    obj=obj,
                    field="vertices",
                    message=(
                        f"{'Floor' if kind == 'floor' else 'Roof/ceiling'} faces {facing} (tilt {tilt:.0f}), "
                        f"its outward normal should point {expected}: the vertices are in reverse order, "
                        "as a clockwise footprint gives. EnergyPlus reports the surface as upside down "
                        "and computes a wrong zone volume"
                    ),
                    code="W005",
                )
            )
    return found


#: Fenestration types whose construction EnergyPlus requires to be a window construction (``E013``).
#: A ``FenestrationSurface:Detailed`` is one unless its surface type is ``Door``.
_GLAZED_FENESTRATION_TYPES = (
    "FenestrationSurface:Detailed",
    "Window",
    "GlazedDoor",
    "Window:Interzone",
    "GlazedDoor:Interzone",
)

#: Material types EnergyPlus treats as opaque layers. A construction of these alone is opaque;
#: any ``WindowMaterial:*`` layer makes it a window construction.
_OPAQUE_MATERIAL_TYPES = (
    "Material",
    "Material:NoMass",
    "Material:AirGap",
    "Material:InfraredTransparent",
    "Material:RoofVegetation",
)


def _construction_layers(construction: IDFObject) -> list[str]:
    """The layer names of a ``Construction``, outside first, upper-cased as collections index them."""
    names = [construction.data.get("outside_layer")]
    names.extend(construction.data.get(f"layer_{i}") for i in range(2, 11))
    return [name.upper() for name in names if isinstance(name, str) and name]


def _opaque_construction_names(doc: AnyIDFDocument) -> set[str]:
    """The upper-cased names of each ``Construction`` whose every layer is an opaque material."""
    opaque: set[str] = set()
    window: set[str] = set()
    for material_type, materials in doc.collections.items():
        if material_type in _OPAQUE_MATERIAL_TYPES:
            opaque.update(obj.name.upper() for obj in materials)
        elif material_type.startswith("WindowMaterial:"):
            window.update(obj.name.upper() for obj in materials)
    only_opaque = opaque - window
    names: set[str] = set()
    for construction in doc.collections.get("Construction", ()):
        layers = _construction_layers(construction)
        if layers and all(layer in only_opaque for layer in layers):
            names.add(construction.name.upper())
    return names


def _needs_window_construction(obj: IDFObject) -> bool:
    """Whether *obj* is glazed fenestration: anything but a ``FenestrationSurface:Detailed`` door."""
    return not is_fenestration_door(obj)


def _validate_window_constructions(doc: AnyIDFDocument, types_to_check: list[str]) -> list[ValidationError]:
    """``E013`` for a window or glass door whose ``Construction`` has only opaque layers.

    Each field is valid and the reference resolves, but EnergyPlus stops in ``GetSurfaceData``
    ("has an opaque surface construction"). Only a construction whose every layer names an opaque
    material is reported: a missing layer is ``E009``'s, and other construction types are not read.
    """
    fenestration = [t for t in _GLAZED_FENESTRATION_TYPES if t in types_to_check and t in doc.collections]
    if not fenestration or "Construction" not in doc.collections:
        return []
    opaque = _opaque_construction_names(doc)
    return [
        ValidationError(
            severity=Severity.ERROR,
            obj_type=obj.obj_type,
            obj_name=obj.name,
            obj=obj,
            field="construction_name",
            message=(
                f"Construction '{obj.data['construction_name']}' has only opaque layers, but a window needs a "
                "window construction (a WindowMaterial layer); EnergyPlus stops on this surface"
            ),
            code="E013",
        )
        for obj_type in fenestration
        for obj in doc.collections[obj_type]
        if isinstance(obj.data.get("construction_name"), str)
        and str(obj.data["construction_name"]).upper() in opaque
        and _needs_window_construction(obj)
    ]


def _as_number(value: Any) -> float | None:
    """*value* as a float when it is an int or float (not a bool), else ``None``."""
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def _schedule_values(obj: IDFObject) -> list[float]:
    """The values a ``Schedule:Compact`` or ``Schedule:Constant`` can take."""
    if obj.obj_type == "Schedule:Constant":
        value = _as_number(obj.data.get("hourly_value"))
        return [] if value is None else [value]
    from .schedules.compact import parse_compact

    periods, _ = parse_compact(obj)
    values: list[float] = []
    for period in periods:
        values.extend(tv.value for rule in period.day_rules for tv in rule.time_values)
        if (period.end_month, period.end_day) == (12, 31):
            break  # EnergyPlus ignores the periods after the one that reaches 12/31
    return values


def _schedule_limit_failure(doc: AnyIDFDocument, obj: IDFObject) -> ValidationError | None:
    """``E012`` for the first value of *obj* outside its ``ScheduleTypeLimits``, if any."""
    limits_name = obj.data.get("schedule_type_limits_name")
    if not isinstance(limits_name, str) or not limits_name or limits_name not in doc["ScheduleTypeLimits"]:
        return None
    limits = doc["ScheduleTypeLimits"][limits_name]
    lower = _as_number(limits.data.get("lower_limit_value"))
    upper = _as_number(limits.data.get("upper_limit_value"))
    if lower is None and upper is None:
        return None
    try:
        schedule_values = _schedule_values(obj)
    except ValueError:
        return None  # E011 reports a schedule that cannot be read
    for value in schedule_values:
        if (lower is not None and value < lower) or (upper is not None and value > upper):
            low = "-inf" if lower is None else f"{lower:g}"
            high = "inf" if upper is None else f"{upper:g}"
            return ValidationError(
                severity=Severity.ERROR,
                obj_type=obj.obj_type,
                obj_name=obj.name,
                obj=obj,
                field="schedule_type_limits_name",
                message=(
                    f"Value {value:g} is outside the limits [{low}, {high}] of ScheduleTypeLimits "
                    f"'{limits.name}'; EnergyPlus stops on this schedule"
                ),
                code="E012",
            )
    return None


def validate_object(
    obj: IDFObject,
    schema: EpJSONSchema,
    *,
    check_required: bool = True,
    check_types: bool = True,
    check_ranges: bool = True,
    check_unknown: bool = True,
) -> list[ValidationError]:
    """
    Validate a single object against schema.

    This is a public API for validating individual objects, useful for
    checking objects at creation time with the validate=True option.

    Args:
        obj: The IDFObject to validate
        schema: The EpJSON schema to validate against
        check_required: Check that required fields are present
        check_types: Check that field values match expected types
        check_ranges: Check that numeric values are within bounds
        check_unknown: Check for unknown fields (not in schema)

    Returns:
        List of ValidationError objects describing any issues found

    Examples:
        Check a newly created zone for schema violations:

        >>> from idfkit import new_document, validate_object, get_schema, LATEST_VERSION
        >>> model = new_document()
        >>> zone = model.add("Zone", "Perimeter_ZN_1")
        >>> errors = validate_object(zone, get_schema(LATEST_VERSION))
        >>> len(errors)
        0
    """
    return _validate_object(
        obj,
        schema,
        check_required=check_required,
        check_types=check_types,
        check_ranges=check_ranges,
        check_unknown=check_unknown,
    )


def field_value_error(obj: IDFObject, field_name: str, value: Any, schema: EpJSONSchema) -> ValidationError | None:
    """The finding *value* would raise as *obj*'s *field_name*, or None when the schema accepts it.

    The type, choice and range checks ``add()`` applies to each value, for one value about to be
    assigned. A blank value clears the field and is not checked, nor is a field the schema does not
    know: whether a name is a field is the caller's question (strict mode, or ``update()``).
    """
    rules = _object_rules(schema, obj.obj_type)
    if rules is None or is_blank_slot(value):
        return None
    rule = rules.fields.get(field_name)
    if rule is None:
        return None
    if type(value) in rule.accepts_outright:
        return None
    if type(value) is str and value.lower() in rule.accepts_folded:
        return None
    return rule.first_error(obj, field_name, value)


def name_error(obj: IDFObject, value: str, schema: EpJSONSchema) -> ValidationError | None:
    """The finding renaming *obj* to *value* would raise, or None when the schema accepts the name.

    A blank or whitespace name on a type whose schema requires one is refused, as ``add()`` refuses it.
    """
    if value.strip():
        return None
    rules = _object_rules(schema, obj.obj_type)
    if rules is None or not rules.name_required:
        return None
    return _missing_name_error(obj)


def _missing_name_error(obj: IDFObject) -> ValidationError:
    """E001 on the name of *obj*, whose type requires one."""
    return ValidationError(
        severity=Severity.ERROR,
        obj_type=obj.obj_type,
        obj_name=obj.name,
        obj=obj,
        field="name",
        message="Required field 'name' is missing",
        code="E001",
    )


def _validate_object(  # noqa: C901
    obj: IDFObject,
    schema: EpJSONSchema,
    check_required: bool = True,
    check_types: bool = True,
    check_ranges: bool = True,
    check_unknown: bool = True,
) -> list[ValidationError]:
    """Validate a single object against schema."""
    errors: list[ValidationError] = []
    obj_type = obj.obj_type

    rules = _object_rules(schema, obj_type)
    if rules is None:
        # Unknown object type
        errors.append(
            ValidationError(
                severity=Severity.WARNING,
                obj_type=obj_type,
                obj_name=obj.name,
                obj=obj,
                field=None,
                message=f"Unknown object type '{obj_type}'",
                code="W002",
            )
        )
        return errors

    data = obj.data
    field_rules = rules.fields

    # Check required fields
    if check_required:
        # The name sits outside `data`, so the loop below never sees it. A blank name on a type
        # whose schema requires one is written as a bare `Zone,`, which EnergyPlus refuses.
        if rules.name_required and not obj.name.strip():
            errors.append(_missing_name_error(obj))
        for field_name in rules.required:
            value = data.get(field_name)
            if value is None or value == "":
                errors.append(
                    ValidationError(
                        severity=Severity.ERROR,
                        obj_type=obj_type,
                        obj_name=obj.name,
                        obj=obj,
                        field=field_name,
                        message=f"Required field '{field_name}' is missing",
                        code="E001",
                    )
                )
        if rules.group_required is not None:
            errors.extend(_missing_group_keys(obj, *rules.group_required))

    # Check field types and ranges
    for field_name, value in data.items():
        rule = field_rules.get(field_name)
        if rule is None:
            # Unknown field, whatever its value. Valid flat extensible spellings were folded into
            # the wrapper key on the way in (add(), the epJSON parser), and the wrapper key is a
            # known field, so anything left is unknown.
            if check_unknown:
                errors.append(
                    ValidationError(
                        severity=Severity.WARNING,
                        obj_type=obj_type,
                        obj_name=obj.name,
                        obj=obj,
                        field=field_name,
                        message=f"Unknown field '{field_name}'",
                        code="W003",
                    )
                )
            continue
        if value is None or value == "":
            continue
        if check_types and (non_finite := _non_finite_error(obj, field_name, value)) is not None:
            errors.extend(non_finite)
            continue

        # Most fields constrain nothing but their type, and most values already have it;
        # most of the rest are choice fields answered by one lookup in the folded enum.
        if type(value) in rule.accepts_outright:
            continue
        if type(value) is str and value.lower() in rule.accepts_folded:
            continue

        error = rule.first_error(obj, field_name, value, check_types=check_types, check_ranges=check_ranges)
        if error is not None:
            errors.append(error)

    return errors


def _missing_group_keys(obj: IDFObject, wrapper: str, required: tuple[str, ...]) -> list[ValidationError]:
    """``E001`` for each required key an extensible group of *obj* does not give.

    The field is named as the group reads it, ``vertices[2].vertex_z_coordinate``. Reading such a
    key raises [MissingRequiredFieldError][idfkit.exceptions.MissingRequiredFieldError] where every release requires it,
    so ``add()`` refuses the group as it refuses an object without a required field.
    """
    groups: Any = obj.data.get(wrapper)
    if not isinstance(groups, list):
        return []
    errors: list[ValidationError] = []
    for index, group in enumerate(cast("list[Any]", groups)):
        if not isinstance(group, dict):
            continue
        slot = cast("dict[str, Any]", group)
        for key in required:
            if is_blank_slot(slot.get(key)):
                field = f"{wrapper}[{index}].{key}"
                errors.append(
                    ValidationError(
                        severity=Severity.ERROR,
                        obj_type=obj.obj_type,
                        obj_name=obj.name,
                        obj=obj,
                        field=field,
                        message=f"Required field '{field}' is missing",
                        code="E001",
                    )
                )
    return errors


@dataclass(frozen=True, slots=True)
class _GroupOnly:
    """What ``W004`` needs from a group-only type.

    Attributes:
        wrapper: The epJSON key of the type's extensible group.
        required: The first field every entry of the group must give, or None when none is required.
    """

    wrapper: str
    required: str | None


def _group_only_type(schema: EpJSONSchema, obj_type: str) -> _GroupOnly | None:
    """The group of *obj_type* when it is a group-only type, or ``None``.

    A group-only type is a nameless type whose only field is an extensible group:
    ``Output:Diagnostics``, ``Output:Table:SummaryReports``, ``OutdoorAir:NodeList`` and
    ``EnergyManagementSystem:GlobalVariable``.
    """
    cache = schema.get_parsing_cache(obj_type)
    # ``all_field_names`` lists the fixed fields only; the wrapper is an epJSON key and never one.
    if cache is None or cache.has_name or not cache.ext_wrapper_key or cache.all_field_names:
        return None
    wrapper = cache.ext_wrapper_key
    # Resolved, since the parsing cache is case-insensitive and the schema lookups are not.
    canonical = schema.resolve_type_name(obj_type) or obj_type
    props: dict[str, Any] = (schema.get_inner_schema(canonical) or {}).get("properties", {})
    items: dict[str, Any] = props.get(wrapper, {}).get("items", {})
    required: list[str] = items.get("required", [])
    return _GroupOnly(wrapper=wrapper, required=required[0] if required else None)


def _holds_a_value(group: Any) -> bool:
    """Whether an extensible *group* gives anything: a dict whose slots are all blank gives nothing."""
    if not isinstance(group, dict):
        return True
    return not all(map(is_blank_slot, cast("dict[str, Any]", group).values()))


def _empty_group_only_object(obj: IDFObject, group_only: _GroupOnly) -> ValidationError | None:
    """``W004`` for a group-only object with no entry that gives a value, or ``None``.

    Holding no entries, or only blank ones, a group-only object says nothing. EnergyPlus runs it in
    epJSON exactly as it runs the model without it, so it is almost always a model left unfinished or
    a group given under a key the type does not have.

    It is also an object IDF cannot carry. The writer spells it ``Type,;``, since ``Type;`` would run
    on into the next object, and EnergyPlus reads that as one blank group: a warning for
    ``Output:Diagnostics``, a Severe for ``Output:Table:SummaryReports``, and refused input for the
    two types whose group has a required field. A list of blank groups is written the same way, as
    the writer trims the blank values, so it is reported too.
    """
    wrapper = group_only.wrapper
    groups = obj.data.get(wrapper)
    if groups and not isinstance(groups, list):
        return None  # Not a list at all, which the type check reports.
    if any(map(_holds_a_value, cast("list[Any]", groups or []))):
        return None
    message = (
        f"'{obj.obj_type}' has no '{wrapper}' entries, so it does nothing in EnergyPlus. Give it at "
        "least one entry or remove it. Written to IDF it becomes one blank entry, which EnergyPlus "
    )
    if group_only.required:
        message += f"refuses because '{group_only.required}' is required."
    else:
        message += "warns about or reports as invalid."
    return ValidationError(
        severity=Severity.WARNING,
        obj_type=obj.obj_type,
        obj_name=obj.name,
        obj=obj,
        field=wrapper,
        message=message,
        code="W004",
    )


def _validate_field(  # pyright: ignore[reportUnusedFunction]
    obj: IDFObject,
    field_name: str,
    value: Any,
    field_schema: dict[str, Any],
    *,
    check_types: bool = True,
    check_ranges: bool = True,
) -> list[ValidationError]:
    """Validate one field value against its raw schema, emitting **at most one** finding.

    This is the entry point for callers holding a schema dict rather than a compiled
    [_FieldRule][idfkit.validation._FieldRule]; ``_validate_object`` uses the compiled
    rules directly. Both go through the same checking code.

    Type, enum and bounds used to be checked by two independently-called helpers, which
    both under-reported (an ``anyOf`` field's constraints live inside its branches and
    were never read) and, once the constraints were read, would have double-reported the
    same field.

    ``anyOf`` fields follow ordinary JSON Schema semantics: the value is valid when it
    *fully* satisfies at least one branch — that branch's type, its ``enum`` if it has
    one, and its bounds if it has any.
    """
    error = _compile_field_rule(field_schema).first_error(
        obj,
        field_name,
        value,
        check_types=check_types,
        check_ranges=check_ranges,
    )
    return [] if error is None else [error]


def _any_of_failure(
    obj: IDFObject,
    field_name: str,
    value: Any,
    branches: tuple[_FieldRule, ...],
    *,
    check_types: bool,
    check_ranges: bool,
) -> ValidationError | None:
    """Apply the ``anyOf`` rule, returning at most one finding.

    1. Collect the branches whose *type* the value satisfies.
    2. Empty set — the value is of no acceptable type: ``E002``.
    3. Any collected branch also satisfying its enum and its bounds — valid.
    4. Otherwise report the first collected branch's most specific failure, using the
       same codes a non-``anyOf`` field would use. Reporting ``E002`` for an
       out-of-range number would tell the user their number is not a number.
    """
    matched = [branch for branch in branches if branch.matches_type(value)]

    if not matched:
        if not check_types:
            return None
        return ValidationError(
            severity=Severity.ERROR,
            obj_type=obj.obj_type,
            obj_name=obj.name,
            obj=obj,
            field=field_name,
            message=f"Value '{value}' does not match any valid type",
            code="E002",
        )

    failures: list[ValidationError] = []
    for branch in matched:
        failure = _branch_constraint_failure(
            obj,
            field_name,
            value,
            branch,
            check_types=check_types,
            check_ranges=check_ranges,
        )
        if failure is None:
            # This branch is fully satisfied, so the value is valid.
            return None
        failures.append(failure)

    # Declaration order: the first branch the value matched on type reports the failure.
    first = failures[0]
    if first.code == "E004" and isinstance(value, str):
        # A string the numeric branch refused and the choice branch did not list. Naming only the
        # choices, ``not in allowed values: ['', 'Autocalculate']``, hides that a number was expected.
        kinds = [b.expected_type for b in branches if b.expected_type in ("number", "integer")]
        if kinds:
            kind = "a number" if "number" in kinds else "an integer"
            choices = [c for b in matched for c in (b.enum or []) if c != ""]
            options = " or ".join(repr(c) for c in choices)
            first.message = f"Expected {kind} or {options}, got '{value}'" if options else first.message
    return first


def _branch_constraint_failure(
    obj: IDFObject,
    field_name: str,
    value: Any,
    branch: _FieldRule,
    *,
    check_types: bool,
    check_ranges: bool,
) -> ValidationError | None:
    """Return the most specific constraint failure for one already type-matched branch.

    ``None`` means the branch is fully satisfied. A disabled check counts as satisfied.
    """
    if check_types and branch.enum is not None and not branch.matches_enum(value):
        return ValidationError(
            severity=Severity.ERROR,
            obj_type=obj.obj_type,
            obj_name=obj.name,
            obj=obj,
            field=field_name,
            message=f"Value '{value}' not in allowed values: {branch.enum}",
            code="E004",
        )

    if check_ranges and branch.bounds and _is_numeric(value):
        return _first_bound_failure(obj, field_name, value, branch.bounds)

    return None


def _non_finite_error(obj: IDFObject, field_name: str, value: Any) -> list[ValidationError] | None:
    """``E003`` for each NaN or infinity in *value*, a field's value or its extensible groups.

    ``None`` (not an empty list) when there is none, which is the answer for any value that is not
    a float or a list, so the per-field cost is two type checks. A NaN satisfies ``number`` and
    every bound compares false against it, so the type and range checks would pass it.
    """
    if isinstance(value, float):
        if math.isfinite(value):
            return None
        found = [(field_name, value)]
    elif isinstance(value, list):
        found = list(non_finite_fields({field_name: value}))
        if not found:
            return None
    else:
        return None
    return [
        ValidationError(
            severity=Severity.ERROR,
            obj_type=obj.obj_type,
            obj_name=obj.name,
            obj=obj,
            field=name,
            message=f"Expected a finite number, got {bad!r}; {NON_FINITE_DETAIL}",
            code="E003",
        )
        for name, bad in found
    ]


def _is_numeric(value: Any) -> bool:
    """True for an int or float, but not for a bool (``True`` is not a number here)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_integral(value: Any) -> bool:
    """True for an int, or a float with no fractional part, but not for a bool."""
    if isinstance(value, bool):
        return False
    return isinstance(value, int) or (isinstance(value, float) and value.is_integer())


def _is_text(value: Any) -> bool:
    """True for a string."""
    return isinstance(value, str)


def _is_boolean(value: Any) -> bool:
    """True for a bool."""
    return isinstance(value, bool)


def _is_array(value: Any) -> bool:
    """True for a list."""
    return isinstance(value, list)


def _is_mapping(value: Any) -> bool:
    """True for a dict."""
    return isinstance(value, dict)


#: One predicate per JSON Schema ``type`` this validator understands. A ``type`` that is
#: absent, unrecognised, or a list of types constrains nothing and matches any value.
_TYPE_TESTS: dict[str, Callable[[Any], bool]] = {
    "number": _is_numeric,
    "integer": _is_integral,
    "string": _is_text,
    "boolean": _is_boolean,
    "array": _is_array,
    "object": _is_mapping,
}

#: The Python types each JSON Schema ``type`` accepts *exactly*, for the fast path in
#: [_validate_object][idfkit.validation._validate_object]. Only exact types, never
#: subclasses: ``bool`` is deliberately absent from ``number`` and ``integer``, and a
#: ``str`` subclass falls through to the predicate above, which still accepts it.
#: ``integer`` omits ``float`` because a float has to be checked for a fractional part.
_EXACT_TYPES: dict[str, frozenset[type]] = {
    "number": frozenset({int, float}),
    "integer": frozenset({int}),
    "string": frozenset({str}),
    "boolean": frozenset({bool}),
    "array": frozenset({list}),
    "object": frozenset({dict}),
}


@dataclass(frozen=True, slots=True)
class _Bound:
    """One numeric bound, resolved from either JSON Schema dialect at compile time.

    ``relation`` and ``code`` are the wording and the finding code this bound reports,
    so a violation needs no further reasoning about which dialect it came from.
    """

    limit: float
    exclusive: bool
    is_maximum: bool
    code: str
    relation: str

    def violated_by(self, value: float) -> bool:
        """Whether *value* falls outside this bound."""
        if self.is_maximum:
            return value >= self.limit if self.exclusive else value > self.limit
        return value <= self.limit if self.exclusive else value < self.limit


@dataclass(frozen=True, slots=True)
class _FieldRule:
    """The constraints of one field schema, resolved once instead of on every value.

    A field schema is read the same way for every object of its type, so the reading is
    done once per (schema version, object type, field) and cached. What is left at
    validation time is the comparison itself.

    Attributes:
        expected_type: The raw ``type`` keyword, kept only for the ``E003`` message.
        type_test: Predicate for ``expected_type``, or None when nothing constrains type.
        enum: The allowed values, or None when the field has no ``enum``.
        enum_folded: ``enum`` lowercased, for the case-insensitive string comparison.
        bounds: The numeric bounds, in the order they report.
        branches: The compiled ``anyOf`` branches, or None for an ordinary field.
        accepts_outright: Python types that settle this field on their own, because the
            type is all the rule constrains. Empty whenever anything else must be read.
        accepts_folded: Folded strings that settle this field on their own, because a
            listed choice is all the rule constrains. Empty unless it is a choice field.
    """

    expected_type: Any
    type_test: Callable[[Any], bool] | None
    enum: list[Any] | None
    enum_folded: frozenset[str]
    bounds: tuple[_Bound, ...]
    branches: tuple[_FieldRule, ...] | None
    accepts_outright: frozenset[type]
    accepts_folded: frozenset[str]

    def matches_type(self, value: Any) -> bool:
        """Whether *value* satisfies this rule's ``type``.

        Only the type is considered: ``enum`` and bounds are constraints checked once the
        branch is known to match on type, never a reason for it not to match. A schema with
        no ``type`` constrains nothing here and matches any value.
        """
        test = self.type_test
        return test is None or test(value)

    def matches_enum(self, value: Any) -> bool:
        """Enum membership: strings compare case-insensitively, numbers compare by value.

        For a string, folded membership subsumes exact membership — an exact member
        lowercases into ``enum_folded`` too — so one set lookup answers both.
        """
        enum = self.enum
        if enum is None:
            return True
        if isinstance(value, str):
            return value.lower() in self.enum_folded
        return value in enum

    def first_error(
        self,
        obj: IDFObject,
        field_name: str,
        value: Any,
        *,
        check_types: bool = True,
        check_ranges: bool = True,
    ) -> ValidationError | None:
        """Validate one value against this rule, reporting **at most one** finding.

        Type failure outranks enum failure, which outranks a bounds failure: telling a
        user their string is out of range would be answering a question they did not ask.
        """
        branches = self.branches
        if branches is not None:
            return _any_of_failure(
                obj,
                field_name,
                value,
                branches,
                check_types=check_types,
                check_ranges=check_ranges,
            )

        if check_types:
            test = self.type_test
            if test is not None and not test(value):
                return ValidationError(
                    severity=Severity.ERROR,
                    obj_type=obj.obj_type,
                    obj_name=obj.name,
                    obj=obj,
                    field=field_name,
                    message=f"Expected {self.expected_type}, got {type(value).__name__}",
                    code="E003",
                )
            if self.enum is not None and not self.matches_enum(value):
                return ValidationError(
                    severity=Severity.ERROR,
                    obj_type=obj.obj_type,
                    obj_name=obj.name,
                    obj=obj,
                    field=field_name,
                    message=f"Value '{value}' not in allowed values: {self.enum}",
                    code="E004",
                )

        # A field with no bounds cannot fail on range, so it need not be inspected at all.
        if check_ranges and self.bounds and _is_numeric(value):
            return _first_bound_failure(obj, field_name, value, self.bounds)

        return None


def _compile_bounds(field_schema: dict[str, Any]) -> tuple[_Bound, ...]:
    """Resolve a field schema's numeric bounds, in the order they report.

    Handles both JSON Schema dialects EnergyPlus has shipped. Schemas for 8.9.0
    through 9.5.0 are draft-04, where ``exclusiveMinimum``/``exclusiveMaximum``
    are *booleans* that make the sibling ``minimum``/``maximum`` exclusive. From
    9.6.0 on they are draft-06+, where the same keys hold the bound itself.
    Comparing a value against the draft-04 boolean would silently treat it as
    ``1``, rejecting every value at or below 1 in a positive-bounded field.
    """
    exclusive_min = field_schema.get("exclusiveMinimum")
    exclusive_max = field_schema.get("exclusiveMaximum")
    # draft-04: the flag qualifies `minimum`/`maximum` rather than carrying a bound.
    min_is_exclusive = exclusive_min is True
    max_is_exclusive = exclusive_max is True

    bounds: list[_Bound] = []
    if "minimum" in field_schema:
        bounds.append(
            _Bound(
                limit=field_schema["minimum"],
                exclusive=min_is_exclusive,
                is_maximum=False,
                code="E006" if min_is_exclusive else "E005",
                relation="must be greater than" if min_is_exclusive else "is below minimum",
            )
        )
    # draft-06+, where the key carries the bound
    if isinstance(exclusive_min, (int, float)) and not isinstance(exclusive_min, bool):
        bounds.append(
            _Bound(
                limit=exclusive_min,
                exclusive=True,
                is_maximum=False,
                code="E006",
                relation="must be greater than",
            )
        )
    if "maximum" in field_schema:
        bounds.append(
            _Bound(
                limit=field_schema["maximum"],
                exclusive=max_is_exclusive,
                is_maximum=True,
                code="E008" if max_is_exclusive else "E007",
                relation="must be less than" if max_is_exclusive else "is above maximum",
            )
        )
    # draft-06+, where the key carries the bound
    if isinstance(exclusive_max, (int, float)) and not isinstance(exclusive_max, bool):
        bounds.append(
            _Bound(
                limit=exclusive_max,
                exclusive=True,
                is_maximum=True,
                code="E008",
                relation="must be less than",
            )
        )
    return tuple(bounds)


def _compile_field_rule(field_schema: dict[str, Any]) -> _FieldRule:
    """Read one field schema into the constraints it imposes."""
    branches = field_schema.get("anyOf")
    if branches is not None:
        return _FieldRule(
            expected_type=None,
            type_test=None,
            enum=None,
            enum_folded=frozenset(),
            bounds=(),
            branches=tuple(_compile_field_rule(branch) for branch in branches),
            accepts_outright=frozenset(),
            accepts_folded=frozenset(),
        )

    expected_type = field_schema.get("type")
    named_type = expected_type if isinstance(expected_type, str) else ""
    enum: list[Any] | None = field_schema.get("enum")
    enum_folded: frozenset[str] = frozenset() if enum is None else frozenset(str(m).lower() for m in enum)
    bounds = _compile_bounds(field_schema)
    unconstrained_beyond_type = enum is None and not bounds
    # A string always satisfies a "string" type, and a typeless rule constrains no type at
    # all, so in both cases a listed choice settles the field.
    choice_only = enum is not None and not bounds and named_type in ("string", "")
    return _FieldRule(
        expected_type=expected_type,
        type_test=_TYPE_TESTS.get(named_type),
        enum=enum,
        enum_folded=enum_folded,
        bounds=bounds,
        branches=None,
        accepts_outright=_EXACT_TYPES.get(named_type, frozenset()) if unconstrained_beyond_type else frozenset(),
        accepts_folded=enum_folded if choice_only else frozenset(),
    )


def _bound_error(obj: IDFObject, field_name: str, value: float, bound: _Bound) -> ValidationError:
    """Build the finding for one violated bound."""
    return ValidationError(
        severity=Severity.ERROR,
        obj_type=obj.obj_type,
        obj_name=obj.name,
        obj=obj,
        field=field_name,
        message=f"Value {value} {bound.relation} {bound.limit}",
        code=bound.code,
    )


def _first_bound_failure(
    obj: IDFObject,
    field_name: str,
    value: float,
    bounds: tuple[_Bound, ...],
) -> ValidationError | None:
    """Report the first bound *value* violates, if any."""
    for bound in bounds:
        if bound.violated_by(value):
            return _bound_error(obj, field_name, value, bound)
    return None


def _validate_field_type(  # pyright: ignore[reportUnusedFunction]
    obj: IDFObject,
    field_name: str,
    value: Any,
    field_schema: dict[str, Any],
) -> list[ValidationError]:
    """Report every type and enum violation of a field with a single schema (no ``anyOf``).

    ``anyOf`` fields are handled by ``_any_of_failure``, which weighs type, enum and
    bounds together per branch; routing them here would check the type of one branch
    against the constraints of another.
    """
    rule = _compile_field_rule(field_schema)
    errors: list[ValidationError] = []

    expected_type = rule.expected_type
    if expected_type and not rule.matches_type(value):
        errors.append(
            ValidationError(
                severity=Severity.ERROR,
                obj_type=obj.obj_type,
                obj_name=obj.name,
                obj=obj,
                field=field_name,
                message=f"Expected {expected_type}, got {type(value).__name__}",
                code="E003",
            )
        )

    if rule.enum is not None and not rule.matches_enum(value):
        errors.append(
            ValidationError(
                severity=Severity.ERROR,
                obj_type=obj.obj_type,
                obj_name=obj.name,
                obj=obj,
                field=field_name,
                message=f"Value '{value}' not in allowed values: {rule.enum}",
                code="E004",
            )
        )

    return errors


def _validate_field_range(  # pyright: ignore[reportUnusedFunction]
    obj: IDFObject,
    field_name: str,
    value: float | int,
    field_schema: dict[str, Any],
) -> list[ValidationError]:
    """Report every numeric bound of *field_schema* that *value* violates."""
    return [
        _bound_error(obj, field_name, value, bound)
        for bound in _compile_bounds(field_schema)
        if bound.violated_by(value)
    ]


@dataclass(frozen=True, slots=True)
class _ObjectRules:
    """Everything the per-object loop needs from one object type's schema.

    Attributes:
        fields: Compiled rule per known field. A field absent here is an unknown field.
        required: Names the schema marks required.
        contributing: Fields carrying ``reference``, so their value declares a name.
        group_required: The extensible wrapper key and the keys the schema marks required, with no
            default, in each of its groups, or None when the type has no group or its groups require
            nothing.
        name_required: Whether the schema marks the type's Name ``is_required``.
    """

    fields: dict[str, _FieldRule]
    required: set[str]
    contributing: tuple[str, ...]
    group_required: tuple[str, tuple[str, ...]] | None = None
    name_required: bool = False


# Compiled object-type rules, keyed by schema version then object type.
_OBJECT_RULES: dict[tuple[int, int, int], dict[str, _ObjectRules]] = {}


def _object_rules(schema: EpJSONSchema, obj_type: str) -> _ObjectRules | None:
    """Return the compiled rules for *obj_type*, or None if the schema does not know it."""
    by_type = _OBJECT_RULES.get(schema.version)
    if by_type is None:
        # ``setdefault`` rather than a plain store, so threads validating at once share one table
        # instead of each overwriting the last one's.
        by_type = _OBJECT_RULES.setdefault(schema.version, {})

    rules = by_type.get(obj_type)
    if rules is not None:
        return rules

    inner_schema = schema.get_inner_schema(obj_type)
    if not inner_schema:
        return None

    properties: dict[str, Any] = inner_schema.get("properties", {})
    rules = _ObjectRules(
        # A falsy field schema was treated as an unknown field before compilation existed;
        # leaving it out of `fields` keeps that. ParsingCache.known_keys applies the same rule.
        fields={name: _compile_field_rule(spec) for name, spec in properties.items() if spec},
        required=set(inner_schema.get("required", [])),
        contributing=tuple(name for name, spec in properties.items() if spec and spec.get("reference")),
        group_required=_group_required(schema, obj_type, properties),
        name_required=_name_required(schema, obj_type),
    )
    by_type[obj_type] = rules
    return rules


def _name_required(schema: EpJSONSchema, obj_type: str) -> bool:
    """Whether *obj_type*'s schema marks its Name ``is_required``; False for a type without a Name field."""
    outer: dict[str, Any] = schema.get_object_schema(obj_type) or {}
    name_spec: dict[str, Any] = outer.get("name") or {}
    return bool(name_spec.get("is_required"))


def _group_required(
    schema: EpJSONSchema, obj_type: str, properties: dict[str, Any]
) -> tuple[str, tuple[str, ...]] | None:
    """The wrapper key of *obj_type*'s extensible group and the keys each group must give, if any.

    A key the schema requires but gives a default (``surrounding_surface_view_factor``) is left out:
    EnergyPlus applies the default to a group without it, the group's item type does not require it,
    and ``add()`` accepts the group as it accepts an object without such a field.
    """
    pc = schema.get_parsing_cache(obj_type)
    wrapper = pc.ext_wrapper_key if pc is not None else None
    if not wrapper:
        return None
    items: dict[str, Any] = properties.get(wrapper, {}).get("items", {})
    keys: dict[str, Any] = items.get("properties", {})
    required = tuple(key for key in items.get("required", []) if "default" not in keys.get(key, {}))
    return (wrapper, required) if required else None


# Reference lists that no field anywhere in a schema contributes to, keyed by schema version.
_UNPOPULATED_LISTS: dict[tuple[int, int, int], frozenset[str]] = {}


def _unpopulated_reference_lists(schema: EpJSONSchema) -> frozenset[str]:
    """Return the reference lists nothing in *schema* can ever put a name into.

    A field carrying ``object_list`` points into a reference list; a field or a name carrying
    ``reference`` contributes to one. Four lists in the EnergyPlus schema are pointed into and
    never contributed to, all of the form ``valid*EquipmentTypes``. They enumerate object TYPE
    names, not object names, so ``component_1_object_type = "OutdoorAir:Mixer"`` is a correct
    value that no object in the document will ever declare. Reporting those as dangling accuses
    a valid model of naming something that does not exist.
    """
    cached = _UNPOPULATED_LISTS.get(schema.version)
    if cached is not None:
        return cached

    contributed: set[str] = set()
    pointed: set[str] = set()

    def scan(properties: dict[str, Any]) -> None:
        for spec in properties.values():
            contributed.update(spec.get("reference", ()) or ())
            pointed.update(spec.get("object_list", ()) or ())
            if spec.get("type") == "array":
                scan(spec.get("items", {}).get("properties", {}))

    for obj_type in schema.object_types:
        outer: dict[str, Any] = schema.get_object_schema(obj_type) or {}
        name_spec: dict[str, Any] = outer.get("name") or {}
        name_refs: list[str] = name_spec.get("reference") or []
        contributed.update(name_refs)
        scan((schema.get_inner_schema(obj_type) or {}).get("properties", {}))

    result = frozenset(pointed - contributed)
    _UNPOPULATED_LISTS[schema.version] = result
    return result


def _is_zonelist_expanded_name(target: str, container_names: set[str], valid_names: set[str]) -> bool:
    """Whether *target* looks like a name EnergyPlus produced by expanding a ZoneList.

    An object assigned to a ``ZoneList`` (or a ``SpaceList``) is expanded by EnergyPlus into
    one instance per member, named ``<member name>`` + a single space + ``<object name>``. A
    reference may legitimately point at one of those instances, and no object in the file
    declares that name. ``5ZoneAirCooledDemandLimiting.idf`` does exactly this: an
    ``ElectricEquipment`` named ``AllZones with Electric Equipment`` is assigned to a
    ``ZoneList``, and a ``DemandManager:ElectricEquipment`` then references
    ``Space1-1 AllZones with Electric Equipment``. The schema documents the convention on the
    field itself: "if ZoneList option is used on the ElectricEquipment object, a single
    equipment object from that assignment can be selected by entering
    ``<Zone Name><space><Global ElectricEquipment Object Name>``".

    Every space is tried as the split point, not only the first: zone names and object names
    both routinely contain spaces.

    This is deliberately an approximation. It does not verify that the referenced object is
    actually assigned to a ZoneList that contains that zone, which would be stricter and more
    correct. The simpler rule cannot produce a false negative on a valid model, which is what
    matters here, and the precise version needs ZoneList membership resolution that the Python
    and TypeScript libraries do not share today.

    Args:
        target: The uppercased reference target that matched no declared name
        container_names: Uppercased names declared by ``Zone`` and ``Space`` objects
        valid_names: Every uppercased name the document declares

    Returns:
        True if some split of *target* at a space yields a zone/space prefix and a declared suffix.
    """
    parts = target.split(" ")
    for split in range(1, len(parts)):
        prefix = " ".join(parts[:split])
        if prefix not in container_names:
            continue
        if " ".join(parts[split:]) in valid_names:
            return True
    return False


def _is_implicit_remainder_space(target: str, zone_names: set[str]) -> bool:
    """Whether *target* names the implicit space EnergyPlus adds to a partly-spaced zone.

    When a ``Zone`` carries ``Space`` objects that do not cover all of its surfaces,
    EnergyPlus creates one more space for the leftovers and names it ``<Zone Name>-Remainder``,
    hyphen-joined. No object declares that name, and references to it are valid.
    ``5ZoneAirCooledWithSpacesHVAC.idf`` does this: ``Zone 5`` declares the spaces
    ``Space 5 Office`` and ``Space 5 Conference``, and ``Zone 5-Remainder`` is referenced
    twelve times without ever being declared.

    Separate from [_is_zonelist_expanded_name][idfkit.validation._is_zonelist_expanded_name],
    not a case of it: ``Zone 5-Remainder`` is joined with a hyphen, so splitting it at its
    spaces yields the prefix ``Zone`` and the suffix ``5-Remainder``, neither of which any
    object declares, and the ZoneList rule correctly declines it.

    Args:
        target: The uppercased reference target that matched no declared name
        zone_names: Uppercased names declared by ``Zone`` objects

    Returns:
        True if *target* is a declared zone name followed by the literal ``-Remainder``.
    """
    suffix = "-REMAINDER"
    if not target.endswith(suffix):
        return False
    return target[: -len(suffix)] in zone_names


#: Built-in fluid names EnergyPlus resolves without a ``FluidProperties:Name``, by the reference
#: list a field looks them up in, uppercased. A glycol lookup (a loop's or secondary system's
#: user-defined fluid) finds only ``Water``: ``EthyleneGlycol`` there stops the run ("User Defined
#: Fluid Type = ETHYLENEGLYCOL, item not found"), since the built-in glycols are reached through a
#: ``FluidProperties:GlycolConcentration``. A refrigerant lookup finds only ``Steam``.
_BUILTIN_NAMES: dict[str, frozenset[str]] = {
    "FluidNames": frozenset({"STEAM"}),
    "FluidAndGlycolNames": frozenset({"WATER"}),
}

#: Fields that give property data for a fluid, where every built-in fluid resolves: a
#: ``FluidProperties:Concentration`` for ``PropyleneGlycol`` (SupermarketSecondary.idf) needs no
#: ``FluidProperties:Name`` to declare it.
_BUILTIN_FLUID_DATA_FIELDS: frozenset[tuple[str, str]] = frozenset({
    ("FLUIDPROPERTIES:CONCENTRATION", "fluid_name"),
    ("FLUIDPROPERTIES:SATURATED", "fluid_name"),
    ("FLUIDPROPERTIES:SUPERHEATED", "fluid_name"),
})
_BUILTIN_FLUIDS = frozenset({"WATER", "STEAM", "ETHYLENEGLYCOL", "PROPYLENEGLYCOL"})


def _is_builtin_name(obj: IDFObject, field_name: str, lists: tuple[str, ...], target: str) -> bool:
    """Whether EnergyPlus defines the uppercased *target* itself for *field_name* of *obj*."""
    if (obj.obj_type.upper(), field_name) in _BUILTIN_FLUID_DATA_FIELDS:
        return target in _BUILTIN_FLUIDS
    return any(target in _BUILTIN_NAMES.get(name, ()) for name in lists)


#: Reference lists whose missing target EnergyPlus only warns about. A schedule naming a
#: ``ScheduleTypeLimits`` that does not exist runs, its values unchecked against limits.
_WARN_ONLY_LISTS: dict[tuple[str, ...], str] = {
    ("ScheduleTypeLimitsNames",): "W006",
}


def _choice(obj: IDFObject, field_name: str, default: str) -> str:
    """The uppercased choice *obj* holds in *field_name*, or *default* when it is blank."""
    value = obj.data.get(field_name)
    return value.strip().upper() if isinstance(value, str) and value.strip() else default.upper()


def _afn_wind_pressure_input(doc: AnyIDFDocument) -> bool:
    """Whether ``AirflowNetwork:SimulationControl`` asks for user-input wind pressure coefficients."""
    control = doc.collections.get("AirflowNetwork:SimulationControl")
    first = control.first() if control is not None else None
    return (
        first is not None and _choice(first, "wind_pressure_coefficient_type", "SurfaceAverageCalculation") == "INPUT"
    )


#: Modes in which an AirflowNetwork zone or surface reads its temperature setpoint schedule.
_AFN_SETPOINT_MODES = frozenset({"TEMPERATURE", "ENTHALPY", "ADJACENTTEMPERATURE", "ADJACENTENTHALPY"})

#: Reference fields EnergyPlus reads only in some modes, with the test of whether *obj* is in one.
#: A name left in a field the chosen mode ignores is never looked up, so it cannot dangle:
#: CrossVent_1Zone_AirflowNetwork.idf keeps a setpoint schedule that does not exist on a zone
#: whose ventilation is ``Constant``, and runs without a severe error.
_MODE_GATED_FIELDS: dict[tuple[str, str], Callable[[AnyIDFDocument, IDFObject], bool]] = {
    ("AIRFLOWNETWORK:MULTIZONE:ZONE", "ventilation_control_zone_temperature_setpoint_schedule_name"): (
        lambda _doc, obj: _choice(obj, "ventilation_control_mode", "NoVent") in _AFN_SETPOINT_MODES
    ),
    ("AIRFLOWNETWORK:MULTIZONE:SURFACE", "ventilation_control_zone_temperature_setpoint_schedule_name"): (
        lambda _doc, obj: _choice(obj, "ventilation_control_mode", "ZoneLevel") in _AFN_SETPOINT_MODES
    ),
    ("AIRFLOWNETWORK:MULTIZONE:SURFACE", "external_node_name"): lambda doc, _obj: _afn_wind_pressure_input(doc),
}


def _field_in_use(doc: AnyIDFDocument, obj: IDFObject, field_name: str) -> bool:
    """Whether EnergyPlus reads *field_name* of *obj*, given the modes *obj* and *doc* choose."""
    gate = _MODE_GATED_FIELDS.get((obj.obj_type.upper(), field_name))
    return gate is None or gate(doc, obj)


@dataclass(frozen=True)
class _DeclaredNames:
    """The uppercased names a document declares, split by what each set is used for."""

    #: Every name any object declares, whether through its name field or a `reference` field.
    all_names: set[str]
    #: Names a ZoneList/SpaceList expansion can prefix an object name with: Zone and Space.
    containers: set[str]
    #: Zone names, the only thing an implicit remainder space can be built from.
    zones: set[str]
    #: Reference list -> the names declared into it. A reference field accepts only these.
    by_list: dict[str, set[str]]
    #: Name -> the object types that declare it, for the message when a field names the wrong type.
    types_by_name: dict[str, set[str]]
    #: Name -> the reference lists it is declared into.
    lists_by_name: dict[str, set[str]]


def _contributed_lists(schema: EpJSONSchema, obj_type: str, field_name: str) -> list[str]:
    """The reference lists a field carrying ``reference`` declares its value into."""
    spec = schema.get_field_schema(obj_type, field_name) or {}
    return list(spec.get("reference") or [])


def _declared_names(doc: AnyIDFDocument, schema: EpJSONSchema) -> _DeclaredNames:
    """Collect the names a document declares.

    An object usually declares its name through its name field, but not always. A field may
    carry `reference`, meaning it CONTRIBUTES its value to a reference list, as opposed to
    `object_list`, which points into one. Anonymous types have no name field at all and
    declare themselves this way: `FluidProperties:Name` names a refrigerant through its
    `fluid_name` field, and `FluidProperties:Superheated` then points at it. Collecting only
    `obj.name` makes those declarations invisible and reports every reference to them as
    dangling. Eleven fields in the 26.1.0 schema declare a reference this way.
    """
    declared = _DeclaredNames(
        all_names=set(), containers=set(), zones=set(), by_list={}, types_by_name={}, lists_by_name={}
    )

    def declare(name_upper: str, obj_type: str, lists: Iterable[str]) -> None:
        declared.all_names.add(name_upper)
        declared.types_by_name.setdefault(name_upper, set()).add(obj_type)
        name_lists = declared.lists_by_name.setdefault(name_upper, set())
        for ref_list in lists:
            name_lists.add(ref_list)
            declared.by_list.setdefault(ref_list, set()).add(name_upper)

    for obj_type, collection in doc.collections.items():
        rules = _object_rules(schema, obj_type)
        contributing = [
            (field_name, _contributed_lists(schema, obj_type, field_name))
            for field_name in (rules.contributing if rules is not None else ())
        ]
        type_upper = obj_type.upper()
        # A type without a Name field declares nothing through ``obj.name``: a name stored on
        # one is dropped on write, so a reference to it would dangle in EnergyPlus.
        type_has_name = schema.has_name(obj_type)
        name_lists = schema.get_name_reference_lists(obj_type)
        for obj in collection:
            if type_has_name and obj.name:
                name_upper = obj.name.upper()
                declare(name_upper, obj_type, name_lists)
                if type_upper in ("ZONE", "SPACE"):
                    declared.containers.add(name_upper)
                if type_upper == "ZONE":
                    declared.zones.add(name_upper)
            for field_name, lists in contributing:
                value = obj.data.get(field_name)
                if isinstance(value, str) and value:
                    declare(value.upper(), obj_type, lists)
    return declared


class _ReferenceResolver:
    """Decides, per reference, whether its field's ``object_list`` accepts the name it holds.

    Holds the per-field and per-list lookups, so a document with thousands of references to a
    few lists reads the schema once per field and builds each accepted-name set once.
    """

    def __init__(self, schema: EpJSONSchema, declared: _DeclaredNames) -> None:
        self._schema = schema
        self._declared = declared
        self._unpopulated = _unpopulated_reference_lists(schema)
        self._lists_by_field: dict[tuple[str, str], tuple[str, ...]] = {}
        # None for lists that accept any declared name: no object_list, or one mixing type-name
        # lists nothing populates with name lists.
        self._valid_by_lists: dict[tuple[str, ...], set[str] | None] = {}
        self._kin_by_lists: dict[tuple[str, ...], ReferenceKin] = {}

    def field_lists(self, obj_type: str, field_name: str) -> tuple[str, ...]:
        """The ``object_list`` of a reference field, inside an extensible group or not."""
        key = (obj_type, field_name)
        lists = self._lists_by_field.get(key)
        if lists is None:
            lists = tuple(self._schema.get_reference_field_object_list(obj_type, field_name) or ())
            self._lists_by_field[key] = lists
        return lists

    def _valid_names(self, lists: tuple[str, ...]) -> set[str]:
        if lists not in self._valid_by_lists:
            if not lists or any(name in self._unpopulated for name in lists):
                self._valid_by_lists[lists] = None
            else:
                by_list = self._declared.by_list
                self._valid_by_lists[lists] = set[str]().union(*(by_list.get(name, set()) for name in lists))
        valid = self._valid_by_lists[lists]
        return self._declared.all_names if valid is None else valid

    def _akin(self, lists: tuple[str, ...], target: str, types: list[str]) -> bool:
        kin = self._kin_by_lists.get(lists)
        if kin is None:
            kin = self._kin_by_lists[lists] = self._schema.get_reference_kin(lists)
        target_lists = self._declared.lists_by_name.get(target, set())
        return any(kin.admits(obj_type, target_lists) for obj_type in types)

    def resolves(self, lists: tuple[str, ...], target: str) -> bool:
        """Whether a field with *lists* accepts the uppercased name *target*."""
        # A field whose every list is unpopulated names object TYPES, which no object declares.
        if lists and all(name in self._unpopulated for name in lists):
            return True
        if target in self._valid_names(lists):
            return True
        declared = self._declared
        types = self.declaring_types(target)
        if types and self._akin(lists, target, types):
            return True
        return _is_zonelist_expanded_name(target, declared.containers, declared.all_names) or (
            _is_implicit_remainder_space(target, declared.zones)
        )

    def declaring_types(self, target: str) -> list[str]:
        """The object types that declare the uppercased name *target*, sorted."""
        return sorted(self._declared.types_by_name.get(target, ()))


def _validate_references(
    doc: AnyIDFDocument,
    schema: EpJSONSchema,
) -> list[ValidationError]:
    """Validate all object references.

    A reference resolves to a name in one of its field's ``object_list`` reference lists, or to an
    object akin to them (see [ReferenceKin][idfkit.schema.ReferenceKin]), as EnergyPlus resolves
    it. A schedule field naming a Zone, or a construction field naming a Material, is as broken as
    one naming nothing: EnergyPlus rejects both.
    """
    errors: list[ValidationError] = []
    resolver = _ReferenceResolver(schema, _declared_names(doc, schema))
    candidates_by_lists: dict[tuple[str, ...], list[str]] = {}
    # Removing one widely referenced object leaves thousands of edges to the same target: the
    # did-you-mean search runs once per (target, reference lists), not once per edge.
    suggestions: dict[tuple[str, tuple[str, ...]], list[str]] = {}
    for obj, field_name, target in doc.references.iter_references():
        key = resolver.field_lists(obj.obj_type, field_name)
        if (
            resolver.resolves(key, target)
            or _is_builtin_name(obj, field_name, key, target)
            or not _field_in_use(doc, obj, field_name)
        ):
            continue
        lists = list(key)
        if key not in candidates_by_lists:
            candidates_by_lists[key] = _reference_candidates(doc, schema, lists)
        value = _typed_value(obj, field_name, target)
        suggestion_key = (target, key)
        if suggestion_key not in suggestions:
            suggestions[suggestion_key] = closest_names(value, candidates_by_lists[key], n=3)
        message = _dangling_message(value, lists, suggestions[suggestion_key], resolver.declaring_types(target))
        warn_code = _WARN_ONLY_LISTS.get(key)
        if warn_code is not None:
            stop = "" if message.endswith("?") else "."
            message = f"{message}{stop} EnergyPlus only warns, and does not check the values against limits"
        errors.append(
            ValidationError(
                severity=Severity.ERROR if warn_code is None else Severity.WARNING,
                obj_type=obj.obj_type,
                obj_name=obj.name,
                obj=obj,
                field=field_name,
                message=message,
                code=warn_code or "E009",
            )
        )

    return errors


def _typed_value(obj: IDFObject, field_name: str, target: str) -> str:
    """The value *obj* holds for the reference *target*, as the user typed it.

    The reference graph keys a reference by its uppercased value; the message quotes the field's
    own spelling. A field inside an extensible group is found in the object's groups.
    """
    values: list[Any] = [obj.data.get(field_name)]
    for group_list in obj.data.values():
        if isinstance(group_list, list):
            values.extend(
                cast("dict[str, Any]", group).get(field_name)
                for group in cast("list[Any]", group_list)
                if isinstance(group, dict)
            )
    for value in values:
        if isinstance(value, str) and value.strip().upper() == target:
            return value.strip()
    return target


def _reference_candidates(doc: AnyIDFDocument, schema: EpJSONSchema, lists: list[str]) -> list[str]:
    """The names the document's objects give the reference lists *lists*, the field's ``object_list``."""
    names: dict[str, str] = {}
    for ref_list in lists:
        for obj_type in schema.get_types_providing_reference(ref_list):
            collection = doc.collections.get(obj_type)
            if collection is None:
                continue
            for candidate in collection:
                if candidate.name:
                    names.setdefault(candidate.name.upper(), candidate.name)
    return list(names.values())


def _dangling_message(value: str, lists: list[str], close: list[str], wrong_types: list[str] | None = None) -> str:
    """The E009 message: the missing name, the reference list it was looked up in, and the closest names.

    *wrong_types* are the object types that do declare the name, when it exists but is not in
    any of the field's reference lists.
    """
    if wrong_types:
        kinds = " and ".join(f"{'an' if t[0] in 'AEIOU' else 'a'} {t}" for t in wrong_types)
        message = f"Reference to '{value}', which is {kinds}"
        if lists:
            message += f", not in {' or '.join(lists)}"
    else:
        message = f"Reference to non-existent object '{value}'"
        if lists:
            message += f" (looked up in {' or '.join(lists)})"
    if close:
        message += ". Did you mean " + " or ".join(f"'{name}'" for name in close) + "?"
    return message
