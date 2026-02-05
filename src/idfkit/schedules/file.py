"""Schedule:File evaluation.

Handles Schedule:File objects which read values from external CSV files.
"""

from __future__ import annotations

import warnings
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

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
        cache_key = str(file_path)

        if cache_key not in self._cache:
            self._cache[cache_key] = _read_schedule_file(obj, fs, file_path)

        return self._cache[cache_key]

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
        self._cache.clear()

    def invalidate(self, path: str | Path) -> None:
        """Invalidate a specific cache entry.

        Args:
            path: Path to invalidate.
        """
        self._cache.pop(str(path), None)


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
