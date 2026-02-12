# Simulation Progress Tracking

The `on_progress` callback provides real-time visibility into what EnergyPlus
is doing during a simulation.  It fires for warmup iterations, simulation day
changes, post-processing steps, and completion -- enabling progress bars, live
logs, and remote monitoring.

## Quick Start

The fastest way to get a progress bar is the built-in tqdm integration:

```bash
pip install idfkit[progress]    # installs tqdm
```

```python
--8<-- "docs/snippets/simulation/progress/quick_start.py:example"
```

That's it.  A tqdm progress bar appears in your terminal (or Jupyter notebook)
and is automatically closed when the simulation finishes -- even on error.

For full control, pass any callable instead:

```python
--8<-- "docs/snippets/simulation/progress/quick_start_2.py:example"
```

Output:

```
[  ?  ] initializing: Initializing New Environment Parameters
[  ?  ] warmup: Warming up {1}
[  ?  ] warmup: Warming up {2}
[  ?  ] warmup: Warmup Complete
[  0.0%] simulating: Starting Simulation at 01/01/2017 for AnnualRun from 01/01/2017 to 12/31/2017
[  8.5%] simulating: Continuing Simulation at 02/01/2017 for AnnualRun
[ 16.2%] simulating: Continuing Simulation at 03/01/2017 for AnnualRun
...
[ 91.5%] simulating: Continuing Simulation at 12/01/2017 for AnnualRun
[  ?  ] postprocessing: Writing tabular output file results using comma format.
[100.0%] complete: EnergyPlus Completed Successfully.
```

## `on_progress` Parameter

All simulation functions accept `on_progress`:

| Value | Behavior |
|-------|----------|
| `None` (default) | No progress tracking.  Zero overhead -- uses the original `subprocess.run()` / `communicate()` code path. |
| `"tqdm"` | Built-in tqdm progress bar.  Auto-detects terminal vs Jupyter.  Requires `pip install idfkit[progress]`.  Supported by `simulate()` and `async_simulate()` only -- batch runners require a custom callback (see [Batch Progress](#batch-progress)). |
| Any `Callable[[SimulationProgress], None]` | Your custom callback, called once per progress line. |
| Any `async Callable` (async runner only) | Async callback, awaited by the runner. |

## SimulationProgress

Each callback invocation receives a `SimulationProgress` event:

| Field | Type | Description |
|-------|------|-------------|
| `phase` | `str` | `"initializing"`, `"warmup"`, `"simulating"`, `"postprocessing"`, or `"complete"` |
| `message` | `str` | Raw EnergyPlus stdout line (stripped) |
| `percent` | <code>float &#124; None</code> | Estimated 0-100 completion, or `None` when indeterminate |
| `environment` | <code>str &#124; None</code> | Current simulation environment name |
| `warmup_day` | <code>int &#124; None</code> | Current warmup iteration (1-based) |
| `sim_day` | <code>int &#124; None</code> | Current day-of-year (1-based) |
| `sim_total_days` | <code>int &#124; None</code> | Total simulation days when known |
| `job_index` | <code>int &#124; None</code> | Batch job index (only set in batch mode) |
| `job_label` | <code>str &#124; None</code> | Batch job label (only set in batch mode) |

### Simulation Phases

| Phase | When | `percent` |
|-------|------|-----------|
| `initializing` | EnergyPlus starts a new environment | `None` |
| `warmup` | Iterating warmup days until convergence | `None` |
| `simulating` | Stepping through the simulation period | `float` when period is known |
| `postprocessing` | Writing output files | `None` |
| `complete` | Simulation finished successfully | `100.0` |

### Percentage Estimation

The `percent` field is estimated from the current simulation date relative to
the run period.  It is only available during the `simulating` phase when
EnergyPlus reports the simulation period (e.g. annual runs).

When the period cannot be determined (design-day runs, custom periods without
date ranges), `percent` is `None`.  Your progress indicator should handle this
with a spinner or indeterminate bar.

## Built-in tqdm Progress Bar

### One-liner

```python
--8<-- "docs/snippets/simulation/progress/one_liner.py:example"
```

The `"tqdm"` shorthand:

- Creates a tqdm bar with sensible defaults (percentage, elapsed, ETA)
- Uses `tqdm.auto` so it works in terminals, Jupyter notebooks, and IPython
- Automatically closes the bar when the simulation finishes (including on error)
- Requires `pip install idfkit[progress]` -- raises a clear `ImportError` if missing

### Customising the tqdm bar

For more control over the bar appearance, use the `tqdm_progress()` context
manager directly:

```python
--8<-- "docs/snippets/simulation/progress/customising_the_tqdm_bar.py:example"
```

`tqdm_progress()` is a context manager that yields a callback.  The bar is
automatically closed when the `with` block exits (even on exception).  All
keyword arguments are forwarded to `tqdm.tqdm`, so you have full control
over colours, file output, miniters, etc.

## Building Your Own Progress Indicator

The examples below show how to build custom `on_progress` callbacks for
different use cases.  Each example is a self-contained recipe you can adapt.

### rich (Console)

[rich](https://rich.readthedocs.io/) provides beautiful terminal output with
spinners, colours, and multi-column layouts.

```python
--8<-- "docs/snippets/simulation/progress/rich_console.py:example"
```

**Batch with rich** -- multiple bars, one per concurrent job:

```python
--8<-- "docs/snippets/simulation/progress/rich_console_2.py:example"
```

### Jupyter (ipywidgets)

```python
--8<-- "docs/snippets/simulation/progress/jupyter_ipywidgets.py:example"
```

!!! tip
    The `"tqdm"` shorthand also works in Jupyter -- `tqdm.auto` renders
    as a native Jupyter widget automatically.

### Structured Logging

Emit structured log entries for observability platforms (Datadog, ELK, etc.):

```python
--8<-- "docs/snippets/simulation/progress/structured_logging.py:example"
```

### Simple Console Log

```python
--8<-- "docs/snippets/simulation/progress/simple_console_log.py:example"
```

### WebSocket Forwarding

Forward progress events to a web client for real-time dashboards.
Use an async callback so WebSocket sends don't block the event loop:

```python
--8<-- "docs/snippets/simulation/progress/websocket_forwarding.py:example"
```

### FastAPI + WebSocket

A complete FastAPI endpoint that streams progress to a browser:

```python
--8<-- "docs/snippets/simulation/progress/fastapi_websocket.py:example"
```

**JavaScript client:**

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/simulate");
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.phase === "done") {
        console.log(`Simulation ${data.success ? "succeeded" : "failed"}`);
    } else {
        updateProgressBar(data.percent);
        updateStatusText(`${data.phase}: ${data.message}`);
    }
};
ws.send(JSON.stringify({ idf_path: "building.idf", weather_path: "weather.epw" }));
```

### Server-Sent Events (SSE)

For one-way streaming without WebSocket overhead (ideal for dashboards):

```python
--8<-- "docs/snippets/simulation/progress/server_sent_events_sse.py:example"
```

### Cloud Logging (AWS CloudWatch / GCP Cloud Logging)

For cloud-deployed simulations, forward events to your cloud logging service:

```python
--8<-- "docs/snippets/simulation/progress/cloud_logging_aws_cloudwatch_gcp_cloud_logging.py:example"
```

**With a message queue (Redis, RabbitMQ, SQS):**

```python
--8<-- "docs/snippets/simulation/progress/cloud_logging_aws_cloudwatch_gcp_cloud_logging_2.py:example"
```

## Async Callbacks

`async_simulate()` accepts both sync and async callables:

```python
--8<-- "docs/snippets/simulation/progress/async_callbacks.py:example"
```

Synchronous callbacks also work in the async runner and are called directly
without awaiting:

```python
# This works too -- no need to make it async for simple logging
result = await async_simulate(model, "weather.epw", on_progress=lambda e: print(e.phase))
```

## Batch Progress

In batch mode, `on_progress` fires for every simulation in the batch.
Events include `job_index` and `job_label` to identify which job they
belong to.

### Dual Progress Tracking

Use `on_progress` for intra-simulation progress and `progress` for
job-level completion -- they are independent and complementary:

```python
--8<-- "docs/snippets/simulation/progress/dual_progress_tracking.py:example"
```

### Batch Progress Bar with tqdm

For batch simulations, the `"tqdm"` shorthand is **not supported** because a
single progress bar cannot meaningfully represent multiple concurrent jobs.
Instead, build per-job bars manually:

```python
--8<-- "docs/snippets/simulation/progress/batch_progress_bar_with_tqdm.py:example"
```

### Async Batch with Stream + Progress

Combine `async_simulate_batch_stream` (job-level events) with
`on_progress` (intra-simulation events):

```python
--8<-- "docs/snippets/simulation/progress/async_batch_with_stream_progress.py:example"
```

## Using ProgressParser Directly

The `ProgressParser` class can be used independently to parse EnergyPlus
stdout output -- useful for custom integrations or when processing log files
from previous simulation runs:

```python
--8<-- "docs/snippets/simulation/progress/using_progressparser_directly.py:example"
```

The parser is stateful (it tracks environment transitions and warmup
counters), so use a fresh instance for each simulation. Non-progress lines
return `None` and never raise exceptions.

## Cloud Execution

When using the `fs` parameter for remote storage, progress callbacks fire
during the local EnergyPlus execution -- before results are uploaded.  This
works identically to local execution:

```python
--8<-- "docs/snippets/simulation/progress/cloud_execution.py:example"
```

For remote execution scenarios (where EnergyPlus runs on a different machine),
use the async callback to forward events over a transport layer
(WebSocket, SSE, message queue). The `SimulationProgress` dataclass is
JSON-serializable via `dataclasses.asdict()`:

```python
--8<-- "docs/snippets/simulation/progress/cloud_execution_2.py:example"
```

## Behavior Notes

- **No callback, no overhead**: When `on_progress` is not provided, the
  original `subprocess.run()` / `proc.communicate()` code paths are used
  with no performance impact.

- **Automatic cleanup**: When using `on_progress="tqdm"`, the progress bar
  is always closed -- even if the simulation raises an exception.  On error,
  the bar preserves its last reported value instead of jumping to 100%.

- **Callback exceptions**: If your callback raises an exception, the
  simulation is killed and `SimulationError` is raised.

- **Thread safety (batch)**: In `simulate_batch()`, the `on_progress`
  callback may be called from multiple threads concurrently. If your
  callback writes to shared state, ensure it is thread-safe (e.g. use a
  lock or thread-safe data structures).

- **Indeterminate phases**: During warmup and post-processing, `percent`
  is `None`. Your progress indicator should handle this gracefully --
  show a spinner or simply log the phase name.

## API Reference

### Functions

| Function | `on_progress` Support |
|----------|----------------------|
| `simulate()` | `"tqdm"`, sync callback, or `None` |
| `async_simulate()` | `"tqdm"`, sync/async callback, or `None` |
| `simulate_batch()` | Sync callback or `None` (events include `job_index`/`job_label`) |
| `async_simulate_batch()` | Sync/async callback or `None` (events include `job_index`/`job_label`) |
| `async_simulate_batch_stream()` | Sync/async callback or `None` (events include `job_index`/`job_label`) |

### Classes / Factories

| Name | Description |
|------|-------------|
| `SimulationProgress` | Frozen dataclass for progress events |
| `ProgressParser` | Stateful EnergyPlus stdout line parser |
| `tqdm_progress()` | Context manager yielding a callback for customised tqdm bars |

## See Also

- [Running Simulations](running.md) -- Full `simulate()` parameter reference
- [Async Simulation](async.md) -- Non-blocking execution guide
- [Batch Processing](batch.md) -- Parallel execution guide
