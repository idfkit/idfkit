# Simulation Architecture

This page explains the design decisions behind idfkit's simulation module
and why certain approaches were chosen.

## Subprocess Execution

idfkit runs EnergyPlus as a **subprocess** rather than linking to its
libraries directly. This approach has several benefits:

- **Isolation** — Each simulation runs in its own directory with clean state
- **Compatibility** — Works with any EnergyPlus version (8.9+)
- **Robustness** — Crashes in EnergyPlus don't crash your Python process
- **Simplicity** — No C++ bindings or version-specific compilation needed

The `simulate()` function:

1. Creates an isolated temporary directory
2. Copies the model (as IDF) and weather file
3. Injects `Output:SQLite` if not present
4. Invokes the EnergyPlus executable
5. Returns a `SimulationResult` with access to all outputs

```python
from idfkit.simulation import simulate

result = simulate(model, "weather.epw", design_day=True)
print(f"Outputs in: {result.run_dir}")
```

## SQLite Over ESO

idfkit's result parsers focus on the **SQLite output database** rather than
the traditional ESO/MTR text files. The SQLite format:

- Contains **all** simulation data in one queryable file
- Provides **structured access** to time-series and tabular data
- Is **faster to parse** than text formats
- Includes **metadata** (environments, variables, units)

The module automatically ensures `Output:SQLite` is present in your model,
so you don't need to add it manually.

```python
# All time-series data is accessible via SQL queries
ts = result.sql.get_timeseries(
    variable_name="Zone Mean Air Temperature",
    key_value="ZONE 1",
)

# Tabular reports (normally in HTML) are also in SQLite
tables = result.sql.get_tabular_data("AnnualBuildingUtilityPerformanceSummary")
```

### What About ESO/HTML?

The following output formats are **not parsed** because SQLite provides the
same data more reliably:

| Format | Alternative |
|--------|-------------|
| ESO/MTR (time-series) | `result.sql.get_timeseries()` |
| HTML (tabular reports) | `result.sql.get_tabular_data()` |
| EIO (metadata) | SQLite metadata tables |

If you have a specific need for these formats, please open an issue.

## Lazy Loading

`SimulationResult` uses **lazy loading** — output files are only parsed when
you access them:

```python
result = simulate(model, weather)  # Fast: just runs EnergyPlus

# These are lazy — parsed on first access:
result.errors    # Parses ERR file
result.sql       # Opens SQLite database
result.variables # Parses RDD file
```

This keeps memory usage low and startup fast, especially for batch
simulations where you might only need specific outputs.

## Model Immutability

The `simulate()` function **copies** your model before simulation:

```python
result = simulate(model, weather)

# model is unchanged — Output:SQLite was added to a copy
assert "Output:SQLite" not in model
```

This ensures:

- Your original model isn't mutated
- Multiple simulations can run concurrently with the same base model
- No unexpected side effects

## EnergyPlus Discovery

idfkit auto-discovers EnergyPlus installations using a priority chain:

1. **Explicit path** — Pass `energyplus_dir` to `simulate()` or `find_energyplus()`
2. **Environment variable** — Set `ENERGYPLUS_DIR`
3. **System PATH** — Looks for `energyplus` executable
4. **Platform defaults**:
    - macOS: `/Applications/EnergyPlus-*/`
    - Linux: `/usr/local/EnergyPlus-*/`
    - Windows: `C:\EnergyPlusV*/`

When multiple versions are found in the default directories, the most
recent version is selected.

```python
from idfkit.simulation import find_energyplus

config = find_energyplus()
print(f"Version: {config.version}")
print(f"Path: {config.executable}")
```

## Concurrent Execution

For parametric studies, `simulate_batch()` runs simulations in parallel
using a thread pool:

```python
from idfkit.simulation import simulate_batch, SimulationJob

jobs = [
    SimulationJob(model=variant1, weather="weather.epw", label="case-1"),
    SimulationJob(model=variant2, weather="weather.epw", label="case-2"),
]

batch = simulate_batch(jobs, max_workers=4)
```

Each simulation runs in its own subprocess and directory, so there are
no conflicts between concurrent runs.

## See Also

- [Caching Strategy](caching.md) — Content-addressed result caching
- [Cloud & Remote Storage](cloud-storage.md) — S3 and custom backends
- [Running Simulations](../simulation/running.md) — Practical guide
