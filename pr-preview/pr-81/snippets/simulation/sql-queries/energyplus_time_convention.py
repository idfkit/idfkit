from __future__ import annotations

from idfkit.simulation import SQLResult, TimeSeriesResult

sql: SQLResult | None = ...  # type: ignore[assignment]
ts: TimeSeriesResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
ts = sql.get_timeseries("Zone Mean Air Temperature", "ZONE 1")

# Timestamps are proper Python datetime objects
first = ts.timestamps[0]
print(f"Year: {first.year}")  # 2017 (reference year)
print(f"Month: {first.month}")
print(f"Day: {first.day}")
print(f"Hour: {first.hour}")
# --8<-- [end:example]
