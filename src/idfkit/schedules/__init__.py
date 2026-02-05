"""Schedule evaluation module for idfkit.

This module provides functions to evaluate EnergyPlus schedules without
running a simulation. It supports all standard schedule types including
Schedule:Compact, Schedule:Year, Schedule:Week:*, Schedule:Day:*, and
Schedule:File.

Basic Usage
-----------

.. code-block:: python

    from datetime import datetime
    from idfkit import load_idf
    from idfkit.schedules import evaluate, values, to_series

    # Load a model
    doc = load_idf("building.idf")

    # Get a schedule
    schedule = doc["Schedule:Compact"]["Office Occupancy"]

    # Evaluate at a specific time
    value = evaluate(schedule, datetime(2024, 1, 8, 10, 0))
    print(f"Value at Monday 10am: {value}")

    # Get hourly values for a full year
    hourly = values(schedule, year=2024)
    print(f"Annual values: {len(hourly)} hours")

    # Convert to pandas Series for plotting (requires pandas)
    series = to_series(schedule, year=2024)
    series.plot()

Design Day Schedules
--------------------

For sizing calculations, you can override the calendar day type using strings:

.. code-block:: python

    from idfkit.schedules import evaluate

    # Evaluate using summer design day schedule
    value = evaluate(
        schedule,
        datetime(2024, 7, 15, 14, 0),
        day_type="summer"  # Options: "normal", "summer", "winter", "holiday"
    )

Schedule:File with Remote Storage
---------------------------------

Schedule:File objects can read CSV files from any storage backend:

.. code-block:: python

    from idfkit.simulation.fs import S3FileSystem
    from idfkit.schedules import values

    # Read CSV from S3
    fs = S3FileSystem(bucket="models", prefix="data/")
    hourly = values(schedule, fs=fs)
"""

from __future__ import annotations

from idfkit.schedules.evaluate import (
    MalformedScheduleError,
    ScheduleEvaluationError,
    ScheduleReferenceError,
    UnsupportedScheduleType,
    evaluate,
    values,
)
from idfkit.schedules.file import ScheduleFileCache
from idfkit.schedules.holidays import (
    extract_special_days,
    get_holidays,
    get_special_days_by_type,
)
from idfkit.schedules.series import plot_day, plot_schedule, plot_week, to_series
from idfkit.schedules.types import (
    CompactDayRule,
    CompactPeriod,
    DayType,
    DayTypeInput,
    DayTypeLiteral,
    Interpolation,
    InterpolationInput,
    InterpolationLiteral,
    SpecialDay,
    TimeValue,
)

__all__ = [
    "CompactDayRule",
    "CompactPeriod",
    "DayType",
    "DayTypeInput",
    "DayTypeLiteral",
    "Interpolation",
    "InterpolationInput",
    "InterpolationLiteral",
    "MalformedScheduleError",
    "ScheduleEvaluationError",
    "ScheduleFileCache",
    "ScheduleReferenceError",
    "SpecialDay",
    "TimeValue",
    "UnsupportedScheduleType",
    "evaluate",
    "extract_special_days",
    "get_holidays",
    "get_special_days_by_type",
    "plot_day",
    "plot_schedule",
    "plot_week",
    "to_series",
    "values",
]
