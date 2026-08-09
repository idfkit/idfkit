from __future__ import annotations

from idfkit.simulation import SQLResult, TimeSeriesResult

sql: SQLResult | None = ...  # type: ignore[assignment]
ts: TimeSeriesResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
ts = sql.get_timeseries(
    variable_name="Zone Mean Air Temperature",
    key_value="THERMAL ZONE 1",
)

print(f"Variable: {ts.variable_name}")
print(f"Key: {ts.key_value}")
print(f"Units: {ts.units}")
print(f"Frequency: {ts.frequency}")
print(f"Data points: {len(ts.values)}")
print(f"Min: {min(ts.values):.1f}, Max: {max(ts.values):.1f}")
# --8<-- [end:example]
