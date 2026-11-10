"""Thread-safety of the process-wide caches, and the documented threading contract.

The race tests start their threads on a :class:`threading.Barrier`, so they hit the shared
structure at the same moment rather than one after another. That is what reproduces a race at
all: the schema-load test fails on the GIL build too without the fix, and the others fail on the
free-threaded build (``python3.14t`` with ``PYTHON_GIL=0``), which is the build CI runs them on.
The tests of one particular interleaving -- a read that straddles an invalidation, a fork while
another thread holds a lock -- force it with events instead, and fail on either build.

The contract they pin, as stated in the ``threading`` agent reference:

* the schema manager, the schema it hands out, and the module-level caches are safe to use from
  any number of threads;
* separate documents are independent, and one document may be READ from many threads at once;
* one document must not be MUTATED from several threads at once, or while another thread reads
  it. A thread that needs to change a shared model works on its own ``doc.copy()``.
"""

from __future__ import annotations

import copy
import os
import pickle
import signal
import sys
import threading
import time
import warnings
from collections.abc import Callable
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
#: Seconds any wait in this module may take before the test fails instead of hanging the run.
TIMEOUT = 30

T = TypeVar("T")


def _all_at_once(fn: Callable[[int], T], threads: int = THREADS) -> list[T]:
    """Run ``fn(i)`` on *threads* threads released together by a barrier; re-raise any failure.

    The threads are daemons joined with a deadline, so a deadlock fails the test after ``TIMEOUT``
    instead of hanging the run.
    """
    barrier = threading.Barrier(threads, timeout=TIMEOUT)
    results: dict[int, T] = {}
    errors: list[BaseException] = []

    def run(i: int) -> None:
        try:
            barrier.wait()
            results[i] = fn(i)
        except BaseException as exc:
            errors.append(exc)

    workers = [threading.Thread(target=run, args=(i,), daemon=True) for i in range(threads)]
    for worker in workers:
        worker.start()
    deadline = time.monotonic() + TIMEOUT
    for worker in workers:
        worker.join(max(0.0, deadline - time.monotonic()))
    if any(worker.is_alive() for worker in workers):
        pytest.fail(f"a thread was still running after {TIMEOUT} s: deadlock?")
    if errors:
        raise errors[0]
    return [results[i] for i in range(threads)]


def _in_background(fn: Callable[[], T]) -> Callable[[], T]:
    """Start ``fn`` on a daemon thread; the returned callable waits up to ``TIMEOUT`` for its result."""
    outcome: list[T] = []
    errors: list[BaseException] = []

    def run() -> None:
        try:
            outcome.append(fn())
        except BaseException as exc:
            errors.append(exc)

    worker = threading.Thread(target=run, daemon=True)
    worker.start()

    def result() -> T:
        worker.join(TIMEOUT)
        if worker.is_alive():
            pytest.fail(f"the background call was still running after {TIMEOUT} s: deadlock?")
        if errors:
            raise errors[0]
        return outcome[0]

    return result


def _in_forked_child(check: Callable[[], bool], waiting_for: str) -> None:
    """Fork, run *check* in the child, and fail unless the child returns True within ``TIMEOUT``."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)  # fork() with a thread running
        pid = os.fork()
    if pid == 0:  # pragma: no cover - the child never returns into pytest
        code = 1
        try:
            code = 0 if check() else 1
        finally:
            os._exit(code)
    deadline = time.monotonic() + TIMEOUT
    while (status := os.waitpid(pid, os.WNOHANG))[0] == 0 and time.monotonic() < deadline:
        time.sleep(0.05)
    if status[0] == 0:
        os.kill(pid, signal.SIGKILL)
        os.waitpid(pid, 0)
        pytest.fail(f"the forked child hung waiting for {waiting_for}")
    assert os.waitstatus_to_exitcode(status[1]) == 0


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

    def test_different_versions_still_load_concurrently(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # Each version's load waits for the other's to start: one lock for every version would
        # serialise the two loads, and the barrier would time out.
        both_loading = threading.Barrier(2, timeout=TIMEOUT)
        real_load = schema_module.load_schema_json

        def overlapping_load(path: Path) -> dict[str, Any]:
            both_loading.wait()
            return real_load(path)

        monkeypatch.setattr(schema_module, "load_schema_json", overlapping_load)
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

    @pytest.mark.skipif(sys.platform != "linux", reason="forks the test process")
    def test_a_child_forked_mid_load_can_load_that_version(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # The child inherits the version's load lock held, by a thread it does not have. Without
        # fresh locks after the fork, its first request for that version waits forever.
        loading = threading.Event()
        release = threading.Event()
        real_load = schema_module.load_schema_json

        def held_load(path: Path) -> dict[str, Any]:
            loading.set()
            release.wait(TIMEOUT)
            return real_load(path)

        monkeypatch.setattr(schema_module, "load_schema_json", held_load)
        manager = SchemaManager()
        loader = threading.Thread(target=manager.get_schema, args=((24, 1, 0),))
        loader.start()

        def child() -> bool:
            schema_module.load_schema_json = real_load
            return manager.get_schema((24, 1, 0)).version == (24, 1, 0)

        try:
            assert loading.wait(TIMEOUT)
            _in_forked_child(child, "the schema load lock")
        finally:
            release.set()
            loader.join()

    def test_a_manager_that_has_loaded_a_version_still_pickles_and_copies(self) -> None:
        # Its per-version load locks cannot be pickled; a copy gets a fresh table of its own.
        manager = SchemaManager()
        schema = manager.get_schema((24, 1, 0))

        for copied in (pickle.loads(pickle.dumps(manager)), copy.deepcopy(manager)):  # noqa: S301
            assert copied.get_schema((24, 1, 0)).version == schema.version


class _FakeScheduleFile:
    """Just enough of a Schedule:File object for :class:`ScheduleFileCache` to key on."""

    def __init__(self, i: int) -> None:
        self._i = i

    def get(self, field: str) -> object:
        return f"/data/file{self._i % 8}.csv" if field == "File Name" else self._i


def _invalidate_file0(cache: ScheduleFileCache) -> None:
    cache.invalidate("/data/file0.csv")


def _one_value(obj: object, fs: object, path: Path) -> list[float]:
    return [1.0]


class TestScheduleFileCache:
    def test_reads_survive_concurrent_clears_and_invalidations(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # Before the fix a hit read the dict twice, so a clear between the two raised KeyError,
        # and `invalidate` iterated the live dict, so a concurrent insert raised RuntimeError.
        monkeypatch.setattr(schedule_file, "_read_schedule_file", _one_value)
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

    @pytest.mark.parametrize("drop", [_invalidate_file0, ScheduleFileCache.clear], ids=["invalidate", "clear"])
    def test_a_read_that_raced_an_invalidation_is_not_cached(
        self, monkeypatch: pytest.MonkeyPatch, drop: Callable[[ScheduleFileCache], None]
    ) -> None:
        # The file is rewritten and invalidated (or the cache cleared) while a read of the old
        # contents is in flight. Storing that read afterwards would undo the invalidation for good.
        file_contents = [1.0]
        reading = threading.Event()
        release = threading.Event()

        def slow_read(obj: object, fs: object, path: Path) -> list[float]:
            seen = list(file_contents)
            reading.set()
            release.wait(TIMEOUT)
            return seen

        monkeypatch.setattr(schedule_file, "_read_schedule_file", slow_read)
        cache = ScheduleFileCache()
        fs: FileSystem = schedule_file.LocalFileSystem()
        obj: Any = _FakeScheduleFile(0)

        in_flight = _in_background(lambda: cache.get_values(obj, fs))
        assert reading.wait(TIMEOUT)
        file_contents[:] = [2.0]
        drop(cache)
        release.set()
        assert in_flight() == [1.0]

        reading.clear()
        assert cache.get_values(obj, fs) == [2.0]
        assert reading.is_set(), "the stale read was cached, so the file was not read again"

    @pytest.mark.skipif(sys.platform != "linux", reason="forks the test process")
    def test_a_child_forked_while_a_thread_holds_the_lock_can_use_the_cache(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # The child inherits the cache's lock held, by a thread it does not have. Without a fresh
        # lock after the fork, its first store, clear or invalidation waits forever.
        monkeypatch.setattr(schedule_file, "_read_schedule_file", _one_value)
        cache = ScheduleFileCache()
        fs: FileSystem = schedule_file.LocalFileSystem()
        obj: Any = _FakeScheduleFile(0)
        holding = threading.Event()
        release = threading.Event()

        def hold() -> None:
            with cache._lock.lock:  # pyright: ignore[reportPrivateUsage]
                holding.set()
                release.wait(TIMEOUT)

        def child() -> bool:
            cache.invalidate("/data/file0.csv")
            return cache.get_values(obj, fs) == [1.0]

        holder = threading.Thread(target=hold)
        holder.start()
        try:
            assert holding.wait(TIMEOUT)
            _in_forked_child(child, "the Schedule:File cache lock")
        finally:
            release.set()
            holder.join()

    def test_a_cache_pickles_and_copies_with_a_lock_of_its_own(self, monkeypatch: pytest.MonkeyPatch) -> None:
        reads: list[Path] = []

        def counting_read(obj: object, fs: object, path: Path) -> list[float]:
            reads.append(path)
            return [1.0]

        monkeypatch.setattr(schedule_file, "_read_schedule_file", counting_read)
        cache = ScheduleFileCache()
        fs: FileSystem = schedule_file.LocalFileSystem()
        obj: Any = _FakeScheduleFile(0)
        cache.get_values(obj, fs)

        for copied in (pickle.loads(pickle.dumps(cache)), copy.deepcopy(cache)):  # noqa: S301
            assert copied.get_values(obj, fs) == [1.0]
            copied.clear()

        assert len(reads) == 1, "a copy did not carry the cached values"
        assert cache.get_values(obj, fs) == [1.0]
        assert len(reads) == 1, "clearing a copy cleared the original"


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


class TestCopiesAndInvalidation:
    """Copying, pickling and invalidating a cache that other threads are using."""

    def test_a_shallow_copy_is_an_independent_cache(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # A shallow copy used to share the dict and the lock but not the generation, so an
        # invalidation through one let a stale read through the other store into the shared dict.
        monkeypatch.setattr(schedule_file, "_read_schedule_file", _one_value)
        cache = ScheduleFileCache()
        fs: FileSystem = schedule_file.LocalFileSystem()
        obj: Any = _FakeScheduleFile(0)
        cache.get_values(obj, fs)

        alias = copy.copy(cache)
        cache.clear()

        assert alias.get_values(obj, fs) == [1.0]
        assert alias._cache  # pyright: ignore[reportPrivateUsage]
        assert not cache._cache  # pyright: ignore[reportPrivateUsage]
        assert alias._lock is not cache._lock  # pyright: ignore[reportPrivateUsage]

    def test_deep_copies_and_pickles_survive_concurrent_stores(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # deepcopy used to walk the live dict without the lock and raise "dictionary changed size".
        monkeypatch.setattr(schedule_file, "_read_schedule_file", _one_value)
        cache = ScheduleFileCache()
        fs: FileSystem = schedule_file.LocalFileSystem()

        def work(i: int) -> None:
            for k in range(1500):
                if i % 2:
                    obj: Any = _FakeScheduleFile(k * THREADS + i)
                    cache.get_values(obj, fs)
                    if k % 50 == 0:
                        cache.clear()
                elif i % 4:
                    copy.deepcopy(cache)
                else:
                    pickle.loads(pickle.dumps(cache))  # noqa: S301

        _all_at_once(work)

    def test_state_pickled_by_1_2_0_still_works(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # idfkit 1.2.0 pickled a cache as its `_cache` dict alone.
        monkeypatch.setattr(schedule_file, "_read_schedule_file", _one_value)
        old = ScheduleFileCache.__new__(ScheduleFileCache)
        old.__setstate__({"_cache": {}})
        fs: FileSystem = schedule_file.LocalFileSystem()
        obj: Any = _FakeScheduleFile(0)

        assert old.get_values(obj, fs) == [1.0]
        old.invalidate("/data/file0.csv")
        old.clear()

        manager = SchemaManager.__new__(SchemaManager)
        fresh = SchemaManager()
        manager.__setstate__({k: v for k, v in fresh.__dict__.items() if k in ("_bundled_dir", "_cache_dir", "_cache")})
        assert manager.get_schema((24, 1, 0)).version == (24, 1, 0)

    def test_invalidating_one_file_leaves_reads_of_others_cacheable(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # One generation for the whole cache used to discard every read in flight whenever any
        # file was invalidated, so a steady stream of invalidations stopped the cache caching.
        reading = threading.Event()
        release = threading.Event()
        reads: list[Path] = []

        def slow_read(obj: object, fs: object, path: Path) -> list[float]:
            reads.append(path)
            reading.set()
            release.wait(TIMEOUT)
            return [1.0]

        monkeypatch.setattr(schedule_file, "_read_schedule_file", slow_read)
        cache = ScheduleFileCache()
        fs: FileSystem = schedule_file.LocalFileSystem()
        obj: Any = _FakeScheduleFile(1)  # /data/file1.csv

        in_flight = _in_background(lambda: cache.get_values(obj, fs))
        assert reading.wait(TIMEOUT)
        cache.invalidate("/data/file0.csv")
        release.set()
        assert in_flight() == [1.0]

        assert cache.get_values(obj, fs) == [1.0]
        assert len(reads) == 1, "the read of an unrelated file was not cached"

    def test_invalidate_swaps_the_dict_in_one_store(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # A child forked mid-invalidate inherits whichever dict was in place: never one with some
        # of the file's entries gone and the rest left behind for nothing to remove.
        monkeypatch.setattr(schedule_file, "_read_schedule_file", _one_value)
        cache = ScheduleFileCache()
        fs: FileSystem = schedule_file.LocalFileSystem()
        for i in range(16):
            obj: Any = _FakeScheduleFile(i)
            cache.get_values(obj, fs)
        before = cache._cache  # pyright: ignore[reportPrivateUsage]

        cache.invalidate("/data/file0.csv")

        assert cache._cache is not before  # pyright: ignore[reportPrivateUsage]
        assert len(before) == 16
        assert not [k for k in cache._cache if k.startswith("/data/file0.csv|")]  # pyright: ignore[reportPrivateUsage]


class TestSchemaManagerClearAndReentry:
    def test_a_load_in_flight_during_clear_cache_is_not_cached(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # The load that straddles the clear returns its schema but must not publish it: a request
        # made after the clear used to wait on that load and be handed the pre-clear instance.
        loading = threading.Event()
        release = threading.Event()
        real_load = schema_module.load_schema_json
        calls: list[Path] = []

        def held_load(path: Path) -> dict[str, Any]:
            calls.append(path)
            if len(calls) == 1:
                loading.set()
                release.wait(TIMEOUT)
            return real_load(path)

        monkeypatch.setattr(schema_module, "load_schema_json", held_load)
        manager = SchemaManager()

        first = _in_background(lambda: manager.get_schema((24, 1, 0)))
        assert loading.wait(TIMEOUT)
        manager.clear_cache()
        release.set()
        old = first()

        new = manager.get_schema((24, 1, 0))
        assert new is not old
        assert len(calls) == 2
        assert manager.owns(new)

    def test_a_load_that_asks_for_its_own_version_again_does_not_deadlock(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # A logging handler (or any code the load runs) asking for the version being loaded used to
        # block forever on the non-reentrant load lock.
        real_load = schema_module.load_schema_json
        manager = SchemaManager()
        depth: list[int] = []

        def reentrant_load(path: Path) -> dict[str, Any]:
            depth.append(1)
            if len(depth) == 1:
                manager.get_schema((24, 1, 0))
            return real_load(path)

        monkeypatch.setattr(schema_module, "load_schema_json", reentrant_load)

        assert _in_background(lambda: manager.get_schema((24, 1, 0)))().version == (24, 1, 0)


@pytest.mark.skipif(sys.platform != "linux", reason="forks the test process")
def test_a_child_forked_while_the_geocoder_paces_a_request_can_geocode() -> None:
    # The rate limiter holds its lock across a sleep of up to a second, the widest window of all.
    from idfkit.weather.geocode import RateLimiter

    limiter = RateLimiter(min_interval=60.0)
    limiter.wait()  # the next wait sleeps for a minute, holding the lock
    pacing = threading.Thread(target=limiter.wait, daemon=True)
    pacing.start()
    deadline = time.monotonic() + TIMEOUT
    while not limiter._lock.lock.locked() and time.monotonic() < deadline:  # pyright: ignore[reportPrivateUsage]
        time.sleep(0.01)

    def child() -> bool:
        return limiter._lock.lock.acquire(timeout=5)  # pyright: ignore[reportPrivateUsage]

    _in_forked_child(child, "the geocoder's rate-limit lock")
