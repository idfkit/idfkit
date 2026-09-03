# Simulation Overview

The simulation module provides subprocess-based EnergyPlus execution with
structured result parsing, batch processing, and content-addressed caching.

{{ parity("local-simulation") }}

## Quick Start

```python
--8<-- "docs/snippets/simulation/index/quick_start.py:example"
```

## Requirements

- **EnergyPlus 8.9+** installed on your system
- idfkit auto-discovers EnergyPlus installations

Check your installation:

```python
--8<-- "docs/snippets/simulation/index/requirements.py:example"
```

## Module Components

| Component | Description |
|-----------|-------------|
| [`simulate()`](running.md) | Run a single simulation |
| [`SimulationResult`](results.md) | Access output files and parsed data |
| [`SQLResult`](sql-queries.md) | Query time-series and tabular data |
| [`simulate_batch()`](batch.md) | Run multiple simulations in parallel |
| [`async_simulate()`](async.md) | Non-blocking single simulation |
| [`async_simulate_batch()`](async.md#async-batch-processing) | Non-blocking parallel simulations |
| [`async_simulate_batch_stream()`](async.md#streaming-progress) | Streaming progress via async generator |
| [`SimulationProgress`](progress.md) | Real-time progress tracking via callbacks |
| [`SimulationCache`](caching.md) | Content-addressed result caching |
| [`OutputVariableIndex`](output-discovery.md) | Discover available output variables |
| [`ErrorReport`](errors.md) | Parse error and warning messages |
| [How to plot simulation results](plotting.md) | Visualize results with matplotlib/plotly |

## Key Features

### Automatic SQLite Output

The module automatically injects `Output:SQLite` into your model, ensuring
reliable access to all simulation data through a single queryable file.

### Lazy Loading

Output files are only parsed when accessed, keeping memory usage low:

```python
--8<-- "docs/snippets/simulation/index/lazy_loading.py:example"
```

### Model Safety

Your original model is never mutated — simulations work on a copy:

```python
--8<-- "docs/snippets/simulation/index/model_safety.py:example"
```

### Parallel Execution

Run parametric studies efficiently with batch processing:

```python
--8<-- "docs/snippets/simulation/index/parallel_execution.py:example"
```

### Async Execution

For async applications, non-blocking variants are available:

```python
from idfkit.simulation import async_simulate, async_simulate_batch_stream

# Single simulation
result = await async_simulate(model, "weather.epw")

# Streaming progress
async for event in async_simulate_batch_stream(jobs, max_concurrent=4):
    print(f"[{event.completed}/{event.total}] {event.label}")
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

- [How to run a simulation](running.md) — Detailed guide to `simulate()`
- [How to run simulations asynchronously](async.md) — Non-blocking execution with `asyncio`
- [How to access simulation results](results.md) — Working with `SimulationResult`
- [Simulation Architecture](../concepts/simulation-architecture.md) — Design decisions
