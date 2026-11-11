# Result parsing

`SimulationResult` is what `simulate(...)` returns. It's a thin container over the EnergyPlus output directory with typed accessors for the SQLite, CSV, ESO/MTR, HTML tabular, ERR, and RDD/MDD files. Use `result.sql` for almost everything — it's complete, queryable, and consistent across EnergyPlus versions. Reach for `result.eso` only when SQLite output wasn't produced, or when you want the fastest extraction of a few variables from a large `.eso`.

## When to use

- A simulation has completed and you want time series or tabular reports.
- You're aggregating results across a batch (peak loads, energy totals, comfort hours).
- You need to read the `.err` file to surface warnings/errors.
- You want available output variables before adding `Output:Variable` objects.
- You want everything a run reported about one model object (sizing, report rows, warnings), or to rank objects by a sized value — see [Results linked to objects](#results-linked-to-objects).

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

## SQL readers

Four typed readers over SQLite tables that `get_tabular_data` and `get_timeseries` don't cover:

```python
sql = result.sql
if sql:
    # ComponentSizes: every autosized value. Type and name come back as EnergyPlus wrote them.
    for size in sql.component_sizes():
        print(size.component_type, size.component_name, size.description, size.value, size.units)
        # Chiller:Electric CENTRAL CHILLER Design Size Nominal Capacity 38762.4 W

    # Errors table: severity is "info" | "warning" | "severe" | "fatal"; count sums recurrences.
    for row in sql.errors():
        if row.severity in ("severe", "fatal"):
            print(row.severity, row.count, row.message)

    # Zones table, with the multipliers EnergyPlus applied.
    for zone in sql.zones():
        print(zone.name, zone.multiplier * zone.list_multiplier)  # 'MID CENTER ZONE' 32

    # Every reported variable and meter key, from ReportDataDictionary only: no values are read,
    # so the cost does not grow with the run length. Fetch values with get_timeseries.
    for key in sql.report_keys():
        print(key.name, key.key_value, key.frequency, key.units, key.is_meter)
```

| Method | Table | Returns |
|---|---|---|
| `component_sizes()` | `ComponentSizes` | `list[ComponentSize]`: `index`, `component_type`, `component_name` (upper case), `description`, `value` (`float \| None`), `units` |
| `errors()` | `Errors` | `list[SQLErrorRow]`: `severity` (`"info"`/`"warning"`/`"severe"`/`"fatal"`), `message` (with continuation lines), `count` |
| `zones()` | `Zones` | `list[ZoneRow]`: `index`, `name` (upper case), `multiplier`, `list_multiplier` |
| `report_keys()` | `ReportDataDictionary` | `list[VariableInfo]`: every variable and meter key. **Never reads `ReportData`**, so it is cheap on any run length |

## Results linked to objects

`ResultIndex.build(doc, result, *, run_revision, run_model_hash)` links a run's SQLite output to the objects of the document that was simulated: `ComponentSizes` rows, object rows of tabular reports, timeseries keys (names only — **`ReportData` values are never read**), and `Errors` messages. It needs `Output:SQLite` (raises `ValueError` without it).

```python
import hashlib

from idfkit import write_idf
from idfkit.simulation import ResultIndex

# Capture what was simulated BEFORE running: simulate() runs a copy, so doc.revision is unchanged.
run_revision = doc.revision
run_model_hash = hashlib.sha256(write_idf(doc).encode()).hexdigest()
result = simulate(doc, "weather.epw")  # needs Output:SQLite, which simulate() injects

# Build right after the run, before editing: linking reads the document's names as they are now.
index = ResultIndex.build(doc, result, run_revision=run_revision, run_model_hash=run_model_hash)
# Raises ValueError when the run has no SQLite output. A second call with the same run is cached.
```

**Staleness.** The index belongs to one run. Build it right after the run, before editing — linking reads the document's names as they are now. After any edit, `index.is_fresh(doc)` is `False` (it compares `doc.revision`, plus the model text hash when you pass `model_hash=`); re-run and rebuild rather than reading old facts as if they described the new model.

```python
doc["Zone"][0].multiplier = 2  # any edit moves doc.revision
if not index.is_fresh(doc):  # compares the revision (and model_hash when given)
    result = simulate(doc, "weather.epw")  # facts describe the OLD model: re-run, then rebuild
    index = ResultIndex.build(doc, result, run_revision=doc.revision, run_model_hash="")

# Stronger check, when you also hash the model text:
fresh = index.is_fresh(doc, model_hash=hashlib.sha256(write_idf(doc).encode()).hexdigest())
```

### One object: `for_object`

`for_object(ObjectKey(type, name))` returns `ObjectResults` (all fields empty when the run reported nothing). Fluid nodes use `ObjectKey("Node", name)`.

```python
from idfkit.simulation import ObjectKey

coil = index.for_object(ObjectKey("Coil:Heating:Water", "SPACE1-1 Zone Coil"))  # case-insensitive
coil.object  # ObjectKey in the model's spelling

for fact in coil.facts:  # sizing rows first, then object rows of tabular reports
    print(fact.source, fact.metric, fact.value, fact.units)  # sizing design_size_rated_capacity_w 4626.6 W
    print(fact.where)  # 'ComponentSizes#11' or 'EquipmentSummary/Heating Coils/SPACE1-1 ZONE COIL/...'

for msg in coil.messages:  # one per message kind, most severe first
    print(msg.severity, msg.kind, msg.occurrences, msg.first_seen, msg.text)

print(coil.available_variables)  # names of recorded output variables; values are NOT read
for neighbour in coil.neighbours:  # one hop over HVAC topology / references, at most 20
    print(neighbour.object, neighbour.top_fact)

# Fluid nodes are keyed by the pseudo-type "Node":
inlet = index.for_object(ObjectKey("Node", "SPACE1-1 Zone Coil Air In Node"))
```

| `ObjectResults` field | Holds |
|---|---|
| `facts` | `ResultFact`s: `source` (`"sizing"`/`"tabular"`/`"timeseries_stat"`), `metric` (snake case with units, e.g. `design_size_nominal_capacity_w`), `value`, `units`, `where` (`ComponentSizes#<i>` or `Report/Table/Row/Column`), `multiplier` (zones only) |
| `messages` | `LinkedMessage`s **deduplicated by kind**: `occurrences` summed, `first_seen` (`"<environment> MM/DD HH:MM"` or `None`), `severity`, `kind`, `text` (first line), `objects` |
| `available_variables` | Output variable names recorded for it; fetch values with `result.sql.get_timeseries` |
| `neighbours` | `ObjectNeighbour`s one hop away over HVAC topology and references (max 20), each with its `top_fact` |
| `coverage` | The index's `Coverage` (see below) |

### Ranking: `objects_with`

```python
# Largest values of one metric across the model, largest first. Metrics are snake-case with units.
for key, fact in index.objects_with("design_size_nominal_capacity_w", top=5):
    print(key.object_type, key.name, fact.value, fact.units, fact.where)
# Chiller:Electric Central Chiller 38762.4 W ComponentSizes#125
```

### Zone multipliers

A zone fact is **per zone instance**; `fact.multiplier` is the `Zone` multiplier times its `ZoneList` multiplier. **Never sum zone facts without applying it.** Also filter on `where`: the same value can appear in more than one report (Zone Summary and Space Summary both carry area).

```python
# Zone facts are per zone instance. fact.multiplier = Zone multiplier x ZoneList multiplier.
# Never sum zone facts without it: MultiStory.idf gives 216 m2 unscaled, 1440 m2 correctly.
floor_area = 0.0
for zone in doc["Zone"]:
    for fact in index.for_object(ObjectKey("Zone", zone.name)).facts:
        in_zone_summary = fact.where.startswith("InputVerificationandResultsSummary/Zone Summary/")
        if in_zone_summary and fact.metric == "area_m2" and isinstance(fact.value, float):
            floor_area += fact.value * (fact.multiplier or 1)
```

### Resolution, confidence and coverage

Every link is a `Resolution(key, rule, confidence, via)`. Rules run in order; the first that answers wins:

| Rule | Matches | Confidence |
|---|---|---|
| `exact` | the source names the type, and an object of that type has the name | `exact` |
| `typed` | known name; the variable/table/message context picks the type | `typed`; `convention` when a shared name falls back to the zone/loop or an `HVACTemplate:*`; `weak` when the context can't tell several types apart (the others are in `via`) |
| `zonelist_composite` | `"<ZONE> <OBJECT>"` — a load applied to every zone of a zone list; the zone is in `via` | `convention` (`weak` if the object type is ambiguous) |
| `space_to_zone` | `"<ZONE>_SPACE"` | `convention` |
| `mirrored_shading` | `"Mir-<SURFACE>"` | `convention` |
| `aggregate` | `Total`, `Total Facility`, `Whole Building`, … → `ObjectKey("Aggregate", raw)` | `convention` |
| `ideal_loads_suffix` | `"<ZONE> Ideal Loads Air System"` | `convention` |
| `ems_key` | the key of an `EnergyManagementSystem:OutputVariable` | `convention` |
| `substring` | longest known name inside the key | **always `weak`** |

Treat `weak` links as candidates to confirm, not facts. Nothing is dropped: items no rule answers are in `index.unresolved` as `(source, raw_key)`, and `index.coverage` counts `resolved`/`unresolved` and lists `uncovered` parts (`unlinked_result`, and `hvac_template` — objects expanded from `HVACTemplate:*` aren't in the model, so they link by convention or not at all).

```python
cov = index.coverage
print(cov.resolved, cov.unresolved, cov.partial)  # 678 0 False
for part in cov.uncovered:  # "unlinked_result", "hvac_template"
    print(part.kind, part.count, part.reason)
for source, raw in index.unresolved:  # never dropped: ("timeseries", "SOME KEY"), ("message", ...)
    print(source, raw)

# How each message link was made, and how far to trust it:
for message in index.messages:
    for link in message.objects:
        print(link.key, link.rule, link.confidence, link.via)
        # ObjectKey('AirLoopHVAC', 'VAV Sys 1') typed typed ()
        if link.confidence == "weak":  # substring match or ambiguous name: confirm before acting
            pass
```

### Message catalogue

`index.messages` are classified by a catalogue of common EnergyPlus messages; `kind` is a stable dotted id, or `"other"`. Classify any text yourself with `classify_message`; `MESSAGE_KINDS` lists every `MessageKind` (`kind`, `pattern`, `hint`, `inspect`, `symptoms`).

```python
from idfkit.simulation import MESSAGE_KINDS, classify_message

kind, named = classify_message('GetAirPathData: AirLoopHVAC="EVAP COOLER SYSTEM" has no Controllers.')
if kind:
    print(kind.kind)  # 'airloop.no_controllers'
    print(kind.hint)  # likely causes, one sentence
    print(kind.inspect)  # ('AirLoopHVAC:ControllerList', 'Controller:OutdoorAir', 'Controller:WaterCoil')
    print(kind.symptoms)  # () here; e.g. ('unmet_heating', 'unmet_cooling') for others
print(named)  # [('AirLoopHVAC', 'EVAP COOLER SYSTEM')] -- type is None when the message omits it

print([k.kind for k in MESSAGE_KINDS])  # 'sizing.zero_load', 'dxcoil.low_outlet_temp', ...
```

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

!!! failure "summing zone facts without the multiplier"

    ```python
    total = sum(f.value for z in doc["Zone"] for f in index.for_object(ObjectKey("Zone", z.name)).facts
                if f.metric == "area_m2")
    # Undercounts every multiplied zone (and double-counts values reported in two tables)
    ```

!!! success "apply `fact.multiplier` and pick one report via `where`"

    ```python
    # Zone facts are per zone instance. fact.multiplier = Zone multiplier x ZoneList multiplier.
    # Never sum zone facts without it: MultiStory.idf gives 216 m2 unscaled, 1440 m2 correctly.
    floor_area = 0.0
    for zone in doc["Zone"]:
        for fact in index.for_object(ObjectKey("Zone", zone.name)).facts:
            in_zone_summary = fact.where.startswith("InputVerificationandResultsSummary/Zone Summary/")
            if in_zone_summary and fact.metric == "area_m2" and isinstance(fact.value, float):
                floor_area += fact.value * (fact.multiplier or 1)
    ```

## Related

- [simulation-execution.md](simulation-execution.md) — running simulations that produce these results.
- [hvac-topology.md](hvac-topology.md) / [model-graph.md](model-graph.md) — the connections `ObjectResults.neighbours` walks.
- API docs: [py.idfkit.com/simulation/parsers/](https://py.idfkit.com/simulation/parsers/)
