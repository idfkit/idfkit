"""Tests for schedules.time_utils module."""

from __future__ import annotations

from datetime import time

from idfkit.schedules.time_utils import END_OF_DAY, END_OF_DAY_MINUTES, evaluate_time_values, time_to_minutes
from idfkit.schedules.types import Interpolation, TimeValue


class TestTimeToMinutes:
    """Tests for time_to_minutes function."""

    def test_midnight(self) -> None:
        """Test midnight returns 0."""
        assert time_to_minutes(time(0, 0)) == 0.0

    def test_noon(self) -> None:
        """Test noon returns 720."""
        assert time_to_minutes(time(12, 0)) == 720.0

    def test_with_minutes(self) -> None:
        """Test time with minutes."""
        assert time_to_minutes(time(8, 30)) == 510.0

    def test_with_seconds(self) -> None:
        """Test time with seconds."""
        assert time_to_minutes(time(8, 0, 30)) == 480.5

    def test_end_of_day_sentinel_returns_exactly_1440(self) -> None:
        """Test END_OF_DAY sentinel returns exactly 1440.0."""
        result = time_to_minutes(END_OF_DAY)
        assert result == END_OF_DAY_MINUTES
        assert result == 1440.0

    def test_end_of_day_is_exact(self) -> None:
        """Test END_OF_DAY produces exact value, not floating-point approximation."""
        # Without sentinel detection, time(23, 59, 59, 999999) would give
        # 1439.999... due to floating-point arithmetic
        result = time_to_minutes(END_OF_DAY)
        assert result == 1440.0
        assert isinstance(result, float)


class TestEvaluateTimeValues:
    """Tests for evaluate_time_values function."""

    def test_empty_returns_zero(self) -> None:
        """Test empty time_values returns 0.0."""
        result = evaluate_time_values([], time(12, 0), Interpolation.NO)
        assert result == 0.0

    def test_step_function(self) -> None:
        """Test step function (no interpolation)."""
        time_values = [
            TimeValue(until_time=time(8, 0), value=0.0),
            TimeValue(until_time=time(18, 0), value=1.0),
            TimeValue(until_time=END_OF_DAY, value=0.0),
        ]

        # Before first interval
        assert evaluate_time_values(time_values, time(6, 0), Interpolation.NO) == 0.0
        # During second interval
        assert evaluate_time_values(time_values, time(12, 0), Interpolation.NO) == 1.0
        # During third interval
        assert evaluate_time_values(time_values, time(20, 0), Interpolation.NO) == 0.0

    def test_at_exact_boundary(self) -> None:
        """Test evaluation at exact boundary transitions to next interval."""
        time_values = [
            TimeValue(until_time=time(8, 0), value=0.0),
            TimeValue(until_time=END_OF_DAY, value=1.0),
        ]

        # At exactly 8:00, should be in the second interval (value 1.0)
        assert evaluate_time_values(time_values, time(8, 0), Interpolation.NO) == 1.0

    def test_interpolation_midpoint(self) -> None:
        """Test linear interpolation at midpoint."""
        time_values = [
            TimeValue(until_time=time(12, 0), value=0.0),
            TimeValue(until_time=END_OF_DAY, value=1.0),
        ]

        # At 6:00 (halfway through first interval 0-12), interpolating from 0 to 0 = 0
        result = evaluate_time_values(time_values, time(6, 0), Interpolation.AVERAGE)
        assert result == 0.0  # prev_value=0.0, tv.value=0.0, so interpolated is 0.0

    def test_past_all_intervals_returns_last_value(self) -> None:
        """Test that time past all intervals returns last value."""
        time_values = [
            TimeValue(until_time=time(12, 0), value=0.5),
        ]

        # 13:00 is past the only interval
        result = evaluate_time_values(time_values, time(13, 0), Interpolation.NO)
        assert result == 0.5
