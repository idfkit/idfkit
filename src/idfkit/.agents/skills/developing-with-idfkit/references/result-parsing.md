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

# 1. Always check errors first: raise SimulationError if EnergyPlus failed
result.raise_for_status()
if result.errors.has_severe:  # a run can succeed with severe errors; read them
    print(result.errors.summary())

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
| `result.sql` | `SQLResult` | Lazy — opens the SQLite file on first access. |
| `result.csv` | `CSVResult` | Lazy. |
| `result.eso` / `result.mtr` | `ESOResult` | Lazy — dictionary parsed on access, variable data on `get_column`. |
| `result.html` | `HTMLResult` | Lazy. |
| `result.variables` | `OutputVariableIndex` | Lazy — parses `.rdd`/`.mdd`. |
| `result.sql_path` / `.err_path` / `.eso_path` / `.mtr_path` / `.csv_path` / `.html_path` / `.rdd_path` / `.mdd_path` | `Path | None` | Direct file paths. |
| `result.migration_report` | `MigrationReport | None` | Set if `auto_migrate=True`. |

The parsed accessors (and their `async_*` counterparts) never return `None`. When the file doesn't exist they raise `OutputNotFoundError` (a `FileNotFoundError`), whose message names the output object to add (`Output:SQLite`, `Output:VariableDictionary`, `readvars=True` for CSV, ...) or, for a failed run, points to `raise_for_status()` and the `.err` file. To test for a file without raising, check its path: `result.csv_path is None`. EnergyPlus may not produce CSV/HTML unless you asked for them in the IDF (`Output:Variable`, `Output:Table:SummaryReports`).

## Errors (always check first)

```python
errs = result.errors  # ErrorReport
print(errs.summary())  # counts, then the fatal and first 3 severe messages
print(errs.summary(max_messages=10))  # quote more severe messages

if errs.has_severe:  # property, not method
    for msg in errs.severe:  # tuple[ErrorMessage, ...]
        print(msg.severity, msg.message)

for warn in errs.warnings:
    print(warn.message)
```

`simulate()` does not raise when EnergyPlus fails: the result has `success=False`, and `result.sql` may still open a partial database. `result.raise_for_status()` raises `SimulationError` for a failed run (the fatal and first severe messages and the `.err` path in its message, the result in `.result`) and returns the result otherwise; `await result.async_raise_for_status()` for an `async_fs` result. `errs.severe` and `errs.fatal` are separate tuples (properties, not methods). Treat a non-empty `errs.severe` as suspect even if EnergyPlus exited zero — many corrupt-output cases leave the file present but unreadable.

## Time series from SQLite

```python
ts = result.sql.get_timeseries(
    variable_name="Zone Mean Air Temperature",
    key_value="Office",  # zone, surface, system name; "*" (default) only if one key is reported
    frequency="Hourly",  # optional filter
    environment=None,  # None = run period (design days only if no run period), "annual", "sizing", "all"
)
print(ts.units, len(ts.values))  # 'C' 8760
ts.timestamps  # tuple[datetime, ...]
ts.values  # tuple[float, ...]

# Pandas (requires idfkit[dataframes])
df = ts.to_dataframe()

# Several series: ONE scan of ReportData instead of one per get_timeseries call.
# Each item is a VariableInfo, a name, (name, key) or (name, key, frequency).
zone_temps = result.sql.get_timeseries_many([
    v for v in result.sql.list_variables() if v.name == "Zone Mean Air Temperature"
])
oat, office = result.sql.get_timeseries_many([
    "Site Outdoor Air Drybulb Temperature",
    ("Zone Mean Air Temperature", "Office", "Hourly"),
])
```

`get_timeseries` matches the variable name, key value and frequency case-insensitively. It must resolve to exactly one reported series, so the default `key_value="*"` works only for a variable reported for a single key (site `Environment` variables, a meter): for a per-zone variable it raises, listing the keys, rather than returning one zone at random. Pass `frequency` when the variable is reported at several (e.g. `"Hourly"` and `"Monthly"`); the error lists them. By default (`environment=None`) it reads the weather-file run period, falling back to the design days only when the run has no run period, so an annual run never mixes 48 design-day hours into its 8760. Pass `"sizing"` for the design days or `"all"` for both in run order; asking for an environment the variable has no data in raises `ResultLookupError`.

EnergyPlus does not index `ReportData` by variable, so every `get_timeseries` call scans the whole table (over a million rows for a one-zone annual run, much more for a large model). To read more than one or two series, use `sql.get_timeseries_many(series, environment=None)`: it resolves each item as `get_timeseries` would and reads them all in one scan, returning the results in order. `eso.get_columns(series, environment_index=None)` does the same for `.eso`/`.mtr` files.

Printing a series is safe: the repr of a `TimeSeriesResult` (and of an `ESOColumn`, `CSVColumn` or `CSVResult`) is a one-line summary, e.g. `TimeSeriesResult('Zone Air Temperature', 'SPACE1-1', units='C', frequency='Hourly', 8760 points, 2017-01-01 01:00 .. 2018-01-01 00:00, min 12.1, max 26.3)`. Read `.timestamps` and `.values` for the data.

Every lookup failure raises `ResultLookupError`, a `KeyError` subclass whose message names the closest variable, key or report spelling ("Did you mean ...?") and the keys reported. A variable missing from the database usually means you didn't add an `Output:Variable` for it in the IDF — see [Output variable discovery](#output-variable-discovery). `get_tabular_value` and `get_tabular_data` raise it too, naming the first of report, `report_for`, table, row and column that matches nothing (`get_tabular_data` called with no filter returns every row instead). When the database holds no tabular report at all, the message says so: EnergyPlus writes them only for a model with `Output:Table:SummaryReports` (`doc.add("Output:Table:SummaryReports", reports=[{"report_name": "AllSummary"}])`, or `prep_outputs(doc)`), and `list_reports()` is then `[]`. `get_timeseries` also raises it when EnergyPlus simulated no environment at all (`sql.list_environments() == []`), rather than returning an empty series.

```python
from idfkit.exceptions import ResultLookupError

try:
    ts = result.sql.get_timeseries("Zone Air Temperature")  # reported for every zone
except ResultLookupError as e:
    print(e)  # ... is reported for 6 keys (PLENUM-1, SPACE1-1, ...); pass key_value= to pick one.
    print(e.available)  # ('PLENUM-1', 'SPACE1-1', ...): the keys you can pass
ts = result.sql.get_timeseries("zone air temperature", "space1-1")  # case-insensitive
```

## Tabular reports

```python
# All rows of a single table
rows = result.sql.get_tabular_data(
    report_name="AnnualBuildingUtilityPerformanceSummary",
    table_name="End Uses",
)
for r in rows:
    print(r.row_name, r.column_name, r.value, r.units)  # value: str, padding stripped

# Single cell as text ("12.50") or as a number (12.5)
text = result.sql.get_tabular_value(
    report_name="AnnualBuildingUtilityPerformanceSummary",
    table_name="End Uses",
    row_name="Total End Uses",
    column_name="Electricity",
)
total: float = result.sql.get_tabular_float(
    report_name="AnnualBuildingUtilityPerformanceSummary",
    table_name="End Uses",
    row_name="Total End Uses",
    column_name="Electricity",
)

# A row's number; as_float() raises ValueError, naming the cell, for a text cell
electricity = {r.row_name: r.as_float() for r in rows if r.column_name == "Electricity"}
```

Cell values are typed `str`, with the whitespace EnergyPlus pads them with stripped. For a number use `TabularRow.as_float()` or `get_tabular_float(...)` (same arguments as `get_tabular_value`), not `float(...)` by hand: both raise `ValueError` naming the cell and quoting its text when the cell is not numeric (a date, a zone name, or empty), and `get_tabular_float` raises `ResultLookupError` for a lookup that matches no row or several, as `get_tabular_value` does.

`get_tabular_data` returns `list[TabularRow]`; there is no direct tabular-to-DataFrame helper. If you need a DataFrame, build one yourself: `pd.DataFrame([dataclasses.asdict(r) for r in rows])`. `SQLResult.to_dataframe` is for time-series variables only (see above).

To enumerate what's available:

```python
for r in result.sql.list_reports():
    print(r)
for v in result.sql.list_variables():
    print(v.name, v.key_value, v.frequency, v.units)  # a meter's key_value is ""
    # Each entry can be passed straight back:
    series = result.sql.get_timeseries(v.name, key_value=v.key_value, frequency=v.frequency)
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
if result.csv_path is not None:  # result.csv raises OutputNotFoundError when there is no .csv
    csv = result.csv
    csv.timestamps  # tuple[str, ...]
    for col in csv.columns:  # each CSVColumn has parsed metadata
        print(col.variable_name, col.key_value, col.units)
    # One column per lookup: key_value= / frequency= are required when the variable is
    # reported for several keys or frequencies; a typo raises ResultLookupError (a KeyError).
    col = csv.get_column("Electricity:Facility")  # a meter, by its full name; it has no key
    # values span EVERY environment (design days, then run period): the CSV has no
    # environment markers. For the run period alone, use result.sql.get_timeseries(...)
    # or result.eso.get_column(..., environment_index=...).
    print(col.units, col.frequency, len(col.values))
```

Prefer SQL — CSV is one shot per `Output:Variable`, while SQL is queryable.

**A CSV series spans every environment.** The CSV file carries no environment markers, so `get_column` returns the sizing design days *and* the run period joined end to end, in run order, and there is no argument to pick one. An annual sum, a peak, or a row-index-to-date mapping over `col.values` silently includes the design days. For a single environment, read `result.sql.get_timeseries(...)` (the run period by default; `environment="sizing"` for the design days) or `result.eso.get_column(..., environment_index=...)` (the last environment, normally the run period, by default).

## HTML tabular

```python
if result.html_path is not None:
    html = result.html
    for table in html.tables:
        print(table.report_name, table.title)
    # header is the column-header row; rows are the data rows below it.
    site = html.tablebyname("Site and Source Energy")
    if site:
        print(site.header)  # ['', 'Total Energy [GJ]', ...]
        print(site.to_dict()["Total Site Energy"]["Total Energy [GJ]"])
```

The HTML parser is mostly useful for surfacing reports that aren't in SQLite (rare in modern EnergyPlus). EnergyPlus writes column headers as `<td>`, so a table's first row becomes `header` and `rows` holds only data; `to_dict()` keys each row by its first cell.

## ESO / MTR time series

The `.eso` (Standard Output) and `.mtr` (Meter) files are EnergyPlus's native time-series format. `result.eso` and `result.mtr` return an `ESOResult` parsed by the same reader. Prefer SQLite when it's available; use ESO when it isn't, or to pull a handful of variables out of a very large file cheaply.

```python
# ESO time series — use when the model has no Output:SQLite, or to pull a few
# variables out of a large .eso fast. The reader parses the dictionary eagerly
# but the data lazily.
if result.eso_path is not None:
    eso = result.eso  # ESOResult
    # Lazy: a single scan that float-parses ONLY this variable. Like sql.get_timeseries,
    # it raises ResultLookupError (a KeyError) on a typo, with the closest names, and when
    # several keys or frequencies match: pass key_value= / frequency= then.
    col = eso.get_column("Zone Mean Air Temperature", "Office")
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
    env = eso.environments[design_day_col.environment_index]

    # Several variables in ONE scan (get_column scans the file once per call):
    temp, oat_col = eso.get_columns([("Zone Mean Air Temperature", "Office"), "Site Outdoor Air Drybulb Temperature"])

    # Eager full parse:
    all_columns = eso.columns  # tuple[ESOColumn, ...] — every variable

# Meter files (.mtr) use the same reader:
if result.mtr_path is not None:
    mtr = result.mtr
    meter = mtr.get_column("Electricity:Facility")  # meters have no key value
```

The reader is **lazy by design**: constructing it parses only the data dictionary, and `get_column(name, key)` runs a single byte-level scan that float-parses only the requested variable — so reading one variable from a large `.eso` doesn't pay to parse the whole file. Accessing `.columns` (or `from_file(..., eager=True)`) materializes every variable in one pass. `ESOColumn` exposes `.values`, `.timestamps`, and `.variable` (an `ESOVariable` with `.variable_name`/`.key_value`/`.units`/`.frequency`); timestamps use the reference year 2017, like the SQL reader. ESO carries no calendar year, so only the year differs from SQL — values and month/day/hour match exactly.

**Selecting an environment.** A file holds several environments — the sizing design days, then the weather run period. `get_column` returns the **last** one (the run period) by default. To target a specific design day, read `result.eso.environments` (a tuple of `ESOEnvironment`) and match `environment_index` to its `title` — EnergyPlus encodes no environment *type* in the ESO format, so the title (`"... ANN HTG 99% CONDNS DB"`, `"RUN PERIOD 1"`, …) is the discriminator. Each `ESOColumn.environment_index` cross-references back into `result.eso.environments`.

## Output variable discovery

If you want to know what variables you *could* report before adding `Output:Variable` objects, parse the RDD/MDD files. These list every variable EnergyPlus knows how to emit for the current model:

```python
if result.rdd_path is not None:  # written only with Output:VariableDictionary
    idx = result.variables
    for v in idx.variables:
        if "Cooling" in v.name:
            print(v.name, v.key, v.frequency)
    for m in idx.meters:
        print(m.name)
```

To produce RDD/MDD, the IDF needs `Output:VariableDictionary, IDF;` (or `regular`). The `idfkit.simulation.prep_outputs` helper adds it for you, together with `Output:SQLite` and an `Output:Table:SummaryReports` requesting `AllSummary`, so `result.sql` and `result.html` are populated too. It skips any of the three the model already has:

```python
from idfkit.simulation import prep_outputs

prep_outputs(doc)  # adds Output:SQLite, Output:Table:SummaryReports (AllSummary), Output:VariableDictionary
result = simulate(doc, "weather.epw")
```

## Reconstructing a result from a directory

If you've simulated outside Python (or cached the outputs), rebuild a `SimulationResult` from the run directory:

```python
from idfkit.simulation import SimulationResult

result = SimulationResult.from_directory("/path/to/run", output_prefix="eplus")

# A run made with simulate(..., output_suffix="L") names its outputs eplusout.err,
# eplustbl.htm, ...; pass the same style so those names are tried first and a
# stale file another style left in a reused directory is not read instead.
legacy = SimulationResult.from_directory("/path/to/run", output_prefix="eplus", output_suffix="L")
```

## Cleaning up (`cleanup` / `close` / context manager)

`simulate()` without an `output_dir` runs EnergyPlus in a new temporary directory, and nothing deletes it on its own: the accessors read their files from `run_dir` lazily. Use the result as a context manager, or call `result.cleanup()`, once you have read what you need:

```python
# Without output_dir, simulate() runs in a temp dir that only cleanup() deletes.
# The with block calls it on exit: it closes the SQLite connection first (so the
# Windows file lock cannot block the delete), then removes the temp run_dir.
with simulate(doc, "weather.epw") as result:
    temps = result.sql.get_timeseries("Zone Mean Air Temperature", "Office")
# result.run_dir is gone here; values already read (temps) stay usable.

# With your own output_dir, the same block only closes: the directory is never deleted.
with simulate(doc, "weather.epw", output_dir="runs/baseline") as result:
    temps = result.sql.get_timeseries("Zone Mean Air Temperature", "Office")

# Equivalent without a context manager:
result = simulate(doc, "weather.epw")
try:
    temps = result.sql.get_timeseries("Zone Mean Air Temperature", "Office")
finally:
    result.cleanup()  # idempotent; result.close() alone keeps the directory
```

`cleanup()` deletes `run_dir` only when idfkit created it (`result.owns_run_dir`); a caller's `output_dir`, a remote `fs=` directory and a cache entry are never touched. It first calls `close()`: `result.sql` holds an open SQLite connection, which on **Windows** locks `eplus.sql` and makes deleting the directory fail with `PermissionError [WinError 32]`. Both are idempotent. `close()` alone releases the connection and keeps the files; touching `result.sql` afterwards reopens it. The other accessors (`errors`, `csv`, `eso`, `html`, `variables`) read their files eagerly and hold no handles; an output not read before `cleanup()` can no longer be read. Async results support `async with` and `await result.async_cleanup()`.

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

`plot_energy_balance` sums each end use's energy columns only (the `Water` volume column is left out) and labels the axis with the report's unit: `GJ` for SI, `kBtu` for IP. A report mixing kWh and kBtu is converted to the unit most cells use. A database without that report (no `Output:Table:SummaryReports`, or `Output:SQLite` not `SimpleAndTabular`) raises `ResultLookupError` saying how to add it, rather than drawing an empty chart.

## Common mistakes

!!! failure "guarding a parsed output with a None check"

    ```python
    if result.sql:                             # never None: raises OutputNotFoundError when there is no .sql
        df = result.sql.to_dataframe("Zone Mean Air Temperature", "Office")
    ```

!!! success "trust the runner's auto-injection, or test the path"

    ```python
    # simulate() injects Output:SQLite, so result.sql is there for every run it made.
    # For a run read from disk, test the path; result.sql itself raises OutputNotFoundError,
    # naming the output object to add, when there is no .sql file.
    if result.sql_path is not None:
        df = result.sql.to_dataframe("Zone Mean Air Temperature", "Office")
    ```

!!! failure "assuming a variable exists"

    ```python
    ts = result.sql.get_timeseries("Zone Cooling Set Point Not Met Time", "Office")
    # KeyError if you didn't add Output:Variable for it
    ```

!!! success "add the output, or discover what's available"

    ```python
    doc.output_variables.add(
        key_value="*", variable_name="Zone Cooling Set Point Not Met Time", reporting_frequency="Hourly"
    )
    # Or check result.variables (after running with Output:VariableDictionary)
    ```

!!! failure "ignoring a failed run"

    ```python
    df = result.sql.to_dataframe("Zone Mean Air Temperature", "Office")
    # Garbage data — EnergyPlus terminated mid-simulation, SQLite was never finalised.
    ```

!!! success "gate on errors"

    ```python
    result.raise_for_status()  # SimulationError naming the cause and the .err path
    if result.errors.has_severe:
        raise SystemExit(result.errors.summary())
    df = result.sql.to_dataframe("Zone Mean Air Temperature", "Office")
    ```

## Related

- [simulation-execution.md](simulation-execution.md) — running simulations that produce these results.
- API docs: [py.idfkit.com/simulation/parsers/](https://py.idfkit.com/simulation/parsers/)
