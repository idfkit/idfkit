"""Tests for MigrationReport and friends."""

from __future__ import annotations

from idfkit.migration.report import FieldDelta, MigrationDiff, MigrationReport, MigrationStep


def test_migration_diff_is_empty() -> None:
    assert MigrationDiff().is_empty is True
    assert MigrationDiff(added_object_types=("Zone",)).is_empty is False


def test_migration_report_completed_and_failed_step() -> None:
    s1 = MigrationStep(from_version=(24, 1, 0), to_version=(24, 2, 0), success=True)
    s2 = MigrationStep(from_version=(24, 2, 0), to_version=(25, 1, 0), success=False, stderr="boom")
    report = MigrationReport(
        migrated_model=None,
        source_version=(24, 1, 0),
        target_version=(25, 1, 0),
        requested_target=(25, 1, 0),
        steps=(s1, s2),
    )
    assert report.success is False
    assert report.completed_steps == (s1,)
    assert report.failed_step is s2


def test_migration_report_no_failure() -> None:
    s1 = MigrationStep(from_version=(24, 1, 0), to_version=(24, 2, 0), success=True)
    report = MigrationReport(
        migrated_model=None,
        source_version=(24, 1, 0),
        target_version=(24, 2, 0),
        requested_target=(24, 2, 0),
        steps=(s1,),
    )
    assert report.failed_step is None


def test_migration_report_summary_mentions_versions() -> None:
    report = MigrationReport(
        migrated_model=None,
        source_version=(24, 1, 0),
        target_version=(24, 2, 0),
        requested_target=(24, 2, 0),
        steps=(),
        diff=MigrationDiff(added_object_types=("FooType",), removed_object_types=("Bar",)),
    )
    text = report.summary()
    assert "24.1.0" in text
    assert "24.2.0" in text
    assert "FooType" in text
    assert "Bar" in text


def test_field_delta_defaults_empty() -> None:
    delta = FieldDelta()
    assert delta.added == ()
    assert delta.removed == ()
