# How the schedule evaluator works

idfkit can compute the value of any EnergyPlus schedule at any moment — or
across a whole year — **without running a simulation**. This page explains how
that evaluator is built and why it behaves the way it does. If you just want to
call it, see [How to evaluate schedules](../schedules/index.md); for the exact
signatures, see the [API reference](../api/schedules/index.md).

## Why evaluate schedules without simulating

EnergyPlus schedules encode when a building is occupied, when lights and
equipment run, and what setpoints apply. Answering "what is this schedule doing
at 2pm on a summer Tuesday?" normally means running a full simulation and
reading the output. That is slow, and it fails as a *preview*: you can't see the
profile you're building until after you've built and run the whole model.

The evaluator interprets schedule objects directly, in pure Python. Its design
goals shape everything below:

- **Stdlib only for the core.** Point evaluation and annual series need nothing
  beyond the standard library; pandas and matplotlib are optional conveniences.
- **Operates on the live model.** It reads `IDFObject` instances straight from
  an `IDFDocument`, so it sees exactly what you'll write out.
- **Matches EnergyPlus semantics.** The interesting design work is reproducing
  E+'s interpretation of schedule syntax faithfully — the rest of this page is
  mostly about those semantics.

## The schedule hierarchy

EnergyPlus schedules are layered. A `Schedule:Year` names date ranges, each
pointing at a `Schedule:Week:*`, which in turn names a `Schedule:Day:*` for each
kind of day. Evaluating a datetime means walking that hierarchy from the top:

```python
--8<-- "docs/snippets/design/schedule-evaluator/hierarchical_schedule_resolution.py:example"
```

Each level resolves a reference and hands the datetime down to the next. Because
idfkit already indexes every object by name, each lookup is O(1) — resolving a
year schedule for one instant is a handful of dictionary hits, not a scan.

## Reading the Compact DSL

`Schedule:Compact` collapses that whole hierarchy into one object using a
mini-DSL of `Through:` (date ranges), `For:` (day types), and `Until:`
(time/value pairs):

```
Schedule:Compact,
  Office Occupancy,        ! Name
  Fraction,                ! Schedule Type Limits
  Through: 12/31,          ! Date range (implicit start 1/1)
  For: Weekdays,           ! Day types
  Until: 08:00, 0.0,       ! Time, Value pairs
  Until: 18:00, 1.0,
  Until: 24:00, 0.0,
  For: Weekends Holidays,
  Until: 24:00, 0.0;
```

The parser turns those flat fields into structured periods and day rules, so
evaluation becomes "find the period containing the date, find the day rule
matching the day type, find the first `Until:` time at or after the moment":

```python
--8<-- "docs/snippets/design/schedule-evaluator/parsing_strategy.py:example"
```

## Matching day types to the calendar

Every level of the hierarchy ultimately asks: *what kind of day is this?* The
evaluator maps EnergyPlus day types onto Python's `datetime.weekday()`:

| E+ Day Type | Python `weekday()` |
|-------------|--------------------|
| Sunday | 6 |
| Monday | 0 |
| Tuesday | 1 |
| Wednesday | 2 |
| Thursday | 3 |
| Friday | 4 |
| Saturday | 5 |
| Weekdays | 0–4 |
| Weekends | 5–6 |
| AllDays | 0–6 |
| Holidays | (requires the holiday list) |
| SummerDesignDay | (special) |
| WinterDesignDay | (special) |
| AllOtherDays | (fallback) |

The special day types don't fall out of the calendar alone — they're why
holidays and design days each need their own handling, below.

## Evaluating a day schedule

At the bottom of the hierarchy, a day schedule gives values by hour or by
interval. `Schedule:Day:Hourly` is 24 explicit values, one per hour:

```python
--8<-- "docs/snippets/design/schedule-evaluator/scheduledayhourly.py:example"
```

`Schedule:Day:Interval` gives time/value pairs, where each value applies *until*
its stated time — a step function unless interpolation is requested:

```python
--8<-- "docs/snippets/design/schedule-evaluator/scheduledayinterval.py:example"
```

### Interpolation: step vs. average

EnergyPlus offers two ways to resolve a moment that falls between a schedule's
native intervals, and the evaluator reproduces both. With interpolation off (the
default), the schedule is a **step function** — the value at the start of an
interval holds until the next one:

```
Schedule interval: 0–15min = 0.0, 15–30min = 0.5
At 10min: 0.0
At 20min: 0.5
```

With **average** interpolation, values are blended linearly when the evaluation
timestep doesn't align with the interval boundaries:

```
Schedule interval: 0–15min = 0.0, 15–30min = 0.5
At 10min: 0.0
At 20min: 0.25   (average of 0.0 and 0.5)
```

Matching this exactly matters: an occupancy fraction previewed with the wrong
interpolation mode won't match what EnergyPlus actually simulates.

## Design decisions

A few behaviours don't follow mechanically from the schedule syntax and had to
be decided deliberately.

### Holidays

Holidays aren't in the schedule objects themselves — they come from
`RunPeriodControl:SpecialDays` in the document. The evaluator extracts them so
that a `For: Holidays` rule resolves against the model's actual holiday
calendar:

```python
--8<-- "docs/snippets/design/schedule-evaluator/1_holidays.py:example"
```

The same mechanism carries `CustomDay1` and `CustomDay2`, EnergyPlus's
user-defined special-day types.

### Design days

`SummerDesignDay` and `WinterDesignDay` never occur on the calendar — they're
sizing conditions. Rather than guess when they apply, the evaluator exposes them
through an explicit `day_type` override, so sizing previews are opt-in:

```python
--8<-- "docs/snippets/design/schedule-evaluator/2_design_days.py:example"
```

### Schedule:File

`Schedule:File` reads values from an external CSV. Reusing idfkit's
`FileSystem` protocol here means the same schedule works whether the CSV lives
on local disk or in remote storage, matching how the simulation module reads and
writes everything else:

```python
--8<-- "docs/snippets/design/schedule-evaluator/4_schedulefile_support.py:example"
```

## See also

- [How to evaluate schedules](../schedules/index.md) — the task-oriented recipes.
- [API reference: schedules](../api/schedules/index.md) — signatures and types.
