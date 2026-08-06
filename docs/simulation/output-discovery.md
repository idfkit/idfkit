# How to discover output variables

The `OutputVariableIndex` helps you discover available output variables
and meters from EnergyPlus, then add them to your model for future simulations.

## Basic Usage

```python
--8<-- "docs/snippets/simulation/output-discovery/basic_usage.py:example"
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
--8<-- "docs/snippets/simulation/output-discovery/creating_an_index.py:example"
```

From files directly:

```python
--8<-- "docs/snippets/simulation/output-discovery/creating_an_index_2.py:example"
```

### Search Variables

```python
--8<-- "docs/snippets/simulation/output-discovery/search_variables.py:example"
```

### Filter by Units

```python
--8<-- "docs/snippets/simulation/output-discovery/filter_by_units.py:example"
```

### List All Variables

```python
--8<-- "docs/snippets/simulation/output-discovery/list_all_variables.py:example"
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
--8<-- "docs/snippets/simulation/output-discovery/add_all_matching.py:example"
```

### Selective Addition

```python
--8<-- "docs/snippets/simulation/output-discovery/selective_addition.py:example"
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
--8<-- "docs/snippets/simulation/output-discovery/reporting_frequencies.py:example"
```

## Workflow: Discover Then Request

A common pattern is to run a "discovery" simulation to find available
outputs, then run a second simulation with those outputs requested:

```python
--8<-- "docs/snippets/simulation/output-discovery/workflow_discover_then_request.py:example"
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
