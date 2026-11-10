"""Schedule:File evaluation.

Handles Schedule:File objects which read values from external CSV files.
"""

from __future__ import annotations

import warnings
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, cast

from idfkit._forksafe import ForkSafeLock
from idfkit.schedules.types import Interpolation
from idfkit.simulation.fs import FileSystem, LocalFileSystem

if TYPE_CHECKING:
    from idfkit.objects import IDFObject

# Column separator mapping
_SEPARATORS = {
    "Comma": ",",
    "Tab": "\t",
    "Space": " ",
    "Semicolon": ";",
    "comma": ",",
    "tab": "\t",
    "space": " ",
    "semicolon": ";",
}


class ScheduleFileCache:
    """Cache for Schedule:File CSV data.

    Caches parsed CSV data to avoid repeated file I/O when evaluating
    the same schedule multiple times.
    """

    def __init__(self) -> None:
        """Initialize an empty cache."""
        self._cache: dict[str, list[float]] = {}
        # A read that began before a `clear`, or before an `invalidate` of its file, must not store
        # what it read: the file may have been rewritten in between, and storing would undo the
        # invalidation. `clear` bumps `_generation`; `invalidate` bumps its path's entry in
        # `_path_generations`, so invalidating one file leaves reads of other files cacheable.
        # The lock makes "check the generations, then store" one step against both.
        self._generation = 0
        self._path_generations: dict[str, int] = {}
        self._lock = ForkSafeLock()

    def __getstate__(self) -> dict[str, object]:
        """Copy and pickle a consistent snapshot, taken under the lock, without the lock itself."""
        with self._lock.lock:
            return {
                "_cache": dict(self._cache),
                "_generation": self._generation,
                "_path_generations": dict(self._path_generations),
            }

    def __setstate__(self, state: dict[str, object]) -> None:
        """Restore a snapshot with a lock of its own; state pickled by idfkit 1.2.0 holds only ``_cache``."""
        self._cache = cast("dict[str, list[float]]", state.get("_cache", {}))
        self._generation = cast("int", state.get("_generation", 0))
        self._path_generations = cast("dict[str, int]", state.get("_path_generations", {}))
        self._lock = ForkSafeLock()

    def __copy__(self) -> ScheduleFileCache:
        """A copy is an independent cache holding the same entries, never an alias of this one's state."""
        new = ScheduleFileCache.__new__(ScheduleFileCache)
        new.__setstate__(self.__getstate__())
        return new

    def get_values(
        self,
        obj: IDFObject,
        fs: FileSystem,
        base_path: Path | str | None = None,
    ) -> list[float]:
        """Get cached values or read from file.

        Args:
            obj: The Schedule:File object.
            fs: FileSystem for reading the file.
            base_path: Base directory for resolving relative paths.

        Returns:
            List of schedule values from the file.
        """
        file_path = self._resolve_path(obj, base_path)
        cache_key = self._make_cache_key(obj, file_path)

        # Held in a local rather than read back from the dict: another thread may clear or
        # invalidate between the store and the read, which would turn a hit into a KeyError.
        values = self._cache.get(cache_key)
        if values is None:
            path_key = str(file_path)
            generation = self._generation
            path_generation = self._path_generations.get(path_key, 0)
            values = _read_schedule_file(obj, fs, file_path)
            with self._lock.lock:
                if generation == self._generation and path_generation == self._path_generations.get(path_key, 0):
                    self._cache[cache_key] = values

        return values

    @staticmethod
    def _make_cache_key(obj: IDFObject, file_path: Path) -> str:
        """Build a cache key that includes file path and parsing parameters.

        Two Schedule:File objects pointing to the same CSV but using
        different columns, row offsets, or separators must not share
        cached values.
        """
        column = obj.get("Column Number")
        rows_to_skip = obj.get("Rows to Skip at Top")
        separator = obj.get("Column Separator")
        return f"{file_path}|col={column}|skip={rows_to_skip}|sep={separator}"

    def _resolve_path(self, obj: IDFObject, base_path: Path | str | None) -> Path:
        """Resolve the file path from the Schedule:File object.

        Args:
            obj: The Schedule:File object.
            base_path: Base directory for relative paths.

        Returns:
            Resolved absolute path.
        """
        file_name = obj.get("File Name")
        if file_name is None:
            msg = "Schedule:File missing 'File Name' field"
            raise ValueError(msg)

        file_path = Path(str(file_name))

        # If relative, resolve against base_path
        if not file_path.is_absolute():
            if base_path is None:
                base_path = Path.cwd()
            file_path = Path(base_path) / file_path

        return file_path

    def clear(self) -> None:
        """Clear the cache."""
        with self._lock.lock:
            # A fresh dict swapped in by one store, not cleared in place, so a child forked mid-call
            # sees the whole cache or none of it.
            self._cache = {}
            self._generation += 1

    def invalidate(self, path: str | Path) -> None:
        """Invalidate all cache entries whose key starts with *path*.

        Args:
            path: File path to invalidate.  All entries for this file
                (regardless of column / separator settings) are removed.
        """
        path_key = str(path)
        prefix = path_key + "|"
        # Every store and removal holds the lock, so the dict cannot change under this iteration.
        with self._lock.lock:
            # Built aside and swapped in by one store, so a child forked mid-call never inherits a
            # half-invalidated cache that nothing would finish invalidating.
            self._cache = {k: v for k, v in self._cache.items() if not k.startswith(prefix)}
            self._path_generations[path_key] = self._path_generations.get(path_key, 0) + 1


# Global cache instance
_default_cache = ScheduleFileCache()


def _read_schedule_file(
    obj: IDFObject,
    fs: FileSystem,
    file_path: Path,
) -> list[float]:
    """Read schedule values from a CSV file.

    Args:
        obj: The Schedule:File object.
        fs: FileSystem for reading the file.
        file_path: Resolved path to the file.

    Returns:
        List of schedule values.
    """
    # Get configuration from the object
    column = obj.get("Column Number")
    column = 1 if column is None else int(column)

    rows_to_skip = obj.get("Rows to Skip at Top")
    rows_to_skip = 0 if rows_to_skip is None else int(rows_to_skip)

    separator_name = obj.get("Column Separator")
    separator = "," if separator_name is None else _SEPARATORS.get(str(separator_name), ",")

    # Read and parse the file
    text = fs.read_text(file_path)
    lines = text.strip().split("\n")

    # Skip header rows
    data_lines = lines[rows_to_skip:]

    values: list[float] = []
    for line in data_lines:
        if not line.strip():
            continue

        cols = line.split(separator)
        if column <= len(cols):
            try:
                # Column is 1-based
                value = float(cols[column - 1].strip())
                values.append(value)
            except ValueError:
                # Skip non-numeric values
                continue
        else:
            warnings.warn(
                f"Schedule:File row has {len(cols)} columns, but column {column} was requested",
                stacklevel=2,
            )

    return values


def _get_interpolation_from_obj(obj: IDFObject, default: Interpolation) -> Interpolation:
    """Get interpolation mode from Schedule:File object."""
    interp_field = obj.get("Interpolate to Timestep")
    if not interp_field:
        return default
    interp_str = str(interp_field).lower()
    if interp_str in ("average", "linear", "yes"):
        return Interpolation.AVERAGE
    return Interpolation.NO


def _interpolate_value(values: list[float], index: int, fraction: float, interpolate: bool) -> float:
    """Get value from list with optional interpolation."""
    if index >= len(values):
        return values[-1] if values else 0.0
    if interpolate and index < len(values) - 1:
        return values[index] + fraction * (values[index + 1] - values[index])
    return values[index]


def evaluate_schedule_file(
    obj: IDFObject,
    dt: datetime,
    fs: FileSystem | None = None,
    base_path: Path | str | None = None,
    cache: ScheduleFileCache | None = None,
    interpolation: Interpolation = Interpolation.NO,
) -> float:
    """Evaluate a Schedule:File at a specific datetime.

    Args:
        obj: The Schedule:File object.
        dt: Datetime to evaluate.
        fs: FileSystem for reading the CSV (default: LocalFileSystem).
        base_path: Base directory for resolving relative paths.
        cache: Cache instance (default: global cache).
        interpolation: Interpolation mode (overridden by object's setting if present).

    Returns:
        The schedule value at the given time.
    """
    fs = fs or LocalFileSystem()
    cache = cache or _default_cache
    interpolation = _get_interpolation_from_obj(obj, interpolation)

    minutes_per_item = obj.get("Minutes per Item")
    minutes_per_item = 60 if minutes_per_item is None else int(minutes_per_item)

    values = cache.get_values(obj, fs, base_path)
    if not values:
        return 0.0

    # Calculate position in the year
    year_start = datetime(dt.year, 1, 1)
    minutes_elapsed = (dt - year_start).total_seconds() / 60
    index = int(minutes_elapsed / minutes_per_item)

    # Calculate fractional position within interval
    interval_start = index * minutes_per_item
    fraction = (minutes_elapsed - interval_start) / minutes_per_item
    interpolate = interpolation in (Interpolation.AVERAGE, Interpolation.LINEAR)

    return _interpolate_value(values, index, fraction, interpolate)


def get_schedule_file_values(
    obj: IDFObject,
    fs: FileSystem | None = None,
    base_path: Path | str | None = None,
    cache: ScheduleFileCache | None = None,
) -> list[float]:
    """Get all values from a Schedule:File.

    Args:
        obj: The Schedule:File object.
        fs: FileSystem for reading the CSV.
        base_path: Base directory for resolving relative paths.
        cache: Cache instance.

    Returns:
        List of all schedule values.
    """
    if fs is None:
        fs = LocalFileSystem()
    if cache is None:
        cache = _default_cache

    return cache.get_values(obj, fs, base_path)
