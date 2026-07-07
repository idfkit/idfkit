from __future__ import annotations

from idfkit.simulation import TimeSeriesResult

ts: TimeSeriesResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import MatplotlibBackend, PlotlyBackend

# Force matplotlib
fig = ts.plot(backend=MatplotlibBackend())

# Force plotly
fig = ts.plot(backend=PlotlyBackend())
# --8<-- [end:example]
