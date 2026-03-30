"""Tests for schedules.compact module."""

from __future__ import annotations

from datetime import date, datetime
from unittest.mock import MagicMock, patch

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

    def test_unknown_day_type_ignored(self) -> None:
        """Unknown day type string is silently ignored."""
        result = _parse_day_types("Weekdays UnknownType")
        assert result == {"Weekdays"}
        assert "UnknownType" not in result


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


class TestMultiplePeriods:
    """Tests covering multi-period and edge-case compact schedule parsing."""

    def test_multi_period_flushes_previous(self) -> None:
        """Multiple Through: fields flush the previous period and rule."""
        obj = _make_compact(
            "Through: 6/30",
            "For: AllDays",
            "Until: 24:00",
            "0.3",
            "Through: 12/31",
            "For: AllDays",
            "Until: 24:00",
            "0.7",
        )
        periods, _ = parse_compact(obj)
        assert len(periods) == 2
        assert periods[0].end_month == 6
        assert periods[1].end_month == 12

    def test_consecutive_for_flush_rule(self) -> None:
        """Two For: blocks in the same period produce two separate day rules."""
        obj = _make_compact(
            "Through: 12/31",
            "For: Weekdays",
            "Until: 24:00",
            "1.0",
            "For: Weekends",
            "Until: 24:00",
            "0.0",
        )
        periods, _ = parse_compact(obj)
        assert len(periods[0].day_rules) == 2

    def test_interpolate_yes_sets_average(self) -> None:
        """'Interpolate: yes' sets interpolation to AVERAGE."""
        obj = _make_compact(
            "Through: 12/31",
            "Interpolate: Yes",
            "For: AllDays",
            "Until: 24:00",
            "1.0",
        )
        _, interp = parse_compact(obj)
        assert interp == Interpolation.AVERAGE

    def test_interpolate_linear_sets_average(self) -> None:
        """'Interpolate: linear' sets interpolation to AVERAGE."""
        obj = _make_compact(
            "Through: 12/31",
            "Interpolate: Linear",
            "For: AllDays",
            "Until: 24:00",
            "1.0",
        )
        _, interp = parse_compact(obj)
        assert interp == Interpolation.AVERAGE

    def test_interpolate_no_stays_no(self) -> None:
        """'Interpolate: no' keeps interpolation as NO."""
        obj = _make_compact(
            "Through: 12/31",
            "Interpolate: No",
            "For: AllDays",
            "Until: 24:00",
            "1.0",
        )
        _, interp = parse_compact(obj)
        assert interp == Interpolation.NO

    def test_until_with_seconds(self) -> None:
        """Until: with an HH:MM:SS value parses correctly."""
        obj = _make_compact(
            "Through: 12/31",
            "For: AllDays",
            "Until: 08:00:00",
            "0.5",
            "Until: 24:00",
            "1.0",
        )
        periods, _ = parse_compact(obj)
        assert len(periods[0].day_rules[0].time_values) == 2

    def test_consecutive_empty_fields_break(self) -> None:
        """Three consecutive empty extensible fields break parsing early."""
        # Build a compact with a valid block then trailing empty fields
        doc = new_document()
        doc.add(
            "Schedule:Compact",
            "SparseSched",
            validate=False,
            field_1="Through: 12/31",
            field_2="For: AllDays",
            field_3="Until: 24:00",
            field_4="0.5",
        )
        obj = doc.get_collection("Schedule:Compact").get("SparseSched")
        # The field_order will have entries beyond field_4 that are empty; parse
        # should break on 3 consecutive empty entries without error.
        periods, _ = parse_compact(obj)
        assert len(periods) == 1

    def test_stale_cache_refreshed_after_mutation(self) -> None:
        """Cache is discarded and reparsed when mutation_version changes."""
        # Use a MagicMock so we can control mutation_version
        obj = MagicMock()
        obj.mutation_version = 0
        obj.field_order = [
            "schedule_type_limits_name",
            "field_1",
            "field_2",
            "field_3",
            "field_4",
        ]
        data: dict[str, str] = {
            "field_1": "Through: 12/31",
            "field_2": "For: AllDays",
            "field_3": "Until: 24:00",
            "field_4": "1.0",
        }
        obj.data = data

        _parse_cache.clear()
        result1 = parse_compact(obj)

        # Bump mutation_version to trigger cache miss
        obj.mutation_version = 1
        result2 = parse_compact(obj)

        # Both results should be valid (cache was refreshed)
        assert len(result1[0]) == 1
        assert len(result2[0]) == 1
        _parse_cache.clear()

    def test_find_period_past_all_returns_last(self) -> None:
        """Date past all period end dates uses the last period as a fallback."""
        periods = [
            CompactPeriod(end_month=3, end_day=31, day_rules=[]),
            CompactPeriod(end_month=6, end_day=30, day_rules=[]),
        ]
        # date after 6/30 — falls through to last-period fallback
        result = _find_period_for_date(periods, date(2024, 7, 1))
        assert result == periods[-1]

    def test_evaluate_compact_no_periods_returns_zero(self) -> None:
        """evaluate_compact returns 0.0 when no periods exist."""
        # Schedule with no Through: fields — results in empty periods
        doc = new_document()
        doc.add("Schedule:Compact", "Empty", validate=False)
        obj = doc.get_collection("Schedule:Compact").get("Empty")
        result = evaluate_compact(obj, datetime(2024, 1, 1, 12, 0))
        assert result == 0.0

    def test_evaluate_compact_period_is_none_returns_zero(self) -> None:
        """evaluate_compact returns 0.0 when no period is found for the given date."""
        from idfkit.schedules import compact as compact_module

        obj = _make_compact(
            "Through: 12/31",
            "For: AllDays",
            "Until: 24:00",
            "1.0",
        )

        with patch.object(compact_module, "_find_period_for_date", return_value=None):
            result = evaluate_compact(obj, datetime(2024, 1, 1, 12, 0))
        assert result == 0.0

    def test_all_other_days_fallback_in_find_matching(self) -> None:
        """AllOtherDays is returned when no higher-priority match exists."""
        from idfkit.schedules.types import DAY_TYPE_ALL_OTHER_DAYS

        rule = CompactDayRule(day_types={DAY_TYPE_ALL_OTHER_DAYS}, time_values=[])
        unmatched_types = {"CustomDay1"}  # Not in priority list for most schedules
        result = _find_matching_rule([rule], unmatched_types)
        assert result == rule

    def test_process_through_with_period_but_no_rule(self) -> None:
        """Second Through: with no preceding For: flushes an empty period."""
        # Schedule: Through:6/30 with nothing after it (no For:), then Through:12/31
        obj = _make_compact(
            "Through: 6/30",
            "Through: 12/31",
            "For: AllDays",
            "Until: 24:00",
            "1.0",
        )
        periods, _ = parse_compact(obj)
        # First period has no rules (Through:6/30 had nothing), second has 1 rule
        assert len(periods) == 2
        assert len(periods[0].day_rules) == 0

    def test_process_until_no_current_rule(self) -> None:
        """Until: appearing before any For: is skipped; subsequent rules are still parsed."""
        # Until: before any For: — current_rule is None
        obj = _make_compact(
            "Through: 12/31",
            "Until: 08:00",  # No For: before this
            "0.5",
            "For: AllDays",
            "Until: 24:00",
            "1.0",
        )
        periods, _ = parse_compact(obj)
        # The Until before For: is ignored; the AllDays rule should still be present
        assert len(periods[0].day_rules) == 1

    def test_process_until_empty_value_field(self) -> None:
        """Until: when the following value field is an empty string is skipped."""

        obj = MagicMock()
        obj.mutation_version = 0
        obj.field_order = [
            "schedule_type_limits_name",
            "field_1",
            "field_2",
            "field_3",
            "field_4",
        ]
        # Until: 08:00 followed by an empty value (not a float)
        obj.data = {
            "field_1": "Through: 12/31",
            "field_2": "For: AllDays",
            "field_3": "Until: 08:00",
            "field_4": "",  # Empty value — should be skipped
        }
        _parse_cache.clear()
        periods, _ = parse_compact(obj)
        # Rule exists but has no time values (empty value was skipped)
        assert len(periods[0].day_rules[0].time_values) == 0
        _parse_cache.clear()

    def test_finalize_with_rule_appended(self) -> None:
        """_finalize_parse_state appends current_rule to period."""
        # A normal schedule: final period has an active rule when parse ends
        obj = _make_compact(
            "Through: 12/31",
            "For: AllDays",
            "Until: 24:00",
            "1.0",
        )
        periods, _ = parse_compact(obj)
        assert len(periods[0].day_rules) == 1
        assert len(periods[0].day_rules[0].time_values) == 1

    def test_finalize_with_no_rule_appends_period_only(self) -> None:
        """_finalize_parse_state appends the period even when current_rule is None."""

        # Build a state where current_period is set but current_rule is None
        # This happens when the last Through: has no following For:
        obj = MagicMock()
        obj.mutation_version = 0
        obj.field_order = ["schedule_type_limits_name", "f1"]
        obj.data = {"f1": "Through: 12/31"}  # Only Through:, no For:
        _parse_cache.clear()
        periods, _ = parse_compact(obj)
        # Period should still be appended even though no rule
        assert len(periods) == 1
        assert len(periods[0].day_rules) == 0
        _parse_cache.clear()

    def test_consecutive_none_breaks_loop(self) -> None:
        """Three consecutive None fields break parsing early."""

        obj = MagicMock()
        obj.mutation_version = 0
        obj.field_order = [
            "schedule_type_limits_name",
            "f1",
            "f2",
            "f3",
            "f4",
            "empty1",
            "empty2",
            "empty3",  # Three consecutive empty fields
        ]
        obj.data = {
            "f1": "Through: 12/31",
            "f2": "For: AllDays",
            "f3": "Until: 24:00",
            "f4": "1.0",
            "empty1": None,
            "empty2": None,
            "empty3": None,
        }
        _parse_cache.clear()
        periods, _ = parse_compact(obj)
        assert len(periods) == 1
        _parse_cache.clear()
