"""High-level visualization functions for simulation results.

Provides convenience functions that combine SQL result queries with
plotting backends to produce common building performance visualizations.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from ...exceptions import ResultLookupError

if TYPE_CHECKING:
    from ..parsers.sql import SQLResult, TimeSeriesResult
    from . import PlotBackend


# Joules per unit for the energy units EnergyPlus tabular reports use (SI, IP, JtoKWH, JtoMJ, ...).
_JOULES_PER_UNIT: dict[str, float] = {
    "J": 1.0,
    "kJ": 1e3,
    "MJ": 1e6,
    "GJ": 1e9,
    "Wh": 3600.0,
    "kWh": 3.6e6,
    "MWh": 3.6e9,
    "Btu": 1055.05585262,
    "kBtu": 1055.05585262e3,
    "MMBtu": 1055.05585262e6,
    "therm": 105.505585262e6,
}


def plot_energy_balance(
    sql: SQLResult,
    *,
    backend: PlotBackend | None = None,
    title: str = "End-Use Energy by Category",
) -> Any:
    """Create a bar chart of end-use energy consumption.

    Extracts data from the ``AnnualBuildingUtilityPerformanceSummary`` report
    and plots energy consumption by end-use category, summed across fuels.
    Only energy columns are summed: the ``Water`` column (m3 or gal) is left
    out.  The axis is labelled with the report's energy unit (``GJ`` for SI
    reports, ``kBtu`` for IP); when the report mixes energy units (IP with
    electricity in kWh, for example) every value is converted to the unit
    most of its cells use.

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

    # Keep the energy cells of each end-use row; water volume and anything else not energy is dropped.
    cells: list[tuple[str, str, float]] = []
    for row in rows:
        if row.row_name in ("", "Total End Uses"):
            continue
        unit = row.units.strip()
        if unit not in _JOULES_PER_UNIT:
            continue
        try:
            value = float(row.value)
        except ValueError:
            continue
        if value == 0:
            continue
        cells.append((row.row_name, unit, value))

    unit_counts = Counter(unit for _, unit, _ in cells)
    target_unit = unit_counts.most_common(1)[0][0] if unit_counts else None

    energy_by_use: dict[str, float] = {}
    for row_name, unit, value in cells:
        if target_unit is not None and unit != target_unit:
            value = value * _JOULES_PER_UNIT[unit] / _JOULES_PER_UNIT[target_unit]
        energy_by_use[row_name] = energy_by_use.get(row_name, 0.0) + value

    # Sort by value descending
    sorted_items = sorted(energy_by_use.items(), key=lambda x: x[1], reverse=True)
    categories = [item[0] for item in sorted_items]
    values = [item[1] for item in sorted_items]

    return backend.bar(
        categories,
        values,
        title=title,
        xlabel="End Use",
        ylabel="Energy" if target_unit is None else f"Energy ({target_unit})",
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


def _zone_temperature(sql: SQLResult, zone: str, frequency: str | None) -> TimeSeriesResult:
    """Read a zone's mean air temperature, preferring hourly data when *frequency* is ``None``."""
    try:
        return sql.get_timeseries("Zone Mean Air Temperature", zone, frequency=frequency)
    except ResultLookupError as exc:
        if frequency is not None or not any(f.casefold() == "hourly" for f in exc.available):
            raise
    return sql.get_timeseries("Zone Mean Air Temperature", zone, frequency="Hourly")


def plot_comfort_hours(
    sql: SQLResult,
    zones: Sequence[str],
    *,
    comfort_min: float = 20.0,
    comfort_max: float = 26.0,
    frequency: str | None = None,
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
        frequency: Reporting frequency of ``Zone Mean Air Temperature`` to
            read (e.g. ``"Hourly"`` or ``"Timestep"``). When ``None`` and the
            variable is reported at several frequencies, ``"Hourly"`` is used.
        backend: Plotting backend to use. Auto-detects if not provided.
        title: Plot title.

    Returns:
        A figure object from the backend.

    Raises:
        ResultLookupError: If the variable is not reported for a zone, or is
            reported at several frequencies, none of them hourly, and
            *frequency* is ``None``.
    """
    if backend is None:
        from . import get_default_backend

        backend = get_default_backend()

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # data[zone_idx][month_idx] = comfort percentage
    data: list[list[float]] = []

    for zone in zones:
        ts = _zone_temperature(sql, zone, frequency)

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
