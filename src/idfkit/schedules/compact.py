"""Schedule:Compact parser and evaluator.

Handles the Schedule:Compact DSL which defines schedules in a compact format
using Through:, For:, Until:, and Interpolate: keywords.
"""

from __future__ import annotations

import re
import weakref
from dataclasses import dataclass
from datetime import date, datetime, time
from typing import TYPE_CHECKING, Any, cast

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

__all__ = [
    "compact_problems",
    "evaluate_compact",
    "parse_compact",
]

# Regex patterns for parsing Schedule:Compact fields. EnergyPlus reads a keyword with or without its
# colon, and with space before it: ``Through 12/31``, ``Through : 12/31``, ``For AllDays`` and
# ``Until 24:00`` all appear in its example files. The keyword must be followed by a colon or a space.
_THROUGH_PATTERN = re.compile(r"^through(?:\s*:\s*|\s+)(\d{1,2})[/\-](\d{1,2})$", re.IGNORECASE)
_FOR_PATTERN = re.compile(r"^for(?:\s*:\s*|\s+)(.+)$", re.IGNORECASE)
_UNTIL_PATTERN = re.compile(r"^until(?:\s*:\s*|\s+)(\d{1,2}):(\d{2})(?::(\d{2}))?$", re.IGNORECASE)
_INTERPOLATE_PATTERN = re.compile(r"^interpolate(?:\s*:\s*|\s+)(yes|no|average|linear)$", re.IGNORECASE)
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
# Each entry stores (result_tuple, mutation_version) so that stale
# results are discarded when the object is mutated.
_ParseResult = tuple[list[CompactPeriod], Interpolation]
_parse_cache: weakref.WeakKeyDictionary[IDFObject, tuple[_ParseResult, int]] = weakref.WeakKeyDictionary()
# compact_problems results, cached the same way: evaluate_compact checks them on every call.
_problems_cache: weakref.WeakKeyDictionary[IDFObject, tuple[tuple[str, ...], int]] = weakref.WeakKeyDictionary()


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
    if state.current_rule is not None and state.current_period is not None:
        state.current_period.day_rules.append(state.current_rule)

    day_types_str = match.group(1)
    day_types = _parse_day_types(day_types_str)
    state.current_rule = CompactDayRule(day_types=day_types, time_values=[])


def _process_until(state: _ParseState, match: re.Match[str], ext_fields: list[str]) -> None:
    """Process an Until: keyword."""
    hour = int(match.group(1))
    minute = int(match.group(2))
    second = int(match.group(3)) if match.group(3) else 0

    until_time = END_OF_DAY if hour == 24 else time(hour, minute, second)

    # Next field should be the value
    state.field_index += 1
    if state.field_index < len(ext_fields) and state.current_rule is not None:
        value_str = ext_fields[state.field_index]
        if value_str:
            schedule_value = float(value_str)
            state.current_rule.time_values.append(TimeValue(until_time=until_time, value=schedule_value))


def _process_field(state: _ParseState, value_str: str, ext_fields: list[str]) -> None:
    """Process a single field value in Schedule:Compact."""
    if match := _THROUGH_PATTERN.match(value_str):
        _process_through(state, match)
    elif match := _FOR_PATTERN.match(value_str):
        _process_for(state, match)
    elif match := _UNTIL_PATTERN.match(value_str):
        _process_until(state, match, ext_fields)
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

    Uses ``field_order`` to read extensible fields in their stored sequence,
    avoiding any dependency on naming conventions (``field`` vs ``field_1``).

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
        result, version = cached
        if version == obj.mutation_version:
            return result

    # Schedule:Compact stores its DSL fields canonically: a list of
    # ``{"field": <token>}`` dicts under the ``data`` wrapper.
    ext_fields: list[str] = []
    items_raw: Any = obj.data.get("data") or []
    if not isinstance(items_raw, list):
        items_raw = []
    for item in cast("list[dict[str, Any]]", items_raw):
        raw = item.get("field")
        ext_fields.append(str(raw).strip() if raw is not None else "")

    state = _ParseState(
        periods=[],
        interpolation=Interpolation.NO,
        current_period=None,
        current_rule=None,
        field_index=0,
        consecutive_none=0,
    )

    while state.field_index < len(ext_fields):
        value_str = ext_fields[state.field_index]

        if not value_str:
            state.consecutive_none += 1
            if state.consecutive_none >= 3:
                break
            state.field_index += 1
            continue

        state.consecutive_none = 0
        _process_field(state, value_str, ext_fields)
        state.field_index += 1

    _finalize_parse_state(state)
    result: _ParseResult = (state.periods, state.interpolation)
    _parse_cache[obj] = (result, obj.mutation_version)
    return result


def compact_problems(obj: IDFObject) -> list[str]:
    """List the ways a Schedule:Compact fails to cover the year that EnergyPlus treats as fatal.

    EnergyPlus terminates on a schedule whose last ``Through:`` is not ``12/31`` ("has missing days
    in its schedule pointers") and on a ``For:`` block whose last ``Until:`` is not ``24:00``
    ("incomplete day detected"). An evaluator that quietly reused the last period or the last
    value for the uncovered time would show values for a model that cannot run.

    Day types a schedule leaves out (``For: Weekdays`` alone) are not listed: EnergyPlus only
    warns about them.

    Args:
        obj: The Schedule:Compact object.

    Returns:
        One message per problem, in field order; empty when the schedule covers the year.

    Examples:
        >>> from idfkit import new_document
        >>> doc = new_document()
        >>> heat = doc.add("Schedule:Compact", "Heat", data=[
        ...     {"field": "Through: 6/30"}, {"field": "For: AllDays"},
        ...     {"field": "Until: 12:00"}, {"field": "20"}])
        >>> for problem in compact_problems(heat):
        ...     print(problem)
        the last 'Through:' is 6/30, not 12/31, so the rest of the year has no values
        'Through: 6/30' block 1 ('For:' AllDays) ends at 'Until: 12:00', not 'Until: 24:00', so the rest of the day has no value
    """
    return list(_cached_problems(obj))


def _cached_problems(obj: IDFObject) -> tuple[str, ...]:
    """[compact_problems][idfkit.schedules.compact.compact_problems], cached until *obj* is mutated."""
    cached = _problems_cache.get(obj)
    if cached is not None and cached[1] == obj.mutation_version:
        return cached[0]
    problems = tuple(_find_compact_problems(obj))
    _problems_cache[obj] = (problems, obj.mutation_version)
    return problems


def _find_compact_problems(obj: IDFObject) -> list[str]:
    """Uncached body of [compact_problems][idfkit.schedules.compact.compact_problems]."""
    periods, _ = parse_compact(obj)
    if not periods:
        return ["it has no 'Through:' field, so no day of the year has values"]

    problems: list[str] = []
    # EnergyPlus reads a 'Through:' after the one that reaches 12/31 without complaint, so the year
    # is covered when any period reaches it, not only the last.
    if all((p.end_month, p.end_day) != (12, 31) for p in periods):
        last = periods[-1]
        problems.append(
            f"the last 'Through:' is {last.end_month}/{last.end_day}, not 12/31, so the rest of the year has no values"
        )
    for period in periods:
        through = f"'Through: {period.end_month}/{period.end_day}'"
        if not period.day_rules:
            problems.append(f"{through} has no 'For:' field, so its days have no values")
        for index, rule in enumerate(period.day_rules, start=1):
            days = " ".join(sorted(rule.day_types)) or "?"
            block = f"{through} block {index} ('For:' {days})"
            if not rule.time_values:
                problems.append(f"{block} has no 'Until:' value, so its days have no values")
                continue
            end = rule.time_values[-1].until_time
            if end != END_OF_DAY:
                problems.append(
                    f"{block} ends at 'Until: {end.hour:02d}:{end.minute:02d}', not 'Until: 24:00', "
                    "so the rest of the day has no value"
                )
    return problems


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

    Raises:
        ValueError: If the schedule does not cover the whole year through ``12/31`` or a day
            through ``24:00`` (see [compact_problems][idfkit.schedules.compact.compact_problems]),
            which EnergyPlus refuses as fatal. ``evaluate()`` raises it as
            ``MalformedScheduleError``.
    """
    periods, interpolation = parse_compact(obj)

    problems = _cached_problems(obj)
    if problems:
        msg = f"schedule {obj.name!r} would stop EnergyPlus: " + "; ".join(problems)
        raise ValueError(msg)

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
