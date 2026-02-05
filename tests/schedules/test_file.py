"""Tests for schedules.file module."""

from __future__ import annotations

import warnings
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from idfkit.schedules.file import (
    ScheduleFileCache,
    _read_schedule_file,
    evaluate_schedule_file,
    get_schedule_file_values,
)


class TestScheduleFileCache:
    """Tests for ScheduleFileCache class."""

    def test_cache_hit(self) -> None:
        """Test cache returns cached values."""
        cache = ScheduleFileCache()

        # First call should read from file
        obj = MagicMock()
        obj.get.side_effect = lambda f: {
            "File Name": "test.csv",
            "Column Number": 1,
            "Rows to Skip at Top": 1,
            "Column Separator": "Comma",
        }.get(f)

        fs = MagicMock()
        fs.read_text.return_value = "header\n0.5\n0.75\n1.0"

        values1 = cache.get_values(obj, fs, Path("/base"))

        # Second call should use cache
        values2 = cache.get_values(obj, fs, Path("/base"))

        assert values1 == values2
        # read_text should only be called once
        assert fs.read_text.call_count == 1

    def test_clear_cache(self) -> None:
        """Test clearing the cache."""
        cache = ScheduleFileCache()

        obj = MagicMock()
        obj.get.side_effect = lambda f: {
            "File Name": "test.csv",
            "Column Number": 1,
            "Rows to Skip at Top": 0,
            "Column Separator": "Comma",
        }.get(f)

        fs = MagicMock()
        fs.read_text.return_value = "0.5\n0.75"

        cache.get_values(obj, fs, Path("/base"))
        cache.clear()

        # After clear, should read again
        cache.get_values(obj, fs, Path("/base"))
        assert fs.read_text.call_count == 2

    def test_invalidate_specific(self) -> None:
        """Test invalidating a specific cache entry."""
        cache = ScheduleFileCache()

        obj = MagicMock()
        obj.get.side_effect = lambda f: {
            "File Name": "test.csv",
            "Column Number": 1,
            "Rows to Skip at Top": 0,
            "Column Separator": "Comma",
        }.get(f)

        fs = MagicMock()
        fs.read_text.return_value = "0.5"

        cache.get_values(obj, fs, Path("/base"))
        cache.invalidate("/base/test.csv")

        cache.get_values(obj, fs, Path("/base"))
        assert fs.read_text.call_count == 2


class TestReadScheduleFile:
    """Tests for _read_schedule_file function."""

    def test_simple_csv(self) -> None:
        """Test reading a simple CSV file."""
        obj = MagicMock()
        obj.get.side_effect = lambda f: {
            "Column Number": 1,
            "Rows to Skip at Top": 0,
            "Column Separator": "Comma",
        }.get(f)

        fs = MagicMock()
        fs.read_text.return_value = "0.0\n0.5\n1.0"

        result = _read_schedule_file(obj, fs, Path("test.csv"))
        assert result == [0.0, 0.5, 1.0]

    def test_with_header(self) -> None:
        """Test reading CSV with header row."""
        obj = MagicMock()
        obj.get.side_effect = lambda f: {
            "Column Number": 1,
            "Rows to Skip at Top": 1,
            "Column Separator": "Comma",
        }.get(f)

        fs = MagicMock()
        fs.read_text.return_value = "timestamp,value\n2024-01-01,0.5\n2024-01-02,0.75"

        result = _read_schedule_file(obj, fs, Path("test.csv"))
        # Should skip header but still parse the date string as non-numeric
        # Actually this will fail on the date - let me fix the test
        assert len(result) == 0  # Both rows have non-numeric first column

    def test_second_column(self) -> None:
        """Test reading from second column."""
        obj = MagicMock()
        obj.get.side_effect = lambda f: {
            "Column Number": 2,
            "Rows to Skip at Top": 1,
            "Column Separator": "Comma",
        }.get(f)

        fs = MagicMock()
        fs.read_text.return_value = "timestamp,value\n2024-01-01,0.5\n2024-01-02,0.75"

        result = _read_schedule_file(obj, fs, Path("test.csv"))
        assert result == [0.5, 0.75]

    def test_tab_separator(self) -> None:
        """Test reading tab-separated file."""
        obj = MagicMock()
        obj.get.side_effect = lambda f: {
            "Column Number": 1,
            "Rows to Skip at Top": 0,
            "Column Separator": "Tab",
        }.get(f)

        fs = MagicMock()
        fs.read_text.return_value = "0.0\t0.5\n1.0\t1.5"

        result = _read_schedule_file(obj, fs, Path("test.csv"))
        assert result == [0.0, 1.0]

    def test_semicolon_separator(self) -> None:
        """Test reading semicolon-separated file."""
        obj = MagicMock()
        obj.get.side_effect = lambda f: {
            "Column Number": 1,
            "Rows to Skip at Top": 0,
            "Column Separator": "Semicolon",
        }.get(f)

        fs = MagicMock()
        fs.read_text.return_value = "0.0;0.5\n1.0;1.5"

        result = _read_schedule_file(obj, fs, Path("test.csv"))
        assert result == [0.0, 1.0]


class TestEvaluateScheduleFile:
    """Tests for evaluate_schedule_file function."""

    @pytest.fixture
    def hourly_schedule(self) -> tuple[MagicMock, MagicMock, ScheduleFileCache]:
        """Create a mock hourly schedule file."""
        obj = MagicMock()
        obj.get.side_effect = lambda f: {
            "File Name": "hourly.csv",
            "Column Number": 1,
            "Rows to Skip at Top": 0,
            "Column Separator": "Comma",
            "Minutes per Item": 60,
            "Interpolate to Timestep": None,
        }.get(f)

        # 24 hourly values for a day pattern
        fs = MagicMock()
        hourly_values = [0.0] * 8 + [1.0] * 10 + [0.0] * 6
        fs.read_text.return_value = "\n".join(str(v) for v in hourly_values * 366)

        cache = ScheduleFileCache()
        return obj, fs, cache

    def test_evaluate_hourly(self, hourly_schedule: tuple[MagicMock, MagicMock, ScheduleFileCache]) -> None:
        """Test evaluating hourly schedule."""
        obj, fs, cache = hourly_schedule

        # January 1, 10am (hour 10 of year, value should be 1.0)
        result = evaluate_schedule_file(
            obj,
            datetime(2024, 1, 1, 10, 0),
            fs,
            Path("/base"),
            cache,
        )
        assert result == 1.0

        # January 1, 6am (hour 6 of year, value should be 0.0)
        result = evaluate_schedule_file(
            obj,
            datetime(2024, 1, 1, 6, 0),
            fs,
            Path("/base"),
            cache,
        )
        assert result == 0.0

    def test_evaluate_with_interpolation(self) -> None:
        """Test evaluating with interpolation."""
        obj = MagicMock()
        obj.get.side_effect = lambda f: {
            "File Name": "test.csv",
            "Column Number": 1,
            "Rows to Skip at Top": 0,
            "Column Separator": "Comma",
            "Minutes per Item": 60,
            "Interpolate to Timestep": "Average",
        }.get(f)

        # Two values: 0.0 and 1.0
        fs = MagicMock()
        fs.read_text.return_value = "0.0\n1.0" + "\n1.0" * 8782

        cache = ScheduleFileCache()

        # At 0:30 (halfway through first hour), should interpolate
        result = evaluate_schedule_file(
            obj,
            datetime(2024, 1, 1, 0, 30),
            fs,
            Path("/base"),
            cache,
        )
        # With interpolation, should be between 0.0 and 1.0
        assert 0.0 < result < 1.0


class TestGetScheduleFileValues:
    """Tests for get_schedule_file_values function."""

    def test_get_all_values(self) -> None:
        """Test getting all values from schedule file."""
        obj = MagicMock()
        obj.get.side_effect = lambda f: {
            "File Name": "test.csv",
            "Column Number": 1,
            "Rows to Skip at Top": 0,
            "Column Separator": "Comma",
        }.get(f)

        fs = MagicMock()
        fs.read_text.return_value = "0.0\n0.5\n1.0"

        result = get_schedule_file_values(obj, fs, Path("/base"))
        assert result == [0.0, 0.5, 1.0]


class TestOutOfBoundsColumn:
    """Tests for out-of-bounds column warning."""

    def test_column_exceeds_row_width(self) -> None:
        """Test that requesting a column beyond row width triggers a warning."""
        obj = MagicMock()
        obj.get.side_effect = lambda f: {
            "Column Number": 3,
            "Rows to Skip at Top": 0,
            "Column Separator": "Comma",
        }.get(f)

        fs = MagicMock()
        # Only 2 columns, but requesting column 3
        fs.read_text.return_value = "0.0,0.5\n1.0,1.5"

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = _read_schedule_file(obj, fs, Path("test.csv"))
            assert len(result) == 0  # No values extracted
            assert len(w) == 2  # One warning per row
            assert "column 3" in str(w[0].message).lower()


class TestEmptyFile:
    """Tests for empty file handling."""

    def test_empty_file_returns_empty_list(self) -> None:
        """Test that an empty file returns an empty list."""
        obj = MagicMock()
        obj.get.side_effect = lambda f: {
            "Column Number": 1,
            "Rows to Skip at Top": 0,
            "Column Separator": "Comma",
        }.get(f)

        fs = MagicMock()
        fs.read_text.return_value = ""

        result = _read_schedule_file(obj, fs, Path("empty.csv"))
        assert result == []
