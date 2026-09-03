from __future__ import annotations

from typing import Any

from idfkit.simulation import TimeSeriesResult

fig: Any = ...  # type: ignore[assignment]
ts: TimeSeriesResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation.plotting.plotly import PlotlyBackend

backend = PlotlyBackend()
fig = backend.line(
    x=list(ts.timestamps),
    y=list(ts.values),
    title="Zone Temperature",
)

# Interactive display
fig.show()

# Save to HTML
fig.write_html("temperature.html")
# --8<-- [end:example]
