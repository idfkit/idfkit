from __future__ import annotations

from idfkit.simulation import SimulationResult, TimeSeriesResult

result: SimulationResult = ...  # type: ignore[assignment]
ts: TimeSeriesResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Get time-series data from SQLite output
ts = result.sql.get_timeseries(
    variable_name="Zone Mean Air Temperature",
    key_value="Office",
)
print(f"Variable: {ts.variable_name}")
print(f"Temperature range: {min(ts.values):.1f}°C to {max(ts.values):.1f}°C")

# Filter by environment if needed
ts_sizing = result.sql.get_timeseries(
    variable_name="Zone Mean Air Temperature",
    key_value="Office",
    environment="sizing",  # Design day data only
)

# Get tabular data
tables = result.sql.get_tabular_data(report_name="AnnualBuildingUtilityPerformanceSummary")
# --8<-- [end:example]
