"""Core compatibility checking engine.

Combines schema diffing with AST extraction to produce diagnostics.
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


def check_compatibility(
    source: str,
    filename: str,
    targets: list[tuple[int, int, int]],
) -> list[Diagnostic]:
    """Check a Python source file for cross-version compatibility issues.

    Args:
        source: Python source code.
        filename: File path (used in diagnostic output).
        targets: List of EnergyPlus version tuples to check against.
            Versions should already be resolved to bundled schema versions.

    Returns:
        List of :class:`Diagnostic` instances, sorted by line then column.
    """
    if len(targets) < 2:
        msg = "at least two target versions are required"
        raise ValueError(msg)

    literals = extract_literals(source, filename)
    if not literals:
        return []

    # Load schema indices for all targets
    indices: dict[tuple[int, int, int], SchemaIndex] = {}
    for version in targets:
        indices[version] = _get_index(version)

    diagnostics: list[Diagnostic] = []
    for literal in literals:
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
        if literal.value in index.object_types:
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

    key = (obj_type, field_name)

    # Collect which versions have this field as an enum and include/exclude the value.
    present_in: list[tuple[int, int, int]] = []
    absent_in: list[tuple[int, int, int]] = []

    for version, index in indices.items():
        choices = index.choices.get(key)
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
