from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult, simulate

doc: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]

# --8<-- [start:quickstart]
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
# --8<-- [end:quickstart]


# --8<-- [start:errors]
errs = result.errors  # ErrorReport
print(errs.summary())  # human-readable rollup

if errs.has_severe:  # property, not method
    for msg in errs.severe:  # tuple[ErrorMessage, ...]
        print(msg.severity, msg.message)

for warn in errs.warnings:
    print(warn.message)
# --8<-- [end:errors]


# --8<-- [start:timeseries]
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
# --8<-- [end:timeseries]


# --8<-- [start:tabular]
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
# --8<-- [end:tabular]


# --8<-- [start:enumerate]
for r in result.sql.list_reports():
    print(r)
for v in result.sql.list_variables():
    print(v.name, v.key_value, v.frequency, v.units)
for e in result.sql.list_environments():
    print(e.environment_type, e.name)
# --8<-- [end:enumerate]


# --8<-- [start:raw-sql]
rows = result.sql.query(
    "SELECT KeyValue, AVG(Value) FROM ReportData "
    "JOIN ReportDataDictionary USING(ReportDataDictionaryIndex) "
    "JOIN Time USING(TimeIndex) "
    "WHERE Name = ? AND COALESCE(WarmupFlag, 0) = 0 "
    "GROUP BY KeyValue",
    ("Zone Mean Air Temperature",),
)
# --8<-- [end:raw-sql]


# --8<-- [start:csv]
# Only available if you called simulate(..., readvars=True)
csv = result.csv
if csv:
    csv.timestamps  # tuple[str, ...]
    for col in csv.columns:  # each CSVColumn has parsed metadata
        print(col.variable_name, col.key_value, col.units)
    col = csv.get_column("Electricity:Facility")  # by variable name, optional key_value=
    if col:
        print(col.units, max(col.values))
# --8<-- [end:csv]


# --8<-- [start:html]
html = result.html
if html:
    for table in html.tables:
        print(table.report_name, table.title)
# --8<-- [end:html]


# --8<-- [start:eso]
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
# --8<-- [end:eso]


# --8<-- [start:output-discovery]
idx = result.variables
if idx:
    for v in idx.variables:
        if "Cooling" in v.name:
            print(v.name, v.key, v.frequency)
    for m in idx.meters:
        print(m.name)
# --8<-- [end:output-discovery]


# --8<-- [start:prep-outputs]
from idfkit.simulation import prep_outputs

prep_outputs(doc)  # adds Output:VariableDictionary (and Output:SQLite)
result = simulate(doc, "weather.epw")
# --8<-- [end:prep-outputs]


# --8<-- [start:from-directory]
from idfkit.simulation import SimulationResult

result = SimulationResult.from_directory("/path/to/run", output_prefix="eplus")
# --8<-- [end:from-directory]


# --8<-- [start:closing]
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
# --8<-- [end:closing]


# --8<-- [start:plotting]
from idfkit.simulation.plotting import (
    plot_temperature_profile,
    plot_energy_balance,
    plot_comfort_hours,
)

if result.sql:
    plot_temperature_profile(result.sql, zones=["Office"])
    plot_energy_balance(result.sql)
    plot_comfort_hours(result.sql, zones=["Office"])
# --8<-- [end:plotting]


# --8<-- [start:mistake-sql-good]
# simulate() injects Output:SQLite if missing — result.sql is almost always present.
# But guard anyway when reading legacy results from disk:
if result.sql:
    df = result.sql.to_dataframe("Zone Mean Air Temperature", "Office")
# --8<-- [end:mistake-sql-good]


# --8<-- [start:mistake-variable-good]
doc.add(
    "Output:Variable", key_value="*", variable_name="Zone Cooling Set Point Not Met Time", reporting_frequency="Hourly"
)
# Or check result.variables (after running with Output:VariableDictionary)
# --8<-- [end:mistake-variable-good]


# --8<-- [start:mistake-errors-good]
if result.errors.has_severe:
    raise SystemExit(result.errors.summary())
df = result.sql.to_dataframe("Zone Mean Air Temperature", "Office")
# --8<-- [end:mistake-errors-good]
