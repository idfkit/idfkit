# Simulation API Overview

The simulation module provides EnergyPlus execution and result parsing.

## Quick Reference

| Function/Class | Description |
|---------------|-------------|
| [`simulate()`](runner.md) | Run a single simulation |
| [`simulate_batch()`](batch.md) | Run multiple simulations in parallel |
| [`find_energyplus()`](runner.md) | Discover EnergyPlus installation |
| [`SimulationResult`](results.md) | Simulation result container |
| [`SimulationJob`](batch.md) | Job specification for batch runs |
| [`BatchResult`](batch.md) | Aggregated batch results |
| [`SQLResult`](sql.md) | SQL database query interface |
| [`SimulationCache`](cache.md) | Content-addressed result cache |
| [`FileSystem`](fs.md) | Pluggable storage protocol |
| [`S3FileSystem`](fs.md) | Amazon S3 storage backend |

## Module Contents

::: idfkit.simulation
    options:
      show_root_heading: false
      show_source: false
      members_order: source
      filters:
        - "!^_"
