"""Day schedule evaluation.

Handles Schedule:Constant, Schedule:Day:Hourly, Schedule:Day:Interval,
and Schedule:Day:List objects.
"""

from __future__ import annotations

import re
from datetime import datetime, time
from typing import TYPE_CHECKING

from idfkit.schedules.time_utils import END_OF_DAY, evaluate_time_values, time_to_minutes
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
        return END_OF_DAY

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
    return evaluate_time_values(time_values, dt.time(), interpolation)


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
            until_time = END_OF_DAY
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

    return evaluate_time_values(time_values, dt.time(), interpolation)


def _parse_interval_time_values(obj: IDFObject) -> list[TimeValue]:
    """Parse time-value pairs from a Schedule:Day:Interval.

    Args:
        obj: The Schedule:Day:Interval object.

    Returns:
        List of TimeValue pairs.

    Raises:
        ValueError: If times are not in ascending order.
    """
    time_values: list[TimeValue] = []

    # Fields are: Time 1, Value Until Time 1, Time 2, Value Until Time 2, ...
    # Maximum 144 intervals (one per 10 minutes)
    prev_minutes = -1.0
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
        current_minutes = time_to_minutes(until_time)

        if current_minutes <= prev_minutes:
            msg = f"Times must be in ascending order: {time_str!r} <= previous"
            raise ValueError(msg)
        prev_minutes = current_minutes

        time_values.append(TimeValue(until_time=until_time, value=float(value)))

    return time_values


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
