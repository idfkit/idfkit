"""Shared time utilities for schedule evaluation.

Provides time conversion and time-value evaluation functions used by
both day.py and compact.py.
"""

from __future__ import annotations

from datetime import time
from typing import TYPE_CHECKING

from idfkit.schedules.types import Interpolation

if TYPE_CHECKING:
    from idfkit.schedules.types import TimeValue

__all__ = [
    "END_OF_DAY",
    "END_OF_DAY_MINUTES",
    "evaluate_time_values",
    "parse_interpolate_keyword",
    "time_to_minutes",
]

#: Sentinel for end-of-day (24:00 mapped to max representable time).
END_OF_DAY = time(23, 59, 59, 999999)

#: Exact minutes corresponding to end-of-day (24 hours).
END_OF_DAY_MINUTES = 1440.0


_INTERPOLATE_KEYWORDS = {
    "no": Interpolation.NO,
    "yes": Interpolation.AVERAGE,
    "average": Interpolation.AVERAGE,
    "linear": Interpolation.LINEAR,
}


def parse_interpolate_keyword(value: object) -> Interpolation | None:
    """Read an EnergyPlus interpolation keyword (``No``, ``Yes``, ``Average``, ``Linear``).

    Args:
        value: The field value, such as a Schedule:Compact ``Interpolate:`` argument or a day
            schedule's ``Interpolate to Timestep``.

    Returns:
        The interpolation mode, or None when the value is blank or not a keyword.
    """
    if value is None:
        return None
    return _INTERPOLATE_KEYWORDS.get(str(value).strip().lower())


def time_to_minutes(t: time) -> float:
    """Convert a time to minutes from midnight.

    Detects the [END_OF_DAY][idfkit.schedules.time_utils.END_OF_DAY] sentinel and returns exactly
    [END_OF_DAY_MINUTES][idfkit.schedules.time_utils.END_OF_DAY_MINUTES] (1440.0) so that ``Until: 24:00``
    intervals cover the full day without floating-point drift.

    Args:
        t: Time to convert.

    Returns:
        Minutes from midnight as a float.
    """
    if t == END_OF_DAY:
        return END_OF_DAY_MINUTES
    return t.hour * 60 + t.minute + t.second / 60 + t.microsecond / 60_000_000


def evaluate_time_values(
    time_values: list[TimeValue],
    current_time: time,
    interpolation: Interpolation,
    interval_minutes: float = 0.0,
) -> float:
    """Evaluate a list of time-value pairs at a given time.

    Args:
        time_values: List of TimeValue pairs (must be sorted by time).
        current_time: Time to evaluate, the start of the timestep.
        interpolation: Interpolation mode. ``AVERAGE`` returns the mean of the step function
            over ``[current_time, current_time + interval_minutes)``, as EnergyPlus does for
            ``Average``; ``LINEAR`` interpolates linearly between ``Until:`` values.
        interval_minutes: Length of the timestep the value stands for. With the default of 0
            (a point evaluation) ``AVERAGE`` gives the step value.

    Returns:
        The schedule value at the given time.
    """
    if not time_values:
        return 0.0

    current_minutes = time_to_minutes(current_time)

    if interpolation is Interpolation.AVERAGE and interval_minutes > 0:
        return _step_mean(time_values, current_minutes, interval_minutes)

    # Find the interval containing current_time
    prev_value = 0.0
    prev_minutes = 0.0

    for tv in time_values:
        until_minutes = time_to_minutes(tv.until_time)

        # "Until: HH:MM" means value applies for times < HH:MM
        # At exactly HH:MM, we transition to the next interval
        if current_minutes < until_minutes:
            if interpolation is Interpolation.LINEAR and until_minutes > prev_minutes:
                fraction = (current_minutes - prev_minutes) / (until_minutes - prev_minutes)
                return prev_value + fraction * (tv.value - prev_value)
            # Step function: return the value for this interval
            return tv.value

        prev_value = tv.value
        prev_minutes = until_minutes

    # Past all intervals, return last value
    return time_values[-1].value


def _step_mean(time_values: list[TimeValue], start: float, length: float) -> float:
    """Mean of the step function defined by ``time_values`` over ``[start, start + length)``."""
    end = start + length
    total = 0.0
    prev_minutes = 0.0
    for tv in time_values:
        until_minutes = time_to_minutes(tv.until_time)
        overlap = min(end, until_minutes) - max(start, prev_minutes)
        if overlap > 0:
            total += overlap * tv.value
        prev_minutes = until_minutes
        if prev_minutes >= end:
            break
    else:
        # Past the last Until: the last value holds, as in the step evaluation.
        total += (end - max(start, prev_minutes)) * time_values[-1].value
    return total / length
