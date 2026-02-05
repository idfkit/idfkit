# Quick Start

Get up and running with idfkit in 5 minutes. This guide covers the essential
operations you'll use every day.

## Load a Model

```python
from idfkit import load_idf

# Load an existing IDF file
model = load_idf("building.idf")
print(f"Loaded {len(model)} objects")
```

## Query Objects

Access objects with O(1) dictionary lookups:

```python
# Get all zones
for zone in model["Zone"]:
    print(f"Zone: {zone.name}")

# Get a specific zone by name
office = model["Zone"]["Office"]
print(f"Origin: ({office.x_origin}, {office.y_origin}, {office.z_origin})")
```

## Modify Fields

Change field values with attribute assignment:

```python
# Update a field
office.x_origin = 10.0

# See what references this zone
for obj in model.get_referencing("Office"):
    print(f"  {obj.obj_type}: {obj.name}")
```

## Discover Available Fields

Not sure what fields an object type has? Use `describe()` to see all available fields:

```python
# See all fields for a Zone
print(model.describe("Zone"))
# === Zone ===
# ...
# Fields (9):
#   direction_of_relative_north (number) [deg] default=0
#   x_origin (number) [m] default=0
#   ...

# See required fields for a Material
desc = model.describe("Material")
print(f"Required: {desc.required_fields}")
# Required: ['roughness', 'thickness', 'conductivity', 'density', 'specific_heat']
```

In REPL/Jupyter, use tab completion to explore object fields:

```python
zone = model["Zone"]["Office"]
zone.<TAB>  # Shows: x_origin, y_origin, z_origin, multiplier, ...
```

Validation is enabled by default, so typos are caught immediately:

```python
model.add("Zone", "Office", x_orgin=0)  # Raises: unknown field 'x_orgin'

# Disable validation for bulk operations where performance matters
model.add("Zone", "Office", x_origin=0, validate=False)
```

## Create a New Model

```python
from idfkit import new_document

# Create an empty model for EnergyPlus 24.1
model = new_document(version=(24, 1, 0))

# Add named objects
model.add("Building", "My Building", north_axis=0, terrain="City")
model.add("Zone", "Office", x_origin=0, y_origin=0, z_origin=0)

# Add unnamed objects (name parameter is optional)
model.add("Timestep", number_of_timesteps_per_hour=4)
model.add("GlobalGeometryRules",
          starting_vertex_position="UpperLeftCorner",
          vertex_entry_direction="Counterclockwise",
          coordinate_system="Relative")
```

## Write Output

```python
from idfkit import write_idf, write_epjson

# Write to IDF format
write_idf(model, "output.idf")

# Or write to epJSON format
write_epjson(model, "output.epJSON")

# Get as string (no file path)
idf_string = write_idf(model)
```

## Run a Simulation

```python
from idfkit.simulation import simulate

result = simulate(
    model,
    weather="weather.epw",
    design_day=True,  # Fast design-day run
)

print(f"Success: {result.success}")
print(f"Runtime: {result.runtime_seconds:.1f}s")

# Check for errors
if result.errors.has_fatal:
    for err in result.errors.fatal:
        print(f"Error: {err.message}")
```

## Query Results

```python
# Get time-series data from SQLite output
ts = result.sql.get_timeseries(
    variable_name="Zone Mean Air Temperature",
    key_value="Office",
)
print(f"Variable: {ts.variable_name}")
print(f"Temperature range: {min(ts.values):.1f}°C to {max(ts.values):.1f}°C")

# Filter by environment if needed
ts_sizing = result.sql.get_timeseries(
    variable_name="Zone Mean Air Temperature",
    key_value="Office",
    environment="sizing",  # Design day data only
)

# Get tabular data
tables = result.sql.get_tabular_data(
    report_name="AnnualBuildingUtilityPerformanceSummary"
)
```

## Find Weather Stations

```python
from idfkit.weather import StationIndex, geocode

# Load the station index (instant, no network needed)
index = StationIndex.load()

# Search by name
results = index.search("chicago ohare")
print(results[0].station.display_name)

# Find nearest station to an address
results = index.nearest(*geocode("Willis Tower, Chicago, IL"))
station = results[0].station
print(f"{station.display_name}: {results[0].distance_km:.0f} km away")
```

## Apply Design Days

```python
from idfkit.weather import DesignDayManager

# Parse a DDY file and apply design days to your model
ddm = DesignDayManager("weather.ddy")
added = ddm.apply_to_model(
    model,
    heating="99.6%",
    cooling="1%",
    update_location=True,
)
print(f"Added {len(added)} design days")
```

## Next Steps

- [Core Tutorial](core-tutorial.ipynb) - Complete interactive walkthrough
- [Simulation Guide](../simulation/index.md) - Deep dive into simulation features
- [Weather Guide](../weather/index.md) - Weather station search and design days
- [API Reference](../api/document.md) - Full API documentation
