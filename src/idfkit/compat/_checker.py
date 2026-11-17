"""Core compatibility linting engine.

Combines schema diffing with AST extraction to produce lint diagnostics
for cross-version EnergyPlus compatibility issues.
"""

from __future__ import annotations

import difflib
from functools import lru_cache

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


def _canonical_object_type(object_type: str, available_types: set[str] | frozenset[str]) -> str | None:
    """Return the schema's spelling of *object_type* in *available_types*, matched case-insensitively."""
    if object_type in available_types:
        return object_type
    needle = object_type.casefold()
    return next((candidate for candidate in available_types if candidate.casefold() == needle), None)


def _contains_object_type_case_insensitive(object_type: str, available_types: set[str] | frozenset[str]) -> bool:
    """Return whether *object_type* exists in *available_types* using case-insensitive matching."""
    return _canonical_object_type(object_type, available_types) is not None


@lru_cache(maxsize=8)
def _types_by_folded_name(versions: tuple[tuple[int, int, int], ...]) -> dict[str, str]:
    """Every object type of *versions*, keyed by its case-folded name."""
    return {t.casefold(): t for v in versions for t in _get_index(v).object_types}


def _passes_group_filter(literal: ExtractedLiteral, allowed_types: set[str], all_types: dict[str, str]) -> bool:
    """Whether *literal* survives an active ``--group``/``--exclude-group`` filter.

    A ``get_collection`` name that no target has belongs to no group, so a group filter cannot
    exclude it: dropping it would hide exactly the misspelling ``C003`` exists to report.
    """
    ot = _literal_obj_type(literal)
    if ot is None or _contains_object_type_case_insensitive(ot, allowed_types):
        return True
    return literal.call == "get_collection" and ot.casefold() not in all_types


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

    all_types = _types_by_folded_name(tuple(sorted(indices))) if allowed_types is not None else {}

    diagnostics: list[Diagnostic] = []
    for literal in literals:
        if allowed_types is not None and not _passes_group_filter(literal, allowed_types, all_types):
            continue

        if literal.kind == LiteralKind.OBJECT_TYPE:
            _check_object_type(literal, indices, filename, diagnostics)
        elif literal.kind == LiteralKind.CHOICE_VALUE:
            _check_choice_value(literal, indices, filename, diagnostics)

    diagnostics.sort(key=lambda d: (d.line, d.col, d.code))
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

    if literal.call == "get_collection":
        _check_get_collection(literal, indices, present_in, filename, out)

    if not absent_in or not present_in:
        # Exists everywhere or nowhere -- nothing more to report.
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


def _check_get_collection(
    literal: ExtractedLiteral,
    indices: dict[tuple[int, int, int], SchemaIndex],
    present_in: list[tuple[int, int, int]],
    filename: str,
    out: list[Diagnostic],
) -> None:
    """Emit ``C003`` or ``C004`` for a literal passed to ``get_collection``.

    ``get_collection`` is typed for dynamic names, so neither a type checker nor ``C001`` alone
    notices what goes wrong with a literal one: a name no target has returns an empty collection at
    run time rather than raising (``C003``), and a correct one gives an untyped collection where the
    document's own item access would have given a typed one (``C004``).
    """
    lowest = version_string(min(indices))
    highest = version_string(max(indices))
    receiver = literal.receiver or "model"

    if not present_in:
        by_folded = _types_by_folded_name(tuple(sorted(indices)))
        close = difflib.get_close_matches(literal.value.casefold(), list(by_folded), n=1, cutoff=0.6)
        suggestion = by_folded[close[0]] if close else None
        hint = f"; did you mean '{suggestion}'?" if suggestion else ""
        out.append(
            Diagnostic(
                code="C003",
                message=(
                    f"Object type '{literal.value}' is not in any target version "
                    f"({', '.join(version_string(v) for v in sorted(indices))}); "
                    f"get_collection returns an empty collection for it{hint}"
                ),
                severity=CompatSeverity.ERROR,
                filename=filename,
                line=literal.line,
                col=literal.col,
                end_col=literal.end_col,
                from_version=lowest,
                to_version=highest,
                suggested_fix=f'{receiver}.get_collection("{suggestion}")' if suggestion else None,
            )
        )
        return

    canonical = _canonical_object_type(literal.value, indices[max(present_in)].object_types) or literal.value
    # A type some target lacks is not a key of a document typed for every release, so the typed
    # lookup needs the document narrowed to one that has it first.
    # The lint cannot see the receiver's type, and a document typed for every supported release
    # (AnyIDFDocument) has only the types all of them share as keys, which can be fewer than the
    # targets share, so the narrowing note is always given, worded for the case at hand.
    narrow = (
        " on a document narrowed with as_version() to a release that has it (C001 lists those without)"
        if len(present_in) < len(indices)
        else " (on an AnyIDFDocument, narrow with as_version() first if some supported release lacks the type)"
    )
    out.append(
        Diagnostic(
            code="C004",
            message=(
                f'{receiver}.get_collection("{literal.value}") is untyped (IDFCollection[IDFObject]); '
                f'{receiver}["{canonical}"] gives the typed collection, and the type checker checks '
                f"the name{narrow}"
            ),
            severity=CompatSeverity.WARNING,
            filename=filename,
            line=literal.line,
            col=literal.col,
            end_col=literal.end_col,
            from_version=lowest,
            to_version=highest,
            suggested_fix=f'{receiver}["{canonical}"]',
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
            canonical_obj_type = _canonical_object_type(obj_type, index.object_types)
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
