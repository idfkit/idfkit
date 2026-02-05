"""Tests for schedules.year module."""

from __future__ import annotations

from datetime import date, datetime
from unittest.mock import MagicMock

import pytest

from idfkit.schedules.types import DayType, Interpolation
from idfkit.schedules.year import (
    _find_week_for_date,
    _find_week_schedule,
    _parse_month_day,
    evaluate_year,
)

# ---------------------------------------------------------------------------
# _parse_month_day
# ---------------------------------------------------------------------------


class TestParseMonthDay:
    """Tests for _parse_month_day."""

    def test_numeric_month_and_day(self) -> None:
        assert _parse_month_day("1", "15") == (1, 15)

    def test_december(self) -> None:
        assert _parse_month_day("12", "31") == (12, 31)

    def test_month_name_january(self) -> None:
        assert _parse_month_day("January", "1") == (1, 1)

    def test_month_name_december(self) -> None:
        assert _parse_month_day("December", "31") == (12, 31)

    def test_month_name_case_insensitive(self) -> None:
        assert _parse_month_day("JUNE", "15") == (6, 15)
        assert _parse_month_day("june", "15") == (6, 15)
        assert _parse_month_day("June", "15") == (6, 15)

    def test_all_month_names(self) -> None:
        expected = [
            ("January", 1),
            ("February", 2),
            ("March", 3),
            ("April", 4),
            ("May", 5),
            ("June", 6),
            ("July", 7),
            ("August", 8),
            ("September", 9),
            ("October", 10),
            ("November", 11),
            ("December", 12),
        ]
        for name, number in expected:
            assert _parse_month_day(name, "1") == (number, 1)

    def test_whitespace_handling(self) -> None:
        assert _parse_month_day("  6  ", "15") == (6, 15)


# ---------------------------------------------------------------------------
# _find_week_schedule
# ---------------------------------------------------------------------------


class TestFindWeekSchedule:
    """Tests for _find_week_schedule."""

    def test_found_week_daily(self) -> None:
        week_obj = MagicMock()
        week_obj.obj_type = "Schedule:Week:Daily"
        week_obj.name = "MyWeek"

        doc = MagicMock()

        def getitem(sched_type: str) -> list[MagicMock]:
            if sched_type == "Schedule:Week:Daily":
                return [week_obj]
            return []

        doc.__getitem__.side_effect = getitem
        assert _find_week_schedule(doc, "MyWeek") is week_obj

    def test_found_week_compact(self) -> None:
        week_obj = MagicMock()
        week_obj.obj_type = "Schedule:Week:Compact"
        week_obj.name = "MyWeek"

        doc = MagicMock()

        def getitem(sched_type: str) -> list[MagicMock]:
            if sched_type == "Schedule:Week:Compact":
                return [week_obj]
            return []

        doc.__getitem__.side_effect = getitem
        assert _find_week_schedule(doc, "MyWeek") is week_obj

    def test_case_insensitive(self) -> None:
        week_obj = MagicMock()
        week_obj.obj_type = "Schedule:Week:Daily"
        week_obj.name = "MyWeek"

        doc = MagicMock()

        def getitem(sched_type: str) -> list[MagicMock]:
            if sched_type == "Schedule:Week:Daily":
                return [week_obj]
            return []

        doc.__getitem__.side_effect = getitem
        assert _find_week_schedule(doc, "myweek") is week_obj
        assert _find_week_schedule(doc, "MYWEEK") is week_obj

    def test_not_found(self) -> None:
        doc = MagicMock()
        doc.__getitem__.return_value = []
        assert _find_week_schedule(doc, "NonExistent") is None


# ---------------------------------------------------------------------------
# _find_week_for_date
# ---------------------------------------------------------------------------


def _make_year_obj(ranges: list[tuple[str, str, str, str, str]]) -> MagicMock:
    """Create a mock Schedule:Year with date ranges.

    Each range is (week_name, start_month, start_day, end_month, end_day).
    """
    obj = MagicMock()
    obj.obj_type = "Schedule:Year"

    fields: dict[str, str | None] = {}
    for i, (week_name, sm, sd, em, ed) in enumerate(ranges, 1):
        fields[f"Schedule:Week Name {i}"] = week_name
        fields[f"Start Month {i}"] = sm
        fields[f"Start Day {i}"] = sd
        fields[f"End Month {i}"] = em
        fields[f"End Day {i}"] = ed
    # Terminate the loop
    fields[f"Schedule:Week Name {len(ranges) + 1}"] = None

    obj.get.side_effect = lambda f: fields.get(f)
    return obj


class TestFindWeekForDate:
    """Tests for _find_week_for_date."""

    def test_single_full_year_range(self) -> None:
        """Single range covering entire year."""
        week_obj = MagicMock()
        week_obj.obj_type = "Schedule:Week:Daily"
        week_obj.name = "AllYear"

        doc = MagicMock()

        def getitem(sched_type: str) -> list[MagicMock]:
            if sched_type == "Schedule:Week:Daily":
                return [week_obj]
            return []

        doc.__getitem__.side_effect = getitem

        year_obj = _make_year_obj([("AllYear", "1", "1", "12", "31")])

        name, result = _find_week_for_date(year_obj, date(2024, 6, 15), 2024, doc)
        assert name == "AllYear"
        assert result is week_obj

    def test_multiple_ranges(self) -> None:
        """Two ranges: Jan-Jun and Jul-Dec."""
        week1 = MagicMock()
        week1.obj_type = "Schedule:Week:Daily"
        week1.name = "FirstHalf"
        week2 = MagicMock()
        week2.obj_type = "Schedule:Week:Daily"
        week2.name = "SecondHalf"

        doc = MagicMock()

        def getitem(sched_type: str) -> list[MagicMock]:
            if sched_type == "Schedule:Week:Daily":
                return [week1, week2]
            return []

        doc.__getitem__.side_effect = getitem

        year_obj = _make_year_obj([
            ("FirstHalf", "1", "1", "6", "30"),
            ("SecondHalf", "7", "1", "12", "31"),
        ])

        name1, result1 = _find_week_for_date(year_obj, date(2024, 3, 15), 2024, doc)
        assert name1 == "FirstHalf"
        assert result1 is week1

        name2, result2 = _find_week_for_date(year_obj, date(2024, 9, 15), 2024, doc)
        assert name2 == "SecondHalf"
        assert result2 is week2

    def test_boundary_dates(self) -> None:
        """Test dates at range boundaries."""
        week_obj = MagicMock()
        week_obj.obj_type = "Schedule:Week:Daily"
        week_obj.name = "FirstHalf"

        doc = MagicMock()

        def getitem(sched_type: str) -> list[MagicMock]:
            if sched_type == "Schedule:Week:Daily":
                return [week_obj]
            return []

        doc.__getitem__.side_effect = getitem

        year_obj = _make_year_obj([("FirstHalf", "1", "1", "6", "30")])

        # Start boundary
        _, result_start = _find_week_for_date(year_obj, date(2024, 1, 1), 2024, doc)
        assert result_start is week_obj

        # End boundary
        _, result_end = _find_week_for_date(year_obj, date(2024, 6, 30), 2024, doc)
        assert result_end is week_obj

        # Just outside range
        name, result_outside = _find_week_for_date(year_obj, date(2024, 7, 1), 2024, doc)
        assert name == ""
        assert result_outside is None

    def test_year_wraparound(self) -> None:
        """Test range that wraps around the year (e.g., Nov 1 - Feb 28)."""
        week_obj = MagicMock()
        week_obj.obj_type = "Schedule:Week:Daily"
        week_obj.name = "WinterWeek"

        doc = MagicMock()

        def getitem(sched_type: str) -> list[MagicMock]:
            if sched_type == "Schedule:Week:Daily":
                return [week_obj]
            return []

        doc.__getitem__.side_effect = getitem

        year_obj = _make_year_obj([("WinterWeek", "11", "1", "2", "28")])

        # November date (end-of-year portion)
        _, result_nov = _find_week_for_date(year_obj, date(2024, 12, 15), 2024, doc)
        assert result_nov is week_obj

        # February date (start-of-year portion)
        _, result_feb = _find_week_for_date(year_obj, date(2024, 1, 15), 2024, doc)
        assert result_feb is week_obj

        # Outside the range
        _, result_outside = _find_week_for_date(year_obj, date(2024, 6, 15), 2024, doc)
        assert result_outside is None

    def test_no_matching_range(self) -> None:
        year_obj = _make_year_obj([("SomeWeek", "6", "1", "8", "31")])

        doc = MagicMock()
        doc.__getitem__.return_value = []

        name, result = _find_week_for_date(year_obj, date(2024, 1, 15), 2024, doc)
        assert name == ""
        assert result is None

    def test_missing_date_fields_skipped(self) -> None:
        """Ranges with missing date fields are skipped."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Year"

        fields: dict[str, str | None] = {
            "Schedule:Week Name 1": "BadWeek",
            "Start Month 1": "1",
            "Start Day 1": None,  # Missing!
            "End Month 1": "6",
            "End Day 1": "30",
            "Schedule:Week Name 2": None,
        }
        obj.get.side_effect = lambda f: fields.get(f)

        doc = MagicMock()
        doc.__getitem__.return_value = []

        name, result = _find_week_for_date(obj, date(2024, 3, 15), 2024, doc)
        assert name == ""
        assert result is None


# ---------------------------------------------------------------------------
# evaluate_year
# ---------------------------------------------------------------------------


class TestEvaluateYear:
    """Tests for evaluate_year."""

    def _make_full_setup(self, value: float = 0.75) -> tuple[MagicMock, MagicMock]:
        """Create year obj and doc with week+day schedules returning given value."""
        day_obj = MagicMock()
        day_obj.obj_type = "Schedule:Constant"
        day_obj.name = "DaySched"
        day_obj.get.return_value = value

        week_obj = MagicMock()
        week_obj.obj_type = "Schedule:Week:Daily"
        week_obj.name = "WeekSched"
        # Week obj returns "DaySched" for all day fields
        week_fields: dict[str, str] = {}
        for field in [
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
        ]:
            week_fields[field] = "DaySched"
        week_obj.get.side_effect = lambda f: week_fields.get(f)

        year_obj = _make_year_obj([("WeekSched", "1", "1", "12", "31")])

        doc = MagicMock()

        def getitem(sched_type: str) -> list[MagicMock]:
            if sched_type == "Schedule:Week:Daily":
                return [week_obj]
            if sched_type == "Schedule:Constant":
                return [day_obj]
            return []

        doc.__getitem__.side_effect = getitem
        return year_obj, doc

    def test_basic_evaluation(self) -> None:
        year_obj, doc = self._make_full_setup(0.75)
        result = evaluate_year(year_obj, datetime(2024, 6, 15, 12, 0), doc)
        assert result == 0.75

    def test_design_day_override(self) -> None:
        year_obj, doc = self._make_full_setup(0.5)
        result = evaluate_year(year_obj, datetime(2024, 7, 15, 12, 0), doc, day_type=DayType.SUMMER_DESIGN)
        assert result == 0.5

    def test_week_not_found_raises(self) -> None:
        """Week schedule name exists but object not in document raises ValueError."""
        year_obj = _make_year_obj([("NonExistent", "1", "1", "12", "31")])
        doc = MagicMock()
        doc.__getitem__.return_value = []

        with pytest.raises(ValueError, match="Week schedule not found"):
            evaluate_year(year_obj, datetime(2024, 6, 15, 12, 0), doc)

    def test_unsupported_week_type_raises(self) -> None:
        """Unsupported week schedule type raises ValueError."""
        bad_week = MagicMock()
        bad_week.obj_type = "Schedule:Week:Unknown"
        bad_week.name = "BadWeek"

        doc = MagicMock()

        def getitem(sched_type: str) -> list[MagicMock]:
            if sched_type == "Schedule:Week:Daily":
                return [bad_week]
            return []

        doc.__getitem__.side_effect = getitem

        year_obj = _make_year_obj([("BadWeek", "1", "1", "12", "31")])

        with pytest.raises(ValueError, match="Unsupported week schedule type"):
            evaluate_year(year_obj, datetime(2024, 6, 15, 12, 0), doc)

    def test_date_out_of_range(self) -> None:
        """Date not covered by any range returns ("", None) which raises."""
        year_obj = _make_year_obj([("WeekSched", "6", "1", "8", "31")])
        doc = MagicMock()
        doc.__getitem__.return_value = []

        with pytest.raises(ValueError, match="Week schedule not found"):
            evaluate_year(year_obj, datetime(2024, 1, 15, 12, 0), doc)

    def test_with_week_compact(self) -> None:
        """evaluate_year dispatches to evaluate_week_compact for Week:Compact."""
        day_obj = MagicMock()
        day_obj.obj_type = "Schedule:Constant"
        day_obj.name = "DaySched"
        day_obj.get.return_value = 0.42

        week_obj = MagicMock()
        week_obj.obj_type = "Schedule:Week:Compact"
        week_obj.name = "WeekSched"
        compact_fields: dict[str, str | None] = {
            "DayType List 1": "AllDays",
            "Schedule:Day Name 1": "DaySched",
            "DayType List 2": None,
        }
        week_obj.get.side_effect = lambda f: compact_fields.get(f)

        doc = MagicMock()

        def getitem(sched_type: str) -> list[MagicMock]:
            if sched_type == "Schedule:Week:Compact":
                return [week_obj]
            if sched_type == "Schedule:Constant":
                return [day_obj]
            return []

        doc.__getitem__.side_effect = getitem

        year_obj = _make_year_obj([("WeekSched", "1", "1", "12", "31")])
        result = evaluate_year(year_obj, datetime(2024, 6, 15, 12, 0), doc)
        assert result == 0.42

    def test_month_name_in_year_fields(self) -> None:
        """Schedule:Year with month names instead of numbers."""
        day_obj = MagicMock()
        day_obj.obj_type = "Schedule:Constant"
        day_obj.name = "DaySched"
        day_obj.get.return_value = 0.33

        week_obj = MagicMock()
        week_obj.obj_type = "Schedule:Week:Daily"
        week_obj.name = "WeekSched"
        week_fields: dict[str, str] = {}
        for field in [
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
        ]:
            week_fields[field] = "DaySched"
        week_obj.get.side_effect = lambda f: week_fields.get(f)

        doc = MagicMock()

        def getitem(sched_type: str) -> list[MagicMock]:
            if sched_type == "Schedule:Week:Daily":
                return [week_obj]
            if sched_type == "Schedule:Constant":
                return [day_obj]
            return []

        doc.__getitem__.side_effect = getitem

        # Use month names
        obj = MagicMock()
        obj.obj_type = "Schedule:Year"
        fields: dict[str, str | None] = {
            "Schedule:Week Name 1": "WeekSched",
            "Start Month 1": "January",
            "Start Day 1": "1",
            "End Month 1": "December",
            "End Day 1": "31",
            "Schedule:Week Name 2": None,
        }
        obj.get.side_effect = lambda f: fields.get(f)

        result = evaluate_year(obj, datetime(2024, 6, 15, 12, 0), doc)
        assert result == 0.33

    def test_interpolation_passed_through(self) -> None:
        """Interpolation parameter is forwarded through the chain."""
        day_obj = MagicMock()
        day_obj.obj_type = "Schedule:Day:Interval"
        day_obj.name = "DaySched"
        day_fields = {
            "Time 1": "24:00",
            "Value Until Time 1": 1.0,
            "Time 2": None,
        }
        day_obj.get.side_effect = lambda f: day_fields.get(f)

        week_obj = MagicMock()
        week_obj.obj_type = "Schedule:Week:Daily"
        week_obj.name = "WeekSched"
        week_fields: dict[str, str] = {}
        for field in [
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
        ]:
            week_fields[field] = "DaySched"
        week_obj.get.side_effect = lambda f: week_fields.get(f)

        doc = MagicMock()

        def getitem(sched_type: str) -> list[MagicMock]:
            if sched_type == "Schedule:Week:Daily":
                return [week_obj]
            if sched_type == "Schedule:Day:Interval":
                return [day_obj]
            return []

        doc.__getitem__.side_effect = getitem

        year_obj = _make_year_obj([("WeekSched", "1", "1", "12", "31")])
        result = evaluate_year(
            year_obj,
            datetime(2024, 6, 15, 12, 0),
            doc,
            interpolation=Interpolation.NO,
        )
        assert result == 1.0
