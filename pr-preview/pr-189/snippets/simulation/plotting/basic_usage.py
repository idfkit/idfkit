from __future__ import annotations

from typing import Any

from idfkit.simulation import TimeSeriesResult

fig: Any = ...  # type: ignore[assignment]
ts: TimeSeriesResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation.plotting.matplotlib import MatplotlibBackend

backend = MatplotlibBackend()
fig = backend.line(
    x=list(ts.timestamps),
    y=list(ts.values),
    title="Zone Temperature",
    xlabel="Time",
    ylabel="Temperature (°C)",
)

# Save to file
fig.savefig("temperature.png")
# --8<-- [end:example]
