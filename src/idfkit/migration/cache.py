"""In-process memo of finished migrations.

Each ``Transition-VX-to-VY`` binary spends seconds loading its two IDDs, so a
migration across several releases takes tens of seconds even for a tiny model.
[migrate()][idfkit.migration.migrate] and
[async_migrate()][idfkit.migration.async_migrate] remember the migrated IDF
text of their last [MAX_ENTRIES][idfkit.migration.cache.MAX_ENTRIES]
migrations, keyed by the hash of the source IDF text, the chain of steps and
the migrator's ``cache_key`` (for the bundled backends, the
``IDFVersionUpdater`` directory they run). Migrating the same content again,
as ``simulate(..., auto_migrate=True)`` does for every run of one model, then
only re-parses the result. Concurrent identical migrations run the binaries
once: later callers wait for the first and reuse its result.

A migrator without a ``cache_key`` attribute (or with ``None``) is never
cached, so a custom backend opts in by exposing a string that changes when
its output would.
"""

from __future__ import annotations

import asyncio
import hashlib
import threading
from collections import OrderedDict
from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass

from .progress import MigrationProgress
from .report import MigrationStep

__all__ = [
    "clear_migration_cache",
]

#: How many finished migrations are kept (least recently used are dropped first).
MAX_ENTRIES = 32

_Chain = tuple[tuple[tuple[int, int, int], tuple[int, int, int]], ...]
CacheKey = tuple[str, _Chain, str]


@dataclass(frozen=True, slots=True)
class CachedMigration:
    """The result of a successful migration chain, as kept in the memo."""

    idf_text: str
    steps: tuple[MigrationStep, ...]


_lock = threading.Lock()
_entries: OrderedDict[CacheKey, CachedMigration] = OrderedDict()
# In-flight locks with a count of holders and waiters, dropped when the count returns to 0.
_thread_locks: dict[CacheKey, tuple[threading.Lock, list[int]]] = {}
_async_locks: dict[tuple[int, CacheKey], tuple[asyncio.Lock, list[int]]] = {}


def cache_key(idf_text: str, chain: _Chain, migrator: object) -> CacheKey | None:
    """The memo key for migrating *idf_text* along *chain* with *migrator*, or ``None``.

    ``None`` when *migrator* has no ``cache_key``: its output cannot be assumed
    to depend only on the input text.
    """
    backend = getattr(migrator, "cache_key", None)
    if not isinstance(backend, str) or not backend:
        return None
    digest = hashlib.sha256(idf_text.encode("utf-8")).hexdigest()
    return (digest, chain, backend)


def get(key: CacheKey) -> CachedMigration | None:
    """The memoized migration for *key*, marking it most recently used."""
    with _lock:
        entry = _entries.get(key)
        if entry is not None:
            _entries.move_to_end(key)
        return entry


def put(key: CacheKey, entry: CachedMigration) -> None:
    """Remember *entry* under *key*, dropping the least recently used beyond `MAX_ENTRIES`."""
    with _lock:
        _entries[key] = entry
        _entries.move_to_end(key)
        while len(_entries) > MAX_ENTRIES:
            _entries.popitem(last=False)


def clear_migration_cache() -> None:
    """Forget every memoized migration, so the next one runs the transition binaries again.

    Examples:
        >>> from idfkit.migration import clear_migration_cache
        >>> clear_migration_cache()
    """
    with _lock:
        _entries.clear()


@contextmanager
def in_flight(key: CacheKey) -> Iterator[None]:
    """Hold the lock for *key*, so one thread migrates a content while the others wait for it."""
    with _lock:
        lock, count = _thread_locks.setdefault(key, (threading.Lock(), [0]))
        count[0] += 1
    try:
        with lock:
            yield
    finally:
        with _lock:
            count[0] -= 1
            if count[0] == 0:
                del _thread_locks[key]


@asynccontextmanager
async def in_flight_async(key: CacheKey) -> AsyncIterator[None]:
    """Async counterpart of `in_flight`, per event loop."""
    loop_key = (id(asyncio.get_running_loop()), key)
    with _lock:
        lock, count = _async_locks.setdefault(loop_key, (asyncio.Lock(), [0]))
        count[0] += 1
    try:
        async with lock:
            yield
    finally:
        with _lock:
            count[0] -= 1
            if count[0] == 0:
                del _async_locks[loop_key]


def cached_progress_event(
    chain: _Chain,
) -> MigrationProgress:
    """The ``transitioning`` event of a migration whose result is reused from the cache."""
    n = len(chain)
    return MigrationProgress(
        phase="transitioning",
        message=f"Reusing the cached result of {n} transition step{'s' if n != 1 else ''}",
        step_index=n - 1,
        total_steps=n,
        from_version=chain[0][0],
        to_version=chain[-1][1],
        percent=100.0,
    )
