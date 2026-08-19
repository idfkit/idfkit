# How to run a simulation

The `simulate()` function executes EnergyPlus as a subprocess and returns
a structured `SimulationResult` with access to all output files.

## Basic Usage

```python
--8<-- "docs/snippets/simulation/running/basic_usage.py:example"
```

## Parameters

For the full `simulate()` signature, with every keyword argument, its type, and
its default, see the generated
[`simulate()` reference](../api/simulation/runner.md). The sections below cover
the arguments you'll reach for most often.

## Simulation Modes

### Design-Day Only

Fast simulation using only design day conditions:

```python
--8<-- "docs/snippets/simulation/running/design_day_only.py:example"
```

### Annual Simulation

Full-year simulation:

```python
--8<-- "docs/snippets/simulation/running/annual_simulation.py:example"
```

### Default Mode

Without flags, EnergyPlus uses whatever run periods are defined in the model:

```python
--8<-- "docs/snippets/simulation/running/default_mode.py:example"
```

## Preprocessing

Some EnergyPlus models contain high-level template objects that must be
expanded into their low-level equivalents before simulation.  idfkit provides
standalone preprocessing functions for this.

### Expanding HVAC Templates

`HVACTemplate:*` objects are shorthand for complex HVAC systems.
`expand_objects()` converts them into their fully specified equivalents:

```python
--8<-- "docs/snippets/simulation/running/expanding_hvac_templates.py:example"
```

!!! note
    `simulate()` runs ExpandObjects automatically when `expand_objects=True`
    (the default).  Call `expand_objects()` directly only when you need to
    inspect or modify the expanded model before simulation.

### Ground Heat Transfer (Slab & Basement)

Models with `GroundHeatTransfer:Slab:*` or `GroundHeatTransfer:Basement:*`
objects need the Slab or Basement preprocessor to compute ground temperatures.

!!! note
    `simulate()` **automatically** runs the Slab and/or Basement
    preprocessors when `expand_objects=True` (the default) and the model
    contains the corresponding ground heat-transfer objects.  In most
    cases you do not need to call these functions yourself.

#### Preprocessor Timeout

Each preprocessor stage (ExpandObjects, Slab, Basement) gets its own
subprocess timeout, separate from the EnergyPlus `timeout`.  Override it
per call with `preprocessor_timeout`:

```python
simulate(model, weather, preprocessor_timeout=600.0)  # 10 min per stage
```

Or set a process-wide default with the `IDFKIT_PREPROCESSOR_TIMEOUT`
environment variable — useful for slow shared hardware (raise it) or
fast CI where you want to catch hangs quickly (lower it):

```bash
export IDFKIT_PREPROCESSOR_TIMEOUT=600   # slow shared hardware
export IDFKIT_PREPROCESSOR_TIMEOUT=30    # fail fast in CI
```

The default is **120 seconds per subprocess**.  `timeout` and
`preprocessor_timeout` are independent budgets — there is no shared
wall-clock cap across the pipeline, so a long `preprocessor_timeout`
will not trip the simulation's `timeout` and vice versa.

For cases where you need to inspect or modify the preprocessed model
before simulation, standalone functions are available:

```python
--8<-- "docs/snippets/simulation/running/ground_heat_transfer_slab_basement.py:example"
```

Each function runs ExpandObjects first (to extract the ground heat-transfer
input), then the Fortran solver, and returns a new `IDFDocument` with the
computed temperature schedules appended.

All preprocessing functions raise
[`ExpandObjectsError`](errors.md) on failure, with
structured `preprocessor`, `exit_code`, and `stderr` fields for
programmatic error handling.

See the [Preprocessing API](../api/simulation/expand.md) reference for full
details.

## EnergyPlus Discovery

By default, `simulate()` auto-discovers EnergyPlus:

```python
--8<-- "docs/snippets/simulation/running/energyplus_discovery.py:example"
```

Discovery priority:

1. Explicit `energyplus` parameter
2. `ENERGYPLUS_DIR` environment variable
3. System PATH
4. Platform default directories

## Output Directory

### Automatic Temporary Directory

By default, outputs go to an auto-generated temp directory:

```python
--8<-- "docs/snippets/simulation/running/automatic_temporary_directory.py:example"
```

### Explicit Directory

Specify where to store outputs:

```python
--8<-- "docs/snippets/simulation/running/explicit_directory.py:example"
```

The directory is created if it doesn't exist.

## Error Handling

### Simulation Errors

```python
--8<-- "docs/snippets/simulation/running/simulation_errors.py:example"
```

### Timeout

```python
--8<-- "docs/snippets/simulation/running/timeout.py:example"
```

### Checking Success

```python
--8<-- "docs/snippets/simulation/running/checking_success.py:example"
```

## Model Safety

`simulate()` copies your model before running — the original is never modified:

```python
--8<-- "docs/snippets/simulation/running/model_safety.py:example"
```

## Command-Line Options

### Output Suffix Modes

| Value | Description |
|-------|-------------|
| `"C"` | Combined table files (default) |
| `"L"` | Legacy separate table files |
| `"D"` | Timestamped separate files |

```python
--8<-- "docs/snippets/simulation/running/output_suffix_modes.py:example"
```

### Extra Arguments

Pass additional EnergyPlus flags:

```python
--8<-- "docs/snippets/simulation/running/extra_arguments.py:example"
```

## Cloud Storage

For remote storage backends (S3, etc.):

```python
--8<-- "docs/snippets/simulation/running/cloud_storage.py:example"
```

See [how to use cloud and remote storage](../concepts/cloud-storage.md) for details.

## Caching

Enable content-addressed caching to avoid redundant simulations:

```python
--8<-- "docs/snippets/simulation/running/caching.py:example"
```

See [how to cache simulation results](caching.md) for details.

## Version Migration

When `model.version` differs from the installed EnergyPlus,
`simulate()` raises [`VersionMismatchError`][idfkit.exceptions.VersionMismatchError]
by default. Pass `auto_migrate=True` to forward-migrate the model
transparently before the run; the resulting
[`MigrationReport`][idfkit.migration.report.MigrationReport] is attached to
[`SimulationResult.migration_report`][idfkit.simulation.result.SimulationResult.migration_report].
See [how to migrate models between versions](migrating-versions.md) for the
full workflow.

## See Also

- [How to migrate models between EnergyPlus versions](migrating-versions.md) — Forward-migrate IDF models across EnergyPlus releases
- [How to track simulation progress](progress.md) — Real-time progress with `on_progress`
- [How to access simulation results](results.md) — Working with `SimulationResult`
- [How to run batch simulations](batch.md) — Running multiple simulations
- [How to handle simulation errors](errors.md) — Understanding error reports
