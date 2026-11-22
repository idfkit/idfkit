# Schedule evaluation

`idfkit.schedules` evaluates EnergyPlus schedules **without running a simulation**. Useful for visualisation, debugging, building parametric inputs, and any workflow where you need the value of a `Schedule:*` at a given timestamp.

## When to use

- You want to see what a `Schedule:Compact` resolves to at hour 14:00 on a Tuesday.
- You're plotting an annual schedule to confirm it matches expectations.
- You're synthesising schedules from a `numpy` array or a pandas `Series`.
- You're auditing a model to find every schedule it uses.

## Quick start

```python
--8<-- "agent_references/snippets/schedule-evaluation.py:quickstart"
```

## Core API

```python
--8<-- "agent_references/snippets/schedule-evaluation.py:core-api"
```

## Supported schedule types

The evaluator covers every standard EnergyPlus schedule type:

- `Schedule:Compact` (the most common)
- `Schedule:Year` + `Schedule:Week:Daily` / `Week:Compact` + `Schedule:Day:Hourly` / `Day:Interval` / `Day:List`
- `Schedule:Constant`
- `Schedule:File` (reads the CSV directly, with optional `FileSystem` for S3)
- `ScheduleTypeLimits` resolution

If you hit an unsupported type, `UnsupportedScheduleType` is raised.

A `Schedule:Compact` that EnergyPlus refuses as fatal raises `MalformedScheduleError` from `evaluate()` and `values()` at any timestamp, instead of being extended or filled: a `Through:` must reach `12/31` (later `Through:` periods are allowed and ignored), and every `For:` block must end at `Until: 24:00`. `compact_problems(sched)` (from `idfkit.schedules`) lists what is wrong without raising, and `validate_document` reports the same as `E011`. Day types a schedule leaves out (`For: Weekdays` alone) still evaluate to `0.0`: EnergyPlus only warns about them.

## Single-timestamp evaluation

```python
--8<-- "agent_references/snippets/schedule-evaluation.py:single-timestamp"
```

`day_type` accepts `"normal"`, `"summer"`, `"winter"`, `"holiday"` and an explicit `DayType` enum.

## Annual values

```python
--8<-- "agent_references/snippets/schedule-evaluation.py:annual-values"
```

`values(sched, timestep=n)` returns the doubles EnergyPlus reports as `Schedule Value` at `n` timesteps per hour, bit for bit; a test holds it to EnergyPlus's own output. Value `i` stands for the `i`-th timestep, and EnergyPlus builds it from the schedule's minutes:

| Interpolation | Timestep value |
|---|---|
| `No` (default) | the timestep's **last** minute, so an `Until: 12:30` at hourly timesteps already shows the new value for 12:00–13:00 |
| `Average` | the mean of the timestep's minutes |
| `Linear` | the ramp at the timestep's last minute; the first `Until:` interval stays flat |

- `Interpolate:` applies to its own `For:` block. A day schedule's `Interpolate to Timestep` wins over the `interpolation=` argument, which only fills a blank field.
- A `Schedule:Day:List` and a `Schedule:File` build no ramp: under `Linear` they step, as under `No`. An hourly `Schedule:File` gives every timestep its hour's row, even under `Average`.
- EnergyPlus 26.1 refuses `Interpolate: Yes` in a `Schedule:Compact`; idfkit reads it as `Average`, its meaning in older versions.
- `evaluate(sched, ts)` gives the value of the minute containing `ts`. Use `values()` with the model's `Timestep` to get what EnergyPlus reports.

By default `values` returns a `list[float]`. For pandas:

```python
--8<-- "agent_references/snippets/schedule-evaluation.py:to-series"
```

## Plotting

```python
--8<-- "agent_references/snippets/schedule-evaluation.py:plotting"
```

These pick the default backend (matplotlib if `idfkit[plot]` is installed, plotly if `idfkit[plotly]`). Pass `backend="plotly"` or `backend="matplotlib"` to force.

## Building schedules programmatically

```python
--8<-- "agent_references/snippets/schedule-evaluation.py:build-programmatically"
```

`create_compact_schedule_from_values` is a one-shot way to take an array and emit a `Schedule:Compact` object — useful when you have hourly inputs from measurement data.

## Auditing schedule usage

```python
--8<-- "agent_references/snippets/schedule-evaluation.py:audit"
```

## Schedule:File

`Schedule:File` reads CSV data from disk (or S3 if you provide a `FileSystem`):

```python
--8<-- "agent_references/snippets/schedule-evaluation.py:schedule-file"
```

For batch workflows reuse a `ScheduleFileCache` to avoid re-reading the same CSV:

```python
--8<-- "agent_references/snippets/schedule-evaluation.py:schedule-file-cache"
```

## Holidays and special days

```python
--8<-- "agent_references/snippets/schedule-evaluation.py:holidays"
```

Both functions read the document's `RunPeriodControl:SpecialDays` objects — idfkit does not bundle external holiday calendars. To use country-specific calendars, add the corresponding `SpecialDays` entries yourself (e.g. from the `holidays` PyPI package) before calling.

## Common mistakes

!!! failure "evaluating a schedule that references missing schedules"

    ```python
    # Compact schedule referencing "Building Occupancy" by name, but that schedule was deleted
    v = evaluate(sched, ts)                    # ScheduleReferenceError
    ```

!!! success "validate first"

    ```python
    --8<-- "agent_references/snippets/schedule-evaluation.py:mistake-broken-good"
    ```

!!! failure "previewing a schedule that does not cover the year"

    ```python
    # Through: 6/30 only, or a day ending at Until: 12:00: EnergyPlus stops on it
    v = evaluate(sched, ts)                    # MalformedScheduleError, not the last value carried on
    ```

!!! failure "assuming hourly when the schedule is sub-hourly"

    ```python
    arr = values(sched, year=2024)             # 8760 hourly values, even if EnergyPlus would interpolate at 15 minutes
    ```

!!! success "match the simulation timestep"

    ```python
    --8<-- "agent_references/snippets/schedule-evaluation.py:mistake-subhourly-good"
    ```

!!! failure "passing a date in a non-leap year for Feb 29"

    ```python
    v = evaluate(sched, datetime(2023, 2, 29, 10, 0))   # ValueError
    ```

!!! success "use a leap year or guard"

    ```python
    --8<-- "agent_references/snippets/schedule-evaluation.py:mistake-leap-good"
    ```

## Related

- [document-and-objects.md](document-and-objects.md) — `doc.add(Schedule:Compact, ...)` etc.
- [reference-tracking.md](reference-tracking.md) — finding what references a schedule.
- [result-parsing.md](result-parsing.md) — compare evaluated schedules against simulated `Schedule Value` outputs.
- API docs: [py.idfkit.com/schedules/](https://py.idfkit.com/schedules/)
