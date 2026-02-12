# Async Simulation

The async simulation API provides non-blocking counterparts to `simulate()`
and `simulate_batch()`, built on Python's `asyncio` module.  Use these when
you need to run EnergyPlus simulations inside an async application (FastAPI,
Jupyter async, event-driven orchestrators) or when you want streaming
progress without callbacks.

## When to Use Async vs Sync

| Scenario | Recommended |
|----------|-------------|
| Scripts, CLI tools | `simulate()` / `simulate_batch()` |
| Async web servers (FastAPI, aiohttp) | `async_simulate()` / `async_simulate_batch()` |
| Real-time progress UI without callbacks | `async_simulate_batch_stream()` |
| Jupyter with `await` support | Either — async avoids blocking the notebook |
| Mixing simulations with other async I/O | `async_simulate()` |

## Basic Usage

```python
--8<-- "docs/snippets/simulation/async/basic_usage.py:example"
```

`async_simulate()` accepts exactly the same parameters as `simulate()` and
returns the same `SimulationResult`.  The only difference is that EnergyPlus
runs as an `asyncio` subprocess, so the event loop is free to do other work
while waiting.

## Async Batch Processing

`async_simulate_batch()` mirrors `simulate_batch()` but uses an
`asyncio.Semaphore` for concurrency control instead of a thread pool:

```python
--8<-- "docs/snippets/simulation/async/async_batch_processing.py:example"
```

Results are returned in the same order as the input jobs, identical to
`simulate_batch()`.

### Concurrency

Control how many simulations run at once:

```python
# Use all CPUs (default)
batch = await async_simulate_batch(jobs)

# Limit to 4 concurrent simulations
batch = await async_simulate_batch(jobs, max_concurrent=4)

# Sequential (useful for debugging)
batch = await async_simulate_batch(jobs, max_concurrent=1)
```

Default: `min(len(jobs), os.cpu_count())`

## Streaming Progress

`async_simulate_batch_stream()` is an async generator that yields
`SimulationEvent` objects as each simulation completes — no callbacks needed:

```python
--8<-- "docs/snippets/simulation/async/streaming_progress.py:example"
```

### SimulationEvent

Each event contains:

| Attribute | Type | Description |
|-----------|------|-------------|
| `index` | `int` | Position of this job in the original sequence |
| `label` | `str` | Human-readable label from `SimulationJob` |
| `result` | `SimulationResult` | The simulation result |
| `completed` | `int` | Number of jobs completed so far |
| `total` | `int` | Total number of jobs |

Events arrive in **completion order**, not submission order.  Use `event.index`
to map back to the original job.

### Early Termination

Breaking out of the stream cancels remaining simulations:

```python
--8<-- "docs/snippets/simulation/async/early_termination.py:example"
```

## Cancellation

Async tasks support cancellation natively.  Cancelling a task kills the
underlying EnergyPlus subprocess:

```python
--8<-- "docs/snippets/simulation/async/cancellation.py:example"
```

## Parametric Study

Create model variants and analyze results — the async equivalent of the
pattern shown in [Batch Processing](batch.md#parametric-studies):

```python
--8<-- "docs/snippets/simulation/async/parametric_study.py:example"
```

## Running Simulations Alongside Other Async Work

A key benefit of the async API is running simulations concurrently with
other I/O-bound tasks — database queries, HTTP requests, file uploads —
without blocking:

```python
--8<-- "docs/snippets/simulation/async/running_simulations_alongside_other_async_work.py:example"
```

## Collecting Streaming Results

The streaming API yields events in completion order.  To collect and
reorder results for analysis:

```python
--8<-- "docs/snippets/simulation/async/collecting_streaming_results.py:example"
```

## Caching and Cloud Storage

All async functions accept the same `cache` and `fs` parameters as their
sync counterparts.  For best results in async code, use an `AsyncFileSystem`
to avoid blocking the event loop during file uploads and result reads:

```python
from idfkit.simulation import SimulationCache, AsyncLocalFileSystem

cache = SimulationCache()
fs = AsyncLocalFileSystem()

result = await async_simulate(
    model, "weather.epw",
    cache=cache,
    output_dir="run-001",
    fs=fs,
)

# Use async accessors to read results without blocking
errors = await result.async_errors()
sql = await result.async_sql()
```

For S3 storage, use `AsyncS3FileSystem` (requires `pip install idfkit[async-s3]`):

```python
from idfkit.simulation import AsyncS3FileSystem, SimulationCache

cache = SimulationCache()

async with AsyncS3FileSystem(bucket="my-bucket", prefix="study/") as fs:
    result = await async_simulate(
        model, "weather.epw",
        cache=cache,
        output_dir="run-001",
        fs=fs,
    )
```

A sync `FileSystem` (e.g., `S3FileSystem`) is still accepted — the upload
step is automatically wrapped in `asyncio.to_thread()` so it doesn't block
the event loop.  However, using `AsyncFileSystem` is recommended because it
provides true non-blocking I/O for both uploads *and* result reads (via the
`async_errors()`, `async_sql()`, etc. accessors), and avoids thread-pool
overhead.

## FastAPI Integration

A minimal example of an async simulation endpoint:

```python
--8<-- "docs/snippets/simulation/async/fastapi_integration.py:example"
```

Because `async_simulate` doesn't block the event loop, the server remains
responsive to other requests while EnergyPlus runs.

## Preprocessing

When `expand_objects=True` (the default), the Slab and Basement
preprocessors run in a background thread via `asyncio.to_thread()` so they
don't block the event loop.  This is transparent — no user action required.

## Error Handling

Error handling is identical to the sync API:

```python
from idfkit.exceptions import SimulationError

try:
    result = await async_simulate(model, weather, timeout=60)
except SimulationError as e:
    if e.exit_code is None:
        print("Simulation timed out")
    else:
        print(f"Failed: {e}")
```

In batch mode, individual failures are captured in the results — the batch
never raises due to a single job failing.

## See Also

- [Running Simulations](running.md) — Sync simulation guide
- [Batch Processing](batch.md) — Sync batch guide
- [Simulation Architecture](../concepts/simulation-architecture.md) — Design decisions
