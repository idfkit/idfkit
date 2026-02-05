# Design Days

The `DesignDayManager` parses DDY files and applies ASHRAE design day
conditions to your EnergyPlus models for HVAC sizing.

## Basic Usage

```python
from idfkit.weather import DesignDayManager

# Parse a DDY file
ddm = DesignDayManager("chicago.ddy")

# Print summary
print(ddm.summary())

# Apply design days to model
added = ddm.apply_to_model(
    model,
    heating="99.6%",
    cooling="1%",
)
print(f"Added {len(added)} design days")
```

## Quick Apply

Use `apply_ashrae_sizing()` for a streamlined workflow:

```python
from idfkit.weather import apply_ashrae_sizing, WeatherDownloader

# Download DDY file
downloader = WeatherDownloader()
files = downloader.download(station)

# Apply standard design conditions
added = apply_ashrae_sizing(
    model,
    ddy_path=files.ddy,
    standard="90.1",  # ASHRAE 90.1 criteria
)
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
| `HUMIDIF_99_6` | 99.6% humidification |
| `MONTHLY` | Monthly design conditions |

## Accessing Design Days

### By Type

```python
from idfkit.weather import DesignDayManager, DesignDayType

ddm = DesignDayManager("chicago.ddy")

# Get specific design day
htg = ddm.get(DesignDayType.HEATING_99_6)
if htg:
    print(f"Heating 99.6% DB: {htg.maximum_dry_bulb_temperature}°C")

clg = ddm.get(DesignDayType.COOLING_DB_1)
if clg:
    print(f"Cooling 1% DB: {clg.maximum_dry_bulb_temperature}°C")
```

### All Design Days

```python
# All classified annual design days
for dd_type, dd_obj in ddm.annual.items():
    print(f"{dd_type.name}: {dd_obj.name}")

# Monthly design days
for dd_obj in ddm.monthly:
    print(dd_obj.name)
```

## Applying to Models

### Basic Application

```python
added = ddm.apply_to_model(
    model,
    heating="99.6%",  # Use 99.6% heating conditions
    cooling="1%",     # Use 1% cooling conditions
)
```

### With Wet-Bulb Design Day

```python
added = ddm.apply_to_model(
    model,
    heating="99.6%",
    cooling="1%",
    include_wet_bulb=True,  # Also add WB=>MDB cooling design day
)
```

### Update Site Location

```python
added = ddm.apply_to_model(
    model,
    heating="99.6%",
    cooling="1%",
    update_location=True,  # Also add/update Site:Location
)
```

## ASHRAE Standards

Different standards recommend different percentiles:

### ASHRAE 90.1 (Energy Standard)

```python
added = ddm.apply_to_model(
    model,
    heating="99.6%",
    cooling="1%",
)

# Or use the convenience function
added = apply_ashrae_sizing(model, ddy_path=files.ddy, standard="90.1")
```

### ASHRAE 62.1 (Ventilation)

```python
added = ddm.apply_to_model(
    model,
    heating="99%",  # Less extreme
    cooling="1%",
)
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
ddm = DesignDayManager("chicago.ddy")
print(ddm.summary())
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
location = ddm.location
if location:
    print(f"Site: {location.name}")
    print(f"Latitude: {location.latitude}")
    print(f"Longitude: {location.longitude}")
    print(f"Time Zone: {location.time_zone}")
    print(f"Elevation: {location.elevation} m")
```

## Complete Workflow

```python
from idfkit import load_idf
from idfkit.weather import (
    StationIndex,
    WeatherDownloader,
    DesignDayManager,
    geocode,
)

# Load model
model = load_idf("building.idf")

# Find nearest station
index = StationIndex.load()
lat, lon = geocode("123 Main St, Chicago, IL")
station = index.nearest(lat, lon)[0].station

# Download weather files
downloader = WeatherDownloader()
files = downloader.download(station)

# Apply design days
ddm = DesignDayManager(files.ddy)
added = ddm.apply_to_model(
    model,
    heating="99.6%",
    cooling="1%",
    include_wet_bulb=True,
    update_location=True,
)

print(f"Added {len(added)} design days")
print(f"Location: {model['Site:Location'].values()[0].name}")
```

## Error Handling

```python
from idfkit.exceptions import NoDesignDaysError

try:
    ddm = DesignDayManager("incomplete.ddy")
    ddm.apply_to_model(model, heating="99.6%", cooling="1%")
except NoDesignDaysError as e:
    print(f"Missing design days: {e}")
```

## See Also

- [Weather Downloads](downloads.md) — Get DDY files
- [Station Search](station-search.md) — Find weather stations
- [Weather Pipeline](../concepts/weather-pipeline.md) — Architecture details
