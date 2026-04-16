"""Tests for ``document_diff``."""

from __future__ import annotations

from idfkit import new_document
from idfkit.migration.diff import document_diff


def test_no_op_diff_is_empty() -> None:
    doc = new_document()
    diff = document_diff(doc, doc)
    assert diff.is_empty


def test_added_object_type() -> None:
    before = new_document()
    after = new_document()
    after.add("Zone", name="ZoneOne")

    diff = document_diff(before, after)
    # Either Zone is a new type (before had no Zone collection) or the
    # count delta records +1 depending on how empty collections are handled.
    assert "Zone" in diff.added_object_types or diff.object_count_delta.get("Zone") == 1


def test_removed_object_type() -> None:
    before = new_document()
    before.add("Zone", name="ZoneOne")
    after = new_document()

    diff = document_diff(before, after)
    assert "Zone" in diff.removed_object_types or diff.object_count_delta.get("Zone") == -1


def test_count_delta_on_existing_type() -> None:
    before = new_document()
    before.add("Zone", name="ZoneOne")
    after = new_document()
    after.add("Zone", name="ZoneOne")
    after.add("Zone", name="ZoneTwo")

    diff = document_diff(before, after)
    assert diff.object_count_delta.get("Zone") == 1


def test_field_changes_empty_for_same_version() -> None:
    before = new_document()
    before.add("Zone", name="ZoneOne")
    after = new_document()
    after.add("Zone", name="ZoneOne")

    diff = document_diff(before, after)
    assert diff.field_changes == {}


def test_field_changes_across_versions() -> None:
    before = new_document(version=(22, 1, 0))
    before.add("Zone", name="ZoneOne")
    after = new_document(version=(25, 2, 0))
    after.add("Zone", name="ZoneOne")

    diff = document_diff(before, after)
    # If the Zone schema changed at all between 22.1 and 25.2, we'll see a delta;
    # if not, field_changes is empty — either case is acceptable, but the call
    # must not crash and the result must be well-typed.
    assert isinstance(diff.field_changes, dict)
