"""Tests for schedules.evaluate module."""

from __future__ import annotations

import math
from collections.abc import Callable
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Literal
from unittest.mock import MagicMock

import pytest

from idfkit import new_document
from idfkit.document import IDFDocument
from idfkit.objects import IDFObject
from idfkit.schedules.compact import evaluate_compact, evaluate_compact_range
from idfkit.schedules.evaluate import (
    MalformedScheduleError,
    ScheduleEvaluationError,
    ScheduleReferenceError,
    UnsupportedScheduleType,
    evaluate,
    values,
)
from idfkit.schedules.holidays import get_holidays, get_special_days_by_type
from idfkit.schedules.types import DayType, DayTypeInput, Interpolation, parse_day_type


def _list_items(get: Callable[[str], object]) -> list[dict[str, object]]:
    """Canonical Schedule:Day:List items for a mock whose ``get`` answers ``Value N``."""
    return [{"value": v} for n in range(1, 1441) if (v := get(f"Value {n}")) is not None]


class TestExceptions:
    """Tests for schedule evaluation exceptions."""

    def test_exception_hierarchy(self) -> None:
        """Test exception inheritance."""
        assert issubclass(UnsupportedScheduleType, ScheduleEvaluationError)
        assert issubclass(ScheduleReferenceError, ScheduleEvaluationError)
        assert issubclass(MalformedScheduleError, ScheduleEvaluationError)


class TestEvaluate:
    """Tests for evaluate function."""

    def test_constant_schedule(self) -> None:
        """Test evaluating Schedule:Constant."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Constant"
        obj.get.return_value = 0.75

        result = evaluate(obj, datetime(2024, 1, 1, 12, 0))
        assert result == 0.75

    def test_day_hourly_schedule(self) -> None:
        """Test evaluating Schedule:Day:Hourly."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Day:Hourly"

        def get_field(field: str) -> float | None:
            if field == "Hour 13":  # Hour 12 (0-indexed)
                return 0.5
            return 0.0

        obj.get.side_effect = get_field

        result = evaluate(obj, datetime(2024, 1, 1, 12, 0))
        assert result == 0.5

    def test_unsupported_type(self) -> None:
        """Test unsupported schedule type raises exception."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Unknown"

        with pytest.raises(UnsupportedScheduleType, match="Unsupported schedule type"):
            evaluate(obj, datetime(2024, 1, 1, 12, 0))

    def test_week_schedule_requires_document(self) -> None:
        """Test week schedule requires document."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Week:Daily"
        # Remove _document attribute
        del obj._document

        with pytest.raises(ScheduleReferenceError, match="Document required"):
            evaluate(obj, datetime(2024, 1, 1, 12, 0))

    def test_year_schedule_requires_document(self) -> None:
        """Test year schedule requires document."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Year"
        del obj._document

        with pytest.raises(ScheduleReferenceError, match="Document required"):
            evaluate(obj, datetime(2024, 1, 1, 12, 0))


class TestMalformedCompact:
    """A Schedule:Compact that EnergyPlus refuses is refused, not extended or filled."""

    @pytest.mark.parametrize(
        ("fields", "match"),
        [
            (["Through: 6/30", "For: AllDays", "Until: 24:00", "20"], "not 12/31"),
            (["Through: 12/31", "For: AllDays", "Until: 12:00", "20"], "not 'Until: 24:00'"),
        ],
        ids=["year-not-covered", "day-not-covered"],
    )
    def test_evaluate_and_values_raise(self, fields: list[str], match: str) -> None:
        doc = new_document()
        sched = doc.add("Schedule:Compact", "Heat", data=[{"field": f} for f in fields], validate=False)
        with pytest.raises(MalformedScheduleError, match=match):
            evaluate(sched, datetime(2024, 7, 6, 14))
        with pytest.raises(MalformedScheduleError, match="'Heat' would stop EnergyPlus"):
            values(sched, year=2024, start_date=(1, 1), end_date=(1, 1))


class TestValues:
    """Tests for values function."""

    def test_constant_schedule_full_year(self) -> None:
        """Test getting full year values for constant schedule."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Constant"
        obj.get.return_value = 0.5
        del obj._document

        result = values(obj, year=2024)

        # 8760 hours in non-leap year, but 2024 is leap year = 8784
        assert len(result) == 8784
        assert all(v == 0.5 for v in result)

    def test_constant_schedule_partial_year(self) -> None:
        """Test getting partial year values."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Constant"
        obj.get.return_value = 0.5
        del obj._document

        result = values(
            obj,
            year=2024,
            start_date=(1, 1),
            end_date=(1, 31),  # January only
        )

        # 31 days * 24 hours = 744 hours
        assert len(result) == 744

    def test_sub_hourly_timestep(self) -> None:
        """Test sub-hourly timestep."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Constant"
        obj.get.return_value = 0.5
        del obj._document

        result = values(
            obj,
            year=2024,
            timestep=4,  # 15-minute intervals
            start_date=(1, 1),
            end_date=(1, 1),  # Single day
        )

        # 24 hours * 4 values per hour = 96
        assert len(result) == 96

    def test_day_interval_with_interpolation(self) -> None:
        """Test day interval schedule with interpolation."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Day:Interval"
        obj.data = {
            "data": [
                {"time": "12:00", "value_until_time": 0.0},
                {"time": "24:00", "value_until_time": 1.0},
            ]
        }
        del obj._document

        result = values(
            obj,
            year=2024,
            timestep=1,
            start_date=(1, 1),
            end_date=(1, 1),
            interpolation=Interpolation.NO,
        )

        # First 12 hours should be 0.0, next 12 should be 1.0
        assert result[:12] == [0.0] * 12
        assert result[12:24] == [1.0] * 12


class TestIntegration:
    """Integration tests with realistic schedules."""

    @pytest.fixture
    def compact_office_schedule(self) -> IDFObject:
        """Create a realistic office schedule."""
        doc = new_document()
        doc.add(
            "Schedule:Compact",
            "Office",
            validate=False,
            data=[
                {"field": "Through: 12/31"},
                {"field": "For: Weekdays"},
                {"field": "Until: 08:00"},
                {"field": "0.0"},
                {"field": "Until: 18:00"},
                {"field": "1.0"},
                {"field": "Until: 24:00"},
                {"field": "0.0"},
                {"field": "For: AllOtherDays"},
                {"field": "Until: 24:00"},
                {"field": "0.0"},
            ],
        )
        return doc.get_collection("Schedule:Compact").get("Office")

    def test_office_schedule_weekday_pattern(self, compact_office_schedule: IDFObject) -> None:
        """Test office schedule produces expected weekday pattern."""
        # Get values for a single Monday (Jan 8, 2024)
        result = values(
            compact_office_schedule,
            year=2024,
            start_date=(1, 8),
            end_date=(1, 8),
        )

        # Hours 0-7: 0.0, Hours 8-17: 1.0, Hours 18-23: 0.0
        assert result[:8] == [0.0] * 8
        assert result[8:18] == [1.0] * 10
        assert result[18:] == [0.0] * 6

    def test_office_schedule_weekend_pattern(self, compact_office_schedule: IDFObject) -> None:
        """Test office schedule produces expected weekend pattern."""
        # Get values for a single Saturday (Jan 6, 2024)
        result = values(
            compact_office_schedule,
            year=2024,
            start_date=(1, 6),
            end_date=(1, 6),
        )

        # All hours should be 0.0 on weekend
        assert result == [0.0] * 24

    def test_office_schedule_week_sum(self, compact_office_schedule: IDFObject) -> None:
        """Test total occupied hours in a week."""
        # Get values for a full week (Mon Jan 8 - Sun Jan 14, 2024)
        result = values(
            compact_office_schedule,
            year=2024,
            start_date=(1, 8),
            end_date=(1, 14),
        )

        # 5 weekdays * 10 occupied hours = 50 hours
        total_occupied = sum(result)
        assert total_occupied == 50.0


class TestMalformedScheduleError:
    """Tests for MalformedScheduleError behavior."""

    def test_malformed_schedule_raises_error(self) -> None:
        """Test that a malformed day schedule raises MalformedScheduleError."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Day:Interval"
        obj.data = {"data": [{"time": "08:00", "value_until_time": "not_a_number"}]}
        del obj._document

        with pytest.raises(MalformedScheduleError):
            evaluate(obj, datetime(2024, 1, 1, 12, 0))

    def test_schedule_reference_error_not_wrapped(self) -> None:
        """Test ScheduleReferenceError passes through, not wrapped in MalformedScheduleError."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Week:Daily"
        del obj._document

        with pytest.raises(ScheduleReferenceError, match="Document required"):
            evaluate(obj, datetime(2024, 1, 1, 12, 0))


class TestLeapYearValues:
    """Tests for leap year value counts."""

    def test_leap_year_value_count(self) -> None:
        """Test that a leap year produces 8784 hourly values."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Constant"
        obj.get.return_value = 1.0
        del obj._document

        result = values(obj, year=2024)
        assert len(result) == 8784  # 366 days * 24 hours

    def test_non_leap_year_value_count(self) -> None:
        """Test that a non-leap year produces 8760 hourly values."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Constant"
        obj.get.return_value = 1.0
        del obj._document

        result = values(obj, year=2023)
        assert len(result) == 8760  # 365 days * 24 hours


class TestEvalSimpleDay:
    """Tests for _eval_simple_day covering all branches."""

    def test_day_list_branch(self) -> None:
        """Test _eval_simple_day dispatches to Schedule:Day:List correctly."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Day:List"

        def get_field(field: str) -> object:
            fields: dict[str, object] = {
                "Minutes per Item": 60,
                "Interpolate to Timestep": None,
                "Value 1": 0.7,
                "Value 2": None,
            }
            return fields.get(field)

        obj.get.side_effect = get_field
        obj.data = {"extensions": _list_items(get_field)}
        del obj._document

        result = evaluate(obj, datetime(2024, 1, 1, 0, 0))
        assert result == 0.7

    def test_not_a_simple_day_raises(self) -> None:
        """Directly calling _eval_simple_day with unknown type raises ValueError."""
        from idfkit.schedules.evaluate import _eval_simple_day  # pyright: ignore[reportPrivateUsage]

        obj = MagicMock()
        with pytest.raises(ValueError, match="Not a simple day schedule"):
            _eval_simple_day(obj, datetime(2024, 1, 1), "Schedule:NotAType")


class TestEvaluateDocumentSchedules:
    """Tests that exercise document-requiring schedule evaluation paths."""

    def test_week_daily_evaluation(self) -> None:
        """Exercise _eval_document_schedule for Schedule:Week:Daily (line 150)."""
        doc = new_document()
        doc.add(
            "Schedule:Day:Interval",
            "DaySched",
            validate=False,
            data=[{"time": "24:00", "value_until_time": "0.5"}],
        )
        doc.add(
            "Schedule:Week:Daily",
            "WeekSched",
            validate=False,
            sunday_schedule_day_name="DaySched",
            monday_schedule_day_name="DaySched",
            tuesday_schedule_day_name="DaySched",
            wednesday_schedule_day_name="DaySched",
            thursday_schedule_day_name="DaySched",
            friday_schedule_day_name="DaySched",
            saturday_schedule_day_name="DaySched",
            holiday_schedule_day_name="DaySched",
            summerdesignday_schedule_day_name="DaySched",
            winterdesignday_schedule_day_name="DaySched",
            customday1_schedule_day_name="DaySched",
            customday2_schedule_day_name="DaySched",
        )
        week_obj = doc.get_collection("Schedule:Week:Daily").get("WeekSched")
        result = evaluate(week_obj, datetime(2024, 1, 8, 12, 0), document=doc)
        assert result == 0.5

    def test_schedule_file_evaluation(self) -> None:
        """Exercise evaluate_schedule_file path in evaluate() (line 158)."""
        obj = MagicMock()
        obj.obj_type = "Schedule:File"

        def get_field(field: str) -> object:
            return {
                "File Name": "sched.csv",
                "Column Number": 1,
                "Rows to Skip at Top": 0,
                "Column Separator": "Comma",
                "Minutes per Item": 60,
                "Interpolate to Timestep": None,
            }.get(field)

        obj.get.side_effect = get_field
        del obj._document

        fs = MagicMock()
        fs.read_text.return_value = "\n".join(["1.0"] * 8784)

        result = evaluate(obj, datetime(2024, 1, 1, 0, 0), fs=fs, base_path=Path("/base"))
        assert result == 1.0

    def test_eval_document_schedule_not_document_raises(self) -> None:
        """_eval_document_schedule with unknown type raises ValueError."""
        from idfkit.schedules.evaluate import _eval_document_schedule  # pyright: ignore[reportPrivateUsage]

        obj = MagicMock()
        obj.obj_type = "Schedule:Unknown"
        doc = MagicMock()
        with pytest.raises(ValueError, match="Not a document schedule"):
            _eval_document_schedule(obj, datetime(2024, 1, 1), doc, DayType.NORMAL, set(), set(), set())

    def test_eval_document_week_compact(self) -> None:
        """Exercise Schedule:Week:Compact through evaluate() (line 184)."""
        doc = new_document()
        doc.add(
            "Schedule:Day:Interval",
            "DaySched",
            validate=False,
            data=[{"time": "24:00", "value_until_time": "0.3"}],
        )
        doc.add(
            "Schedule:Week:Compact",
            "WeekCompact",
            validate=False,
            data=[{"daytype_list": "AllDays", "schedule_day_name": "DaySched"}],
        )
        week_obj = doc.get_collection("Schedule:Week:Compact").get("WeekCompact")
        result = evaluate(week_obj, datetime(2024, 1, 8, 12, 0), document=doc)
        assert result == 0.3

    def test_eval_document_year(self) -> None:
        """Exercise Schedule:Year through evaluate() (line 186)."""
        doc = new_document()
        doc.add(
            "Schedule:Day:Interval",
            "DaySched",
            validate=False,
            data=[{"time": "24:00", "value_until_time": "0.8"}],
        )
        doc.add(
            "Schedule:Week:Daily",
            "WeekSched",
            validate=False,
            sunday_schedule_day_name="DaySched",
            monday_schedule_day_name="DaySched",
            tuesday_schedule_day_name="DaySched",
            wednesday_schedule_day_name="DaySched",
            thursday_schedule_day_name="DaySched",
            friday_schedule_day_name="DaySched",
            saturday_schedule_day_name="DaySched",
            holiday_schedule_day_name="DaySched",
            summerdesignday_schedule_day_name="DaySched",
            winterdesignday_schedule_day_name="DaySched",
            customday1_schedule_day_name="DaySched",
            customday2_schedule_day_name="DaySched",
        )
        doc.add(
            "Schedule:Year",
            "YearSched",
            validate=False,
            schedule_weeks=[
                {
                    "schedule_week_name": "WeekSched",
                    "start_month": "1",
                    "start_day": "1",
                    "end_month": "12",
                    "end_day": "31",
                }
            ],
        )
        year_obj = doc.get_collection("Schedule:Year").get("YearSched")
        result = evaluate(year_obj, datetime(2024, 6, 15, 12, 0), document=doc)
        assert result == 0.8


class TestValuesWithDocument:
    """Tests for values() that exercise the document-based holiday path (line 228->232)."""

    def test_values_with_document(self) -> None:
        """values() fetches holidays from document when document is provided."""
        doc = new_document()
        doc.add(
            "Schedule:Compact",
            "Sched",
            validate=False,
            data=[
                {"field": "Through: 12/31"},
                {"field": "For: AllDays"},
                {"field": "Until: 24:00"},
                {"field": "1.0"},
            ],
        )
        sched_obj = doc.get_collection("Schedule:Compact").get("Sched")
        result = values(sched_obj, year=2024, start_date=(1, 1), end_date=(1, 1), document=doc)
        assert len(result) == 24
        assert all(v == 1.0 for v in result)


class TestValuesScheduleFile:
    """Tests for values() with Schedule:File type (line 259)."""

    def test_values_schedule_file_cache_created(self) -> None:
        """Verify Schedule:File path in values() creates a cache (line 259)."""
        obj = MagicMock()
        obj.obj_type = "Schedule:File"

        def get_field(field: str) -> object:
            return {
                "File Name": "sched.csv",
                "Column Number": 1,
                "Rows to Skip at Top": 0,
                "Column Separator": "Comma",
                "Minutes per Item": 60,
                "Interpolate to Timestep": None,
            }.get(field)

        obj.get.side_effect = get_field
        del obj._document

        fs = MagicMock()
        fs.read_text.return_value = "\n".join(["0.5"] * 8784)

        result = values(
            obj,
            year=2024,
            start_date=(1, 1),
            end_date=(1, 1),
            fs=fs,
            base_path=Path("/base"),
        )
        assert len(result) == 24
        assert all(v == 0.5 for v in result)


class TestEvaluateWithInterpolation:
    """Tests for _evaluate_with_interpolation covering missing branches."""

    def test_day_list_with_interpolation(self) -> None:
        """Exercise Schedule:Day:List path in _evaluate_with_interpolation (line 301)."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Day:List"

        def get_field(field: str) -> object:
            fields: dict[str, object] = {
                "Minutes per Item": 60,
                "Interpolate to Timestep": None,
                "Value 1": 1.0,
                "Value 2": None,
            }
            return fields.get(field)

        obj.get.side_effect = get_field
        obj.data = {"extensions": _list_items(get_field)}
        del obj._document

        result = values(
            obj,
            year=2024,
            timestep=1,
            start_date=(1, 1),
            end_date=(1, 1),
            interpolation="no",
        )
        assert result[0] == 1.0

    def test_schedule_file_in_values_with_interpolation(self) -> None:
        """Exercise Schedule:File path in _evaluate_with_interpolation (line 305)."""
        obj = MagicMock()
        obj.obj_type = "Schedule:File"

        def get_field(field: str) -> object:
            return {
                "File Name": "sched.csv",
                "Column Number": 1,
                "Rows to Skip at Top": 0,
                "Column Separator": "Comma",
                "Minutes per Item": 60,
                "Interpolate to Timestep": None,
            }.get(field)

        obj.get.side_effect = get_field
        del obj._document

        fs = MagicMock()
        fs.read_text.return_value = "\n".join(["0.5"] * 8784)

        result = values(
            obj,
            year=2024,
            timestep=1,
            start_date=(1, 1),
            end_date=(1, 1),
            interpolation="average",
            fs=fs,
            base_path=Path("/base"),
        )
        assert len(result) == 24

    def test_week_schedule_requires_document_in_values(self) -> None:
        """Exercise document-required check in _evaluate_with_interpolation (lines 309-312)."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Week:Daily"
        del obj._document

        with pytest.raises(ScheduleReferenceError, match="Document required"):
            values(obj, year=2024, start_date=(1, 1), end_date=(1, 1))

    def test_week_compact_with_interpolation_in_values(self) -> None:
        """Exercise _eval_document_with_interp for Schedule:Week:Compact (line 337)."""
        doc = new_document()
        doc.add(
            "Schedule:Day:Interval",
            "DaySched",
            validate=False,
            data=[{"time": "24:00", "value_until_time": "0.6"}],
        )
        doc.add(
            "Schedule:Week:Compact",
            "WeekCompact",
            validate=False,
            data=[{"daytype_list": "AllDays", "schedule_day_name": "DaySched"}],
        )
        week_obj = doc.get_collection("Schedule:Week:Compact").get("WeekCompact")
        result = values(
            week_obj,
            year=2024,
            timestep=1,
            start_date=(1, 1),
            end_date=(1, 1),
            interpolation="average",
            document=doc,
        )
        assert len(result) == 24
        assert all(isinstance(v, float) for v in result)

    def test_year_schedule_with_interpolation_in_values(self) -> None:
        """Exercise _eval_document_with_interp for Schedule:Year (line 341)."""
        doc = new_document()
        doc.add(
            "Schedule:Day:Interval",
            "DaySched",
            validate=False,
            data=[{"time": "24:00", "value_until_time": "0.9"}],
        )
        doc.add(
            "Schedule:Week:Daily",
            "WeekSched",
            validate=False,
            sunday_schedule_day_name="DaySched",
            monday_schedule_day_name="DaySched",
            tuesday_schedule_day_name="DaySched",
            wednesday_schedule_day_name="DaySched",
            thursday_schedule_day_name="DaySched",
            friday_schedule_day_name="DaySched",
            saturday_schedule_day_name="DaySched",
            holiday_schedule_day_name="DaySched",
            summerdesignday_schedule_day_name="DaySched",
            winterdesignday_schedule_day_name="DaySched",
            customday1_schedule_day_name="DaySched",
            customday2_schedule_day_name="DaySched",
        )
        doc.add(
            "Schedule:Year",
            "YearSched",
            validate=False,
            schedule_weeks=[
                {
                    "schedule_week_name": "WeekSched",
                    "start_month": "1",
                    "start_day": "1",
                    "end_month": "12",
                    "end_day": "31",
                }
            ],
        )
        year_obj = doc.get_collection("Schedule:Year").get("YearSched")
        result = values(
            year_obj,
            year=2024,
            timestep=1,
            start_date=(1, 1),
            end_date=(1, 1),
            interpolation="average",
            document=doc,
        )
        assert len(result) == 24
        assert all(isinstance(v, float) for v in result)

    def test_average_in_values_is_mean_over_each_timestep(self) -> None:
        """values(interpolation="average") on a day schedule averages each timestep (#364)."""
        doc = new_document()
        doc.add(
            "Schedule:Day:Interval",
            "DaySched",
            validate=False,
            data=[{"time": "12:15", "value_until_time": "0"}, {"time": "24:00", "value_until_time": "1"}],
        )
        day_obj = doc.get_collection("Schedule:Day:Interval").get("DaySched")
        result = values(day_obj, year=2024, end_date=(1, 1), interpolation="average")
        assert result == [0.0] * 12 + [0.75] + [1.0] * 11

    def test_average_in_values_through_year_schedule(self) -> None:
        """The timestep length reaches a day schedule referenced through Year and Week."""
        doc = new_document()
        doc.add(
            "Schedule:Day:Interval",
            "DaySched",
            validate=False,
            data=[{"time": "12:15", "value_until_time": "0"}, {"time": "24:00", "value_until_time": "1"}],
        )
        day_fields = (
            "sunday",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "holiday",
            "summerdesignday",
            "winterdesignday",
            "customday1",
            "customday2",
        )
        doc.add(
            "Schedule:Week:Daily",
            "WeekSched",
            validate=False,
            **{f"{d}_schedule_day_name": "DaySched" for d in day_fields},
        )
        doc.add(
            "Schedule:Year",
            "YearSched",
            validate=False,
            schedule_weeks=[
                {"schedule_week_name": "WeekSched", "start_month": 1, "start_day": 1, "end_month": 12, "end_day": 31}
            ],
        )
        year_obj = doc.get_collection("Schedule:Year").get("YearSched")
        result = values(year_obj, year=2024, end_date=(1, 1), interpolation="average", document=doc)
        assert result[12] == pytest.approx(0.75)

    def test_day_interval_uses_its_own_interpolate_field(self) -> None:
        """A Schedule:Day:Interval set to Average averages without an interpolation= argument."""
        doc = new_document()
        day_obj = doc.add(
            "Schedule:Day:Interval",
            "DayAvg",
            validate=False,
            interpolate_to_timestep="Average",
            data=[{"time": "12:30", "value_until_time": "0"}, {"time": "24:00", "value_until_time": "1"}],
        )
        result = values(day_obj, year=2024, end_date=(1, 1))
        assert result[12] == pytest.approx(0.5)

    @pytest.mark.parametrize("timestep", [0, 7, 8, 45])
    def test_timestep_energyplus_cannot_run_is_refused(self, timestep: int) -> None:
        """EnergyPlus only runs timesteps that divide the hour; values() refuses the others."""
        doc = new_document()
        sched = doc.add("Schedule:Constant", "C", validate=False, hourly_value=1.0)
        with pytest.raises(ValueError, match="timestep"):
            values(sched, year=2024, timestep=timestep, end_date=(1, 1))

    def test_eval_document_with_interp_not_document_schedule_raises(self) -> None:
        """_eval_document_with_interp with unknown type raises ValueError (line 343)."""
        from idfkit.schedules.evaluate import _eval_document_with_interp  # pyright: ignore[reportPrivateUsage]

        obj = MagicMock()
        obj.obj_type = "Schedule:Unknown"
        doc = MagicMock()
        with pytest.raises(ValueError, match="Not a document schedule"):
            _eval_document_with_interp(
                obj, datetime(2024, 1, 1), doc, DayType.NORMAL, set(), set(), set(), Interpolation.NO
            )

    def test_week_daily_with_interpolation_in_values(self) -> None:
        """Exercise _eval_document_with_interp for Schedule:Week:Daily (line 333)."""
        doc = new_document()
        doc.add(
            "Schedule:Day:Interval",
            "DaySched",
            validate=False,
            data=[{"time": "24:00", "value_until_time": "0.4"}],
        )
        doc.add(
            "Schedule:Week:Daily",
            "WeekSched",
            validate=False,
            sunday_schedule_day_name="DaySched",
            monday_schedule_day_name="DaySched",
            tuesday_schedule_day_name="DaySched",
            wednesday_schedule_day_name="DaySched",
            thursday_schedule_day_name="DaySched",
            friday_schedule_day_name="DaySched",
            saturday_schedule_day_name="DaySched",
            holiday_schedule_day_name="DaySched",
            summerdesignday_schedule_day_name="DaySched",
            winterdesignday_schedule_day_name="DaySched",
            customday1_schedule_day_name="DaySched",
            customday2_schedule_day_name="DaySched",
        )
        week_obj = doc.get_collection("Schedule:Week:Daily").get("WeekSched")
        result = values(
            week_obj,
            year=2024,
            timestep=1,
            start_date=(1, 1),
            end_date=(1, 1),
            interpolation="average",
            document=doc,
        )
        assert len(result) == 24
        assert all(isinstance(v, float) for v in result)


def _compact(doc: IDFDocument[Literal[True]], name: str, fields: list[str]) -> None:
    doc.add("Schedule:Compact", name, validate=False, data=[{"field": f} for f in fields])


def _special_days_doc() -> IDFDocument[Literal[True]]:
    """A document with holidays, custom days and Schedule:Compact objects in every interpolation mode.

    ``Until:`` times fall inside timesteps (07:30, 10:15, 06:07, 13:20) so that Average and the last
    minute of a timestep differ, and Linear ramps cross timestep boundaries.
    """
    doc = new_document()
    specials = [
        ("NewYear", "January 1", 1, "Holiday"),
        ("MLK", "3rd Monday in January", 1, "Holiday"),
        ("Memorial", "Last Monday in May", 1, "Holiday"),
        ("Summer", "7/1", 3, "CustomDay1"),
        ("Audit", "1 October", 2, "CustomDay2"),
        ("Thanksgiving", "4th Thursday in November", 2, "Holiday"),
        ("Overlap", "11/28", 1, "CustomDay1"),
        ("Christmas", "December 25", 1, "Holiday"),
    ]
    for name, start, duration, kind in specials:
        doc.add(
            "RunPeriodControl:SpecialDays",
            name,
            start_date=start,
            duration=duration,
            special_day_type=kind,
            validate=False,
        )
    # Steps only, with a Through: halfway and every special day type.
    _compact(
        doc,
        "Mixed",
        [
            "Through: 6/30",
            "For: Weekdays SummerDesignDay",
            "Until: 07:30",
            "0.1",
            "Until: 18:00",
            "0.9",
            "Until: 24:00",
            "0.2",
            "For: Holiday",
            "Until: 24:00",
            "0.05",
            "For: CustomDay1 CustomDay2",
            "Until: 12:00",
            "0.4",
            "Until: 24:00",
            "0.6",
            "For: AllOtherDays",
            "Until: 24:00",
            "0.3",
            "Through: 12/31",
            "For: Saturday",
            "Until: 10:15",
            "0.25",
            "Until: 24:00",
            "0.75",
            "For: CustomDay2",
            "Until: 24:00",
            "0.66",
            "For: Holiday CustomDay1",
            "Until: 24:00",
            "0.01",
            "For: AllOtherDays",
            "Until: 08:00",
            "-0.0",
            "Until: 17:00",
            "1.0",
            "Until: 24:00",
            "0.5",
        ],
    )
    # One block per interpolation mode, with special days on their own blocks.
    _compact(
        doc,
        "Modes",
        [
            "Through: 12/31",
            "For: Holiday",
            "Interpolate: Linear",
            "Until: 06:07",
            "0.0",
            "Until: 13:20",
            "1.0",
            "Until: 24:00",
            "0.0",
            "For: CustomDay1",
            "Interpolate: Average",
            "Until: 06:07",
            "0.2",
            "Until: 10:15",
            "0.7",
            "Until: 24:00",
            "0.1",
            "For: Weekdays",
            "Interpolate: Average",
            "Until: 07:30",
            "0.1",
            "Until: 13:20",
            "0.95",
            "Until: 17:45",
            "0.333",
            "Until: 24:00",
            "0.0",
            "For: Saturday",
            "Interpolate: Linear",
            "Until: 06:00",
            "0.0",
            "Until: 18:00",
            "1.0",
            "Until: 24:00",
            "-0.0",
            "For: AllOtherDays",
            "Interpolate: No",
            "Until: 06:07",
            "0.3",
            "Until: 24:00",
            "0.6",
        ],
    )
    # Interpolate: before the first For: applies to that block only.
    _compact(
        doc,
        "Leading",
        [
            "Through: 12/31",
            "Interpolate: Yes",
            "For: Weekdays",
            "Until: 08:10",
            "0.15",
            "Until: 24:00",
            "0.85",
            "For: AllOtherDays",
            "Until: 08:10",
            "0.4",
            "Until: 24:00",
            "0.2",
        ],
    )
    return doc


def _per_timestep(
    schedule: IDFObject,
    doc: IDFDocument[Literal[True]],
    year: int,
    timestep: int,
    start_date: tuple[int, int],
    end_date: tuple[int, int],
    day_type: DayTypeInput | None,
) -> list[float]:
    """values() computed the slow way: one evaluate_compact() call per timestep, as values() did."""
    holidays = get_holidays(doc, year)
    custom_day_1 = get_special_days_by_type(doc, year, "CustomDay1")
    custom_day_2 = get_special_days_by_type(doc, year, "CustomDay2")
    minutes = 60 // timestep
    current = datetime(year, *start_date, 0, 0)
    end = datetime(year, *end_date, 23, 59)
    result: list[float] = []
    while current <= end:
        result.append(
            evaluate_compact(
                schedule,
                current,
                parse_day_type(day_type),
                holidays,
                custom_day_1,
                custom_day_2,
                interval_minutes=minutes,
            )
        )
        current += timedelta(minutes=minutes)
    return result


class TestCompactValuesMatchPerTimestep:
    """values() on a Schedule:Compact must equal a per-timestep evaluation, special days included."""

    @pytest.mark.parametrize("name", ["Mixed", "Modes", "Leading"])
    @pytest.mark.parametrize(
        ("year", "timestep", "start_date", "end_date", "day_type"),
        [
            (2024, 1, (1, 1), (12, 31), None),
            (2023, 1, (1, 1), (12, 31), None),
            (2009, 4, (1, 1), (12, 31), None),
            (2024, 3, (2, 20), (3, 5), None),
            (2024, 6, (6, 25), (7, 10), None),
            (2024, 12, (5, 20), (7, 5), None),
            (2024, 60, (11, 25), (11, 30), None),
            (2024, 2, (1, 1), (1, 31), "summer"),
            (2024, 4, (1, 1), (1, 10), "winter"),
            (2024, 1, (1, 1), (1, 31), "holiday"),
            (2024, 4, (6, 25), (7, 10), "customday1"),
            (2024, 10, (9, 28), (10, 5), "customday2"),
        ],
    )
    def test_bit_identical(
        self,
        name: str,
        year: int,
        timestep: int,
        start_date: tuple[int, int],
        end_date: tuple[int, int],
        day_type: DayTypeInput | None,
    ) -> None:
        doc = _special_days_doc()
        schedule = doc.get_collection("Schedule:Compact").get(name)
        assert schedule is not None
        fast = values(
            schedule,
            year=year,
            timestep=timestep,
            start_date=start_date,
            end_date=end_date,
            document=doc,
            day_type=day_type,
        )
        slow = _per_timestep(schedule, doc, year, timestep, start_date, end_date, day_type)
        assert fast == slow
        assert [math.copysign(1.0, v) for v in fast] == [math.copysign(1.0, v) for v in slow]

    def test_fixture_exercises_every_mode(self) -> None:
        """The comparison above is not vacuous: special days, Average and Linear all change values."""
        doc = _special_days_doc()
        schedule = doc.get_collection("Schedule:Compact").get("Modes")
        assert schedule is not None
        with_specials = values(schedule, year=2024, timestep=4, document=doc)
        # Weekday Average: 13:20 falls inside the 13:15 timestep, which averages 0.95 and 0.333.
        weekday = (date(2024, 1, 3) - date(2024, 1, 1)).days * 96
        assert 0.333 < with_specials[weekday + 53] < 0.95
        # Saturday Linear: the ramp passes through values between its ends.
        saturday = (date(2024, 1, 6) - date(2024, 1, 1)).days * 96
        assert 0.0 < with_specials[saturday + 40] < 1.0
        for obj in list(doc["RunPeriodControl:SpecialDays"]):
            doc.removeidfobject(obj)
        assert with_specials != values(schedule, year=2024, timestep=4, document=doc)

    def test_empty_range(self) -> None:
        """An end date before the start date gives no values, without evaluating the schedule."""
        doc = new_document()
        _compact(doc, "Short", ["Through: 6/30", "For: AllDays", "Until: 24:00", "1.0"])
        schedule = doc.get_collection("Schedule:Compact").get("Short")
        assert schedule is not None
        assert values(schedule, year=2024, start_date=(3, 2), end_date=(3, 1), document=doc) == []

    @pytest.mark.parametrize("minutes", [0, -15, 7, 45, 120])
    def test_compact_range_rejects_step_that_does_not_divide_the_hour(self, minutes: int) -> None:
        doc = _special_days_doc()
        schedule = doc.get_collection("Schedule:Compact").get("Mixed")
        assert schedule is not None
        with pytest.raises(ValueError, match="must divide the hour"):
            evaluate_compact_range(schedule, date(2024, 1, 1), date(2024, 1, 2), minutes)

    def test_malformed_compact_raises_in_values(self) -> None:
        """A schedule EnergyPlus would refuse still raises MalformedScheduleError from values()."""
        doc = new_document()
        _compact(doc, "Short", ["Through: 6/30", "For: AllDays", "Until: 24:00", "1.0"])
        schedule = doc.get_collection("Schedule:Compact").get("Short")
        assert schedule is not None
        with pytest.raises(MalformedScheduleError, match="Error evaluating Schedule:Compact"):
            values(schedule, year=2024, document=doc)
