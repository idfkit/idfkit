"""Pluggable plotting layer for simulation results.

Provides a :class:`PlotBackend` protocol so that visualizations can be
rendered with either matplotlib or plotly (or a custom backend). Users can
choose their preferred library without requiring both as dependencies.

Example:
    >>> from idfkit.simulation import SQLResult
    >>> from idfkit.simulation.plotting import get_default_backend
    >>>
    >>> backend = get_default_backend()
    >>> ts = sql.get_timeseries("Zone Mean Air Temperature", "ZONE 1")
    >>> fig = ts.plot(backend=backend)
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Protocol, runtime_checkable

from .visualizations import plot_comfort_hours, plot_energy_balance, plot_temperature_profile


@runtime_checkable
class PlotBackend(Protocol):
    """Protocol for plotting backends used by the simulation module.

    Implementations must provide methods for common chart types. Each method
    returns a figure object native to the backend (e.g. matplotlib ``Figure``
    or plotly ``Figure``).
    """

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
        """Create a single line plot.

        Args:
            x: X-axis values (e.g. timestamps).
            y: Y-axis values.
            title: Optional plot title.
            xlabel: Optional X-axis label.
            ylabel: Optional Y-axis label.
            label: Optional line label for legend.

        Returns:
            A figure object native to the backend.
        """
        ...

    def multi_line(
        self,
        x: Sequence[Any],
        y_series: dict[str, Sequence[float]],
        *,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
    ) -> Any:
        """Create a multi-line plot with legend.

        Args:
            x: Shared X-axis values.
            y_series: Mapping of label to Y values for each line.
            title: Optional plot title.
            xlabel: Optional X-axis label.
            ylabel: Optional Y-axis label.

        Returns:
            A figure object native to the backend.
        """
        ...

    def heatmap(
        self,
        data: Sequence[Sequence[float]],
        *,
        x_labels: Sequence[str] | None = None,
        y_labels: Sequence[str] | None = None,
        title: str | None = None,
        colorbar_label: str | None = None,
    ) -> Any:
        """Create a 2D heatmap.

        Args:
            data: 2D array of values (rows, columns).
            x_labels: Optional labels for columns.
            y_labels: Optional labels for rows.
            title: Optional plot title.
            colorbar_label: Optional label for the colorbar.

        Returns:
            A figure object native to the backend.
        """
        ...

    def bar(
        self,
        categories: Sequence[str],
        values: Sequence[float],
        *,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
    ) -> Any:
        """Create a bar chart.

        Args:
            categories: Category labels for each bar.
            values: Values for each bar.
            title: Optional plot title.
            xlabel: Optional X-axis label.
            ylabel: Optional Y-axis label.

        Returns:
            A figure object native to the backend.
        """
        ...

    def stacked_bar(
        self,
        categories: Sequence[str],
        series: dict[str, Sequence[float]],
        *,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
    ) -> Any:
        """Create a stacked bar chart.

        Args:
            categories: Category labels for each bar group.
            series: Mapping of series label to values.
            title: Optional plot title.
            xlabel: Optional X-axis label.
            ylabel: Optional Y-axis label.

        Returns:
            A figure object native to the backend.
        """
        ...


def get_default_backend() -> PlotBackend:
    """Auto-detect and return an available plotting backend.

    Tries matplotlib first, then plotly. Raises ImportError if neither
    is available.

    Returns:
        A PlotBackend instance.

    Raises:
        ImportError: If neither matplotlib nor plotly is installed.
    """
    # Try matplotlib first (more common)
    try:
        from .matplotlib import MatplotlibBackend

        return MatplotlibBackend()
    except ImportError:
        pass

    # Fall back to plotly
    try:
        from .plotly import PlotlyBackend

        return PlotlyBackend()
    except ImportError:
        pass

    msg = (
        "No plotting backend available. Install matplotlib or plotly: "
        "pip install idfkit[plot] or pip install idfkit[plotly]"
    )
    raise ImportError(msg)


__all__ = [
    "PlotBackend",
    "get_default_backend",
    "plot_comfort_hours",
    "plot_energy_balance",
    "plot_temperature_profile",
]
