"""Thread-safety of the process-wide caches, and the documented threading contract.

Every test here starts its threads on a :class:`threading.Barrier`, so they hit the shared
structure at the same moment rather than one after another. That is what reproduces a race at
all: the schema-load test fails on the GIL build too without the fix, and the others fail on the
free-threaded build (``python3.14t`` with ``PYTHON_GIL=0``), which is the build CI runs them on.

The contract they pin, as stated in the ``threading`` agent reference:

* the schema manager, the schema it hands out, and the module-level caches are safe to use from
  any number of threads;
* separate documents are independent, and one document may be READ from many threads at once;
* one document must not be MUTATED from several threads at once, or while another thread reads
  it. A thread that needs to change a shared model works on its own ``doc.copy()``.
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, TypeVar

import pytest

import idfkit.schedules.file as schedule_file
import idfkit.schema as schema_module
from idfkit import IDFDocument, new_document, write_idf
from idfkit.schedules.file import ScheduleFileCache
from idfkit.schema import EpJSONSchema, SchemaManager
from idfkit.simulation.fs import FileSystem
from idfkit.validation import validate_document

THREADS = 16

T = TypeVar("T")


def _all_at_once(fn: Callable[[int], T], threads: int = THREADS) -> list[T]:
    """Run ``fn(i)`` on *threads* threads released together by a barrier; re-raise any failure."""
    barrier = threading.Barrier(threads)

    def run(i: int) -> T:
        barrier.wait()
        return fn(i)

    with ThreadPoolExecutor(max_workers=threads) as pool:
        return list(pool.map(run, range(threads)))


class TestSchemaManager:
    def test_a_version_requested_by_many_threads_at_once_loads_once(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # Before the fix every thread missed, loaded the 4 MB schema itself, and walked away with
        # its own instance: sixteen loads, sixteen schemas, and `owns` false for all but one.
        loads: list[Path] = []
        real_load = schema_module.load_schema_json

        def counting_load(path: Path) -> dict[str, Any]:
            loads.append(path)
            return real_load(path)

        monkeypatch.setattr(schema_module, "load_schema_json", counting_load)
        manager = SchemaManager()

        schemas = _all_at_once(lambda _: manager.get_schema((24, 1, 0)))

        assert len(loads) == 1
        assert len({id(s) for s in schemas}) == 1
        assert all(manager.owns(s) for s in schemas)

    def test_different_versions_still_load_concurrently(self) -> None:
        manager = SchemaManager()
        versions = [(24, 1, 0), (24, 2, 0)] * (THREADS // 2)

        schemas = _all_at_once(lambda i: manager.get_schema(versions[i]))

        by_version: dict[tuple[int, int, int], set[int]] = {}
        for schema in schemas:
            by_version.setdefault(schema.version, set()).add(id(schema))
        assert {v: len(ids) for v, ids in by_version.items()} == {(24, 1, 0): 1, (24, 2, 0): 1}

    def test_the_first_call_from_many_threads_creates_one_manager(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # Free-threaded only, before the fix: several threads saw no manager and each made one.
        monkeypatch.setattr(schema_module, "_schema_manager", None)

        managers = _all_at_once(lambda _: schema_module.get_schema_manager())

        assert len({id(m) for m in managers}) == 1


class _FakeScheduleFile:
    """Just enough of a Schedule:File object for :class:`ScheduleFileCache` to key on."""

    def __init__(self, i: int) -> None:
        self._i = i

    def get(self, field: str) -> object:
        return f"/data/file{self._i % 8}.csv" if field == "File Name" else self._i


class TestScheduleFileCache:
    def test_reads_survive_concurrent_clears_and_invalidations(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # Before the fix a hit read the dict twice, so a clear between the two raised KeyError,
        # and `invalidate` iterated the live dict, so a concurrent insert raised RuntimeError.
        def fake_read(obj: object, fs: object, path: Path) -> list[float]:
            return [1.0]

        monkeypatch.setattr(schedule_file, "_read_schedule_file", fake_read)
        cache = ScheduleFileCache()
        fs: FileSystem = schedule_file.LocalFileSystem()

        def hammer(i: int) -> None:
            for k in range(2000):
                if i % 4 == 0:
                    cache.clear()
                elif i % 4 == 1:
                    cache.invalidate(f"/data/file{k % 8}.csv")
                else:
                    obj: Any = _FakeScheduleFile(k)
                    assert cache.get_values(obj, fs) == [1.0]

        _all_at_once(hammer)


def _model(zones: int = 40) -> IDFDocument:
    doc = new_document(version=(24, 1, 0))
    doc.add("Material", "Mat", roughness="Smooth", thickness=0.1, conductivity=1.0, density=1000, specific_heat=900)
    doc.add("Construction", "Wall", outside_layer="Mat")
    for z in range(zones):
        doc.add("Zone", f"Zone{z}")
        doc.add(
            "BuildingSurface:Detailed",
            f"Wall{z}",
            surface_type="Wall",
            construction_name="Wall",
            zone_name=f"Zone{z}",
            outside_boundary_condition="Outdoors",
            vertices=[
                {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                {"vertex_x_coordinate": 1.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                {"vertex_x_coordinate": 1.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
            ],
        )
    return doc


class TestDocumentContract:
    def test_one_document_can_be_read_from_many_threads(self) -> None:
        doc = _model()
        text = write_idf(doc)
        errors = len(validate_document(doc).errors)

        def read(_: int) -> bool:
            for _ in range(3):
                assert write_idf(doc) == text
                assert len(validate_document(doc).errors) == errors
                assert write_idf(doc.copy()) == text
                assert {o.name for o in doc.get_referencing("Zone7")} == {"Wall7"}
                assert doc["BuildingSurface:Detailed"]["Wall3"].zone_name == "Zone3"
            return True

        assert all(_all_at_once(read))

    def test_copies_of_a_shared_document_can_be_mutated_in_parallel(self) -> None:
        doc = _model()
        text = write_idf(doc)

        def mutate_own_copy(i: int) -> set[str]:
            mine = doc.copy()
            mine.rename("Zone", "Zone1", f"Renamed{i}")
            mine.add("Zone", f"Extra{i}")
            return {o.name for o in mine.get_referencing(f"Renamed{i}")}

        assert _all_at_once(mutate_own_copy) == [{"Wall1"}] * THREADS
        assert write_idf(doc) == text

    def test_separate_documents_are_independent(self) -> None:
        texts = _all_at_once(lambda _: write_idf(_model()))
        assert len(set(texts)) == 1

    def test_lazily_built_schema_metadata_is_shared_safely(self) -> None:
        # A schema built here, not taken from the manager, so its per-type parsing caches start
        # empty and every thread builds them at once. They are built whole and then published,
        # so a race costs duplicate work and never a half-built entry.
        shared = schema_module.get_schema((24, 1, 0))
        fresh = EpJSONSchema((24, 1, 0), shared._raw)  # pyright: ignore[reportPrivateUsage]
        types = fresh.object_types[:200]

        def build(_: int) -> list[object]:
            return [fresh.get_parsing_cache(t) for t in types]

        results = _all_at_once(build)
        assert all(all(pc is not None for pc in r) for r in results)
        # Whoever lost a race got an equal value, and the cache now hands out one per type.
        assert [fresh.get_parsing_cache(t) for t in types] == results[0]
