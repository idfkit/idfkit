# Simulation execution

`idfkit.simulation` wraps the EnergyPlus executable as a subprocess. You pass an `IDFDocument` and a weather file; it writes the model to a run directory, optionally runs `ExpandObjects` and ground-heat preprocessors, invokes EnergyPlus, and returns a `SimulationResult` pointing at the outputs.

## When to use

- You want to run a single simulation against a weather file.
- You're running parameter sweeps (use `simulate_batch` / `async_simulate_batch`).
- You need progress events streaming back as EnergyPlus runs.
- You want results cached by content hash to skip re-running unchanged inputs.

## Quick start

```python
--8<-- "docs/snippets/agent_references/simulation-execution.py:quickstart"
```

## Core API

```python
--8<-- "docs/snippets/agent_references/simulation-execution.py:core-api"
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
--8<-- "docs/snippets/agent_references/simulation-execution.py:discover"
```

Discovery checks `$ENERGYPLUS_DIR`, `$PATH`, and standard install locations (`/usr/local/EnergyPlus-*`, `/Applications/EnergyPlus-*`, `C:\EnergyPlusV*`, plus `/opt/eplus` for Claude Code web sessions). Pass the result to `simulate(..., energyplus=config)` to skip rediscovery on every call.

If EnergyPlus is missing, `EnergyPlusNotFoundError` is raised.

## Version handling

`simulate` refuses to run if `model.version` doesn't match the installed EnergyPlus version. Two ways to handle:

```python
--8<-- "docs/snippets/agent_references/simulation-execution.py:version-handling"
```

Backward migration (installed EP older than the model) is never attempted — it raises `VersionMismatchError`.

## Design day vs. annual

```python
--8<-- "docs/snippets/agent_references/simulation-execution.py:design-day-vs-annual"
```

## Async

For UI loops or asyncio-based batch tooling:

```python
--8<-- "docs/snippets/agent_references/simulation-execution.py:async"
```

## Batch parameter sweeps

```python
--8<-- "docs/snippets/agent_references/simulation-execution.py:batch"
```

`async_simulate_batch` and `async_simulate_batch_stream` give you async/streaming variants. `simulate_batch` runs jobs in parallel processes (use `max_workers` to cap parallelism).

## Caching

If you re-simulate the same model + weather + flags often (e.g. iterating on output processing), wrap in a `SimulationCache`:

```python
--8<-- "docs/snippets/agent_references/simulation-execution.py:caching"
```

The cache key is the SHA-256 of the (model bytes + weather bytes + flags) tuple. Any change invalidates the entry.

## Progress events

```python
--8<-- "docs/snippets/agent_references/simulation-execution.py:progress"
```

Events carry `phase` (warmup/run/postprocessing), `percent` (where known), the EnergyPlus message, and the timestamp.

## Remote storage (S3)

```python
--8<-- "docs/snippets/agent_references/simulation-execution.py:remote-s3"
```

The weather file must be local — remote weather is not auto-downloaded. Pre-stage with `WeatherDownloader` (see [weather-data.md](weather-data.md)).

## Common mistakes

!!! failure "running without checking the version"

    ```python
    result = simulate(doc, "weather.epw")      # VersionMismatchError if EP version != model version
    ```

!!! success "use `auto_migrate=True` or migrate explicitly"

    ```python
    --8<-- "docs/snippets/agent_references/simulation-execution.py:mistake-version-good"
    ```

!!! failure "assuming `result.sql` always exists"

    ```python
    result = simulate(doc, "weather.epw")
    ts = result.sql.get_timeseries(...)       # AttributeError if SQLite output was disabled
    ```

!!! success "let the runner ensure SQLite output is on"

    ```python
    --8<-- "docs/snippets/agent_references/simulation-execution.py:mistake-sql-good"
    ```

!!! failure "re-running the same simulation across iterations"

    ```python
    for _ in range(10):
        result = simulate(doc, "weather.epw")   # full run each time, even if nothing changed
    ```

!!! success "cache"

    ```python
    --8<-- "docs/snippets/agent_references/simulation-execution.py:mistake-rerun-good"
    ```

!!! failure "silently swallowing simulation errors"

    ```python
    result = simulate(doc, "weather.epw")
    # proceed regardless of result.errors.has_severe()
    ```

!!! success "gate on errors"

    ```python
    --8<-- "docs/snippets/agent_references/simulation-execution.py:mistake-errors-good"
    ```

## Related

- [result-parsing.md](result-parsing.md) — extracting data from `SimulationResult`.
- [weather-data.md](weather-data.md) — getting an `.epw` file.
- [hvac-templates.md](hvac-templates.md) — why `expand_objects=True` matters.
- [version-migration.md](version-migration.md) — when `auto_migrate` runs.
- API docs: [py.idfkit.com/simulation/](https://py.idfkit.com/simulation/)
