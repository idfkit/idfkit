# Simulation Overview

The simulation module provides subprocess-based EnergyPlus execution with
structured result parsing, batch processing, and content-addressed caching.

## Quick Start

```python
from idfkit import load_idf
from idfkit.simulation import simulate

# Load a model and run a simulation
model = load_idf("building.idf")
result = simulate(model, "weather.epw", design_day=True)

# Check results
print(f"Success: {result.success}")
print(f"Runtime: {result.runtime_seconds:.1f}s")

# Query time-series data
ts = result.sql.get_timeseries(
    variable_name="Zone Mean Air Temperature",
    key_value="THERMAL ZONE 1",
)
print(f"Max temp: {max(ts.values):.1f}°C")
```

## Requirements

- **EnergyPlus 8.9+** installed on your system
- idfkit auto-discovers EnergyPlus installations

Check your installation:

```python
from idfkit.simulation import find_energyplus

config = find_energyplus()
print(f"Found EnergyPlus {config.version[0]}.{config.version[1]}")
```

## Module Components

| Component | Description |
|-----------|-------------|
| [`simulate()`](running.md) | Run a single simulation |
| [`SimulationResult`](results.md) | Access output files and parsed data |
| [`SQLResult`](sql-queries.md) | Query time-series and tabular data |
| [`simulate_batch()`](batch.md) | Run multiple simulations in parallel |
| [`SimulationCache`](caching.md) | Content-addressed result caching |
| [`OutputVariableIndex`](output-discovery.md) | Discover available output variables |
| [`ErrorReport`](errors.md) | Parse error and warning messages |
| [Plotting](plotting.md) | Visualize results with matplotlib/plotly |

## Key Features

### Automatic SQLite Output

The module automatically injects `Output:SQLite` into your model, ensuring
reliable access to all simulation data through a single queryable file.

### Lazy Loading

Output files are only parsed when accessed, keeping memory usage low:

```python
result = simulate(model, weather)  # Just runs EnergyPlus
result.errors    # Parses ERR file on first access
result.sql       # Opens SQLite database on first access
```

### Model Safety

Your original model is never mutated — simulations work on a copy:

```python
result = simulate(model, weather)
assert "Output:SQLite" not in model  # Original unchanged
```

### Parallel Execution

Run parametric studies efficiently with batch processing:

```python
from idfkit.simulation import simulate_batch, SimulationJob

jobs = [
    SimulationJob(model=variant, weather="weather.epw", label=f"case-{i}")
    for i, variant in enumerate(variants)
]
batch = simulate_batch(jobs, max_workers=4)
```

## Installation

The simulation module requires no extra dependencies for basic operation.

For optional features:

```bash
# DataFrame conversion
pip install idfkit[dataframes]

# Plotting
pip install idfkit[plot]      # matplotlib
pip install idfkit[plotly]    # plotly

# Cloud storage
pip install idfkit[s3]
```

## Next Steps

- [Running Simulations](running.md) — Detailed guide to `simulate()`
- [Parsing Results](results.md) — Working with `SimulationResult`
- [Simulation Architecture](../concepts/simulation-architecture.md) — Design decisions
