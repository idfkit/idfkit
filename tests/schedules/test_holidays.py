"""Tests for schedules.holidays module."""

from __future__ import annotations

import warnings
from datetime import date
from unittest.mock import MagicMock

import pytest

from idfkit.schedules.holidays import (
    _last_weekday_of_month,
    _nth_weekday_of_month,
    _parse_date_spec,
    extract_special_days,
    get_holidays,
    get_special_days_by_type,
)


class TestParseDateSpec:
    """Tests for _parse_date_spec function."""

    def test_numeric_slash(self) -> None:
        """Test numeric format with slash."""
        assert _parse_date_spec("1/1", 2024) == date(2024, 1, 1)
        assert _parse_date_spec("12/25", 2024) == date(2024, 12, 25)

    def test_numeric_dash(self) -> None:
        """Test numeric format with dash."""
        assert _parse_date_spec("1-1", 2024) == date(2024, 1, 1)
        assert _parse_date_spec("12-25", 2024) == date(2024, 12, 25)

    def test_month_day(self) -> None:
        """Test Month Day format."""
        assert _parse_date_spec("January 1", 2024) == date(2024, 1, 1)
        assert _parse_date_spec("December 25", 2024) == date(2024, 12, 25)

    def test_day_month(self) -> None:
        """Test Day Month format."""
        assert _parse_date_spec("1 January", 2024) == date(2024, 1, 1)
        assert _parse_date_spec("25 December", 2024) == date(2024, 12, 25)

    def test_month_abbreviation(self) -> None:
        """Test abbreviated month names."""
        assert _parse_date_spec("Jan 1", 2024) == date(2024, 1, 1)
        assert _parse_date_spec("Dec 25", 2024) == date(2024, 12, 25)

    def test_nth_weekday(self) -> None:
        """Test nth weekday in month format."""
        # 4th Thursday in November 2024 = November 28
        assert _parse_date_spec("4th Thursday in November", 2024) == date(2024, 11, 28)
        # 3rd Monday in January 2024 = January 15 (MLK Day)
        assert _parse_date_spec("3rd Monday in January", 2024) == date(2024, 1, 15)

    def test_last_weekday(self) -> None:
        """Test last weekday in month format."""
        # Last Monday in May 2024 = May 27 (Memorial Day)
        assert _parse_date_spec("Last Monday in May", 2024) == date(2024, 5, 27)

    def test_invalid(self) -> None:
        """Test invalid format."""
        with pytest.raises(ValueError, match="Cannot parse date"):
            _parse_date_spec("invalid date", 2024)


class TestNthWeekdayOfMonth:
    """Tests for _nth_weekday_of_month function."""

    def test_first_monday(self) -> None:
        """Test first Monday of month."""
        # First Monday of January 2024 = January 1
        assert _nth_weekday_of_month(2024, 1, 0, 1) == date(2024, 1, 1)

    def test_second_tuesday(self) -> None:
        """Test second Tuesday of month."""
        # Second Tuesday of January 2024 = January 9
        assert _nth_weekday_of_month(2024, 1, 1, 2) == date(2024, 1, 9)

    def test_fourth_thursday(self) -> None:
        """Test fourth Thursday of month."""
        # Fourth Thursday of November 2024 = November 28
        assert _nth_weekday_of_month(2024, 11, 3, 4) == date(2024, 11, 28)

    def test_invalid_fifth(self) -> None:
        """Test invalid fifth occurrence."""
        with pytest.raises(ValueError, match="No 5th occurrence"):
            _nth_weekday_of_month(2024, 2, 0, 5)  # No 5th Monday in Feb 2024


class TestLastWeekdayOfMonth:
    """Tests for _last_weekday_of_month function."""

    def test_last_monday(self) -> None:
        """Test last Monday of month."""
        # Last Monday of May 2024 = May 27
        assert _last_weekday_of_month(2024, 5, 0) == date(2024, 5, 27)

    def test_last_friday(self) -> None:
        """Test last Friday of month."""
        # Last Friday of December 2024 = December 27
        assert _last_weekday_of_month(2024, 12, 4) == date(2024, 12, 27)


class TestExtractSpecialDays:
    """Tests for extract_special_days function."""

    def test_empty_document(self) -> None:
        """Test document with no special days."""
        doc = MagicMock()
        # Empty collection (IDFDocument[] returns empty IDFCollection)
        empty_collection = MagicMock()
        empty_collection.__iter__ = lambda self: iter([])
        empty_collection.__len__ = lambda self: 0
        doc.__getitem__.return_value = empty_collection

        result = extract_special_days(doc, 2024)
        assert result == []

    def test_simple_holiday(self) -> None:
        """Test extracting a simple holiday."""
        doc = MagicMock()

        # Mock a single holiday
        holiday_obj = MagicMock()
        holiday_obj.name = "Christmas"
        holiday_obj.get.side_effect = lambda f: {
            "Start Date": "December 25",
            "Duration": 1,
            "Special Day Type": "Holiday",
        }.get(f)

        holiday_list = [holiday_obj]
        collection = MagicMock()
        collection.__iter__ = lambda self: iter(holiday_list)
        collection.__len__ = lambda self: len(holiday_list)
        doc.__getitem__.return_value = collection

        result = extract_special_days(doc, 2024)
        assert len(result) == 1
        assert result[0].name == "Christmas"
        assert result[0].start_date == date(2024, 12, 25)
        assert result[0].duration == 1
        assert result[0].day_type == "Holiday"

    def test_multi_day_holiday(self) -> None:
        """Test extracting a multi-day holiday."""
        doc = MagicMock()

        holiday_obj = MagicMock()
        holiday_obj.name = "Christmas Break"
        holiday_obj.get.side_effect = lambda f: {
            "Start Date": "12/24",
            "Duration": 3,
            "Special Day Type": "Holiday",
        }.get(f)

        holiday_list = [holiday_obj]
        collection = MagicMock()
        collection.__iter__ = lambda self: iter(holiday_list)
        collection.__len__ = lambda self: len(holiday_list)
        doc.__getitem__.return_value = collection

        result = extract_special_days(doc, 2024)
        assert len(result) == 1
        assert result[0].duration == 3


class TestGetHolidays:
    """Tests for get_holidays function."""

    def test_single_day_holiday(self) -> None:
        """Test getting single-day holidays."""
        doc = MagicMock()

        holiday_obj = MagicMock()
        holiday_obj.name = "Christmas"
        holiday_obj.get.side_effect = lambda f: {
            "Start Date": "December 25",
            "Duration": 1,
            "Special Day Type": "Holiday",
        }.get(f)

        holiday_list = [holiday_obj]
        collection = MagicMock()
        collection.__iter__ = lambda self: iter(holiday_list)
        collection.__len__ = lambda self: len(holiday_list)
        doc.__getitem__.return_value = collection

        holidays = get_holidays(doc, 2024)
        assert date(2024, 12, 25) in holidays
        assert len(holidays) == 1

    def test_multi_day_holiday(self) -> None:
        """Test getting multi-day holidays."""
        doc = MagicMock()

        holiday_obj = MagicMock()
        holiday_obj.name = "Break"
        holiday_obj.get.side_effect = lambda f: {
            "Start Date": "12/24",
            "Duration": 3,
            "Special Day Type": "Holiday",
        }.get(f)

        holiday_list = [holiday_obj]
        collection = MagicMock()
        collection.__iter__ = lambda self: iter(holiday_list)
        collection.__len__ = lambda self: len(holiday_list)
        doc.__getitem__.return_value = collection

        holidays = get_holidays(doc, 2024)
        assert date(2024, 12, 24) in holidays
        assert date(2024, 12, 25) in holidays
        assert date(2024, 12, 26) in holidays
        assert len(holidays) == 3


class TestGetSpecialDaysByType:
    """Tests for get_special_days_by_type function."""

    def test_filter_by_type(self) -> None:
        """Test filtering special days by type."""
        doc = MagicMock()

        holiday_obj = MagicMock()
        holiday_obj.name = "Christmas"
        holiday_obj.get.side_effect = lambda f: {
            "Start Date": "12/25",
            "Duration": 1,
            "Special Day Type": "Holiday",
        }.get(f)

        custom_obj = MagicMock()
        custom_obj.name = "Company Day"
        custom_obj.get.side_effect = lambda f: {
            "Start Date": "6/15",
            "Duration": 1,
            "Special Day Type": "CustomDay1",
        }.get(f)

        obj_list = [holiday_obj, custom_obj]
        collection = MagicMock()
        collection.__iter__ = lambda self: iter(obj_list)
        collection.__len__ = lambda self: len(obj_list)
        doc.__getitem__.return_value = collection

        holidays = get_special_days_by_type(doc, 2024, "Holiday")
        assert date(2024, 12, 25) in holidays
        assert date(2024, 6, 15) not in holidays

        custom = get_special_days_by_type(doc, 2024, "CustomDay1")
        assert date(2024, 6, 15) in custom
        assert date(2024, 12, 25) not in custom


class TestMalformedDateWarning:
    """Tests for warning on malformed date specs."""

    def test_malformed_date_spec_triggers_warning(self) -> None:
        """Test that a malformed date spec produces a warning, not silent skip."""
        doc = MagicMock()

        holiday_obj = MagicMock()
        holiday_obj.name = "Bad Holiday"
        holiday_obj.get.side_effect = lambda f: {
            "Start Date": "totally invalid date",
            "Duration": 1,
            "Special Day Type": "Holiday",
        }.get(f)

        holiday_list = [holiday_obj]
        collection = MagicMock()
        collection.__iter__ = lambda self: iter(holiday_list)
        collection.__len__ = lambda self: len(holiday_list)
        doc.__getitem__.return_value = collection

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = extract_special_days(doc, 2024)
            assert len(result) == 0  # Malformed entry skipped
            assert len(w) == 1
            assert "cannot parse date" in str(w[0].message).lower()
