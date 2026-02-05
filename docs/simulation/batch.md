# Batch Processing

The `simulate_batch()` function runs multiple EnergyPlus simulations in
parallel using a thread pool, ideal for parametric studies and sensitivity
analyses.

## Basic Usage

```python
from idfkit.simulation import simulate_batch, SimulationJob

# Create jobs
jobs = [
    SimulationJob(model=model1, weather="weather.epw", label="baseline"),
    SimulationJob(model=model2, weather="weather.epw", label="improved"),
]

# Run in parallel
batch = simulate_batch(jobs, max_workers=4)

print(f"Completed: {len(batch.succeeded)}/{len(batch)}")
for i, result in enumerate(batch):
    print(f"  Job {i}: {'Success' if result.success else 'Failed'}")
```

## SimulationJob

Define individual simulations with `SimulationJob`:

```python
from idfkit.simulation import SimulationJob

job = SimulationJob(
    model=my_model,              # Required: IDFDocument
    weather="weather.epw",       # Required: Path to weather file
    label="case-001",            # Optional: Label for progress reporting
    output_dir="./output/case1", # Optional: Output directory
    design_day=True,             # Optional: Design-day-only
    annual=False,                # Optional: Annual simulation
    timeout=3600.0,              # Optional: Max runtime in seconds
)
```

### SimulationJob Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | `IDFDocument` | Required | EnergyPlus model |
| `weather` | `str \| Path` | Required | Weather file path |
| `label` | `str` | `""` | Human-readable label |
| `output_dir` | `str \| Path \| None` | `None` | Output directory |
| `expand_objects` | `bool` | `True` | Run ExpandObjects |
| `annual` | `bool` | `False` | Annual simulation |
| `design_day` | `bool` | `False` | Design-day-only |
| `output_prefix` | `str` | `"eplus"` | Output file prefix |
| `output_suffix` | `"C" \| "L" \| "D"` | `"C"` | Output naming style |
| `readvars` | `bool` | `False` | Run ReadVarsESO |
| `timeout` | `float` | `3600.0` | Max runtime (seconds) |
| `extra_args` | `tuple[str, ...] \| None` | `None` | Extra CLI args |

## Parametric Studies

Create model variants for parametric analysis:

```python
from idfkit.simulation import simulate_batch, SimulationJob

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
batch = simulate_batch(jobs, max_workers=4)

# Analyze results
for job, result in zip(jobs, batch):
    if result.success:
        ts = result.sql.get_timeseries(
            "Zone Mean Air Temperature",
            "ZONE 1",
        )
        print(f"{job.label}: Max temp {max(ts.values):.1f}°C")
```

## BatchResult

The `BatchResult` class aggregates results:

```python
batch = simulate_batch(jobs)

# Access results
batch.results          # All results as tuple
batch[0]               # First result (by index)
len(batch)             # Number of jobs

# Filter by success
batch.succeeded        # Only successful results
batch.failed           # Only failed results
batch.all_succeeded    # True if all succeeded

# Timing
print(f"Total time: {batch.total_runtime_seconds:.1f}s")
```

## Progress Callbacks

Monitor progress with a callback function:

```python
def on_progress(completed, total, label, success):
    status = "OK" if success else "FAIL"
    print(f"[{completed}/{total}] {label}: {status}")

batch = simulate_batch(jobs, progress=on_progress)
```

The callback receives:

| Parameter | Type | Description |
|-----------|------|-------------|
| `completed` | `int` | Number of completed jobs |
| `total` | `int` | Total number of jobs |
| `label` | `str` | Label of the just-completed job |
| `success` | `bool` | Whether the job succeeded |

### Rich Progress Bar

```python
from rich.progress import Progress

with Progress() as progress:
    task = progress.add_task("Simulating...", total=len(jobs))

    def callback(completed, total, label, success):
        progress.update(task, completed=completed)

    batch = simulate_batch(jobs, progress=callback)
```

## Parallelism

### Worker Count

Control concurrency with `max_workers`:

```python
# Use all CPUs
batch = simulate_batch(jobs, max_workers=None)  # Default

# Limit to 4 concurrent simulations
batch = simulate_batch(jobs, max_workers=4)

# Sequential (useful for debugging)
batch = simulate_batch(jobs, max_workers=1)
```

Default: `min(len(jobs), os.cpu_count())`

### Thread vs Process

`simulate_batch` uses **threads** (not processes) because:

- EnergyPlus runs as a subprocess (releases GIL)
- Lower memory overhead than multiprocessing
- Simpler error handling

## Error Handling

Failed simulations don't stop the batch:

```python
batch = simulate_batch(jobs)

for i, result in enumerate(batch):
    if not result.success:
        print(f"Job {i} failed:")
        print(f"  Exit code: {result.exit_code}")
        print(f"  Stderr: {result.stderr}")
        for err in result.errors.fatal:
            print(f"  Error: {err.message}")
```

### Partial Failures

```python
if not batch.all_succeeded:
    failed_count = len(batch.failed)
    print(f"{failed_count} jobs failed")

    # Process only successful results
    for result in batch.succeeded:
        # ... analyze results
```

## Caching

Share a cache across batch jobs:

```python
from idfkit.simulation import SimulationCache

cache = SimulationCache()

# All jobs share the same cache
batch = simulate_batch(jobs, cache=cache)

# Re-running is instant for unchanged models
batch2 = simulate_batch(jobs, cache=cache)  # Cache hits
```

## Cloud Storage

Store results in S3:

```python
from idfkit.simulation import S3FileSystem

fs = S3FileSystem(bucket="my-bucket", prefix="study-001/")

# Each job needs an explicit output_dir
jobs = [
    SimulationJob(
        model=variant,
        weather="weather.epw",
        label=f"case-{i}",
        output_dir=f"case-{i}",  # Required with fs
    )
    for i, variant in enumerate(variants)
]

batch = simulate_batch(jobs, fs=fs)
```

## Best Practices

1. **Use labels** — Makes progress tracking and debugging easier
2. **Set timeouts** — Prevent runaway simulations from blocking
3. **Share caches** — Avoid redundant work across similar models
4. **Handle failures gracefully** — Check `result.success` before accessing outputs
5. **Start small** — Test with a few jobs before running thousands

## See Also

- [Running Simulations](running.md) — Single simulation guide
- [Caching](caching.md) — Content-addressed caching
- [Examples: Parametric Study](../examples/parametric-study.ipynb) — Complete example
