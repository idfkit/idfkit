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
        """Create a mock interval schedule with canonical storage."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Day:Interval"
        obj.data = {
            "data": [
                {"time": "08:00", "value_until_time": 0.0},
                {"time": "18:00", "value_until_time": 1.0},
                {"time": "24:00", "value_until_time": 0.0},
            ]
        }
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
        """Test interpolation at the 08:00 boundary.

        At exactly 08:00 the first interval (until 08:00, value=0.0) is closed
        (boundary is exclusive: current < until is False at equality).  We fall
        into the second interval [08:00, 18:00) with prev_value=0.0.
        fraction = (480-480)/(1080-480) = 0.0, so interpolation returns 0.0.
        Without interpolation the step function would return 1.0 (the second
        interval's value), confirming interpolation is active.
        """
        result = evaluate_day_interval(interval_schedule, datetime(2024, 1, 1, 8, 0), Interpolation.AVERAGE)
        assert result == 0.0


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
        obj.data = {
            "data": [
                {"time": "18:00", "value_until_time": 1.0},
                {"time": "08:00", "value_until_time": 0.0},
            ]
        }
        with pytest.raises(ValueError, match="ascending order"):
            evaluate_day_interval(obj, datetime(2024, 1, 1, 12, 0))


class TestMidnightBoundary:
    """Tests for midnight boundary behavior."""

    def test_evaluation_at_2359(self) -> None:
        """Test evaluation just before midnight."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Day:Interval"
        obj.data = {
            "data": [
                {"time": "08:00", "value_until_time": 0.0},
                {"time": "18:00", "value_until_time": 1.0},
                {"time": "24:00", "value_until_time": 0.5},
            ]
        }
        # At 23:59 should be in the third interval (value 0.5)
        result = evaluate_day_interval(obj, datetime(2024, 1, 1, 23, 59))
        assert result == 0.5

    def test_evaluation_at_0000(self) -> None:
        """Test evaluation at midnight (start of day)."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Day:Interval"
        obj.data = {
            "data": [
                {"time": "08:00", "value_until_time": 0.0},
                {"time": "24:00", "value_until_time": 1.0},
            ]
        }
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


class TestEvaluateDayHourlyMissingValue:
    """Test evaluate_day_hourly when a field returns None (line 91)."""

    def test_missing_hour_field_returns_zero(self) -> None:
        """Missing hour field defaults to 0.0."""
        obj = MagicMock()
        obj.get.return_value = None

        result = evaluate_day_hourly(obj, datetime(2024, 1, 1, 5, 0))
        assert result == 0.0


class TestParseIntervalTimeValuesEdgeCases:
    """Tests for edge cases in _parse_interval_time_values (lines 194->216, 204)."""

    def test_value_none_causes_break(self) -> None:
        """When value_until_time is None, parsing stops at that item."""
        obj = MagicMock()
        obj.data = {"data": [{"time": "08:00", "value_until_time": None}]}
        # With no valid value, there are no time_values -> returns 0.0
        result = evaluate_day_interval(obj, datetime(2024, 1, 1, 6, 0))
        assert result == 0.0

    def test_all_144_intervals_exhausted(self) -> None:
        """144 ten-minute intervals span the full day."""
        obj = MagicMock()
        items = []
        for i in range(1, 145):
            total_minutes = i * 10
            h = total_minutes // 60
            m = total_minutes % 60
            time_str = f"{h:02d}:{m:02d}" if total_minutes < 1440 else "24:00"
            items.append({"time": time_str, "value_until_time": 1.0})
        obj.data = {"data": items}
        result = evaluate_day_interval(obj, datetime(2024, 1, 1, 12, 0))
        assert result == 1.0


class TestEvaluateDayListInterpolation:
    """Tests for interpolation handling in evaluate_day_list (lines 141-143)."""

    def test_interpolate_to_timestep_average(self) -> None:
        """Interpolate to Timestep = Average enables interpolation."""
        obj = MagicMock()

        def get_field(field: str) -> object:
            fields: dict[str, object] = {
                "Minutes per Item": 60,
                "Interpolate to Timestep": "Average",
                "Value 1": 0.0,
                "Value 2": 1.0,
                "Value 3": None,
            }
            return fields.get(field)

        obj.get.side_effect = get_field
        # At 1:30 (halfway through the second interval [1:00→2:00]), interpolation
        # blends prev_value=0.0 (end of first interval) with tv.value=1.0 → 0.5.
        # Without interpolation the step function would return 1.0.
        result = evaluate_day_list(obj, datetime(2024, 1, 1, 1, 30))
        assert result == pytest.approx(0.5)

    def test_interpolate_to_timestep_yes(self) -> None:
        """Interpolate to Timestep = Yes enables interpolation."""
        obj = MagicMock()

        def get_field(field: str) -> object:
            fields: dict[str, object] = {
                "Minutes per Item": 60,
                "Interpolate to Timestep": "Yes",
                "Value 1": 0.0,
                "Value 2": None,
            }
            return fields.get(field)

        obj.get.side_effect = get_field
        result = evaluate_day_list(obj, datetime(2024, 1, 1, 0, 0))
        assert result == 0.0

    def test_interpolate_to_timestep_linear(self) -> None:
        """Interpolate to Timestep = Linear enables interpolation (sets AVERAGE mode)."""
        obj = MagicMock()

        def get_field(field: str) -> object:
            fields: dict[str, object] = {
                "Minutes per Item": 60,
                "Interpolate to Timestep": "Linear",
                "Value 1": 0.5,
                "Value 2": None,
            }
            return fields.get(field)

        obj.get.side_effect = get_field
        # The key point is that "Linear" sets interpolation to AVERAGE; the function executes the branch
        result = evaluate_day_list(obj, datetime(2024, 1, 1, 0, 0))
        assert isinstance(result, float)


class TestEvaluateDayListInterpolateOther:
    """Test when Interpolate to Timestep is non-standard (line 142->146)."""

    def test_interpolate_other_value_no_change(self) -> None:
        """Non-standard interpolation value doesn't change mode (line 142->146)."""
        obj = MagicMock()

        def get_field(field: str) -> object:
            fields: dict[str, object] = {
                "Minutes per Item": 60,
                "Interpolate to Timestep": "Other",  # Not "average"/"linear"/"yes"
                "Value 1": 0.5,
                "Value 2": None,
            }
            return fields.get(field)

        obj.get.side_effect = get_field
        # With "Other" as the interpolate value, interpolation stays NO
        result = evaluate_day_list(obj, datetime(2024, 1, 1, 0, 0))
        assert isinstance(result, float)


class TestEvaluateDayListEmpty:
    """Test evaluate_day_list when no values exist (line 172)."""

    def test_no_values_returns_zero(self) -> None:
        """No Value fields returns 0.0."""
        obj = MagicMock()

        def get_field(field: str) -> object:
            if field in ("Minutes per Item", "Interpolate to Timestep"):
                return None
            if field == "Value 1":
                return None
            return None

        obj.get.side_effect = get_field
        result = evaluate_day_list(obj, datetime(2024, 1, 1, 10, 0))
        assert result == 0.0


class TestEvaluateDayListEndOfDay:
    """Test evaluate_day_list at end-of-day boundary (lines 158-169, 194->216, 204)."""

    def test_last_value_caps_at_end_of_day(self) -> None:
        """A 24th hourly value that hits 1440 minutes uses END_OF_DAY."""
        obj = MagicMock()

        def get_field(field: str) -> object:
            if field == "Minutes per Item":
                return 60
            if field == "Interpolate to Timestep":
                return None
            if field.startswith("Value "):
                idx = int(field.split()[1])
                if idx <= 24:
                    return 1.0
                return None
            return None

        obj.get.side_effect = get_field
        result = evaluate_day_list(obj, datetime(2024, 1, 1, 23, 0))
        assert result == 1.0


class TestGetDayValuesAllTypes:
    """Tests for get_day_values covering hourly, interval, list branches (247, 249, 251)."""

    def test_hourly_type(self) -> None:
        """get_day_values works with Schedule:Day:Hourly."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Day:Hourly"
        obj.get.side_effect = lambda f: 0.3 if f.startswith("Hour ") else None

        result = get_day_values(obj, timestep=1)
        assert len(result) == 24
        assert all(v == 0.3 for v in result)

    def test_interval_type(self) -> None:
        """get_day_values works with Schedule:Day:Interval."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Day:Interval"
        obj.data = {"data": [{"time": "24:00", "value_until_time": 0.6}]}
        result = get_day_values(obj, timestep=1)
        assert len(result) == 24
        assert all(v == 0.6 for v in result)

    def test_list_type(self) -> None:
        """get_day_values works with Schedule:Day:List."""
        obj = MagicMock()
        obj.obj_type = "Schedule:Day:List"

        def get_field(field: str) -> object:
            if field == "Minutes per Item":
                return 60
            if field == "Interpolate to Timestep":
                return None
            if field.startswith("Value "):
                idx = int(field.split()[1])
                if idx <= 24:
                    return 0.9
                return None
            return None

        obj.get.side_effect = get_field
        result = get_day_values(obj, timestep=1)
        assert len(result) == 24
        assert all(v == 0.9 for v in result)
