"""Core compatibility linting engine.

Combines schema diffing with AST extraction to produce lint diagnostics
for cross-version EnergyPlus compatibility issues.
"""

from __future__ import annotations

from ..schema import EpJSONSchema, get_schema
from ..versions import find_closest_version, version_string
from ._diff import SchemaIndex, build_schema_index
from ._extract import extract_literals
from ._models import CompatSeverity, Diagnostic, ExtractedLiteral, LiteralKind

# Cache of schema indices, keyed by version tuple.
_index_cache: dict[tuple[int, int, int], SchemaIndex] = {}


def _get_index(version: tuple[int, int, int]) -> SchemaIndex:
    """Load and cache a :class:`SchemaIndex` for *version*."""
    if version not in _index_cache:
        schema: EpJSONSchema = get_schema(version)
        _index_cache[version] = build_schema_index(schema)
    return _index_cache[version]


def resolve_version(version: tuple[int, int, int]) -> tuple[int, int, int]:
    """Resolve a user-supplied version to the closest bundled schema version.

    Raises:
        ValueError: If no matching schema version is available.
    """
    closest = find_closest_version(version)
    if closest is None:
        vs = version_string(version)
        msg = f"No bundled schema found for version {vs}"
        raise ValueError(msg)
    return closest


def _build_allowed_types(
    indices: dict[tuple[int, int, int], SchemaIndex],
    include_groups: set[str] | None,
    exclude_groups: set[str] | None,
) -> set[str] | None:
    """Build the set of object types that pass group filters, or ``None`` if no filter is active."""
    if include_groups is None and exclude_groups is None:
        return None
    merged_groups: dict[str, str] = {}
    for index in indices.values():
        merged_groups.update(index.groups)
    allowed: set[str] = set()
    for obj_type, group in merged_groups.items():
        if include_groups is not None and group not in include_groups:
            continue
        if exclude_groups is not None and group in exclude_groups:
            continue
        allowed.add(obj_type)
    return allowed


def _literal_obj_type(literal: ExtractedLiteral) -> str | None:
    """Return the object type associated with *literal* for group-filter purposes."""
    if literal.kind == LiteralKind.OBJECT_TYPE:
        return literal.value
    return literal.obj_type


def _contains_object_type_case_insensitive(object_type: str, available_types: set[str] | frozenset[str]) -> bool:
    """Return whether *object_type* exists in *available_types* using case-insensitive matching."""
    needle = object_type.casefold()
    return any(candidate.casefold() == needle for candidate in available_types)


def check_compatibility(
    source: str,
    filename: str,
    targets: list[tuple[int, int, int]],
    *,
    include_groups: set[str] | None = None,
    exclude_groups: set[str] | None = None,
) -> list[Diagnostic]:
    """Lint a Python source file for cross-version EnergyPlus compatibility issues.

    Parses *source* via the AST (no code execution) and compares extracted
    string literals against the bundled epJSON schemas for the given
    *targets*, emitting a :class:`Diagnostic` for every object type or
    choice value that does not exist in all target versions.

    Args:
        source: Python source code to lint.
        filename: File path (used in diagnostic output).
        targets: List of EnergyPlus version tuples to lint against.
            Versions should already be resolved to bundled schema versions.
        include_groups: If set, only lint object types belonging to these
            IDD groups (e.g. ``{"Thermal Zones and Surfaces"}``).
        exclude_groups: If set, skip object types belonging to these IDD groups.

    Returns:
        List of :class:`Diagnostic` instances, sorted by line then column.
    """
    if len(targets) < 2:
        msg = "at least two target versions are required"
        raise ValueError(msg)

    literals = extract_literals(source, filename)
    if not literals:
        return []

    indices: dict[tuple[int, int, int], SchemaIndex] = {v: _get_index(v) for v in targets}
    allowed_types = _build_allowed_types(indices, include_groups, exclude_groups)

    diagnostics: list[Diagnostic] = []
    for literal in literals:
        if allowed_types is not None:
            ot = _literal_obj_type(literal)
            if ot is not None and not _contains_object_type_case_insensitive(ot, allowed_types):
                continue

        if literal.kind == LiteralKind.OBJECT_TYPE:
            _check_object_type(literal, indices, filename, diagnostics)
        elif literal.kind == LiteralKind.CHOICE_VALUE:
            _check_choice_value(literal, indices, filename, diagnostics)

    diagnostics.sort(key=lambda d: (d.line, d.col))
    return diagnostics


def _check_object_type(
    literal: ExtractedLiteral,
    indices: dict[tuple[int, int, int], SchemaIndex],
    filename: str,
    out: list[Diagnostic],
) -> None:
    """Emit diagnostics for an object-type literal missing in some target versions."""
    present_in: list[tuple[int, int, int]] = []
    absent_in: list[tuple[int, int, int]] = []

    for version, index in indices.items():
        if _contains_object_type_case_insensitive(literal.value, index.object_types):
            present_in.append(version)
        else:
            absent_in.append(version)

    if not absent_in or not present_in:
        # Exists everywhere or nowhere -- nothing to report.
        return

    # Use the first present version as the reference.
    ref_version = sorted(present_in)[0]

    for missing_version in sorted(absent_in):
        out.append(
            Diagnostic(
                code="C001",
                message=(
                    f"Object type '{literal.value}' not found in "
                    f"{version_string(missing_version)} "
                    f"(exists in {version_string(ref_version)})"
                ),
                severity=CompatSeverity.WARNING,
                filename=filename,
                line=literal.line,
                col=literal.col,
                end_col=literal.end_col,
                from_version=version_string(ref_version),
                to_version=version_string(missing_version),
            )
        )


def _check_choice_value(
    literal: ExtractedLiteral,
    indices: dict[tuple[int, int, int], SchemaIndex],
    filename: str,
    out: list[Diagnostic],
) -> None:
    """Emit diagnostics for a choice value that is absent in some target versions."""
    obj_type = literal.obj_type
    field_name = literal.field_name
    if obj_type is None or field_name is None:
        return

    # Collect which versions have this field as an enum and include/exclude the value.
    present_in: list[tuple[int, int, int]] = []
    absent_in: list[tuple[int, int, int]] = []

    for version, index in indices.items():
        choices = index.choices.get((obj_type, field_name))
        if choices is None:
            canonical_obj_type = next(
                (candidate for candidate in index.object_types if candidate.casefold() == obj_type.casefold()),
                None,
            )
            if canonical_obj_type is not None:
                choices = index.choices.get((canonical_obj_type, field_name))
        if choices is None:
            # Field has no enum in this version -- not applicable; skip.
            continue
        if literal.value in choices:
            present_in.append(version)
        else:
            # Case-insensitive fallback
            choices_lower = {c.lower() for c in choices}
            if literal.value.lower() in choices_lower:
                present_in.append(version)
            else:
                absent_in.append(version)

    if not absent_in or not present_in:
        return

    ref_version = sorted(present_in)[0]

    for missing_version in sorted(absent_in):
        out.append(
            Diagnostic(
                code="C002",
                message=(
                    f"Choice value '{literal.value}' for "
                    f"{obj_type}.{field_name} not found in "
                    f"{version_string(missing_version)} "
                    f"(exists in {version_string(ref_version)})"
                ),
                severity=CompatSeverity.WARNING,
                filename=filename,
                line=literal.line,
                col=literal.col,
                end_col=literal.end_col,
                from_version=version_string(ref_version),
                to_version=version_string(missing_version),
            )
        )
