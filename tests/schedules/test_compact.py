"""Tests for schedules.compact module."""

from __future__ import annotations

from datetime import date, datetime

import pytest

from idfkit import new_document
from idfkit.objects import IDFObject
from idfkit.schedules.compact import (
    _find_matching_rule,
    _find_period_for_date,
    _parse_cache,
    _parse_day_types,
    evaluate_compact,
    parse_compact,
)
from idfkit.schedules.day_types import get_applicable_day_types
from idfkit.schedules.types import (
    DAY_TYPE_ALLDAYS,
    DAY_TYPE_HOLIDAY,
    DAY_TYPE_MONDAY,
    DAY_TYPE_SUMMER_DESIGN,
    DAY_TYPE_WEEKDAYS,
    DAY_TYPE_WEEKENDS,
    CompactDayRule,
    CompactPeriod,
    DayType,
    Interpolation,
)


def _make_compact(*fields: str, name: str = "Test") -> IDFObject:
    """Create a real Schedule:Compact object from field values."""
    doc = new_document()
    kwargs = {f"field_{i + 1}": v for i, v in enumerate(fields)}
    doc.add("Schedule:Compact", name, validate=False, **kwargs)
    return doc.get_collection("Schedule:Compact").get(name)


class TestParseDayTypes:
    """Tests for _parse_day_types function."""

    def test_single_type(self) -> None:
        """Test parsing single day type."""
        result = _parse_day_types("Weekdays")
        assert result == {"Weekdays"}

    def test_multiple_types(self) -> None:
        """Test parsing multiple day types."""
        result = _parse_day_types("Weekdays Weekends")
        assert result == {"Weekdays", "Weekends"}

    def test_with_commas(self) -> None:
        """Test parsing with comma separators."""
        result = _parse_day_types("Weekdays, Weekends")
        assert result == {"Weekdays", "Weekends"}

    def test_case_insensitive(self) -> None:
        """Test case insensitivity."""
        result = _parse_day_types("WEEKDAYS weekends")
        assert result == {"Weekdays", "Weekends"}

    def test_holidays(self) -> None:
        """Test parsing holidays."""
        result = _parse_day_types("Holidays")
        assert result == {"Holiday"}


class TestParseCompact:
    """Tests for parse_compact function."""

    @pytest.fixture
    def simple_compact_schedule(self) -> IDFObject:
        """Create a simple compact schedule."""
        return _make_compact(
            "Through: 12/31",
            "For: AllDays",
            "Until: 08:00",
            "0.0",
            "Until: 18:00",
            "1.0",
            "Until: 24:00",
            "0.0",
        )

    def test_simple_parse(self, simple_compact_schedule: IDFObject) -> None:
        """Test parsing simple compact schedule."""
        periods, interp = parse_compact(simple_compact_schedule)

        assert len(periods) == 1
        assert periods[0].end_month == 12
        assert periods[0].end_day == 31
        assert len(periods[0].day_rules) == 1
        assert DAY_TYPE_ALLDAYS in periods[0].day_rules[0].day_types
        assert len(periods[0].day_rules[0].time_values) == 3
        assert interp == Interpolation.NO

    @pytest.fixture
    def weekday_weekend_schedule(self) -> IDFObject:
        """Create a schedule with different weekday/weekend patterns."""
        return _make_compact(
            "Through: 12/31",
            "For: Weekdays",
            "Until: 08:00",
            "0.0",
            "Until: 18:00",
            "1.0",
            "Until: 24:00",
            "0.0",
            "For: Weekends Holidays",
            "Until: 24:00",
            "0.0",
        )

    def test_weekday_weekend_parse(self, weekday_weekend_schedule: IDFObject) -> None:
        """Test parsing schedule with weekday/weekend rules."""
        periods, _ = parse_compact(weekday_weekend_schedule)

        assert len(periods) == 1
        assert len(periods[0].day_rules) == 2

        weekday_rule = periods[0].day_rules[0]
        assert DAY_TYPE_WEEKDAYS in weekday_rule.day_types
        assert len(weekday_rule.time_values) == 3

        weekend_rule = periods[0].day_rules[1]
        assert DAY_TYPE_WEEKENDS in weekend_rule.day_types
        assert DAY_TYPE_HOLIDAY in weekend_rule.day_types


class TestFindPeriodForDate:
    """Tests for _find_period_for_date function."""

    def test_single_period(self) -> None:
        """Test finding period in single-period schedule."""
        periods = [CompactPeriod(end_month=12, end_day=31, day_rules=[])]

        assert _find_period_for_date(periods, date(2024, 1, 1)) == periods[0]
        assert _find_period_for_date(periods, date(2024, 6, 15)) == periods[0]
        assert _find_period_for_date(periods, date(2024, 12, 31)) == periods[0]

    def test_two_periods(self) -> None:
        """Test finding period in multi-period schedule."""
        periods = [
            CompactPeriod(end_month=6, end_day=30, day_rules=[]),
            CompactPeriod(end_month=12, end_day=31, day_rules=[]),
        ]

        assert _find_period_for_date(periods, date(2024, 3, 15)) == periods[0]
        assert _find_period_for_date(periods, date(2024, 6, 30)) == periods[0]
        assert _find_period_for_date(periods, date(2024, 7, 1)) == periods[1]
        assert _find_period_for_date(periods, date(2024, 12, 31)) == periods[1]

    def test_empty_returns_none(self) -> None:
        """Test empty periods list."""
        assert _find_period_for_date([], date(2024, 1, 1)) is None


class TestFindMatchingRule:
    """Tests for _find_matching_rule function."""

    def test_weekday_match(self) -> None:
        """Test matching weekday rule."""
        rules = [
            CompactDayRule(day_types={DAY_TYPE_WEEKDAYS}, time_values=[]),
            CompactDayRule(day_types={DAY_TYPE_WEEKENDS}, time_values=[]),
        ]

        day_types = get_applicable_day_types(
            date(2024, 1, 8),  # Monday
            DayType.NORMAL,
            holidays=set(),
            custom_day_1=set(),
            custom_day_2=set(),
        )
        result = _find_matching_rule(rules, day_types)
        assert result == rules[0]

    def test_weekend_match(self) -> None:
        """Test matching weekend rule."""
        rules = [
            CompactDayRule(day_types={DAY_TYPE_WEEKDAYS}, time_values=[]),
            CompactDayRule(day_types={DAY_TYPE_WEEKENDS}, time_values=[]),
        ]

        day_types = get_applicable_day_types(
            date(2024, 1, 6),  # Saturday
            DayType.NORMAL,
            holidays=set(),
            custom_day_1=set(),
            custom_day_2=set(),
        )
        result = _find_matching_rule(rules, day_types)
        assert result == rules[1]

    def test_alldays_match(self) -> None:
        """Test AllDays matches any day."""
        rules = [CompactDayRule(day_types={DAY_TYPE_ALLDAYS}, time_values=[])]

        day_types = get_applicable_day_types(
            date(2024, 1, 8),  # Monday
            DayType.NORMAL,
            holidays=set(),
            custom_day_1=set(),
            custom_day_2=set(),
        )
        result = _find_matching_rule(rules, day_types)
        assert result == rules[0]

    def test_holiday_match(self) -> None:
        """Test holiday matching."""
        rules = [
            CompactDayRule(day_types={DAY_TYPE_WEEKDAYS}, time_values=[]),
            CompactDayRule(day_types={DAY_TYPE_HOLIDAY}, time_values=[]),
        ]

        day_types = get_applicable_day_types(
            date(2024, 12, 25),  # Wednesday but holiday
            DayType.NORMAL,
            holidays={date(2024, 12, 25)},
            custom_day_1=set(),
            custom_day_2=set(),
        )
        result = _find_matching_rule(rules, day_types)
        assert result == rules[1]

    def test_specific_day_match(self) -> None:
        """Test matching specific day type (Monday)."""
        rules = [
            CompactDayRule(day_types={DAY_TYPE_MONDAY}, time_values=[]),
            CompactDayRule(day_types={DAY_TYPE_WEEKDAYS}, time_values=[]),
        ]

        day_types = get_applicable_day_types(
            date(2024, 1, 8),  # Monday
            DayType.NORMAL,
            holidays=set(),
            custom_day_1=set(),
            custom_day_2=set(),
        )
        result = _find_matching_rule(rules, day_types)
        assert result == rules[0]

    def test_no_match(self) -> None:
        """Test no matching rule returns None."""
        rules = [CompactDayRule(day_types={DAY_TYPE_SUMMER_DESIGN}, time_values=[])]

        day_types = get_applicable_day_types(
            date(2024, 1, 8),  # Monday
            DayType.NORMAL,
            holidays=set(),
            custom_day_1=set(),
            custom_day_2=set(),
        )
        result = _find_matching_rule(rules, day_types)
        assert result is None


class TestEvaluateCompact:
    """Tests for evaluate_compact function."""

    @pytest.fixture
    def office_schedule(self) -> IDFObject:
        """Create an office occupancy schedule."""
        return _make_compact(
            "Through: 12/31",
            "For: Weekdays",
            "Until: 08:00",
            "0.0",
            "Until: 18:00",
            "1.0",
            "Until: 24:00",
            "0.0",
            "For: Weekends Holidays",
            "Until: 24:00",
            "0.0",
        )

    def test_weekday_occupied(self, office_schedule: IDFObject) -> None:
        """Test weekday during occupied hours."""
        # Monday at 10am
        result = evaluate_compact(office_schedule, datetime(2024, 1, 8, 10, 0))
        assert result == 1.0

    def test_weekday_unoccupied_morning(self, office_schedule: IDFObject) -> None:
        """Test weekday before occupied hours."""
        # Monday at 6am
        result = evaluate_compact(office_schedule, datetime(2024, 1, 8, 6, 0))
        assert result == 0.0

    def test_weekday_unoccupied_evening(self, office_schedule: IDFObject) -> None:
        """Test weekday after occupied hours."""
        # Monday at 8pm
        result = evaluate_compact(office_schedule, datetime(2024, 1, 8, 20, 0))
        assert result == 0.0

    def test_weekend(self, office_schedule: IDFObject) -> None:
        """Test weekend (always unoccupied)."""
        # Saturday at 10am
        result = evaluate_compact(office_schedule, datetime(2024, 1, 6, 10, 0))
        assert result == 0.0

    def test_holiday(self, office_schedule: IDFObject) -> None:
        """Test holiday (uses weekend schedule)."""
        # Wednesday (would be weekday), but marked as holiday
        result = evaluate_compact(
            office_schedule,
            datetime(2024, 12, 25, 10, 0),  # Christmas
            holidays={date(2024, 12, 25)},
        )
        assert result == 0.0

    def test_summer_design_day(self, office_schedule: IDFObject) -> None:
        """Test summer design day override."""
        # No SummerDesignDay rule in this schedule, so should return 0
        result = evaluate_compact(
            office_schedule,
            datetime(2024, 7, 15, 10, 0),
            day_type=DayType.SUMMER_DESIGN,
        )
        assert result == 0.0


class TestParseCompactCaching:
    """Tests for parse_compact caching."""

    def test_second_call_uses_cache(self) -> None:
        """Test that calling parse_compact twice returns cached result."""
        obj = _make_compact(
            "Through: 12/31",
            "For: AllDays",
            "Until: 24:00",
            "1.0",
        )

        _parse_cache.clear()

        result1 = parse_compact(obj)
        result2 = parse_compact(obj)
        assert result1 is result2

        _parse_cache.clear()


class TestBoundaryTimes:
    """Tests for boundary time evaluation."""

    @pytest.fixture
    def boundary_schedule(self) -> IDFObject:
        """Create a schedule with boundary values at 00:00, 08:00, and 24:00."""
        return _make_compact(
            "Through: 12/31",
            "For: AllDays",
            "Until: 08:00",
            "0.0",
            "Until: 18:00",
            "1.0",
            "Until: 24:00",
            "0.5",
        )

    def test_at_midnight(self, boundary_schedule: IDFObject) -> None:
        """Test value at exactly midnight."""
        result = evaluate_compact(boundary_schedule, datetime(2024, 1, 1, 0, 0))
        assert result == 0.0

    def test_at_exact_0800(self, boundary_schedule: IDFObject) -> None:
        """Test value at exactly 08:00 (boundary between 0.0 and 1.0)."""
        result = evaluate_compact(boundary_schedule, datetime(2024, 1, 1, 8, 0))
        assert result == 1.0

    def test_at_2359(self, boundary_schedule: IDFObject) -> None:
        """Test value at 23:59."""
        result = evaluate_compact(boundary_schedule, datetime(2024, 1, 1, 23, 59))
        assert result == 0.5
