"""Tests for the in-process memo of finished migrations (``idfkit.migration.cache``)."""

from __future__ import annotations

import asyncio
import threading
import time
from collections.abc import Iterator
from pathlib import Path

import pytest

from idfkit import new_document
from idfkit.exceptions import MigrationError
from idfkit.migration import (
    AsyncSubprocessMigrator,
    SubprocessMigrator,
    async_migrate,
    clear_migration_cache,
    migrate,
)
from idfkit.migration import cache as migration_cache
from idfkit.migration.progress import MigrationProgress
from idfkit.migration.protocol import MigrationStepResult
from idfkit.versioned import AnyIDFDocument


def _version_text(version: tuple[int, int, int]) -> str:
    return f"Version,\n  {version[0]}.{version[1]};\n"


class _CachingMigrator:
    """A stub migrator that opts into the memo with a ``cache_key``."""

    def __init__(self, cache_key: str | None = "stub-binaries", *, delay: float = 0.0, fail: bool = False) -> None:
        self.cache_key = cache_key
        self.calls: list[tuple[tuple[int, int, int], tuple[int, int, int]]] = []
        self._delay = delay
        self._fail = fail
        self._lock = threading.Lock()

    def migrate_step(
        self,
        idf_text: str,
        from_version: tuple[int, int, int],
        to_version: tuple[int, int, int],
        *,
        work_dir: Path,
    ) -> MigrationStepResult:
        with self._lock:
            self.calls.append((from_version, to_version))
        if self._delay:
            time.sleep(self._delay)
        if self._fail:
            raise MigrationError("boom", from_version=from_version, to_version=to_version)
        return MigrationStepResult(idf_text=_version_text(to_version), stdout="ok")


class _AsyncCachingMigrator:
    def __init__(self, cache_key: str = "stub-binaries", *, delay: float = 0.0) -> None:
        self.cache_key = cache_key
        self.calls: list[tuple[tuple[int, int, int], tuple[int, int, int]]] = []
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
        return MigrationStepResult(idf_text=_version_text(to_version), stdout="ok")


@pytest.fixture(autouse=True)
def _empty_cache() -> Iterator[None]:
    clear_migration_cache()
    yield
    clear_migration_cache()


def _model(zone: str = "Z") -> AnyIDFDocument:
    doc = new_document(version=(24, 1, 0))
    doc.add("Zone", zone)
    return doc


def test_second_migration_of_the_same_content_reuses_the_first() -> None:
    migrator = _CachingMigrator()
    first = migrate(_model(), (25, 1, 0), migrator=migrator)
    second = migrate(_model(), (25, 1, 0), migrator=migrator)

    assert len(migrator.calls) == 2  # two steps, run once
    assert first.from_cache is False
    assert second.from_cache is True
    assert second.steps == first.steps
    assert second.migrated_model is not None
    assert first.migrated_model is not None
    assert second.migrated_model is not first.migrated_model
    assert second.migrated_model.version == (25, 1, 0)


def test_cache_hit_reports_one_transitioning_event() -> None:
    migrator = _CachingMigrator()
    migrate(_model(), (25, 1, 0), migrator=migrator)
    events: list[MigrationProgress] = []
    migrate(_model(), (25, 1, 0), migrator=migrator, on_progress=events.append)

    transitioning = [e for e in events if e.phase == "transitioning"]
    assert len(transitioning) == 1
    assert "cached" in transitioning[0].message
    assert transitioning[0].from_version == (24, 1, 0)
    assert transitioning[0].to_version == (25, 1, 0)


def test_different_content_or_target_is_not_reused() -> None:
    migrator = _CachingMigrator()
    migrate(_model("A"), (25, 1, 0), migrator=migrator)
    other_content = migrate(_model("B"), (25, 1, 0), migrator=migrator)
    other_target = migrate(_model("A"), (24, 2, 0), migrator=migrator)

    assert other_content.from_cache is False
    assert other_target.from_cache is False
    assert len(migrator.calls) == 2 + 2 + 1


def test_a_different_backend_key_is_not_reused() -> None:
    migrate(_model(), (24, 2, 0), migrator=_CachingMigrator("install-a"))
    other = _CachingMigrator("install-b")
    report = migrate(_model(), (24, 2, 0), migrator=other)

    assert report.from_cache is False
    assert len(other.calls) == 1


def test_cache_false_always_runs_the_steps() -> None:
    migrator = _CachingMigrator()
    migrate(_model(), (24, 2, 0), migrator=migrator)
    report = migrate(_model(), (24, 2, 0), migrator=migrator, cache=False)

    assert report.from_cache is False
    assert len(migrator.calls) == 2


def test_an_inspection_work_dir_bypasses_the_cache(tmp_path: Path) -> None:
    migrator = _CachingMigrator()
    migrate(_model(), (24, 2, 0), migrator=migrator)
    report = migrate(_model(), (24, 2, 0), migrator=migrator, work_dir=tmp_path, keep_work_dir=True)

    assert report.from_cache is False
    assert len(migrator.calls) == 2
    assert (tmp_path / "step_0_input.idf").exists()


@pytest.mark.asyncio
async def test_async_inspection_work_dir_bypasses_the_cache(tmp_path: Path) -> None:
    migrate(_model(), (24, 2, 0), migrator=_CachingMigrator())
    async_migrator = _AsyncCachingMigrator()
    report = await async_migrate(_model(), (24, 2, 0), migrator=async_migrator, work_dir=tmp_path)

    assert report.from_cache is False
    assert len(async_migrator.calls) == 1


def test_migrator_without_cache_key_is_never_cached() -> None:
    migrator = _CachingMigrator(cache_key=None)
    migrate(_model(), (24, 2, 0), migrator=migrator)
    report = migrate(_model(), (24, 2, 0), migrator=migrator)

    assert report.from_cache is False
    assert len(migrator.calls) == 2


def test_failed_migration_is_not_cached() -> None:
    with pytest.raises(MigrationError):
        migrate(_model(), (24, 2, 0), migrator=_CachingMigrator(fail=True))
    migrator = _CachingMigrator()
    report = migrate(_model(), (24, 2, 0), migrator=migrator)

    assert report.from_cache is False
    assert len(migrator.calls) == 1


def test_clear_migration_cache_forgets_results() -> None:
    migrator = _CachingMigrator()
    migrate(_model(), (24, 2, 0), migrator=migrator)
    clear_migration_cache()
    report = migrate(_model(), (24, 2, 0), migrator=migrator)

    assert report.from_cache is False
    assert len(migrator.calls) == 2


def test_least_recently_used_entry_is_dropped(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(migration_cache, "MAX_ENTRIES", 2)
    migrator = _CachingMigrator()
    for zone in ("A", "B", "C"):
        migrate(_model(zone), (24, 2, 0), migrator=migrator)

    assert migrate(_model("C"), (24, 2, 0), migrator=migrator).from_cache is True
    assert migrate(_model("A"), (24, 2, 0), migrator=migrator).from_cache is False


def test_concurrent_identical_migrations_run_the_steps_once() -> None:
    migrator = _CachingMigrator(delay=0.05)
    reports: list[bool] = []

    def run() -> None:
        reports.append(migrate(_model(), (25, 1, 0), migrator=migrator).from_cache)

    threads = [threading.Thread(target=run) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(migrator.calls) == 2
    assert sorted(reports) == [False, True, True, True]


@pytest.mark.asyncio
async def test_async_migrate_shares_the_cache_with_migrate() -> None:
    migrate(_model(), (24, 2, 0), migrator=_CachingMigrator())
    async_migrator = _AsyncCachingMigrator()
    report = await async_migrate(_model(), (24, 2, 0), migrator=async_migrator)

    assert report.from_cache is True
    assert async_migrator.calls == []


@pytest.mark.asyncio
async def test_concurrent_identical_async_migrations_run_the_steps_once() -> None:
    migrator = _AsyncCachingMigrator(delay=0.05)
    reports = await asyncio.gather(*(async_migrate(_model(), (25, 1, 0), migrator=migrator) for _ in range(4)))

    assert len(migrator.calls) == 2
    assert sorted(r.from_cache for r in reports) == [False, True, True, True]


def test_bundled_backends_share_a_key_per_install(tmp_path: Path) -> None:
    a = tmp_path / "a" / "IDFVersionUpdater"
    b = tmp_path / "b" / "IDFVersionUpdater"

    assert SubprocessMigrator(a).cache_key == AsyncSubprocessMigrator(a).cache_key
    assert SubprocessMigrator(a).cache_key != SubprocessMigrator(b).cache_key
