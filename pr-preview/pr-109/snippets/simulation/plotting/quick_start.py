from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult, TimeSeriesResult

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
ts: TimeSeriesResult = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import simulate

result = simulate(model, weather)

# Plot time series
ts = result.sql.get_timeseries(
    "Zone Mean Air Temperature",
    "ZONE 1",
)
fig = ts.plot()  # Auto-detects available backend
# --8<-- [end:example]
