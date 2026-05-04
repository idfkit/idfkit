from __future__ import annotations

from idfkit.simulation import TimeSeriesResult

ts: TimeSeriesResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
fig = ts.plot()  # Auto-detects matplotlib/plotly
# --8<-- [end:example]
