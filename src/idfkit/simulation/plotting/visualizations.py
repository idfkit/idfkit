"""High-level visualization functions for simulation results.

Provides convenience functions that combine SQL result queries with
plotting backends to produce common building performance visualizations.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..parsers.sql import SQLResult
    from . import PlotBackend


def plot_energy_balance(
    sql: SQLResult,
    *,
    backend: PlotBackend | None = None,
    title: str = "End-Use Energy by Category",
) -> Any:
    """Create a bar chart of end-use energy consumption.

    Extracts data from the ``AnnualBuildingUtilityPerformanceSummary`` report
    and plots energy consumption by end-use category.

    Args:
        sql: An open SQLResult database.
        backend: Plotting backend to use. Auto-detects if not provided.
        title: Plot title.

    Returns:
        A figure object from the backend.
    """
    if backend is None:
        from . import get_default_backend

        backend = get_default_backend()

    # Query end-use breakdown from the tabular report
    rows = sql.get_tabular_data(
        report_name="AnnualBuildingUtilityPerformanceSummary",
        table_name="End Uses",
    )

    # Aggregate by row_name (end-use category), summing across fuels
    # We want column_name "Total Energy" or sum numeric values from fuel columns
    energy_by_use: dict[str, float] = {}
    for row in rows:
        # Skip header rows and non-numeric values
        if row.row_name in ("", "Total End Uses"):
            continue
        try:
            value = float(row.value)
        except ValueError:
            continue
        # Skip zero or empty values
        if value == 0:
            continue
        # Accumulate by end-use category
        if row.row_name not in energy_by_use:
            energy_by_use[row.row_name] = 0.0
        energy_by_use[row.row_name] += value

    # Sort by value descending
    sorted_items = sorted(energy_by_use.items(), key=lambda x: x[1], reverse=True)
    categories = [item[0] for item in sorted_items]
    values = [item[1] for item in sorted_items]

    return backend.bar(
        categories,
        values,
        title=title,
        xlabel="End Use",
        ylabel="Energy (GJ)",
    )


def plot_temperature_profile(
    sql: SQLResult,
    zones: Sequence[str],
    *,
    backend: PlotBackend | None = None,
    title: str = "Zone Air Temperatures",
    frequency: str | None = None,
) -> Any:
    """Create a multi-line plot of zone air temperatures.

    Queries ``Zone Mean Air Temperature`` for each specified zone and
    plots them on a shared time axis.

    Args:
        sql: An open SQLResult database.
        zones: Zone names to plot.
        backend: Plotting backend to use. Auto-detects if not provided.
        title: Plot title.
        frequency: Optional frequency filter (e.g. ``"Hourly"``).

    Returns:
        A figure object from the backend.
    """
    if backend is None:
        from . import get_default_backend

        backend = get_default_backend()

    timestamps: Sequence[Any] = ()
    y_series: dict[str, Sequence[float]] = {}

    for zone in zones:
        ts = sql.get_timeseries("Zone Mean Air Temperature", zone, frequency=frequency)
        if not timestamps:
            timestamps = ts.timestamps
        y_series[zone] = ts.values

    return backend.multi_line(
        timestamps,
        y_series,
        title=title,
        xlabel="Time",
        ylabel="Temperature (C)",
    )


def plot_comfort_hours(
    sql: SQLResult,
    zones: Sequence[str],
    *,
    comfort_min: float = 20.0,
    comfort_max: float = 26.0,
    backend: PlotBackend | None = None,
    title: str = "Comfort Hours by Zone and Month",
) -> Any:
    """Create a heatmap of comfort hours by zone and month.

    For each zone, calculates the percentage of hours within the comfort
    range for each month and displays as a heatmap.

    Args:
        sql: An open SQLResult database.
        zones: Zone names to analyze.
        comfort_min: Minimum comfort temperature (default 20C).
        comfort_max: Maximum comfort temperature (default 26C).
        backend: Plotting backend to use. Auto-detects if not provided.
        title: Plot title.

    Returns:
        A figure object from the backend.
    """
    if backend is None:
        from . import get_default_backend

        backend = get_default_backend()

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # data[zone_idx][month_idx] = comfort percentage
    data: list[list[float]] = []

    for zone in zones:
        ts = sql.get_timeseries("Zone Mean Air Temperature", zone)

        # Count hours per month
        month_hours: dict[int, int] = dict.fromkeys(range(1, 13), 0)
        month_comfort: dict[int, int] = dict.fromkeys(range(1, 13), 0)

        for timestamp, value in zip(ts.timestamps, ts.values, strict=True):
            month = timestamp.month
            month_hours[month] += 1
            if comfort_min <= value <= comfort_max:
                month_comfort[month] += 1

        # Calculate percentage for each month
        row: list[float] = []
        for m in range(1, 13):
            pct = 100.0 * month_comfort[m] / month_hours[m] if month_hours[m] > 0 else 0.0
            row.append(pct)
        data.append(row)

    return backend.heatmap(
        data,
        x_labels=months,
        y_labels=list(zones),
        title=title,
        colorbar_label="Comfort Hours (%)",
    )
