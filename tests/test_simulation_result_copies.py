"""Every place that builds one SimulationResult from another carries every field.

Three functions copy a result: a cache hit restored into ``output_dir`` and a local run published to
``fs=`` (sync and async). Each used to name the fields it copied, so a field added to
``SimulationResult`` later was silently dropped there and took its default instead. These tests fill
every init field with a non-default value and check that each copy keeps all of them except the ones
the copy is meant to change, so a new field is covered without being named here.
"""

from __future__ import annotations

import asyncio
import dataclasses
from pathlib import Path
from typing import Any

from idfkit.simulation import async_runner, runner
from idfkit.simulation._common import restore_cached_result
from idfkit.simulation.result import SimulationResult
from tests.conftest import InMemoryAsyncFileSystem, InMemoryFileSystem

# Fields each copy sets itself; every other init field must come through unchanged.
_LOCATION_FIELDS = {"run_dir", "fs", "async_fs", "owns_run_dir"}


def _non_default(f: dataclasses.Field[Any]) -> Any:
    """A value for *f* that differs from its default, so a dropped field shows."""
    sentinels: dict[str, Any] = {
        "success": True,
        "exit_code": 7,
        "stdout": "out",
        "stderr": "err",
        "runtime_seconds": 12.5,
        "output_prefix": "custom",
        "migration_report": object(),
        "refusal": None,  # a refused result reads no files; keep it a real run
        "cached": True,
        "owns_run_dir": True,
        "cancelled": False,
    }
    if f.name in sentinels:
        return sentinels[f.name]
    # A field this table does not know yet: any value unlike its default proves it is carried.
    return f"sentinel-{f.name}"


def _full_result(run_dir: Path) -> SimulationResult:
    values = {f.name: _non_default(f) for f in dataclasses.fields(SimulationResult) if f.init}
    values.update(run_dir=run_dir, fs=None, async_fs=None)
    return SimulationResult(**values)


def _assert_carried(original: SimulationResult, copy: SimulationResult) -> None:
    for f in dataclasses.fields(SimulationResult):
        if not f.init or f.name in _LOCATION_FIELDS:
            continue
        if f.name == "cached":
            continue  # each test checks cached on its own
        assert getattr(copy, f.name) is getattr(original, f.name) or getattr(copy, f.name) == getattr(
            original, f.name
        ), f"{f.name} was not carried"


def test_every_field_is_initialisable() -> None:
    """The helper must build a result, or the copy tests prove nothing."""
    result = _full_result(Path("/run"))
    assert result.exit_code == 7


def test_restored_cache_hit_carries_every_field(tmp_path: Path) -> None:
    entry_dir = tmp_path / "entry"
    entry_dir.mkdir()
    (entry_dir / "eplusout.err").write_text("")
    entry = _full_result(entry_dir)

    restored = restore_cached_result(entry, tmp_path / "out")

    _assert_carried(entry, restored)
    assert restored.run_dir == (tmp_path / "out").resolve()
    assert restored.cached is True
    assert restored.owns_run_dir is False
    assert restored.fs is None
    assert restored.async_fs is None


def test_published_result_carries_every_field(tmp_path: Path) -> None:
    local_dir = tmp_path / "local"
    local_dir.mkdir()
    (local_dir / "eplusout.err").write_text("")
    local = _full_result(local_dir)
    fs = InMemoryFileSystem()

    published = runner._publish(local, Path("remote/run"), fs, None)  # pyright: ignore[reportPrivateUsage]

    _assert_carried(local, published)
    assert published.cached is local.cached
    assert published.run_dir == Path("remote/run")
    assert published.fs is fs
    assert published.owns_run_dir is False


def test_async_published_result_carries_every_field(tmp_path: Path) -> None:
    local_dir = tmp_path / "local"
    local_dir.mkdir()
    (local_dir / "eplusout.err").write_text("")
    local = _full_result(local_dir)

    for fs in (InMemoryFileSystem(), InMemoryAsyncFileSystem()):
        published = asyncio.run(
            async_runner._publish(local, Path("remote/run"), fs, None)  # pyright: ignore[reportPrivateUsage]
        )
        _assert_carried(local, published)
        assert published.cached is local.cached
        assert published.run_dir == Path("remote/run")
        assert published.owns_run_dir is False
        if isinstance(fs, InMemoryAsyncFileSystem):
            assert published.async_fs is fs
            assert published.fs is None
        else:
            assert published.fs is fs
            assert published.async_fs is None
