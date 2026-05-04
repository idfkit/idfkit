## Allow passing a preprocessor timeout to `simulate()` for automatic Slab/Basement preprocessing

### Problem

When `simulate()` (and its async/batch variants) automatically invokes the Slab and/or Basement preprocessors via `maybe_preprocess`, it calls `run_preprocessing()` **without forwarding any timeout**, so the preprocessors always use their hardcoded default of **120 seconds**:

```python
# src/idfkit/simulation/_common.py
preprocessed = run_preprocessing(
    sim_model,
    energyplus=config,
    weather=weather_path,
    # no timeout argument — always defaults to 120 s
)
```

The caller's `timeout` argument (default `3600.0`) is applied only to the main EnergyPlus subprocess. There is currently no way to raise or lower the preprocessor timeout when going through the automatic pipeline.

### Why this matters

- **Complex slab/basement geometries** can easily exceed 120 s on slow or shared hardware, causing spurious `ExpandObjectsError` timeouts.
- **Fast CI environments** may want a much shorter ceiling to catch hangs quickly.
- The asymmetry is surprising: a user who passes `timeout=7200` reasonably expects that budget to cover the whole pipeline, not just the final EnergyPlus run.

### Affected code

| File | Symbol | Note |
|---|---|---|
| `src/idfkit/simulation/_common.py` | `maybe_preprocess()` | Calls `run_preprocessing()` with no `timeout` |
| `src/idfkit/simulation/runner.py` | `simulate()` ~line 174 | Calls `maybe_preprocess()` without forwarding `timeout` |
| `src/idfkit/simulation/async_runner.py` | `async_simulate()` | Same gap via the shared helper |
| `src/idfkit/simulation/batch.py` / `async_batch.py` | batch entry points | Inherit the same gap |

### Proposed fix

Add a `preprocessor_timeout: float = 120.0` parameter to `simulate()`, `async_simulate()`, and the batch entry points, and thread it through `maybe_preprocess()` → `run_preprocessing()`.

An alternative is to reuse the existing `timeout` parameter for every subprocess in the pipeline, but a dedicated parameter is clearer and avoids silently changing the behaviour of existing callers who pass a large `timeout` solely for long EnergyPlus runs.
