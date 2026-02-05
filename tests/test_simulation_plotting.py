"""Tests for the plotting module."""

from __future__ import annotations

import sys
from collections.abc import Sequence
from datetime import datetime
from typing import Any
from unittest.mock import patch

import pytest

from idfkit.simulation.parsers.sql import TabularRow, TimeSeriesResult
from idfkit.simulation.plotting import PlotBackend, get_default_backend

# ---------------------------------------------------------------------------
# MockBackend for testing
# ---------------------------------------------------------------------------


class MockBackend:
    """Test backend that records all method calls."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[Any, ...], dict[str, Any]]] = []

    def line(
        self,
        x: Sequence[Any],
        y: Sequence[float],
        *,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        label: str | None = None,
    ) -> dict[str, Any]:
        self.calls.append(("line", (x, y), {"title": title, "xlabel": xlabel, "ylabel": ylabel, "label": label}))
        return {"type": "line", "x": list(x), "y": list(y)}

    def multi_line(
        self,
        x: Sequence[Any],
        y_series: dict[str, Sequence[float]],
        *,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
    ) -> dict[str, Any]:
        self.calls.append(("multi_line", (x, y_series), {"title": title, "xlabel": xlabel, "ylabel": ylabel}))
        return {"type": "multi_line", "x": list(x), "y_series": y_series}

    def heatmap(
        self,
        data: Sequence[Sequence[float]],
        *,
        x_labels: Sequence[str] | None = None,
        y_labels: Sequence[str] | None = None,
        title: str | None = None,
        colorbar_label: str | None = None,
    ) -> dict[str, Any]:
        self.calls.append((
            "heatmap",
            (data,),
            {"x_labels": x_labels, "y_labels": y_labels, "title": title, "colorbar_label": colorbar_label},
        ))
        return {"type": "heatmap", "data": data}

    def bar(
        self,
        categories: Sequence[str],
        values: Sequence[float],
        *,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
    ) -> dict[str, Any]:
        self.calls.append(("bar", (categories, values), {"title": title, "xlabel": xlabel, "ylabel": ylabel}))
        return {"type": "bar", "categories": list(categories), "values": list(values)}

    def stacked_bar(
        self,
        categories: Sequence[str],
        series: dict[str, Sequence[float]],
        *,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
    ) -> dict[str, Any]:
        self.calls.append(("stacked_bar", (categories, series), {"title": title, "xlabel": xlabel, "ylabel": ylabel}))
        return {"type": "stacked_bar", "categories": list(categories), "series": series}


# ---------------------------------------------------------------------------
# Protocol compliance tests
# ---------------------------------------------------------------------------


class TestPlotBackendProtocol:
    """Tests for the PlotBackend protocol."""

    def test_mock_backend_satisfies_protocol(self) -> None:
        """MockBackend should satisfy the PlotBackend protocol."""
        assert isinstance(MockBackend(), PlotBackend)

    def test_custom_class_satisfies_protocol(self) -> None:
        """A custom class implementing all methods passes isinstance."""

        class Custom:
            def line(
                self,
                x: Sequence[Any],
                y: Sequence[float],
                *,
                title: str | None = None,
                xlabel: str | None = None,
                ylabel: str | None = None,
                label: str | None = None,
            ) -> Any:
                return None

            def multi_line(
                self,
                x: Sequence[Any],
                y_series: dict[str, Sequence[float]],
                *,
                title: str | None = None,
                xlabel: str | None = None,
                ylabel: str | None = None,
            ) -> Any:
                return None

            def heatmap(
                self,
                data: Sequence[Sequence[float]],
                *,
                x_labels: Sequence[str] | None = None,
                y_labels: Sequence[str] | None = None,
                title: str | None = None,
                colorbar_label: str | None = None,
            ) -> Any:
                return None

            def bar(
                self,
                categories: Sequence[str],
                values: Sequence[float],
                *,
                title: str | None = None,
                xlabel: str | None = None,
                ylabel: str | None = None,
            ) -> Any:
                return None

            def stacked_bar(
                self,
                categories: Sequence[str],
                series: dict[str, Sequence[float]],
                *,
                title: str | None = None,
                xlabel: str | None = None,
                ylabel: str | None = None,
            ) -> Any:
                return None

        assert isinstance(Custom(), PlotBackend)


# ---------------------------------------------------------------------------
# get_default_backend tests
# ---------------------------------------------------------------------------


class TestGetDefaultBackend:
    """Tests for get_default_backend function."""

    def test_returns_matplotlib_when_available(self) -> None:
        """When matplotlib is available, returns MatplotlibBackend."""
        # This test relies on matplotlib being installed in dev dependencies
        try:
            import matplotlib.pyplot  # noqa: F401

            backend = get_default_backend()
            from idfkit.simulation.plotting.matplotlib import MatplotlibBackend

            assert isinstance(backend, MatplotlibBackend)
        except ImportError:
            pytest.skip("matplotlib not installed")

    def test_raises_when_no_backend_available(self) -> None:
        """When neither matplotlib nor plotly is installed, raises ImportError."""
        # Block both imports
        with (
            patch.dict(
                sys.modules,
                {"matplotlib": None, "matplotlib.pyplot": None, "plotly": None, "plotly.graph_objects": None},
            ),
            pytest.raises(ImportError, match="No plotting backend available"),
        ):
            get_default_backend()


# ---------------------------------------------------------------------------
# TimeSeriesResult.plot() tests
# ---------------------------------------------------------------------------


class TestTimeSeriesPlot:
    """Tests for TimeSeriesResult.plot() method."""

    @pytest.fixture
    def time_series(self) -> TimeSeriesResult:
        """Create a simple time series for testing."""
        return TimeSeriesResult(
            variable_name="Zone Mean Air Temperature",
            key_value="ZONE 1",
            units="C",
            frequency="Hourly",
            timestamps=(
                datetime(2017, 1, 1, 1, 0),
                datetime(2017, 1, 1, 2, 0),
                datetime(2017, 1, 1, 3, 0),
            ),
            values=(20.0, 21.0, 22.0),
        )

    def test_plot_with_mock_backend(self, time_series: TimeSeriesResult) -> None:
        """Plotting with a mock backend records the call correctly."""
        backend = MockBackend()
        result = time_series.plot(backend=backend)

        assert len(backend.calls) == 1
        method, args, kwargs = backend.calls[0]
        assert method == "line"
        assert args[0] == list(time_series.timestamps)
        assert args[1] == list(time_series.values)
        assert kwargs["title"] == "ZONE 1: Zone Mean Air Temperature"
        assert kwargs["xlabel"] == "Time"
        assert kwargs["ylabel"] == "Zone Mean Air Temperature (C)"
        assert kwargs["label"] == "ZONE 1"
        assert result["type"] == "line"

    def test_plot_with_custom_title(self, time_series: TimeSeriesResult) -> None:
        """Custom title overrides the default."""
        backend = MockBackend()
        time_series.plot(backend=backend, title="My Custom Title")

        _, _, kwargs = backend.calls[0]
        assert kwargs["title"] == "My Custom Title"


# ---------------------------------------------------------------------------
# Visualization function tests
# ---------------------------------------------------------------------------


class MockSQLResult:
    """Mock SQLResult for testing visualization functions."""

    def __init__(
        self,
        *,
        timeseries_data: dict[str, TimeSeriesResult] | None = None,
        tabular_data: list[TabularRow] | None = None,
    ) -> None:
        self._timeseries = timeseries_data or {}
        self._tabular = tabular_data or []

    def get_timeseries(
        self,
        variable_name: str,
        key_value: str = "*",
        frequency: str | None = None,
        environment: str | None = "annual",
    ) -> TimeSeriesResult:
        key = f"{variable_name}:{key_value}"
        if key in self._timeseries:
            return self._timeseries[key]
        raise KeyError(f"Variable not found: {variable_name!r} (key={key_value!r})")  # noqa: TRY003

    def get_tabular_data(
        self,
        report_name: str | None = None,
        table_name: str | None = None,
    ) -> list[TabularRow]:
        result = self._tabular
        if report_name:
            result = [r for r in result if r.report_name == report_name]
        if table_name:
            result = [r for r in result if r.table_name == table_name]
        return result


class TestPlotEnergyBalance:
    """Tests for plot_energy_balance function."""

    def test_creates_bar_chart(self) -> None:
        """Creates a bar chart from tabular data."""
        from idfkit.simulation.plotting.visualizations import plot_energy_balance

        tabular_data = [
            TabularRow(
                "AnnualBuildingUtilityPerformanceSummary",
                "Entire Facility",
                "End Uses",
                "Heating",
                "Electricity",
                "GJ",
                "100.5",
            ),
            TabularRow(
                "AnnualBuildingUtilityPerformanceSummary",
                "Entire Facility",
                "End Uses",
                "Cooling",
                "Electricity",
                "GJ",
                "50.2",
            ),
            TabularRow(
                "AnnualBuildingUtilityPerformanceSummary",
                "Entire Facility",
                "End Uses",
                "Lighting",
                "Electricity",
                "GJ",
                "30.0",
            ),
        ]
        sql = MockSQLResult(tabular_data=tabular_data)
        backend = MockBackend()

        result = plot_energy_balance(sql, backend=backend)  # type: ignore[arg-type]

        assert len(backend.calls) == 1
        method, args, _ = backend.calls[0]
        assert method == "bar"
        assert "Heating" in args[0]
        assert "Cooling" in args[0]
        assert "Lighting" in args[0]
        assert result["type"] == "bar"


class TestPlotTemperatureProfile:
    """Tests for plot_temperature_profile function."""

    def test_creates_multi_line_chart(self) -> None:
        """Creates a multi-line chart for multiple zones."""
        from idfkit.simulation.plotting.visualizations import plot_temperature_profile

        ts1 = TimeSeriesResult(
            "Zone Mean Air Temperature",
            "ZONE 1",
            "C",
            "Hourly",
            (datetime(2017, 1, 1, 1), datetime(2017, 1, 1, 2)),
            (20.0, 21.0),
        )
        ts2 = TimeSeriesResult(
            "Zone Mean Air Temperature",
            "ZONE 2",
            "C",
            "Hourly",
            (datetime(2017, 1, 1, 1), datetime(2017, 1, 1, 2)),
            (22.0, 23.0),
        )
        sql = MockSQLResult(
            timeseries_data={
                "Zone Mean Air Temperature:ZONE 1": ts1,
                "Zone Mean Air Temperature:ZONE 2": ts2,
            }
        )
        backend = MockBackend()

        result = plot_temperature_profile(sql, ["ZONE 1", "ZONE 2"], backend=backend)  # type: ignore[arg-type]

        assert len(backend.calls) == 1
        method, args, _ = backend.calls[0]
        assert method == "multi_line"
        assert "ZONE 1" in args[1]
        assert "ZONE 2" in args[1]
        assert result["type"] == "multi_line"


class TestPlotComfortHours:
    """Tests for plot_comfort_hours function."""

    def test_creates_heatmap(self) -> None:
        """Creates a heatmap for comfort hours analysis."""
        from idfkit.simulation.plotting.visualizations import plot_comfort_hours

        # Create a year's worth of hourly data (simplified - just a few months)
        timestamps = tuple(datetime(2017, m, 1, h) for m in range(1, 4) for h in range(1, 3))
        # All values within comfort range for simplicity
        values = tuple(22.0 for _ in timestamps)

        ts = TimeSeriesResult("Zone Mean Air Temperature", "ZONE 1", "C", "Hourly", timestamps, values)
        sql = MockSQLResult(timeseries_data={"Zone Mean Air Temperature:ZONE 1": ts})
        backend = MockBackend()

        result = plot_comfort_hours(sql, ["ZONE 1"], backend=backend, comfort_min=20.0, comfort_max=26.0)  # type: ignore[arg-type]

        assert len(backend.calls) == 1
        method, _, kwargs = backend.calls[0]
        assert method == "heatmap"
        assert kwargs["x_labels"] is not None
        assert len(kwargs["x_labels"]) == 12  # 12 months
        assert kwargs["y_labels"] == ["ZONE 1"]
        assert result["type"] == "heatmap"


# ---------------------------------------------------------------------------
# Backend import error tests
# ---------------------------------------------------------------------------


class TestMatplotlibBackendImportError:
    """Tests for MatplotlibBackend import handling."""

    def test_raises_when_matplotlib_missing(self) -> None:
        """Raises ImportError when matplotlib is not installed."""
        with patch.dict(sys.modules, {"matplotlib": None, "matplotlib.pyplot": None}):
            from importlib import reload

            import idfkit.simulation.plotting.matplotlib as mpl_module

            with pytest.raises(ImportError, match="matplotlib is required"):
                reload(mpl_module)
                mpl_module.MatplotlibBackend()


class TestPlotlyBackendImportError:
    """Tests for PlotlyBackend import handling."""

    def test_raises_when_plotly_missing(self) -> None:
        """Raises ImportError when plotly is not installed."""
        with patch.dict(sys.modules, {"plotly": None, "plotly.graph_objects": None}):
            from importlib import reload

            import idfkit.simulation.plotting.plotly as plotly_module

            with pytest.raises(ImportError, match="plotly is required"):
                reload(plotly_module)
                plotly_module.PlotlyBackend()


# ---------------------------------------------------------------------------
# MatplotlibBackend tests (when available)
# ---------------------------------------------------------------------------


class TestMatplotlibBackend:
    """Tests for MatplotlibBackend (requires matplotlib)."""

    @pytest.fixture
    def backend(self) -> Any:
        """Create a MatplotlibBackend, skipping if matplotlib not available."""
        try:
            from idfkit.simulation.plotting.matplotlib import MatplotlibBackend

            return MatplotlibBackend()
        except ImportError:
            pytest.skip("matplotlib not installed")

    def test_satisfies_protocol(self, backend: Any) -> None:
        """MatplotlibBackend satisfies PlotBackend protocol."""
        assert isinstance(backend, PlotBackend)

    def test_line_returns_figure(self, backend: Any) -> None:
        """line() returns a matplotlib Figure."""
        import matplotlib.pyplot as plt

        fig = backend.line([1, 2, 3], [10, 20, 30], title="Test")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_multi_line_returns_figure(self, backend: Any) -> None:
        """multi_line() returns a matplotlib Figure."""
        import matplotlib.pyplot as plt

        fig = backend.multi_line([1, 2, 3], {"A": [10, 20, 30], "B": [15, 25, 35]}, title="Test")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_heatmap_returns_figure(self, backend: Any) -> None:
        """heatmap() returns a matplotlib Figure."""
        import matplotlib.pyplot as plt

        fig = backend.heatmap([[1, 2], [3, 4]], x_labels=["X1", "X2"], y_labels=["Y1", "Y2"], title="Test")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_bar_returns_figure(self, backend: Any) -> None:
        """bar() returns a matplotlib Figure."""
        import matplotlib.pyplot as plt

        fig = backend.bar(["A", "B", "C"], [10, 20, 30], title="Test")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_stacked_bar_returns_figure(self, backend: Any) -> None:
        """stacked_bar() returns a matplotlib Figure."""
        import matplotlib.pyplot as plt

        fig = backend.stacked_bar(["A", "B"], {"X": [10, 20], "Y": [5, 10]}, title="Test")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)
