# SQL Output Queries

The `SQLResult` class provides structured access to EnergyPlus's SQLite
output database, containing time-series data, tabular reports, and metadata.

## Opening the Database

```python
from idfkit.simulation import simulate

result = simulate(model, weather)

sql = result.sql
if sql is not None:
    # Query data...
```

Or open directly:

```python
from idfkit.simulation import SQLResult

sql = SQLResult("/path/to/eplusout.sql")
```

## Time-Series Data

### Basic Query

```python
ts = sql.get_timeseries(
    variable_name="Zone Mean Air Temperature",
    key_value="THERMAL ZONE 1",
)

print(f"Variable: {ts.variable_name}")
print(f"Key: {ts.key_value}")
print(f"Units: {ts.units}")
print(f"Frequency: {ts.frequency}")
print(f"Data points: {len(ts.values)}")
print(f"Min: {min(ts.values):.1f}, Max: {max(ts.values):.1f}")
```

### TimeSeriesResult Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `variable_name` | `str` | Output variable name |
| `key_value` | `str` | Key (zone, surface, etc.) |
| `units` | `str` | Variable units |
| `frequency` | `str` | Reporting frequency |
| `timestamps` | `tuple[datetime, ...]` | Timestamps for each point |
| `values` | `tuple[float, ...]` | Numeric values |

### Filtering by Environment

Specify which simulation environment to query:

```python
# Design day results only
ts = sql.get_timeseries(
    "Zone Mean Air Temperature",
    "ZONE 1",
    environment_name="CHICAGO ANN HTG 99.6% CONDNS DB",
)

# Run period results only
ts = sql.get_timeseries(
    "Zone Mean Air Temperature",
    "ZONE 1",
    environment_name="RUN PERIOD 1",
)
```

### Converting to DataFrame

```python
df = ts.to_dataframe()
print(df.head())
#                              Zone Mean Air Temperature
# timestamp
# 2017-01-01 01:00:00                               21.2
# 2017-01-01 02:00:00                               21.1
# ...
```

Requires pandas: `pip install idfkit[dataframes]`

### Plotting Time Series

```python
fig = ts.plot()  # Auto-detects matplotlib/plotly
```

Requires matplotlib or plotly: `pip install idfkit[plot]`

## Tabular Data

### Query Tabular Reports

```python
rows = sql.get_tabular_data(
    report_name="AnnualBuildingUtilityPerformanceSummary"
)

for row in rows[:5]:
    print(f"{row.table_name} | {row.row_name} | {row.column_name}: {row.value}")
```

### TabularRow Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `report_name` | `str` | Report name |
| `report_for` | `str` | Report scope (e.g., "Entire Facility") |
| `table_name` | `str` | Table name within report |
| `row_name` | `str` | Row label |
| `column_name` | `str` | Column label |
| `units` | `str` | Value units |
| `value` | `str` | Cell value as string |

### Filter by Table

```python
rows = sql.get_tabular_data(
    report_name="AnnualBuildingUtilityPerformanceSummary",
    table_name="Site and Source Energy",
)
```

### Common Reports

| Report Name | Description |
|-------------|-------------|
| `AnnualBuildingUtilityPerformanceSummary` | Energy use summary |
| `InputVerificationandResultsSummary` | Model summary |
| `EnvelopeSummary` | Building envelope details |
| `LightingSummary` | Lighting power densities |
| `EquipmentSummary` | Equipment capacities |
| `HVACSizingSummary` | HVAC sizing results |
| `ZoneComponentLoadSummary` | Zone load components |

## Variable Metadata

### List Available Variables

```python
variables = sql.get_available_variables()

for var in variables[:10]:
    print(f"{var.name} ({var.key_value}) [{var.units}] - {var.frequency}")
```

### VariableInfo Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Variable name |
| `key_value` | `str` | Key value |
| `frequency` | `str` | Reporting frequency |
| `units` | `str` | Variable units |
| `is_meter` | `bool` | Whether this is a meter |
| `variable_type` | `str` | Variable type (Zone, HVAC, etc.) |

### Search Variables

```python
# By name pattern
temp_vars = [v for v in variables if "Temperature" in v.name]

# By key
zone1_vars = [v for v in variables if v.key_value == "ZONE 1"]
```

## Environment Metadata

### List Environments

```python
environments = sql.get_environments()

for env in environments:
    print(f"{env.index}: {env.name} (type={env.environment_type})")
```

### Environment Types

| Type | Value | Description |
|------|-------|-------------|
| Design Day | 1 | `SizingPeriod:DesignDay` simulation |
| Design Run Period | 2 | `SizingPeriod:WeatherFileDays` |
| Weather File Run Period | 3 | Regular `RunPeriod` simulation |

### EnvironmentInfo Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `index` | `int` | Environment period index |
| `name` | `str` | Environment name |
| `environment_type` | `int` | Type code (1, 2, or 3) |

## Timestamps

EnergyPlus uses a fixed reference year (2017) for timestamps. The SQLResult
automatically converts database timestamps to Python `datetime` objects.

### EnergyPlus Time Convention

- Hour 24 in the database → midnight of the next day
- Warmup days are filtered out automatically

```python
ts = sql.get_timeseries("Zone Mean Air Temperature", "ZONE 1")

# Timestamps are proper Python datetime objects
first = ts.timestamps[0]
print(f"Year: {first.year}")   # 2017 (reference year)
print(f"Month: {first.month}")
print(f"Day: {first.day}")
print(f"Hour: {first.hour}")
```

## Context Manager

`SQLResult` is a context manager for clean database cleanup:

```python
with SQLResult("/path/to/eplusout.sql") as sql:
    ts = sql.get_timeseries("Zone Mean Air Temperature", "ZONE 1")
    # Connection automatically closed on exit
```

## Error Handling

```python
sql = result.sql
if sql is None:
    print("No SQL output - was Output:SQLite in the model?")
    return

# Get time series (returns None if not found)
ts = sql.get_timeseries("Nonexistent Variable", "ZONE 1")
if ts is None:
    print("Variable not found in database")
```

## Performance Tips

1. **Filter early** — Use `environment_name` to reduce data size
2. **Query once** — Store results in variables rather than re-querying
3. **Use lazy loading** — Don't access `result.sql` if you don't need it

## See Also

- [Parsing Results](results.md) — Overview of result parsing
- [Plotting](plotting.md) — Visualizing query results
- [Output Discovery](output-discovery.md) — Finding available variables
