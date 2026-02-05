# Schedules Overview

The schedules module lets you evaluate EnergyPlus schedules without running a
simulation. This is useful for previewing schedule profiles, validating inputs,
and understanding building operation patterns.

## Quick Start

```python
from datetime import datetime
from idfkit import load_idf
from idfkit.schedules import evaluate, values

# Load a model
doc = load_idf("building.idf")

# Get a schedule by name
schedule = doc["Schedule:Compact"]["Office Occupancy"]

# Evaluate at a specific time
value = evaluate(schedule, datetime(2024, 1, 8, 10, 0), document=doc)
print(f"Value at Monday 10am: {value}")

# Get hourly values for a full year
hourly = values(schedule, year=2024, document=doc)
print(f"Annual hours: {len(hourly)}")  # 8784 for leap year
```

## Supported Schedule Types

| Schedule Type | Description |
|--------------|-------------|
| `Schedule:Compact` | DSL-based schedules with Through/For/Until syntax |
| `Schedule:Year` | References week schedules for date ranges |
| `Schedule:Week:Daily` | References day schedules for each weekday |
| `Schedule:Week:Compact` | Compact syntax for week schedules |
| `Schedule:Day:Hourly` | 24 hourly values |
| `Schedule:Day:Interval` | Time/value pairs |
| `Schedule:Day:List` | Values at fixed intervals |
| `Schedule:Constant` | Single constant value |
| `Schedule:File` | Values from external CSV file |

## Key Features

### Design Day Evaluation

For sizing calculations, override the day type to use design day schedules:

```python
from idfkit.schedules import evaluate

# Summer design day (typically peak cooling)
value = evaluate(
    schedule,
    datetime(2024, 7, 15, 14, 0),
    document=doc,
    day_type="summer",
)

# Winter design day (typically peak heating)
value = evaluate(
    schedule,
    datetime(2024, 1, 15, 6, 0),
    document=doc,
    day_type="winter",
)
```

Valid `day_type` values: `"normal"`, `"summer"`, `"winter"`, `"holiday"`, `"customday1"`, `"customday2"`

### Holiday Support

Holidays are automatically extracted from `RunPeriodControl:SpecialDays` objects
in your model:

```python
from idfkit.schedules import get_holidays, evaluate

# See what holidays are defined
holidays = get_holidays(doc, year=2024)
print(f"Holidays: {holidays}")

# Evaluation automatically uses holiday schedules on those dates
christmas = datetime(2024, 12, 25, 10, 0)
value = evaluate(schedule, christmas, document=doc)
```

### Sub-Hourly Timesteps

Generate values at any timestep (values per hour):

```python
from idfkit.schedules import values

# 15-minute intervals (4 per hour)
quarter_hourly = values(schedule, year=2024, timestep=4, document=doc)
print(f"Values: {len(quarter_hourly)}")  # 35136 for leap year

# 1-minute intervals
minute_values = values(schedule, year=2024, timestep=60, document=doc)
```

### Interpolation

Control how values are interpolated between defined points:

```python
from idfkit.schedules import values

# Step function (default) - value changes at each Until time
step_values = values(schedule, timestep=4, interpolation="no")

# Linear interpolation between values
smooth_values = values(schedule, timestep=4, interpolation="average")
```

Valid `interpolation` values: `"no"` (or `"step"`), `"average"` (or `"linear"`)

### Schedule:File with Remote Storage

Read CSV files from any storage backend using the FileSystem interface:

```python
from idfkit.simulation.fs import S3FileSystem
from idfkit.schedules import evaluate

# Configure S3 storage
fs = S3FileSystem(bucket="my-bucket", prefix="schedules/")

# Evaluate Schedule:File reading from S3
value = evaluate(schedule, dt, fs=fs, base_path="")
```

## Pandas Integration

Convert schedules to pandas Series for analysis and plotting:

```python
from idfkit.schedules import to_series, plot_schedule

# Convert to pandas Series with datetime index
series = to_series(schedule, year=2024, document=doc)
print(series.describe())

# Quick visualization
plot_schedule(schedule, year=2024, document=doc)
```

## Example: Analyze Office Occupancy

```python
from datetime import datetime
from idfkit import load_idf
from idfkit.schedules import values, to_series

doc = load_idf("office.idf")
occupancy = doc["Schedule:Compact"]["BLDG_OCC_SCH"]

# Get annual values
annual = values(occupancy, year=2024, document=doc)

# Basic statistics
total_hours = len([v for v in annual if v > 0])
print(f"Occupied hours: {total_hours}")

# Peak analysis with pandas
series = to_series(occupancy, year=2024, document=doc)
print(f"Peak occupancy: {series.max()}")
print(f"Average (occupied): {series[series > 0].mean():.2f}")

# Weekly pattern
weekly = series.groupby(series.index.dayofweek).mean()
print("Average by day of week:")
print(weekly)
```

## Next Steps

- [API Reference](../api/schedules/index.md) - Full API documentation
- [Design Document](../design/schedule-evaluator.md) - Implementation details
