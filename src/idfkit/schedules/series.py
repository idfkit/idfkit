"""Pandas Series integration for schedule evaluation.

Provides to_series() function to convert schedules to pandas Series
with DatetimeIndex for easy plotting and analysis.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any

from idfkit.schedules.evaluate import values
from idfkit.schedules.types import DayTypeInput, InterpolationInput

if TYPE_CHECKING:
    from matplotlib.axes import Axes

    from idfkit.document import IDFDocument
    from idfkit.objects import IDFObject
    from idfkit.simulation.fs import FileSystem


def to_series(
    schedule: IDFObject,
    year: int = 2024,
    freq: str = "h",
    start_date: tuple[int, int] = (1, 1),
    end_date: tuple[int, int] = (12, 31),
    document: IDFDocument | None = None,
    day_type: DayTypeInput | None = None,
    interpolation: InterpolationInput | None = None,
    fs: FileSystem | None = None,
    base_path: Path | str | None = None,
) -> Any:  # pd.Series — typed as Any for optional dependency
    """Convert a schedule to a pandas Series with DatetimeIndex.

    Args:
        schedule: An IDF schedule object.
        year: Year for the date range.
        freq: Pandas frequency string ("h" for hourly, "30min", "15min", etc.).
        start_date: Start date as (month, day).
        end_date: End date as (month, day).
        document: Required for schedules that reference others.
        day_type: Override day type ("normal", "summer", "winter", etc.).
        interpolation: Interpolation mode ("no", "average", "linear").
        fs: FileSystem for Schedule:File.
        base_path: Base directory for Schedule:File relative paths.

    Returns:
        pandas Series with DatetimeIndex.

    Raises:
        ImportError: If pandas is not installed.
    """
    try:
        import pandas
    except ImportError:
        msg = "pandas is required for to_series(). Install with: pip install idfkit[dataframes]"
        raise ImportError(msg) from None

    # Use Any type to avoid pyright issues with pandas stubs
    pd: Any = pandas

    # Map frequency string to timestep
    timestep = _freq_to_timestep(freq)

    # Get values
    vals = values(
        schedule,
        year=year,
        timestep=timestep,
        start_date=start_date,
        end_date=end_date,
        document=document,
        day_type=day_type,
        interpolation=interpolation,
        fs=fs,
        base_path=base_path,
    )

    # Build DatetimeIndex
    start = datetime(year, start_date[0], start_date[1], 0, 0)
    minutes_per_step = 60 // timestep
    index = pd.date_range(
        start=start,
        periods=len(vals),
        freq=f"{minutes_per_step}min",
    )

    # Create Series
    name = schedule.name or schedule.obj_type
    return pd.Series(vals, index=index, name=name)


def _freq_to_timestep(freq: str) -> int:
    """Convert pandas frequency string to timestep (values per hour).

    Args:
        freq: Pandas frequency string.

    Returns:
        Number of values per hour.
    """
    freq = freq.lower().strip()

    # Handle common formats
    freq_map = {
        "h": 1,
        "1h": 1,
        "60min": 1,
        "60t": 1,
        "30min": 2,
        "30t": 2,
        "20min": 3,
        "20t": 3,
        "15min": 4,
        "15t": 4,
        "10min": 6,
        "10t": 6,
        "5min": 12,
        "5t": 12,
        "1min": 60,
        "1t": 60,
        "min": 60,
        "t": 60,
    }

    if freq in freq_map:
        return freq_map[freq]

    # Try to parse custom formats like "2h", "45min"
    import re

    match = re.match(r"^(\d+)\s*(h|min|t)$", freq)
    if match:
        value = int(match.group(1))
        unit = match.group(2)
        if unit == "h":
            return 1  # Can't go coarser than hourly
        else:  # min or t
            if 60 % value == 0:
                return 60 // value

    # Default to hourly
    return 1


def plot_schedule(
    schedule: IDFObject,
    year: int = 2024,
    start_date: tuple[int, int] = (1, 1),
    end_date: tuple[int, int] = (12, 31),
    document: IDFDocument | None = None,
    day_type: DayTypeInput | None = None,
    fs: FileSystem | None = None,
    base_path: Path | str | None = None,
    **plot_kwargs: Any,
) -> Axes:
    """Plot a schedule as a time series.

    Args:
        schedule: An IDF schedule object.
        year: Year for the date range.
        start_date: Start date as (month, day).
        end_date: End date as (month, day).
        document: Required for schedules that reference others.
        day_type: Override day type ("normal", "summer", "winter", etc.).
        fs: FileSystem for Schedule:File.
        base_path: Base directory for Schedule:File relative paths.
        **plot_kwargs: Additional arguments passed to pandas Series.plot().

    Returns:
        matplotlib Axes object.

    Raises:
        ImportError: If pandas or matplotlib is not installed.
    """
    series = to_series(
        schedule,
        year=year,
        start_date=start_date,
        end_date=end_date,
        document=document,
        day_type=day_type,
        fs=fs,
        base_path=base_path,
    )

    # Set default plot style
    if "drawstyle" not in plot_kwargs:
        plot_kwargs["drawstyle"] = "steps-post"

    return series.plot(**plot_kwargs)


def plot_week(
    schedule: IDFObject,
    year: int = 2024,
    week: int = 1,
    document: IDFDocument | None = None,
    day_type: DayTypeInput | None = None,
    fs: FileSystem | None = None,
    base_path: Path | str | None = None,
    **plot_kwargs: Any,
) -> Axes:
    """Plot a schedule for a single week.

    Args:
        schedule: An IDF schedule object.
        year: Year.
        week: ISO week number (1-53).
        document: Required for schedules that reference others.
        day_type: Override day type ("normal", "summer", "winter", etc.).
        fs: FileSystem for Schedule:File.
        base_path: Base directory for Schedule:File relative paths.
        **plot_kwargs: Additional arguments passed to pandas Series.plot().

    Returns:
        matplotlib Axes object.
    """
    # Calculate start and end dates for the week
    jan1 = datetime(year, 1, 1)
    # Find the Monday of week 1
    week1_monday = jan1 - timedelta(days=jan1.weekday())
    if jan1.weekday() > 3:  # If Jan 1 is Fri-Sun, week 1 starts next week
        week1_monday += timedelta(days=7)

    week_start = week1_monday + timedelta(weeks=week - 1)
    week_end = week_start + timedelta(days=6)

    return plot_schedule(
        schedule,
        year=year,
        start_date=(week_start.month, week_start.day),
        end_date=(week_end.month, week_end.day),
        document=document,
        day_type=day_type,
        fs=fs,
        base_path=base_path,
        **plot_kwargs,
    )


def plot_day(
    schedule: IDFObject,
    year: int = 2024,
    month: int = 1,
    day: int = 1,
    document: IDFDocument | None = None,
    day_type: DayTypeInput | None = None,
    fs: FileSystem | None = None,
    base_path: Path | str | None = None,
    **plot_kwargs: Any,
) -> Axes:
    """Plot a schedule for a single day.

    Args:
        schedule: An IDF schedule object.
        year: Year.
        month: Month (1-12).
        day: Day (1-31).
        document: Required for schedules that reference others.
        day_type: Override day type ("normal", "summer", "winter", etc.).
        fs: FileSystem for Schedule:File.
        base_path: Base directory for Schedule:File relative paths.
        **plot_kwargs: Additional arguments passed to pandas Series.plot().

    Returns:
        matplotlib Axes object.
    """
    return plot_schedule(
        schedule,
        year=year,
        start_date=(month, day),
        end_date=(month, day),
        document=document,
        day_type=day_type,
        fs=fs,
        base_path=base_path,
        **plot_kwargs,
    )
