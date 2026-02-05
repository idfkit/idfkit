"""Day schedule evaluation.

Handles Schedule:Constant, Schedule:Day:Hourly, Schedule:Day:Interval,
and Schedule:Day:List objects.
"""

from __future__ import annotations

import re
from datetime import datetime, time
from typing import TYPE_CHECKING

from idfkit.schedules.types import Interpolation, TimeValue

if TYPE_CHECKING:
    from idfkit.objects import IDFObject


def _parse_time(time_str: str) -> time:
    """Parse an EnergyPlus time string.

    Formats: "HH:MM", "H:MM", "HH:MM:SS", or just "HH" (hour only).
    Special case: "24:00" means end of day (treated as 23:59:59.999999).

    Args:
        time_str: Time string to parse.

    Returns:
        Python time object.
    """
    time_str = time_str.strip()

    # Handle "24:00" as end of day
    if time_str.startswith("24"):
        return time(23, 59, 59, 999999)

    # Try various formats
    # HH:MM:SS
    match = re.match(r"^(\d{1,2}):(\d{2}):(\d{2})$", time_str)
    if match:
        return time(int(match[1]), int(match[2]), int(match[3]))

    # HH:MM
    match = re.match(r"^(\d{1,2}):(\d{2})$", time_str)
    if match:
        return time(int(match[1]), int(match[2]))

    # HH only
    match = re.match(r"^(\d{1,2})$", time_str)
    if match:
        return time(int(match[1]), 0)

    msg = f"Cannot parse time: {time_str!r}"
    raise ValueError(msg)


def _time_to_minutes(t: time) -> float:
    """Convert a time to minutes from midnight."""
    return t.hour * 60 + t.minute + t.second / 60 + t.microsecond / 60_000_000


def evaluate_constant(obj: IDFObject, dt: datetime) -> float:
    """Evaluate a Schedule:Constant.

    Args:
        obj: The Schedule:Constant object.
        dt: The datetime to evaluate (unused, value is constant).

    Returns:
        The constant schedule value.
    """
    _ = dt  # Unused but kept for consistent interface
    value = obj.get("Hourly Value")
    if value is None:
        return 0.0
    return float(value)


def evaluate_day_hourly(obj: IDFObject, dt: datetime) -> float:
    """Evaluate a Schedule:Day:Hourly.

    This schedule type has 24 values, one for each hour of the day.

    Args:
        obj: The Schedule:Day:Hourly object.
        dt: The datetime to evaluate.

    Returns:
        The schedule value for the given hour.
    """
    hour = dt.hour  # 0-23
    field_name = f"Hour {hour + 1}"  # Fields are "Hour 1" through "Hour 24"
    value = obj.get(field_name)
    if value is None:
        return 0.0
    return float(value)


def evaluate_day_interval(
    obj: IDFObject,
    dt: datetime,
    interpolation: Interpolation = Interpolation.NO,
) -> float:
    """Evaluate a Schedule:Day:Interval.

    This schedule type has time/value pairs where each value applies
    UNTIL the specified time.

    Args:
        obj: The Schedule:Day:Interval object.
        dt: The datetime to evaluate.
        interpolation: Interpolation mode.

    Returns:
        The schedule value at the given time.
    """
    time_values = _parse_interval_time_values(obj)
    return _evaluate_time_values(time_values, dt.time(), interpolation)


def evaluate_day_list(
    obj: IDFObject,
    dt: datetime,
    interpolation: Interpolation = Interpolation.NO,
) -> float:
    """Evaluate a Schedule:Day:List.

    This schedule type has values at fixed intervals.

    Args:
        obj: The Schedule:Day:List object.
        dt: The datetime to evaluate.
        interpolation: Interpolation mode.

    Returns:
        The schedule value at the given time.
    """
    # Get minutes per item (default 60)
    minutes_per_item = obj.get("Minutes per Item")
    minutes_per_item = 60 if minutes_per_item is None else int(minutes_per_item)

    # Get interpolate setting from the object
    interpolate_field = obj.get("Interpolate to Timestep")
    if interpolate_field:
        interpolate_str = str(interpolate_field).lower()
        if interpolate_str in ("average", "linear", "yes"):
            interpolation = Interpolation.AVERAGE

    # Build time-value pairs from the list
    time_values: list[TimeValue] = []
    current_minutes = 0
    i = 1

    while True:
        field_name = f"Value {i}"
        value = obj.get(field_name)
        if value is None:
            break

        current_minutes += minutes_per_item
        # Cap at end of day
        if current_minutes >= 1440:
            until_time = time(23, 59, 59, 999999)
        else:
            hours = current_minutes // 60
            mins = current_minutes % 60
            until_time = time(hours, mins)

        time_values.append(TimeValue(until_time=until_time, value=float(value)))
        i += 1

        if current_minutes >= 1440:
            break

    if not time_values:
        return 0.0

    return _evaluate_time_values(time_values, dt.time(), interpolation)


def _parse_interval_time_values(obj: IDFObject) -> list[TimeValue]:
    """Parse time-value pairs from a Schedule:Day:Interval.

    Args:
        obj: The Schedule:Day:Interval object.

    Returns:
        List of TimeValue pairs.
    """
    time_values: list[TimeValue] = []

    # Fields are: Time 1, Value Until Time 1, Time 2, Value Until Time 2, ...
    # Maximum 144 intervals (one per 10 minutes)
    for i in range(1, 145):
        time_field = f"Time {i}"
        value_field = f"Value Until Time {i}"

        time_str = obj.get(time_field)
        if time_str is None:
            break

        value = obj.get(value_field)
        if value is None:
            break

        until_time = _parse_time(str(time_str))
        time_values.append(TimeValue(until_time=until_time, value=float(value)))

    return time_values


def _evaluate_time_values(
    time_values: list[TimeValue],
    current_time: time,
    interpolation: Interpolation,
) -> float:
    """Evaluate a list of time-value pairs at a given time.

    Args:
        time_values: List of TimeValue pairs (must be sorted by time).
        current_time: Time to evaluate.
        interpolation: Interpolation mode.

    Returns:
        The schedule value at the given time.
    """
    if not time_values:
        return 0.0

    current_minutes = _time_to_minutes(current_time)

    # Find the interval containing current_time
    prev_value = 0.0
    prev_minutes = 0.0

    for tv in time_values:
        until_minutes = _time_to_minutes(tv.until_time)

        # "Until: HH:MM" means value applies for times < HH:MM
        # At exactly HH:MM, we transition to the next interval
        if current_minutes < until_minutes:
            # Linear interpolation when enabled and interval is valid
            should_interpolate = (
                interpolation in (Interpolation.AVERAGE, Interpolation.LINEAR) and until_minutes > prev_minutes
            )
            if should_interpolate:
                fraction = (current_minutes - prev_minutes) / (until_minutes - prev_minutes)
                return prev_value + fraction * (tv.value - prev_value)
            # Step function: return the value for this interval
            return tv.value

        prev_value = tv.value
        prev_minutes = until_minutes

    # Past all intervals, return last value
    return time_values[-1].value


def get_day_values(
    obj: IDFObject,
    timestep: int = 1,
    interpolation: Interpolation = Interpolation.NO,
) -> list[float]:
    """Get all values for a day schedule at the specified timestep.

    Args:
        obj: A day schedule object (Constant, Hourly, Interval, or List).
        timestep: Number of values per hour (1, 2, 4, 6, 12, or 60).
        interpolation: Interpolation mode.

    Returns:
        List of values for the day (24 * timestep values).
    """
    obj_type = obj.obj_type
    values: list[float] = []

    minutes_per_step = 60 // timestep

    for hour in range(24):
        for step in range(timestep):
            minute = step * minutes_per_step
            dt = datetime(2024, 1, 1, hour, minute)

            if obj_type == "Schedule:Constant":
                value = evaluate_constant(obj, dt)
            elif obj_type == "Schedule:Day:Hourly":
                value = evaluate_day_hourly(obj, dt)
            elif obj_type == "Schedule:Day:Interval":
                value = evaluate_day_interval(obj, dt, interpolation)
            elif obj_type == "Schedule:Day:List":
                value = evaluate_day_list(obj, dt, interpolation)
            else:
                msg = f"Unsupported day schedule type: {obj_type}"
                raise ValueError(msg)

            values.append(value)

    return values
