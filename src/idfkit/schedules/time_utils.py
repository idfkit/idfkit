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

#: Sentinel for end-of-day (24:00 mapped to max representable time).
END_OF_DAY = time(23, 59, 59, 999999)

#: Exact minutes corresponding to end-of-day (24 hours).
END_OF_DAY_MINUTES = 1440.0


def time_to_minutes(t: time) -> float:
    """Convert a time to minutes from midnight.

    Detects the :data:`END_OF_DAY` sentinel and returns exactly
    :data:`END_OF_DAY_MINUTES` (1440.0) so that ``Until: 24:00``
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

    current_minutes = time_to_minutes(current_time)

    # Find the interval containing current_time
    prev_value = 0.0
    prev_minutes = 0.0

    for tv in time_values:
        until_minutes = time_to_minutes(tv.until_time)

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
