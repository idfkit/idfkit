# Schedules API Reference

The schedules module provides functions to evaluate EnergyPlus schedules without
running a simulation.

## Quick Reference

| Function/Class | Description |
|---------------|-------------|
| [`evaluate()`](#idfkit.schedules.evaluate) | Evaluate a schedule at a specific datetime |
| [`values()`](#idfkit.schedules.values) | Generate values for a date range |
| [`to_series()`](#idfkit.schedules.to_series) | Convert to pandas Series |
| [`plot_schedule()`](#idfkit.schedules.plot_schedule) | Quick visualization |
| [`get_holidays()`](#idfkit.schedules.get_holidays) | Extract holidays from model |

## String Parameters

The `day_type` and `interpolation` parameters accept strings for convenience:

**day_type**: `"normal"`, `"summer"`, `"winter"`, `"holiday"`, `"customday1"`, `"customday2"`

**interpolation**: `"no"`, `"step"`, `"average"`, `"linear"`

## Core Functions

::: idfkit.schedules.evaluate
    options:
      show_root_heading: true
      show_source: false

::: idfkit.schedules.values
    options:
      show_root_heading: true
      show_source: false

## Pandas Integration

::: idfkit.schedules.to_series
    options:
      show_root_heading: true
      show_source: false

::: idfkit.schedules.plot_schedule
    options:
      show_root_heading: true
      show_source: false

::: idfkit.schedules.plot_week
    options:
      show_root_heading: true
      show_source: false

::: idfkit.schedules.plot_day
    options:
      show_root_heading: true
      show_source: false

## Enumerations

::: idfkit.schedules.DayType
    options:
      show_root_heading: true
      show_source: false
      members_order: source

::: idfkit.schedules.Interpolation
    options:
      show_root_heading: true
      show_source: false
      members_order: source

## Holiday Functions

::: idfkit.schedules.get_holidays
    options:
      show_root_heading: true
      show_source: false

::: idfkit.schedules.get_special_days_by_type
    options:
      show_root_heading: true
      show_source: false

::: idfkit.schedules.extract_special_days
    options:
      show_root_heading: true
      show_source: false

## Data Classes

::: idfkit.schedules.SpecialDay
    options:
      show_root_heading: true
      show_source: false

::: idfkit.schedules.TimeValue
    options:
      show_root_heading: true
      show_source: false

::: idfkit.schedules.CompactDayRule
    options:
      show_root_heading: true
      show_source: false

::: idfkit.schedules.CompactPeriod
    options:
      show_root_heading: true
      show_source: false

## File Support

::: idfkit.schedules.ScheduleFileCache
    options:
      show_root_heading: true
      show_source: false

## Exceptions

::: idfkit.schedules.ScheduleEvaluationError
    options:
      show_root_heading: true
      show_source: false

::: idfkit.schedules.UnsupportedScheduleType
    options:
      show_root_heading: true
      show_source: false

::: idfkit.schedules.ScheduleReferenceError
    options:
      show_root_heading: true
      show_source: false

::: idfkit.schedules.MalformedScheduleError
    options:
      show_root_heading: true
      show_source: false
