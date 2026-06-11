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
--8<-- "docs/snippets/concepts/simulation-architecture/subprocess_execution.py:example"
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
--8<-- "docs/snippets/concepts/simulation-architecture/sqlite_over_eso.py:example"
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
--8<-- "docs/snippets/concepts/simulation-architecture/lazy_loading.py:example"
```

This keeps memory usage low and startup fast, especially for batch
simulations where you might only need specific outputs.

## Model Immutability

The `simulate()` function **copies** your model before simulation:

```python
--8<-- "docs/snippets/concepts/simulation-architecture/model_immutability.py:example"
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
4. **`/opt/eplus`** — Standard install location in Claude Code web sessions
5. **Platform defaults**:
    - macOS: `/Applications/EnergyPlus-*/`
    - Linux: `/usr/local/EnergyPlus-*/`
    - Windows: `C:\EnergyPlusV*/`

When multiple versions are found in the default directories, the most
recent version is selected.

```python
--8<-- "docs/snippets/concepts/simulation-architecture/energyplus_discovery.py:example"
```

## Concurrent Execution

For parametric studies, `simulate_batch()` runs simulations in parallel
using a thread pool:

```python
--8<-- "docs/snippets/concepts/simulation-architecture/concurrent_execution.py:example"
```

Each simulation runs in its own subprocess and directory, so there are
no conflicts between concurrent runs.

## Async Execution

The async simulation API (`async_simulate`, `async_simulate_batch`,
`async_simulate_batch_stream`) provides non-blocking counterparts to the
sync API using Python's `asyncio` module.

### Why Async?

The sync API blocks the calling thread during `subprocess.run()`.  This is
fine for scripts but problematic when:

- Running inside an async web server (FastAPI, aiohttp)
- Mixing simulations with other async I/O (network, database)
- Wanting streaming progress without callbacks

### How It Works

The async runner replaces `subprocess.run()` with
`asyncio.create_subprocess_exec()`.  All preparation steps (model copy,
directory setup, cache lookup) are synchronous and fast — only the
EnergyPlus subprocess execution is truly async.

Preprocessing (ExpandObjects, Slab, Basement) uses `subprocess.run()`
internally.  Rather than rewriting the entire preprocessor stack, these
are delegated to a thread via `asyncio.to_thread()` so they don't block
the event loop.

### Concurrency Model

| API | Concurrency mechanism |
|-----|----------------------|
| `simulate_batch()` | `ThreadPoolExecutor` with `max_workers` |
| `async_simulate_batch()` | `asyncio.Semaphore` with `max_concurrent` |

Both achieve the same effect: limiting the number of concurrent EnergyPlus
subprocesses to avoid overwhelming the system.

### Streaming

`async_simulate_batch_stream()` uses an `asyncio.Queue` to decouple
producer tasks from the consumer's `async for` loop.  Events arrive in
completion order.  Breaking out of the loop cancels remaining tasks.

```python
--8<-- "docs/snippets/concepts/simulation-architecture/streaming.py:example"
```

## See Also

- [Caching Strategy](caching.md) — Content-addressed result caching
- [Cloud & Remote Storage](cloud-storage.md) — S3 and custom backends
- [Running Simulations](../simulation/running.md) — Practical guide
