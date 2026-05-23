# Result parsing

`SimulationResult` is what `simulate(...)` returns. It's a thin container over the EnergyPlus output directory with typed accessors for the SQLite, CSV, HTML tabular, ERR, and RDD/MDD files. Use `result.sql` for almost everything — it's complete, queryable, and consistent across EnergyPlus versions.

## When to use

- A simulation has completed and you want time series or tabular reports.
- You're aggregating results across a batch (peak loads, energy totals, comfort hours).
- You need to read the `.err` file to surface warnings/errors.
- You want available output variables before adding `Output:Variable` objects.

## Quick start

```python
result = simulate(doc, "weather.epw")

# 1. Always check errors first
if result.errors.has_severe():
    print(result.errors.summary())
    raise SystemExit

# 2. Time series
ts = result.sql.get_timeseries("Zone Mean Air Temperature", "Office", frequency="Hourly")
print(max(ts.values), ts.units)            # 27.3 'C'

# 3. Tabular reports (annual energy, sizing, …)
rows = result.sql.get_tabular_data(report_name="AnnualBuildingUtilityPerformanceSummary")
```

## What's on `SimulationResult`

| Accessor | Returns | Lazy? |
|---|---|---|
| `result.errors` | `ErrorReport` (always available) | Eager (parsed on construction). |
| `result.sql` | `SQLResult | None` | Lazy — opens the SQLite file on first access. |
| `result.csv` | `CSVResult | None` | Lazy. |
| `result.html` | `HTMLResult | None` | Lazy. |
| `result.variables` | `OutputVariableIndex | None` | Lazy — parses `.rdd`/`.mdd`. |
| `result.sql_path` / `.err_path` / `.eso_path` / `.csv_path` / `.html_path` / `.rdd_path` / `.mdd_path` | `Path | None` | Direct file paths. |
| `result.migration_report` | `MigrationReport | None` | Set if `auto_migrate=True`. |

All `None` returns mean "the file doesn't exist" — EnergyPlus may not produce CSV/HTML unless you asked for them in the IDF (`Output:Variable`, `Output:Table:SummaryReports`).

## Errors (always check first)

```python
errs = result.errors                       # ErrorReport
print(errs.summary())                      # human-readable rollup

if errs.has_severe():
    for msg in errs.severe():
        print(msg.severity, msg.text)

for warn in errs.warnings():
    print(warn.text)
```

`severe()` includes both `Severe` and `Fatal`. Always treat a non-empty `severe()` as a simulation failure even if EnergyPlus exited zero — many corrupt-output cases leave the file present but unreadable.

## Time series from SQLite

```python
ts = result.sql.get_timeseries(
    variable_name="Zone Mean Air Temperature",
    key_value="Office",                    # zone, surface, system name; "*" for environment vars
    frequency="Hourly",                    # optional filter
    environment=None,                      # None=all, "annual", or "sizing"
)
print(ts.units, len(ts.values))            # 'C' 8760
ts.timestamps                              # tuple[datetime, ...]
ts.values                                  # tuple[float, ...]

# Pandas (requires idfkit[dataframes])
df = ts.to_dataframe()
```

`get_timeseries` is case-insensitive on key value and raises `KeyError` if the variable isn't in the database (typically because you didn't add an `Output:Variable` for it in the IDF — see [Output variable discovery](#output-variable-discovery)).

Use `frequency` to disambiguate when the same variable is reported at multiple frequencies (e.g. `"Hourly"`, `"Daily"`, `"Monthly"`). Use `environment="annual"` to skip design-day data when both ran.

## Tabular reports

```python
# All rows of a single table
rows = result.sql.get_tabular_data(
    report_name="AnnualBuildingUtilityPerformanceSummary",
    table_name="End Uses",
)
for r in rows:
    print(r.row_name, r.column_name, r.value, r.units)

# Single value
total = result.sql.get_tabular_value(
    report_name="AnnualBuildingUtilityPerformanceSummary",
    table_name="End Uses",
    row_name="Total End Uses",
    column_name="Electricity",
)
```

`get_tabular_data` returns `list[TabularRow]`; there is no direct tabular-to-DataFrame helper. If you need a DataFrame, build one yourself: `pd.DataFrame([dataclasses.asdict(r) for r in rows])`. `SQLResult.to_dataframe` is for time-series variables only (see above).

To enumerate what's available:

```python
for r in result.sql.list_reports():
    print(r)
for v in result.sql.list_variables():
    print(v.name, v.key_value, v.reporting_frequency, v.units)
for e in result.sql.list_environments():
    print(e.environment_type, e.environment_name)
```

## Raw SQL

For ad-hoc queries SQLResult exposes the underlying connection:

```python
rows = result.sql.query(
    "SELECT KeyValue, AVG(Value) FROM ReportData "
    "JOIN ReportDataDictionary USING(ReportDataDictionaryIndex) "
    "JOIN Time USING(TimeIndex) "
    "WHERE Name = ? AND COALESCE(WarmupFlag, 0) = 0 "
    "GROUP BY KeyValue",
    ("Zone Mean Air Temperature",),
)
```

The EnergyPlus SQLite schema is documented at [bigladdersoftware.com/epx/docs/](https://bigladdersoftware.com/epx/docs/) (the SQL Output sections).

## CSV (if `readvars=True`)

```python
# Only available if you called simulate(..., readvars=True) or added Output:VariableDictionary
csv = result.csv
if csv:
    df = csv.to_dataframe()                # full file, requires idfkit[dataframes]
    col = csv.get_column("ELECTRICITY:FACILITY [J](Hourly)")
    print(col.units, max(col.values))
```

Prefer SQL — CSV is one shot per `Output:Variable`, while SQL is queryable.

## HTML tabular

```python
html = result.html
if html:
    for table in html.tables:
        print(table.report_name, table.table_name)
```

The HTML parser is mostly useful for surfacing reports that aren't in SQLite (rare in modern EnergyPlus).

## Output variable discovery

If you want to know what variables you *could* report before adding `Output:Variable` objects, parse the RDD/MDD files. These list every variable EnergyPlus knows how to emit for the current model:

```python
idx = result.variables
if idx:
    for v in idx.variables:
        if "Cooling" in v.name:
            print(v.name, v.key_value, v.reporting_frequency)
    for m in idx.meters:
        print(m.name)
```

To produce RDD/MDD, the IDF needs `Output:VariableDictionary, IDF;` (or `regular`). The `idfkit.simulation.prep_outputs` helper adds it for you:

```python
from idfkit.simulation import prep_outputs
prep_outputs(doc)                           # adds Output:VariableDictionary (and Output:SQLite)
result = simulate(doc, "weather.epw")
```

## Reconstructing a result from a directory

If you've simulated outside Python (or cached the outputs), rebuild a `SimulationResult` from the run directory:

```python
from idfkit.simulation import SimulationResult

result = SimulationResult.from_directory("/path/to/run", output_prefix="eplus")
```

## Plotting helpers

```python
from idfkit.simulation.plotting import (
    plot_temperature_profile,
    plot_energy_balance,
    plot_comfort_hours,
)

plot_temperature_profile(result.sql, zones=["Office"])
plot_energy_balance(result.sql)
plot_comfort_hours(result.sql, zones=["Office"])
```

Backends: matplotlib (default, requires `idfkit[plot]`) and plotly (requires `idfkit[plotly]`). Pick with `get_default_backend(...)` or pass `backend=` explicitly.

## Common mistakes

**BAD — accessing `result.sql` without a None check**

```python
df = result.sql.to_dataframe("Zone Mean Air Temperature", "Office")
# AttributeError if SQL output was disabled
```

**GOOD — check or trust the runner's auto-injection**

```python
# simulate() injects Output:SQLite if missing — result.sql is almost always present.
# But guard anyway when reading legacy results from disk:
if result.sql:
    df = result.sql.to_dataframe("Zone Mean Air Temperature", "Office")
```

**BAD — assuming a variable exists**

```python
ts = result.sql.get_timeseries("Zone Cooling Set Point Not Met Time", "Office")
# KeyError if you didn't add Output:Variable for it
```

**GOOD — add the output, or discover what's available**

```python
doc.add("Output:Variable", key_value="*",
        variable_name="Zone Cooling Set Point Not Met Time",
        reporting_frequency="Hourly")
# Or check result.variables (after running with Output:VariableDictionary)
```

**BAD — ignoring `result.errors.has_severe()`**

```python
df = result.sql.to_dataframe("Zone Mean Air Temperature", "Office")
# Garbage data — EnergyPlus terminated mid-simulation, SQLite was never finalised.
```

**GOOD — gate on errors**

```python
if result.errors.has_severe():
    raise SystemExit(result.errors.summary())
df = result.sql.to_dataframe("Zone Mean Air Temperature", "Office")
```

## Related

- [simulation-execution.md](simulation-execution.md) — running simulations that produce these results.
- API docs: [py.idfkit.com/simulation/parsers/](https://py.idfkit.com/simulation/parsers/)
