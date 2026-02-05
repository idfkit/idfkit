"""Holiday and special day extraction from IDF documents.

Parses RunPeriodControl:SpecialDays objects to determine which dates
are holidays, custom days, or other special day types.
"""

from __future__ import annotations

import calendar
import re
import warnings
from datetime import date, timedelta
from typing import TYPE_CHECKING

from idfkit.schedules.types import SpecialDay

if TYPE_CHECKING:
    from idfkit.document import IDFDocument

# Month name to number mapping (case-insensitive)
_MONTH_NAMES = {
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
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}

# Ordinal patterns for "nth weekday" specifications
_ORDINAL_PATTERN = re.compile(r"(\d+)(st|nd|rd|th)", re.IGNORECASE)

# Weekday name to number (Monday=0)
_WEEKDAY_NAMES = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
    "mon": 0,
    "tue": 1,
    "wed": 2,
    "thu": 3,
    "fri": 4,
    "sat": 5,
    "sun": 6,
}


def _parse_date_spec(spec: str, year: int) -> date:
    """Parse an EnergyPlus date specification.

    Supported formats:
    - "January 1" or "1 January" - specific date
    - "1/1" or "1-1" - month/day numeric
    - "3rd Monday in January" - nth weekday in month
    - "Last Monday in May" - last weekday in month

    Args:
        spec: Date specification string.
        year: Year to use for the date.

    Returns:
        The parsed date.

    Raises:
        ValueError: If the date specification cannot be parsed.
    """
    spec = spec.strip()

    # Try numeric format: "1/1" or "1-1" (month/day)
    numeric_match = re.match(r"^(\d{1,2})[/-](\d{1,2})$", spec)
    if numeric_match:
        month = int(numeric_match.group(1))
        day = int(numeric_match.group(2))
        return date(year, month, day)

    # Try "Month Day" or "Day Month" format
    parts = spec.split()
    if len(parts) >= 2:
        # Check for "January 1" format
        month_name = parts[0].lower()
        if month_name in _MONTH_NAMES:
            day = int(re.sub(r"\D", "", parts[1]))  # Remove non-digits
            return date(year, _MONTH_NAMES[month_name], day)

        # Check for "1 January" format
        if parts[0].isdigit():
            day = int(parts[0])
            month_name = parts[1].lower()
            if month_name in _MONTH_NAMES:
                return date(year, _MONTH_NAMES[month_name], day)

    # Try "nth weekday in Month" format
    nth_match = re.match(
        r"^(\d+)(?:st|nd|rd|th)?\s+(\w+)\s+in\s+(\w+)$",
        spec,
        re.IGNORECASE,
    )
    if nth_match:
        n = int(nth_match.group(1))
        weekday_name = nth_match.group(2).lower()
        month_name = nth_match.group(3).lower()

        if weekday_name in _WEEKDAY_NAMES and month_name in _MONTH_NAMES:
            weekday = _WEEKDAY_NAMES[weekday_name]
            month = _MONTH_NAMES[month_name]
            return _nth_weekday_of_month(year, month, weekday, n)

    # Try "Last weekday in Month" format
    last_match = re.match(
        r"^last\s+(\w+)\s+in\s+(\w+)$",
        spec,
        re.IGNORECASE,
    )
    if last_match:
        weekday_name = last_match.group(1).lower()
        month_name = last_match.group(2).lower()

        if weekday_name in _WEEKDAY_NAMES and month_name in _MONTH_NAMES:
            weekday = _WEEKDAY_NAMES[weekday_name]
            month = _MONTH_NAMES[month_name]
            return _last_weekday_of_month(year, month, weekday)

    msg = f"Cannot parse date specification: {spec!r}"
    raise ValueError(msg)


def _nth_weekday_of_month(year: int, month: int, weekday: int, n: int) -> date:
    """Get the nth occurrence of a weekday in a month.

    Args:
        year: Year.
        month: Month (1-12).
        weekday: Weekday (Monday=0, Sunday=6).
        n: Which occurrence (1=first, 2=second, etc.).

    Returns:
        The date of the nth occurrence.

    Raises:
        ValueError: If there is no nth occurrence in the month.
    """
    # Find first occurrence of the weekday
    first_day = date(year, month, 1)
    days_until_weekday = (weekday - first_day.weekday()) % 7
    first_occurrence = first_day + timedelta(days=days_until_weekday)

    # Add weeks to get nth occurrence
    result = first_occurrence + timedelta(weeks=n - 1)

    if result.month != month:
        msg = f"No {n}th occurrence of weekday {weekday} in {year}-{month:02d}"
        raise ValueError(msg)

    return result


def _last_weekday_of_month(year: int, month: int, weekday: int) -> date:
    """Get the last occurrence of a weekday in a month.

    Args:
        year: Year.
        month: Month (1-12).
        weekday: Weekday (Monday=0, Sunday=6).

    Returns:
        The date of the last occurrence.
    """
    # Get the last day of the month
    last_day = date(year, month, calendar.monthrange(year, month)[1])

    # Find the last occurrence of the weekday
    days_back = (last_day.weekday() - weekday) % 7
    return last_day - timedelta(days=days_back)


def extract_special_days(doc: IDFDocument, year: int) -> list[SpecialDay]:
    """Parse all RunPeriodControl:SpecialDays objects from a document.

    Args:
        doc: The IDF document to extract special days from.
        year: Year to use for date calculations.

    Returns:
        List of SpecialDay objects representing all special days.
    """
    special_days: list[SpecialDay] = []

    # Get the collection - returns empty collection if type doesn't exist
    collection = doc["RunPeriodControl:SpecialDays"]
    if len(collection) == 0:
        return special_days

    for obj in collection:
        name = obj.name or ""

        # Get start date specification
        start_spec = obj.get("Start Date")
        if not start_spec:
            continue

        try:
            start_date = _parse_date_spec(str(start_spec), year)
        except ValueError:
            warnings.warn(
                f"Skipping RunPeriodControl:SpecialDays {name!r}: cannot parse date {str(start_spec)!r}",
                stacklevel=2,
            )
            continue

        # Get duration (default is 1 day)
        duration_field = obj.get("Duration")
        duration = int(duration_field) if duration_field else 1

        # Get day type (default is Holiday)
        day_type = obj.get("Special Day Type")
        if not day_type:
            day_type = "Holiday"

        special_days.append(
            SpecialDay(
                name=name,
                start_date=start_date,
                duration=duration,
                day_type=str(day_type),
            )
        )

    return special_days


def get_holidays(doc: IDFDocument, year: int) -> set[date]:
    """Get all dates marked as Holiday for a given year.

    Args:
        doc: The IDF document.
        year: Year to get holidays for.

    Returns:
        Set of dates that are holidays.
    """
    holidays: set[date] = set()
    special_days = extract_special_days(doc, year)

    for sd in special_days:
        if sd.day_type == "Holiday":
            for i in range(sd.duration):
                holidays.add(sd.start_date + timedelta(days=i))

    return holidays


def get_special_days_by_type(doc: IDFDocument, year: int, day_type: str) -> set[date]:
    """Get all dates of a specific day type.

    Args:
        doc: The IDF document.
        year: Year to get dates for.
        day_type: The day type to filter by ("Holiday", "CustomDay1", "CustomDay2").

    Returns:
        Set of dates matching the day type.
    """
    dates: set[date] = set()
    special_days = extract_special_days(doc, year)

    for sd in special_days:
        if sd.day_type == day_type:
            for i in range(sd.duration):
                dates.add(sd.start_date + timedelta(days=i))

    return dates
