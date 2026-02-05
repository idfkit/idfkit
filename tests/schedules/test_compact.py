"""Tests for schedules.compact module."""

from __future__ import annotations

from datetime import date, datetime
from unittest.mock import MagicMock

import pytest

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
    def simple_compact_schedule(self) -> MagicMock:
        """Create a simple compact schedule mock."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Compact"

        # Fields: Through: 12/31, For: AllDays, Until: 08:00, 0.0, Until: 18:00, 1.0, Until: 24:00, 0.0
        fields = {
            "Field 1": "Through: 12/31",
            "Field 2": "For: AllDays",
            "Field 3": "Until: 08:00",
            "Field 4": "0.0",
            "Field 5": "Until: 18:00",
            "Field 6": "1.0",
            "Field 7": "Until: 24:00",
            "Field 8": "0.0",
        }

        def get_field(name: str) -> str | None:
            return fields.get(name)

        obj.get.side_effect = get_field
        return obj

    def test_simple_parse(self, simple_compact_schedule: MagicMock) -> None:
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
    def weekday_weekend_schedule(self) -> MagicMock:
        """Create a schedule with different weekday/weekend patterns."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Compact"

        fields = {
            "Field 1": "Through: 12/31",
            "Field 2": "For: Weekdays",
            "Field 3": "Until: 08:00",
            "Field 4": "0.0",
            "Field 5": "Until: 18:00",
            "Field 6": "1.0",
            "Field 7": "Until: 24:00",
            "Field 8": "0.0",
            "Field 9": "For: Weekends Holidays",
            "Field 10": "Until: 24:00",
            "Field 11": "0.0",
        }

        def get_field(name: str) -> str | None:
            return fields.get(name)

        obj.get.side_effect = get_field
        return obj

    def test_weekday_weekend_parse(self, weekday_weekend_schedule: MagicMock) -> None:
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

    def test_multiple_periods(self) -> None:
        """Test finding period in multi-period schedule."""
        periods = [
            CompactPeriod(end_month=6, end_day=30, day_rules=[]),
            CompactPeriod(end_month=12, end_day=31, day_rules=[]),
        ]

        assert _find_period_for_date(periods, date(2024, 3, 15)) == periods[0]
        assert _find_period_for_date(periods, date(2024, 6, 30)) == periods[0]
        assert _find_period_for_date(periods, date(2024, 7, 1)) == periods[1]
        assert _find_period_for_date(periods, date(2024, 12, 31)) == periods[1]


class TestGetApplicableDayTypes:
    """Tests for _get_applicable_day_types function."""

    def test_weekday(self) -> None:
        """Test applicable types for a weekday."""
        types = get_applicable_day_types(
            date(2024, 1, 8),  # Monday
            DayType.NORMAL,
            set(),
            set(),
            set(),
        )

        assert DAY_TYPE_MONDAY in types
        assert DAY_TYPE_WEEKDAYS in types
        assert DAY_TYPE_ALLDAYS in types
        assert DAY_TYPE_WEEKENDS not in types

    def test_weekend(self) -> None:
        """Test applicable types for a weekend day."""
        types = get_applicable_day_types(
            date(2024, 1, 6),  # Saturday
            DayType.NORMAL,
            set(),
            set(),
            set(),
        )

        assert "Saturday" in types
        assert DAY_TYPE_WEEKENDS in types
        assert DAY_TYPE_ALLDAYS in types
        assert DAY_TYPE_WEEKDAYS not in types

    def test_holiday(self) -> None:
        """Test applicable types for a holiday."""
        types = get_applicable_day_types(
            date(2024, 12, 25),
            DayType.NORMAL,
            {date(2024, 12, 25)},  # Christmas
            set(),
            set(),
        )

        assert DAY_TYPE_HOLIDAY in types
        assert DAY_TYPE_ALLDAYS in types

    def test_design_day_override(self) -> None:
        """Test design day override."""
        types = get_applicable_day_types(
            date(2024, 7, 15),
            DayType.SUMMER_DESIGN,
            set(),
            set(),
            set(),
        )

        assert DAY_TYPE_SUMMER_DESIGN in types
        assert DAY_TYPE_ALLDAYS in types
        # Should not include normal weekday types when overridden
        assert DAY_TYPE_WEEKDAYS not in types


class TestFindMatchingRule:
    """Tests for _find_matching_rule function."""

    def test_exact_match(self) -> None:
        """Test exact day type match."""
        rules = [
            CompactDayRule(day_types={DAY_TYPE_WEEKDAYS}, time_values=[]),
            CompactDayRule(day_types={DAY_TYPE_WEEKENDS}, time_values=[]),
        ]

        applicable = {DAY_TYPE_MONDAY, DAY_TYPE_WEEKDAYS, DAY_TYPE_ALLDAYS}
        result = _find_matching_rule(rules, applicable)

        assert result == rules[0]

    def test_priority_order(self) -> None:
        """Test priority ordering (specific before general)."""
        rules = [
            CompactDayRule(day_types={DAY_TYPE_ALLDAYS}, time_values=[]),
            CompactDayRule(day_types={DAY_TYPE_HOLIDAY}, time_values=[]),
        ]

        # Holiday should match before AllDays
        applicable = {DAY_TYPE_HOLIDAY, DAY_TYPE_ALLDAYS}
        result = _find_matching_rule(rules, applicable)

        assert result == rules[1]


class TestEvaluateCompact:
    """Tests for evaluate_compact function."""

    @pytest.fixture
    def office_schedule(self) -> MagicMock:
        """Create an office occupancy schedule."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Compact"

        fields = {
            "Field 1": "Through: 12/31",
            "Field 2": "For: Weekdays",
            "Field 3": "Until: 08:00",
            "Field 4": "0.0",
            "Field 5": "Until: 18:00",
            "Field 6": "1.0",
            "Field 7": "Until: 24:00",
            "Field 8": "0.0",
            "Field 9": "For: Weekends Holidays",
            "Field 10": "Until: 24:00",
            "Field 11": "0.0",
        }

        def get_field(name: str) -> str | None:
            return fields.get(name)

        obj.get.side_effect = get_field
        return obj

    def test_weekday_occupied(self, office_schedule: MagicMock) -> None:
        """Test weekday during occupied hours."""
        # Monday at 10am
        result = evaluate_compact(office_schedule, datetime(2024, 1, 8, 10, 0))
        assert result == 1.0

    def test_weekday_unoccupied_morning(self, office_schedule: MagicMock) -> None:
        """Test weekday before occupied hours."""
        # Monday at 6am
        result = evaluate_compact(office_schedule, datetime(2024, 1, 8, 6, 0))
        assert result == 0.0

    def test_weekday_unoccupied_evening(self, office_schedule: MagicMock) -> None:
        """Test weekday after occupied hours."""
        # Monday at 8pm
        result = evaluate_compact(office_schedule, datetime(2024, 1, 8, 20, 0))
        assert result == 0.0

    def test_weekend(self, office_schedule: MagicMock) -> None:
        """Test weekend (always unoccupied)."""
        # Saturday at 10am
        result = evaluate_compact(office_schedule, datetime(2024, 1, 6, 10, 0))
        assert result == 0.0

    def test_holiday(self, office_schedule: MagicMock) -> None:
        """Test holiday (uses weekend schedule)."""
        # Wednesday (would be weekday), but marked as holiday
        result = evaluate_compact(
            office_schedule,
            datetime(2024, 12, 25, 10, 0),  # Christmas
            holidays={date(2024, 12, 25)},
        )
        assert result == 0.0

    def test_summer_design_day(self, office_schedule: MagicMock) -> None:
        """Test summer design day override."""
        # Summer design day should use whatever rule matches SummerDesignDay
        # In this schedule, there's no explicit SummerDesignDay rule
        # so it should fall back to AllOtherDays behavior
        result = evaluate_compact(
            office_schedule,
            datetime(2024, 7, 15, 10, 0),
            day_type=DayType.SUMMER_DESIGN,
        )
        # No SummerDesignDay rule, so should return 0 (no matching rule)
        assert result == 0.0


class TestParseCompactCaching:
    """Tests for parse_compact caching."""

    def test_second_call_uses_cache(self) -> None:
        """Test that calling parse_compact twice returns cached result."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Compact"

        fields = {
            "Field 1": "Through: 12/31",
            "Field 2": "For: AllDays",
            "Field 3": "Until: 24:00",
            "Field 4": "1.0",
        }

        call_count = 0

        def get_field(name: str) -> str | None:
            nonlocal call_count
            call_count += 1
            return fields.get(name)

        obj.get.side_effect = get_field

        # Clear cache to ensure clean state
        _parse_cache.clear()

        # First call
        result1 = parse_compact(obj)
        calls_after_first = call_count

        # Second call should use cache — no additional get() calls
        result2 = parse_compact(obj)
        assert call_count == calls_after_first  # No new calls
        assert result1 is result2  # Same object (not just equal)

        # Clean up
        _parse_cache.clear()


class TestBoundaryTimes:
    """Tests for boundary time evaluation."""

    @pytest.fixture
    def boundary_schedule(self) -> MagicMock:
        """Create a schedule with boundary values at 00:00, 08:00, and 24:00."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Compact"

        fields = {
            "Field 1": "Through: 12/31",
            "Field 2": "For: AllDays",
            "Field 3": "Until: 08:00",
            "Field 4": "0.0",
            "Field 5": "Until: 18:00",
            "Field 6": "1.0",
            "Field 7": "Until: 24:00",
            "Field 8": "0.5",
        }

        def get_field(name: str) -> str | None:
            return fields.get(name)

        obj.get.side_effect = get_field
        return obj

    def test_at_midnight(self, boundary_schedule: MagicMock) -> None:
        """Test evaluation at 00:00."""
        _parse_cache.clear()
        result = evaluate_compact(boundary_schedule, datetime(2024, 1, 1, 0, 0))
        assert result == 0.0

    def test_at_exact_0800(self, boundary_schedule: MagicMock) -> None:
        """Test evaluation at exactly 08:00 transitions to next interval."""
        _parse_cache.clear()
        result = evaluate_compact(boundary_schedule, datetime(2024, 1, 1, 8, 0))
        assert result == 1.0

    def test_at_2359(self, boundary_schedule: MagicMock) -> None:
        """Test evaluation just before 24:00."""
        _parse_cache.clear()
        result = evaluate_compact(boundary_schedule, datetime(2024, 1, 1, 23, 59))
        assert result == 0.5
