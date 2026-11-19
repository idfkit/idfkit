# Simulation execution

`idfkit.simulation` wraps the EnergyPlus executable as a subprocess. You pass an `IDFDocument` and a weather file; it writes the model to a run directory, optionally runs `ExpandObjects` and ground-heat preprocessors, invokes EnergyPlus, and returns a `SimulationResult` pointing at the outputs.

## When to use

- You want to run a single simulation against a weather file.
- You're running parameter sweeps (use `simulate_batch` / `async_simulate_batch`).
- You need progress events streaming back as EnergyPlus runs.
- You want results cached by content hash to skip re-running unchanged inputs.

## Quick start

```python
--8<-- "agent_references/snippets/simulation-execution.py:quickstart"
```

## Core API

```python
--8<-- "agent_references/snippets/simulation-execution.py:core-api"
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
--8<-- "agent_references/snippets/simulation-execution.py:discover"
```

Discovery checks `$ENERGYPLUS_DIR`, `$PATH`, and standard install locations (`/usr/local/EnergyPlus-*`, `/Applications/EnergyPlus-*`, `C:\EnergyPlusV*`, plus `/opt/eplus` for Claude Code web sessions). Pass the result to `simulate(..., energyplus=config)` to skip rediscovery on every call.

If EnergyPlus is missing, `EnergyPlusNotFoundError` is raised.

## Version handling

`simulate` refuses to run if `model.version` doesn't match the installed EnergyPlus version. Two ways to handle:

```python
--8<-- "agent_references/snippets/simulation-execution.py:version-handling"
```

Backward migration (installed EP older than the model) is never attempted — it raises `VersionMismatchError`. This is what a `new_document()` model hits when the installed EnergyPlus is older than the latest bundled release, since `new_document()` defaults to the latest: build the model at the installed release instead, `new_document(version=idfkit.simulation.find_energyplus().version)`, or install the newer EnergyPlus. The error message names both fixes, and `auto_migrate=True` for an older model.

## Design day vs. annual

```python
--8<-- "agent_references/snippets/simulation-execution.py:design-day-vs-annual"
```

## Async

For UI loops or asyncio-based batch tooling:

```python
--8<-- "agent_references/snippets/simulation-execution.py:async"
```

## Batch parameter sweeps

```python
--8<-- "agent_references/snippets/simulation-execution.py:batch"
```

`async_simulate_batch` and `async_simulate_batch_stream` give you async/streaming variants. `simulate_batch` runs jobs concurrently on a thread pool (use `max_workers` to cap parallelism); each job is an EnergyPlus subprocess, so threads are all the parallelism it needs and documents never cross a process boundary.

`SimulationJob` takes the per-run `simulate()` options, `auto_migrate=True` among them, so a batch of older models can be migrated per job. `model=` is a loaded document (a path raises `TypeError`; load it first), and `extra_args=` takes a list or tuple, as `simulate()` does. Migration costs seconds per release step, and every variant of a parametric sweep is different content, so for variants of one older seed migrate the seed once with `migrate()` and build the jobs from the migrated model (see "Speed: migrate once, then batch" in [version-migration.md](version-migration.md)). Identical content (one model across many weather files) is migrated once and reused.

`simulate_batch(progress=...)` calls the callback with keywords only, `progress(completed=, total=, label=, success=)`; it is typed as `BatchProgressCallback`, and a callback that cannot take all four is refused before any job runs.

A job that fails never raises out of the batch: its result has `success=False` and the reason in `result.stderr`. A job for which `simulate()` raised (refused before EnergyPlus ran, for example `weather=None` on a job that is not design-day-only, or EnergyPlus not found) has the reason in `result.refusal`: its repr reads `SimulationResult(refused: '...')`, its `errors` hold one fatal `refused: ...` message, `raise_for_status()` raises `SimulationError("Simulation refused: ...")`, and no output file is read from its `run_dir`. A job that raised after EnergyPlus wrote to its `output_dir` (a timeout) is not a refusal: its `errors` read that run's `.err`. One that named no `output_dir` gets `run_dir == REFUSED_RUN_DIR`, a placeholder that is never created. With `fs=`, every job needs an `output_dir`: `simulate_batch` and `async_simulate_batch` raise `ValueError` before any job runs otherwise.

## Caching

If you re-simulate the same model + weather + flags often (e.g. iterating on output processing), wrap in a `SimulationCache`:

```python
--8<-- "agent_references/snippets/simulation-execution.py:caching"
```

The cache key is the SHA-256 of the model, the weather file, the run flags, and the contents of every other file the model names: `Schedule:File` and `Schedule:File:Shading` CSVs, `Table:Lookup` / `Table:IndependentVariable` data files, `Construction:WindowDataFile`, ASHRAE 205 representation files and imported FMUs (the list is derived from the model's schema, so it follows the EnergyPlus version). Any change to any of them is a miss, and restoring a file's earlier content is a hit on the earlier entry. So staging a `Schedule:File` CSV into `output_dir` and varying it across runs caches correctly. A relative file path is resolved the way EnergyPlus resolves it: against `output_dir`, then the EnergyPlus executable's directory.

A model with a `PythonPlugin:Instance`, or with an `ExternalInterface` in `PtolemyServer` or `FunctionalMockupUnitExport` mode, has inputs no key can cover. `simulate` never caches it and logs a warning saying why.

A hit is copied into `output_dir`, exactly where a fresh run would have written, so writing into `result.run_dir` never touches the cache. Without `output_dir` nothing is copied: `result.run_dir` is the cache entry itself, so treat it as read-only (pass `output_dir` if you need to write next to the outputs). `result.cached` is `True` for a hit; its `runtime_seconds` and `exit_code` are those of the run that filled the entry, and `stdout`/`stderr` are empty. Count `result.cached` to report a hit rate.

## Progress events

```python
--8<-- "agent_references/snippets/simulation-execution.py:progress"
```

Each `SimulationProgress` carries `phase` (`"initializing"`, `"warmup"`, `"simulating"`, `"postprocessing"`, then `"complete"` once EnergyPlus reports success; `"preprocessing"` is in the type but not emitted today), `percent` (0-100 within the current environment, `None` during warmup), `message` (the EnergyPlus line), `environment`, `sim_day` / `sim_total_days`, and `job_index` / `job_label` in a batch. Recent EnergyPlus releases (26.1, for one) do not print a period's end date, so `simulate` reads each environment's length from the model's `RunPeriod` and `SizingPeriod:*` objects to compute `percent`; `percent` restarts at 0 for each design day and run period.

## Remote storage (S3)

```python
--8<-- "agent_references/snippets/simulation-execution.py:remote-s3"
```

The weather file must be local — remote weather is not auto-downloaded. Pre-stage with `WeatherDownloader` (see [weather-data.md](weather-data.md)).

`cache=` combines with `fs=`: the cache stays local, a miss is cached from the local run directory, and a hit uploads the cached outputs to `output_dir`, so the remote folder exists after every call.

## Common mistakes

!!! failure "running without checking the version"

    ```python
    result = simulate(doc, "weather.epw")      # VersionMismatchError if EP version != model version
    ```

!!! success "use `auto_migrate=True` or migrate explicitly"

    ```python
    --8<-- "agent_references/snippets/simulation-execution.py:mistake-version-good"
    ```

!!! failure "assuming `result.sql` always exists"

    ```python
    result = simulate(doc, "weather.epw")
    ts = result.sql.get_timeseries(...)       # AttributeError if SQLite output was disabled
    ```

!!! success "let the runner ensure SQLite output is on"

    ```python
    --8<-- "agent_references/snippets/simulation-execution.py:mistake-sql-good"
    ```

!!! failure "re-running the same simulation across iterations"

    ```python
    for _ in range(10):
        result = simulate(doc, "weather.epw")   # full run each time, even if nothing changed
    ```

!!! success "cache"

    ```python
    --8<-- "agent_references/snippets/simulation-execution.py:mistake-rerun-good"
    ```

!!! failure "silently swallowing simulation errors"

    ```python
    result = simulate(doc, "weather.epw")
    # proceed regardless of result.errors.has_severe()
    ```

!!! success "gate on errors"

    ```python
    --8<-- "agent_references/snippets/simulation-execution.py:mistake-errors-good"
    ```

## Related

- [result-parsing.md](result-parsing.md) — extracting data from `SimulationResult`.
- [weather-data.md](weather-data.md) — getting an `.epw` file.
- [hvac-templates.md](hvac-templates.md) — why `expand_objects=True` matters.
- [version-migration.md](version-migration.md) — when `auto_migrate` runs.
- API docs: [py.idfkit.com/simulation/](https://py.idfkit.com/simulation/)
