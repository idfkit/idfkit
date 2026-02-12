# Parsing Results

The `SimulationResult` class provides structured access to all EnergyPlus
output files with lazy loading for efficient memory usage.

## SimulationResult Overview

```python
--8<-- "docs/snippets/simulation/results/simulationresult_overview.py:example"
```

## Output File Paths

Access paths to specific output files:

```python
--8<-- "docs/snippets/simulation/results/output_file_paths.py:example"
```

Each returns `None` if the file wasn't produced.

## Error Report

Parse warnings and errors from the `.err` file:

```python
--8<-- "docs/snippets/simulation/results/error_report.py:example"
```

See [Error Handling](errors.md) for detailed error parsing.

## SQL Database

Query time-series and tabular data from the SQLite output:

```python
--8<-- "docs/snippets/simulation/results/sql_database.py:example"
```

See [SQL Output Queries](sql-queries.md) for detailed SQL parsing.

## Output Variables

Discover available output variables from `.rdd`/`.mdd` files:

```python
--8<-- "docs/snippets/simulation/results/output_variables.py:example"
```

See [Output Discovery](output-discovery.md) for variable discovery.

## CSV Output

Parse CSV time-series output:

```python
--8<-- "docs/snippets/simulation/results/csv_output.py:example"
```

## HTML Tabular Output

Parse the HTML tabular summary file (`eplustbl.htm`) that EnergyPlus
produces alongside every simulation:

```python
--8<-- "docs/snippets/simulation/results/html_tabular_output.py:example"
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
--8<-- "docs/snippets/simulation/results/html_tabular_output_2.py:example"
```

This replaces eppy's `readhtml` module.

## Lazy Loading

Output files are parsed only when accessed:

```python
--8<-- "docs/snippets/simulation/results/lazy_loading.py:example"
```

This keeps memory usage low, especially for batch simulations where you
might only need specific outputs.

## Reconstructing from Directory

Inspect results from a previous simulation:

```python
--8<-- "docs/snippets/simulation/results/reconstructing_from_directory.py:example"
```

## Attributes Reference

| Attribute | Type | Description |
|-----------|------|-------------|
| `run_dir` | `Path` | Directory containing output files |
| `success` | `bool` | Whether simulation succeeded |
| `exit_code` | <code>int &#124; None</code> | Process exit code (None if timed out) |
| `stdout` | `str` | Captured standard output |
| `stderr` | `str` | Captured standard error |
| `runtime_seconds` | `float` | Wall-clock execution time |
| `output_prefix` | `str` | Output file prefix (default "eplus") |

## Properties Reference

| Property | Type | Description |
|----------|------|-------------|
| `errors` | `ErrorReport` | Parsed error/warning report |
| `sql` | <code>SQLResult &#124; None</code> | SQL database accessor |
| `variables` | <code>OutputVariableIndex &#124; None</code> | Variable discovery |
| `csv` | <code>CSVResult &#124; None</code> | CSV output parser |
| `html` | <code>HTMLResult &#124; None</code> | HTML tabular output parser |
| `sql_path` | <code>Path &#124; None</code> | Path to .sql file |
| `err_path` | <code>Path &#124; None</code> | Path to .err file |
| `eso_path` | <code>Path &#124; None</code> | Path to .eso file |
| `csv_path` | <code>Path &#124; None</code> | Path to .csv file |
| `html_path` | <code>Path &#124; None</code> | Path to HTML file |
| `rdd_path` | <code>Path &#124; None</code> | Path to .rdd file |
| `mdd_path` | <code>Path &#124; None</code> | Path to .mdd file |

## See Also

- [SQL Output Queries](sql-queries.md) — Detailed SQL database access
- [Output Discovery](output-discovery.md) — Finding available variables
- [Error Handling](errors.md) — Parsing error reports
