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
result.raise_for_status()  # SimulationError quoting the fatal/severe messages if EnergyPlus failed
print(result.errors.summary())  # counts, plus the fatal and first severe messages
```

## Core API

```python
from idfkit.simulation import (
    simulate,  # sync, single model
    async_simulate,  # async, single model
    simulate_batch,  # sync, multiple jobs
    find_energyplus,  # discover the EnergyPlus install
    EnergyPlusConfig,  # pre-configured install handle
    SimulationCache,  # content-addressed cache
    SimulationJob,  # one job in a batch
    BatchResult,  # results from simulate_batch
    SimulationResult,  # result container — see result-parsing.md
    SimulationProgress,  # progress event payload
)
```

`simulate` is the workhorse. The most useful arguments:

| Argument | Default | Purpose |
|---|---|---|
| `model` | required | `IDFDocument` to simulate. Not mutated. |
| `weather` | `None` | Path to an `.epw` file. `None` is accepted only for a design-day-only run (`design_day=True`, `annual=False`); it is refused for a model with `GroundHeatTransfer:Slab:*` or `GroundHeatTransfer:Basement:*` objects while `expand_objects=True` and `GroundHeatTransfer:Control` sets the matching `run_*_preprocessor` field to `Yes`, and for a run directory that already holds `in.epw`. |
| `output_dir` | temp dir | Where outputs are written. |
| `energyplus` | auto-discover | Pre-built `EnergyPlusConfig` (skip discovery). |
| `expand_objects` | `True` | Run `ExpandObjects` + ground-heat preprocessors as needed. |
| `annual` | `False` | `-a` flag (annual sim, skip design days). Needs a `RunPeriod`: without one EnergyPlus simulates nothing yet exits successfully, so `simulate` raises `SimulationError` before running. `new_document()` and the geometry builders add none. |
| `design_day` | `False` | `-D` flag (design-day only, skip annual). Needs a `SizingPeriod:DesignDay`: without one EnergyPlus stops blaming the weather data input, so `simulate` raises `SimulationError` before running. Add them with `DesignDayManager(ddy).apply_to_model(doc)` or `apply_ashrae_sizing(doc, station)`. |
| `output_suffix` | `"C"` | File-naming style: `"C"` gives `eplus.err`, `eplusTable.htm`; `"L"` (legacy) gives `eplusout.err`, `eplustbl.htm`; `"D"` gives `eplus.err`, `eplus-table.htm`. `result.*_path` finds the file in any style. |
| `readvars` | `False` | Run `ReadVarsESO` to produce `eplus.csv` (`eplusout.csv` with `"L"`). |
| `timeout` | `3600` | Wall-clock seconds for the main EnergyPlus process. |
| `cache` | `None` | `SimulationCache` for content-hash skip. |
| `auto_migrate` | `False` | Forward-migrate the model to match the installed EP version. |
| `on_progress` | `None` | Callback or `"tqdm"` for progress events. |
| `fs` | `None` | `FileSystem` backend (e.g. S3) for storing outputs remotely. |

## Discovering EnergyPlus

```python
from idfkit.simulation import find_energyplus

config = find_energyplus()  # latest installed
config = find_energyplus(version=(24, 1, 0))
print(config.executable, config.version)
```

Discovery checks `$ENERGYPLUS_DIR`, `$PATH`, and standard install locations (`/usr/local/EnergyPlus-*`, `/Applications/EnergyPlus-*`, `C:\EnergyPlusV*`, plus `/opt/eplus` for Claude Code web sessions). Pass the result to `simulate(..., energyplus=config)` to skip rediscovery on every call.

If EnergyPlus is missing, `EnergyPlusNotFoundError` is raised. With `version=`, an install at another version is named in the message and on `.found` as `(version, install_dir)` pairs: drop `version=`, install that release, or migrate the model to an installed one (`simulate(..., auto_migrate=True)`).

## Version handling

`simulate` refuses to run if `model.version` doesn't match the installed EnergyPlus version. Two ways to handle:

```python
# Option 1 — explicit migration before simulate (recommended for production)
from idfkit import migrate

doc = load_idf("v22_model.idf")
doc = migrate(doc, target_version=config.version).migrated_model

# Option 2 — let simulate forward-migrate transparently
result = simulate(doc, "weather.epw", auto_migrate=True)
print(result.migration_report.summary())  # what was changed
```

Backward migration (installed EP older than the model) is never attempted — it raises `VersionMismatchError`. This is what a `new_document()` model hits when the installed EnergyPlus is older than the latest bundled release, since `new_document()` defaults to the latest: build the model at the installed release instead, `new_document(version=idfkit.simulation.find_energyplus().version)`, or install the newer EnergyPlus. The error message names both fixes, and `auto_migrate=True` for an older model.

## Design day vs. annual

```python
from idfkit.weather import DesignDayManager

# Quick smoke-test with the heating/cooling design days only — seconds.
# design_day=True needs SizingPeriod:DesignDay objects (new_document() adds none)
if "SizingPeriod:DesignDay" not in doc:
    DesignDayManager("weather.ddy").apply_to_model(doc)
result = simulate(doc, "weather.epw", design_day=True)

# Design days only, without a weather file (weather defaults to None)
result = simulate(doc, design_day=True)

# Full annual run — minutes. annual=True needs a RunPeriod (new_document() adds none)
if "RunPeriod" not in doc:
    doc.add("RunPeriod", "Annual", begin_month=1, begin_day_of_month=1, end_month=12, end_day_of_month=31)
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
from idfkit.simulation import REFUSED_RUN_DIR, simulate_batch, SimulationJob

jobs = []
for wwr in (0.2, 0.3, 0.4, 0.5):
    variant = doc.copy()
    from idfkit import set_wwr

    set_wwr(variant, wwr=wwr)
    jobs.append(SimulationJob(model=variant, weather="weather.epw", label=f"wwr_{int(wwr * 100)}"))

batch = simulate_batch(jobs, max_workers=4)
for job, result in zip(jobs, batch):
    if result.run_dir == REFUSED_RUN_DIR:
        print(job.label, "refused:", result.stderr)  # EnergyPlus never ran
    else:
        print(job.label, result.errors.summary())
```

`async_simulate_batch` and `async_simulate_batch_stream` give you async/streaming variants. `simulate_batch` runs jobs concurrently on a thread pool (use `max_workers` to cap parallelism); each job is an EnergyPlus subprocess, so threads are all the parallelism it needs and documents never cross a process boundary.

`SimulationJob` takes the per-run `simulate()` options, `auto_migrate=True` among them, so a batch of older models can be migrated per job. `model=` is a loaded document (a path raises `TypeError`; load it first), and `extra_args=` takes a list or tuple, as `simulate()` does. Migration costs seconds per release step, and every variant of a parametric sweep is different content, so for variants of one older seed migrate the seed once with `migrate()` and build the jobs from the migrated model (see "Speed: migrate once, then batch" in [version-migration.md](version-migration.md)). Identical content (one model across many weather files) is migrated once and reused.

`simulate_batch(progress=...)` calls the callback with keywords only, `progress(completed=, total=, label=, success=)`; it is typed as `BatchProgressCallback`, and a callback that cannot take all four is refused before any job runs.

Stopping a batch: Ctrl-C, or any exception raised in the calling thread (a `progress` callback that raises, to abort on the first `success=False`), cancels the queued jobs and kills the running EnergyPlus processes (and any ExpandObjects/Slab/Basement preprocessor or `auto_migrate` transition step) before it propagates. Cancelling an `async_simulate()` or `async_simulate_batch()` task (`asyncio.wait_for`, a dropped web request) kills its EnergyPlus and preprocessor processes too. Leaving `async for ... in async_simulate_batch_stream(...)` early cancels the rest once the generator is closed; wrap it in `contextlib.aclosing(...)` to close it at the `break` rather than when it is garbage-collected.

A job that fails never raises out of the batch: its result has `success=False` and the reason in `result.stderr`. A job for which `simulate()` raised (refused before EnergyPlus ran, for example `weather=None` on a job that is not design-day-only, or EnergyPlus not found) has the reason in `result.refusal`: its repr reads `SimulationResult(refused: '...')`, its `errors` hold one fatal `refused: ...` message, `raise_for_status()` raises `SimulationError("Simulation refused: ...")`, and no output file is read from its `run_dir`. A job that raised after EnergyPlus wrote to its `output_dir` (a timeout) is not a refusal: its `errors` read that run's `.err`. One that named no `output_dir` gets `run_dir == REFUSED_RUN_DIR`, a placeholder that is never created. With `fs=`, every job needs an `output_dir`: `simulate_batch` and `async_simulate_batch` raise `ValueError` before any job runs otherwise.

## Caching

If you re-simulate the same model + weather + flags often (e.g. iterating on output processing), wrap in a `SimulationCache`:

```python
from idfkit.simulation import SimulationCache

cache = SimulationCache(cache_dir=".sim_cache")
result = simulate(doc, "weather.epw", cache=cache)  # first call runs
result = simulate(doc, "weather.epw", cache=cache)  # second call cache-hits, milliseconds
print(result.cached)  # True: a hit; no output_dir, so run_dir is the read-only cache entry

# Bound it: evict least-recently-used entries after each store, or trim by size/age on demand.
cache = SimulationCache(cache_dir=".sim_cache", max_bytes=5 * 1024**3)
removed = cache.prune(max_bytes=1024**3, max_age=7 * 24 * 3600)  # entries removed
print(cache.size_bytes())
```

The cache key is the SHA-256 of the model, the weather file, the run flags, and the contents of every other file the model names: `Schedule:File` and `Schedule:File:Shading` CSVs, `Table:Lookup` / `Table:IndependentVariable` data files, `Construction:WindowDataFile`, ASHRAE 205 representation files and imported FMUs (the list is derived from the model's schema, so it follows the EnergyPlus version). Any change to any of them is a miss, and restoring a file's earlier content is a hit on the earlier entry. So staging a `Schedule:File` CSV into `output_dir` and varying it across runs caches correctly. A relative file path is resolved the way EnergyPlus resolves it: against `output_dir`, then the EnergyPlus executable's directory.

A model with a `PythonPlugin:Instance`, or with an `ExternalInterface` in `PtolemyServer` or `FunctionalMockupUnitExport` mode, has inputs no key can cover. `simulate` never caches it and logs a warning saying why.

A hit is copied into `output_dir`, exactly where a fresh run would have written, so writing into `result.run_dir` never touches the cache. Without `output_dir` nothing is copied: `result.run_dir` is the cache entry itself, so treat it as read-only (pass `output_dir` if you need to write next to the outputs). `result.cached` is `True` for a hit; its `runtime_seconds` and `exit_code` are those of the run that filled the entry, and `stdout`/`stderr` are empty. Count `result.cached` to report a hit rate.

An entry holds the run's outputs (tens of MB for an annual run) but not the weather file, whose content is already in the key. The cache never shrinks by itself: pass `max_bytes=` to evict the least recently used entries after each store, or call `cache.prune(max_bytes=..., max_age=...)` (seconds since last use) yourself; `cache.size_bytes()` reports the total. A result whose `run_dir` is an evicted entry stops working: a hit read without an `output_dir` returns the entry itself, and a later store in the same batch can evict it, so give runs whose results you keep an `output_dir` (the hit is copied there).

## Progress events

```python
from idfkit.simulation import SimulationProgress


def on_progress(event: SimulationProgress) -> None:
    print(event.phase, event.percent, event.message)


result = simulate(doc, "weather.epw", on_progress=on_progress)

# Or for an interactive shell:
result = simulate(doc, "weather.epw", on_progress="tqdm")  # requires idfkit[progress]
```

Each `SimulationProgress` carries `phase` (`"initializing"`, `"warmup"`, `"simulating"`, `"postprocessing"`, then `"complete"` once EnergyPlus reports success; `"preprocessing"` is in the type but not emitted today), `percent` (0-100 within the current environment, `None` during warmup), `message` (the EnergyPlus line), `environment`, `sim_day` / `sim_total_days`, and `job_index` / `job_label` in a batch. Recent EnergyPlus releases (26.1, for one) do not print a period's end date, so `simulate` reads each environment's length from the model's `RunPeriod` and `SizingPeriod:*` objects to compute `percent`; `percent` restarts at 0 for each design day and run period.

## Remote storage (S3)

```python
from idfkit.simulation import simulate, S3FileSystem

fs = S3FileSystem(bucket="my-sim-outputs")
result = simulate(
    doc,
    "weather.epw",
    output_dir="runs/2026-05-23/baseline",
    fs=fs,
)
# EnergyPlus runs in a local temp dir; outputs are uploaded to s3://my-sim-outputs/runs/2026-05-23/baseline/
```

The weather file must be local — remote weather is not auto-downloaded. Pre-stage with `WeatherDownloader` (see [weather-data.md](weather-data.md)).

With `fs=`, EnergyPlus runs in a local temp directory that is deleted once its outputs are uploaded (the copy of the weather file is not uploaded). Reading `result.sql` then downloads the `.sql` once into a temp file, removed by `result.close()`.

`cache=` combines with `fs=`: the cache stays local, a miss is cached from the local run directory, and a hit uploads the cached outputs to `output_dir`, so the remote folder exists after every call.

## Common mistakes

!!! failure "running without checking the version"

    ```python
    result = simulate(doc, "weather.epw")      # VersionMismatchError if EP version != model version
    ```

!!! success "use `auto_migrate=True` or migrate explicitly"

    ```python
    result = simulate(doc, "weather.epw", auto_migrate=True)
    ```

!!! failure "assuming `result.sql` always exists"

    ```python
    result = simulate(doc, "weather.epw")
    ts = result.sql.get_timeseries(...)       # AttributeError if SQLite output was disabled
    ```

!!! success "let the runner ensure SQLite output is on"

    ```python
    # simulate() auto-injects Output:SQLite if missing — just access result.sql safely:
    if result.sql:
        ts = result.sql.get_timeseries("Zone Mean Air Temperature", "Office")
    ```

!!! failure "re-running the same simulation across iterations"

    ```python
    for _ in range(10):
        result = simulate(doc, "weather.epw")   # full run each time, even if nothing changed
    ```

!!! success "cache"

    ```python
    cache = SimulationCache(cache_dir=".sim_cache")
    for _ in range(10):
        result = simulate(doc, "weather.epw", cache=cache)  # cache-hits after the first
    ```

!!! failure "silently swallowing simulation errors"

    ```python
    result = simulate(doc, "weather.epw")
    # proceed regardless of result.errors.has_severe()
    ```

!!! success "gate on errors"

    ```python
    result = simulate(doc, "weather.epw")
    if result.errors.has_severe:
        print(result.errors.summary())
        for msg in result.errors.severe:
            print(msg.severity, msg.message)
        raise SystemExit("Simulation failed")
    ```

## Related

- [result-parsing.md](result-parsing.md) — extracting data from `SimulationResult`.
- [weather-data.md](weather-data.md) — getting an `.epw` file.
- [hvac-templates.md](hvac-templates.md) — why `expand_objects=True` matters.
- [version-migration.md](version-migration.md) — when `auto_migrate` runs.
- API docs: [py.idfkit.com/simulation/](https://py.idfkit.com/simulation/)
