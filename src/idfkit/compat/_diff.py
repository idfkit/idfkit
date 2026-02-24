"""Schema indexing and cross-version diffing.

Builds lightweight indices of object types and enumerated choice sets
from ``EpJSONSchema`` instances, then computes diffs between versions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

from ..schema import EpJSONSchema


@dataclass(frozen=True)
class SchemaIndex:
    """Pre-computed index of user-facing string identifiers in a schema.

    Attributes:
        version: The EnergyPlus version this index was built from.
        object_types: All object type names in the schema.
        choices: Mapping from ``(object_type, field_name)`` to the set of
            valid enum/choice string values for that field.
    """

    version: tuple[int, int, int]
    object_types: frozenset[str]
    choices: dict[tuple[str, str], frozenset[str]]


@dataclass(frozen=True)
class SchemaDiff:
    """Differences between two schema versions.

    Attributes:
        from_version: Source version.
        to_version: Target version.
        removed_types: Object types present in *from_version* but absent in *to_version*.
        added_types: Object types present in *to_version* but absent in *from_version*.
        removed_choices: For each ``(obj_type, field_name)`` key, the set of
            choice values that were removed going from *from_version* to *to_version*.
        added_choices: Choice values that were added.
    """

    from_version: tuple[int, int, int]
    to_version: tuple[int, int, int]
    removed_types: frozenset[str]
    added_types: frozenset[str]
    removed_choices: dict[tuple[str, str], frozenset[str]]
    added_choices: dict[tuple[str, str], frozenset[str]]


def _extract_enum_values(field_schema: dict[str, Any]) -> set[str]:
    """Extract string enum values from a field schema definition.

    Handles both direct ``"enum"`` keys and ``"anyOf"`` branches.
    """
    values: set[str] = set()
    if "enum" in field_schema:
        for v in field_schema["enum"]:
            if isinstance(v, str):
                values.add(v)
    if "anyOf" in field_schema:
        any_of_list = cast(list[Any], field_schema["anyOf"])
        for sub in any_of_list:
            sub_dict = cast(dict[str, Any], sub)
            if isinstance(sub, dict) and "enum" in sub_dict:
                for val in cast(list[Any], sub_dict["enum"]):
                    if isinstance(val, str):
                        values.add(val)
    return values


def build_schema_index(schema: EpJSONSchema) -> SchemaIndex:
    """Build a :class:`SchemaIndex` from an ``EpJSONSchema``.

    Iterates over all object types and their field properties to collect
    the set of object type names and all enumerated choice values.
    """
    object_types: set[str] = set()
    choices: dict[tuple[str, str], frozenset[str]] = {}

    for obj_type in schema.object_types:
        object_types.add(obj_type)
        inner = schema.get_inner_schema(obj_type)
        if inner is None:
            continue
        props: dict[str, Any] = inner.get("properties", {})
        for field_name in props:
            raw_field = props[field_name]
            if not isinstance(raw_field, dict):
                continue
            field_def = cast(dict[str, Any], raw_field)
            enum_values = _extract_enum_values(field_def)
            if enum_values:
                choices[(obj_type, field_name)] = frozenset(enum_values)

    return SchemaIndex(
        version=schema.version,
        object_types=frozenset(object_types),
        choices=choices,
    )


def diff_schemas(from_index: SchemaIndex, to_index: SchemaIndex) -> SchemaDiff:
    """Compute the diff between two :class:`SchemaIndex` instances.

    Returns a :class:`SchemaDiff` describing which object types and choice
    values were added or removed between *from_index* and *to_index*.
    """
    removed_types = from_index.object_types - to_index.object_types
    added_types = to_index.object_types - from_index.object_types

    removed_choices: dict[tuple[str, str], frozenset[str]] = {}
    added_choices: dict[tuple[str, str], frozenset[str]] = {}

    all_keys = set(from_index.choices.keys()) | set(to_index.choices.keys())
    for key in all_keys:
        from_vals = from_index.choices.get(key, frozenset())
        to_vals = to_index.choices.get(key, frozenset())
        removed = from_vals - to_vals
        added = to_vals - from_vals
        if removed:
            removed_choices[key] = frozenset(removed)
        if added:
            added_choices[key] = frozenset(added)

    return SchemaDiff(
        from_version=from_index.version,
        to_version=to_index.version,
        removed_types=removed_types,
        added_types=added_types,
        removed_choices=removed_choices,
        added_choices=added_choices,
    )
