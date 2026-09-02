# How to evaluate schedules

The schedules module lets you evaluate EnergyPlus schedules without running a
simulation. This is useful for previewing schedule profiles, validating inputs,
and understanding building operation patterns.

## Quick Start

```python
--8<-- "docs/snippets/schedules/index/quick_start.py:example"
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
--8<-- "docs/snippets/schedules/index/design_day_evaluation.py:example"
```

Valid `day_type` values: `"normal"`, `"summer"`, `"winter"`, `"holiday"`, `"customday1"`, `"customday2"`

### Holiday Support

Holidays are automatically extracted from `RunPeriodControl:SpecialDays` objects
in your model:

```python
--8<-- "docs/snippets/schedules/index/holiday_support.py:example"
```

### Sub-Hourly Timesteps

Generate values at any timestep (values per hour):

```python
--8<-- "docs/snippets/schedules/index/sub_hourly_timesteps.py:example"
```

### Interpolation

Control how values are interpolated between defined points:

```python
--8<-- "docs/snippets/schedules/index/interpolation.py:example"
```

Valid `interpolation` values: `"no"` (or `"step"`), `"average"` (or `"linear"`)

### Schedule:File with Remote Storage

Read CSV files from any storage backend using the FileSystem interface:

```python
--8<-- "docs/snippets/schedules/index/schedulefile_with_remote_storage.py:example"
```

## Pandas Integration

Convert schedules to pandas Series for analysis and plotting:

```python
--8<-- "docs/snippets/schedules/index/pandas_integration.py:example"
```

## Example: Analyze Office Occupancy

```python
--8<-- "docs/snippets/schedules/index/example_analyze_office_occupancy.py:example"
```

## Next Steps

- [API Reference](../api/schedules/index.md) - Full API documentation
- [Design Document](../design/schedule-evaluator.md) - Implementation details
