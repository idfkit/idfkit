# Error Handling

This page covers error handling in the simulation module, including
parsing EnergyPlus error reports and handling simulation failures.

## Error Report

The `ErrorReport` class parses the `.err` file produced by EnergyPlus:

```python
from idfkit.simulation import simulate

result = simulate(model, weather)

# Access the error report
errors = result.errors

# Check for problems
if errors.has_fatal:
    print("Simulation had fatal errors")
if errors.has_severe:
    print("Simulation had severe errors")
if errors.warning_count > 0:
    print(f"Simulation had {errors.warning_count} warnings")
```

## Error Severity Levels

EnergyPlus uses several error severity levels:

| Level | Description | Effect |
|-------|-------------|--------|
| **Fatal** | Unrecoverable error | Simulation stops immediately |
| **Severe** | Serious problem | May cause incorrect results |
| **Warning** | Potential issue | Simulation continues |
| **Info** | Informational | No action needed |

## Querying Errors

### By Severity

```python
errors = result.errors

# Fatal errors (simulation stopped)
for err in errors.fatal:
    print(f"FATAL: {err.message}")

# Severe errors (may cause incorrect results)
for err in errors.severe:
    print(f"SEVERE: {err.message}")

# Warnings
for warn in errors.warnings:
    print(f"Warning: {warn.message}")
```

### Error Counts

```python
print(f"Fatal: {errors.fatal_count}")
print(f"Severe: {errors.severe_count}")
print(f"Warnings: {errors.warning_count}")
```

### Summary

```python
# Get a formatted summary string
print(errors.summary())
# Output: "0 Fatal, 2 Severe, 15 Warnings"
```

## ErrorMessage Attributes

Each error/warning is an `ErrorMessage` object:

| Attribute | Type | Description |
|-----------|------|-------------|
| `severity` | `str` | "Fatal", "Severe", "Warning", etc. |
| `message` | `str` | The error message text |

## Simulation Exceptions

The `simulate()` function raises `SimulationError` for certain failures:

```python
from idfkit.exceptions import SimulationError

try:
    result = simulate(model, weather)
except SimulationError as e:
    print(f"Simulation failed: {e}")
    print(f"Exit code: {e.exit_code}")
    print(f"Stderr: {e.stderr}")
```

### Exception Cases

| Situation | Exception |
|-----------|-----------|
| Weather file not found | `SimulationError` |
| EnergyPlus not found | `EnergyPlusNotFoundError` |
| Timeout exceeded | `SimulationError` (exit_code=None) |
| OS error starting process | `SimulationError` |

### Timeout Handling

```python
try:
    result = simulate(model, weather, timeout=60.0)
except SimulationError as e:
    if e.exit_code is None:
        print("Simulation timed out")
    else:
        print(f"Simulation failed with exit code {e.exit_code}")
```

## Non-Exception Failures

Some simulation failures don't raise exceptions but return a result
with `success=False`:

```python
result = simulate(model, weather)

if not result.success:
    print(f"Exit code: {result.exit_code}")

    # Check errors
    if result.errors.has_fatal:
        for err in result.errors.fatal:
            print(f"Fatal: {err.message}")
```

## Batch Error Handling

In batch processing, individual failures don't stop the batch:

```python
from idfkit.simulation import simulate_batch

batch = simulate_batch(jobs)

# Check overall success
if not batch.all_succeeded:
    print(f"{len(batch.failed)} jobs failed")

# Handle failures individually
for i, result in enumerate(batch):
    if not result.success:
        print(f"Job {i} failed:")
        for err in result.errors.fatal:
            print(f"  {err.message}")
```

## Common EnergyPlus Errors

### Missing Required Input

```
** Severe  ** GetSurfaceData: BuildingSurface:Detailed="WALL_1", Construction="EXTERIOR_WALL" was not found.
```

**Solution**: Ensure all referenced objects exist in the model.

### Invalid Weather Data

```
** Fatal  ** GetWeatherDataPeriods: Weather file has no data for requested period
```

**Solution**: Check that run period dates match weather file coverage.

### Geometry Errors

```
** Severe  ** GetSurfaceData: Surface="WALL_1" has zero or negative area
```

**Solution**: Fix surface vertex coordinates.

### Schedule Errors

```
** Severe  ** GetSchedule: Schedule="OCCUPANCY" was not found
```

**Solution**: Add the missing schedule or fix the reference.

### HVAC Sizing

```
** Severe  ** Sizing:Zone: Zone="ZONE_1" has zero volume
```

**Solution**: Ensure zone geometry is properly enclosed.

## Debugging Tips

### 1. Check the Error Report First

```python
if not result.success:
    print(errors.summary())
    for err in errors.fatal + errors.severe:
        print(err.message)
```

### 2. Examine Raw Output

```python
# Check stderr
print(result.stderr)

# Check the run directory
print(f"Outputs in: {result.run_dir}")
```

### 3. Run Design-Day First

Design-day simulations are faster and catch most errors:

```python
# Quick validation
result = simulate(model, weather, design_day=True)
if result.success:
    # Then run full annual
    result = simulate(model, weather, annual=True)
```

### 4. Validate Before Simulation

```python
from idfkit import validate_document

validation = validate_document(model)
if not validation.is_valid:
    for err in validation.errors:
        print(err)
```

## Error Report from File

Parse an error file directly:

```python
from idfkit.simulation import ErrorReport

errors = ErrorReport.from_file("/path/to/eplusout.err")
print(errors.summary())
```

Or from string:

```python
err_text = Path("eplusout.err").read_text()
errors = ErrorReport.from_string(err_text)
```

## See Also

- [Running Simulations](running.md) — Basic simulation guide
- [Parsing Results](results.md) — Working with SimulationResult
- [Troubleshooting](../troubleshooting/errors.md) — Common error solutions
