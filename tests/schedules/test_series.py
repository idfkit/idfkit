"""Tests for schedules.series module."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from idfkit.schedules.series import _freq_to_timestep

# ---------------------------------------------------------------------------
# _freq_to_timestep
# ---------------------------------------------------------------------------


class TestFreqToTimestep:
    """Tests for _freq_to_timestep."""

    @pytest.mark.parametrize(
        ("freq", "expected"),
        [
            ("h", 1),
            ("1h", 1),
            ("60min", 1),
            ("60t", 1),
            ("30min", 2),
            ("30t", 2),
            ("20min", 3),
            ("20t", 3),
            ("15min", 4),
            ("15t", 4),
            ("10min", 6),
            ("10t", 6),
            ("5min", 12),
            ("5t", 12),
            ("1min", 60),
            ("1t", 60),
            ("min", 60),
            ("t", 60),
        ],
    )
    def test_predefined_frequencies(self, freq: str, expected: int) -> None:
        assert _freq_to_timestep(freq) == expected

    def test_case_insensitive(self) -> None:
        assert _freq_to_timestep("H") == 1
        assert _freq_to_timestep("30MIN") == 2

    def test_whitespace_stripped(self) -> None:
        assert _freq_to_timestep("  h  ") == 1

    def test_custom_hour_format(self) -> None:
        """Custom hour format defaults to 1 (can't go coarser than hourly)."""
        assert _freq_to_timestep("2h") == 1

    def test_custom_minute_evenly_divisible(self) -> None:
        assert _freq_to_timestep("12min") == 5  # 60/12

    def test_custom_minute_not_evenly_divisible(self) -> None:
        """Non-evenly-divisible minutes default to hourly."""
        assert _freq_to_timestep("7min") == 1

    def test_unparseable_defaults_to_hourly(self) -> None:
        assert _freq_to_timestep("garbage") == 1


# ---------------------------------------------------------------------------
# to_series
# ---------------------------------------------------------------------------


class TestToSeries:
    """Tests for to_series (requires pandas)."""

    @pytest.fixture
    def constant_schedule(self) -> MagicMock:
        obj = MagicMock()
        obj.obj_type = "Schedule:Constant"
        obj.get.return_value = 0.5
        obj.name = "TestSchedule"
        del obj._document
        return obj

    def test_basic_hourly_series(self, constant_schedule: MagicMock) -> None:
        pandas = pytest.importorskip("pandas")
        from idfkit.schedules.series import to_series

        series = to_series(
            constant_schedule,
            year=2024,
            start_date=(1, 1),
            end_date=(1, 1),
        )

        assert len(series) == 24
        assert all(v == 0.5 for v in series)
        assert series.name == "TestSchedule"
        # Check DatetimeIndex
        assert series.index[0] == pandas.Timestamp(2024, 1, 1, 0, 0)

    def test_sub_hourly_series(self, constant_schedule: MagicMock) -> None:
        pytest.importorskip("pandas")
        from idfkit.schedules.series import to_series

        series = to_series(
            constant_schedule,
            year=2024,
            freq="15min",
            start_date=(1, 1),
            end_date=(1, 1),
        )

        # 24 hours * 4 per hour = 96
        assert len(series) == 96

    def test_custom_date_range(self, constant_schedule: MagicMock) -> None:
        pytest.importorskip("pandas")
        from idfkit.schedules.series import to_series

        series = to_series(
            constant_schedule,
            year=2024,
            start_date=(1, 1),
            end_date=(1, 31),
        )

        # 31 days * 24 hours = 744
        assert len(series) == 744

    def test_schedule_without_name_uses_obj_type(self) -> None:
        pytest.importorskip("pandas")
        from idfkit.schedules.series import to_series

        obj = MagicMock()
        obj.obj_type = "Schedule:Constant"
        obj.get.return_value = 1.0
        obj.name = None
        del obj._document

        series = to_series(obj, year=2024, start_date=(1, 1), end_date=(1, 1))
        assert series.name == "Schedule:Constant"

    def test_import_error_without_pandas(self) -> None:
        """to_series raises ImportError when pandas not available."""
        import builtins

        real_import = builtins.__import__

        def mock_import(name: str, *args: object, **kwargs: object) -> object:
            if name == "pandas":
                raise ImportError
            return real_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            from idfkit.schedules import series

            # Force reimport to trigger the import error
            with pytest.raises(ImportError, match="pandas is required"):
                series.to_series(MagicMock(), year=2024)


# ---------------------------------------------------------------------------
# plot_schedule, plot_week, plot_day
# ---------------------------------------------------------------------------


class TestPlotFunctions:
    """Tests for plot_schedule, plot_week, and plot_day."""

    @pytest.fixture
    def constant_schedule(self) -> MagicMock:
        obj = MagicMock()
        obj.obj_type = "Schedule:Constant"
        obj.get.return_value = 0.5
        obj.name = "TestSchedule"
        del obj._document
        return obj

    def test_plot_schedule_default_drawstyle(self, constant_schedule: MagicMock) -> None:
        pytest.importorskip("pandas")
        pytest.importorskip("matplotlib")
        from idfkit.schedules.series import plot_schedule

        ax = plot_schedule(
            constant_schedule,
            year=2024,
            start_date=(1, 1),
            end_date=(1, 1),
        )
        # Just check it returns something (Axes object)
        assert ax is not None

    def test_plot_schedule_custom_kwargs(self, constant_schedule: MagicMock) -> None:
        pytest.importorskip("pandas")
        pytest.importorskip("matplotlib")
        from idfkit.schedules.series import plot_schedule

        ax = plot_schedule(
            constant_schedule,
            year=2024,
            start_date=(1, 1),
            end_date=(1, 1),
            drawstyle="default",
            color="red",
        )
        assert ax is not None

    def test_plot_day(self, constant_schedule: MagicMock) -> None:
        pytest.importorskip("pandas")
        pytest.importorskip("matplotlib")
        from idfkit.schedules.series import plot_day

        ax = plot_day(
            constant_schedule,
            year=2024,
            month=6,
            day=15,
        )
        assert ax is not None

    def test_plot_week(self, constant_schedule: MagicMock) -> None:
        pytest.importorskip("pandas")
        pytest.importorskip("matplotlib")
        from idfkit.schedules.series import plot_week

        ax = plot_week(
            constant_schedule,
            year=2024,
            week=1,
        )
        assert ax is not None

    def test_plot_week_various_weeks(self, constant_schedule: MagicMock) -> None:
        """Test different week numbers compute valid date ranges."""
        pytest.importorskip("pandas")
        pytest.importorskip("matplotlib")
        from idfkit.schedules.series import plot_week

        # Just verify these don't raise
        for week_num in [1, 26, 52]:
            ax = plot_week(constant_schedule, year=2024, week=week_num)
            assert ax is not None
