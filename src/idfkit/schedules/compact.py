"""Schedule:Compact parser and evaluator.

Handles the Schedule:Compact DSL which defines schedules in a compact format
using Through:, For:, Until:, and Interpolate: keywords.
"""

from __future__ import annotations

import re
import weakref
from dataclasses import dataclass
from datetime import date, datetime, time
from typing import TYPE_CHECKING

from idfkit.schedules.day_types import get_applicable_day_types
from idfkit.schedules.time_utils import END_OF_DAY, evaluate_time_values
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
    CompactDayRule,
    CompactPeriod,
    DayType,
    Interpolation,
    TimeValue,
)

if TYPE_CHECKING:
    from idfkit.objects import IDFObject

# Regex patterns for parsing Schedule:Compact fields
_THROUGH_PATTERN = re.compile(r"^through:\s*(\d{1,2})[/\-](\d{1,2})$", re.IGNORECASE)
_FOR_PATTERN = re.compile(r"^for:\s*(.+)$", re.IGNORECASE)
_UNTIL_PATTERN = re.compile(r"^until:\s*(\d{1,2}):(\d{2})(?::(\d{2}))?$", re.IGNORECASE)
_INTERPOLATE_PATTERN = re.compile(r"^interpolate:\s*(yes|no|average|linear)$", re.IGNORECASE)
_VALUE_PATTERN = re.compile(r"^-?\d+\.?\d*$")

# Day type name mapping (case-insensitive)
_DAY_TYPE_MAP = {
    "sunday": DAY_TYPE_SUNDAY,
    "monday": DAY_TYPE_MONDAY,
    "tuesday": DAY_TYPE_TUESDAY,
    "wednesday": DAY_TYPE_WEDNESDAY,
    "thursday": DAY_TYPE_THURSDAY,
    "friday": DAY_TYPE_FRIDAY,
    "saturday": DAY_TYPE_SATURDAY,
    "weekdays": DAY_TYPE_WEEKDAYS,
    "weekends": DAY_TYPE_WEEKENDS,
    "alldays": DAY_TYPE_ALLDAYS,
    "holidays": DAY_TYPE_HOLIDAY,
    "holiday": DAY_TYPE_HOLIDAY,
    "summerdesignday": DAY_TYPE_SUMMER_DESIGN,
    "winterdesignday": DAY_TYPE_WINTER_DESIGN,
    "customday1": DAY_TYPE_CUSTOM_DAY_1,
    "customday2": DAY_TYPE_CUSTOM_DAY_2,
    "allotherdays": DAY_TYPE_ALL_OTHER_DAYS,
}

# Cache for parse_compact results, keyed by IDFObject identity.
# IDFObject.__hash__ uses id(self) so WeakKeyDictionary works correctly.
_parse_cache: weakref.WeakKeyDictionary[IDFObject, tuple[list[CompactPeriod], Interpolation]] = (
    weakref.WeakKeyDictionary()
)


@dataclass
class _ParseState:
    """Internal state for parsing Schedule:Compact."""

    periods: list[CompactPeriod]
    interpolation: Interpolation
    current_period: CompactPeriod | None
    current_rule: CompactDayRule | None
    field_index: int
    consecutive_none: int


def _process_through(state: _ParseState, match: re.Match[str]) -> None:
    """Process a Through: keyword."""
    # Save previous period if exists
    if state.current_period is not None:
        if state.current_rule is not None:
            state.current_period.day_rules.append(state.current_rule)
        state.periods.append(state.current_period)

    month = int(match.group(1))
    day = int(match.group(2))
    state.current_period = CompactPeriod(end_month=month, end_day=day, day_rules=[])
    state.current_rule = None


def _process_for(state: _ParseState, match: re.Match[str]) -> None:
    """Process a For: keyword."""
    # Save previous rule if exists
    if state.current_rule is not None and state.current_period is not None:
        state.current_period.day_rules.append(state.current_rule)

    day_types_str = match.group(1)
    day_types = _parse_day_types(day_types_str)
    state.current_rule = CompactDayRule(day_types=day_types, time_values=[])


def _process_until(state: _ParseState, match: re.Match[str], obj: IDFObject) -> None:
    """Process an Until: keyword."""
    hour = int(match.group(1))
    minute = int(match.group(2))
    second = int(match.group(3)) if match.group(3) else 0

    # Handle "24:00" as end of day
    until_time = END_OF_DAY if hour == 24 else time(hour, minute, second)

    # Next field should be the value
    state.field_index += 1
    value_field = _get_extensible_field(obj, state.field_index)
    if value_field is not None and state.current_rule is not None:
        schedule_value = float(value_field)
        state.current_rule.time_values.append(TimeValue(until_time=until_time, value=schedule_value))


def _process_field(state: _ParseState, value_str: str, obj: IDFObject) -> None:
    """Process a single field value in Schedule:Compact."""
    if match := _THROUGH_PATTERN.match(value_str):
        _process_through(state, match)
    elif match := _FOR_PATTERN.match(value_str):
        _process_for(state, match)
    elif match := _UNTIL_PATTERN.match(value_str):
        _process_until(state, match, obj)
    elif (match := _INTERPOLATE_PATTERN.match(value_str)) and match.group(1).lower() in ("yes", "average", "linear"):
        state.interpolation = Interpolation.AVERAGE


def _finalize_parse_state(state: _ParseState) -> None:
    """Save the final period and rule from parse state."""
    if state.current_period is not None:
        if state.current_rule is not None:
            state.current_period.day_rules.append(state.current_rule)
        state.periods.append(state.current_period)


def parse_compact(obj: IDFObject) -> tuple[list[CompactPeriod], Interpolation]:
    """Parse a Schedule:Compact object into structured data.

    Results are cached per object identity (the cache uses a WeakKeyDictionary
    so entries are automatically cleaned up when the object is garbage-collected).

    Args:
        obj: The Schedule:Compact object.

    Returns:
        Tuple of (list of CompactPeriod, interpolation mode).

    Raises:
        ValueError: If the schedule syntax is invalid.
    """
    cached = _parse_cache.get(obj)
    if cached is not None:
        return cached

    state = _ParseState(
        periods=[],
        interpolation=Interpolation.NO,
        current_period=None,
        current_rule=None,
        field_index=0,
        consecutive_none=0,
    )
    max_fields = 500

    while state.field_index < max_fields:
        try:
            value = _get_extensible_field(obj, state.field_index)
        except (IndexError, KeyError):
            break

        if value is None:
            state.consecutive_none += 1
            if state.consecutive_none >= 3:
                break
            state.field_index += 1
            continue

        state.consecutive_none = 0
        value_str = str(value).strip()
        if value_str:
            _process_field(state, value_str, obj)
        state.field_index += 1

    _finalize_parse_state(state)
    result = state.periods, state.interpolation
    _parse_cache[obj] = result
    return result


def _get_extensible_field(obj: IDFObject, index: int) -> str | None:
    """Get an extensible field by index from Schedule:Compact.

    Schedule:Compact has fields:
    - Name (field 0)
    - Schedule Type Limits Name (field 1)
    - Field 1, Field 2, ... (extensible, starting at index 2)

    Args:
        obj: The Schedule:Compact object.
        index: The extensible field index (0-based from first extensible field).

    Returns:
        The field value as a string, or None.
    """
    # Field names in Schedule:Compact are "Field 1", "Field 2", etc.
    field_name = f"Field {index + 1}"
    value = obj.get(field_name)
    return str(value) if value is not None else None


def _parse_day_types(day_types_str: str) -> set[str]:
    """Parse a day types string from the For: field.

    Can contain multiple day types separated by spaces or commas.

    Args:
        day_types_str: The day types string.

    Returns:
        Set of normalized day type strings.
    """
    day_types: set[str] = set()

    # Split by whitespace and commas
    parts = re.split(r"[\s,]+", day_types_str)

    for part in parts:
        part = part.strip().lower()
        if part in _DAY_TYPE_MAP:
            day_types.add(_DAY_TYPE_MAP[part])

    return day_types


def evaluate_compact(
    obj: IDFObject,
    dt: datetime,
    day_type: DayType = DayType.NORMAL,
    holidays: set[date] | None = None,
    custom_day_1: set[date] | None = None,
    custom_day_2: set[date] | None = None,
) -> float:
    """Evaluate a Schedule:Compact at a specific datetime.

    Args:
        obj: The Schedule:Compact object.
        dt: The datetime to evaluate.
        day_type: Override day type.
        holidays: Set of holiday dates.
        custom_day_1: Set of CustomDay1 dates.
        custom_day_2: Set of CustomDay2 dates.

    Returns:
        The schedule value.
    """
    periods, interpolation = parse_compact(obj)

    if not periods:
        return 0.0

    d = dt.date()
    current_time = dt.time()

    # Find the period containing this date
    period = _find_period_for_date(periods, d)
    if period is None:
        return 0.0

    # Get applicable day types for this date
    applicable_types = get_applicable_day_types(
        d, day_type, holidays or set(), custom_day_1 or set(), custom_day_2 or set()
    )

    # Find the matching day rule
    rule = _find_matching_rule(period.day_rules, applicable_types)
    if rule is None:
        return 0.0

    # Evaluate the time-value pairs
    return evaluate_time_values(rule.time_values, current_time, interpolation)


def _find_period_for_date(periods: list[CompactPeriod], d: date) -> CompactPeriod | None:
    """Find the period containing a date.

    Periods are sequential and cover the entire year. Each period's end date
    is its boundary, and the next period starts the following day.

    Args:
        periods: List of periods in order.
        d: The date to find.

    Returns:
        The period containing the date, or None.
    """
    for period in periods:
        if (d.month, d.day) <= (period.end_month, period.end_day):
            return period

    # If date is past all periods, use the last period (wrap around to next year)
    return periods[-1] if periods else None


def _find_matching_rule(rules: list[CompactDayRule], applicable_types: set[str]) -> CompactDayRule | None:
    """Find the first rule that matches the applicable day types.

    Rules are checked in order. The first rule with a matching day type wins.
    More specific day types (like individual weekdays) should be listed before
    more general ones (like AllDays).

    Args:
        rules: List of day rules.
        applicable_types: Set of applicable day type strings.

    Returns:
        The first matching rule, or None.
    """
    from idfkit.schedules.day_types import DAY_TYPE_PRIORITY

    # For each priority level, check if any rule matches
    for priority_type in DAY_TYPE_PRIORITY:
        if priority_type not in applicable_types:
            continue

        for rule in rules:
            if priority_type in rule.day_types:
                return rule

    # Fallback: check AllOtherDays
    for rule in rules:
        if DAY_TYPE_ALL_OTHER_DAYS in rule.day_types:
            return rule

    return None
