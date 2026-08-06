# How to apply design days

The `DesignDayManager` parses DDY files and applies ASHRAE design day
conditions to your EnergyPlus models for HVAC sizing.

## Basic Usage

```python
--8<-- "docs/snippets/weather/design-days/basic_usage.py:example"
```

## Quick Apply

Use `apply_ashrae_sizing()` for a streamlined workflow:

```python
--8<-- "docs/snippets/weather/design-days/quick_apply.py:example"
```

## Design Day Types

DDY files contain multiple design day types classified by ASHRAE criteria:

### Heating Design Days

| Type | Description | Use Case |
|------|-------------|----------|
| `HEATING_99_6` | 99.6% heating DB | ASHRAE 90.1 (coldest) |
| `HEATING_99` | 99% heating DB | ASHRAE 62.1 |
| `HTG_WIND_99_6` | Heating wind 99.6% | Wind-driven infiltration |

### Cooling Design Days

| Type | Description | Use Case |
|------|-------------|----------|
| `COOLING_DB_0_4` | 0.4% cooling DB=>MWB | Extreme cooling |
| `COOLING_DB_1` | 1% cooling DB=>MWB | ASHRAE 90.1 |
| `COOLING_DB_2` | 2% cooling DB=>MWB | Less extreme |
| `COOLING_WB_0_4` | 0.4% cooling WB=>MDB | Humidity-driven |
| `COOLING_WB_1` | 1% cooling WB=>MDB | ASHRAE 90.1 |
| `COOLING_ENTH_0_4` | 0.4% enthalpy | Peak enthalpy |
| `COOLING_ENTH_1` | 1% enthalpy | Standard enthalpy |

### Other Types

| Type | Description |
|------|-------------|
| `DEHUMID_0_4` | 0.4% dehumidification |
| `DEHUMID_1` | 1% dehumidification |
| `HUMIDIFICATION_99_6` | 99.6% humidification |
| `HUMIDIFICATION_99` | 99% humidification |

## Accessing Design Days

### By Type

```python
--8<-- "docs/snippets/weather/design-days/by_type.py:example"
```

### All Design Days

```python
--8<-- "docs/snippets/weather/design-days/all_design_days.py:example"
```

## Applying to Models

### Basic Application

```python
--8<-- "docs/snippets/weather/design-days/basic_application.py:example"
```

### With Wet-Bulb Design Day

```python
--8<-- "docs/snippets/weather/design-days/with_wet_bulb_design_day.py:example"
```

### Skip Site Location Update

By default, `apply_to_model` also updates the `Site:Location` object.
To skip this, set `update_location=False`:

```python
--8<-- "docs/snippets/weather/design-days/skip_site_location_update.py:example"
```

## ASHRAE Standards

Different standards recommend different percentiles:

### ASHRAE 90.1 (Energy Standard)

```python
--8<-- "docs/snippets/weather/design-days/ashrae_901_energy_standard.py:example"
```

### ASHRAE 62.1 (Ventilation)

```python
--8<-- "docs/snippets/weather/design-days/ashrae_621_ventilation.py:example"
```

## Design Day Object Fields

When you access a design day, it's an `IDFObject` with these fields:

| Field | Description |
|-------|-------------|
| `name` | Design day name |
| `month` | Month (1-12) |
| `day_of_month` | Day of month |
| `day_type` | Day type string |
| `maximum_dry_bulb_temperature` | Peak dry-bulb temp (°C) |
| `daily_dry_bulb_temperature_range` | Diurnal range (°C) |
| `humidity_condition_type` | How humidity is specified |
| `wetbulb_or_dewpoint_at_maximum_dry_bulb` | Humidity value |
| `wind_speed` | Design wind speed (m/s) |
| `wind_direction` | Wind direction (degrees) |

## Summary Output

```python
--8<-- "docs/snippets/weather/design-days/summary_output.py:example"
```

Output:
```
Design days from: chicago.ddy

  Location: Chicago Ohare Intl AP
  Design days found: 114
  Annual (classified): 18
  Monthly: 96

  [heating_99.6] Chicago Ohare Intl AP Ann Htg 99.6% Condns DB
  [heating_99] Chicago Ohare Intl AP Ann Htg 99% Condns DB
  [cooling_db_0.4] Chicago Ohare Intl AP Ann Clg .4% Condns DB=>MWB
  ...
```

## Location Object

DDY files also contain `Site:Location` data:

```python
--8<-- "docs/snippets/weather/design-days/location_object.py:example"
```

## Complete Workflow

```python
--8<-- "docs/snippets/weather/design-days/complete_workflow.py:example"
```

## Error Handling

```python
--8<-- "docs/snippets/weather/design-days/error_handling.py:example"
```

## See Also

- [Weather Downloads](downloads.md) — Get DDY files
- [Station Search](station-search.md) — Find weather stations
- [Weather Pipeline](../concepts/weather-pipeline.md) — Architecture details
