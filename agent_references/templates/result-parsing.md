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
--8<-- "agent_references/snippets/result-parsing.py:quickstart"
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
--8<-- "agent_references/snippets/result-parsing.py:errors"
```

`severe()` includes both `Severe` and `Fatal`. Always treat a non-empty `severe()` as a simulation failure even if EnergyPlus exited zero — many corrupt-output cases leave the file present but unreadable.

## Time series from SQLite

```python
--8<-- "agent_references/snippets/result-parsing.py:timeseries"
```

`get_timeseries` is case-insensitive on key value and raises `KeyError` if the variable isn't in the database (typically because you didn't add an `Output:Variable` for it in the IDF — see [Output variable discovery](#output-variable-discovery)).

Use `frequency` to disambiguate when the same variable is reported at multiple frequencies (e.g. `"Hourly"`, `"Daily"`, `"Monthly"`). Use `environment="annual"` to skip design-day data when both ran.

## Tabular reports

```python
--8<-- "agent_references/snippets/result-parsing.py:tabular"
```

`get_tabular_data` returns `list[TabularRow]`; there is no direct tabular-to-DataFrame helper. If you need a DataFrame, build one yourself: `pd.DataFrame([dataclasses.asdict(r) for r in rows])`. `SQLResult.to_dataframe` is for time-series variables only (see above).

To enumerate what's available:

```python
--8<-- "agent_references/snippets/result-parsing.py:enumerate"
```

## Raw SQL

For ad-hoc queries SQLResult exposes the underlying connection:

```python
--8<-- "agent_references/snippets/result-parsing.py:raw-sql"
```

The EnergyPlus SQLite schema is documented at [bigladdersoftware.com/epx/docs/](https://bigladdersoftware.com/epx/docs/) (the SQL Output sections).

## SQL readers

Four typed readers over SQLite tables that `get_tabular_data` and `get_timeseries` don't cover:

```python
--8<-- "agent_references/snippets/result-parsing.py:sql-readers"
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
--8<-- "agent_references/snippets/result-parsing.py:link-build"
```

**Staleness.** The index belongs to one run. Build it right after the run, before editing — linking reads the document's names as they are now. After any edit, `index.is_fresh(doc)` is `False` (it compares `doc.revision`, plus the model text hash when you pass `model_hash=`); re-run and rebuild rather than reading old facts as if they described the new model.

```python
--8<-- "agent_references/snippets/result-parsing.py:link-fresh"
```

### One object: `for_object`

`for_object(ObjectKey(type, name))` returns `ObjectResults` (all fields empty when the run reported nothing). Fluid nodes use `ObjectKey("Node", name)`.

```python
--8<-- "agent_references/snippets/result-parsing.py:link-object"
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
--8<-- "agent_references/snippets/result-parsing.py:link-rank"
```

### Zone multipliers

A zone fact is **per zone instance**; `fact.multiplier` is the `Zone` multiplier times its `ZoneList` multiplier. **Never sum zone facts without applying it.** Also filter on `where`: the same value can appear in more than one report (Zone Summary and Space Summary both carry area).

```python
--8<-- "agent_references/snippets/result-parsing.py:link-multiplier"
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
--8<-- "agent_references/snippets/result-parsing.py:link-coverage"
```

### Message catalogue

`index.messages` are classified by a catalogue of common EnergyPlus messages; `kind` is a stable dotted id, or `"other"`. Classify any text yourself with `classify_message`; `MESSAGE_KINDS` lists every `MessageKind` (`kind`, `pattern`, `hint`, `inspect`, `symptoms`).

```python
--8<-- "agent_references/snippets/result-parsing.py:message-catalogue"
```

## CSV (if `readvars=True`)

```python
--8<-- "agent_references/snippets/result-parsing.py:csv"
```

Prefer SQL — CSV is one shot per `Output:Variable`, while SQL is queryable.

## HTML tabular

```python
--8<-- "agent_references/snippets/result-parsing.py:html"
```

The HTML parser is mostly useful for surfacing reports that aren't in SQLite (rare in modern EnergyPlus).

## ESO / MTR time series

The `.eso` (Standard Output) and `.mtr` (Meter) files are EnergyPlus's native time-series format. `result.eso` and `result.mtr` return an `ESOResult` parsed by the same reader. Prefer SQLite when it's available; use ESO when it isn't, or to pull a handful of variables out of a very large file cheaply.

```python
--8<-- "agent_references/snippets/result-parsing.py:eso"
```

The reader is **lazy by design**: constructing it parses only the data dictionary, and `get_column(name, key)` runs a single byte-level scan that float-parses only the requested variable — so reading one variable from a large `.eso` doesn't pay to parse the whole file. Accessing `.columns` (or `from_file(..., eager=True)`) materializes every variable in one pass. `ESOColumn` exposes `.values`, `.timestamps`, and `.variable` (an `ESOVariable` with `.variable_name`/`.key_value`/`.units`/`.frequency`); timestamps use the reference year 2017, like the SQL reader. ESO carries no calendar year, so only the year differs from SQL — values and month/day/hour match exactly.

**Selecting an environment.** A file holds several environments — the sizing design days, then the weather run period. `get_column` returns the **last** one (the run period) by default. To target a specific design day, read `result.eso.environments` (a tuple of `ESOEnvironment`) and match `environment_index` to its `title` — EnergyPlus encodes no environment *type* in the ESO format, so the title (`"... ANN HTG 99% CONDNS DB"`, `"RUN PERIOD 1"`, …) is the discriminator. Each `ESOColumn.environment_index` cross-references back into `result.eso.environments`.

## Output variable discovery

If you want to know what variables you *could* report before adding `Output:Variable` objects, parse the RDD/MDD files. These list every variable EnergyPlus knows how to emit for the current model:

```python
--8<-- "agent_references/snippets/result-parsing.py:output-discovery"
```

To produce RDD/MDD, the IDF needs `Output:VariableDictionary, IDF;` (or `regular`). The `idfkit.simulation.prep_outputs` helper adds it for you:

```python
--8<-- "agent_references/snippets/result-parsing.py:prep-outputs"
```

## Reconstructing a result from a directory

If you've simulated outside Python (or cached the outputs), rebuild a `SimulationResult` from the run directory:

```python
--8<-- "agent_references/snippets/result-parsing.py:from-directory"
```

## Releasing file handles (`close` / context manager)

`result.sql` opens a SQLite connection on first access and caches it. That connection holds an OS-level lock on `eplus.sql`. On **Windows**, the lock blocks deleting the run directory — `shutil.rmtree` / `TemporaryDirectory` cleanup fails with `PermissionError [WinError 32]: the process cannot access the file because it is being used by another process`. POSIX doesn't lock on open, so this only bites Windows users.

Close the result — or use it as a context manager — before the run directory is removed:

```python
--8<-- "agent_references/snippets/result-parsing.py:closing"
```

`close()` is idempotent and resets the cached connection, so touching `result.sql` afterwards transparently reopens it. The other accessors (`errors`, `csv`, `eso`, `html`, `variables`) read their files eagerly and hold no handles, so they need no cleanup.

## Plotting helpers

```python
--8<-- "agent_references/snippets/result-parsing.py:plotting"
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
    --8<-- "agent_references/snippets/result-parsing.py:mistake-sql-good"
    ```

!!! failure "assuming a variable exists"

    ```python
    ts = result.sql.get_timeseries("Zone Cooling Set Point Not Met Time", "Office")
    # KeyError if you didn't add Output:Variable for it
    ```

!!! success "add the output, or discover what's available"

    ```python
    --8<-- "agent_references/snippets/result-parsing.py:mistake-variable-good"
    ```

!!! failure "ignoring `result.errors.has_severe()`"

    ```python
    df = result.sql.to_dataframe("Zone Mean Air Temperature", "Office")
    # Garbage data — EnergyPlus terminated mid-simulation, SQLite was never finalised.
    ```

!!! success "gate on errors"

    ```python
    --8<-- "agent_references/snippets/result-parsing.py:mistake-errors-good"
    ```

!!! failure "summing zone facts without the multiplier"

    ```python
    total = sum(f.value for z in doc["Zone"] for f in index.for_object(ObjectKey("Zone", z.name)).facts
                if f.metric == "area_m2")
    # Undercounts every multiplied zone (and double-counts values reported in two tables)
    ```

!!! success "apply `fact.multiplier` and pick one report via `where`"

    ```python
    --8<-- "agent_references/snippets/result-parsing.py:link-multiplier"
    ```

## Related

- [simulation-execution.md](simulation-execution.md) — running simulations that produce these results.
- [hvac-topology.md](hvac-topology.md) / [model-graph.md](model-graph.md) — the connections `ObjectResults.neighbours` walks.
- API docs: [py.idfkit.com/simulation/parsers/](https://py.idfkit.com/simulation/parsers/)
