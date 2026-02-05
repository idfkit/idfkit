"""Plotly plotting backend for simulation results.

Provides :class:`PlotlyBackend` which implements the :class:`PlotBackend`
protocol using plotly. Requires plotly to be installed.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any


class PlotlyBackend:
    """Plotting backend using plotly.

    Lazily imports plotly when methods are called. Each method returns
    a plotly ``Figure`` object.

    Raises:
        ImportError: If plotly is not installed.
    """

    def __init__(self) -> None:
        """Initialize the backend, verifying plotly is available."""
        try:
            import plotly.graph_objects  # type: ignore[import-not-found]  # noqa: F401
        except ImportError:
            msg = "plotly is required for PlotlyBackend. Install it with: pip install idfkit[plotly]"
            raise ImportError(msg) from None

    def _get_go(self) -> Any:
        """Get plotly.graph_objects module."""
        import plotly.graph_objects as go  # type: ignore[import-not-found]

        return go

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
            x: X-axis values.
            y: Y-axis values.
            title: Optional plot title.
            xlabel: Optional X-axis label.
            ylabel: Optional Y-axis label.
            label: Optional line label for legend.

        Returns:
            A plotly Figure.
        """
        go = self._get_go()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(x), y=list(y), mode="lines", name=label or ""))
        fig.update_layout(
            title=title,
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            showlegend=label is not None,
        )
        return fig

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
            y_series: Mapping of label to Y values.
            title: Optional plot title.
            xlabel: Optional X-axis label.
            ylabel: Optional Y-axis label.

        Returns:
            A plotly Figure.
        """
        go = self._get_go()
        fig = go.Figure()
        for name, y in y_series.items():
            fig.add_trace(go.Scatter(x=list(x), y=list(y), mode="lines", name=name))
        fig.update_layout(
            title=title,
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            showlegend=bool(y_series),
        )
        return fig

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
            A plotly Figure.
        """
        go = self._get_go()
        heatmap_args: dict[str, Any] = {
            "z": [list(row) for row in data],
        }
        if x_labels is not None:
            heatmap_args["x"] = list(x_labels)
        if y_labels is not None:
            heatmap_args["y"] = list(y_labels)
        if colorbar_label:
            heatmap_args["colorbar"] = {"title": colorbar_label}

        fig = go.Figure(data=go.Heatmap(**heatmap_args))
        fig.update_layout(title=title)
        return fig

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
            A plotly Figure.
        """
        go = self._get_go()
        fig = go.Figure(data=go.Bar(x=list(categories), y=list(values)))
        fig.update_layout(
            title=title,
            xaxis_title=xlabel,
            yaxis_title=ylabel,
        )
        return fig

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
            A plotly Figure.
        """
        go = self._get_go()
        fig = go.Figure()
        for name, bar_values in series.items():
            fig.add_trace(go.Bar(x=list(categories), y=list(bar_values), name=name))
        fig.update_layout(
            title=title,
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            barmode="stack",
        )
        return fig
