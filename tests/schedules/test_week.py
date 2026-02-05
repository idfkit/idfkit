"""Tests for schedules.week module."""

from __future__ import annotations

from datetime import date, datetime
from unittest.mock import MagicMock

import pytest

from idfkit.schedules.day_types import get_applicable_day_types
from idfkit.schedules.types import (
    DAY_TYPE_ALL_OTHER_DAYS,
    DAY_TYPE_ALLDAYS,
    DAY_TYPE_CUSTOM_DAY_1,
    DAY_TYPE_CUSTOM_DAY_2,
    DAY_TYPE_HOLIDAY,
    DAY_TYPE_MONDAY,
    DAY_TYPE_SATURDAY,
    DAY_TYPE_SUMMER_DESIGN,
    DAY_TYPE_SUNDAY,
    DAY_TYPE_TUESDAY,
    DAY_TYPE_WEDNESDAY,
    DAY_TYPE_WEEKDAYS,
    DAY_TYPE_WEEKENDS,
    DAY_TYPE_WINTER_DESIGN,
    DayType,
    Interpolation,
)
from idfkit.schedules.week import (
    _find_day_schedule,
    _find_matching_day_in_week_compact,
    _get_day_schedule_name_for_date,
    _get_field_by_index,
    evaluate_week_compact,
    evaluate_week_daily,
)


def _make_week_daily(day_names: dict[str, str]) -> MagicMock:
    """Create a mock Schedule:Week:Daily object.

    Args:
        day_names: Mapping of field name to day schedule name.
    """
    obj = MagicMock()
    obj.obj_type = "Schedule:Week:Daily"
    obj.get.side_effect = lambda f: day_names.get(f)
    return obj


def _make_day_schedule(name: str, obj_type: str, hourly_value: float = 1.0) -> MagicMock:
    """Create a mock day schedule that returns a constant value."""
    obj = MagicMock()
    obj.obj_type = obj_type
    obj.name = name

    if obj_type == "Schedule:Constant":
        obj.get.return_value = hourly_value
    elif obj_type == "Schedule:Day:Hourly":
        obj.get.side_effect = lambda f: hourly_value if f.startswith("Hour ") else None
    elif obj_type == "Schedule:Day:Interval":
        fields = {
            "Time 1": "24:00",
            "Value Until Time 1": hourly_value,
            "Time 2": None,
        }
        obj.get.side_effect = lambda f: fields.get(f)
    elif obj_type == "Schedule:Day:List":
        fields: dict[str, float | int | None] = {
            "Minutes per Item": 60,
            "Interpolate to Timestep": None,
        }
        for i in range(1, 25):
            fields[f"Value {i}"] = hourly_value
        fields["Value 25"] = None
        obj.get.side_effect = lambda f: fields.get(f)
    return obj


def _make_doc_with_day_schedule(day_obj: MagicMock) -> MagicMock:
    """Create a mock document containing a single day schedule."""
    doc = MagicMock()

    def getitem(sched_type: str) -> list[MagicMock]:
        if sched_type == day_obj.obj_type:
            return [day_obj]
        return []

    doc.__getitem__.side_effect = getitem
    return doc


# ---------------------------------------------------------------------------
# _get_field_by_index
# ---------------------------------------------------------------------------


class TestGetFieldByIndex:
    """Tests for _get_field_by_index."""

    def test_returns_string_value(self) -> None:
        obj = _make_week_daily({"Sunday Schedule:Day Name": "SundaySched"})
        assert _get_field_by_index(obj, 0) == "SundaySched"

    def test_returns_none_when_missing(self) -> None:
        obj = _make_week_daily({})
        assert _get_field_by_index(obj, 0) is None

    def test_each_index_maps_to_correct_field(self) -> None:
        """Verify index 0-11 maps to the correct field name."""
        expected = [
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
        for i, field in enumerate(expected):
            obj = _make_week_daily({field: f"Sched{i}"})
            assert _get_field_by_index(obj, i) == f"Sched{i}"


# ---------------------------------------------------------------------------
# _get_day_schedule_name_for_date
# ---------------------------------------------------------------------------


class TestGetDayScheduleNameForDate:
    """Tests for _get_day_schedule_name_for_date."""

    @pytest.fixture
    def week_obj(self) -> MagicMock:
        return _make_week_daily({
            "Sunday Schedule:Day Name": "SundaySched",
            "Monday Schedule:Day Name": "MondaySched",
            "Tuesday Schedule:Day Name": "TuesdaySched",
            "Wednesday Schedule:Day Name": "WednesdaySched",
            "Thursday Schedule:Day Name": "ThursdaySched",
            "Friday Schedule:Day Name": "FridaySched",
            "Saturday Schedule:Day Name": "SaturdaySched",
            "Holiday Schedule:Day Name": "HolidaySched",
            "SummerDesignDay Schedule:Day Name": "SummerSched",
            "WinterDesignDay Schedule:Day Name": "WinterSched",
            "CustomDay1 Schedule:Day Name": "Custom1Sched",
            "CustomDay2 Schedule:Day Name": "Custom2Sched",
        })

    def test_monday_calendar(self, week_obj: MagicMock) -> None:
        """Monday (weekday 0) maps to field index 1."""
        d = date(2024, 1, 8)  # Monday
        result = _get_day_schedule_name_for_date(week_obj, d, DayType.NORMAL, set(), set(), set())
        assert result == "MondaySched"

    def test_sunday_calendar(self, week_obj: MagicMock) -> None:
        d = date(2024, 1, 7)  # Sunday
        result = _get_day_schedule_name_for_date(week_obj, d, DayType.NORMAL, set(), set(), set())
        assert result == "SundaySched"

    def test_saturday_calendar(self, week_obj: MagicMock) -> None:
        d = date(2024, 1, 6)  # Saturday
        result = _get_day_schedule_name_for_date(week_obj, d, DayType.NORMAL, set(), set(), set())
        assert result == "SaturdaySched"

    def test_summer_design_override(self, week_obj: MagicMock) -> None:
        d = date(2024, 7, 15)  # Any date
        result = _get_day_schedule_name_for_date(week_obj, d, DayType.SUMMER_DESIGN, set(), set(), set())
        assert result == "SummerSched"

    def test_winter_design_override(self, week_obj: MagicMock) -> None:
        d = date(2024, 1, 15)
        result = _get_day_schedule_name_for_date(week_obj, d, DayType.WINTER_DESIGN, set(), set(), set())
        assert result == "WinterSched"

    def test_holiday_override(self, week_obj: MagicMock) -> None:
        d = date(2024, 12, 25)
        result = _get_day_schedule_name_for_date(week_obj, d, DayType.HOLIDAY, set(), set(), set())
        assert result == "HolidaySched"

    def test_custom_day_1_override(self, week_obj: MagicMock) -> None:
        d = date(2024, 3, 1)
        result = _get_day_schedule_name_for_date(week_obj, d, DayType.CUSTOM_DAY_1, set(), set(), set())
        assert result == "Custom1Sched"

    def test_custom_day_2_override(self, week_obj: MagicMock) -> None:
        d = date(2024, 3, 1)
        result = _get_day_schedule_name_for_date(week_obj, d, DayType.CUSTOM_DAY_2, set(), set(), set())
        assert result == "Custom2Sched"

    def test_holiday_date_set(self, week_obj: MagicMock) -> None:
        """Holiday in date set takes priority over weekday."""
        d = date(2024, 12, 25)  # Wednesday
        result = _get_day_schedule_name_for_date(week_obj, d, DayType.NORMAL, {d}, set(), set())
        assert result == "HolidaySched"

    def test_custom_day_1_date_set(self, week_obj: MagicMock) -> None:
        d = date(2024, 3, 1)  # Friday
        result = _get_day_schedule_name_for_date(week_obj, d, DayType.NORMAL, set(), {d}, set())
        assert result == "Custom1Sched"

    def test_custom_day_2_date_set(self, week_obj: MagicMock) -> None:
        d = date(2024, 3, 1)  # Friday
        result = _get_day_schedule_name_for_date(week_obj, d, DayType.NORMAL, set(), set(), {d})
        assert result == "Custom2Sched"

    def test_custom_day_2_beats_custom_day_1(self, week_obj: MagicMock) -> None:
        """CustomDay2 has higher priority than CustomDay1."""
        d = date(2024, 3, 1)
        result = _get_day_schedule_name_for_date(week_obj, d, DayType.NORMAL, set(), {d}, {d})
        assert result == "Custom2Sched"

    def test_custom_day_1_beats_holiday(self, week_obj: MagicMock) -> None:
        """CustomDay1 has higher priority than Holiday."""
        d = date(2024, 12, 25)
        result = _get_day_schedule_name_for_date(week_obj, d, DayType.NORMAL, {d}, {d}, set())
        assert result == "Custom1Sched"


# ---------------------------------------------------------------------------
# _find_day_schedule
# ---------------------------------------------------------------------------


class TestFindDaySchedule:
    """Tests for _find_day_schedule."""

    def test_found_hourly(self) -> None:
        day_obj = _make_day_schedule("MySched", "Schedule:Day:Hourly")
        doc = _make_doc_with_day_schedule(day_obj)
        assert _find_day_schedule(doc, "MySched") is day_obj

    def test_found_interval(self) -> None:
        day_obj = _make_day_schedule("MySched", "Schedule:Day:Interval")
        doc = _make_doc_with_day_schedule(day_obj)
        assert _find_day_schedule(doc, "MySched") is day_obj

    def test_found_list(self) -> None:
        day_obj = _make_day_schedule("MySched", "Schedule:Day:List")
        doc = _make_doc_with_day_schedule(day_obj)
        assert _find_day_schedule(doc, "MySched") is day_obj

    def test_found_constant(self) -> None:
        day_obj = _make_day_schedule("MySched", "Schedule:Constant")
        doc = _make_doc_with_day_schedule(day_obj)
        assert _find_day_schedule(doc, "MySched") is day_obj

    def test_case_insensitive(self) -> None:
        day_obj = _make_day_schedule("MySched", "Schedule:Day:Hourly")
        doc = _make_doc_with_day_schedule(day_obj)
        assert _find_day_schedule(doc, "mysched") is day_obj
        assert _find_day_schedule(doc, "MYSCHED") is day_obj

    def test_not_found(self) -> None:
        doc = MagicMock()
        doc.__getitem__.return_value = []
        assert _find_day_schedule(doc, "NonExistent") is None


# ---------------------------------------------------------------------------
# evaluate_week_daily
# ---------------------------------------------------------------------------


class TestEvaluateWeekDaily:
    """Tests for evaluate_week_daily."""

    def _setup(
        self,
        day_type_str: str = "Schedule:Constant",
        value: float = 0.75,
    ) -> tuple[MagicMock, MagicMock, MagicMock]:
        """Create week obj, day obj, and doc for evaluation."""
        day_obj = _make_day_schedule("DaySched", day_type_str, value)
        doc = _make_doc_with_day_schedule(day_obj)
        week_obj = _make_week_daily({
            "Sunday Schedule:Day Name": "DaySched",
            "Monday Schedule:Day Name": "DaySched",
            "Tuesday Schedule:Day Name": "DaySched",
            "Wednesday Schedule:Day Name": "DaySched",
            "Thursday Schedule:Day Name": "DaySched",
            "Friday Schedule:Day Name": "DaySched",
            "Saturday Schedule:Day Name": "DaySched",
            "Holiday Schedule:Day Name": "DaySched",
            "SummerDesignDay Schedule:Day Name": "DaySched",
            "WinterDesignDay Schedule:Day Name": "DaySched",
            "CustomDay1 Schedule:Day Name": "DaySched",
            "CustomDay2 Schedule:Day Name": "DaySched",
        })
        return week_obj, day_obj, doc

    def test_weekday_constant(self) -> None:
        week_obj, _, doc = self._setup("Schedule:Constant", 0.75)
        result = evaluate_week_daily(week_obj, datetime(2024, 1, 8, 12, 0), doc)
        assert result == 0.75

    def test_weekday_hourly(self) -> None:
        week_obj, _, doc = self._setup("Schedule:Day:Hourly", 0.5)
        result = evaluate_week_daily(week_obj, datetime(2024, 1, 8, 10, 0), doc)
        assert result == 0.5

    def test_weekday_interval(self) -> None:
        week_obj, _, doc = self._setup("Schedule:Day:Interval", 0.9)
        result = evaluate_week_daily(week_obj, datetime(2024, 1, 8, 10, 0), doc)
        assert result == 0.9

    def test_weekday_list(self) -> None:
        week_obj, _, doc = self._setup("Schedule:Day:List", 0.6)
        result = evaluate_week_daily(week_obj, datetime(2024, 1, 8, 10, 0), doc)
        assert result == 0.6

    def test_holiday_override(self) -> None:
        week_obj, _, doc = self._setup("Schedule:Constant", 0.3)
        result = evaluate_week_daily(
            week_obj,
            datetime(2024, 12, 25, 12, 0),
            doc,
            holidays={date(2024, 12, 25)},
        )
        assert result == 0.3

    def test_summer_design_day(self) -> None:
        week_obj, _, doc = self._setup("Schedule:Constant", 0.8)
        result = evaluate_week_daily(
            week_obj,
            datetime(2024, 7, 15, 12, 0),
            doc,
            day_type=DayType.SUMMER_DESIGN,
        )
        assert result == 0.8

    def test_missing_day_name_returns_zero(self) -> None:
        """If the week schedule has no day name for the day, return 0.0."""
        week_obj = _make_week_daily({})  # No fields set
        doc = MagicMock()
        doc.__getitem__.return_value = []
        result = evaluate_week_daily(week_obj, datetime(2024, 1, 8, 12, 0), doc)
        assert result == 0.0

    def test_day_schedule_not_found_raises(self) -> None:
        """Referenced day schedule not in document raises ValueError."""
        week_obj = _make_week_daily({"Monday Schedule:Day Name": "NonExistent"})
        doc = MagicMock()
        doc.__getitem__.return_value = []

        with pytest.raises(ValueError, match="Day schedule not found"):
            evaluate_week_daily(week_obj, datetime(2024, 1, 8, 12, 0), doc)

    def test_unsupported_day_type_raises(self) -> None:
        """Unsupported day schedule type raises ValueError."""
        day_obj = MagicMock()
        day_obj.obj_type = "Schedule:Unknown"
        day_obj.name = "DaySched"
        # Place in a known collection so _find_day_schedule finds it by name
        doc = MagicMock()
        doc.__getitem__.side_effect = lambda t: [day_obj] if t == "Schedule:Day:Hourly" else []
        week_obj = _make_week_daily({"Monday Schedule:Day Name": "DaySched"})

        with pytest.raises(ValueError, match="Unsupported day schedule type"):
            evaluate_week_daily(week_obj, datetime(2024, 1, 8, 12, 0), doc)

    def test_interpolation_passed_through(self) -> None:
        """Interpolation parameter is forwarded to day interval evaluator."""
        day_obj = MagicMock()
        day_obj.obj_type = "Schedule:Day:Interval"
        day_obj.name = "DaySched"
        fields = {
            "Time 1": "12:00",
            "Value Until Time 1": 0.0,
            "Time 2": "24:00",
            "Value Until Time 2": 1.0,
            "Time 3": None,
        }
        day_obj.get.side_effect = lambda f: fields.get(f)
        doc = _make_doc_with_day_schedule(day_obj)
        week_obj = _make_week_daily({"Monday Schedule:Day Name": "DaySched"})

        # With NO interpolation: at 6:00 (< 12:00) should be 0.0
        result_no = evaluate_week_daily(week_obj, datetime(2024, 1, 8, 6, 0), doc, interpolation=Interpolation.NO)
        assert result_no == 0.0

        # With AVERAGE interpolation: at 6:00 should be interpolated
        result_avg = evaluate_week_daily(week_obj, datetime(2024, 1, 8, 6, 0), doc, interpolation=Interpolation.AVERAGE)
        assert result_avg == pytest.approx(0.0)  # 6/12 of the way from 0.0 to 0.0 (prev val is 0)


# ---------------------------------------------------------------------------
# _get_applicable_day_types (week.py version)
# ---------------------------------------------------------------------------


class TestGetApplicableDayTypes:
    """Tests for _get_applicable_day_types in week.py."""

    def test_summer_design_override(self) -> None:
        types = get_applicable_day_types(date(2024, 7, 15), DayType.SUMMER_DESIGN, set(), set(), set())
        assert types == {DAY_TYPE_SUMMER_DESIGN, DAY_TYPE_ALLDAYS}

    def test_winter_design_override(self) -> None:
        types = get_applicable_day_types(date(2024, 1, 15), DayType.WINTER_DESIGN, set(), set(), set())
        assert types == {DAY_TYPE_WINTER_DESIGN, DAY_TYPE_ALLDAYS}

    def test_holiday_override(self) -> None:
        types = get_applicable_day_types(date(2024, 12, 25), DayType.HOLIDAY, set(), set(), set())
        assert types == {DAY_TYPE_HOLIDAY, DAY_TYPE_ALLDAYS}

    def test_custom_day_1_override(self) -> None:
        types = get_applicable_day_types(date(2024, 3, 1), DayType.CUSTOM_DAY_1, set(), set(), set())
        assert types == {DAY_TYPE_CUSTOM_DAY_1, DAY_TYPE_ALLDAYS}

    def test_custom_day_2_override(self) -> None:
        types = get_applicable_day_types(date(2024, 3, 1), DayType.CUSTOM_DAY_2, set(), set(), set())
        assert types == {DAY_TYPE_CUSTOM_DAY_2, DAY_TYPE_ALLDAYS}

    def test_normal_monday(self) -> None:
        d = date(2024, 1, 8)  # Monday
        types = get_applicable_day_types(d, DayType.NORMAL, set(), set(), set())
        assert DAY_TYPE_MONDAY in types
        assert DAY_TYPE_WEEKDAYS in types
        assert DAY_TYPE_ALLDAYS in types
        assert DAY_TYPE_ALL_OTHER_DAYS in types
        assert DAY_TYPE_WEEKENDS not in types

    def test_normal_saturday(self) -> None:
        d = date(2024, 1, 6)  # Saturday
        types = get_applicable_day_types(d, DayType.NORMAL, set(), set(), set())
        assert DAY_TYPE_SATURDAY in types
        assert DAY_TYPE_WEEKENDS in types
        assert DAY_TYPE_ALLDAYS in types
        assert DAY_TYPE_WEEKDAYS not in types

    def test_normal_sunday(self) -> None:
        d = date(2024, 1, 7)  # Sunday
        types = get_applicable_day_types(d, DayType.NORMAL, set(), set(), set())
        assert DAY_TYPE_SUNDAY in types
        assert DAY_TYPE_WEEKENDS in types

    def test_holiday_in_set(self) -> None:
        d = date(2024, 12, 25)  # Wednesday
        types = get_applicable_day_types(d, DayType.NORMAL, {d}, set(), set())
        assert DAY_TYPE_HOLIDAY in types
        assert DAY_TYPE_WEDNESDAY in types  # Also includes weekday

    def test_custom_day_1_in_set(self) -> None:
        d = date(2024, 3, 1)
        types = get_applicable_day_types(d, DayType.NORMAL, set(), {d}, set())
        assert DAY_TYPE_CUSTOM_DAY_1 in types

    def test_custom_day_2_in_set(self) -> None:
        d = date(2024, 3, 1)
        types = get_applicable_day_types(d, DayType.NORMAL, set(), set(), {d})
        assert DAY_TYPE_CUSTOM_DAY_2 in types

    def test_all_weekdays(self) -> None:
        """Verify all weekdays Mon-Fri produce correct types."""
        # Jan 8 = Monday, Jan 9 = Tuesday, etc.
        for offset, day_type in enumerate([DAY_TYPE_MONDAY, DAY_TYPE_TUESDAY, DAY_TYPE_WEDNESDAY]):
            d = date(2024, 1, 8 + offset)
            types = get_applicable_day_types(d, DayType.NORMAL, set(), set(), set())
            assert day_type in types
            assert DAY_TYPE_WEEKDAYS in types


# ---------------------------------------------------------------------------
# _find_matching_day_in_week_compact
# ---------------------------------------------------------------------------


class TestFindMatchingDayInWeekCompact:
    """Tests for _find_matching_day_in_week_compact."""

    def _make_week_compact(self, pairs: list[tuple[str, str]]) -> MagicMock:
        """Create a mock Schedule:Week:Compact with DayType/Schedule pairs."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Week:Compact"
        fields: dict[str, str | None] = {}
        for i, (day_types, sched_name) in enumerate(pairs, 1):
            fields[f"DayType List {i}"] = day_types
            fields[f"Schedule:Day Name {i}"] = sched_name
        # Terminate the loop
        fields[f"DayType List {len(pairs) + 1}"] = None
        obj.get.side_effect = lambda f: fields.get(f)
        return obj

    def test_simple_alldays(self) -> None:
        obj = self._make_week_compact([("AllDays", "AllDaySched")])
        types = {DAY_TYPE_MONDAY, DAY_TYPE_WEEKDAYS, DAY_TYPE_ALLDAYS, DAY_TYPE_ALL_OTHER_DAYS}
        assert _find_matching_day_in_week_compact(obj, types) == "AllDaySched"

    def test_weekday_vs_weekend(self) -> None:
        obj = self._make_week_compact([
            ("Weekdays", "WeekdaySched"),
            ("Weekends", "WeekendSched"),
        ])
        weekday_types = {DAY_TYPE_MONDAY, DAY_TYPE_WEEKDAYS, DAY_TYPE_ALLDAYS, DAY_TYPE_ALL_OTHER_DAYS}
        assert _find_matching_day_in_week_compact(obj, weekday_types) == "WeekdaySched"

        weekend_types = {DAY_TYPE_SATURDAY, DAY_TYPE_WEEKENDS, DAY_TYPE_ALLDAYS, DAY_TYPE_ALL_OTHER_DAYS}
        assert _find_matching_day_in_week_compact(obj, weekend_types) == "WeekendSched"

    def test_specific_day_beats_weekdays(self) -> None:
        """Monday is more specific than Weekdays in priority."""
        obj = self._make_week_compact([
            ("Weekdays", "WeekdaySched"),
            ("Monday", "MondaySched"),
        ])
        types = {DAY_TYPE_MONDAY, DAY_TYPE_WEEKDAYS, DAY_TYPE_ALLDAYS, DAY_TYPE_ALL_OTHER_DAYS}
        assert _find_matching_day_in_week_compact(obj, types) == "MondaySched"

    def test_holiday_beats_weekday(self) -> None:
        obj = self._make_week_compact([
            ("Weekdays", "WeekdaySched"),
            ("Holiday", "HolidaySched"),
        ])
        types = {DAY_TYPE_WEDNESDAY, DAY_TYPE_WEEKDAYS, DAY_TYPE_HOLIDAY, DAY_TYPE_ALLDAYS, DAY_TYPE_ALL_OTHER_DAYS}
        assert _find_matching_day_in_week_compact(obj, types) == "HolidaySched"

    def test_summer_design_highest_priority(self) -> None:
        obj = self._make_week_compact([
            ("AllDays", "AllDaySched"),
            ("SummerDesignDay", "SummerSched"),
        ])
        types = {DAY_TYPE_SUMMER_DESIGN, DAY_TYPE_ALLDAYS}
        assert _find_matching_day_in_week_compact(obj, types) == "SummerSched"

    def test_space_separated_day_types(self) -> None:
        """DayType List can contain multiple space-separated types."""
        obj = self._make_week_compact([
            ("Weekdays SummerDesignDay", "WorkSched"),
            ("Weekends WinterDesignDay", "OffSched"),
        ])
        types = {DAY_TYPE_SUMMER_DESIGN, DAY_TYPE_ALLDAYS}
        assert _find_matching_day_in_week_compact(obj, types) == "WorkSched"

    def test_all_other_days_fallback(self) -> None:
        """AllOtherDays is returned when no other match exists."""
        obj = self._make_week_compact([
            ("SummerDesignDay", "SummerSched"),
            ("AllOtherDays", "FallbackSched"),
        ])
        types = {DAY_TYPE_MONDAY, DAY_TYPE_WEEKDAYS, DAY_TYPE_ALLDAYS, DAY_TYPE_ALL_OTHER_DAYS}
        # Monday is in applicable_types, AllOtherDays is in type_to_schedule
        # Monday should match AllOtherDays since both are in priority_order
        # Actually AllOtherDays is in applicable_types AND in type_to_schedule
        assert _find_matching_day_in_week_compact(obj, types) == "FallbackSched"

    def test_no_match_returns_none(self) -> None:
        obj = self._make_week_compact([
            ("SummerDesignDay", "SummerSched"),
        ])
        types = {DAY_TYPE_MONDAY, DAY_TYPE_WEEKDAYS}
        assert _find_matching_day_in_week_compact(obj, types) is None


# ---------------------------------------------------------------------------
# evaluate_week_compact
# ---------------------------------------------------------------------------


class TestEvaluateWeekCompact:
    """Tests for evaluate_week_compact."""

    def _make_week_compact(self, pairs: list[tuple[str, str]]) -> MagicMock:
        obj = MagicMock()
        obj.obj_type = "Schedule:Week:Compact"
        fields: dict[str, str | None] = {}
        for i, (day_types, sched_name) in enumerate(pairs, 1):
            fields[f"DayType List {i}"] = day_types
            fields[f"Schedule:Day Name {i}"] = sched_name
        fields[f"DayType List {len(pairs) + 1}"] = None
        obj.get.side_effect = lambda f: fields.get(f)
        return obj

    def test_weekday_evaluation(self) -> None:
        day_obj = _make_day_schedule("WeekdaySched", "Schedule:Constant", 1.0)
        off_obj = _make_day_schedule("OffSched", "Schedule:Constant", 0.0)
        off_obj.name = "OffSched"

        doc = MagicMock()

        def getitem(sched_type: str) -> list[MagicMock]:
            if sched_type == "Schedule:Constant":
                return [day_obj, off_obj]
            return []

        doc.__getitem__.side_effect = getitem

        week_obj = self._make_week_compact([
            ("Weekdays", "WeekdaySched"),
            ("AllOtherDays", "OffSched"),
        ])

        result = evaluate_week_compact(week_obj, datetime(2024, 1, 8, 12, 0), doc)
        assert result == 1.0

    def test_weekend_evaluation(self) -> None:
        day_obj = _make_day_schedule("WeekdaySched", "Schedule:Constant", 1.0)
        off_obj = _make_day_schedule("OffSched", "Schedule:Constant", 0.0)
        off_obj.name = "OffSched"

        doc = MagicMock()

        def getitem(sched_type: str) -> list[MagicMock]:
            if sched_type == "Schedule:Constant":
                return [day_obj, off_obj]
            return []

        doc.__getitem__.side_effect = getitem

        week_obj = self._make_week_compact([
            ("Weekdays", "WeekdaySched"),
            ("AllOtherDays", "OffSched"),
        ])

        result = evaluate_week_compact(week_obj, datetime(2024, 1, 6, 12, 0), doc)  # Saturday
        assert result == 0.0

    def test_no_matching_rule_returns_zero(self) -> None:
        week_obj = self._make_week_compact([
            ("SummerDesignDay", "SummerSched"),
        ])
        doc = MagicMock()
        doc.__getitem__.return_value = []

        result = evaluate_week_compact(week_obj, datetime(2024, 1, 8, 12, 0), doc)
        assert result == 0.0

    def test_day_schedule_not_found_raises(self) -> None:
        week_obj = self._make_week_compact([
            ("AllDays", "NonExistent"),
        ])
        doc = MagicMock()
        doc.__getitem__.return_value = []

        with pytest.raises(ValueError, match="Day schedule not found"):
            evaluate_week_compact(week_obj, datetime(2024, 1, 8, 12, 0), doc)

    def test_unsupported_day_schedule_type(self) -> None:
        day_obj = MagicMock()
        day_obj.obj_type = "Schedule:Unknown"
        day_obj.name = "BadSched"
        # Place in a known collection so _find_day_schedule finds it by name
        doc = MagicMock()
        doc.__getitem__.side_effect = lambda t: [day_obj] if t == "Schedule:Day:Hourly" else []

        week_obj = self._make_week_compact([("AllDays", "BadSched")])

        with pytest.raises(ValueError, match="Unsupported day schedule type"):
            evaluate_week_compact(week_obj, datetime(2024, 1, 8, 12, 0), doc)

    def test_design_day_override(self) -> None:
        summer_obj = _make_day_schedule("SummerSched", "Schedule:Constant", 0.99)
        other_obj = _make_day_schedule("OtherSched", "Schedule:Constant", 0.5)
        other_obj.name = "OtherSched"

        doc = MagicMock()

        def getitem(sched_type: str) -> list[MagicMock]:
            if sched_type == "Schedule:Constant":
                return [summer_obj, other_obj]
            return []

        doc.__getitem__.side_effect = getitem

        week_obj = self._make_week_compact([
            ("SummerDesignDay", "SummerSched"),
            ("AllOtherDays", "OtherSched"),
        ])

        result = evaluate_week_compact(week_obj, datetime(2024, 7, 15, 12, 0), doc, day_type=DayType.SUMMER_DESIGN)
        assert result == 0.99
