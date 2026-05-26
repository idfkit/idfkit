# Result parsing

`SimulationResult` is what `simulate(...)` returns. It's a thin container over the EnergyPlus output directory with typed accessors for the SQLite, CSV, ESO/MTR, HTML tabular, ERR, and RDD/MDD files. Use `result.sql` for almost everything — it's complete, queryable, and consistent across EnergyPlus versions. Reach for `result.eso` only when SQLite output wasn't produced, or when you want the fastest extraction of a few variables from a large `.eso`.

## When to use

- A simulation has completed and you want time series or tabular reports.
- You're aggregating results across a batch (peak loads, energy totals, comfort hours).
- You need to read the `.err` file to surface warnings/errors.
- You want available output variables before adding `Output:Variable` objects.

## Quick start

```python
--8<-- "docs/snippets/agent_references/result-parsing.py:quickstart"
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
--8<-- "docs/snippets/agent_references/result-parsing.py:errors"
```

`severe()` includes both `Severe` and `Fatal`. Always treat a non-empty `severe()` as a simulation failure even if EnergyPlus exited zero — many corrupt-output cases leave the file present but unreadable.

## Time series from SQLite

```python
--8<-- "docs/snippets/agent_references/result-parsing.py:timeseries"
```

`get_timeseries` is case-insensitive on key value and raises `KeyError` if the variable isn't in the database (typically because you didn't add an `Output:Variable` for it in the IDF — see [Output variable discovery](#output-variable-discovery)).

Use `frequency` to disambiguate when the same variable is reported at multiple frequencies (e.g. `"Hourly"`, `"Daily"`, `"Monthly"`). Use `environment="annual"` to skip design-day data when both ran.

## Tabular reports

```python
--8<-- "docs/snippets/agent_references/result-parsing.py:tabular"
```

`get_tabular_data` returns `list[TabularRow]`; there is no direct tabular-to-DataFrame helper. If you need a DataFrame, build one yourself: `pd.DataFrame([dataclasses.asdict(r) for r in rows])`. `SQLResult.to_dataframe` is for time-series variables only (see above).

To enumerate what's available:

```python
--8<-- "docs/snippets/agent_references/result-parsing.py:enumerate"
```

## Raw SQL

For ad-hoc queries SQLResult exposes the underlying connection:

```python
--8<-- "docs/snippets/agent_references/result-parsing.py:raw-sql"
```

The EnergyPlus SQLite schema is documented at [bigladdersoftware.com/epx/docs/](https://bigladdersoftware.com/epx/docs/) (the SQL Output sections).

## CSV (if `readvars=True`)

```python
--8<-- "docs/snippets/agent_references/result-parsing.py:csv"
```

Prefer SQL — CSV is one shot per `Output:Variable`, while SQL is queryable.

## HTML tabular

```python
--8<-- "docs/snippets/agent_references/result-parsing.py:html"
```

The HTML parser is mostly useful for surfacing reports that aren't in SQLite (rare in modern EnergyPlus).

## ESO / MTR time series

The `.eso` (Standard Output) and `.mtr` (Meter) files are EnergyPlus's native time-series format. `result.eso` and `result.mtr` return an `ESOResult` parsed by the same reader. Prefer SQLite when it's available; use ESO when it isn't, or to pull a handful of variables out of a very large file cheaply.

```python
--8<-- "docs/snippets/agent_references/result-parsing.py:eso"
```

The reader is **lazy by design**: constructing it parses only the data dictionary, and `get_column(name, key)` runs a single byte-level scan that float-parses only the requested variable — so reading one variable from a large `.eso` doesn't pay to parse the whole file. `get_column` defaults to the last environment (the run period); pass `environment_index=` for a design day. Accessing `.columns` (or `from_file(..., eager=True)`) materializes every variable in one pass. `ESOColumn` exposes `.values`, `.timestamps`, and `.variable` (an `ESOVariable` with `.variable_name`/`.key_value`/`.units`/`.frequency`); timestamps use the reference year 2017, like the SQL reader. ESO carries no calendar year, so only the year differs from SQL — values and month/day/hour match exactly.

## Output variable discovery

If you want to know what variables you *could* report before adding `Output:Variable` objects, parse the RDD/MDD files. These list every variable EnergyPlus knows how to emit for the current model:

```python
--8<-- "docs/snippets/agent_references/result-parsing.py:output-discovery"
```

To produce RDD/MDD, the IDF needs `Output:VariableDictionary, IDF;` (or `regular`). The `idfkit.simulation.prep_outputs` helper adds it for you:

```python
--8<-- "docs/snippets/agent_references/result-parsing.py:prep-outputs"
```

## Reconstructing a result from a directory

If you've simulated outside Python (or cached the outputs), rebuild a `SimulationResult` from the run directory:

```python
--8<-- "docs/snippets/agent_references/result-parsing.py:from-directory"
```

## Plotting helpers

```python
--8<-- "docs/snippets/agent_references/result-parsing.py:plotting"
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
    --8<-- "docs/snippets/agent_references/result-parsing.py:mistake-sql-good"
    ```

!!! failure "assuming a variable exists"

    ```python
    ts = result.sql.get_timeseries("Zone Cooling Set Point Not Met Time", "Office")
    # KeyError if you didn't add Output:Variable for it
    ```

!!! success "add the output, or discover what's available"

    ```python
    --8<-- "docs/snippets/agent_references/result-parsing.py:mistake-variable-good"
    ```

!!! failure "ignoring `result.errors.has_severe()`"

    ```python
    df = result.sql.to_dataframe("Zone Mean Air Temperature", "Office")
    # Garbage data — EnergyPlus terminated mid-simulation, SQLite was never finalised.
    ```

!!! success "gate on errors"

    ```python
    --8<-- "docs/snippets/agent_references/result-parsing.py:mistake-errors-good"
    ```

## Related

- [simulation-execution.md](simulation-execution.md) — running simulations that produce these results.
- API docs: [py.idfkit.com/simulation/parsers/](https://py.idfkit.com/simulation/parsers/)
