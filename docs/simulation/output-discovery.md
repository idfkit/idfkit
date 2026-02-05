# Output Discovery

The `OutputVariableIndex` helps you discover available output variables
and meters from EnergyPlus, then add them to your model for future simulations.

## Basic Usage

```python
from idfkit.simulation import simulate

result = simulate(model, weather)

variables = result.variables
if variables is not None:
    # Search for temperature-related outputs
    matches = variables.search("Temperature")
    for var in matches[:10]:
        print(f"{var.name} [{var.units}]")
```

## Understanding RDD and MDD Files

EnergyPlus generates these files to describe available outputs:

| File | Contents |
|------|----------|
| `.rdd` | Output variables (zone temps, surface temps, etc.) |
| `.mdd` | Output meters (energy consumption, etc.) |

These files are only generated after a simulation runs — they describe
what outputs **could be** requested, not what was actually recorded.

## OutputVariableIndex

### Creating an Index

From simulation results:

```python
variables = result.variables
```

From files directly:

```python
from idfkit.simulation import OutputVariableIndex

index = OutputVariableIndex.from_files(
    rdd_path="/path/to/eplusout.rdd",
    mdd_path="/path/to/eplusout.mdd",
)
```

### Search Variables

```python
# Search by name pattern
matches = variables.search("Zone Mean Air Temperature")

# Search with regex
matches = variables.search(r"Zone.*Temperature")

# Case-insensitive
matches = variables.search("temperature")  # Finds all temperature vars
```

### Filter by Units

```python
# Get all temperature variables (°C)
temp_vars = variables.filter_by_units("C")

# Get all energy variables
energy_vars = variables.filter_by_units("J")
```

### List All Variables

```python
# All output variables
for var in variables.variables:
    print(f"Variable: {var.name} [{var.units}]")

# All meters
for meter in variables.meters:
    print(f"Meter: {meter.name} [{meter.units}]")
```

## OutputVariable and OutputMeter

### OutputVariable Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Variable name |
| `units` | `str` | Variable units |
| `key_options` | `str` | Key types (e.g., "Zone", "*") |

### OutputMeter Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Meter name |
| `units` | `str` | Meter units |
| `resource_type` | `str` | Resource being measured |
| `end_use` | `str` | End use category |

## Adding Outputs to Model

### Add All Matching

```python
# Add all temperature outputs
count = variables.add_all_to_model(
    model,
    filter_pattern="Zone.*Temperature",
)
print(f"Added {count} output requests")
```

### Selective Addition

```python
# Search first, review, then add selectively
matches = variables.search("Heating")

# Filter to specific ones
selected = [v for v in matches if "Coil" in v.name]

# Add to model (name is optional for Output:Variable)
for var in selected:
    model.add(
        "Output:Variable",
        key_value="*",
        variable_name=var.name,
        reporting_frequency="Timestep",
    )
```

### Reporting Frequencies

| Frequency | Description |
|-----------|-------------|
| `"Detailed"` | Every zone timestep |
| `"Timestep"` | Every zone timestep |
| `"Hourly"` | Once per hour |
| `"Daily"` | Once per day |
| `"Monthly"` | Once per month |
| `"RunPeriod"` | Once per run period |
| `"Environment"` | Once per environment |

```python
variables.add_all_to_model(
    model,
    filter_pattern="Temperature",
    reporting_frequency="Hourly",
)
```

## Workflow: Discover Then Request

A common pattern is to run a "discovery" simulation to find available
outputs, then run a second simulation with those outputs requested:

```python
from idfkit.simulation import simulate

# Step 1: Discovery run
result = simulate(model, weather, design_day=True)

# Step 2: Find interesting outputs
matches = result.variables.search("Zone Mean Air Temperature")
print(f"Found {len(matches)} matching variables")

# Step 3: Add outputs to model
result.variables.add_all_to_model(
    model,
    filter_pattern="Zone Mean Air Temperature",
    reporting_frequency="Hourly",
)

# Step 4: Full run with outputs
result = simulate(model, weather, annual=True)

# Step 5: Query the data
for zone in ["ZONE 1", "ZONE 2"]:
    ts = result.sql.get_timeseries(
        "Zone Mean Air Temperature",
        zone,
    )
    print(f"{zone}: avg {sum(ts.values)/len(ts.values):.1f}°C")
```

## Common Output Variables

### Zone-Level

| Variable | Description |
|----------|-------------|
| `Zone Mean Air Temperature` | Average zone air temperature |
| `Zone Air Relative Humidity` | Zone relative humidity |
| `Zone Air System Sensible Cooling Energy` | Cooling energy delivered |
| `Zone Air System Sensible Heating Energy` | Heating energy delivered |
| `Zone People Total Heating Energy` | Heat from occupants |
| `Zone Lights Total Heating Energy` | Heat from lights |
| `Zone Electric Equipment Total Heating Energy` | Heat from equipment |

### Surface-Level

| Variable | Description |
|----------|-------------|
| `Surface Inside Face Temperature` | Interior surface temperature |
| `Surface Outside Face Temperature` | Exterior surface temperature |
| `Surface Inside Face Convection Heat Transfer Coefficient` | Interior convection |
| `Surface Outside Face Convection Heat Transfer Coefficient` | Exterior convection |

### HVAC

| Variable | Description |
|----------|-------------|
| `Zone Ideal Loads Supply Air Total Cooling Energy` | Ideal loads cooling |
| `Zone Ideal Loads Supply Air Total Heating Energy` | Ideal loads heating |
| `Facility Total Electric Demand Power` | Total electric load |

## Common Meters

| Meter | Description |
|-------|-------------|
| `Electricity:Facility` | Total facility electricity |
| `Gas:Facility` | Total facility gas |
| `Heating:Electricity` | Heating electricity |
| `Cooling:Electricity` | Cooling electricity |
| `InteriorLights:Electricity` | Interior lighting electricity |
| `InteriorEquipment:Electricity` | Interior equipment electricity |

## See Also

- [SQL Output Queries](sql-queries.md) — Querying recorded data
- [Parsing Results](results.md) — Working with SimulationResult
- [Running Simulations](running.md) — Basic simulation guide
