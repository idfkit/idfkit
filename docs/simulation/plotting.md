# Plotting

The simulation module provides pluggable plotting backends for visualizing
results with matplotlib or plotly.

## Quick Start

```python
from idfkit.simulation import simulate

result = simulate(model, weather)

# Plot time series
ts = result.sql.get_timeseries(
    "Zone Mean Air Temperature",
    "ZONE 1",
)
fig = ts.plot()  # Auto-detects available backend
```

## Installation

Install a plotting backend:

```bash
# Matplotlib (recommended for static plots)
pip install idfkit[plot]

# Plotly (for interactive plots)
pip install idfkit[plotly]

# Both
pip install idfkit[plot,plotly]
```

## Built-in Visualizations

### Temperature Profile

```python
from idfkit.simulation import plot_temperature_profile

fig = plot_temperature_profile(
    result,
    zone_name="THERMAL ZONE 1",
    title="Zone Temperatures",
)
```

### Energy Balance

```python
from idfkit.simulation import plot_energy_balance

fig = plot_energy_balance(
    result,
    title="Annual Energy Balance",
)
```

### Comfort Hours

```python
from idfkit.simulation import plot_comfort_hours

fig = plot_comfort_hours(
    result,
    zone_name="THERMAL ZONE 1",
    title="Thermal Comfort Analysis",
)
```

## Time Series Plotting

`TimeSeriesResult` has a built-in `plot()` method:

```python
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
```

## Backend Selection

### Auto-Detection

By default, the first available backend is used:

```python
from idfkit.simulation import get_default_backend

backend = get_default_backend()
print(type(backend).__name__)  # MatplotlibBackend or PlotlyBackend
```

Priority: matplotlib → plotly

### Explicit Backend

```python
from idfkit.simulation import MatplotlibBackend, PlotlyBackend

# Force matplotlib
fig = ts.plot(backend=MatplotlibBackend())

# Force plotly
fig = ts.plot(backend=PlotlyBackend())
```

## PlotBackend Protocol

Create custom backends by implementing the `PlotBackend` protocol:

```python
from idfkit.simulation import PlotBackend

class MyBackend(PlotBackend):
    def line(
        self,
        x: list,
        y: list,
        *,
        title: str = "",
        xlabel: str = "",
        ylabel: str = "",
        label: str | None = None,
    ):
        # Return a figure object
        ...

    def bar(
        self,
        categories: list[str],
        values: list[float],
        *,
        title: str = "",
        xlabel: str = "",
        ylabel: str = "",
    ):
        # Return a figure object
        ...
```

## Matplotlib Backend

### Basic Usage

```python
from idfkit.simulation import MatplotlibBackend

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
```

### Customization

```python
import matplotlib.pyplot as plt

# Create custom figure
fig, ax = plt.subplots(figsize=(12, 6))

# Plot multiple series
for zone_name in zone_names:
    ts = result.sql.get_timeseries(
        "Zone Mean Air Temperature",
        zone_name,
    )
    ax.plot(ts.timestamps, ts.values, label=zone_name)

ax.legend()
ax.set_xlabel("Time")
ax.set_ylabel("Temperature (°C)")
plt.show()
```

## Plotly Backend

### Basic Usage

```python
from idfkit.simulation import PlotlyBackend

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
```

### Customization

```python
import plotly.graph_objects as go

fig = go.Figure()

for zone_name in zone_names:
    ts = result.sql.get_timeseries(
        "Zone Mean Air Temperature",
        zone_name,
    )
    fig.add_trace(go.Scatter(
        x=list(ts.timestamps),
        y=list(ts.values),
        name=zone_name,
    ))

fig.update_layout(
    title="Zone Temperatures",
    xaxis_title="Time",
    yaxis_title="Temperature (°C)",
)
fig.show()
```

## DataFrame Integration

Convert to pandas and use native plotting:

```python
# Get DataFrame
df = ts.to_dataframe()

# Matplotlib via pandas
df.plot(figsize=(12, 6))

# Plotly via pandas
import plotly.express as px
fig = px.line(df.reset_index(), x="timestamp", y=ts.variable_name)
```

## Multiple Time Series

### Same Variable, Multiple Keys

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

for zone_name in ["ZONE 1", "ZONE 2", "ZONE 3"]:
    ts = result.sql.get_timeseries(
        "Zone Mean Air Temperature",
        zone_name,
    )
    ax.plot(ts.timestamps, ts.values, label=zone_name)

ax.legend()
plt.show()
```

### Different Variables

```python
fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Temperature
ts_temp = result.sql.get_timeseries("Zone Mean Air Temperature", "ZONE 1")
axes[0].plot(ts_temp.timestamps, ts_temp.values)
axes[0].set_ylabel("Temperature (°C)")

# Humidity
ts_rh = result.sql.get_timeseries("Zone Air Relative Humidity", "ZONE 1")
axes[1].plot(ts_rh.timestamps, ts_rh.values)
axes[1].set_ylabel("Relative Humidity (%)")

plt.tight_layout()
plt.show()
```

## Saving Figures

### Matplotlib

```python
fig.savefig("plot.png", dpi=300, bbox_inches="tight")
fig.savefig("plot.pdf")
fig.savefig("plot.svg")
```

### Plotly

```python
fig.write_html("plot.html")
fig.write_image("plot.png")  # Requires kaleido
fig.write_image("plot.pdf")
```

## See Also

- [SQL Output Queries](sql-queries.md) — Getting time series data
- [Parsing Results](results.md) — Working with SimulationResult
- [Examples: Parametric Study](../examples/parametric-study.ipynb) — Visualization examples
