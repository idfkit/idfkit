# Simulation execution

`idfkit.simulation` wraps the EnergyPlus executable as a subprocess. You pass an `IDFDocument` and a weather file; it writes the model to a run directory, optionally runs `ExpandObjects` and ground-heat preprocessors, invokes EnergyPlus, and returns a `SimulationResult` pointing at the outputs.

## When to use

- You want to run a single simulation against a weather file.
- You're running parameter sweeps (use `simulate_batch` / `async_simulate_batch`).
- You need progress events streaming back as EnergyPlus runs.
- You want results cached by content hash to skip re-running unchanged inputs.

## Quick start

```python
from idfkit import load_idf
from idfkit.simulation import simulate

doc = load_idf("building.idf")
result = simulate(doc, "weather.epw", design_day=True)
print(result.errors.summary())
```

## Core API

```python
from idfkit.simulation import (
    simulate,                # sync, single model
    async_simulate,          # async, single model
    simulate_batch,          # sync, multiple jobs
    async_simulate_batch,    # async, multiple jobs
    find_energyplus,         # discover the EnergyPlus install
    EnergyPlusConfig,        # pre-configured install handle
    SimulationCache,         # content-addressed cache
    SimulationJob,           # one job in a batch
    BatchResult,             # results from simulate_batch
    SimulationResult,        # result container — see result-parsing.md
    SimulationProgress,      # progress event payload
)
```

`simulate` is the workhorse. The most useful arguments:

| Argument | Default | Purpose |
|---|---|---|
| `model` | required | `IDFDocument` to simulate. Not mutated. |
| `weather` | required | Path to an `.epw` file. |
| `output_dir` | temp dir | Where outputs are written. |
| `energyplus` | auto-discover | Pre-built `EnergyPlusConfig` (skip discovery). |
| `expand_objects` | `True` | Run `ExpandObjects` + ground-heat preprocessors as needed. |
| `annual` | `False` | `-a` flag (annual sim, skip design days). |
| `design_day` | `False` | `-D` flag (design-day only, skip annual). |
| `output_suffix` | `"C"` | Combined-table output. `"L"` for legacy, `"D"` for timestamped. |
| `readvars` | `False` | Run `ReadVarsESO` to produce `eplusout.csv`. |
| `timeout` | `3600` | Wall-clock seconds for the main EnergyPlus process. |
| `cache` | `None` | `SimulationCache` for content-hash skip. |
| `auto_migrate` | `False` | Forward-migrate the model to match the installed EP version. |
| `on_progress` | `None` | Callback or `"tqdm"` for progress events. |
| `fs` | `None` | `FileSystem` backend (e.g. S3) for storing outputs remotely. |

## Discovering EnergyPlus

```python
from idfkit.simulation import find_energyplus

config = find_energyplus()                 # latest installed
config = find_energyplus(version=(24, 1, 0))
print(config.executable, config.version)
```

Discovery checks `$ENERGYPLUS_DIR`, `$PATH`, and standard install locations (`/usr/local/EnergyPlus-*`, `/Applications/EnergyPlus-*`, `C:\EnergyPlusV*`). Pass the result to `simulate(..., energyplus=config)` to skip rediscovery on every call.

If EnergyPlus is missing, `EnergyPlusNotFoundError` is raised.

## Version handling

`simulate` refuses to run if `model.version` doesn't match the installed EnergyPlus version. Two ways to handle:

```python
# Option 1 — explicit migration before simulate (recommended for production)
from idfkit import migrate
doc = load_idf("v22_model.idf")
doc = migrate(doc, target_version=config.version).migrated_model

# Option 2 — let simulate forward-migrate transparently
result = simulate(doc, "weather.epw", auto_migrate=True)
print(result.migration_report.summary())   # what was changed
```

Backward migration (installed EP older than the model) is never attempted — it raises `VersionMismatchError`.

## Design day vs. annual

```python
# Quick smoke-test with the heating/cooling design days only — seconds
result = simulate(doc, "weather.epw", design_day=True)

# Full annual run — minutes
result = simulate(doc, "weather.epw", annual=True)

# Default (both flags False) — EnergyPlus's default, governed by SimulationControl in the IDF
result = simulate(doc, "weather.epw")
```

## Async

For UI loops or asyncio-based batch tooling:

```python
import asyncio
from idfkit.simulation import async_simulate

async def main():
    result = await async_simulate(doc, "weather.epw")
    print(result.errors.summary())

asyncio.run(main())
```

## Batch parameter sweeps

```python
from idfkit.simulation import simulate_batch, SimulationJob

jobs = []
for wwr in (0.2, 0.3, 0.4, 0.5):
    variant = doc.copy()
    from idfkit import set_wwr
    set_wwr(variant, wwr=wwr)
    jobs.append(SimulationJob(model=variant, weather="weather.epw", label=f"wwr_{int(wwr*100)}"))

batch = simulate_batch(jobs, max_workers=4)
for job, result in zip(jobs, batch.results):
    print(job.label, result.errors.summary())
```

`async_simulate_batch` and `async_simulate_batch_stream` give you async/streaming variants. `simulate_batch` runs jobs in parallel processes (use `max_workers` to cap parallelism).

## Caching

If you re-simulate the same model + weather + flags often (e.g. iterating on output processing), wrap in a `SimulationCache`:

```python
from idfkit.simulation import SimulationCache

cache = SimulationCache(cache_dir=".sim_cache")
result = simulate(doc, "weather.epw", cache=cache)   # first call runs
result = simulate(doc, "weather.epw", cache=cache)   # second call cache-hits, milliseconds
```

The cache key is the SHA-256 of the (model bytes + weather bytes + flags) tuple. Any change invalidates the entry.

## Progress events

```python
from idfkit.simulation import SimulationProgress

def on_progress(event: SimulationProgress) -> None:
    print(event.phase, event.percent, event.message)

result = simulate(doc, "weather.epw", on_progress=on_progress)

# Or for an interactive shell:
result = simulate(doc, "weather.epw", on_progress="tqdm")   # requires idfkit[progress]
```

Events carry `phase` (warmup/run/postprocessing), `percent` (where known), the EnergyPlus message, and the timestamp.

## Remote storage (S3)

```python
from idfkit.simulation import simulate, S3FileSystem

fs = S3FileSystem(bucket="my-sim-outputs")
result = simulate(
    doc, "weather.epw",
    output_dir="runs/2026-05-23/baseline",
    fs=fs,
)
# EnergyPlus runs in a local temp dir; outputs are uploaded to s3://my-sim-outputs/runs/2026-05-23/baseline/
```

The weather file must be local — remote weather is not auto-downloaded. Pre-stage with `WeatherDownloader` (see [weather-data.md](weather-data.md)).

## Common mistakes

**BAD — running without checking the version**

```python
result = simulate(doc, "weather.epw")      # VersionMismatchError if EP version != model version
```

**GOOD — use `auto_migrate=True` or migrate explicitly**

```python
result = simulate(doc, "weather.epw", auto_migrate=True)
```

**BAD — assuming `result.sql` always exists**

```python
result = simulate(doc, "weather.epw")
ts = result.sql.get_timeseries(...)       # AttributeError if SQLite output was disabled
```

**GOOD — let the runner ensure SQLite output is on**

```python
# simulate() auto-injects Output:SQLite if missing — just access result.sql safely:
if result.sql:
    ts = result.sql.get_timeseries(...)
```

**BAD — re-running the same simulation across iterations**

```python
for _ in range(10):
    result = simulate(doc, "weather.epw")   # full run each time, even if nothing changed
```

**GOOD — cache**

```python
cache = SimulationCache(cache_dir=".sim_cache")
for _ in range(10):
    result = simulate(doc, "weather.epw", cache=cache)   # cache-hits after the first
```

**BAD — silently swallowing simulation errors**

```python
result = simulate(doc, "weather.epw")
# proceed regardless of result.errors.has_severe()
```

**GOOD — gate on errors**

```python
result = simulate(doc, "weather.epw")
if result.errors.has_severe():
    print(result.errors.summary())
    for msg in result.errors.severe():
        print(msg)
    raise SystemExit("Simulation failed")
```

## Related

- [result-parsing.md](result-parsing.md) — extracting data from `SimulationResult`.
- [weather-data.md](weather-data.md) — getting an `.epw` file.
- [hvac-templates.md](hvac-templates.md) — why `expand_objects=True` matters.
- [version-migration.md](version-migration.md) — when `auto_migrate` runs.
- API docs: [py.idfkit.com/simulation/](https://py.idfkit.com/simulation/)
