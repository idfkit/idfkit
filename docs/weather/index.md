# Weather Overview

The weather module provides tools for searching weather stations, downloading
weather files, and applying ASHRAE design day conditions to your models.

## Quick Start

```python
from idfkit.weather import StationIndex, WeatherDownloader

# Load station index (instant, no network needed)
index = StationIndex.load()
print(f"{len(index)} stations from {len(index.countries)} countries")

# Search by name
results = index.search("chicago ohare")
station = results[0].station
print(f"Found: {station.display_name}")

# Download weather files
downloader = WeatherDownloader()
files = downloader.download(station)
print(f"EPW: {files.epw}")
print(f"DDY: {files.ddy}")
```

## Key Features

### 55,000+ Weather Stations

The bundled index contains data from climate.onebuilding.org, covering:

- **~55,000 dataset entries** from 10 world regions
- **~17,300 unique physical stations**
- **248 countries and territories**

### No Network Required

`StationIndex.load()` works instantly without network access — the index
is pre-compiled and bundled with the package.

### Address-Based Search

Find the nearest weather station to any address:

```python
from idfkit.weather import StationIndex, geocode

index = StationIndex.load()
results = index.nearest(*geocode("350 Fifth Avenue, New York, NY"))

for r in results[:3]:
    print(f"{r.station.display_name}: {r.distance_km:.0f} km")
```

### ASHRAE Design Days

Apply standard design day conditions to your model:

```python
from idfkit.weather import apply_ashrae_sizing

# Apply ASHRAE 90.1 design conditions
added = apply_ashrae_sizing(model, station, standard="90.1")
print(f"Added {len(added)} design days")
```

## Module Components

| Component | Description |
|-----------|-------------|
| [`StationIndex`](station-search.md) | Search and filter weather stations |
| [`WeatherDownloader`](downloads.md) | Download EPW and DDY files |
| [`DesignDayManager`](design-days.md) | Parse and apply design days |
| [`geocode()`](geocoding.md) | Convert addresses to coordinates |

## Installation

The core weather module requires no extra dependencies:

```python
from idfkit.weather import StationIndex

index = StationIndex.load()  # Works out of the box
```

To refresh the index from upstream:

```bash
pip install idfkit[weather]  # Adds openpyxl
```

```python
if index.check_for_updates():
    index = StationIndex.refresh()  # Downloads latest data
```

## Workflow Example

Complete workflow from address to simulation-ready model:

```python
from idfkit import load_idf
from idfkit.weather import (
    StationIndex,
    WeatherDownloader,
    DesignDayManager,
    geocode,
)

# Load your model
model = load_idf("building.idf")

# Find nearest station to project location
index = StationIndex.load()
lat, lon = geocode("123 Main St, Chicago, IL")
station = index.nearest(lat, lon)[0].station

# Download weather files
downloader = WeatherDownloader()
files = downloader.download(station)

# Apply design days
ddm = DesignDayManager(files.ddy)
ddm.apply_to_model(
    model,
    heating="99.6%",
    cooling="1%",
    update_location=True,
)

# Now ready for simulation
from idfkit.simulation import simulate
result = simulate(model, files.epw)
```

## Data Source

All weather data comes from [climate.onebuilding.org](https://climate.onebuilding.org),
which provides:

- TMYx (Typical Meteorological Year) files
- Multiple year ranges per station (2007-2021, 2009-2023, etc.)
- EPW format for EnergyPlus simulation
- DDY files with ASHRAE design day conditions

## Next Steps

- [Station Search](station-search.md) — Find weather stations
- [Weather Downloads](downloads.md) — Download EPW/DDY files
- [Design Days](design-days.md) — Apply ASHRAE conditions
- [Weather Pipeline Concepts](../concepts/weather-pipeline.md) — Architecture details
