"""Shared day-type utilities for schedule evaluation.

Provides :data:`DAY_TYPE_PRIORITY` ordering and :func:`get_applicable_day_types`
used by both compact.py and week.py.
"""

from __future__ import annotations

from datetime import date

from idfkit.schedules.types import (
    DAY_TYPE_ALL_OTHER_DAYS,
    DAY_TYPE_ALLDAYS,
    DAY_TYPE_CUSTOM_DAY_1,
    DAY_TYPE_CUSTOM_DAY_2,
    DAY_TYPE_FRIDAY,
    DAY_TYPE_HOLIDAY,
    DAY_TYPE_MONDAY,
    DAY_TYPE_SATURDAY,
    DAY_TYPE_SUMMER_DESIGN,
    DAY_TYPE_SUNDAY,
    DAY_TYPE_THURSDAY,
    DAY_TYPE_TUESDAY,
    DAY_TYPE_WEDNESDAY,
    DAY_TYPE_WEEKDAYS,
    DAY_TYPE_WEEKENDS,
    DAY_TYPE_WINTER_DESIGN,
    WEEKDAY_TO_DAY_TYPE,
    DayType,
)

#: Priority order for day-type matching (more specific first).
DAY_TYPE_PRIORITY: list[str] = [
    DAY_TYPE_SUMMER_DESIGN,
    DAY_TYPE_WINTER_DESIGN,
    DAY_TYPE_CUSTOM_DAY_2,
    DAY_TYPE_CUSTOM_DAY_1,
    DAY_TYPE_HOLIDAY,
    DAY_TYPE_SUNDAY,
    DAY_TYPE_MONDAY,
    DAY_TYPE_TUESDAY,
    DAY_TYPE_WEDNESDAY,
    DAY_TYPE_THURSDAY,
    DAY_TYPE_FRIDAY,
    DAY_TYPE_SATURDAY,
    DAY_TYPE_WEEKDAYS,
    DAY_TYPE_WEEKENDS,
    DAY_TYPE_ALLDAYS,
    DAY_TYPE_ALL_OTHER_DAYS,
]


def get_applicable_day_types(
    d: date,
    day_type: DayType,
    holidays: set[date],
    custom_day_1: set[date],
    custom_day_2: set[date],
) -> set[str]:
    """Get all day types that apply to a date.

    Args:
        d: The date.
        day_type: Override day type.
        holidays: Set of holiday dates.
        custom_day_1: Set of CustomDay1 dates.
        custom_day_2: Set of CustomDay2 dates.

    Returns:
        Set of applicable day type strings.
    """
    types: set[str] = set()

    # Handle explicit override
    if day_type == DayType.SUMMER_DESIGN:
        types.add(DAY_TYPE_SUMMER_DESIGN)
        types.add(DAY_TYPE_ALLDAYS)
        return types
    if day_type == DayType.WINTER_DESIGN:
        types.add(DAY_TYPE_WINTER_DESIGN)
        types.add(DAY_TYPE_ALLDAYS)
        return types
    if day_type == DayType.HOLIDAY:
        types.add(DAY_TYPE_HOLIDAY)
        types.add(DAY_TYPE_ALLDAYS)
        return types
    if day_type == DayType.CUSTOM_DAY_1:
        types.add(DAY_TYPE_CUSTOM_DAY_1)
        types.add(DAY_TYPE_ALLDAYS)
        return types
    if day_type == DayType.CUSTOM_DAY_2:
        types.add(DAY_TYPE_CUSTOM_DAY_2)
        types.add(DAY_TYPE_ALLDAYS)
        return types

    # Check special days
    if d in custom_day_2:
        types.add(DAY_TYPE_CUSTOM_DAY_2)
    if d in custom_day_1:
        types.add(DAY_TYPE_CUSTOM_DAY_1)
    if d in holidays:
        types.add(DAY_TYPE_HOLIDAY)

    # Add weekday type
    weekday = d.weekday()
    types.add(WEEKDAY_TO_DAY_TYPE[weekday])

    # Add group types
    if weekday < 5:  # Monday-Friday
        types.add(DAY_TYPE_WEEKDAYS)
    else:  # Saturday-Sunday
        types.add(DAY_TYPE_WEEKENDS)

    types.add(DAY_TYPE_ALLDAYS)
    types.add(DAY_TYPE_ALL_OTHER_DAYS)

    return types
