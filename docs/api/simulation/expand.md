# Preprocessing API

Functions for expanding template and preprocessor objects before simulation.

EnergyPlus models may contain high-level template objects that must be
expanded into their low-level equivalents before a simulation can run.
Three preprocessors are supported:

| Function | Preprocessor | Objects handled |
|----------|-------------|-----------------|
| [`expand_objects()`](#expand_objects) | ExpandObjects | `HVACTemplate:*` |
| [`run_slab_preprocessor()`](#run_slab_preprocessor) | Slab | `GroundHeatTransfer:Slab:*` |
| [`run_basement_preprocessor()`](#run_basement_preprocessor) | Basement | `GroundHeatTransfer:Basement:*` |

All three return a **new** `IDFDocument` — the original model is never mutated.
If the model contains no objects for a given preprocessor, a copy is returned
immediately without invoking any external process.

## expand_objects

::: idfkit.simulation.expand.expand_objects
    options:
      show_root_heading: true
      show_source: true

## run_slab_preprocessor

::: idfkit.simulation.expand.run_slab_preprocessor
    options:
      show_root_heading: true
      show_source: true

## run_basement_preprocessor

::: idfkit.simulation.expand.run_basement_preprocessor
    options:
      show_root_heading: true
      show_source: true

## Error Handling

All three functions raise
[`ExpandObjectsError`](../exceptions.md)
on failure.  The exception carries structured fields for programmatic access:

```python
from idfkit.exceptions import ExpandObjectsError

try:
    expanded = expand_objects(model)
except ExpandObjectsError as e:
    print(e.preprocessor)  # "ExpandObjects", "Slab", or "Basement"
    print(e.exit_code)     # Process exit code, or None for timeout/OS error
    print(e.stderr)        # Captured stderr (truncated to 500 chars)
```

### Error modes

| Failure | `preprocessor` | `exit_code` | `stderr` |
|---------|----------------|-------------|----------|
| Executable not found | Name | `None` | `None` |
| Process timeout | Name | `None` | Partial output |
| OS error (permissions) | Name | `None` | `None` |
| Process crash (SIGSEGV) | Name | `139` | Signal info |
| Empty output (solver failure) | Name | `0` | Solver output |
| Fatal PreprocessorMessage | Name | `0` | Error message |
| Missing output file | Name | Exit code | Process stderr |
