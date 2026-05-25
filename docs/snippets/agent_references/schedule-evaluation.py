from __future__ import annotations

from datetime import datetime

from idfkit import IDFDocument, IDFObject, validate_document

doc: IDFDocument = ...  # type: ignore[assignment]
sched: IDFObject = ...  # type: ignore[assignment]
ts: datetime = ...  # type: ignore[assignment]

# --8<-- [start:quickstart]
from datetime import datetime
from idfkit import load_idf
from idfkit.schedules import evaluate, values, to_series

doc = load_idf("building.idf")
sched = doc["Schedule:Compact"]["Office Occupancy"]

# Single timestamp
v = evaluate(sched, datetime(2024, 1, 8, 10, 0))
print(v)  # 1.0 (fully occupied at Monday 10am)

# Full year, hourly
year = values(sched, year=2024)
print(len(year))  # 8760

# Pandas (requires idfkit[dataframes])
series = to_series(sched, year=2024)
series.plot()
# --8<-- [end:quickstart]


# --8<-- [start:core-api]
from idfkit.schedules import (
    evaluate,  # single-timestamp lookup
    values,  # array of hourly (or sub-hourly) values
    to_series,  # pandas Series
    plot_schedule,
    plot_day,
    plot_week,  # quick plots
    create_compact_schedule_from_values,
    create_constant_schedule,
    create_schedule_type_limits,
    ScheduleFileCache,
    get_holidays,
    extract_special_days,
)
# --8<-- [end:core-api]


# --8<-- [start:single-timestamp]
from datetime import datetime
from idfkit.schedules import evaluate

sched = doc["Schedule:Compact"]["Office Occupancy"]

# Default — uses the calendar day type derived from the date
v = evaluate(sched, datetime(2024, 7, 15, 14, 0))

# Override day type (useful for sizing checks)
v_summer = evaluate(sched, datetime(2024, 7, 15, 14, 0), day_type="summer")
v_winter = evaluate(sched, datetime(2024, 1, 15, 6, 0), day_type="winter")
v_holiday = evaluate(sched, datetime(2024, 12, 25, 10, 0), day_type="holiday")
# --8<-- [end:single-timestamp]


# --8<-- [start:annual-values]
from idfkit.schedules import values

annual = values(sched, year=2024)  # 8760 hourly values
sub_hourly = values(sched, year=2024, timestep=4)  # 35,040 quarter-hourly values
# --8<-- [end:annual-values]


# --8<-- [start:to-series]
from idfkit.schedules import to_series

ts = to_series(sched, year=2024)  # DatetimeIndex, length 8760
# --8<-- [end:to-series]


# --8<-- [start:plotting]
from idfkit.schedules import plot_schedule, plot_day, plot_week

plot_schedule(sched, year=2024)  # entire year
plot_day(sched, year=2024, month=7, day=15)  # one day
plot_week(sched, year=2024, week=29)  # week 29 (mid-July)
# --8<-- [end:plotting]


# --8<-- [start:build-programmatically]
from idfkit.schedules import (
    create_constant_schedule,
    create_compact_schedule_from_values,
    create_schedule_type_limits,
)

# Type limits (required by many schedule types)
limits = create_schedule_type_limits(doc, "Fraction", lower=0.0, upper=1.0)

# Constant
always_on = create_constant_schedule(doc, "Always On", value=1.0, type_limits="Fraction")

# From an array of hourly values for the year. The array length must match
# the number of hours in the target year (8760 for non-leap, 8784 for leap).
import numpy as np

arr = np.zeros(8760)
arr[6 * 24 : 18 * 24] = 1.0  # mornings of week 1 occupied (toy example)
sched = create_compact_schedule_from_values(
    doc,
    "Office Occupancy",
    arr.tolist(),  # Sequence[float] — NumPy arrays need .tolist()
    year=2023,  # non-leap → 8760
    type_limits="Fraction",
)
# --8<-- [end:build-programmatically]


# --8<-- [start:audit]
# Names of every schedule referenced by anything in the model
used = doc.get_used_schedules()  # set[str]
all_schedules = doc.schedules_dict  # {name: IDFObject} across all Schedule:* types

# Unused schedules — can usually be deleted
for name in all_schedules.keys() - used:
    print("unused:", name)
# --8<-- [end:audit]


# --8<-- [start:schedule-file]
from idfkit.simulation.fs import S3FileSystem
from idfkit.schedules import values

fs = S3FileSystem(bucket="models", prefix="data/")
hourly = values(doc["Schedule:File"]["Plug Loads"], fs=fs)
# --8<-- [end:schedule-file]


# --8<-- [start:schedule-file-cache]
from idfkit.schedules import ScheduleFileCache
from idfkit.simulation.fs import LocalFileSystem

# Reuse one cache across many Schedule:File reads to avoid re-parsing the CSV.
cache = ScheduleFileCache()
file_sched = doc["Schedule:File"]["Plug Loads"]
raw = cache.get_values(file_sched, LocalFileSystem())  # parsed once, cached by file + column
# --8<-- [end:schedule-file-cache]


# --8<-- [start:holidays]
from idfkit.schedules import get_holidays, extract_special_days

# Pull RunPeriodControl:SpecialDays from a document for a year
specials = extract_special_days(doc, 2024)

# Set[date] of dates classified as holidays for that year
holidays = get_holidays(doc, 2024)
# --8<-- [end:holidays]


# --8<-- [start:mistake-broken-good]
result = validate_document(doc)  # check_references=True catches broken schedule refs
# --8<-- [end:mistake-broken-good]


# --8<-- [start:mistake-subhourly-good]
arr = values(sched, year=2024, timestep=4)  # 35,040 quarter-hourly values for a 15-minute timestep
# --8<-- [end:mistake-subhourly-good]


# --8<-- [start:mistake-leap-good]
v = evaluate(sched, datetime(2024, 2, 29, 10, 0))
# --8<-- [end:mistake-leap-good]
