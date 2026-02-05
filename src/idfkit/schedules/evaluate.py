"""Core schedule evaluation logic.

Provides the main evaluate() and values() functions that dispatch to
type-specific evaluators.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING

from idfkit.schedules.compact import evaluate_compact
from idfkit.schedules.day import (
    evaluate_constant,
    evaluate_day_hourly,
    evaluate_day_interval,
    evaluate_day_list,
)
from idfkit.schedules.file import ScheduleFileCache, evaluate_schedule_file
from idfkit.schedules.holidays import get_holidays, get_special_days_by_type
from idfkit.schedules.types import (
    DayType,
    DayTypeInput,
    Interpolation,
    InterpolationInput,
    parse_day_type,
    parse_interpolation,
)
from idfkit.schedules.week import evaluate_week_compact, evaluate_week_daily
from idfkit.schedules.year import evaluate_year
from idfkit.simulation.fs import FileSystem, LocalFileSystem

if TYPE_CHECKING:
    from idfkit.document import IDFDocument
    from idfkit.objects import IDFObject


class ScheduleEvaluationError(Exception):
    """Base exception for schedule evaluation errors."""

    pass


class UnsupportedScheduleType(ScheduleEvaluationError):
    """Raised when a schedule type is not supported."""

    pass


class ScheduleReferenceError(ScheduleEvaluationError):
    """Raised when a referenced schedule cannot be found."""

    pass


class MalformedScheduleError(ScheduleEvaluationError):
    """Raised when a schedule has invalid syntax."""

    pass


def _get_special_days(document: IDFDocument | None, year: int) -> tuple[set[date], set[date], set[date]]:
    """Get holidays and custom days from document."""
    if document is None:
        return set(), set(), set()
    holidays = get_holidays(document, year)
    custom_day_1 = get_special_days_by_type(document, year, "CustomDay1")
    custom_day_2 = get_special_days_by_type(document, year, "CustomDay2")
    return holidays, custom_day_1, custom_day_2


def _eval_simple_day(schedule: IDFObject, dt: datetime, schedule_type: str) -> float:
    """Evaluate simple day schedule types that don't need document."""
    if schedule_type == "Schedule:Constant":
        return evaluate_constant(schedule, dt)
    if schedule_type == "Schedule:Day:Hourly":
        return evaluate_day_hourly(schedule, dt)
    if schedule_type == "Schedule:Day:Interval":
        return evaluate_day_interval(schedule, dt)
    if schedule_type == "Schedule:Day:List":
        return evaluate_day_list(schedule, dt)
    msg = f"Not a simple day schedule: {schedule_type}"
    raise ValueError(msg)


# Schedule types that don't need a document reference
_SIMPLE_DAY_TYPES = frozenset([
    "Schedule:Constant",
    "Schedule:Day:Hourly",
    "Schedule:Day:Interval",
    "Schedule:Day:List",
])

# Schedule types that require a document
_DOCUMENT_REQUIRED_TYPES = frozenset(["Schedule:Week:Daily", "Schedule:Week:Compact", "Schedule:Year"])


def evaluate(
    schedule: IDFObject,
    dt: datetime,
    document: IDFDocument | None = None,
    day_type: DayTypeInput | None = None,
    fs: FileSystem | None = None,
    base_path: Path | str | None = None,
) -> float:
    """Evaluate a schedule at a specific datetime.

    Args:
        schedule: An IDF schedule object (any supported type).
        dt: The datetime to evaluate.
        document: Required for schedules that reference others (Year, Week).
                  If None, extracted from schedule._document if available.
        day_type: Override with design day schedule (for sizing calculations).
                  Accepts "normal", "summer", "winter", "holiday", "customday1", "customday2".
        fs: FileSystem for Schedule:File (default: LocalFileSystem).
        base_path: Base directory for Schedule:File relative paths.

    Returns:
        The schedule value as a float.

    Raises:
        ScheduleEvaluationError: If schedule type is unsupported or malformed.
        ScheduleReferenceError: If a referenced schedule cannot be found.

    Examples:
        >>> evaluate(schedule, datetime(2024, 7, 15, 14, 0))  # Normal evaluation
        >>> evaluate(schedule, dt, day_type="summer")  # Summer design day
        >>> evaluate(schedule, dt, day_type="winter")  # Winter design day
    """
    if document is None:
        document = getattr(schedule, "_document", None)

    day_type_enum = parse_day_type(day_type)
    schedule_type = schedule.obj_type

    try:
        # Simple day schedules
        if schedule_type in _SIMPLE_DAY_TYPES:
            return _eval_simple_day(schedule, dt, schedule_type)

        # Get special days for complex types
        holidays, custom_day_1, custom_day_2 = _get_special_days(document, dt.year)

        # Document-required types
        if schedule_type in _DOCUMENT_REQUIRED_TYPES:
            if document is None:
                msg = f"Document required for {schedule_type} evaluation"
                raise ScheduleReferenceError(msg)
            return _eval_document_schedule(schedule, dt, document, day_type_enum, holidays, custom_day_1, custom_day_2)

        # Schedule:Compact
        if schedule_type == "Schedule:Compact":
            return evaluate_compact(schedule, dt, day_type_enum, holidays, custom_day_1, custom_day_2)

        # Schedule:File
        if schedule_type == "Schedule:File":
            return evaluate_schedule_file(schedule, dt, fs or LocalFileSystem(), base_path)

        msg = f"Unsupported schedule type: {schedule_type}"
        raise UnsupportedScheduleType(msg)

    except ScheduleEvaluationError:
        raise
    except (ValueError, KeyError) as e:
        msg = f"Error evaluating {schedule_type}: {e}"
        raise MalformedScheduleError(msg) from e


def _eval_document_schedule(
    schedule: IDFObject,
    dt: datetime,
    document: IDFDocument,
    day_type: DayType,
    holidays: set[date],
    custom_day_1: set[date],
    custom_day_2: set[date],
) -> float:
    """Evaluate schedule types that require a document."""
    schedule_type = schedule.obj_type
    if schedule_type == "Schedule:Week:Daily":
        return evaluate_week_daily(schedule, dt, document, day_type, holidays, custom_day_1, custom_day_2)
    if schedule_type == "Schedule:Week:Compact":
        return evaluate_week_compact(schedule, dt, document, day_type, holidays, custom_day_1, custom_day_2)
    if schedule_type == "Schedule:Year":
        return evaluate_year(schedule, dt, document, day_type, holidays, custom_day_1, custom_day_2)
    msg = f"Not a document schedule: {schedule_type}"
    raise ValueError(msg)


def values(
    schedule: IDFObject,
    year: int = 2024,
    timestep: int = 1,
    start_date: tuple[int, int] = (1, 1),
    end_date: tuple[int, int] = (12, 31),
    document: IDFDocument | None = None,
    day_type: DayTypeInput | None = None,
    interpolation: InterpolationInput | None = None,
    fs: FileSystem | None = None,
    base_path: Path | str | None = None,
) -> list[float]:
    """Generate schedule values for a date range.

    Args:
        schedule: An IDF schedule object.
        year: Year for the date range.
        timestep: Values per hour (1, 2, 4, 6, 12, or 60).
        start_date: Start date as (month, day).
        end_date: End date as (month, day).
        document: Required for schedules that reference others.
        day_type: Override day type for all days.
                  Accepts "normal", "summer", "winter", "holiday", "customday1", "customday2".
        interpolation: Interpolation mode for sub-hourly values.
                       Accepts "no", "step", "average", "linear".
        fs: FileSystem for Schedule:File.
        base_path: Base directory for Schedule:File relative paths.

    Returns:
        List of values, one per timestep for the entire period.

    Examples:
        >>> values(schedule, year=2024)  # Hourly values for full year
        >>> values(schedule, year=2024, timestep=4)  # 15-minute intervals
        >>> values(schedule, year=2024, day_type="summer")  # Summer design day
    """
    # Get document from schedule if not provided
    if document is None:
        document = getattr(schedule, "_document", None)

    # Parse enum inputs
    day_type_enum = parse_day_type(day_type)
    interpolation_enum = parse_interpolation(interpolation)

    # Get holidays and custom days
    holidays: set[date] = set()
    custom_day_1: set[date] = set()
    custom_day_2: set[date] = set()

    if document is not None:
        holidays = get_holidays(document, year)
        custom_day_1 = get_special_days_by_type(document, year, "CustomDay1")
        custom_day_2 = get_special_days_by_type(document, year, "CustomDay2")

    # Calculate time step in minutes
    minutes_per_step = 60 // timestep

    # Build the date range
    start = datetime(year, start_date[0], start_date[1], 0, 0)
    end = datetime(year, end_date[0], end_date[1], 23, 59)

    result: list[float] = []
    current = start

    # Pre-compute for Schedule:File
    schedule_type = schedule.obj_type
    file_cache: ScheduleFileCache | None = None
    if schedule_type == "Schedule:File":
        file_cache = ScheduleFileCache()

    while current <= end:
        value = _evaluate_with_interpolation(
            schedule,
            current,
            document,
            day_type_enum,
            holidays,
            custom_day_1,
            custom_day_2,
            interpolation_enum,
            fs,
            base_path,
            file_cache,
        )
        result.append(value)
        current += timedelta(minutes=minutes_per_step)

    return result


def _evaluate_with_interpolation(
    schedule: IDFObject,
    dt: datetime,
    document: IDFDocument | None,
    day_type: DayType,
    holidays: set[date],
    custom_day_1: set[date],
    custom_day_2: set[date],
    interpolation: Interpolation,
    fs: FileSystem | None,
    base_path: Path | str | None,
    file_cache: ScheduleFileCache | None,
) -> float:
    """Evaluate with interpolation support."""
    schedule_type = schedule.obj_type

    # Day schedules with native interpolation support
    if schedule_type == "Schedule:Day:Interval":
        return evaluate_day_interval(schedule, dt, interpolation)
    if schedule_type == "Schedule:Day:List":
        return evaluate_day_list(schedule, dt, interpolation)

    # Schedule:File with interpolation
    if schedule_type == "Schedule:File":
        return evaluate_schedule_file(schedule, dt, fs or LocalFileSystem(), base_path, file_cache, interpolation)

    # Week/Year schedules need document and pass interpolation through
    if schedule_type in _DOCUMENT_REQUIRED_TYPES:
        if document is None:
            msg = f"Document required for {schedule_type} evaluation"
            raise ScheduleReferenceError(msg)
        return _eval_document_with_interp(
            schedule, dt, document, day_type, holidays, custom_day_1, custom_day_2, interpolation
        )

    # For other types, use simple evaluation
    return evaluate(schedule, dt, document, day_type, fs, base_path)


def _eval_document_with_interp(
    schedule: IDFObject,
    dt: datetime,
    document: IDFDocument,
    day_type: DayType,
    holidays: set[date],
    custom_day_1: set[date],
    custom_day_2: set[date],
    interpolation: Interpolation,
) -> float:
    """Evaluate document-dependent schedules with interpolation."""
    schedule_type = schedule.obj_type
    if schedule_type == "Schedule:Week:Daily":
        return evaluate_week_daily(
            schedule, dt, document, day_type, holidays, custom_day_1, custom_day_2, interpolation
        )
    if schedule_type == "Schedule:Week:Compact":
        return evaluate_week_compact(
            schedule, dt, document, day_type, holidays, custom_day_1, custom_day_2, interpolation
        )
    if schedule_type == "Schedule:Year":
        return evaluate_year(schedule, dt, document, day_type, holidays, custom_day_1, custom_day_2, interpolation)
    msg = f"Not a document schedule: {schedule_type}"
    raise ValueError(msg)
