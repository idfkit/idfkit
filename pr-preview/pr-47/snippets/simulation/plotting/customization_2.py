from __future__ import annotations

from idfkit.simulation import SimulationResult, TimeSeriesResult
from typing import Any

fig: Any = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
ts: TimeSeriesResult = ...  # type: ignore[assignment]
zone_names: list[str] = ...  # type: ignore[assignment]
# --8<-- [start:example]
import plotly.graph_objects as go

fig = go.Figure()

for zone_name in zone_names:
    ts = result.sql.get_timeseries(
        "Zone Mean Air Temperature",
        zone_name,
    )
    fig.add_trace(
        go.Scatter(
            x=list(ts.timestamps),
            y=list(ts.values),
            name=zone_name,
        )
    )

fig.update_layout(
    title="Zone Temperatures",
    xaxis_title="Time",
    yaxis_title="Temperature (°C)",
)
fig.show()
# --8<-- [end:example]
