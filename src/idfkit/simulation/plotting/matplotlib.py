"""Matplotlib plotting backend for simulation results.

Provides :class:`MatplotlibBackend` which implements the :class:`PlotBackend`
protocol using matplotlib. Requires matplotlib to be installed.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any


class MatplotlibBackend:
    """Plotting backend using matplotlib.

    Lazily imports matplotlib when methods are called. Each method returns
    a matplotlib ``Figure`` object.

    Raises:
        ImportError: If matplotlib is not installed.
    """

    def __init__(self) -> None:
        """Initialize the backend, verifying matplotlib is available."""
        try:
            import matplotlib.pyplot  # type: ignore[import-not-found]  # noqa: F401
        except ImportError:
            msg = "matplotlib is required for MatplotlibBackend. Install it with: pip install idfkit[plot]"
            raise ImportError(msg) from None

    def _get_pyplot(self) -> Any:
        """Get matplotlib.pyplot module."""
        import matplotlib.pyplot as plt  # type: ignore[import-not-found]

        return plt

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
            A matplotlib Figure.
        """
        plt = self._get_pyplot()
        fig, ax = plt.subplots()
        ax.plot(x, y, label=label)
        if title:
            ax.set_title(title)
        if xlabel:
            ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel)
        if label:
            ax.legend()
        fig.tight_layout()
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
            A matplotlib Figure.
        """
        plt = self._get_pyplot()
        fig, ax = plt.subplots()
        for line_label, y in y_series.items():
            ax.plot(x, y, label=line_label)
        if title:
            ax.set_title(title)
        if xlabel:
            ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel)
        if y_series:
            ax.legend()
        fig.tight_layout()
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
            A matplotlib Figure.
        """
        plt = self._get_pyplot()
        fig, ax = plt.subplots()
        im = ax.imshow(data, aspect="auto")
        cbar = fig.colorbar(im, ax=ax)
        if colorbar_label:
            cbar.set_label(colorbar_label)
        if x_labels is not None:
            ax.set_xticks(range(len(x_labels)))
            ax.set_xticklabels(x_labels, rotation=45, ha="right")
        if y_labels is not None:
            ax.set_yticks(range(len(y_labels)))
            ax.set_yticklabels(y_labels)
        if title:
            ax.set_title(title)
        fig.tight_layout()
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
            A matplotlib Figure.
        """
        plt = self._get_pyplot()
        fig, ax = plt.subplots()
        ax.bar(categories, values)
        if title:
            ax.set_title(title)
        if xlabel:
            ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel)
        ax.tick_params(axis="x", rotation=45)
        fig.tight_layout()
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
            A matplotlib Figure.
        """
        plt = self._get_pyplot()
        fig, ax = plt.subplots()
        # Build x positions and bottom accumulator manually to avoid numpy
        x_positions = list(range(len(categories)))
        bottom: list[float] = [0.0] * len(categories)

        for bar_label, bar_values in series.items():
            ax.bar(x_positions, bar_values, bottom=bottom, label=bar_label)
            for i, v in enumerate(bar_values):
                bottom[i] += v

        ax.set_xticks(x_positions)
        ax.set_xticklabels(categories, rotation=45, ha="right")
        if title:
            ax.set_title(title)
        if xlabel:
            ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel)
        if series:
            ax.legend()
        fig.tight_layout()
        return fig
