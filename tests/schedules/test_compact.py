"""Tests for schedules.compact module."""

from __future__ import annotations

from datetime import date, datetime

import pytest

from idfkit import new_document
from idfkit.objects import IDFObject
from idfkit.schedules.compact import (  # pyright: ignore[reportPrivateUsage]
    _find_matching_rule,
    _find_period_for_date,
    _parse_cache,
    _parse_day_types,
    compact_problems,
    evaluate_compact,
    parse_compact,
)
from idfkit.schedules.day_types import get_applicable_day_types
from idfkit.schedules.evaluate import values
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
    data = [{"field": v} for v in fields]
    doc.add("Schedule:Compact", name, validate=False, data=data)
    return doc.get_collection("Schedule:Compact").get(name)


class TestParseDayTypes:
    """Tests for _parse_day_types function."""

    def test_single_type(self) -> None:
        """Test parsing single day type."""
        result = _parse_day_types("Weekdays")
        assert result == {"Weekdays"}

    def test_unrecognized_type_ignored(self) -> None:
        """Unrecognized day type part is silently ignored (line 232->230)."""
        result = _parse_day_types("Weekdays UnknownDayType")
        # UnknownDayType is not in _DAY_TYPE_MAP, only Weekdays should be in result
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


class TestMultiplePeriods:
    """Tests that exercise multi-period compact schedules (lines 95-97)."""

    def test_two_periods_appends_first(self) -> None:
        """A second Through: keyword finalizes and stores the first period."""
        sched = _make_compact(
            "Through: 06/30",
            "For: AllDays",
            "Until: 24:00",
            "0.5",
            "Through: 12/31",
            "For: AllDays",
            "Until: 24:00",
            "1.0",
        )
        periods, _ = parse_compact(sched)
        assert len(periods) == 2
        assert periods[0].end_month == 6
        assert periods[1].end_month == 12

    def test_two_periods_evaluates_correct_period(self) -> None:
        """Date in first period returns its value; date in second returns the other."""
        sched = _make_compact(
            "Through: 06/30",
            "For: AllDays",
            "Until: 24:00",
            "0.25",
            "Through: 12/31",
            "For: AllDays",
            "Until: 24:00",
            "0.75",
        )
        assert evaluate_compact(sched, datetime(2024, 3, 1, 12, 0)) == 0.25
        assert evaluate_compact(sched, datetime(2024, 9, 1, 12, 0)) == 0.75

    def test_two_through_no_for_in_first(self) -> None:
        """Second Through: with no rule in first period (current_rule=None branch, line 95->97)."""
        # Two Through: keywords with no For: in the first period
        # This exercises the branch where current_period is not None but current_rule IS None
        sched = _make_compact(
            "Through: 06/30",
            # No For:/Until: for first period
            "Through: 12/31",
            "For: AllDays",
            "Until: 24:00",
            "1.0",
        )
        periods, _ = parse_compact(sched)
        # First period has no rules (empty), second has the AllDays rule
        assert len(periods) == 2
        assert len(periods[0].day_rules) == 0


class TestProcessUntilEdgeCases:
    """Tests for _process_until edge cases (lines 125->exit, 127->exit)."""

    def test_until_at_end_of_fields_no_value(self) -> None:
        """Until: as the last field with no following value (field_index past end)."""
        doc = new_document()
        # Until is last field; no value follows it
        doc.add(
            "Schedule:Compact",
            "NoValueAfterUntil",
            validate=False,
            data=[
                {"field": "Through: 12/31"},
                {"field": "For: AllDays"},
                {"field": "Until: 24:00"},
                # No value field
            ],
        )
        obj = doc.get_collection("Schedule:Compact").get("NoValueAfterUntil")
        periods, _ = parse_compact(obj)
        # The Until: was processed but no time_value could be added
        assert len(periods) == 1
        assert len(periods[0].day_rules[0].time_values) == 0

    def test_until_followed_by_empty_value(self) -> None:
        """Until: followed by an empty value string (line 127->exit branch)."""
        doc = new_document()
        doc.add(
            "Schedule:Compact",
            "EmptyValue",
            validate=False,
            data=[
                {"field": "Through: 12/31"},
                {"field": "For: AllDays"},
                {"field": "Until: 24:00"},
                {"field": ""},  # Empty value string
            ],
        )
        obj = doc.get_collection("Schedule:Compact").get("EmptyValue")
        periods, _ = parse_compact(obj)
        assert len(periods) == 1
        # Empty value → no time_value appended
        assert len(periods[0].day_rules[0].time_values) == 0


class TestInterpolateKeyword:
    """Tests for Interpolate: Yes/Average/Linear branch (lines 140-141)."""

    def test_interpolate_yes_sets_average(self) -> None:
        """Interpolate: Yes sets interpolation mode to AVERAGE."""
        sched = _make_compact(
            "Through: 12/31",
            "For: AllDays",
            "Interpolate: Yes",
            "Until: 24:00",
            "1.0",
        )
        _, interp = parse_compact(sched)
        assert interp == Interpolation.AVERAGE

    def test_interpolate_average_sets_average(self) -> None:
        """Interpolate: Average sets interpolation mode."""
        sched = _make_compact(
            "Through: 12/31",
            "For: AllDays",
            "Interpolate: Average",
            "Until: 24:00",
            "1.0",
        )
        _, interp = parse_compact(sched)
        assert interp == Interpolation.AVERAGE

    def test_interpolate_linear_sets_linear(self) -> None:
        """Interpolate: Linear sets the LINEAR mode, distinct from AVERAGE."""
        sched = _make_compact(
            "Through: 12/31",
            "For: AllDays",
            "Interpolate: Linear",
            "Until: 24:00",
            "1.0",
        )
        _, interp = parse_compact(sched)
        assert interp == Interpolation.LINEAR

    def test_interpolate_no_keeps_no(self) -> None:
        """Interpolate: No does not change to AVERAGE."""
        sched = _make_compact(
            "Through: 12/31",
            "For: AllDays",
            "Interpolate: No",
            "Until: 24:00",
            "1.0",
        )
        _, interp = parse_compact(sched)
        assert interp == Interpolation.NO


def _ramp(mode: str, noon: str = "12:00") -> IDFObject:
    return _make_compact(
        "Through: 12/31", "For: AllDays", f"Interpolate: {mode}", f"Until: {noon}", "0", "Until: 24:00", "1"
    )


class TestInterpolatedValues:
    """values() for Interpolate: Average/Yes averages the step over each timestep (#364)."""

    @pytest.mark.parametrize("mode", ["Average", "Yes"])
    def test_average_on_timestep_boundaries_is_the_step(self, mode: str) -> None:
        """Until: times on timestep boundaries give the plain step, not a ramp."""
        result = values(_ramp(mode), year=2024, end_date=(1, 1))
        assert result == [0.0] * 12 + [1.0] * 12

    def test_average_is_mean_over_the_timestep(self) -> None:
        """An Until: inside a timestep gives the mean of the step over that timestep."""
        result = values(_ramp("Average", noon="12:15"), year=2024, end_date=(1, 1))
        assert result == [0.0] * 12 + [0.75] + [1.0] * 11

    def test_average_at_sub_hourly_timestep(self) -> None:
        """The average is taken over the requested timestep, not over the hour."""
        result = values(_ramp("Average", noon="12:10"), year=2024, end_date=(1, 1), timestep=4)
        assert result[47:51] == [0.0, pytest.approx(1 / 3), 1.0, 1.0]

    def test_linear_ramps_to_the_end_of_each_timestep(self) -> None:
        """Interpolate: Linear reads the ramp at the end of each timestep, as EnergyPlus does.

        EnergyPlus 26.1 gives 0.0833 for 12:00-13:00 and 1.0 for 23:00-24:00 on this schedule.
        """
        result = values(_ramp("Linear"), year=2024, end_date=(1, 1))
        assert result[11] == 0.0
        assert result[12] == pytest.approx(1 / 12)
        assert result[23] == pytest.approx(1.0)

    def test_point_evaluation_of_average_is_the_step(self) -> None:
        """evaluate_compact without a timestep returns the step value."""
        assert evaluate_compact(_ramp("Average"), datetime(2024, 1, 1, 18, 0)) == 1.0


class TestInterpolatePerForBlock:
    """Interpolate: applies to its own For: block, as in EnergyPlus."""

    def test_each_rule_keeps_its_own_mode(self) -> None:
        """A block without Interpolate: steps even when another block averages."""
        sched = _make_compact(
            "Through: 12/31",
            "For: WinterDesignDay",
            "Until: 24:00",
            "1",
            "For: AllOtherDays",
            "Interpolate: Average",
            "Until: 24:00",
            "1",
        )
        periods, _ = parse_compact(sched)
        assert [rule.interpolation for rule in periods[0].day_rules] == [Interpolation.NO, Interpolation.AVERAGE]

    def test_later_no_does_not_cancel_earlier_average(self) -> None:
        """A later block's Interpolate: No leaves an earlier block's Average in force."""
        sched = _make_compact(
            "Through: 12/31",
            "For: WinterDesignDay",
            "Interpolate: Average",
            "Until: 12:30",
            "0",
            "Until: 24:00",
            "1",
            "For: AllOtherDays",
            "Interpolate: No",
            "Until: 24:00",
            "0",
        )
        result = values(sched, year=2024, start_date=(12, 21), end_date=(12, 21), day_type="winter")
        assert result[12] == pytest.approx(0.5)


class TestSpecialDayReplacesWeekday:
    """A holiday or custom day is its own day type in EnergyPlus, not also its weekday."""

    def test_holiday_monday_uses_all_other_days(self) -> None:
        """A Monday holiday falls to AllOtherDays when no block names Holiday, not to Weekdays."""
        sched = _make_compact(
            "Through: 12/31", "For: Weekdays", "Until: 24:00", "1", "For: AllOtherDays", "Until: 24:00", "0"
        )
        monday_holiday = date(2024, 12, 23)
        assert evaluate_compact(sched, datetime(2024, 12, 23, 10, 0), holidays={monday_holiday}) == 0.0
        assert evaluate_compact(sched, datetime(2024, 12, 30, 10, 0), holidays={monday_holiday}) == 1.0


class TestCacheStaleness:
    """Tests that a mutated object invalidates the parse cache (lines 173-179)."""

    def test_stale_cache_re_parses(self) -> None:
        """After mutation_version changes, parse_compact re-parses the object."""
        sched = _make_compact(
            "Through: 12/31",
            "For: AllDays",
            "Until: 24:00",
            "1.0",
        )
        _parse_cache.clear()

        # Prime cache
        result1, _ = parse_compact(sched)
        assert result1[0].day_rules[0].time_values[0].value == 1.0

        # Trigger a real mutation (sets field, bumps _version)
        sched.schedule_type_limits_name = "Fraction"  # pyright: ignore[reportAttributeAccessIssue]

        # Now parse again — stale cache entry should be discarded
        # (The DSL data is unchanged, so result should still parse correctly)
        result2, _ = parse_compact(sched)
        assert result2[0].day_rules[0].time_values[0].value == 1.0

        _parse_cache.clear()


class TestProblemsCache:
    """compact_problems is computed once per parse, not on every evaluation."""

    def test_evaluate_reuses_problems_until_mutation(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import idfkit.schedules.compact as compact_mod

        sched = _make_compact("Through: 12/31", "For: AllDays", "Until: 24:00", "1.0")
        calls: list[IDFObject] = []
        original = compact_mod._find_compact_problems  # pyright: ignore[reportPrivateUsage]

        def counting(obj: IDFObject) -> list[str]:
            calls.append(obj)
            return original(obj)

        monkeypatch.setattr(compact_mod, "_find_compact_problems", counting)
        for hour in range(5):
            evaluate_compact(sched, datetime(2024, 1, 1, hour))
        assert len(calls) == 1

        sched.schedule_type_limits_name = "Fraction"  # pyright: ignore[reportAttributeAccessIssue]
        evaluate_compact(sched, datetime(2024, 1, 1, 6))
        assert len(calls) == 2

    def test_returned_list_is_a_copy(self) -> None:
        sched = _make_compact("Through: 6/30", "For: AllDays", "Until: 24:00", "1.0")
        compact_problems(sched).clear()
        assert compact_problems(sched)


class TestConsecutiveNoneLimit:
    """Tests for consecutive None termination (lines 198-202)."""

    def test_three_consecutive_blanks_stop_parsing(self) -> None:
        """Three consecutive empty fields break the parsing loop."""
        doc = new_document()
        # Add a schedule with blanks embedded after valid data
        doc.add(
            "Schedule:Compact",
            "BlankTest",
            validate=False,
            data=[
                {"field": "Through: 12/31"},
                {"field": "For: AllDays"},
                {"field": "Until: 24:00"},
                {"field": "1.0"},
                # Three trailing blank fields
                {"field": ""},
                {"field": ""},
                {"field": ""},
            ],
        )
        obj = doc.get_collection("Schedule:Compact").get("BlankTest")
        periods, _ = parse_compact(obj)
        assert len(periods) == 1


class TestFinalizeWithNoRule:
    """Tests for _finalize_parse_state when current_rule is None (line 147->149)."""

    def test_period_with_no_rule_is_finalized(self) -> None:
        """A period that has no For: rule still gets appended in finalization."""
        sched = _make_compact(
            "Through: 12/31",
            # No For:/Until: at all
        )
        periods, _ = parse_compact(sched)
        # Period exists but has no rules
        assert len(periods) == 1
        assert len(periods[0].day_rules) == 0


class TestNoPeriods:
    """Tests for evaluate_compact with no periods (line 262)."""

    def test_empty_compact_refused(self) -> None:
        """A compact schedule with no data covers no day, so it is refused rather than read as 0.0."""
        doc = new_document()
        # Add a schedule with no extensible fields at all
        doc.add("Schedule:Compact", "Empty", validate=False)
        obj = doc.get_collection("Schedule:Compact").get("Empty")
        with pytest.raises(ValueError, match="no 'Through:' field"):
            evaluate_compact(obj, datetime(2024, 1, 1, 12, 0))


class TestCoverage:
    """A schedule EnergyPlus refuses as fatal is refused, not extended or filled."""

    def test_complete_schedule_has_no_problems(self) -> None:
        sched = _make_compact(
            "Through: 6/30", "For: AllDays", "Until: 24:00", "1",
            "Through: 12/31", "For: Weekdays", "Until: 8:00", "0", "Until: 24:00", "1",
            "For: AllOtherDays", "Until: 24:00", "0",
        )  # fmt: skip
        assert compact_problems(sched) == []
        assert evaluate_compact(sched, datetime(2024, 7, 8, 14)) == 1.0

    def test_year_not_covered_refused(self) -> None:
        sched = _make_compact("Through: 6/30", "For: AllDays", "Until: 24:00", "20")
        assert compact_problems(sched) == [
            "the last 'Through:' is 6/30, not 12/31, so the rest of the year has no values"
        ]
        # A date inside the covered part is refused too: EnergyPlus refuses the whole schedule.
        for when in (datetime(2024, 7, 6, 14), datetime(2024, 1, 1, 0)):
            with pytest.raises(ValueError, match="would stop EnergyPlus: the last 'Through:' is 6/30"):
                evaluate_compact(sched, when)

    def test_day_not_ending_at_midnight_refused(self) -> None:
        sched = _make_compact("Through: 12/31", "For: AllDays", "Until: 12:00", "20")
        (problem,) = compact_problems(sched)
        assert "ends at 'Until: 12:00', not 'Until: 24:00'" in problem
        with pytest.raises(ValueError, match="Until: 24:00"):
            evaluate_compact(sched, datetime(2024, 7, 6, 14))

    def test_each_incomplete_block_reported(self) -> None:
        sched = _make_compact(
            "Through: 12/31", "For: Weekdays", "Until: 18:00", "1",
            "For: AllOtherDays", "Until: 12:00", "0",
        )  # fmt: skip
        problems = compact_problems(sched)
        assert len(problems) == 2
        assert "block 1" in problems[0]
        assert "block 2" in problems[1]

    def test_block_without_until_reported(self) -> None:
        sched = _make_compact("Through: 12/31", "For: AllDays")
        assert compact_problems(sched) == [
            "'Through: 12/31' block 1 ('For:' AllDays) has no 'Until:' value, so its days have no values"
        ]

    @pytest.mark.parametrize(
        "fields",
        [
            ("Through 12/31", "For AllDays", "Until 12:00", "1", "Until 24:00", "2"),
            ("Through : 12/31", "For: AllDays", "Until: 12:00", "1", "Until 24:00", "2"),
        ],
        ids=["no-colons", "space-before-colon"],
    )
    def test_keywords_without_colon_parsed(self, fields: tuple[str, ...]) -> None:
        """EnergyPlus reads these spellings (its example files use them), so they are not refused."""
        sched = _make_compact(*fields)
        assert compact_problems(sched) == []
        assert evaluate_compact(sched, datetime(2024, 7, 8, 14)) == 2.0

    def test_through_after_year_end_ignored(self) -> None:
        """A 'Through:' after the one reaching 12/31 is read by EnergyPlus without complaint."""
        sched = _make_compact(
            "Through: 12/31", "For: AllDays", "Until: 24:00", "1",
            "Through: 01/01", "For: AllDays", "Until: 24:00", "2",
        )  # fmt: skip
        assert compact_problems(sched) == []

    def test_missing_day_types_still_evaluate(self) -> None:
        """EnergyPlus only warns about day types a schedule leaves out, so they are not refused."""
        sched = _make_compact("Through: 12/31", "For: Weekdays", "Until: 24:00", "1")
        assert compact_problems(sched) == []


class TestNoMatchingRule:
    """Tests for evaluate_compact when no rule matches (lines 270, 280)."""

    def test_no_matching_rule_returns_zero(self) -> None:
        """When no day rule matches the day type, returns 0.0."""
        # SummerDesignDay-only schedule evaluated on a normal Monday
        sched = _make_compact(
            "Through: 12/31",
            "For: SummerDesignDay",
            "Until: 24:00",
            "1.0",
        )
        result = evaluate_compact(sched, datetime(2024, 1, 8, 12, 0))  # Monday
        assert result == 0.0

    def test_period_none_returns_zero(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """period=None from _find_period_for_date returns 0.0 (line 270)."""
        import idfkit.schedules.compact as compact_module

        monkeypatch.setattr(compact_module, "_find_period_for_date", lambda periods, d: None)

        sched = _make_compact(
            "Through: 12/31",
            "For: AllDays",
            "Until: 24:00",
            "1.0",
        )
        result = evaluate_compact(sched, datetime(2024, 1, 1, 12, 0))
        assert result == 0.0


class TestAllOtherDaysFallback:
    """Tests for AllOtherDays fallback in _find_matching_rule (line 335)."""

    def test_all_other_days_fallback(self) -> None:
        """AllOtherDays rule is used when no specific match exists."""
        rules = [
            CompactDayRule(day_types={DAY_TYPE_SUMMER_DESIGN}, time_values=[]),
            CompactDayRule(day_types={"AllOtherDays"}, time_values=[]),
        ]
        # Monday day types won't match SummerDesignDay but will fall back to AllOtherDays
        from idfkit.schedules.day_types import get_applicable_day_types

        day_types = get_applicable_day_types(
            date(2024, 1, 8),  # Monday
            DayType.NORMAL,
            holidays=set(),
            custom_day_1=set(),
            custom_day_2=set(),
        )
        result = _find_matching_rule(rules, day_types)
        assert result == rules[1]

    def test_all_other_days_fallback_for_design_day(self) -> None:
        """AllOtherDays fallback when applicable_types is a design-day set (line 335).

        When evaluating a summer design day, applicable_types = {SummerDesignDay, AllDays}.
        If no rule has SummerDesignDay or AllDays, but a rule has AllOtherDays,
        the fallback code at line 335 should fire.
        """
        rules = [
            CompactDayRule(day_types={"AllOtherDays"}, time_values=[]),
        ]
        # Summer design day types: only {SummerDesignDay, AllDays}
        # AllOtherDays is NOT in these applicable_types, so priority loop won't find it
        # The fallback at line 333-335 should pick up the AllOtherDays rule
        applicable_types = {DAY_TYPE_SUMMER_DESIGN}  # No AllDays, no AllOtherDays
        result = _find_matching_rule(rules, applicable_types)
        assert result == rules[0]
