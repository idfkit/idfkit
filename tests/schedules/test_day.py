"""Tests for schedules.day module."""

from __future__ import annotations

from datetime import datetime, time
from unittest.mock import MagicMock

import pytest

from idfkit.schedules.day import (
    _parse_time,
    evaluate_constant,
    evaluate_day_hourly,
    evaluate_day_interval,
    evaluate_day_list,
    get_day_values,
)
from idfkit.schedules.time_utils import time_to_minutes
from idfkit.schedules.types import Interpolation


class TestParseTime:
    """Tests for _parse_time function."""

    def test_hh_mm(self) -> None:
        """Test HH:MM format."""
        assert _parse_time("08:00") == time(8, 0)
        assert _parse_time("18:30") == time(18, 30)

    def test_h_mm(self) -> None:
        """Test H:MM format."""
        assert _parse_time("8:00") == time(8, 0)

    def test_hh_mm_ss(self) -> None:
        """Test HH:MM:SS format."""
        assert _parse_time("08:30:15") == time(8, 30, 15)

    def test_hour_only(self) -> None:
        """Test hour-only format."""
        assert _parse_time("8") == time(8, 0)
        assert _parse_time("18") == time(18, 0)

    def test_24_00(self) -> None:
        """Test 24:00 as end of day."""
        t = _parse_time("24:00")
        assert t.hour == 23
        assert t.minute == 59
        assert t.second == 59

    def test_whitespace(self) -> None:
        """Test handling of whitespace."""
        assert _parse_time("  08:00  ") == time(8, 0)

    def test_invalid(self) -> None:
        """Test invalid time format."""
        with pytest.raises(ValueError, match="Cannot parse time"):
            _parse_time("invalid")


class TestTimeToMinutes:
    """Tests for _time_to_minutes function."""

    def test_midnight(self) -> None:
        """Test midnight conversion."""
        assert time_to_minutes(time(0, 0)) == 0.0

    def test_noon(self) -> None:
        """Test noon conversion."""
        assert time_to_minutes(time(12, 0)) == 720.0

    def test_with_minutes(self) -> None:
        """Test time with minutes."""
        assert time_to_minutes(time(8, 30)) == 510.0

    def test_with_seconds(self) -> None:
        """Test time with seconds."""
        assert time_to_minutes(time(8, 0, 30)) == 480.5


class TestEvaluateConstant:
    """Tests for evaluate_constant function."""

    def test_evaluate(self) -> None:
        """Test evaluating a constant schedule."""
        obj = MagicMock()
        obj.get.return_value = 0.5

        result = evaluate_constant(obj, datetime(2024, 1, 1, 10, 0))
        assert result == 0.5

    def test_missing_value(self) -> None:
        """Test missing value defaults to 0."""
        obj = MagicMock()
        obj.get.return_value = None

        result = evaluate_constant(obj, datetime(2024, 1, 1, 10, 0))
        assert result == 0.0


class TestEvaluateDayHourly:
    """Tests for evaluate_day_hourly function."""

    def test_evaluate_hours(self) -> None:
        """Test evaluating different hours."""
        obj = MagicMock()

        def get_hour(field: str) -> float | None:
            hour_values = {f"Hour {i}": float(i) / 24 for i in range(1, 25)}
            return hour_values.get(field)

        obj.get.side_effect = get_hour

        # Hour 0 -> Field "Hour 1"
        assert evaluate_day_hourly(obj, datetime(2024, 1, 1, 0, 0)) == 1 / 24
        # Hour 12 -> Field "Hour 13"
        assert evaluate_day_hourly(obj, datetime(2024, 1, 1, 12, 0)) == 13 / 24
        # Hour 23 -> Field "Hour 24"
        assert evaluate_day_hourly(obj, datetime(2024, 1, 1, 23, 0)) == 24 / 24


class TestEvaluateDayInterval:
    """Tests for evaluate_day_interval function."""

    @pytest.fixture
    def interval_schedule(self) -> MagicMock:
        """Create a mock interval schedule."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Day:Interval"

        def get_field(field: str) -> str | float | None:
            fields = {
                "Time 1": "08:00",
                "Value Until Time 1": 0.0,
                "Time 2": "18:00",
                "Value Until Time 2": 1.0,
                "Time 3": "24:00",
                "Value Until Time 3": 0.0,
            }
            return fields.get(field)

        obj.get.side_effect = get_field
        return obj

    def test_before_first_interval(self, interval_schedule: MagicMock) -> None:
        """Test time before first interval."""
        # Before 8am -> value is 0.0
        result = evaluate_day_interval(interval_schedule, datetime(2024, 1, 1, 6, 0))
        assert result == 0.0

    def test_during_occupied(self, interval_schedule: MagicMock) -> None:
        """Test time during occupied period."""
        # Between 8am and 6pm -> value is 1.0
        result = evaluate_day_interval(interval_schedule, datetime(2024, 1, 1, 12, 0))
        assert result == 1.0

    def test_after_occupied(self, interval_schedule: MagicMock) -> None:
        """Test time after occupied period."""
        # After 6pm -> value is 0.0
        result = evaluate_day_interval(interval_schedule, datetime(2024, 1, 1, 20, 0))
        assert result == 0.0

    def test_interpolation(self, interval_schedule: MagicMock) -> None:
        """Test interpolation between values."""
        # At 8am boundary with interpolation
        result = evaluate_day_interval(interval_schedule, datetime(2024, 1, 1, 8, 0), Interpolation.AVERAGE)
        # At exactly 8:00, should be interpolated
        assert 0.0 <= result <= 1.0


class TestEvaluateDayList:
    """Tests for evaluate_day_list function."""

    @pytest.fixture
    def list_schedule(self) -> MagicMock:
        """Create a mock list schedule with 24 hourly values."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Day:List"

        def get_field(field: str) -> int | float | None:
            # 24 values, one per hour
            if field == "Minutes per Item":
                return 60
            if field == "Interpolate to Timestep":
                return None
            if field.startswith("Value "):
                try:
                    idx = int(field.split()[1])
                    if 1 <= idx <= 24:
                        # Simple pattern: 0 for hours 0-7, 1 for hours 8-17, 0 for hours 18-23
                        hour = idx - 1
                        return 1.0 if 8 <= hour < 18 else 0.0
                except (ValueError, IndexError):
                    pass
            return None

        obj.get.side_effect = get_field
        return obj

    def test_evaluate(self, list_schedule: MagicMock) -> None:
        """Test evaluating list schedule."""
        # Early morning
        assert evaluate_day_list(list_schedule, datetime(2024, 1, 1, 6, 0)) == 0.0
        # During work hours
        assert evaluate_day_list(list_schedule, datetime(2024, 1, 1, 12, 0)) == 1.0
        # Evening
        assert evaluate_day_list(list_schedule, datetime(2024, 1, 1, 20, 0)) == 0.0


class TestGetDayValues:
    """Tests for get_day_values function."""

    def test_constant_schedule(self) -> None:
        """Test getting values for constant schedule."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Constant"
        obj.get.return_value = 0.5

        values = get_day_values(obj, timestep=1)
        assert len(values) == 24
        assert all(v == 0.5 for v in values)

    def test_sub_hourly_timestep(self) -> None:
        """Test sub-hourly timestep."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Constant"
        obj.get.return_value = 0.5

        values = get_day_values(obj, timestep=4)
        assert len(values) == 96  # 24 hours * 4 values per hour

    def test_unsupported_type(self) -> None:
        """Test unsupported schedule type."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Unknown"

        with pytest.raises(ValueError, match="Unsupported day schedule type"):
            get_day_values(obj)


class TestTimeOrdering:
    """Tests for time ordering validation in interval schedules."""

    def test_descending_times_raises_value_error(self) -> None:
        """Test that descending times raise ValueError."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Day:Interval"

        def get_field(field: str) -> str | float | None:
            fields = {
                "Time 1": "18:00",
                "Value Until Time 1": 1.0,
                "Time 2": "08:00",  # Descending — invalid
                "Value Until Time 2": 0.0,
            }
            return fields.get(field)

        obj.get.side_effect = get_field

        with pytest.raises(ValueError, match="ascending order"):
            evaluate_day_interval(obj, datetime(2024, 1, 1, 12, 0))


class TestMidnightBoundary:
    """Tests for midnight boundary behavior."""

    def test_evaluation_at_2359(self) -> None:
        """Test evaluation just before midnight."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Day:Interval"

        def get_field(field: str) -> str | float | None:
            fields = {
                "Time 1": "08:00",
                "Value Until Time 1": 0.0,
                "Time 2": "18:00",
                "Value Until Time 2": 1.0,
                "Time 3": "24:00",
                "Value Until Time 3": 0.5,
            }
            return fields.get(field)

        obj.get.side_effect = get_field

        # At 23:59 should be in the third interval (value 0.5)
        result = evaluate_day_interval(obj, datetime(2024, 1, 1, 23, 59))
        assert result == 0.5

    def test_evaluation_at_0000(self) -> None:
        """Test evaluation at midnight (start of day)."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Day:Interval"

        def get_field(field: str) -> str | float | None:
            fields = {
                "Time 1": "08:00",
                "Value Until Time 1": 0.0,
                "Time 2": "24:00",
                "Value Until Time 2": 1.0,
            }
            return fields.get(field)

        obj.get.side_effect = get_field

        # At 00:00 should be in the first interval (value 0.0)
        result = evaluate_day_interval(obj, datetime(2024, 1, 1, 0, 0))
        assert result == 0.0


class TestLeapYear:
    """Tests for leap year behavior."""

    def test_feb_29_evaluation(self) -> None:
        """Test evaluation on Feb 29 in a leap year."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Constant"
        obj.get.return_value = 0.75

        # Feb 29, 2024 (leap year)
        result = evaluate_constant(obj, datetime(2024, 2, 29, 12, 0))
        assert result == 0.75
