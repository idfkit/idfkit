# Common Errors

This page covers common errors you may encounter when using idfkit and how
to resolve them.

## idfkit Errors

### EnergyPlusNotFoundError

```
EnergyPlusNotFoundError: Could not find EnergyPlus installation
```

**Cause:** idfkit cannot locate an EnergyPlus installation.

**Solutions:**

1. Install EnergyPlus from [energyplus.net/downloads](https://energyplus.net/downloads)

2. Set the `ENERGYPLUS_DIR` environment variable:
   ```bash
   export ENERGYPLUS_DIR=/path/to/EnergyPlus-24-1-0
   ```

3. Pass the path explicitly:
   ```python
   from idfkit.simulation import find_energyplus
   config = find_energyplus("/path/to/EnergyPlus")
   result = simulate(model, weather, energyplus=config)
   ```

### SimulationError

```
SimulationError: Weather file not found: /path/to/weather.epw
```

**Cause:** The specified weather file doesn't exist.

**Solutions:**

1. Verify the path is correct
2. Use absolute paths instead of relative
3. Download weather files using `WeatherDownloader`

### SimulationError (Timeout)

```
SimulationError: Simulation timed out after 3600 seconds
```

**Cause:** The simulation exceeded the timeout limit.

**Solutions:**

1. Increase the timeout:
   ```python
   result = simulate(model, weather, timeout=7200.0)
   ```

2. Use design-day-only mode for testing:
   ```python
   result = simulate(model, weather, design_day=True)
   ```

3. Check for infinite loops in the model

### NoDesignDaysError

```
NoDesignDaysError: No heating design days found in DDY file
```

**Cause:** The DDY file doesn't contain the requested design day type.

**Solutions:**

1. Check available design days:
   ```python
   ddm = DesignDayManager("file.ddy")
   print(ddm.summary())
   ```

2. Use a different percentile:
   ```python
   ddm.apply_to_model(model, heating="99%", cooling="1%")
   ```

### GeocodingError

```
GeocodingError: No results found for address: ...
```

**Cause:** The address couldn't be geocoded.

**Solutions:**

1. Try a more specific address
2. Try a different format (city name, ZIP code, landmark)
3. Use coordinates directly:
   ```python
   results = index.nearest(41.88, -87.63)
   ```

## Import Errors

### Missing Optional Dependencies

```
ImportError: pandas is required for DataFrame conversion
```

**Solutions:**

```bash
# Install specific extra
pip install idfkit[dataframes]

# Or install all extras
pip install idfkit[all]
```

Common extras:

| Feature | Install Command |
|---------|-----------------|
| DataFrames | `pip install idfkit[dataframes]` |
| Plotting (matplotlib) | `pip install idfkit[plot]` |
| Plotting (plotly) | `pip install idfkit[plotly]` |
| S3 Storage | `pip install idfkit[s3]` |
| Weather refresh | `pip install idfkit[weather]` |

### boto3 Not Found

```
ImportError: boto3 is required for S3FileSystem
```

**Solution:**

```bash
pip install idfkit[s3]
```

## Validation Errors

### Reference to Non-Existent Object

```
[ERROR] People:'Zone1_People'.zone_name: Reference to non-existent object 'ZONE1'
```

**Cause:** A field references an object name that doesn't exist.

**Solutions:**

1. Check the object name spelling (case-insensitive)
2. Add the missing object:
   ```python
   model.add("Zone", "Zone1", ...)
   ```
3. Fix the reference:
   ```python
   people_obj.zone_name = "Correct_Zone_Name"
   ```

### Required Field Missing

```
[ERROR] People:'Zone1_People'.activity_level_schedule_name: Required field is missing
```

**Cause:** A required field wasn't provided.

**Solution:**

```python
# Add the required field
model.add(
    "People", "Zone1_People",
    zone_or_zonelist_or_space_or_spacelist_name="Zone1",
    number_of_people_schedule_name="Always_On",
    activity_level_schedule_name="Activity_Schedule",  # Required!
    number_of_people_calculation_method="People",
    number_of_people=10,
)
```

## File Format Errors

### Invalid IDF Syntax

```
ValueError: Failed to parse IDF at line 42
```

**Cause:** The IDF file has invalid syntax.

**Solutions:**

1. Check for unclosed objects (missing `;`)
2. Check for invalid field separators
3. Validate with EnergyPlus directly first

### Version Mismatch

```
ValueError: Schema for version (99, 0, 0) not found
```

**Cause:** The IDF version isn't supported.

**Solutions:**

1. Check supported versions:
   ```python
   from idfkit import get_schema_manager
   print(get_schema_manager().get_available_versions())
   ```

2. Specify a supported version:
   ```python
   doc = load_idf("file.idf", version=(24, 1, 0))
   ```

## Performance Issues

### Slow Station Index Loading

**Cause:** First load compiles the index from source files.

**Solution:** Subsequent loads are instant (uses cached index).

### Large Memory Usage

**Cause:** Loading many large models or keeping many results in memory.

**Solutions:**

1. Use `model = None` to release memory after use
2. Process batch results incrementally:
   ```python
   for result in batch:
       process(result)
       # Result memory released when loop continues
   ```

## See Also

- [EnergyPlus Issues](energyplus.md) — EnergyPlus-specific errors
- [Simulation Error Handling](../simulation/errors.md) — Detailed error parsing
