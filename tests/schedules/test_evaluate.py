"""Tests for schedules.evaluate module."""

from __future__ import annotations

from datetime import datetime
from unittest.mock import MagicMock

import pytest

from idfkit.schedules.evaluate import (
    MalformedScheduleError,
    ScheduleEvaluationError,
    ScheduleReferenceError,
    UnsupportedScheduleType,
    evaluate,
    values,
)
from idfkit.schedules.types import Interpolation


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
    def compact_office_schedule(self) -> MagicMock:
        """Create a realistic office schedule."""
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
            "Field 9": "For: AllOtherDays",
            "Field 10": "Until: 24:00",
            "Field 11": "0.0",
        }

        def get_field(name: str) -> str | None:
            return fields.get(name)

        obj.get.side_effect = get_field
        del obj._document
        return obj

    def test_office_schedule_weekday_pattern(self, compact_office_schedule: MagicMock) -> None:
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

    def test_office_schedule_weekend_pattern(self, compact_office_schedule: MagicMock) -> None:
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

    def test_office_schedule_week_sum(self, compact_office_schedule: MagicMock) -> None:
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
