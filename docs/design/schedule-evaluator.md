# Schedule Evaluator Module Design

## Overview

A lightweight module to evaluate EnergyPlus schedules without running a simulation.
Returns the schedule value at any given datetime or produces hourly time series.

## Goals

1. **Minimal dependencies** - Core functionality requires only stdlib; pandas/matplotlib optional
2. **Works with existing idfkit** - Operates on `IDFObject` instances from `IDFDocument`
3. **Correct EnergyPlus semantics** - Matches E+ interpretation of schedule syntax
4. **Composable API** - Low-level `evaluate()` + high-level `to_series()`

## Supported Schedule Types

| Type | Priority | Complexity |
|------|----------|------------|
| `Schedule:Constant` | P0 | Trivial |
| `Schedule:Day:Hourly` | P0 | Simple - 24 values |
| `Schedule:Day:Interval` | P0 | Medium - time/value pairs |
| `Schedule:Day:List` | P1 | Medium - values at fixed intervals |
| `Schedule:Week:Daily` | P0 | Simple - 7 day schedule refs |
| `Schedule:Week:Compact` | P1 | Medium - day type rules |
| `Schedule:Year` | P0 | Medium - date ranges → week refs |
| `Schedule:Compact` | P0 | Complex - nested DSL |
| `Schedule:File` | P2 | External CSV parsing |

## Module Structure

```
src/idfkit/schedules/
├── __init__.py          # Public API exports
├── evaluate.py          # Core evaluation logic + dispatch
├── types.py             # DayType, Interpolation enums, SpecialDay dataclass
├── compact.py           # Schedule:Compact parser
├── day.py               # Day schedule handlers (Hourly, Interval, List)
├── week.py              # Week schedule handlers (Daily, Compact)
├── year.py              # Year schedule + date matching
├── file.py              # Schedule:File CSV reader with FileSystem support
├── holidays.py          # RunPeriodControl:SpecialDays parser
└── series.py            # pandas integration (optional)
```

## Public API

### Core Function

```python
def evaluate(
    schedule: IDFObject,
    dt: datetime,
    document: IDFDocument | None = None,
    day_type: DayType = DayType.NORMAL,
    fs: FileSystem | None = None,
) -> float:
    """
    Get schedule value at a specific datetime.

    Args:
        schedule: An IDF schedule object (any supported type)
        dt: The datetime to evaluate
        document: Required for schedules that reference others (Year, Week)
                  If None, extracted from schedule._document
        day_type: Override with design day schedule (for sizing calcs)
        fs: FileSystem for Schedule:File (default: LocalFileSystem)

    Returns:
        The schedule value as a float

    Raises:
        ScheduleEvaluationError: If schedule type unsupported or malformed
    """
```

### Batch Evaluation

```python
def values(
    schedule: IDFObject,
    year: int = 2024,
    timestep: int = 1,  # per hour
    start_date: tuple[int, int] = (1, 1),   # (month, day)
    end_date: tuple[int, int] = (12, 31),
    document: IDFDocument | None = None,
    day_type: DayType = DayType.NORMAL,
    interpolation: Interpolation = Interpolation.NO,
    fs: FileSystem | None = None,
) -> list[float]:
    """
    Generate schedule values for a date range.

    Returns one value per timestep for the entire period.
    Default: 8760 hourly values for a full year.

    Args:
        timestep: Values per hour (1, 2, 4, 6, 12, or 60)
        interpolation: How to handle sub-hourly alignment
        day_type: Use design day schedule for all days
    """
```

### Pandas Integration (optional)

```python
def to_series(
    schedule: IDFObject,
    year: int = 2024,
    freq: str = "h",  # hourly
    start_date: tuple[int, int] = (1, 1),
    end_date: tuple[int, int] = (12, 31),
    document: IDFDocument | None = None,
    day_type: DayType = DayType.NORMAL,
    interpolation: Interpolation = Interpolation.NO,
    fs: FileSystem | None = None,
) -> pd.Series:
    """
    Convert schedule to pandas Series with DatetimeIndex.

    Requires: pandas (optional dependency)
    """
```

### Convenience on IDFDocument

```python
class IDFDocument:
    def evaluate_schedule(
        self,
        name: str,
        dt: datetime,
        day_type: DayType = DayType.NORMAL,
    ) -> float:
        """Shorthand for evaluate(self.get_schedule(name), dt, self)"""

    def schedule_values(
        self,
        name: str,
        year: int = 2024,
        timestep: int = 1,
        day_type: DayType = DayType.NORMAL,
        interpolation: Interpolation = Interpolation.NO,
    ) -> list[float]:
        """Shorthand for values(self.get_schedule(name), ...)"""
```

## Schedule:Compact Parser

The most complex part. Schedule:Compact uses a mini-DSL:

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

### Parsing Strategy

```python
@dataclass
class CompactPeriod:
    """A 'Through:' block covering a date range."""
    end_month: int
    end_day: int
    day_rules: list[CompactDayRule]

@dataclass
class CompactDayRule:
    """A 'For:' block with day types and time-value pairs."""
    day_types: set[str]  # {"Weekdays", "Weekends", "Holidays", ...}
    time_values: list[tuple[time, float]]  # [(08:00, 0.0), (18:00, 1.0), ...]

def parse_compact(obj: IDFObject) -> list[CompactPeriod]:
    """Parse Schedule:Compact fields into structured data."""
```

### Day Type Mapping

EnergyPlus day types to Python weekday:

| E+ Day Type | Python weekday() |
|-------------|------------------|
| Sunday | 6 |
| Monday | 0 |
| Tuesday | 1 |
| Wednesday | 2 |
| Thursday | 3 |
| Friday | 4 |
| Saturday | 5 |
| Weekdays | 0-4 |
| Weekends | 5-6 |
| AllDays | 0-6 |
| Holidays | (requires holiday list) |
| SummerDesignDay | (special) |
| WinterDesignDay | (special) |
| AllOtherDays | (fallback) |

## Hierarchical Schedule Resolution

`Schedule:Year` references `Schedule:Week:*` which references `Schedule:Day:*`:

```python
def evaluate_year(obj: IDFObject, dt: datetime, doc: IDFDocument) -> float:
    # 1. Find which date range contains dt
    # 2. Get the referenced week schedule name
    # 3. Look up week schedule in document
    # 4. Evaluate week schedule for dt
    week_name = find_week_for_date(obj, dt)
    week_obj = doc.get_schedule(week_name) or doc[week_type][week_name]
    return evaluate_week(week_obj, dt, doc)

def evaluate_week_daily(obj: IDFObject, dt: datetime, doc: IDFDocument) -> float:
    # Schedule:Week:Daily has 12 fields: Sunday-Saturday + Holiday + Summer/Winter DD + Custom
    day_index = dt.weekday()  # 0=Mon, need to map to E+ order (Sun=0)
    field_map = {6: 0, 0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6}  # Python weekday → E+ field
    day_name = obj[field_name_for_index(field_map[day_index])]
    day_obj = doc[day_schedule_type][day_name]
    return evaluate_day(day_obj, dt, doc)
```

## Schedule:Day Evaluation

### Schedule:Day:Hourly

24 values, one per hour:

```python
def evaluate_day_hourly(obj: IDFObject, dt: datetime) -> float:
    hour = dt.hour  # 0-23
    field_name = f"Hour {hour + 1}"  # "Hour 1" through "Hour 24"
    return float(obj[field_name])
```

### Schedule:Day:Interval

Time/value pairs where value applies UNTIL that time:

```python
def evaluate_day_interval(obj: IDFObject, dt: datetime) -> float:
    # Fields: Time 1, Value Until Time 1, Time 2, Value Until Time 2, ...
    current_time = dt.time()
    last_value = 0.0

    for i in range(1, 145):  # Max 144 intervals
        time_field = f"Time {i}"
        value_field = f"Value Until Time {i}"
        if not obj.get(time_field):
            break
        until_time = parse_time(obj[time_field])  # "HH:MM"
        if current_time < until_time:
            return float(obj[value_field])
        last_value = float(obj[value_field])

    return last_value
```

## Error Handling

```python
class ScheduleEvaluationError(Exception):
    """Raised when schedule cannot be evaluated."""
    pass

class UnsupportedScheduleType(ScheduleEvaluationError):
    """Schedule type not yet implemented."""
    pass

class ScheduleReferenceError(ScheduleEvaluationError):
    """Referenced schedule not found in document."""
    pass

class MalformedScheduleError(ScheduleEvaluationError):
    """Schedule syntax is invalid."""
    pass
```

## Testing Strategy

1. **Unit tests per schedule type** - Test each parser/evaluator in isolation
2. **Known-value tests** - Compare against EnergyPlus ESO output for same schedule
3. **Round-trip tests** - `values()` output matches E+ hourly report
4. **Edge cases** - Leap years, DST (E+ doesn't use DST), midnight boundaries

### Example Test

```python
def test_compact_weekday_schedule():
    doc = load_idf("tests/fixtures/office_schedules.idf")
    schedule = doc.get_schedule("Office Occupancy")

    # Monday 10am should be occupied
    assert evaluate(schedule, datetime(2024, 1, 8, 10, 0)) == 1.0

    # Saturday 10am should be unoccupied
    assert evaluate(schedule, datetime(2024, 1, 6, 10, 0)) == 0.0

    # Monday 6am should be unoccupied (before 8am)
    assert evaluate(schedule, datetime(2024, 1, 8, 6, 0)) == 0.0
```

## Dependencies

### Required
- None (stdlib only for core)

### Internal (from idfkit)
- `idfkit.simulation.fs.FileSystem` - For Schedule:File CSV reading
- `idfkit.simulation.fs.LocalFileSystem` - Default filesystem

### Optional
- `pandas` - for `to_series()` and DataFrame integration

```toml
[project.optional-dependencies]
# No new deps needed - reuse existing
dataframes = ["pandas>=2.0"]  # Already exists
```

### FileSystem Integration

The `FileSystem` protocol enables Schedule:File to work with remote storage:

```python
from idfkit import load_idf
from idfkit.simulation.fs import S3FileSystem
from idfkit.schedules import values

# Load model from S3
fs = S3FileSystem(bucket="models", prefix="building-42/")
model = load_idf("model.idf")  # Local IDF

# Evaluate Schedule:File that references CSV on S3
schedule = model.get_schedule("External Occupancy")
hourly = values(schedule, fs=fs)  # Reads CSV from S3
```

## Implementation Order

1. **Phase 1: Foundation** (~120 LOC)
   - `types.py`: Enums (`DayType`, `Interpolation`), `SpecialDay` dataclass
   - `holidays.py`: Parse `RunPeriodControl:SpecialDays`
   - `day.py`: `Schedule:Constant`, `Schedule:Day:Hourly`, `Schedule:Day:Interval`

2. **Phase 2: Hierarchical schedules** (~150 LOC)
   - `week.py`: `Schedule:Week:Daily`, `Schedule:Week:Compact`
   - `year.py`: `Schedule:Year`, date range matching
   - Reference resolution across schedule types

3. **Phase 3: Compact parser** (~200 LOC)
   - `compact.py`: `Schedule:Compact` DSL parser
   - `Through:`, `For:`, `Until:` syntax
   - Day type matching (Weekdays, Weekends, Holidays, Design days)

4. **Phase 4: Schedule:File** (~100 LOC)
   - `file.py`: CSV parsing with `FileSystem` protocol
   - Column/separator handling
   - Value caching

5. **Phase 5: Integration** (~80 LOC)
   - `evaluate.py`: Dispatch + interpolation logic
   - `series.py`: `to_series()` pandas wrapper
   - `IDFDocument` convenience methods

Total estimate: ~650 LOC + tests

## Design Decisions

### 1. Holidays

Holidays are extracted from `RunPeriodControl:SpecialDays` objects in the document.

```python
@dataclass
class SpecialDay:
    """A special day period from RunPeriodControl:SpecialDays."""
    name: str
    start_date: date  # Parsed from "January 1" or "1/1" etc.
    duration: int     # Days
    day_type: str     # "Holiday", "CustomDay1", "CustomDay2", etc.

def extract_special_days(doc: IDFDocument) -> list[SpecialDay]:
    """Parse all RunPeriodControl:SpecialDays objects."""
    ...

def get_holidays(doc: IDFDocument, year: int) -> set[date]:
    """Get all dates marked as Holiday for a given year."""
    ...
```

Day types from `RunPeriodControl:SpecialDays`:
- `Holiday` - Standard holiday
- `CustomDay1`, `CustomDay2` - User-defined special day types

### 2. Design Days

Expose `SummerDesignDay` and `WinterDesignDay` via explicit parameter:

```python
class DayType(Enum):
    """Special day type for evaluation."""
    NORMAL = "normal"           # Use calendar day
    SUMMER_DESIGN = "summer"    # Use SummerDesignDay schedule
    WINTER_DESIGN = "winter"    # Use WinterDesignDay schedule

def evaluate(
    schedule: IDFObject,
    dt: datetime,
    document: IDFDocument | None = None,
    day_type: DayType = DayType.NORMAL,
) -> float:
    """
    Get schedule value at a specific datetime.

    Args:
        day_type: Override calendar day with design day schedule.
                  Used for sizing calculations.
    """
```

### 3. Interpolation

Match EnergyPlus interpolation behavior exactly. E+ has two modes:

**"No" (default)**: Step function - value at each interval applies until the next interval.
```
Schedule interval: 0-15min=0.0, 15-30min=0.5
Timestep 10min: value = 0.0
Timestep 20min: value = 0.5
```

**"Average"**: Linear interpolation when timestep doesn't align with intervals.
```
Schedule interval: 0-15min=0.0, 15-30min=0.5
Timestep 10min: value = 0.0
Timestep 20min: value = 0.25  (average of 0.0 and 0.5)
```

```python
class Interpolation(Enum):
    NO = "no"           # Step function (default)
    AVERAGE = "average" # Linear interpolation
    LINEAR = "linear"   # Alias for AVERAGE

def values(
    schedule: IDFObject,
    year: int = 2024,
    timestep: int = 1,  # per hour
    interpolation: Interpolation = Interpolation.NO,
    ...
) -> list[float]:
    """
    Generate schedule values with specified interpolation.

    The interpolation mode affects how values are computed when the
    evaluation timestep doesn't align with the schedule's native intervals.
    """
```

### 4. Schedule:File Support

Support external CSV files via the existing `FileSystem` protocol:

```python
def evaluate_schedule_file(
    obj: IDFObject,
    dt: datetime,
    fs: FileSystem | None = None,
    base_path: Path | str | None = None,
) -> float:
    """
    Evaluate a Schedule:File at a specific datetime.

    Args:
        obj: The Schedule:File IDF object
        dt: Datetime to evaluate
        fs: FileSystem for reading the CSV (default: LocalFileSystem)
        base_path: Base directory for resolving relative file paths
                   (default: directory containing the IDF)
    """
```

**Schedule:File fields:**
| Field | Description |
|-------|-------------|
| Name | Schedule name |
| Schedule Type Limits Name | Reference to ScheduleTypeLimits |
| File Name | Path to CSV file (relative or absolute) |
| Column Number | 1-based column index in CSV |
| Rows to Skip at Top | Header rows to skip |
| Number of Hours of Data | Usually 8760 (or 8784 for leap year) |
| Column Separator | Comma, Tab, Space, Semicolon |
| Interpolate to Timestep | "No" or "Average" |
| Minutes per Item | 60, 30, 15, 10, 5, or 1 |

**CSV parsing with FileSystem:**
```python
from idfkit.simulation.fs import FileSystem, LocalFileSystem

def _read_schedule_csv(
    file_path: str,
    column: int,
    skip_rows: int,
    separator: str,
    fs: FileSystem,
) -> list[float]:
    """Read schedule values from CSV using FileSystem protocol."""
    text = fs.read_text(file_path)
    lines = text.strip().split("\n")[skip_rows:]
    sep = {"Comma": ",", "Tab": "\t", "Space": " ", "Semicolon": ";"}[separator]
    values = []
    for line in lines:
        cols = line.split(sep)
        values.append(float(cols[column - 1]))  # 1-based index
    return values
```

**Caching:** Schedule:File data should be cached after first read to avoid repeated I/O:

```python
class ScheduleFileCache:
    """Cache for Schedule:File CSV data."""
    _cache: dict[str, list[float]]  # file_path -> values

    def get_values(
        self,
        obj: IDFObject,
        fs: FileSystem,
        base_path: Path,
    ) -> list[float]:
        """Get cached values or read from file."""
```
