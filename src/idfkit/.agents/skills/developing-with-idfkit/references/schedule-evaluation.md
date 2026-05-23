# Schedule evaluation

`idfkit.schedules` evaluates EnergyPlus schedules **without running a simulation**. Useful for visualisation, debugging, building parametric inputs, and any workflow where you need the value of a `Schedule:*` at a given timestamp.

## When to use

- You want to see what a `Schedule:Compact` resolves to at hour 14:00 on a Tuesday.
- You're plotting an annual schedule to confirm it matches expectations.
- You're synthesising schedules from a `numpy` array or a pandas `Series`.
- You're auditing a model to find every schedule it uses.

## Quick start

```python
from datetime import datetime
from idfkit import load_idf
from idfkit.schedules import evaluate, values, to_series

doc = load_idf("building.idf")
sched = doc["Schedule:Compact"]["Office Occupancy"]

# Single timestamp
v = evaluate(sched, datetime(2024, 1, 8, 10, 0))
print(v)                                   # 1.0 (fully occupied at Monday 10am)

# Full year, hourly
year = values(sched, year=2024)
print(len(year))                           # 8760

# Pandas (requires idfkit[dataframes])
series = to_series(sched, year=2024)
series.plot()
```

## Core API

```python
from idfkit.schedules import (
    evaluate,                            # single-timestamp lookup
    values,                              # array of hourly (or sub-hourly) values
    to_series,                           # pandas Series
    plot_schedule, plot_day, plot_week,  # quick plots
    create_compact_schedule_from_values,
    create_constant_schedule,
    create_schedule_type_limits,
    ScheduleFileCache,
    get_holidays,
    extract_special_days,
)
```

## Supported schedule types

The evaluator covers every standard EnergyPlus schedule type:

- `Schedule:Compact` (the most common)
- `Schedule:Year` + `Schedule:Week:Daily` / `Week:Compact` + `Schedule:Day:Hourly` / `Day:Interval` / `Day:List`
- `Schedule:Constant`
- `Schedule:File` (reads the CSV directly, with optional `FileSystem` for S3)
- `ScheduleTypeLimits` resolution

If you hit an unsupported type, `UnsupportedScheduleType` is raised.

## Single-timestamp evaluation

```python
from datetime import datetime
from idfkit.schedules import evaluate

sched = doc["Schedule:Compact"]["Office Occupancy"]

# Default — uses the calendar day type derived from the date
v = evaluate(sched, datetime(2024, 7, 15, 14, 0))

# Override day type (useful for sizing checks)
v_summer = evaluate(sched, datetime(2024, 7, 15, 14, 0), day_type="summer")
v_winter = evaluate(sched, datetime(2024, 1, 15, 6, 0),  day_type="winter")
v_holiday = evaluate(sched, datetime(2024, 12, 25, 10, 0), day_type="holiday")
```

`day_type` accepts `"normal"`, `"summer"`, `"winter"`, `"holiday"` and an explicit `DayType` enum.

## Annual values

```python
from idfkit.schedules import values

annual = values(sched, year=2024)                 # 8760 hourly values
sub_hourly = values(sched, year=2024, timestep=4) # 35,040 quarter-hourly values
```

By default `values` returns a `list[float]`. For pandas:

```python
from idfkit.schedules import to_series

ts = to_series(sched, year=2024)                  # DatetimeIndex, length 8760
```

## Plotting

```python
from idfkit.schedules import plot_schedule, plot_day, plot_week

plot_schedule(sched, year=2024)            # entire year
plot_day(sched, datetime(2024, 7, 15))     # one day
plot_week(sched, datetime(2024, 7, 15))    # surrounding week
```

These pick the default backend (matplotlib if `idfkit[plot]` is installed, plotly if `idfkit[plotly]`). Pass `backend="plotly"` or `backend="matplotlib"` to force.

## Building schedules programmatically

```python
from idfkit.schedules import (
    create_constant_schedule,
    create_compact_schedule_from_values,
    create_schedule_type_limits,
)

# Type limits (required by many schedule types)
limits = create_schedule_type_limits(doc, "Fraction", lower=0.0, upper=1.0, numeric_type="Continuous")

# Constant
always_on = create_constant_schedule(doc, "Always On", value=1.0, type_limits_name="Fraction")

# From an array of 8760 hourly values
import numpy as np
arr = np.zeros(8760)
arr[6 * 24 : 18 * 24] = 1.0                # mornings of week 1 occupied (toy example)
sched = create_compact_schedule_from_values(
    doc, "Office Occupancy", arr,
    type_limits_name="Fraction",
)
```

`create_compact_schedule_from_values` is a one-shot way to take an array and emit a `Schedule:Compact` object — useful when you have hourly inputs from measurement data.

## Auditing schedule usage

```python
# Names of every schedule referenced by anything in the model
used = doc.get_used_schedules()            # set[str]
all_schedules = doc.schedules_dict        # {name: IDFObject} across all Schedule:* types

# Unused schedules — can usually be deleted
for name in all_schedules.keys() - used:
    print("unused:", name)
```

## Schedule:File

`Schedule:File` reads CSV data from disk (or S3 if you provide a `FileSystem`):

```python
from idfkit.simulation.fs import S3FileSystem
from idfkit.schedules import values

fs = S3FileSystem(bucket="models", prefix="data/")
hourly = values(doc["Schedule:File"]["Plug Loads"], fs=fs)
```

For batch workflows reuse a `ScheduleFileCache` to avoid re-reading the same CSV:

```python
from idfkit.schedules import ScheduleFileCache

cache = ScheduleFileCache()
hourly = values(sched, file_cache=cache)
```

## Holidays and special days

```python
from idfkit.schedules import get_holidays, extract_special_days

# Pull RunPeriodControl:SpecialDays from a document for a year
specials = extract_special_days(doc, 2024)

# Set[date] of dates classified as holidays for that year
holidays = get_holidays(doc, 2024)
```

Both functions read the document's `RunPeriodControl:SpecialDays` objects — idfkit does not bundle external holiday calendars. To use country-specific calendars, add the corresponding `SpecialDays` entries yourself (e.g. from the `holidays` PyPI package) before calling.

## Common mistakes

**BAD — evaluating a schedule that references missing schedules**

```python
# Compact schedule referencing "Building Occupancy" by name, but that schedule was deleted
v = evaluate(sched, ts)                    # ScheduleReferenceError
```

**GOOD — validate first**

```python
result = validate_document(doc)            # check_references=True catches broken schedule refs
```

**BAD — assuming hourly when the schedule is sub-hourly**

```python
arr = values(sched, year=2024)             # 8760 hourly values, even if EnergyPlus would interpolate at 15 minutes
```

**GOOD — match the simulation timestep**

```python
arr = values(sched, year=2024, timestep=4) # 35,040 quarter-hourly values for a 15-minute timestep
```

**BAD — passing a date in a non-leap year for Feb 29**

```python
v = evaluate(sched, datetime(2023, 2, 29, 10, 0))   # ValueError
```

**GOOD — use a leap year or guard**

```python
v = evaluate(sched, datetime(2024, 2, 29, 10, 0))
```

## Related

- [document-and-objects.md](document-and-objects.md) — `doc.add(Schedule:Compact, ...)` etc.
- [reference-tracking.md](reference-tracking.md) — finding what references a schedule.
- [result-parsing.md](result-parsing.md) — compare evaluated schedules against simulated `Schedule Value` outputs.
- API docs: [py.idfkit.com/schedules/](https://py.idfkit.com/schedules/)
