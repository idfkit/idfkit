"""Shared time utilities for schedule evaluation.

Provides time conversion and time-value evaluation functions used by
both day.py and compact.py.

A day schedule is evaluated the way EnergyPlus evaluates it, so that the values are the same
doubles EnergyPlus computes: the day is expanded to one value per minute
([day_minute_values][idfkit.schedules.time_utils.day_minute_values]), and a timestep takes its
value from those minutes ([timestep_value][idfkit.schedules.time_utils.timestep_value]).
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import time
from functools import lru_cache
from typing import TYPE_CHECKING

from idfkit.schedules.types import Interpolation

if TYPE_CHECKING:
    from idfkit.schedules.types import TimeValue

__all__ = [
    "END_OF_DAY",
    "END_OF_DAY_MINUTES",
    "MINUTES_PER_DAY",
    "day_minute_values",
    "evaluate_time_values",
    "parse_interpolate_keyword",
    "step_minute_values",
    "time_to_minutes",
    "timestep_value",
]

#: Minutes in a day: the length of a day's minute values.
MINUTES_PER_DAY = 1440

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
        interpolation: Interpolation mode, as in
            [day_minute_values][idfkit.schedules.time_utils.day_minute_values].
        interval_minutes: Length of the timestep starting at ``current_time``. The value is then
            the one EnergyPlus reports for that timestep: see
            [timestep_value][idfkit.schedules.time_utils.timestep_value]. With the default of 0
            (a point evaluation) it is the value of the minute containing ``current_time``.

    Returns:
        The schedule value at the given time.
    """
    if not time_values:
        return 0.0
    minutes = day_minute_values(tuple((tv.until_time, tv.value) for tv in time_values), interpolation)
    start = min(int(time_to_minutes(current_time)), MINUTES_PER_DAY - 1)
    if interval_minutes > 0:
        return timestep_value(minutes, start, int(interval_minutes), interpolation)
    return minutes[start]


@lru_cache(maxsize=1024)
def day_minute_values(pairs: tuple[tuple[time, float], ...], interpolation: Interpolation) -> tuple[float, ...]:
    """Expand ``Until:`` time-value pairs to one value per minute, as EnergyPlus does.

    This follows EnergyPlus's ``ProcessIntervalFields``. Each value holds from the previous
    ``Until:`` time up to, not including, its own. With ``LINEAR`` the first interval is flat and
    each later one ramps from the previous value: minute ``k`` (from 1) of an interval of ``n``
    minutes holds ``start + k * (end - start) / n``, accumulated minute by minute in the same
    order as EnergyPlus, so the doubles are the same. Minutes after the last ``Until:`` hold its
    value (EnergyPlus refuses such a day).

    Args:
        pairs: ``(until_time, value)`` pairs, sorted by time.
        interpolation: Interpolation mode; only ``LINEAR`` changes the minute values.

    Returns:
        1440 values, one per minute of the day.
    """
    minutes = [0.0] * MINUTES_PER_DAY
    begin = 0
    end_value = 0.0
    for count, (until_time, value) in enumerate(pairs):
        until = min(int(time_to_minutes(until_time)), MINUTES_PER_DAY)
        if interpolation is Interpolation.LINEAR:
            start_value = value if count == 0 else end_value
            end_value = value
            increment = (end_value - start_value) / ((until - begin) or 1)
            current = start_value + increment
            for minute in range(begin, until):
                minutes[minute] = current
                current += increment
        else:
            minutes[begin:until] = [value] * max(until - begin, 0)
        begin = max(begin, until)
    if begin < MINUTES_PER_DAY:
        minutes[begin:] = [pairs[-1][1]] * (MINUTES_PER_DAY - begin)
    return tuple(minutes)


@lru_cache(maxsize=1024)
def step_minute_values(items: tuple[float, ...], minutes_per_item: int) -> tuple[float, ...]:
    """Minute values for evenly spaced items, as EnergyPlus fills a Day:List or Schedule:File day.

    Item ``k`` holds minutes ``[k * minutes_per_item, (k + 1) * minutes_per_item)``. Minutes past
    the last item hold its value (EnergyPlus refuses a day the items do not fill).

    Args:
        items: The day's values, in order.
        minutes_per_item: Minutes each item lasts.

    Returns:
        1440 values, one per minute of the day.
    """
    return tuple(items[min(minute // minutes_per_item, len(items) - 1)] for minute in range(MINUTES_PER_DAY))


def timestep_value(minutes: Sequence[float], start: int, length: int, interpolation: Interpolation) -> float:
    """The value EnergyPlus reports for the timestep of ``length`` minutes starting at minute ``start``.

    This follows EnergyPlus's ``populateFromMinuteVals``: with ``AVERAGE`` the minutes of the
    timestep are summed in order and divided by their count; otherwise the timestep takes the
    value of its last minute.

    Args:
        minutes: The day's 1440 minute values.
        start: First minute of the timestep.
        length: Minutes in the timestep.
        interpolation: Interpolation mode.

    Returns:
        The timestep's value.
    """
    end = min(start + length, len(minutes))
    if interpolation is Interpolation.AVERAGE:
        accum = 0.0
        for minute in range(start, end):
            accum += minutes[minute]
        return accum / float(length)
    return minutes[end - 1]
