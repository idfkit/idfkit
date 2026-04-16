# Error Handling

This page covers error handling in the simulation module, including
parsing EnergyPlus error reports and handling simulation failures.

## Error Report

The `ErrorReport` class parses the `.err` file produced by EnergyPlus:

```python
--8<-- "docs/snippets/simulation/errors/error_report.py:example"
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
--8<-- "docs/snippets/simulation/errors/by_severity.py:example"
```

### Error Counts

```python
--8<-- "docs/snippets/simulation/errors/error_counts.py:example"
```

### Summary

```python
--8<-- "docs/snippets/simulation/errors/summary.py:example"
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
--8<-- "docs/snippets/simulation/errors/simulation_exceptions.py:example"
```

### Exception Cases

| Situation | Exception |
|-----------|-----------|
| Weather file not found | `SimulationError` |
| EnergyPlus not found | `EnergyPlusNotFoundError` |
| Timeout exceeded | `SimulationError` (exit_code=None) |
| OS error starting process | `SimulationError` |
| Model version differs from installed EnergyPlus | `VersionMismatchError` |

### Version Mismatch

By default `simulate()` refuses to run when `model.version` doesn't match
the installed EnergyPlus version, raising
[`VersionMismatchError`][idfkit.exceptions.VersionMismatchError] with a
suggested migration chain. Two ways to resolve it:

```python
# Option A: let simulate() forward-migrate transparently
result = simulate(model, weather, auto_migrate=True)
print(result.migration_report.summary())

# Option B: migrate explicitly first, inspect the report, then simulate
from idfkit import migrate
report = migrate(model, target_version=(25, 2, 0))
result = simulate(report.migrated_model, weather)
```

Backward migration (installed EnergyPlus older than the model) is never
attempted and always raises. See [Migrating Versions](migrating-versions.md).

### Timeout Handling

```python
--8<-- "docs/snippets/simulation/errors/timeout_handling.py:example"
```

## Non-Exception Failures

Some simulation failures don't raise exceptions but return a result
with `success=False`:

```python
--8<-- "docs/snippets/simulation/errors/non_exception_failures.py:example"
```

## Batch Error Handling

In batch processing, individual failures don't stop the batch:

```python
--8<-- "docs/snippets/simulation/errors/batch_error_handling.py:example"
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
--8<-- "docs/snippets/simulation/errors/1_check_the_error_report_first.py:example"
```

### 2. Examine Raw Output

```python
--8<-- "docs/snippets/simulation/errors/2_examine_raw_output.py:example"
```

### 3. Run Design-Day First

Design-day simulations are faster and catch most errors:

```python
--8<-- "docs/snippets/simulation/errors/3_run_design_day_first.py:example"
```

### 4. Validate Before Simulation

```python
--8<-- "docs/snippets/simulation/errors/4_validate_before_simulation.py:example"
```

## Error Report from File

Parse an error file directly:

```python
--8<-- "docs/snippets/simulation/errors/error_report_from_file.py:example"
```

Or from string:

```python
--8<-- "docs/snippets/simulation/errors/error_report_from_file_2.py:example"
```

## See Also

- [Running Simulations](running.md) — Basic simulation guide
- [Parsing Results](results.md) — Working with SimulationResult
- [Migrating Versions](migrating-versions.md) — Resolving `VersionMismatchError`
- [Troubleshooting](../troubleshooting/errors.md) — Common error solutions
