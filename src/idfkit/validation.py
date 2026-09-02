"""
On-demand validation system for IDF documents.

Provides validation against EpJSON schema without requiring
eager validation during parsing.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, cast

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .document import IDFDocument
    from .objects import IDFObject
    from .schema import EpJSONSchema


class Severity(Enum):
    """Validation issue severity levels."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
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
    """

    severity: Severity
    obj_type: str
    obj_name: str
    field: str | None
    message: str
    code: str

    def __str__(self) -> str:
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
    doc: IDFDocument,
    schema: EpJSONSchema | None = None,
    check_references: bool = True,
    check_required: bool = True,
    check_types: bool = True,
    check_ranges: bool = True,
    check_singletons: bool = True,
    object_types: list[str] | None = None,
) -> ValidationResult:
    """
    Validate an IDF document against schema.

    Args:
        doc: The document to validate
        schema: Schema to validate against (uses doc's schema if not provided)
        check_references: Check reference integrity
        check_required: Check required fields
        check_types: Check field types
        check_ranges: Check numeric ranges
        check_singletons: Check singleton (maxProperties) constraints
        object_types: Only validate these types (None = all)

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
                            field=None,
                            message=f"Singleton type '{obj_type}' has {count} instances (maximum 1 allowed)",
                            code="E010",
                        )
                    )

    for obj_type in types_to_check:
        if obj_type not in doc.collections:
            continue

        for obj in doc.get_collection(obj_type):
            obj_errors = _validate_object(
                obj,
                schema,
                check_required=check_required,
                check_types=check_types,
                check_ranges=check_ranges,
            )

            for err in obj_errors:
                if err.severity == Severity.ERROR:
                    errors.append(err)
                elif err.severity == Severity.WARNING:
                    warnings.append(err)
                else:
                    info.append(err)

    # Check reference integrity
    if check_references:
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


def _validate_object(
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
    obj_name = obj.name

    inner_schema = schema.get_inner_schema(obj_type)
    if not inner_schema:
        # Unknown object type
        errors.append(
            ValidationError(
                severity=Severity.WARNING,
                obj_type=obj_type,
                obj_name=obj_name,
                field=None,
                message=f"Unknown object type '{obj_type}'",
                code="W002",
            )
        )
        return errors

    properties = inner_schema.get("properties", {})
    required = set(inner_schema.get("required", []))

    # Check required fields
    if check_required:
        for field_name in required:
            value = obj.data.get(field_name)
            if value is None or value == "":
                errors.append(
                    ValidationError(
                        severity=Severity.ERROR,
                        obj_type=obj_type,
                        obj_name=obj_name,
                        field=field_name,
                        message=f"Required field '{field_name}' is missing",
                        code="E001",
                    )
                )

    # Check field types and ranges
    for field_name, value in obj.data.items():
        if value is None or value == "":
            continue

        field_schema = properties.get(field_name)
        if not field_schema:
            # Unknown field - could be extensible or error
            if check_unknown and not schema.is_extensible(obj_type):
                errors.append(
                    ValidationError(
                        severity=Severity.WARNING,
                        obj_type=obj_type,
                        obj_name=obj_name,
                        field=field_name,
                        message=f"Unknown field '{field_name}'",
                        code="W003",
                    )
                )
            continue

        errors.extend(
            _validate_field(
                obj,
                field_name,
                value,
                field_schema,
                check_types=check_types,
                check_ranges=check_ranges,
            )
        )

    return errors


def _validate_field(
    obj: IDFObject,
    field_name: str,
    value: Any,
    field_schema: dict[str, Any],
    *,
    check_types: bool = True,
    check_ranges: bool = True,
) -> list[ValidationError]:
    """Validate one field value against its schema, emitting **at most one** finding.

    This is the single entry point for per-field checks. Type, enum and bounds used
    to be checked by two independently-called helpers, which both under-reported
    (an ``anyOf`` field's constraints live inside its branches and were never read)
    and, once the constraints were read, would have double-reported the same field.

    ``anyOf`` fields follow ordinary JSON Schema semantics: the value is valid when it
    *fully* satisfies at least one branch — that branch's type, its ``enum`` if it has
    one, and its bounds if it has any.
    """
    if "anyOf" in field_schema:
        return _validate_any_of_field(
            obj,
            field_name,
            value,
            field_schema["anyOf"],
            check_types=check_types,
            check_ranges=check_ranges,
        )

    errors: list[ValidationError] = []
    if check_types:
        errors = _validate_field_type(obj, field_name, value, field_schema)
    if not errors and check_ranges and _is_numeric(value):
        errors = _validate_field_range(obj, field_name, value, field_schema)
    return errors[:1]


def _validate_any_of_field(
    obj: IDFObject,
    field_name: str,
    value: Any,
    branches: list[dict[str, Any]],
    *,
    check_types: bool = True,
    check_ranges: bool = True,
) -> list[ValidationError]:
    """Apply the ``anyOf`` rule, emitting at most one finding.

    1. Collect the branches whose *type* the value satisfies.
    2. Empty set — the value is of no acceptable type: ``E002``.
    3. Any collected branch also satisfying its enum and its bounds — valid.
    4. Otherwise report the first collected branch's most specific failure, using the
       same codes a non-``anyOf`` field would use. Reporting ``E002`` for an
       out-of-range number would tell the user their number is not a number.
    """
    matched = [branch for branch in branches if _value_matches_type(value, branch)]

    if not matched:
        if not check_types:
            return []
        return [
            ValidationError(
                severity=Severity.ERROR,
                obj_type=obj.obj_type,
                obj_name=obj.name,
                field=field_name,
                message=f"Value '{value}' does not match any valid type",
                code="E002",
            )
        ]

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
            return []
        failures.append(failure)

    # Declaration order: the first branch the value matched on type reports the failure.
    return failures[:1]


def _branch_constraint_failure(
    obj: IDFObject,
    field_name: str,
    value: Any,
    branch: dict[str, Any],
    *,
    check_types: bool,
    check_ranges: bool,
) -> ValidationError | None:
    """Return the most specific constraint failure for one already type-matched branch.

    ``None`` means the branch is fully satisfied. A disabled check counts as satisfied.
    """
    if check_types and "enum" in branch and not _value_matches_enum(value, branch["enum"]):
        return ValidationError(
            severity=Severity.ERROR,
            obj_type=obj.obj_type,
            obj_name=obj.name,
            field=field_name,
            message=f"Value '{value}' not in allowed values: {branch['enum']}",
            code="E004",
        )

    if check_ranges and _is_numeric(value):
        range_errors = _validate_field_range(obj, field_name, value, branch)
        if range_errors:
            return range_errors[0]

    return None


def _is_numeric(value: Any) -> bool:
    """True for an int or float, but not for a bool (``True`` is not a number here)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _value_matches_enum(value: Any, enum: list[Any]) -> bool:
    """Enum membership: strings compare case-insensitively, numbers compare by value."""
    if value in enum:
        return True
    return isinstance(value, str) and value.lower() in [str(member).lower() for member in enum]


def _validate_field_type(
    obj: IDFObject,
    field_name: str,
    value: Any,
    field_schema: dict[str, Any],
) -> list[ValidationError]:
    """Validate the type and enum of a field with a single schema (no ``anyOf``).

    ``anyOf`` fields are handled by :func:`_validate_any_of_field`, which weighs type,
    enum and bounds together per branch; routing them here would check the type of one
    branch against the constraints of another. :func:`_validate_field` dispatches.
    """
    errors: list[ValidationError] = []

    # Handle single type
    expected_type = field_schema.get("type")
    if expected_type and not _value_matches_type(value, field_schema):
        errors.append(
            ValidationError(
                severity=Severity.ERROR,
                obj_type=obj.obj_type,
                obj_name=obj.name,
                field=field_name,
                message=f"Expected {expected_type}, got {type(value).__name__}",
                code="E003",
            )
        )

    # Check enum values
    if "enum" in field_schema and not _value_matches_enum(value, field_schema["enum"]):
        errors.append(
            ValidationError(
                severity=Severity.ERROR,
                obj_type=obj.obj_type,
                obj_name=obj.name,
                field=field_name,
                message=f"Value '{value}' not in allowed values: {field_schema['enum']}",
                code="E004",
            )
        )

    return errors


def _value_matches_type(value: Any, schema: dict[str, Any]) -> bool:
    """Check whether a value satisfies a schema's ``type``.

    Only the type is considered: ``enum`` and bounds are constraints checked once the
    branch is known to match on type, never a reason for it not to match. A schema with
    no ``type`` constrains nothing here and matches any value.
    """
    expected_type = schema.get("type")

    if expected_type == "number":
        return _is_numeric(value)
    elif expected_type == "integer":
        if isinstance(value, bool):
            return False
        return isinstance(value, int) or (isinstance(value, float) and value.is_integer())
    elif expected_type == "string":
        return isinstance(value, str)
    elif expected_type == "boolean":
        return isinstance(value, bool)
    elif expected_type == "array":
        return isinstance(value, list)
    elif expected_type == "object":
        return isinstance(value, dict)

    return True  # No type constraint - any value matches


def _validate_field_range(
    obj: IDFObject,
    field_name: str,
    value: float | int,
    field_schema: dict[str, Any],
) -> list[ValidationError]:
    """Validate numeric field range.

    Handles both JSON Schema dialects EnergyPlus has shipped. Schemas for 8.9.0
    through 9.5.0 are draft-04, where ``exclusiveMinimum``/``exclusiveMaximum``
    are *booleans* that make the sibling ``minimum``/``maximum`` exclusive. From
    9.6.0 on they are draft-06+, where the same keys hold the bound itself.
    Comparing a value against the draft-04 boolean would silently treat it as
    ``1``, rejecting every value at or below 1 in a positive-bounded field.
    """
    errors: list[ValidationError] = []

    exclusive_min = field_schema.get("exclusiveMinimum")
    exclusive_max = field_schema.get("exclusiveMaximum")
    # draft-04: the flag qualifies `minimum`/`maximum` rather than carrying a bound.
    min_is_exclusive = exclusive_min is True
    max_is_exclusive = exclusive_max is True

    # Check minimum
    if "minimum" in field_schema:
        minimum = field_schema["minimum"]
        if value <= minimum if min_is_exclusive else value < minimum:
            relation = "must be greater than" if min_is_exclusive else "is below minimum"
            errors.append(
                ValidationError(
                    severity=Severity.ERROR,
                    obj_type=obj.obj_type,
                    obj_name=obj.name,
                    field=field_name,
                    message=f"Value {value} {relation} {minimum}",
                    code="E006" if min_is_exclusive else "E005",
                )
            )

    # Check exclusive minimum (draft-06+, where the key carries the bound)
    if isinstance(exclusive_min, (int, float)) and not isinstance(exclusive_min, bool) and value <= exclusive_min:
        errors.append(
            ValidationError(
                severity=Severity.ERROR,
                obj_type=obj.obj_type,
                obj_name=obj.name,
                field=field_name,
                message=f"Value {value} must be greater than {exclusive_min}",
                code="E006",
            )
        )

    # Check maximum
    if "maximum" in field_schema:
        maximum = field_schema["maximum"]
        if value >= maximum if max_is_exclusive else value > maximum:
            relation = "must be less than" if max_is_exclusive else "is above maximum"
            errors.append(
                ValidationError(
                    severity=Severity.ERROR,
                    obj_type=obj.obj_type,
                    obj_name=obj.name,
                    field=field_name,
                    message=f"Value {value} {relation} {maximum}",
                    code="E008" if max_is_exclusive else "E007",
                )
            )

    # Check exclusive maximum (draft-06+, where the key carries the bound)
    if isinstance(exclusive_max, (int, float)) and not isinstance(exclusive_max, bool) and value >= exclusive_max:
        errors.append(
            ValidationError(
                severity=Severity.ERROR,
                obj_type=obj.obj_type,
                obj_name=obj.name,
                field=field_name,
                message=f"Value {value} must be less than {exclusive_max}",
                code="E008",
            )
        )

    return errors


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


def _reference_field_spec(schema: EpJSONSchema, obj_type: str, field_name: str) -> dict[str, Any]:
    """Return the schema spec for a reference field, looking inside extensible groups too.

    A reference field is not always positional: it may live inside an extensible group, where
    the schema describes it under the array property's ``items.properties`` rather than at the
    top level of the object's properties.
    """
    properties: dict[str, Any] = (schema.get_inner_schema(obj_type) or {}).get("properties", {})
    spec = properties.get(field_name)
    if isinstance(spec, dict):
        return cast("dict[str, Any]", spec)
    for prop in properties.values():
        if prop.get("type") != "array":
            continue
        inner: dict[str, Any] = prop.get("items", {}).get("properties", {})
        nested = inner.get(field_name)
        if isinstance(nested, dict):
            return cast("dict[str, Any]", nested)
    return {}


@dataclass(frozen=True)
class _DeclaredNames:
    """The uppercased names a document declares, split by what each set is used for."""

    #: Every name any object declares, whether through its name field or a `reference` field.
    all_names: set[str]
    #: Names a ZoneList/SpaceList expansion can prefix an object name with: Zone and Space.
    containers: set[str]
    #: Zone names, the only thing an implicit remainder space can be built from.
    zones: set[str]


def _declared_names(doc: IDFDocument, schema: EpJSONSchema) -> _DeclaredNames:
    """Collect the names a document declares.

    An object usually declares its name through its name field, but not always. A field may
    carry `reference`, meaning it CONTRIBUTES its value to a reference list, as opposed to
    `object_list`, which points into one. Anonymous types have no name field at all and
    declare themselves this way: `FluidProperties:Name` names a refrigerant through its
    `fluid_name` field, and `FluidProperties:Superheated` then points at it. Collecting only
    `obj.name` makes those declarations invisible and reports every reference to them as
    dangling. Eleven fields in the 26.1.0 schema declare a reference this way.
    """
    declared = _DeclaredNames(all_names=set(), containers=set(), zones=set())
    for obj_type, collection in doc.collections.items():
        inner: dict[str, Any] = schema.get_inner_schema(obj_type) or {}
        contributing = [name for name, spec in inner.get("properties", {}).items() if spec.get("reference")]
        type_upper = obj_type.upper()
        for obj in collection:
            if obj.name:
                name_upper = obj.name.upper()
                declared.all_names.add(name_upper)
                if type_upper in ("ZONE", "SPACE"):
                    declared.containers.add(name_upper)
                if type_upper == "ZONE":
                    declared.zones.add(name_upper)
            for field_name in contributing:
                value = obj.data.get(field_name)
                if isinstance(value, str) and value:
                    declared.all_names.add(value.upper())
    return declared


def _validate_references(
    doc: IDFDocument,
    schema: EpJSONSchema,
) -> list[ValidationError]:
    """Validate all object references."""
    errors: list[ValidationError] = []
    declared = _declared_names(doc, schema)
    valid_names = declared.all_names

    # Check for dangling references, skipping fields whose reference list nothing populates.
    unpopulated = _unpopulated_reference_lists(schema)
    for obj, field_name, target in doc.references.get_dangling_references(valid_names):
        field_spec = _reference_field_spec(schema, obj.obj_type, field_name)
        lists: list[str] = field_spec.get("object_list") or []
        if lists and all(name in unpopulated for name in lists):
            continue
        if _is_zonelist_expanded_name(target, declared.containers, valid_names):
            continue
        if _is_implicit_remainder_space(target, declared.zones):
            continue
        errors.append(
            ValidationError(
                severity=Severity.ERROR,
                obj_type=obj.obj_type,
                obj_name=obj.name,
                field=field_name,
                message=f"Reference to non-existent object '{target}'",
                code="E009",
            )
        )

    return errors
