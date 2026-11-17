"""Core compatibility linting engine.

Combines schema diffing with AST extraction to produce lint diagnostics
for cross-version EnergyPlus compatibility issues.
"""

from __future__ import annotations

import difflib
from collections.abc import Collection
from functools import lru_cache

from ..schema import EpJSONSchema, get_schema
from ..versions import find_closest_version, version_string
from ._diff import SchemaIndex, build_schema_index
from ._extract import extract_literals
from ._models import (
    DEFAULT_RULES,
    DIAGNOSTIC_CODES,
    RULE_SEVERITIES,
    Diagnostic,
    ExtractedLiteral,
    LiteralKind,
)
from ._suppress import Suppression, parse_suppressions

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
) -> frozenset[str] | None:
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
    return frozenset(allowed)


def _literal_obj_type(literal: ExtractedLiteral) -> str | None:
    """Return the object type associated with *literal* for group-filter purposes."""
    if literal.kind == LiteralKind.OBJECT_TYPE:
        return literal.value
    return literal.obj_type


def _canonical_object_type(object_type: str, available_types: frozenset[str]) -> str | None:
    """Return the schema's spelling of *object_type* in *available_types*, matched case-insensitively."""
    if object_type in available_types:
        return object_type
    return _by_folded_name(available_types).get(object_type.casefold())


@lru_cache(maxsize=64)
def _by_folded_name(available_types: frozenset[str]) -> dict[str, str]:
    """*available_types* keyed by case-folded name, built once per set (a frozenset caches its hash)."""
    return {t.casefold(): t for t in available_types}


def _contains_object_type_case_insensitive(object_type: str, available_types: frozenset[str]) -> bool:
    """Return whether *object_type* exists in *available_types* using case-insensitive matching."""
    return _canonical_object_type(object_type, available_types) is not None


@lru_cache(maxsize=8)
def _types_by_folded_name(versions: tuple[tuple[int, int, int], ...]) -> dict[str, str]:
    """Every object type of *versions*, keyed by its case-folded name."""
    return {t.casefold(): t for v in versions for t in _get_index(v).object_types}


def _passes_group_filter(literal: ExtractedLiteral, allowed_types: frozenset[str], all_types: dict[str, str]) -> bool:
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
    select: Collection[str] | None = None,
    ignore: Collection[str] | None = None,
    suppressions: bool = True,
    package: str | None = None,
) -> list[Diagnostic]:
    """Lint a Python source file for cross-version EnergyPlus compatibility issues.

    Parses *source* via the AST (no code execution) and compares extracted
    string literals against the bundled epJSON schemas for the given
    *targets*, emitting a :class:`Diagnostic` for every object type or
    choice value that does not exist in all target versions.

    A literal is checked only against the targets its code can run on: a lookup on
    ``as_version(doc, ...)`` or inside ``if doc.version >= (9, 4, 0):`` is checked against the
    targets that call or test admits (see :mod:`idfkit.compat._narrow` for exactly what is
    recognised). A ``# idfkit: ignore[C001]`` comment on the literal's line silences the listed
    rules there, and a comment that silences nothing is reported as ``C005``.

    Args:
        source: Python source code to lint.
        filename: File path (used in diagnostic output).
        targets: List of EnergyPlus version tuples to lint against.
            Versions should already be resolved to bundled schema versions.
        include_groups: If set, only lint object types belonging to these
            IDD groups (e.g. ``{"Thermal Zones and Surfaces"}``).
        exclude_groups: If set, skip object types belonging to these IDD groups.
        select: Rule codes to check. ``None`` checks :data:`DEFAULT_RULES`, which leaves out
            the opt-in ``C004``.
        ignore: Rule codes not to check, removed from *select*.
        suppressions: Whether ``# idfkit: ignore`` comments are honoured (and unused ones
            reported as ``C005``).
        package: The dotted package *filename* belongs to, so that its relative imports can be
            recognised as idfkit's (see :func:`~idfkit.compat.extract_literals`).

    Returns:
        List of :class:`Diagnostic` instances, sorted by line then column.

    Raises:
        ValueError: If fewer than two targets are given, or a rule code is unknown.
    """
    if len(targets) < 2:
        msg = "at least two target versions are required"
        raise ValueError(msg)
    enabled = enabled_rules(select, ignore)

    literals = extract_literals(source, filename, package=package)

    indices: dict[tuple[int, int, int], SchemaIndex] = {v: _get_index(v) for v in targets}
    allowed_types = _build_allowed_types(indices, include_groups, exclude_groups)

    all_types = _types_by_folded_name(tuple(sorted(indices))) if allowed_types is not None else {}

    diagnostics: list[Diagnostic] = []
    for literal in literals:
        if allowed_types is not None and not _passes_group_filter(literal, allowed_types, all_types):
            continue
        scope = frozenset(v for v in indices if literal.releases is None or v in literal.releases)
        if not scope:
            # The code is guarded off for every target (``if doc.version < (9, 4, 0):`` with 22.1+).
            continue

        # Presence is judged over every target and misses are reported only within *scope*: a
        # literal no release in scope has, but some other target has, is a definite bug in the
        # guarded code, not a name that exists nowhere.
        if literal.kind == LiteralKind.OBJECT_TYPE:
            _check_object_type(literal, indices, filename, diagnostics, scope=scope)
        elif literal.kind == LiteralKind.CHOICE_VALUE:
            _check_choice_value(literal, indices, filename, diagnostics, scope=scope)

    diagnostics = [d for d in diagnostics if d.code in enabled]
    if suppressions:
        diagnostics = _apply_suppressions(
            source,
            filename,
            diagnostics,
            enabled,
            # A group filter hides diagnostics a comment is there for, so it cannot tell unused.
            report_unused="C005" in enabled and allowed_types is None,
            span=(version_string(min(indices)), version_string(max(indices))),
        )

    diagnostics.sort(key=lambda d: (d.line, d.col, d.code))
    return diagnostics


def enabled_rules(select: Collection[str] | None, ignore: Collection[str] | None) -> frozenset[str]:
    """The rules a run checks: *select* (or :data:`DEFAULT_RULES`) less *ignore*.

    Raises:
        ValueError: If a code is not a rule of :data:`DIAGNOSTIC_CODES`.
    """
    chosen: set[str] = {c.upper() for c in select} if select is not None else set(DEFAULT_RULES)
    dropped: set[str] = {c.upper() for c in ignore} if ignore is not None else set()
    unknown = (chosen | dropped) - DIAGNOSTIC_CODES.keys()
    if unknown:
        msg = f"unknown rule code(s): {', '.join(sorted(unknown))}; valid codes: {', '.join(sorted(DIAGNOSTIC_CODES))}"
        raise ValueError(msg)
    return frozenset(chosen - dropped)


def _apply_suppressions(
    source: str,
    filename: str,
    diagnostics: list[Diagnostic],
    enabled: frozenset[str],
    *,
    report_unused: bool,
    span: tuple[str, str],
) -> list[Diagnostic]:
    """Drop the diagnostics a ``# idfkit: ignore`` comment covers, and report unused comments."""
    comments = parse_suppressions(source)
    if not comments:
        return diagnostics
    kept: list[Diagnostic] = []
    for d in diagnostics:
        comment = comments.get(d.line)
        if comment is not None and comment.covers(d.code):
            comment.used.add(d.code)
        else:
            kept.append(d)
    if not report_unused:
        return kept
    for comment in comments.values():
        problem = _unused_problem(comment, enabled)
        if problem is None:
            continue
        kept.append(
            Diagnostic(
                code="C005",
                message=problem,
                severity=RULE_SEVERITIES["C005"],
                filename=filename,
                line=comment.line,
                col=comment.col,
                end_col=comment.end_col,
                from_version=span[0],
                to_version=span[1],
                suggested_fix="remove the comment" if not comment.used else None,
            )
        )
    return kept


def _unused_problem(comment: Suppression, enabled: frozenset[str]) -> str | None:
    """Why *comment* is reported as ``C005``, or ``None`` when it earns its place.

    A code is reported unused only when its rule ran: a ``C004`` comment is not stale in a run
    that does not check ``C004``.
    """
    if comment.codes is None:
        return None if comment.used else "Unused suppression: '# idfkit: ignore' silences nothing on this line"
    if not comment.codes:
        return "Suppression comment lists no rule codes: write '# idfkit: ignore[C001]'"
    unknown = sorted(comment.codes - DIAGNOSTIC_CODES.keys())
    if unknown:
        return f"Suppression names unknown rule code(s) {', '.join(unknown)}; valid codes: {', '.join(sorted(DIAGNOSTIC_CODES))}"
    unused = sorted(c for c in comment.codes if c in enabled and c not in comment.used and c != "C005")
    if not unused:
        return None
    return f"Unused suppression of {', '.join(unused)}: nothing on this line reports it for these targets"


def _check_object_type(
    literal: ExtractedLiteral,
    indices: dict[tuple[int, int, int], SchemaIndex],
    filename: str,
    out: list[Diagnostic],
    *,
    scope: frozenset[tuple[int, int, int]] | None = None,
) -> None:
    """Emit diagnostics for an object-type literal missing in some target versions of *scope* (default: all)."""
    if scope is None:
        scope = frozenset(indices)
    present_in = [
        v for v, index in indices.items() if _contains_object_type_case_insensitive(literal.value, index.object_types)
    ]
    absent_in = [v for v in indices if v in scope and v not in present_in]

    if literal.call == "get_collection":
        _check_get_collection(literal, indices, present_in, filename, out, scope=scope)

    if not absent_in or not present_in:
        # Exists everywhere in scope, or in no target at all -- nothing more to report.
        return

    ref_version = _reference_version(present_in, scope)

    for missing_version in sorted(absent_in):
        out.append(
            Diagnostic(
                code="C001",
                message=(
                    f"Object type '{literal.value}' not found in "
                    f"{version_string(missing_version)} "
                    f"(exists in {version_string(ref_version)})"
                ),
                severity=RULE_SEVERITIES["C001"],
                filename=filename,
                line=literal.line,
                col=literal.col,
                end_col=literal.end_col,
                from_version=version_string(ref_version),
                to_version=version_string(missing_version),
            )
        )


def _reference_version(
    present_in: list[tuple[int, int, int]], scope: frozenset[tuple[int, int, int]]
) -> tuple[int, int, int]:
    """The release a missing literal is reported as existing in: the earliest in *scope* that has it, else any."""
    in_scope = [v for v in present_in if v in scope]
    return min(in_scope or present_in)


def _check_get_collection(
    literal: ExtractedLiteral,
    indices: dict[tuple[int, int, int], SchemaIndex],
    present_in: list[tuple[int, int, int]],
    filename: str,
    out: list[Diagnostic],
    *,
    scope: frozenset[tuple[int, int, int]],
) -> None:
    """Emit ``C003`` or ``C004`` for a literal passed to ``get_collection``.

    ``get_collection`` is typed for dynamic names, so neither a type checker nor ``C001`` alone
    notices what goes wrong with a literal one: a name no target has returns an empty collection at
    run time rather than raising (``C003``), and a correct one gives an untyped collection where the
    document's own item access would have given a typed one (``C004``).
    """
    # Listed and searched over the releases the code can run on; whether the name exists at all
    # is judged over every target (*present_in*), so a type some other target has is C001's.
    lowest = version_string(min(scope))
    highest = version_string(max(scope))
    receiver = literal.receiver or "model"

    if not present_in:
        by_folded = _types_by_folded_name(tuple(sorted(scope)))
        close = difflib.get_close_matches(literal.value.casefold(), list(by_folded), n=1, cutoff=0.6)
        suggestion = by_folded[close[0]] if close else None
        hint = f"; did you mean '{suggestion}'?" if suggestion else ""
        out.append(
            Diagnostic(
                code="C003",
                message=(
                    f"Object type '{literal.value}' is not in any target version "
                    f"({', '.join(version_string(v) for v in sorted(scope))}); "
                    f"get_collection returns an empty collection for it{hint}"
                ),
                severity=RULE_SEVERITIES["C003"],
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
        if not scope <= set(present_in)
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
            severity=RULE_SEVERITIES["C004"],
            filename=filename,
            line=literal.line,
            col=literal.col,
            end_col=literal.end_col,
            from_version=lowest,
            to_version=highest,
            suggested_fix=f'{receiver}["{canonical}"]',
        )
    )


def _choices_of(index: SchemaIndex, obj_type: str, field_name: str) -> frozenset[str] | None:
    """The choices of *obj_type*'s *field_name* in *index*, the type matched case-insensitively."""
    choices = index.choices.get((obj_type, field_name))
    if choices is None:
        canonical_obj_type = _canonical_object_type(obj_type, index.object_types)
        if canonical_obj_type is not None:
            choices = index.choices.get((canonical_obj_type, field_name))
    return choices


def _check_choice_value(
    literal: ExtractedLiteral,
    indices: dict[tuple[int, int, int], SchemaIndex],
    filename: str,
    out: list[Diagnostic],
    *,
    scope: frozenset[tuple[int, int, int]] | None = None,
) -> None:
    """Emit diagnostics for a choice value that is absent in some target versions of *scope* (default: all)."""
    if scope is None:
        scope = frozenset(indices)
    obj_type = literal.obj_type
    field_name = literal.field_name
    if obj_type is None or field_name is None:
        return

    # Collect which versions have this field as an enum and include/exclude the value.
    present_in: list[tuple[int, int, int]] = []
    absent_in: list[tuple[int, int, int]] = []

    for version, index in indices.items():
        choices = _choices_of(index, obj_type, field_name)
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
            elif version in scope:
                absent_in.append(version)

    if not absent_in or not present_in:
        return

    ref_version = _reference_version(present_in, scope)

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
                severity=RULE_SEVERITIES["C002"],
                filename=filename,
                line=literal.line,
                col=literal.col,
                end_col=literal.end_col,
                from_version=version_string(ref_version),
                to_version=version_string(missing_version),
            )
        )
