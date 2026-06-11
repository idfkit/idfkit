# Result parsing

`SimulationResult` is what `simulate(...)` returns. It's a thin container over the EnergyPlus output directory with typed accessors for the SQLite, CSV, ESO/MTR, HTML tabular, ERR, and RDD/MDD files. Use `result.sql` for almost everything — it's complete, queryable, and consistent across EnergyPlus versions. Reach for `result.eso` only when SQLite output wasn't produced, or when you want the fastest extraction of a few variables from a large `.eso`.

## When to use

- A simulation has completed and you want time series or tabular reports.
- You're aggregating results across a batch (peak loads, energy totals, comfort hours).
- You need to read the `.err` file to surface warnings/errors.
- You want available output variables before adding `Output:Variable` objects.

## Quick start

```python
result = simulate(doc, "weather.epw")

# 1. Always check errors first
if result.errors.has_severe:
    print(result.errors.summary())
    raise SystemExit

# 2. Time series
ts = result.sql.get_timeseries("Zone Mean Air Temperature", "Office", frequency="Hourly")
print(max(ts.values), ts.units)  # 27.3 'C'

# 3. Tabular reports (annual energy, sizing, …)
rows = result.sql.get_tabular_data(report_name="AnnualBuildingUtilityPerformanceSummary")
```

## What's on `SimulationResult`

| Accessor | Returns | Lazy? |
|---|---|---|
| `result.errors` | `ErrorReport` (always available) | Eager (parsed on construction). |
| `result.sql` | `SQLResult | None` | Lazy — opens the SQLite file on first access. |
| `result.csv` | `CSVResult | None` | Lazy. |
| `result.eso` / `result.mtr` | `ESOResult | None` | Lazy — dictionary parsed on access, variable data on `get_column`. |
| `result.html` | `HTMLResult | None` | Lazy. |
| `result.variables` | `OutputVariableIndex | None` | Lazy — parses `.rdd`/`.mdd`. |
| `result.sql_path` / `.err_path` / `.eso_path` / `.mtr_path` / `.csv_path` / `.html_path` / `.rdd_path` / `.mdd_path` | `Path | None` | Direct file paths. |
| `result.migration_report` | `MigrationReport | None` | Set if `auto_migrate=True`. |

All `None` returns mean "the file doesn't exist" — EnergyPlus may not produce CSV/HTML unless you asked for them in the IDF (`Output:Variable`, `Output:Table:SummaryReports`).

## Errors (always check first)

```python
errs = result.errors  # ErrorReport
print(errs.summary())  # human-readable rollup

if errs.has_severe:  # property, not method
    for msg in errs.severe:  # tuple[ErrorMessage, ...]
        print(msg.severity, msg.message)

for warn in errs.warnings:
    print(warn.message)
```

`severe()` includes both `Severe` and `Fatal`. Always treat a non-empty `severe()` as a simulation failure even if EnergyPlus exited zero — many corrupt-output cases leave the file present but unreadable.

## Time series from SQLite

```python
ts = result.sql.get_timeseries(
    variable_name="Zone Mean Air Temperature",
    key_value="Office",  # zone, surface, system name; "*" for environment vars
    frequency="Hourly",  # optional filter
    environment=None,  # None=all, "annual", or "sizing"
)
print(ts.units, len(ts.values))  # 'C' 8760
ts.timestamps  # tuple[datetime, ...]
ts.values  # tuple[float, ...]

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
    print(v.name, v.key_value, v.frequency, v.units)
for e in result.sql.list_environments():
    print(e.environment_type, e.name)
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
# Only available if you called simulate(..., readvars=True)
csv = result.csv
if csv:
    csv.timestamps  # tuple[str, ...]
    for col in csv.columns:  # each CSVColumn has parsed metadata
        print(col.variable_name, col.key_value, col.units)
    col = csv.get_column("Electricity:Facility")  # by variable name, optional key_value=
    if col:
        print(col.units, max(col.values))
```

Prefer SQL — CSV is one shot per `Output:Variable`, while SQL is queryable.

## HTML tabular

```python
html = result.html
if html:
    for table in html.tables:
        print(table.report_name, table.title)
```

The HTML parser is mostly useful for surfacing reports that aren't in SQLite (rare in modern EnergyPlus).

## ESO / MTR time series

The `.eso` (Standard Output) and `.mtr` (Meter) files are EnergyPlus's native time-series format. `result.eso` and `result.mtr` return an `ESOResult` parsed by the same reader. Prefer SQLite when it's available; use ESO when it isn't, or to pull a handful of variables out of a very large file cheaply.

```python
# ESO time series — use when the model has no Output:SQLite, or to pull a few
# variables out of a large .eso fast. The reader parses the dictionary eagerly
# but the data lazily.
eso = result.eso  # ESOResult | None
if eso:
    # Lazy: a single scan that float-parses ONLY this variable.
    col = eso.get_column("Zone Mean Air Temperature", "Office")
    if col:
        print(col.variable.units, len(col.values))  # 'C' 8760
        col.values  # tuple[float, ...]
        col.timestamps  # tuple[datetime, ...]
        df = col.to_dataframe()  # requires idfkit[dataframes]

    # A file has several environments: the design days, then the run period.
    # get_column returns the LAST one (the run period) by default. To pick a
    # specific design day, map index -> title via .environments:
    for env in eso.environments:
        print(env.index, env.title)  # 0 '... ANN HTG ...'  1 '... ANN CLG ...'  2 'RUN PERIOD 1'
    htg = next(e.index for e in eso.environments if "HTG" in e.title)
    design_day_col = eso.get_column("Zone Mean Air Temperature", "Office", environment_index=htg)
    # And back the other way — a column tells you its environment:
    if design_day_col:
        env = eso.environments[design_day_col.environment_index]

    # Eager full parse:
    all_columns = eso.columns  # tuple[ESOColumn, ...] — every variable

# Meter files (.mtr) use the same reader:
mtr = result.mtr
if mtr:
    meter = mtr.get_column("Electricity:Facility")  # meters have no key value
```

The reader is **lazy by design**: constructing it parses only the data dictionary, and `get_column(name, key)` runs a single byte-level scan that float-parses only the requested variable — so reading one variable from a large `.eso` doesn't pay to parse the whole file. Accessing `.columns` (or `from_file(..., eager=True)`) materializes every variable in one pass. `ESOColumn` exposes `.values`, `.timestamps`, and `.variable` (an `ESOVariable` with `.variable_name`/`.key_value`/`.units`/`.frequency`); timestamps use the reference year 2017, like the SQL reader. ESO carries no calendar year, so only the year differs from SQL — values and month/day/hour match exactly.

**Selecting an environment.** A file holds several environments — the sizing design days, then the weather run period. `get_column` returns the **last** one (the run period) by default. To target a specific design day, read `result.eso.environments` (a tuple of `ESOEnvironment`) and match `environment_index` to its `title` — EnergyPlus encodes no environment *type* in the ESO format, so the title (`"... ANN HTG 99% CONDNS DB"`, `"RUN PERIOD 1"`, …) is the discriminator. Each `ESOColumn.environment_index` cross-references back into `result.eso.environments`.

## Output variable discovery

If you want to know what variables you *could* report before adding `Output:Variable` objects, parse the RDD/MDD files. These list every variable EnergyPlus knows how to emit for the current model:

```python
idx = result.variables
if idx:
    for v in idx.variables:
        if "Cooling" in v.name:
            print(v.name, v.key, v.frequency)
    for m in idx.meters:
        print(m.name)
```

To produce RDD/MDD, the IDF needs `Output:VariableDictionary, IDF;` (or `regular`). The `idfkit.simulation.prep_outputs` helper adds it for you:

```python
from idfkit.simulation import prep_outputs

prep_outputs(doc)  # adds Output:VariableDictionary (and Output:SQLite)
result = simulate(doc, "weather.epw")
```

## Reconstructing a result from a directory

If you've simulated outside Python (or cached the outputs), rebuild a `SimulationResult` from the run directory:

```python
from idfkit.simulation import SimulationResult

result = SimulationResult.from_directory("/path/to/run", output_prefix="eplus")
```

## Releasing file handles (`close` / context manager)

`result.sql` opens a SQLite connection on first access and caches it. That connection holds an OS-level lock on `eplus.sql`. On **Windows**, the lock blocks deleting the run directory — `shutil.rmtree` / `TemporaryDirectory` cleanup fails with `PermissionError [WinError 32]: the process cannot access the file because it is being used by another process`. POSIX doesn't lock on open, so this only bites Windows users.

Close the result — or use it as a context manager — before the run directory is removed:

```python
import tempfile
from pathlib import Path

# result.sql opens a SQLite connection that holds an OS lock on eplus.sql.
# On Windows that lock blocks deletion of the run directory. Close the result
# (or use it as a context manager) before the directory is removed. The result
# context exits first — closing the connection — then TemporaryDirectory cleans
# up, so rmtree succeeds.
with tempfile.TemporaryDirectory() as tmp, simulate(doc, "weather.epw", output_dir=Path(tmp) / "run") as result:
    temps = result.sql.get_timeseries("Zone Mean Air Temperature", "Office")

# Equivalent without a context manager:
result = simulate(doc, "weather.epw")
try:
    temps = result.sql.get_timeseries("Zone Mean Air Temperature", "Office")
finally:
    result.close()  # idempotent; reopens lazily if you touch result.sql again
```

`close()` is idempotent and resets the cached connection, so touching `result.sql` afterwards transparently reopens it. The other accessors (`errors`, `csv`, `eso`, `html`, `variables`) read their files eagerly and hold no handles, so they need no cleanup.

## Plotting helpers

```python
from idfkit.simulation.plotting import (
    plot_temperature_profile,
    plot_energy_balance,
    plot_comfort_hours,
)

if result.sql:
    plot_temperature_profile(result.sql, zones=["Office"])
    plot_energy_balance(result.sql)
    plot_comfort_hours(result.sql, zones=["Office"])
```

Backends: matplotlib (default, requires `idfkit[plot]`) and plotly (requires `idfkit[plotly]`). Pick with `get_default_backend(...)` or pass `backend=` explicitly.

## Common mistakes

!!! failure "accessing `result.sql` without a None check"

    ```python
    df = result.sql.to_dataframe("Zone Mean Air Temperature", "Office")
    # AttributeError if SQL output was disabled
    ```

!!! success "check or trust the runner's auto-injection"

    ```python
    # simulate() injects Output:SQLite if missing — result.sql is almost always present.
    # But guard anyway when reading legacy results from disk:
    if result.sql:
        df = result.sql.to_dataframe("Zone Mean Air Temperature", "Office")
    ```

!!! failure "assuming a variable exists"

    ```python
    ts = result.sql.get_timeseries("Zone Cooling Set Point Not Met Time", "Office")
    # KeyError if you didn't add Output:Variable for it
    ```

!!! success "add the output, or discover what's available"

    ```python
    doc.add(
        "Output:Variable", key_value="*", variable_name="Zone Cooling Set Point Not Met Time", reporting_frequency="Hourly"
    )
    # Or check result.variables (after running with Output:VariableDictionary)
    ```

!!! failure "ignoring `result.errors.has_severe()`"

    ```python
    df = result.sql.to_dataframe("Zone Mean Air Temperature", "Office")
    # Garbage data — EnergyPlus terminated mid-simulation, SQLite was never finalised.
    ```

!!! success "gate on errors"

    ```python
    if result.errors.has_severe:
        raise SystemExit(result.errors.summary())
    df = result.sql.to_dataframe("Zone Mean Air Temperature", "Office")
    ```

## Related

- [simulation-execution.md](simulation-execution.md) — running simulations that produce these results.
- API docs: [py.idfkit.com/simulation/parsers/](https://py.idfkit.com/simulation/parsers/)
