# Parsing Results

The `SimulationResult` class provides structured access to all EnergyPlus
output files with lazy loading for efficient memory usage.

## SimulationResult Overview

```python
from idfkit.simulation import simulate

result = simulate(model, weather)

# Basic info
print(f"Success: {result.success}")
print(f"Exit code: {result.exit_code}")
print(f"Runtime: {result.runtime_seconds:.1f}s")
print(f"Output dir: {result.run_dir}")

# Parsed outputs (lazy-loaded)
result.errors     # ErrorReport from .err file
result.sql        # SQLResult from .sql database
result.variables  # OutputVariableIndex from .rdd/.mdd
result.csv        # CSVResult from .csv file
result.html       # HTMLResult from HTML tabular output
```

## Output File Paths

Access paths to specific output files:

```python
result.sql_path   # Path to .sql database
result.err_path   # Path to .err file
result.eso_path   # Path to .eso file
result.csv_path   # Path to .csv file
result.html_path  # Path to HTML table file
result.rdd_path   # Path to .rdd file
result.mdd_path   # Path to .mdd file
```

Each returns `None` if the file wasn't produced.

## Error Report

Parse warnings and errors from the `.err` file:

```python
errors = result.errors

# Summary
print(errors.summary())

# Check for fatal errors
if errors.has_fatal:
    for err in errors.fatal:
        print(f"FATAL: {err.message}")

# Check for severe errors
if errors.has_severe:
    for err in errors.severe:
        print(f"SEVERE: {err.message}")

# All warnings
for warn in errors.warnings:
    print(f"Warning: {warn.message}")

# Counts
print(f"Fatal: {errors.fatal_count}")
print(f"Severe: {errors.severe_count}")
print(f"Warnings: {errors.warning_count}")
```

See [Error Handling](errors.md) for detailed error parsing.

## SQL Database

Query time-series and tabular data from the SQLite output:

```python
sql = result.sql
if sql is not None:
    # Time-series data
    ts = sql.get_timeseries(
        variable_name="Zone Mean Air Temperature",
        key_value="THERMAL ZONE 1",
    )
    print(f"Max: {max(ts.values):.1f}°C")

    # Tabular reports
    rows = sql.get_tabular_data(
        report_name="AnnualBuildingUtilityPerformanceSummary"
    )
```

See [SQL Output Queries](sql-queries.md) for detailed SQL parsing.

## Output Variables

Discover available output variables from `.rdd`/`.mdd` files:

```python
variables = result.variables
if variables is not None:
    # Search for variables
    matches = variables.search("Temperature")
    for var in matches:
        print(f"{var.name} [{var.units}]")

    # Add outputs to model for next run
    variables.add_all_to_model(model, filter_pattern="Zone.*Temperature")
```

See [Output Discovery](output-discovery.md) for variable discovery.

## CSV Output

Parse CSV time-series output:

```python
csv_result = result.csv
if csv_result is not None:
    # List all columns
    for col in csv_result.columns:
        print(f"{col.variable_name} ({col.key_value}) [{col.units}]")

    # Get data for a specific column
    values = csv_result.get_column_values("Zone Mean Air Temperature")
```

## HTML Tabular Output

Parse the HTML tabular summary file (`eplustbl.htm`) that EnergyPlus
produces alongside every simulation:

```python
html = result.html
if html is not None:
    # Iterate all tables
    for table in html:
        print(f"{table.title}: {len(table.rows)} rows")

    # eppy-compatible (title, rows) pairs
    for title, rows in html.titletable():
        print(title)

    # Look up a table by title (case-insensitive substring match)
    table = html.tablebyname("Site and Source Energy")
    if table:
        data = table.to_dict()  # {row_key: {col_header: value}}
        print(data)

    # Get all tables from a specific report
    annual = html.tablesbyreport("Annual Building Utility Performance Summary")

    # Access by index
    first = html.tablebyindex(0)
```

Each `HTMLTable` has these attributes:

| Attribute | Type | Description |
|-----------|------|-------------|
| `title` | `str` | Bold title preceding the table |
| `header` | `list[str]` | Column headers |
| `rows` | `list[list[str]]` | Data rows |
| `report_name` | `str` | Parent report name |
| `for_string` | `str` | The "For:" qualifier (e.g. "Entire Facility") |

You can also parse a standalone HTML file without a full simulation:

```python
from idfkit.simulation.parsers.html import HTMLResult

html = HTMLResult.from_file("eplustbl.htm")
html = HTMLResult.from_string(html_string)
```

This replaces eppy's `readhtml` module.

## Lazy Loading

Output files are parsed only when accessed:

```python
result = simulate(model, weather)

# Nothing parsed yet - only metadata stored

result.errors    # NOW parses .err file
result.sql       # NOW opens SQLite database
result.variables # NOW parses .rdd/.mdd files
result.html      # NOW parses HTML tabular output
```

This keeps memory usage low, especially for batch simulations where you
might only need specific outputs.

## Reconstructing from Directory

Inspect results from a previous simulation:

```python
from idfkit.simulation import SimulationResult

# From a local directory
result = SimulationResult.from_directory("/path/to/sim_output")

# From a cloud storage location
from idfkit.simulation import S3FileSystem
fs = S3FileSystem(bucket="my-bucket")
result = SimulationResult.from_directory("runs/run-001", fs=fs)

# Query data
ts = result.sql.get_timeseries(
    "Zone Mean Air Temperature",
    "ZONE 1"
)
```

## Attributes Reference

| Attribute | Type | Description |
|-----------|------|-------------|
| `run_dir` | `Path` | Directory containing output files |
| `success` | `bool` | Whether simulation succeeded |
| `exit_code` | `int \| None` | Process exit code (None if timed out) |
| `stdout` | `str` | Captured standard output |
| `stderr` | `str` | Captured standard error |
| `runtime_seconds` | `float` | Wall-clock execution time |
| `output_prefix` | `str` | Output file prefix (default "eplus") |

## Properties Reference

| Property | Type | Description |
|----------|------|-------------|
| `errors` | `ErrorReport` | Parsed error/warning report |
| `sql` | `SQLResult \| None` | SQL database accessor |
| `variables` | `OutputVariableIndex \| None` | Variable discovery |
| `csv` | `CSVResult \| None` | CSV output parser |
| `html` | `HTMLResult \| None` | HTML tabular output parser |
| `sql_path` | `Path \| None` | Path to .sql file |
| `err_path` | `Path \| None` | Path to .err file |
| `eso_path` | `Path \| None` | Path to .eso file |
| `csv_path` | `Path \| None` | Path to .csv file |
| `html_path` | `Path \| None` | Path to HTML file |
| `rdd_path` | `Path \| None` | Path to .rdd file |
| `mdd_path` | `Path \| None` | Path to .mdd file |

## See Also

- [SQL Output Queries](sql-queries.md) — Detailed SQL database access
- [Output Discovery](output-discovery.md) — Finding available variables
- [Error Handling](errors.md) — Parsing error reports
