"""Structural diff between two IDFDocuments at different versions."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ..exceptions import MigrationError
from .report import FieldDelta, MigrationDiff

if TYPE_CHECKING:
    from ..document import IDFDocument
    from ..schema import EpJSONSchema


def document_diff(before: IDFDocument, after: IDFDocument) -> MigrationDiff:
    """Compute a structural diff between *before* and *after*.

    The diff compares the two documents at three levels:

    1. Object types present in one document but not the other.
    2. Per-type signed change in object count.
    3. Per-type schema-level field renames (computed from each document's
       bundled schema — so ``after`` picks up fields that only exist in the
       newer IDD, and ``before`` may carry fields that have since been removed).

    Args:
        before: Document before migration.
        after: Document after migration.

    Returns:
        A [MigrationDiff][idfkit.migration.report.MigrationDiff] capturing
        the observable changes.
    """
    before_types = set(before.collections.keys())
    after_types = set(after.collections.keys())

    added = tuple(sorted(after_types - before_types))
    removed = tuple(sorted(before_types - after_types))

    count_delta: dict[str, int] = {}
    for obj_type in sorted(before_types | after_types):
        before_count = len(before.collections.get(obj_type, ()))
        after_count = len(after.collections.get(obj_type, ()))
        delta = after_count - before_count
        if delta != 0:
            count_delta[obj_type] = delta

    field_changes = _compute_field_changes(before, after, shared_types=before_types & after_types)

    return MigrationDiff(
        added_object_types=added,
        removed_object_types=removed,
        object_count_delta=count_delta,
        field_changes=field_changes,
    )


def _compute_field_changes(
    before: IDFDocument,
    after: IDFDocument,
    *,
    shared_types: set[str],
) -> dict[str, FieldDelta]:
    """Return per-type ``FieldDelta`` for types present in both schemas."""
    before_schema = before.schema
    after_schema = after.schema
    if before_schema is None or after_schema is None:
        return {}

    changes: dict[str, FieldDelta] = {}
    for obj_type in sorted(shared_types):
        before_fields = _schema_field_names(before_schema, obj_type)
        after_fields = _schema_field_names(after_schema, obj_type)
        if before_fields is None or after_fields is None:
            continue
        added_fields = tuple(sorted(after_fields - before_fields))
        removed_fields = tuple(sorted(before_fields - after_fields))
        if added_fields or removed_fields:
            changes[obj_type] = FieldDelta(added=added_fields, removed=removed_fields)
    return changes


def verify_migration_output(
    source: IDFDocument,
    migrated: IDFDocument,
    *,
    target_version: tuple[int, int, int],
    completed_steps: tuple[tuple[tuple[int, int, int], tuple[int, int, int]], ...],
) -> None:
    """Raise ``MigrationError`` if the re-parsed migrated document is suspect.

    Catches the case where a transition binary exits 0 but emits garbage —
    ``parse_idf`` silently produces an empty document for non-IDF input, so
    the only way to detect it is to compare object counts against the source.
    """
    source_count = sum(len(c) for c in source.collections.values())
    migrated_count = sum(len(c) for c in migrated.collections.values())

    if source_count > 0 and migrated_count == 0:
        from_v, to_v = completed_steps[-1] if completed_steps else (target_version, target_version)
        msg = (
            f"Migration produced an empty document (source had {source_count} objects). "
            "The transition binary likely emitted malformed IDF without signaling an error."
        )
        raise MigrationError(
            msg,
            from_version=from_v,
            to_version=to_v,
            completed_steps=completed_steps,
        )


def _schema_field_names(schema: EpJSONSchema, obj_type: str) -> set[str] | None:
    """Return the set of field names for *obj_type* in *schema*.

    Returns ``None`` when the object type is not in the schema, so the caller
    can skip this type rather than treating it as having zero fields.
    """
    inner = schema.get_inner_schema(obj_type)
    if inner is None:
        return None
    raw_properties = inner.get("properties")
    if not isinstance(raw_properties, dict):
        return None
    properties = cast("dict[str, object]", raw_properties)
    return set(properties.keys())
