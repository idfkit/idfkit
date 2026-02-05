"""Tests for schedules.types module."""

from __future__ import annotations

from datetime import date, time

import pytest

from idfkit.schedules.types import (
    WEEKDAY_TO_DAY_TYPE,
    CompactDayRule,
    CompactPeriod,
    DayType,
    Interpolation,
    SpecialDay,
    TimeValue,
    parse_day_type,
    parse_interpolation,
)


class TestDayType:
    """Tests for DayType enum."""

    def test_values(self) -> None:
        """Test DayType enum values."""
        assert DayType.NORMAL.value == "normal"
        assert DayType.SUMMER_DESIGN.value == "summer"
        assert DayType.WINTER_DESIGN.value == "winter"
        assert DayType.HOLIDAY.value == "holiday"

    def test_all_day_types_exist(self) -> None:
        """Test all expected day types exist."""
        assert hasattr(DayType, "NORMAL")
        assert hasattr(DayType, "SUMMER_DESIGN")
        assert hasattr(DayType, "WINTER_DESIGN")
        assert hasattr(DayType, "HOLIDAY")
        assert hasattr(DayType, "CUSTOM_DAY_1")
        assert hasattr(DayType, "CUSTOM_DAY_2")


class TestInterpolation:
    """Tests for Interpolation enum."""

    def test_values(self) -> None:
        """Test Interpolation enum values."""
        assert Interpolation.NO.value == "no"
        assert Interpolation.AVERAGE.value == "average"
        assert Interpolation.LINEAR.value == "linear"


class TestSpecialDay:
    """Tests for SpecialDay dataclass."""

    def test_create(self) -> None:
        """Test creating a SpecialDay."""
        sd = SpecialDay(
            name="Christmas",
            start_date=date(2024, 12, 25),
            duration=1,
            day_type="Holiday",
        )
        assert sd.name == "Christmas"
        assert sd.start_date == date(2024, 12, 25)
        assert sd.duration == 1
        assert sd.day_type == "Holiday"

    def test_contains_single_day(self) -> None:
        """Test contains() for single-day special day."""
        sd = SpecialDay(
            name="Christmas",
            start_date=date(2024, 12, 25),
            duration=1,
            day_type="Holiday",
        )
        assert sd.contains(date(2024, 12, 25))
        assert not sd.contains(date(2024, 12, 24))
        assert not sd.contains(date(2024, 12, 26))

    def test_contains_multi_day(self) -> None:
        """Test contains() for multi-day special day."""
        sd = SpecialDay(
            name="Christmas Break",
            start_date=date(2024, 12, 24),
            duration=3,
            day_type="Holiday",
        )
        assert sd.contains(date(2024, 12, 24))
        assert sd.contains(date(2024, 12, 25))
        assert sd.contains(date(2024, 12, 26))
        assert not sd.contains(date(2024, 12, 23))
        assert not sd.contains(date(2024, 12, 27))

    def test_frozen(self) -> None:
        """Test that SpecialDay is immutable."""
        sd = SpecialDay(
            name="Christmas",
            start_date=date(2024, 12, 25),
            duration=1,
            day_type="Holiday",
        )
        with pytest.raises(AttributeError):
            sd.name = "New Year"  # type: ignore[misc]


class TestTimeValue:
    """Tests for TimeValue dataclass."""

    def test_create(self) -> None:
        """Test creating a TimeValue."""
        tv = TimeValue(until_time=time(8, 0), value=0.0)
        assert tv.until_time == time(8, 0)
        assert tv.value == 0.0

    def test_frozen(self) -> None:
        """Test that TimeValue is immutable."""
        tv = TimeValue(until_time=time(8, 0), value=0.0)
        with pytest.raises(AttributeError):
            tv.value = 1.0  # type: ignore[misc]


class TestCompactDayRule:
    """Tests for CompactDayRule dataclass."""

    def test_create(self) -> None:
        """Test creating a CompactDayRule."""
        rule = CompactDayRule(
            day_types={"Weekdays"},
            time_values=[
                TimeValue(until_time=time(8, 0), value=0.0),
                TimeValue(until_time=time(18, 0), value=1.0),
            ],
        )
        assert "Weekdays" in rule.day_types
        assert len(rule.time_values) == 2


class TestCompactPeriod:
    """Tests for CompactPeriod dataclass."""

    def test_create(self) -> None:
        """Test creating a CompactPeriod."""
        period = CompactPeriod(end_month=6, end_day=30, day_rules=[])
        assert period.end_month == 6
        assert period.end_day == 30

    def test_contains(self) -> None:
        """Test contains() method."""
        period = CompactPeriod(end_month=6, end_day=30, day_rules=[])
        assert period.contains(date(2024, 1, 1))
        assert period.contains(date(2024, 6, 30))
        assert not period.contains(date(2024, 7, 1))


class TestWeekdayMapping:
    """Tests for weekday to day type mapping."""

    def test_weekday_mapping(self) -> None:
        """Test WEEKDAY_TO_DAY_TYPE mapping."""
        assert WEEKDAY_TO_DAY_TYPE[0] == "Monday"
        assert WEEKDAY_TO_DAY_TYPE[1] == "Tuesday"
        assert WEEKDAY_TO_DAY_TYPE[2] == "Wednesday"
        assert WEEKDAY_TO_DAY_TYPE[3] == "Thursday"
        assert WEEKDAY_TO_DAY_TYPE[4] == "Friday"
        assert WEEKDAY_TO_DAY_TYPE[5] == "Saturday"
        assert WEEKDAY_TO_DAY_TYPE[6] == "Sunday"


class TestParseDayType:
    """Tests for parse_day_type function."""

    def test_none_returns_normal(self) -> None:
        """Test None returns NORMAL."""
        assert parse_day_type(None) == DayType.NORMAL

    def test_enum_passthrough(self) -> None:
        """Test DayType enum passes through."""
        assert parse_day_type(DayType.SUMMER_DESIGN) == DayType.SUMMER_DESIGN

    def test_string_literals(self) -> None:
        """Test string literal inputs."""
        assert parse_day_type("normal") == DayType.NORMAL
        assert parse_day_type("summer") == DayType.SUMMER_DESIGN
        assert parse_day_type("winter") == DayType.WINTER_DESIGN
        assert parse_day_type("holiday") == DayType.HOLIDAY
        assert parse_day_type("customday1") == DayType.CUSTOM_DAY_1
        assert parse_day_type("customday2") == DayType.CUSTOM_DAY_2

    def test_invalid_string_raises_key_error(self) -> None:
        """Test invalid string raises KeyError."""
        with pytest.raises(KeyError):
            parse_day_type("invalid")  # type: ignore[arg-type]


class TestParseInterpolation:
    """Tests for parse_interpolation function."""

    def test_none_returns_no(self) -> None:
        """Test None returns NO."""
        assert parse_interpolation(None) == Interpolation.NO

    def test_enum_passthrough(self) -> None:
        """Test Interpolation enum passes through."""
        assert parse_interpolation(Interpolation.AVERAGE) == Interpolation.AVERAGE

    def test_string_literals(self) -> None:
        """Test string literal inputs."""
        assert parse_interpolation("no") == Interpolation.NO
        assert parse_interpolation("step") == Interpolation.NO
        assert parse_interpolation("average") == Interpolation.AVERAGE
        assert parse_interpolation("linear") == Interpolation.LINEAR

    def test_invalid_string_raises_key_error(self) -> None:
        """Test invalid string raises KeyError."""
        with pytest.raises(KeyError):
            parse_interpolation("invalid")  # type: ignore[arg-type]
