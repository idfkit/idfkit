"""Week schedule evaluation.

Handles Schedule:Week:Daily and Schedule:Week:Compact objects.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING

from idfkit.schedules.day_types import DAY_TYPE_PRIORITY, get_applicable_day_types
from idfkit.schedules.types import (
    DAY_TYPE_ALL_OTHER_DAYS,
    DayType,
    Interpolation,
)

if TYPE_CHECKING:
    from idfkit.document import IDFDocument
    from idfkit.objects import IDFObject

# Schedule:Week:Daily field order (EnergyPlus uses Sunday as first day)
_WEEK_DAILY_FIELDS = [
    "Sunday Schedule:Day Name",
    "Monday Schedule:Day Name",
    "Tuesday Schedule:Day Name",
    "Wednesday Schedule:Day Name",
    "Thursday Schedule:Day Name",
    "Friday Schedule:Day Name",
    "Saturday Schedule:Day Name",
    "Holiday Schedule:Day Name",
    "SummerDesignDay Schedule:Day Name",
    "WinterDesignDay Schedule:Day Name",
    "CustomDay1 Schedule:Day Name",
    "CustomDay2 Schedule:Day Name",
]

# Map Python weekday (Monday=0) to Schedule:Week:Daily field index
_WEEKDAY_TO_FIELD_INDEX = {
    0: 1,  # Monday
    1: 2,  # Tuesday
    2: 3,  # Wednesday
    3: 4,  # Thursday
    4: 5,  # Friday
    5: 6,  # Saturday
    6: 0,  # Sunday
}

# Map DayType enum to field index
_DAY_TYPE_TO_FIELD_INDEX = {
    DayType.HOLIDAY: 7,
    DayType.SUMMER_DESIGN: 8,
    DayType.WINTER_DESIGN: 9,
    DayType.CUSTOM_DAY_1: 10,
    DayType.CUSTOM_DAY_2: 11,
}


def _get_day_schedule_name_for_date(
    obj: IDFObject,
    d: date,
    day_type: DayType,
    holidays: set[date],
    custom_day_1: set[date],
    custom_day_2: set[date],
) -> str | None:
    """Get the day schedule name for a specific date from a week schedule.

    Args:
        obj: The Schedule:Week:Daily object.
        d: The date to get the schedule for.
        day_type: Override day type (NORMAL uses calendar day).
        holidays: Set of holiday dates.
        custom_day_1: Set of CustomDay1 dates.
        custom_day_2: Set of CustomDay2 dates.

    Returns:
        The name of the day schedule, or None if not found.
    """
    # Check for explicit day type override
    if day_type != DayType.NORMAL:
        field_index = _DAY_TYPE_TO_FIELD_INDEX.get(day_type)
        if field_index is not None:
            return _get_field_by_index(obj, field_index)

    # Check for special days in order of priority
    if d in custom_day_2:
        return _get_field_by_index(obj, 11)  # CustomDay2
    if d in custom_day_1:
        return _get_field_by_index(obj, 10)  # CustomDay1
    if d in holidays:
        return _get_field_by_index(obj, 7)  # Holiday

    # Use calendar weekday
    field_index = _WEEKDAY_TO_FIELD_INDEX[d.weekday()]
    return _get_field_by_index(obj, field_index)


def _get_field_by_index(obj: IDFObject, index: int) -> str | None:
    """Get a field value by index from Schedule:Week:Daily.

    Args:
        obj: The Schedule:Week:Daily object.
        index: Field index (0-11).

    Returns:
        The field value as a string, or None.
    """
    field_name = _WEEK_DAILY_FIELDS[index]
    value = obj.get(field_name)
    return str(value) if value is not None else None


def evaluate_week_daily(
    obj: IDFObject,
    dt: datetime,
    doc: IDFDocument,
    day_type: DayType = DayType.NORMAL,
    holidays: set[date] | None = None,
    custom_day_1: set[date] | None = None,
    custom_day_2: set[date] | None = None,
    interpolation: Interpolation = Interpolation.NO,
) -> float:
    """Evaluate a Schedule:Week:Daily at a specific datetime.

    Args:
        obj: The Schedule:Week:Daily object.
        dt: The datetime to evaluate.
        doc: The IDF document (for looking up day schedules).
        day_type: Override day type.
        holidays: Set of holiday dates.
        custom_day_1: Set of CustomDay1 dates.
        custom_day_2: Set of CustomDay2 dates.
        interpolation: Interpolation mode.

    Returns:
        The schedule value.

    Raises:
        ValueError: If the referenced day schedule cannot be found.
    """
    from idfkit.schedules.day import (
        evaluate_constant,
        evaluate_day_hourly,
        evaluate_day_interval,
        evaluate_day_list,
    )

    d = dt.date()
    day_name = _get_day_schedule_name_for_date(
        obj,
        d,
        day_type,
        holidays or set(),
        custom_day_1 or set(),
        custom_day_2 or set(),
    )

    if day_name is None:
        return 0.0

    # Look up the day schedule in the document
    day_obj = _find_day_schedule(doc, day_name)
    if day_obj is None:
        msg = f"Day schedule not found: {day_name!r}"
        raise ValueError(msg)

    # Evaluate based on day schedule type
    day_type_str = day_obj.obj_type
    if day_type_str == "Schedule:Constant":
        return evaluate_constant(day_obj, dt)
    elif day_type_str == "Schedule:Day:Hourly":
        return evaluate_day_hourly(day_obj, dt)
    elif day_type_str == "Schedule:Day:Interval":
        return evaluate_day_interval(day_obj, dt, interpolation)
    elif day_type_str == "Schedule:Day:List":
        return evaluate_day_list(day_obj, dt, interpolation)
    else:
        msg = f"Unsupported day schedule type: {day_type_str}"
        raise ValueError(msg)


def _find_day_schedule(doc: IDFDocument, name: str) -> IDFObject | None:
    """Find a day schedule by name in the document.

    Searches all day schedule types.

    Args:
        doc: The IDF document.
        name: The schedule name to find.

    Returns:
        The day schedule object, or None if not found.
    """
    day_types = [
        "Schedule:Day:Hourly",
        "Schedule:Day:Interval",
        "Schedule:Day:List",
        "Schedule:Constant",
    ]

    name_upper = name.upper()
    for sched_type in day_types:
        collection = doc[sched_type]
        for obj in collection:
            if obj.name and obj.name.upper() == name_upper:
                return obj

    return None


def evaluate_week_compact(
    obj: IDFObject,
    dt: datetime,
    doc: IDFDocument,
    day_type: DayType = DayType.NORMAL,
    holidays: set[date] | None = None,
    custom_day_1: set[date] | None = None,
    custom_day_2: set[date] | None = None,
    interpolation: Interpolation = Interpolation.NO,
) -> float:
    """Evaluate a Schedule:Week:Compact at a specific datetime.

    Schedule:Week:Compact uses "DayType List" and "Schedule:Day Name" pairs
    to define which day schedule applies to which day types.

    Args:
        obj: The Schedule:Week:Compact object.
        dt: The datetime to evaluate.
        doc: The IDF document.
        day_type: Override day type.
        holidays: Set of holiday dates.
        custom_day_1: Set of CustomDay1 dates.
        custom_day_2: Set of CustomDay2 dates.
        interpolation: Interpolation mode.

    Returns:
        The schedule value.
    """
    from idfkit.schedules.day import (
        evaluate_constant,
        evaluate_day_hourly,
        evaluate_day_interval,
        evaluate_day_list,
    )

    d = dt.date()

    # Determine what day types apply to this date
    applicable_types = get_applicable_day_types(
        d, day_type, holidays or set(), custom_day_1 or set(), custom_day_2 or set()
    )

    # Find the first matching DayType List / Schedule:Day Name pair
    day_name = _find_matching_day_in_week_compact(obj, applicable_types)

    if day_name is None:
        return 0.0

    # Look up and evaluate the day schedule
    day_obj = _find_day_schedule(doc, day_name)
    if day_obj is None:
        msg = f"Day schedule not found: {day_name!r}"
        raise ValueError(msg)

    day_type_str = day_obj.obj_type
    if day_type_str == "Schedule:Constant":
        return evaluate_constant(day_obj, dt)
    elif day_type_str == "Schedule:Day:Hourly":
        return evaluate_day_hourly(day_obj, dt)
    elif day_type_str == "Schedule:Day:Interval":
        return evaluate_day_interval(day_obj, dt, interpolation)
    elif day_type_str == "Schedule:Day:List":
        return evaluate_day_list(day_obj, dt, interpolation)
    else:
        msg = f"Unsupported day schedule type: {day_type_str}"
        raise ValueError(msg)


def _find_matching_day_in_week_compact(obj: IDFObject, applicable_types: set[str]) -> str | None:
    """Find the day schedule name that matches the applicable day types.

    Schedule:Week:Compact has pairs of fields:
    - "DayType List 1", "Schedule:Day Name 1"
    - "DayType List 2", "Schedule:Day Name 2"
    - etc.

    Args:
        obj: The Schedule:Week:Compact object.
        applicable_types: Set of day type strings that apply.

    Returns:
        The matching day schedule name, or None.
    """
    # Build a map of day type -> schedule name from the object
    type_to_schedule: dict[str, str] = {}

    for i in range(1, 13):  # Max 12 pairs
        daytype_field = f"DayType List {i}"
        schedule_field = f"Schedule:Day Name {i}"

        daytype_value = obj.get(daytype_field)
        schedule_value = obj.get(schedule_field)

        if daytype_value is None or schedule_value is None:
            break

        # DayType List can have multiple day types separated by spaces
        daytype_str = str(daytype_value)
        schedule_name = str(schedule_value)

        for dt_part in daytype_str.split():
            type_to_schedule[dt_part] = schedule_name

    # Find the first matching day type by priority
    for dt in DAY_TYPE_PRIORITY:
        if dt in applicable_types and dt in type_to_schedule:
            return type_to_schedule[dt]

    # Fallback to AllOtherDays if available
    if DAY_TYPE_ALL_OTHER_DAYS in type_to_schedule:
        return type_to_schedule[DAY_TYPE_ALL_OTHER_DAYS]

    return None
