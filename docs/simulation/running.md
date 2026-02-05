# Running Simulations

The `simulate()` function executes EnergyPlus as a subprocess and returns
a structured `SimulationResult` with access to all output files.

## Basic Usage

```python
from idfkit import load_idf
from idfkit.simulation import simulate

model = load_idf("building.idf")
result = simulate(model, "weather.epw")

print(f"Success: {result.success}")
print(f"Runtime: {result.runtime_seconds:.1f}s")
print(f"Output directory: {result.run_dir}")
```

## Simulation Modes

### Design-Day Only

Fast simulation using only design day conditions:

```python
result = simulate(model, weather, design_day=True)
```

### Annual Simulation

Full-year simulation:

```python
result = simulate(model, weather, annual=True)
```

### Default Mode

Without flags, EnergyPlus uses whatever run periods are defined in the model:

```python
result = simulate(model, weather)  # Uses model's RunPeriod objects
```

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
| `expand_objects` | `True` | Run ExpandObjects before simulation |
| `annual` | `False` | Run annual simulation (`-a` flag) |
| `design_day` | `False` | Run design-day-only (`-D` flag) |
| `output_prefix` | `"eplus"` | Prefix for output files |
| `output_suffix` | `"C"` | Output naming style (C/L/D) |
| `readvars` | `False` | Run ReadVarsESO after simulation |
| `timeout` | `3600.0` | Maximum runtime in seconds |
| `extra_args` | `None` | Additional command-line arguments |
| `cache` | `None` | Simulation cache for result reuse |
| `fs` | `None` | File system backend for cloud storage |

## EnergyPlus Discovery

By default, `simulate()` auto-discovers EnergyPlus:

```python
# Auto-discovery
result = simulate(model, weather)

# Explicit path
from idfkit.simulation import find_energyplus
config = find_energyplus("/custom/path/EnergyPlus-24-1-0")
result = simulate(model, weather, energyplus=config)

# Environment variable
# Set ENERGYPLUS_DIR=/path/to/EnergyPlus before running
result = simulate(model, weather)
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
result = simulate(model, weather)
print(result.run_dir)  # e.g., /tmp/idfkit_sim_abc123/
```

### Explicit Directory

Specify where to store outputs:

```python
result = simulate(model, weather, output_dir="./sim_output")
```

The directory is created if it doesn't exist.

## Error Handling

### Simulation Errors

```python
from idfkit.exceptions import SimulationError

try:
    result = simulate(model, weather)
except SimulationError as e:
    print(f"Simulation failed: {e}")
    print(f"Exit code: {e.exit_code}")
    print(f"Stderr: {e.stderr}")
```

### Timeout

```python
try:
    result = simulate(model, weather, timeout=60.0)  # 1 minute max
except SimulationError as e:
    if e.exit_code is None:
        print("Simulation timed out")
```

### Checking Success

```python
result = simulate(model, weather)

if not result.success:
    print(f"Exit code: {result.exit_code}")
    print(f"Stderr: {result.stderr}")
    for err in result.errors.fatal:
        print(f"Error: {err.message}")
```

## Model Safety

`simulate()` copies your model before running — the original is never modified:

```python
model = load_idf("building.idf")
original_count = len(model)

result = simulate(model, weather)

# Model unchanged
assert len(model) == original_count
assert "Output:SQLite" not in model
```

## Command-Line Options

### Output Suffix Modes

| Value | Description |
|-------|-------------|
| `"C"` | Combined table files (default) |
| `"L"` | Legacy separate table files |
| `"D"` | Timestamped separate files |

```python
result = simulate(model, weather, output_suffix="L")
```

### Extra Arguments

Pass additional EnergyPlus flags:

```python
result = simulate(
    model, weather,
    extra_args=["--convert-only"]  # Just convert, don't simulate
)
```

## Cloud Storage

For remote storage backends (S3, etc.):

```python
from idfkit.simulation import S3FileSystem

fs = S3FileSystem(bucket="my-bucket", prefix="runs/")
result = simulate(
    model, weather,
    output_dir="run-001",  # Required with fs
    fs=fs,
)
```

See [Cloud & Remote Storage](../concepts/cloud-storage.md) for details.

## Caching

Enable content-addressed caching to avoid redundant simulations:

```python
from idfkit.simulation import SimulationCache

cache = SimulationCache()

# First run: executes simulation
result1 = simulate(model, weather, cache=cache)

# Second run: instant cache hit
result2 = simulate(model, weather, cache=cache)
```

See [Caching](caching.md) for details.

## See Also

- [Parsing Results](results.md) — Working with `SimulationResult`
- [Batch Processing](batch.md) — Running multiple simulations
- [Error Handling](errors.md) — Understanding error reports
