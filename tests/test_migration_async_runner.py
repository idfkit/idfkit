"""Tests for the async migration orchestrator.

Mirrors [tests.test_migration_runner][] with an async stub migrator, and
adds a concurrency assertion: a sibling coroutine must be able to make
progress while a slow transition step is pending.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from idfkit import new_document
from idfkit.exceptions import MigrationError, UnsupportedVersionError
from idfkit.migration.async_runner import async_migrate
from idfkit.migration.progress import MigrationProgress
from idfkit.migration.protocol import MigrationStepResult
from idfkit.migration.report import MigrationReport


class _AsyncStubMigrator:
    """Async test double recording calls and returning canned output."""

    def __init__(
        self,
        emitted_versions: list[tuple[int, int, int]],
        *,
        delay: float = 0.0,
    ) -> None:
        self.calls: list[tuple[tuple[int, int, int], tuple[int, int, int]]] = []
        self._emitted_versions = emitted_versions
        self._index = 0
        self._delay = delay

    async def migrate_step(
        self,
        idf_text: str,
        from_version: tuple[int, int, int],
        to_version: tuple[int, int, int],
        *,
        work_dir: Path,
    ) -> MigrationStepResult:
        self.calls.append((from_version, to_version))
        if self._delay:
            await asyncio.sleep(self._delay)
        version = self._emitted_versions[self._index]
        self._index += 1
        return MigrationStepResult(
            idf_text=f"Version,\n  {version[0]}.{version[1]};\n",
            stdout="ok",
            stderr="",
        )


@pytest.mark.asyncio
async def test_noop_returns_trivial_report() -> None:
    doc = new_document(version=(24, 1, 0))
    report = await async_migrate(doc, target_version=(24, 1, 0), migrator=_AsyncStubMigrator([]))
    assert report.success is True
    assert report.steps == ()
    assert report.migrated_model is None


@pytest.mark.asyncio
async def test_migrates_through_chain() -> None:
    doc = new_document(version=(24, 1, 0))
    migrator = _AsyncStubMigrator([(24, 2, 0), (25, 1, 0)])
    report = await async_migrate(doc, target_version=(25, 1, 0), migrator=migrator)

    assert migrator.calls == [((24, 1, 0), (24, 2, 0)), ((24, 2, 0), (25, 1, 0))]
    assert report.success is True
    assert len(report.steps) == 2
    assert report.migrated_model is not None
    assert report.migrated_model.version == (25, 1, 0)


@pytest.mark.asyncio
async def test_target_accepts_string() -> None:
    doc = new_document(version=(24, 1, 0))
    report = await async_migrate(
        doc,
        target_version="24.2.0",
        migrator=_AsyncStubMigrator([(24, 2, 0)]),
    )
    assert report.target_version == (24, 2, 0)


@pytest.mark.asyncio
async def test_unsupported_target_raises() -> None:
    doc = new_document(version=(24, 1, 0))
    with pytest.raises(UnsupportedVersionError):
        await async_migrate(doc, target_version=(99, 0, 0), migrator=_AsyncStubMigrator([]))


@pytest.mark.asyncio
async def test_backward_migration_raises() -> None:
    doc = new_document(version=(24, 2, 0))
    with pytest.raises(ValueError, match="Backward migration"):
        await async_migrate(doc, target_version=(24, 1, 0), migrator=_AsyncStubMigrator([]))


@pytest.mark.asyncio
async def test_step_failure_records_prior_successes() -> None:
    class _FailingAsyncMigrator:
        async def migrate_step(
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
        await async_migrate(doc, target_version=(25, 1, 0), migrator=_FailingAsyncMigrator())

    assert exc_info.value.completed_steps == (((24, 1, 0), (24, 2, 0)),)


@pytest.mark.asyncio
async def test_progress_sync_callback_receives_events() -> None:
    events: list[MigrationProgress] = []
    doc = new_document(version=(24, 1, 0))
    await async_migrate(
        doc,
        target_version=(24, 2, 0),
        migrator=_AsyncStubMigrator([(24, 2, 0)]),
        on_progress=events.append,
    )
    phases = [e.phase for e in events]
    assert "planning" in phases
    assert phases[-1] == "complete"


@pytest.mark.asyncio
async def test_progress_async_callback_receives_events() -> None:
    events: list[MigrationProgress] = []

    async def _async_cb(event: MigrationProgress) -> None:
        events.append(event)

    doc = new_document(version=(24, 1, 0))
    await async_migrate(
        doc,
        target_version=(24, 2, 0),
        migrator=_AsyncStubMigrator([(24, 2, 0)]),
        on_progress=_async_cb,
    )
    assert any(e.phase == "transitioning" for e in events)


@pytest.mark.asyncio
async def test_progress_callback_exception_is_swallowed() -> None:
    def _raises(_event: MigrationProgress) -> None:
        msg = "do not propagate"
        raise RuntimeError(msg)

    doc = new_document(version=(24, 1, 0))
    await async_migrate(
        doc,
        target_version=(24, 2, 0),
        migrator=_AsyncStubMigrator([(24, 2, 0)]),
        on_progress=_raises,
    )


@pytest.mark.asyncio
async def test_does_not_block_event_loop() -> None:
    """A sibling coroutine must make progress while a slow step is pending."""
    doc = new_document(version=(24, 1, 0))

    # Slow-enough step that the sibling coroutine gets to run mid-flight.
    step_delay = 0.05
    migrator = _AsyncStubMigrator([(24, 2, 0)], delay=step_delay)

    sibling_ticks = 0

    async def _sibling() -> None:
        nonlocal sibling_ticks
        # Tick frequently so at least a few fire while the migrator is awaiting.
        for _ in range(10):
            sibling_ticks += 1
            await asyncio.sleep(0)

    migrate_task = asyncio.create_task(async_migrate(doc, target_version=(24, 2, 0), migrator=migrator))
    sibling_task = asyncio.create_task(_sibling())

    report = await migrate_task
    await sibling_task

    assert report.success
    assert sibling_ticks > 0


@pytest.mark.asyncio
async def test_async_migrate_is_exported_at_package_level() -> None:
    import idfkit

    assert idfkit.async_migrate is async_migrate


@pytest.mark.asyncio
async def test_async_stub_migrator_satisfies_protocol() -> None:
    from idfkit.migration.protocol import AsyncMigrator

    stub = _AsyncStubMigrator([(24, 2, 0)])
    assert isinstance(stub, AsyncMigrator)


@pytest.mark.asyncio
async def test_accepts_custom_work_dir(tmp_path: Path) -> None:
    doc = new_document(version=(24, 1, 0))
    work = tmp_path / "async_custom"
    report = await async_migrate(
        doc,
        target_version=(24, 2, 0),
        migrator=_AsyncStubMigrator([(24, 2, 0)]),
        work_dir=work,
        keep_work_dir=True,
    )
    assert work.exists()
    assert report.success


@pytest.mark.asyncio
async def test_returns_migration_report() -> None:
    doc = new_document(version=(24, 1, 0))
    report = await async_migrate(
        doc,
        target_version=(24, 2, 0),
        migrator=_AsyncStubMigrator([(24, 2, 0)]),
    )
    assert isinstance(report, MigrationReport)
