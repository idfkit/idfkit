# idfkit Developer Guide (for CLAUDE.md)

> Copy this section into your project's `CLAUDE.md` to give Claude Code context on idfkit usage.

---

## idfkit Dependency Guide

**idfkit** is a Python toolkit for EnergyPlus IDF/epJSON files. It provides O(1) object lookups, automatic reference tracking, schema-driven validation, simulation execution, weather data, schedule evaluation, thermal calculations, and 3D geometry operations. Zero third-party dependencies for the core package (including simulation, schedules, thermal, and geometry). Optional extras: `weather` (openpyxl), `pandas`, `plot` (matplotlib), `plotly`, `progress` (tqdm), `s3`/`async-s3` (cloud storage), or `all`.

### Loading & Creating Documents

```python
from idfkit import load_idf, load_epjson, new_document

model = load_idf("building.idf")               # Load IDF file
model = load_epjson("building.epjson")          # Load epJSON file
model = new_document()                          # New doc (latest EnergyPlus version)
model = new_document(version=(24, 1, 0))        # Specific version
```

### Accessing Objects (O(1) Lookups)

```python
# By IDF type name (dict-style) — returns IDFCollection
zones = model["Zone"]
zone = zones["Office"]                          # O(1) by name

# By Python attribute — snake_case mapped to IDF type
zones = model.zones                             # same as model["Zone"]
surfaces = model.building_surfaces              # BuildingSurface:Detailed

# Iteration
for obj_type in model:                          # iterate object types
    for obj in model[obj_type]:                 # iterate objects of that type
        print(obj.name)
```

### Creating & Modifying Objects

```python
# Add objects — fields use snake_case Python names
zone = model.add("Zone", "Office", x_origin=0.0, y_origin=0.0, z_origin=0.0)

# Modify fields via attribute access
zone.x_origin = 10.0

# Rename (auto-updates all references across the document)
model.rename("Zone", "Office", "Office_A")

# Remove
model.removeidfobject(zone)

# Deep copy entire document
model_copy = model.copy()
```

### Reference Tracking

```python
# Find all objects that reference a given name (O(1))
refs = model.references.get_referencing("Office")        # set of IDFObjects
refs = model.references.get_referencing_with_fields("Office")  # set of (obj, field)

# Check if a name is referenced
model.references.is_referenced("Office")  # bool
```

### Writing Files

```python
from idfkit import write_idf, write_epjson

write_idf(model, "output.idf")
write_epjson(model, "output.epjson")
```

### Validation

```python
from idfkit import validate_document

result = validate_document(model)
print(result.is_valid)          # bool
for err in result.errors:       # ValidationError objects
    print(err.obj_type, err.field, err.message)
```

### Schema Introspection

```python
desc = model.describe("Zone")       # ObjectDescription
for field in desc.fields:           # FieldDescription objects
    print(field.name, field.field_type, field.required, field.default)
```

### Simulation (no extras required; requires EnergyPlus installed)

```python
from idfkit.simulation import simulate, async_simulate
from idfkit.simulation import simulate_batch, SimulationJob

# Sync
result = simulate(model, weather="weather.epw", design_day=True)
print(result.success, result.runtime_seconds)

# Access SQL results
ts = result.sql.get_timeseries("Zone Mean Air Temperature", "Office")

# Async
result = await async_simulate(model, weather="weather.epw")

# Batch (parallel)
jobs = [SimulationJob(model, "w1.epw", label="Run1"),
        SimulationJob(model, "w2.epw", label="Run2")]
batch = simulate_batch(jobs, max_workers=4)
print(batch.all_succeeded)
for r in batch.succeeded:
    print(r.label, r.result.success)
```

### Weather Data (bundled index; `idfkit[weather]` extra for index refresh)

```python
from idfkit.weather import WeatherDownloader

dl = WeatherDownloader()
results = dl.search("San Francisco")            # text search (~17k stations)
spatial = dl.search_spatial(37.77, -122.42)      # geographic search
station = results[0].station
dl.download(station, "./weather")                # downloads EPW + DDY

# Inject design days into model
from idfkit.weather import inject_design_days
inject_design_days(model, "./weather/station.ddy")
```

### Schedule Evaluation (no extras required)

```python
from datetime import datetime
from idfkit.schedules import evaluate, values

# Evaluate at a point in time (supports all 8 EnergyPlus schedule types)
val = evaluate(schedule_obj, datetime(2024, 7, 15, 14, 0), document=model)

# Generate annual timeseries (returns DataFrame if pandas available)
df = values(schedule_obj, year=2024, timestep=1, document=model)

# Create schedules
from idfkit.schedules import create_constant_schedule
sched = create_constant_schedule(model, "AlwaysOn", value=1.0)
```

### Thermal Properties (no extras required)

```python
from idfkit.thermal import calculate_u_value, calculate_r_value
from idfkit.thermal import calculate_shgc, get_thermal_properties

u = calculate_u_value(construction_obj)    # W/m²·K (with films)
r = calculate_r_value(construction_obj)    # m²·K/W (without films)
shgc = calculate_shgc(construction_obj)    # glazing only

props = get_thermal_properties(construction_obj)  # full breakdown
for layer in props.layers:
    print(layer.name, layer.r_value)
```

### Geometry

```python
from idfkit import Vector3D, Polygon3D
from idfkit.geometry import (
    calculate_surface_area, calculate_zone_volume,
    translate_building, rotate_building, scale_building,
    intersect_match, set_wwr,
)

# Surface/zone calculations
area = calculate_surface_area(surface_obj)
vol = calculate_zone_volume(zone_obj)

# Building transforms
translate_building(model, dx=10, dy=0, dz=0)
rotate_building(model, angle=45)
scale_building(model, factor=1.5)

# Window-to-wall ratio
set_wwr(model, wwr=0.4)

# Surface intersection and matching
intersect_match(model)
```

### Key Patterns & Pitfalls

- **Version-bound**: Each document is tied to an EnergyPlus version. Supported: 8.9.0–25.2.0.
- **Snake-case fields**: Use `zone.x_origin`, not `zone["X Origin"]` (both work, attributes preferred).
- **Validation is opt-in**: Call `validate_document()` explicitly; parsing does not validate.
- **Rename cascades**: `model.rename()` updates all cross-references automatically.
- **Strict mode**: `model.strict = True` raises `AttributeError` on field typos (useful for debugging).
- **Optional extras**: Core features (simulation, schedules, thermal, geometry) need no extras. Install `idfkit[weather]` for index refresh, `idfkit[pandas]` for DataFrames, `idfkit[plot]`/`idfkit[plotly]` for plotting, `idfkit[progress]` for tqdm bars, `idfkit[s3]` for cloud storage, or `idfkit[all]`.

### Exception Hierarchy

All exceptions inherit from `IdfKitError`:
- `IDFParseError`, `ParseError` — parsing failures
- `UnknownObjectTypeError` — invalid IDF object type
- `DuplicateObjectError` — singleton constraint violation
- `ValidationFailedError` — validation errors
- `SimulationError`, `EnergyPlusNotFoundError` — simulation failures
- `VersionNotFoundError`, `SchemaNotFoundError` — version/schema issues
