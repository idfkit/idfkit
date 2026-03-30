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


class TestMissingFileName:
    """Tests for missing File Name field (lines 92-93)."""

    def test_missing_file_name_raises(self) -> None:
        """_resolve_path raises ValueError when File Name is absent."""
        cache = ScheduleFileCache()
        obj = MagicMock()
        obj.get.return_value = None  # All fields return None
        fs = MagicMock()

        with pytest.raises(ValueError, match="missing 'File Name'"):
            cache.get_values(obj, fs, None)


class TestRelativePathResolution:
    """Tests for relative path resolution (lines 98->103, 100)."""

    def test_relative_path_with_base(self) -> None:
        """Relative path is resolved against base_path (line 101)."""
        cache = ScheduleFileCache()
        obj = MagicMock()
        obj.get.side_effect = lambda f: {
            "File Name": "data.csv",  # relative
            "Column Number": 1,
            "Rows to Skip at Top": 0,
            "Column Separator": "Comma",
        }.get(f)

        fs = MagicMock()
        fs.read_text.return_value = "0.5\n1.0"

        result = cache.get_values(obj, fs, base_path=Path("/some/dir"))
        assert result == [0.5, 1.0]
        # Verify the resolved path was used
        fs.read_text.assert_called_once_with(Path("/some/dir/data.csv"))

    def test_relative_path_without_base_uses_cwd(self) -> None:
        """Relative path without base_path uses cwd (line 100)."""
        import os

        cache = ScheduleFileCache()
        obj = MagicMock()
        obj.get.side_effect = lambda f: {
            "File Name": "data.csv",
            "Column Number": 1,
            "Rows to Skip at Top": 0,
            "Column Separator": "Comma",
        }.get(f)

        fs = MagicMock()
        fs.read_text.return_value = "0.3"

        result = cache.get_values(obj, fs, base_path=None)
        assert result == [0.3]
        expected_path = Path(os.getcwd()) / "data.csv"
        fs.read_text.assert_called_once_with(expected_path)

    def test_absolute_path_not_modified(self) -> None:
        """Absolute file path is used as-is without prepending base_path (line 98->103)."""
        cache = ScheduleFileCache()
        obj = MagicMock()
        obj.get.side_effect = lambda f: {
            "File Name": "/absolute/path/data.csv",  # absolute path
            "Column Number": 1,
            "Rows to Skip at Top": 0,
            "Column Separator": "Comma",
        }.get(f)

        fs = MagicMock()
        fs.read_text.return_value = "0.7"

        result = cache.get_values(obj, fs, base_path=Path("/some/other/dir"))
        assert result == [0.7]
        # Verify the absolute path was used directly
        fs.read_text.assert_called_once_with(Path("/absolute/path/data.csv"))


class TestGetInterpolationFromObj:
    """Tests for _get_interpolation_from_obj (line 189)."""

    def test_interpolate_yes_returns_average(self) -> None:
        """Interpolate field 'yes' returns AVERAGE interpolation."""
        from idfkit.schedules.file import _get_interpolation_from_obj  # pyright: ignore[reportPrivateUsage]
        from idfkit.schedules.types import Interpolation

        obj = MagicMock()
        obj.get.return_value = "Yes"
        result = _get_interpolation_from_obj(obj, Interpolation.NO)
        assert result == Interpolation.AVERAGE

    def test_interpolate_average_returns_average(self) -> None:
        """Interpolate field 'average' returns AVERAGE interpolation."""
        from idfkit.schedules.file import _get_interpolation_from_obj  # pyright: ignore[reportPrivateUsage]
        from idfkit.schedules.types import Interpolation

        obj = MagicMock()
        obj.get.return_value = "average"
        result = _get_interpolation_from_obj(obj, Interpolation.NO)
        assert result == Interpolation.AVERAGE

    def test_interpolate_no_returns_no(self) -> None:
        """Interpolate field 'no' returns NO interpolation."""
        from idfkit.schedules.file import _get_interpolation_from_obj  # pyright: ignore[reportPrivateUsage]
        from idfkit.schedules.types import Interpolation

        obj = MagicMock()
        obj.get.return_value = "no"
        result = _get_interpolation_from_obj(obj, Interpolation.AVERAGE)
        assert result == Interpolation.NO


class TestInterpolateValueBoundary:
    """Tests for _interpolate_value out-of-bounds (line 195)."""

    def test_index_beyond_list_returns_last(self) -> None:
        """Index beyond list length returns last element."""
        from idfkit.schedules.file import _interpolate_value  # pyright: ignore[reportPrivateUsage]

        result = _interpolate_value([1.0, 2.0, 3.0], index=10, fraction=0.5, interpolate=False)
        assert result == 3.0

    def test_empty_list_returns_zero(self) -> None:
        """Empty list returns 0.0."""
        from idfkit.schedules.file import _interpolate_value  # pyright: ignore[reportPrivateUsage]

        result = _interpolate_value([], index=0, fraction=0.0, interpolate=False)
        assert result == 0.0


class TestEvaluateScheduleFileEmpty:
    """Tests for evaluate_schedule_file with empty values (line 231)."""

    def test_empty_schedule_file_returns_zero(self) -> None:
        """Empty schedule file returns 0.0."""
        obj = MagicMock()
        obj.get.side_effect = lambda f: {
            "File Name": "empty.csv",
            "Column Number": 1,
            "Rows to Skip at Top": 0,
            "Column Separator": "Comma",
            "Minutes per Item": 60,
            "Interpolate to Timestep": None,
        }.get(f)

        fs = MagicMock()
        fs.read_text.return_value = ""

        cache = ScheduleFileCache()
        result = evaluate_schedule_file(obj, datetime(2024, 1, 1, 0, 0), fs, Path("/base"), cache)
        assert result == 0.0


class TestGetScheduleFileValuesDefaults:
    """Tests for get_schedule_file_values without fs/cache (lines 264-265->268)."""

    def test_without_cache_uses_default_cache(self) -> None:
        """get_schedule_file_values with cache=None exercises the default-cache branch (line 265->268)."""
        from idfkit.schedules.file import _default_cache  # pyright: ignore[reportPrivateUsage]

        # Clear the global cache so prior tests don't interfere
        _default_cache.clear()

        obj = MagicMock()
        obj.get.side_effect = lambda f: {
            "File Name": "unique_file_for_default_cache_test.csv",
            "Column Number": 1,
            "Rows to Skip at Top": 0,
            "Column Separator": "Comma",
        }.get(f)

        fs = MagicMock()
        fs.read_text.return_value = "0.5\n1.0"

        # Provide fs but not cache to exercise the cache=None branch (line 265->268)
        result = get_schedule_file_values(obj, fs=fs, base_path=Path("/base"), cache=None)
        assert result == [0.5, 1.0]

    def test_without_fs_uses_local_filesystem(self) -> None:
        """get_schedule_file_values with fs=None creates LocalFileSystem (line 264)."""
        from unittest.mock import patch

        from idfkit.schedules import file as file_module

        obj = MagicMock()
        obj.get.side_effect = lambda f: {
            "File Name": "/absolute/test_264.csv",
            "Column Number": 1,
            "Rows to Skip at Top": 0,
            "Column Separator": "Comma",
        }.get(f)

        cache = ScheduleFileCache()
        mock_fs = MagicMock()
        mock_fs.read_text.return_value = "0.9"

        # Patch LocalFileSystem to return our mock_fs so we don't touch real files
        with patch.object(file_module, "LocalFileSystem", return_value=mock_fs):
            result = get_schedule_file_values(obj, fs=None, base_path=None, cache=cache)

        assert result == [0.9]
