"""Tests for schedules.evaluate module."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from idfkit import new_document
from idfkit.objects import IDFObject
from idfkit.schedules.evaluate import (
    MalformedScheduleError,
    ScheduleEvaluationError,
    ScheduleReferenceError,
    UnsupportedScheduleType,
    evaluate,
    values,
)
from idfkit.schedules.types import DayType, Interpolation


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

        def get_field(field: str) -> str | float | None:
            fields = {
                "Time 1": "12:00",
                "Value Until Time 1": 0.0,
                "Time 2": "24:00",
                "Value Until Time 2": 1.0,
            }
            return fields.get(field)

        obj.get.side_effect = get_field
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
            field_1="Through: 12/31",
            field_2="For: Weekdays",
            field_3="Until: 08:00",
            field_4="0.0",
            field_5="Until: 18:00",
            field_6="1.0",
            field_7="Until: 24:00",
            field_8="0.0",
            field_9="For: AllOtherDays",
            field_10="Until: 24:00",
            field_11="0.0",
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

        def get_field(field: str) -> str | float | None:
            # Return non-numeric value for a numeric field
            fields: dict[str, str | float] = {
                "Time 1": "08:00",
                "Value Until Time 1": "not_a_number",
            }
            return fields.get(field)

        obj.get.side_effect = get_field
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
        doc.add("Schedule:Day:Interval", "DaySched", validate=False, time_1="24:00", value_until_time_1="0.5")
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
        doc.add("Schedule:Day:Interval", "DaySched", validate=False, time_1="24:00", value_until_time_1="0.3")
        doc.add(
            "Schedule:Week:Compact",
            "WeekCompact",
            validate=False,
            daytype_list_1="AllDays",
            schedule_day_name_1="DaySched",
        )
        week_obj = doc.get_collection("Schedule:Week:Compact").get("WeekCompact")
        result = evaluate(week_obj, datetime(2024, 1, 8, 12, 0), document=doc)
        assert result == 0.3

    def test_eval_document_year(self) -> None:
        """Exercise Schedule:Year through evaluate() (line 186)."""
        doc = new_document()
        doc.add("Schedule:Day:Interval", "DaySched", validate=False, time_1="24:00", value_until_time_1="0.8")
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
            schedule_week_name="WeekSched",
            start_month="1",
            start_day="1",
            end_month="12",
            end_day="31",
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
            field_1="Through: 12/31",
            field_2="For: AllDays",
            field_3="Until: 24:00",
            field_4="1.0",
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
        doc.add("Schedule:Day:Interval", "DaySched", validate=False, time_1="24:00", value_until_time_1="0.6")
        doc.add(
            "Schedule:Week:Compact",
            "WeekCompact",
            validate=False,
            daytype_list_1="AllDays",
            schedule_day_name_1="DaySched",
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
        doc.add("Schedule:Day:Interval", "DaySched", validate=False, time_1="24:00", value_until_time_1="0.9")
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
            schedule_week_name="WeekSched",
            start_month="1",
            start_day="1",
            end_month="12",
            end_day="31",
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
        doc.add("Schedule:Day:Interval", "DaySched", validate=False, time_1="24:00", value_until_time_1="0.4")
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
