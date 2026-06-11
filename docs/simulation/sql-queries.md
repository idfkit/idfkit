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
--8<-- "docs/snippets/simulation/sql-queries/opening_the_database_2.py:example"
```

## Time-Series Data

### Basic Query

```python
--8<-- "docs/snippets/simulation/sql-queries/basic_query.py:example"
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
--8<-- "docs/snippets/simulation/sql-queries/filtering_by_environment.py:example"
```

The `environment` parameter accepts:

| Value | Description |
|-------|-------------|
| `None` | All data from all environments (default) |
| `"annual"` | Weather-file run period data only |
| `"sizing"` | Design day data only |

### Converting to DataFrame

```python
--8<-- "docs/snippets/simulation/sql-queries/converting_to_dataframe.py:example"
```

Requires pandas: `pip install idfkit[dataframes]`

### Plotting Time Series

```python
--8<-- "docs/snippets/simulation/sql-queries/plotting_time_series.py:example"
```

Requires matplotlib or plotly: `pip install idfkit[plot]`

## Tabular Data

### Query Tabular Reports

```python
--8<-- "docs/snippets/simulation/sql-queries/query_tabular_reports.py:example"
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
--8<-- "docs/snippets/simulation/sql-queries/filter_by_table.py:example"
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
--8<-- "docs/snippets/simulation/sql-queries/list_available_variables.py:example"
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
--8<-- "docs/snippets/simulation/sql-queries/search_variables.py:example"
```

## Environment Metadata

### List Environments

```python
--8<-- "docs/snippets/simulation/sql-queries/list_environments.py:example"
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
--8<-- "docs/snippets/simulation/sql-queries/energyplus_time_convention.py:example"
```

## Context Manager

`SQLResult` is a context manager for clean database cleanup:

```python
--8<-- "docs/snippets/simulation/sql-queries/context_manager.py:example"
```

`SimulationResult` — the usual entry point via `simulate()` — is also a
context manager. Exiting the `with` block closes the SQLite connection that
`result.sql` opened lazily, which matters on Windows where the open
connection locks `eplus.sql` and blocks deleting the run directory:

```python
--8<-- "docs/snippets/simulation/sql-queries/simulationresult_context_manager.py:example"
```

See [Releasing File Handles](results.md#releasing-file-handles) for details.

## Error Handling

```python
--8<-- "docs/snippets/simulation/sql-queries/error_handling.py:example"
```

## Performance Tips

1. **Filter early** — Use the `environment` parameter to reduce data size
2. **Query once** — Store results in variables rather than re-querying
3. **Use lazy loading** — Don't access `result.sql` if you don't need it

## See Also

- [Parsing Results](results.md) — Overview of result parsing
- [Plotting](plotting.md) — Visualizing query results
- [Output Discovery](output-discovery.md) — Finding available variables
