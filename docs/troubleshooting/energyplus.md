# EnergyPlus Issues

This page covers common EnergyPlus-related issues and their solutions.

## Installation Problems

### EnergyPlus Not Found

idfkit searches for EnergyPlus in this order:

1. Explicit path in code
2. `ENERGYPLUS_DIR` environment variable
3. System PATH
4. Platform default locations:
    - macOS: `/Applications/EnergyPlus-*/`
    - Linux: `/usr/local/EnergyPlus-*/`
    - Windows: `C:\EnergyPlusV*/`

**Verify installation:**

```python
from idfkit.simulation import find_energyplus

try:
    config = find_energyplus()
    print(f"Found: {config.executable}")
except Exception as e:
    print(f"Not found: {e}")
```

**Specify path manually:**

```python
config = find_energyplus("/path/to/EnergyPlus-24-1-0")
result = simulate(model, weather, energyplus=config)
```

### Multiple Versions Installed

When multiple versions exist, idfkit uses the newest by default.

**Use a specific version:**

```python
# Find a specific version
config = find_energyplus("/Applications/EnergyPlus-23-2-0")
result = simulate(model, weather, energyplus=config)
```

### Permission Denied

**Linux/macOS:**

```bash
chmod +x /usr/local/EnergyPlus-*/energyplus
```

**Windows:** Run as Administrator or check file permissions.

## Simulation Failures

### Fatal Errors

Check the error report for details:

```python
result = simulate(model, weather)

if not result.success:
    for err in result.errors.fatal:
        print(f"Fatal: {err.message}")
```

### Common Fatal Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "No surfaces in zone" | Zone has no surfaces | Add surfaces referencing the zone |
| "Weather file has no data" | Date mismatch | Check RunPeriod matches weather file |
| "Node not found" | HVAC node missing | Fix HVAC connections |
| "Schedule not found" | Missing schedule | Add the referenced schedule |

### Severe Errors

Severe errors don't stop the simulation but may cause incorrect results:

```python
for err in result.errors.severe:
    print(f"Severe: {err.message}")
```

### Warnings

Warnings are informational but worth reviewing:

```python
print(f"Warning count: {result.errors.warning_count}")
```

## Model Issues

### Missing Output:SQLite

idfkit automatically adds `Output:SQLite` if missing. However, if you
see SQL-related errors:

```python
# Verify SQL output is present
if "Output:SQLite" not in model:
    model.add("Output:SQLite", option_type="SimpleAndTabular")
```

### Version Mismatch

If the model was created for a different EnergyPlus version:

```python
# Load with explicit version
model = load_idf("old_model.idf", version=(24, 1, 0))
```

### Geometry Errors

Common geometry issues:

| Error | Solution |
|-------|----------|
| "Surface has zero area" | Fix vertex coordinates |
| "Zone volume is zero" | Ensure zone is fully enclosed |
| "Surface vertices are not planar" | Adjust vertices to be coplanar |

Use idfkit's geometry tools to diagnose:

```python
from idfkit.geometry import calculate_surface_area, calculate_zone_volume

for surface in model["BuildingSurface:Detailed"].values():
    area = calculate_surface_area(surface)
    if area <= 0:
        print(f"Invalid surface: {surface.name}")

volume = calculate_zone_volume(model, "Zone1")
if volume <= 0:
    print("Zone has invalid volume")
```

## Performance Issues

### Simulation Takes Too Long

1. **Use design-day mode for testing:**
   ```python
   result = simulate(model, weather, design_day=True)
   ```

2. **Reduce timesteps:**
   ```python
   # Check current timesteps
   if "Timestep" in model:
       print(model["Timestep"].values()[0].number_of_timesteps_per_hour)
   ```

3. **Simplify the model:**
   - Reduce zone count
   - Simplify HVAC systems
   - Use ideal loads for initial testing

### High Memory Usage

Large models may consume significant memory:

1. Close SQL connections when done:
   ```python
   sql = result.sql
   # ... use sql ...
   del sql  # Or let it go out of scope
   ```

2. Process results incrementally in batch runs

## Output Issues

### No SQL Output

If `result.sql` is `None`:

1. Check that EnergyPlus completed:
   ```python
   print(f"Exit code: {result.exit_code}")
   print(f"Success: {result.success}")
   ```

2. Check the error report:
   ```python
   print(result.errors.summary())
   ```

3. Verify output files exist:
   ```python
   print(f"SQL path: {result.sql_path}")
   ```

### Missing Time-Series Data

If `get_timeseries()` returns `None`:

1. Verify the variable name matches exactly:
   ```python
   # List available variables
   for var in result.sql.get_available_variables():
       if "Temperature" in var.name:
           print(f"{var.name} | {var.key_value}")
   ```

2. Check the reporting frequency in your model

3. Verify the output was requested:
   ```python
   # Add output request (name is optional for Output:Variable)
   model.add(
       "Output:Variable",
       key_value="*",
       variable_name="Zone Mean Air Temperature",
       reporting_frequency="Hourly",
   )
   ```

## Platform-Specific Issues

### macOS

**Gatekeeper blocks EnergyPlus:**

```bash
xattr -d com.apple.quarantine /Applications/EnergyPlus-*/energyplus
```

### Linux

**Shared library errors:**

```bash
# Install required libraries
sudo apt-get install libgl1-mesa-glx libxkbcommon-x11-0
```

### Windows

**Path with spaces:**

Avoid installing EnergyPlus in paths with spaces. If necessary, use
short paths or quotes.

**Long path issues:**

Enable long paths in Windows or use shorter directory names.

## Getting Help

If you can't resolve an issue:

1. Check the [idfkit GitHub issues](https://github.com/samuelduchesne/idfkit/issues)
2. Check the [EnergyPlus documentation](https://energyplus.net/documentation)
3. Search the [EnergyPlus Helpdesk](https://energyplushelp.freshdesk.com/)

When reporting issues, include:

- idfkit version (`idfkit.__version__`)
- EnergyPlus version
- Python version
- Operating system
- Error messages and stack traces
- Minimal reproducible example

## See Also

- [Common Errors](errors.md) — General error reference
- [Simulation Error Handling](../simulation/errors.md) — Parsing error reports
- [Running Simulations](../simulation/running.md) — Simulation guide
