# Batch Processing

The `simulate_batch()` function runs multiple EnergyPlus simulations in
parallel using a thread pool, ideal for parametric studies and sensitivity
analyses.

## Basic Usage

```python
--8<-- "docs/snippets/simulation/batch/basic_usage.py:example"
```

## SimulationJob

Define individual simulations with `SimulationJob`:

```python
--8<-- "docs/snippets/simulation/batch/simulationjob.py:example"
```

### SimulationJob Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | `IDFDocument` | Required | EnergyPlus model |
| `weather` | <code>str &#124; Path</code> | Required | Weather file path |
| `label` | `str` | `""` | Human-readable label |
| `output_dir` | <code>str &#124; Path &#124; None</code> | `None` | Output directory |
| `expand_objects` | `bool` | `True` | Run ExpandObjects |
| `annual` | `bool` | `False` | Annual simulation |
| `design_day` | `bool` | `False` | Design-day-only |
| `output_prefix` | `str` | `"eplus"` | Output file prefix |
| `output_suffix` | <code>"C" &#124; "L" &#124; "D"</code> | `"C"` | Output naming style |
| `readvars` | `bool` | `False` | Run ReadVarsESO |
| `timeout` | `float` | `3600.0` | Max runtime (seconds) |
| `extra_args` | <code>tuple[str, ...] &#124; None</code> | `None` | Extra CLI args |

## Parametric Studies

Create model variants for parametric analysis:

```python
--8<-- "docs/snippets/simulation/batch/parametric_studies.py:example"
```

## BatchResult

The `BatchResult` class aggregates results:

```python
--8<-- "docs/snippets/simulation/batch/batchresult.py:example"
```

## Progress Callbacks

Monitor progress with a callback function:

```python
--8<-- "docs/snippets/simulation/batch/progress_callbacks.py:example"
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
--8<-- "docs/snippets/simulation/batch/rich_progress_bar.py:example"
```

## Parallelism

### Worker Count

Control concurrency with `max_workers`:

```python
--8<-- "docs/snippets/simulation/batch/worker_count.py:example"
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
--8<-- "docs/snippets/simulation/batch/error_handling.py:example"
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
--8<-- "docs/snippets/simulation/batch/caching.py:example"
```

## Cloud Storage

Store results in S3:

```python
--8<-- "docs/snippets/simulation/batch/cloud_storage.py:example"
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
