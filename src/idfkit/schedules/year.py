"""Year schedule evaluation.

Handles Schedule:Year objects which reference week schedules for date ranges.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING

from idfkit.schedules.types import DayType, Interpolation

if TYPE_CHECKING:
    from idfkit.document import IDFDocument
    from idfkit.objects import IDFObject


def _parse_month_day(month_str: str, day_str: str) -> tuple[int, int]:
    """Parse month and day fields from Schedule:Year.

    Args:
        month_str: Month value (number or name).
        day_str: Day value.

    Returns:
        Tuple of (month, day).
    """
    # Month can be a number or name
    month_names = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12,
    }

    month_str = str(month_str).strip().lower()
    month = month_names[month_str] if month_str in month_names else int(month_str)

    day = int(day_str)
    return month, day


def evaluate_year(
    obj: IDFObject,
    dt: datetime,
    doc: IDFDocument,
    day_type: DayType = DayType.NORMAL,
    holidays: set[date] | None = None,
    custom_day_1: set[date] | None = None,
    custom_day_2: set[date] | None = None,
    interpolation: Interpolation = Interpolation.NO,
) -> float:
    """Evaluate a Schedule:Year at a specific datetime.

    Schedule:Year defines date ranges that reference week schedules.

    Args:
        obj: The Schedule:Year object.
        dt: The datetime to evaluate.
        doc: The IDF document.
        day_type: Override day type.
        holidays: Set of holiday dates.
        custom_day_1: Set of CustomDay1 dates.
        custom_day_2: Set of CustomDay2 dates.
        interpolation: Interpolation mode.

    Returns:
        The schedule value.

    Raises:
        ValueError: If the week schedule cannot be found or date is out of range.
    """
    from idfkit.schedules.week import evaluate_week_compact, evaluate_week_daily

    d = dt.date()
    year = dt.year

    # Find the week schedule for this date
    week_name, week_obj = _find_week_for_date(obj, d, year, doc)

    if week_obj is None:
        msg = f"Week schedule not found: {week_name!r}"
        raise ValueError(msg)

    # Evaluate based on week schedule type
    week_type = week_obj.obj_type
    if week_type == "Schedule:Week:Daily":
        return evaluate_week_daily(
            week_obj,
            dt,
            doc,
            day_type,
            holidays,
            custom_day_1,
            custom_day_2,
            interpolation,
        )
    elif week_type == "Schedule:Week:Compact":
        return evaluate_week_compact(
            week_obj,
            dt,
            doc,
            day_type,
            holidays,
            custom_day_1,
            custom_day_2,
            interpolation,
        )
    else:
        msg = f"Unsupported week schedule type: {week_type}"
        raise ValueError(msg)


def _find_week_for_date(
    obj: IDFObject,
    d: date,
    year: int,
    doc: IDFDocument,
) -> tuple[str, IDFObject | None]:
    """Find the week schedule that covers a specific date.

    Schedule:Year has repeating groups of:
    - Schedule:Week Name
    - Start Month
    - Start Day
    - End Month
    - End Day

    Args:
        obj: The Schedule:Year object.
        d: The date to find.
        year: Year for date comparison.
        doc: The IDF document.

    Returns:
        Tuple of (week_name, week_object). week_object may be None if not found.
    """
    # Parse all date ranges from the object
    i = 1
    while True:
        week_name_field = f"Schedule:Week Name {i}"
        start_month_field = f"Start Month {i}"
        start_day_field = f"Start Day {i}"
        end_month_field = f"End Month {i}"
        end_day_field = f"End Day {i}"

        week_name = obj.get(week_name_field)
        if week_name is None:
            break

        start_month = obj.get(start_month_field)
        start_day = obj.get(start_day_field)
        end_month = obj.get(end_month_field)
        end_day = obj.get(end_day_field)

        if any(v is None for v in [start_month, start_day, end_month, end_day]):
            i += 1
            continue

        start_m, start_d = _parse_month_day(str(start_month), str(start_day))
        end_m, end_d = _parse_month_day(str(end_month), str(end_day))

        start_date = date(year, start_m, start_d)
        end_date = date(year, end_m, end_d)

        # Handle year wraparound (e.g., Nov 1 - Feb 28)
        if end_date < start_date:
            # Check if date is in the end-of-year portion or start-of-year portion
            if d >= start_date or d <= end_date:
                week_obj = _find_week_schedule(doc, str(week_name))
                return str(week_name), week_obj
        else:
            if start_date <= d <= end_date:
                week_obj = _find_week_schedule(doc, str(week_name))
                return str(week_name), week_obj

        i += 1

    # No matching date range found
    return "", None


def _find_week_schedule(doc: IDFDocument, name: str) -> IDFObject | None:
    """Find a week schedule by name in the document.

    Args:
        doc: The IDF document.
        name: The schedule name to find.

    Returns:
        The week schedule object, or None if not found.
    """
    week_types = ["Schedule:Week:Daily", "Schedule:Week:Compact"]

    name_upper = name.upper()
    for sched_type in week_types:
        collection = doc[sched_type]
        for obj in collection:
            if obj.name and obj.name.upper() == name_upper:
                return obj

    return None
