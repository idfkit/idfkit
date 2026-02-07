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
import asyncio
from idfkit import load_idf
from idfkit.simulation import async_simulate

async def main():
    model = load_idf("building.idf")
    result = await async_simulate(model, "weather.epw", design_day=True)

    print(f"Success: {result.success}")
    print(f"Runtime: {result.runtime_seconds:.1f}s")

asyncio.run(main())
```

`async_simulate()` accepts exactly the same parameters as `simulate()` and
returns the same `SimulationResult`.  The only difference is that EnergyPlus
runs as an `asyncio` subprocess, so the event loop is free to do other work
while waiting.

## Async Batch Processing

`async_simulate_batch()` mirrors `simulate_batch()` but uses an
`asyncio.Semaphore` for concurrency control instead of a thread pool:

```python
import asyncio
from idfkit.simulation import async_simulate_batch, SimulationJob

async def main():
    jobs = [
        SimulationJob(model=model1, weather="weather.epw", label="baseline"),
        SimulationJob(model=model2, weather="weather.epw", label="improved"),
    ]

    batch = await async_simulate_batch(jobs, max_concurrent=4)

    print(f"Completed: {len(batch.succeeded)}/{len(batch)}")
    for i, result in enumerate(batch):
        print(f"  Job {i}: {'Success' if result.success else 'Failed'}")

asyncio.run(main())
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
import asyncio
from idfkit.simulation import async_simulate_batch_stream, SimulationJob

async def main():
    jobs = [
        SimulationJob(model=variant, weather="weather.epw", label=f"case-{i}")
        for i, variant in enumerate(variants)
    ]

    async for event in async_simulate_batch_stream(jobs, max_concurrent=4):
        status = "OK" if event.result.success else "FAIL"
        print(f"[{event.completed}/{event.total}] {event.label}: {status}")

asyncio.run(main())
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
async for event in async_simulate_batch_stream(jobs, max_concurrent=4):
    if not event.result.success:
        print(f"Job {event.label} failed — aborting remaining")
        break  # Remaining tasks are cancelled automatically
```

## Cancellation

Async tasks support cancellation natively.  Cancelling a task kills the
underlying EnergyPlus subprocess:

```python
async def run_with_timeout():
    task = asyncio.create_task(
        async_simulate(model, "weather.epw")
    )

    try:
        result = await asyncio.wait_for(task, timeout=120)
    except asyncio.TimeoutError:
        print("Simulation cancelled after 120s")
```

## Parametric Study

Create model variants and analyze results — the async equivalent of the
pattern shown in [Batch Processing](batch.md#parametric-studies):

```python
import asyncio
from idfkit.simulation import async_simulate_batch, SimulationJob

async def main():
    # Create variants
    jobs = []
    for insulation in [0.05, 0.10, 0.15, 0.20]:
        variant = model.copy()
        variant["Material"]["Insulation"].thickness = insulation
        jobs.append(SimulationJob(
            model=variant,
            weather="weather.epw",
            label=f"insulation-{insulation}m",
            design_day=True,
        ))

    # Run all variants
    batch = await async_simulate_batch(jobs, max_concurrent=4)

    # Analyze results
    for job, result in zip(jobs, batch):
        if result.success:
            ts = result.sql.get_timeseries(
                "Zone Mean Air Temperature",
                "ZONE 1",
            )
            print(f"{job.label}: Max temp {max(ts.values):.1f}°C")

asyncio.run(main())
```

## Running Simulations Alongside Other Async Work

A key benefit of the async API is running simulations concurrently with
other I/O-bound tasks — database queries, HTTP requests, file uploads —
without blocking:

```python
import asyncio
from idfkit.simulation import async_simulate

async def fetch_weather_data(station_id: str) -> dict:
    """Fetch weather metadata from a remote API."""
    ...

async def main():
    # Run a simulation and an API call concurrently
    sim_task = async_simulate(model, "weather.epw", design_day=True)
    api_task = fetch_weather_data("725300")

    result, weather_meta = await asyncio.gather(sim_task, api_task)

    print(f"Simulation: {result.runtime_seconds:.1f}s")
    print(f"Weather station: {weather_meta}")

asyncio.run(main())
```

## Collecting Streaming Results

The streaming API yields events in completion order.  To collect and
reorder results for analysis:

```python
import asyncio
from idfkit.simulation import async_simulate_batch_stream, SimulationJob

async def main():
    jobs = [
        SimulationJob(model=variant, weather="weather.epw", label=f"case-{i}")
        for i, variant in enumerate(variants)
    ]

    # Collect events and reorder by original index
    results = [None] * len(jobs)
    async for event in async_simulate_batch_stream(jobs, max_concurrent=4):
        results[event.index] = event.result
        pct = event.completed / event.total * 100
        print(f"[{pct:3.0f}%] {event.label}: {'OK' if event.result.success else 'FAIL'}")

    # Results are now in submission order
    for i, result in enumerate(results):
        if result.success:
            ts = result.sql.get_timeseries(
                "Zone Mean Air Temperature", "ZONE 1"
            )
            print(f"Case {i}: max temp {max(ts.values):.1f}°C")

asyncio.run(main())
```

## Caching and Cloud Storage

All async functions accept the same `cache` and `fs` parameters as their
sync counterparts:

```python
from idfkit.simulation import SimulationCache, S3FileSystem

cache = SimulationCache()
fs = S3FileSystem(bucket="my-bucket", prefix="study/")

result = await async_simulate(
    model, "weather.epw",
    cache=cache,
    output_dir="run-001",
    fs=fs,
)
```

## FastAPI Integration

A minimal example of an async simulation endpoint:

```python
from fastapi import FastAPI
from idfkit import load_idf
from idfkit.simulation import async_simulate

app = FastAPI()

@app.post("/simulate")
async def run_simulation(idf_path: str, weather_path: str):
    model = load_idf(idf_path)
    result = await async_simulate(model, weather_path, design_day=True)

    return {
        "success": result.success,
        "runtime": result.runtime_seconds,
        "errors": result.errors.summary(),
    }
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
