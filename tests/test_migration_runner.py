"""Tests for the top-level migration orchestrator."""

from __future__ import annotations

from pathlib import Path

import pytest

from idfkit import new_document
from idfkit.exceptions import MigrationError, UnsupportedVersionError
from idfkit.migration.progress import MigrationProgress
from idfkit.migration.protocol import MigrationStepResult
from idfkit.migration.report import MigrationReport
from idfkit.migration.runner import migrate


class _StubMigrator:
    """Test double that records calls and returns canned step output."""

    def __init__(self, emitted_versions: list[tuple[int, int, int]]) -> None:
        self.calls: list[tuple[tuple[int, int, int], tuple[int, int, int]]] = []
        self._emitted_versions = emitted_versions
        self._index = 0

    def migrate_step(
        self,
        idf_text: str,
        from_version: tuple[int, int, int],
        to_version: tuple[int, int, int],
        *,
        work_dir: Path,
    ) -> MigrationStepResult:
        self.calls.append((from_version, to_version))
        version = self._emitted_versions[self._index]
        self._index += 1
        return MigrationStepResult(
            idf_text=f"Version,\n  {version[0]}.{version[1]};\n",
            stdout="ok",
            stderr="",
        )


def test_noop_returns_trivial_report() -> None:
    doc = new_document(version=(24, 1, 0))
    report = migrate(doc, target_version=(24, 1, 0), migrator=_StubMigrator([]))

    assert report.success is True
    assert report.steps == ()
    assert report.migrated_model is None
    assert report.source_version == report.target_version == (24, 1, 0)


def test_migrates_through_chain() -> None:
    doc = new_document(version=(24, 1, 0))
    migrator = _StubMigrator([(24, 2, 0), (25, 1, 0)])
    report = migrate(doc, target_version=(25, 1, 0), migrator=migrator)

    assert migrator.calls == [((24, 1, 0), (24, 2, 0)), ((24, 2, 0), (25, 1, 0))]
    assert report.success is True
    assert len(report.steps) == 2
    assert all(s.success for s in report.steps)
    assert report.migrated_model is not None
    assert report.migrated_model.version == (25, 1, 0)


def test_target_accepts_string() -> None:
    doc = new_document(version=(24, 1, 0))
    report = migrate(doc, target_version="24.2.0", migrator=_StubMigrator([(24, 2, 0)]))
    assert report.target_version == (24, 2, 0)


def test_invalid_target_string_raises() -> None:
    doc = new_document(version=(24, 1, 0))
    with pytest.raises(ValueError, match="version"):
        migrate(doc, target_version="not-a-version", migrator=_StubMigrator([]))


def test_unsupported_target_raises() -> None:
    doc = new_document(version=(24, 1, 0))
    with pytest.raises(UnsupportedVersionError):
        migrate(doc, target_version=(99, 0, 0), migrator=_StubMigrator([]))


def test_backward_migration_raises() -> None:
    doc = new_document(version=(24, 2, 0))
    with pytest.raises(ValueError, match="Backward migration"):
        migrate(doc, target_version=(24, 1, 0), migrator=_StubMigrator([]))


def test_step_failure_records_prior_successes() -> None:
    class _FailingMigrator:
        def migrate_step(
            self,
            idf_text: str,
            from_version: tuple[int, int, int],
            to_version: tuple[int, int, int],
            *,
            work_dir: Path,
        ) -> MigrationStepResult:
            if from_version == (24, 2, 0):
                msg = "second step fails"
                raise MigrationError(
                    msg,
                    from_version=from_version,
                    to_version=to_version,
                    exit_code=2,
                    stderr="boom",
                )
            return MigrationStepResult(idf_text="Version,\n  24.2;\n")

    doc = new_document(version=(24, 1, 0))
    with pytest.raises(MigrationError) as exc_info:
        migrate(doc, target_version=(25, 1, 0), migrator=_FailingMigrator())

    assert exc_info.value.completed_steps == (((24, 1, 0), (24, 2, 0)),)
    assert exc_info.value.exit_code == 2


def test_progress_callback_receives_events() -> None:
    doc = new_document(version=(24, 1, 0))
    events: list[MigrationProgress] = []
    migrate(
        doc,
        target_version=(24, 2, 0),
        migrator=_StubMigrator([(24, 2, 0)]),
        on_progress=events.append,
    )
    phases = [e.phase for e in events]
    assert "planning" in phases
    assert "transitioning" in phases
    assert phases[-1] == "complete"


def test_progress_callback_exception_is_swallowed() -> None:
    def _raises(_event: MigrationProgress) -> None:
        msg = "do not propagate"
        raise RuntimeError(msg)

    doc = new_document(version=(24, 1, 0))
    # Must not raise despite callback throwing.
    migrate(
        doc,
        target_version=(24, 2, 0),
        migrator=_StubMigrator([(24, 2, 0)]),
        on_progress=_raises,
    )


def test_migrate_is_exported_at_package_level() -> None:
    import idfkit

    assert idfkit.migrate is migrate
    assert isinstance(idfkit.MigrationReport, type)


def test_stub_migrator_protocol_compliance() -> None:
    """``_StubMigrator`` should satisfy the ``Migrator`` protocol."""
    from idfkit.migration.protocol import Migrator

    stub = _StubMigrator([(24, 2, 0)])
    assert isinstance(stub, Migrator)


def test_accepts_custom_work_dir(tmp_path: Path) -> None:
    doc = new_document(version=(24, 1, 0))
    work = tmp_path / "custom"
    report = migrate(
        doc,
        target_version=(24, 2, 0),
        migrator=_StubMigrator([(24, 2, 0)]),
        work_dir=work,
        keep_work_dir=True,
    )
    assert work.exists()
    assert report.success is True


def test_silent_garbage_output_is_caught() -> None:
    """If a backend returns garbage IDF text but claims success, the orchestrator
    must raise ``MigrationError`` instead of returning an empty document."""
    from idfkit.migration.protocol import MigrationStepResult

    class _GarbageMigrator:
        def migrate_step(
            self,
            idf_text: str,
            from_version: tuple[int, int, int],
            to_version: tuple[int, int, int],
            *,
            work_dir: Path,
        ) -> MigrationStepResult:
            return MigrationStepResult(idf_text="!!! NOT VALID IDF !!!", stdout="", stderr="")

    # Seed the source doc with a real object so the source_count > 0 guard fires.
    doc = new_document(version=(24, 1, 0))
    doc.add("Zone", "Office")

    with pytest.raises(MigrationError, match="empty document"):
        migrate(doc, target_version=(24, 2, 0), migrator=_GarbageMigrator())


def test_migration_report_type() -> None:
    doc = new_document(version=(24, 1, 0))
    report = migrate(doc, target_version=(24, 2, 0), migrator=_StubMigrator([(24, 2, 0)]))
    assert isinstance(report, MigrationReport)
