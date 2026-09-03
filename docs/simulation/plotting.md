# How to plot simulation results

The simulation module provides pluggable plotting backends for visualizing
results with matplotlib or plotly.

## Quick Start

```python
--8<-- "docs/snippets/simulation/plotting/quick_start.py:example"
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

Each of these takes the SQL database from a completed run, `result.sql`,
shown below as `sql`.

### Temperature Profile

```python
--8<-- "docs/snippets/simulation/plotting/temperature_profile.py:example"
```

### Energy Balance

```python
--8<-- "docs/snippets/simulation/plotting/energy_balance.py:example"
```

### Comfort Hours

```python
--8<-- "docs/snippets/simulation/plotting/comfort_hours.py:example"
```

## Time Series Plotting

`TimeSeriesResult` has a built-in `plot()` method:

```python
--8<-- "docs/snippets/simulation/plotting/time_series_plotting.py:example"
```

## Backend Selection

### Auto-Detection

By default, the first available backend is used:

```python
--8<-- "docs/snippets/simulation/plotting/auto_detection.py:example"
```

Priority: matplotlib → plotly

### Explicit Backend

```python
--8<-- "docs/snippets/simulation/plotting/explicit_backend.py:example"
```

## PlotBackend Protocol

Create custom backends by implementing the `PlotBackend` protocol:

```python
--8<-- "docs/snippets/simulation/plotting/plotbackend_protocol.py:example"
```

The backend classes live in their own modules so that importing
`idfkit.simulation` never pulls in matplotlib or plotly.

## Matplotlib Backend

### Basic Usage

```python
--8<-- "docs/snippets/simulation/plotting/basic_usage.py:example"
```

### Customization

```python
--8<-- "docs/snippets/simulation/plotting/customization.py:example"
```

## Plotly Backend

### Basic Usage

```python
--8<-- "docs/snippets/simulation/plotting/basic_usage_2.py:example"
```

### Customization

```python
--8<-- "docs/snippets/simulation/plotting/customization_2.py:example"
```

## DataFrame Integration

Convert to pandas and use native plotting:

```python
--8<-- "docs/snippets/simulation/plotting/dataframe_integration.py:example"
```

## Multiple Time Series

### Same Variable, Multiple Keys

```python
--8<-- "docs/snippets/simulation/plotting/same_variable_multiple_keys.py:example"
```

### Different Variables

```python
--8<-- "docs/snippets/simulation/plotting/different_variables.py:example"
```

## Saving Figures

### Matplotlib

```python
--8<-- "docs/snippets/simulation/plotting/matplotlib.py:example"
```

### Plotly

```python
--8<-- "docs/snippets/simulation/plotting/plotly.py:example"
```

## See Also

- [How to query simulation SQL output](sql-queries.md) — Getting time series data
- [How to access simulation results](results.md) — Working with SimulationResult
- [Examples: Parametric Study](../examples/parametric-study.ipynb) — Visualization examples
