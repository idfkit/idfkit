from __future__ import annotations

from idfkit.simulation import SimulationResult, TimeSeriesResult

result: SimulationResult = ...  # type: ignore[assignment]
ts: TimeSeriesResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
ts = result.sql.get_timeseries(
    "Zone Mean Air Temperature",
    "ZONE 1",
)

# Default plot
fig = ts.plot()

# Custom title
fig = ts.plot(title="My Custom Title")

# Explicit backend
from idfkit.simulation import MatplotlibBackend

fig = ts.plot(backend=MatplotlibBackend())
# --8<-- [end:example]
