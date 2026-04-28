from __future__ import annotations

from idfkit.simulation import TimeSeriesResult

ts: TimeSeriesResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Get DataFrame
df = ts.to_dataframe()

# Matplotlib via pandas
df.plot(figsize=(12, 6))

# Plotly via pandas
import plotly.express as px

fig = px.line(df.reset_index(), x="timestamp", y=ts.variable_name)
# --8<-- [end:example]
