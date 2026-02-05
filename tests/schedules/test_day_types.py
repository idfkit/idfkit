"""Tests for schedules.day_types module."""

from __future__ import annotations

from datetime import date

from idfkit.schedules.day_types import DAY_TYPE_PRIORITY, get_applicable_day_types
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
    DAY_TYPE_WEEKDAYS,
    DAY_TYPE_WEEKENDS,
    DAY_TYPE_WINTER_DESIGN,
    DayType,
)


class TestDayTypePriority:
    """Tests for DAY_TYPE_PRIORITY list."""

    def test_design_days_before_weekdays(self) -> None:
        """Test design days come before regular weekdays in priority."""
        summer_idx = DAY_TYPE_PRIORITY.index(DAY_TYPE_SUMMER_DESIGN)
        monday_idx = DAY_TYPE_PRIORITY.index(DAY_TYPE_MONDAY)
        assert summer_idx < monday_idx

    def test_holiday_before_weekdays(self) -> None:
        """Test holiday comes before individual weekdays."""
        holiday_idx = DAY_TYPE_PRIORITY.index(DAY_TYPE_HOLIDAY)
        monday_idx = DAY_TYPE_PRIORITY.index(DAY_TYPE_MONDAY)
        assert holiday_idx < monday_idx

    def test_individual_days_before_groups(self) -> None:
        """Test individual weekdays come before group types."""
        saturday_idx = DAY_TYPE_PRIORITY.index(DAY_TYPE_SATURDAY)
        weekends_idx = DAY_TYPE_PRIORITY.index(DAY_TYPE_WEEKENDS)
        assert saturday_idx < weekends_idx

    def test_alldays_near_end(self) -> None:
        """Test AllDays is near the end of priority."""
        alldays_idx = DAY_TYPE_PRIORITY.index(DAY_TYPE_ALLDAYS)
        assert alldays_idx == len(DAY_TYPE_PRIORITY) - 2  # Before AllOtherDays

    def test_all_other_days_last(self) -> None:
        """Test AllOtherDays is last."""
        assert DAY_TYPE_PRIORITY[-1] == DAY_TYPE_ALL_OTHER_DAYS


class TestGetApplicableDayTypes:
    """Tests for get_applicable_day_types function."""

    def test_weekday(self) -> None:
        """Test applicable types for a weekday (Monday)."""
        types = get_applicable_day_types(
            date(2024, 1, 8),  # Monday
            DayType.NORMAL,
            set(),
            set(),
            set(),
        )

        assert DAY_TYPE_MONDAY in types
        assert DAY_TYPE_WEEKDAYS in types
        assert DAY_TYPE_ALLDAYS in types
        assert DAY_TYPE_ALL_OTHER_DAYS in types
        assert DAY_TYPE_WEEKENDS not in types
        assert DAY_TYPE_SATURDAY not in types

    def test_weekend(self) -> None:
        """Test applicable types for a weekend day (Saturday)."""
        types = get_applicable_day_types(
            date(2024, 1, 6),  # Saturday
            DayType.NORMAL,
            set(),
            set(),
            set(),
        )

        assert DAY_TYPE_SATURDAY in types
        assert DAY_TYPE_WEEKENDS in types
        assert DAY_TYPE_ALLDAYS in types
        assert DAY_TYPE_WEEKDAYS not in types

    def test_sunday(self) -> None:
        """Test applicable types for Sunday."""
        types = get_applicable_day_types(
            date(2024, 1, 7),  # Sunday
            DayType.NORMAL,
            set(),
            set(),
            set(),
        )

        assert DAY_TYPE_SUNDAY in types
        assert DAY_TYPE_WEEKENDS in types

    def test_holiday(self) -> None:
        """Test applicable types for a holiday."""
        types = get_applicable_day_types(
            date(2024, 12, 25),
            DayType.NORMAL,
            {date(2024, 12, 25)},
            set(),
            set(),
        )

        assert DAY_TYPE_HOLIDAY in types
        assert DAY_TYPE_ALLDAYS in types
        # Weekday type should still be present
        assert DAY_TYPE_WEEKDAYS in types or DAY_TYPE_WEEKENDS in types

    def test_summer_design_day_override(self) -> None:
        """Test summer design day override returns only design + AllDays."""
        types = get_applicable_day_types(
            date(2024, 7, 15),  # Monday
            DayType.SUMMER_DESIGN,
            set(),
            set(),
            set(),
        )

        assert types == {DAY_TYPE_SUMMER_DESIGN, DAY_TYPE_ALLDAYS}

    def test_winter_design_day_override(self) -> None:
        """Test winter design day override."""
        types = get_applicable_day_types(
            date(2024, 1, 15),
            DayType.WINTER_DESIGN,
            set(),
            set(),
            set(),
        )

        assert types == {DAY_TYPE_WINTER_DESIGN, DAY_TYPE_ALLDAYS}

    def test_holiday_override(self) -> None:
        """Test holiday day type override."""
        types = get_applicable_day_types(
            date(2024, 7, 15),  # A Monday
            DayType.HOLIDAY,
            set(),  # Not in the holiday set
            set(),
            set(),
        )

        assert types == {DAY_TYPE_HOLIDAY, DAY_TYPE_ALLDAYS}

    def test_custom_day_1(self) -> None:
        """Test CustomDay1 set membership."""
        types = get_applicable_day_types(
            date(2024, 6, 15),
            DayType.NORMAL,
            set(),
            {date(2024, 6, 15)},
            set(),
        )

        assert DAY_TYPE_CUSTOM_DAY_1 in types

    def test_custom_day_2(self) -> None:
        """Test CustomDay2 set membership."""
        types = get_applicable_day_types(
            date(2024, 6, 15),
            DayType.NORMAL,
            set(),
            set(),
            {date(2024, 6, 15)},
        )

        assert DAY_TYPE_CUSTOM_DAY_2 in types

    def test_custom_day_1_override(self) -> None:
        """Test CustomDay1 day type override."""
        types = get_applicable_day_types(
            date(2024, 7, 15),
            DayType.CUSTOM_DAY_1,
            set(),
            set(),
            set(),
        )

        assert types == {DAY_TYPE_CUSTOM_DAY_1, DAY_TYPE_ALLDAYS}

    def test_custom_day_2_override(self) -> None:
        """Test CustomDay2 day type override."""
        types = get_applicable_day_types(
            date(2024, 7, 15),
            DayType.CUSTOM_DAY_2,
            set(),
            set(),
            set(),
        )

        assert types == {DAY_TYPE_CUSTOM_DAY_2, DAY_TYPE_ALLDAYS}
