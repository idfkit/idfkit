# Running Simulations

The `simulate()` function executes EnergyPlus as a subprocess and returns
a structured `SimulationResult` with access to all output files.

## Basic Usage

```python
--8<-- "docs/snippets/simulation/running/basic_usage.py:example"
```

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

## Function Signature

```python
def simulate(
    model: IDFDocument,
    weather: str | Path,
    *,
    output_dir: str | Path | None = None,
    energyplus: EnergyPlusConfig | None = None,
    expand_objects: bool = True,
    annual: bool = False,
    design_day: bool = False,
    output_prefix: str = "eplus",
    output_suffix: Literal["C", "L", "D"] = "C",
    readvars: bool = False,
    timeout: float = 3600.0,
    extra_args: list[str] | None = None,
    cache: SimulationCache | None = None,
    fs: FileSystem | None = None,
    on_progress: Callable[[SimulationProgress], Any] | Literal["tqdm"] | None = None,
    auto_migrate: bool = False,
) -> SimulationResult:
```

## Parameters

### Required

| Parameter | Description |
|-----------|-------------|
| `model` | The EnergyPlus model to simulate |
| `weather` | Path to the weather file (.epw) |

### Optional

| Parameter | Default | Description |
|-----------|---------|-------------|
| `output_dir` | Auto temp | Directory for output files |
| `energyplus` | Auto-detect | Pre-configured EnergyPlus installation |
| `expand_objects` | `True` | Run ExpandObjects (and Slab/Basement if needed) before simulation |
| `annual` | `False` | Run annual simulation (`-a` flag) |
| `design_day` | `False` | Run design-day-only (`-D` flag) |
| `output_prefix` | `"eplus"` | Prefix for output files |
| `output_suffix` | `"C"` | Output naming style (C/L/D) |
| `readvars` | `False` | Run ReadVarsESO after simulation |
| `timeout` | `3600.0` | Maximum runtime in seconds |
| `extra_args` | `None` | Additional command-line arguments |
| `cache` | `None` | Simulation cache for result reuse |
| `fs` | `None` | File system backend for cloud storage |
| `on_progress` | `None` | Callback or `"tqdm"` for real-time progress updates |
| `auto_migrate` | `False` | Forward-migrate the model when its version differs from the installed EnergyPlus (see [Migrating Versions](migrating-versions.md)) |

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

See [Cloud & Remote Storage](../concepts/cloud-storage.md) for details.

## Caching

Enable content-addressed caching to avoid redundant simulations:

```python
--8<-- "docs/snippets/simulation/running/caching.py:example"
```

See [Caching](caching.md) for details.

## Version Migration

When `model.version` differs from the installed EnergyPlus,
`simulate()` raises [`VersionMismatchError`][idfkit.exceptions.VersionMismatchError]
by default. Pass `auto_migrate=True` to forward-migrate the model
transparently before the run; the resulting
[`MigrationReport`][idfkit.migration.report.MigrationReport] is attached to
[`SimulationResult.migration_report`][idfkit.simulation.result.SimulationResult.migration_report].
See [Migrating Versions](migrating-versions.md) for the full workflow.

## See Also

- [Migrating Versions](migrating-versions.md) — Forward-migrate IDF models across EnergyPlus releases
- [Progress Tracking](progress.md) — Real-time progress with `on_progress`
- [Parsing Results](results.md) — Working with `SimulationResult`
- [Batch Processing](batch.md) — Running multiple simulations
- [Error Handling](errors.md) — Understanding error reports
