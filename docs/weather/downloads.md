# Weather Downloads

The `WeatherDownloader` downloads EPW and DDY weather files from
climate.onebuilding.org with automatic caching.

## Basic Usage

```python
from idfkit.weather import StationIndex, WeatherDownloader

# Find a station
index = StationIndex.load()
station = index.search("chicago ohare")[0].station

# Download weather files
downloader = WeatherDownloader()
files = downloader.download(station)

print(f"EPW: {files.epw}")
print(f"DDY: {files.ddy}")
```

## WeatherFiles

The `download()` method returns a `WeatherFiles` object:

| Attribute | Type | Description |
|-----------|------|-------------|
| `epw` | `Path` | Path to the EPW file |
| `ddy` | `Path \| None` | Path to the DDY file (may be None) |

```python
files = downloader.download(station)

# Use for simulation
from idfkit.simulation import simulate
result = simulate(model, files.epw)

# Use for design days
if files.ddy:
    from idfkit.weather import DesignDayManager
    ddm = DesignDayManager(files.ddy)
```

## Caching

Downloaded files are cached locally to avoid redundant downloads:

```python
# First download: fetches from internet
files1 = downloader.download(station)

# Second download: instant from cache
files2 = downloader.download(station)

assert files1.epw == files2.epw  # Same cached file
```

### Cache Location

Default locations by platform:

| Platform | Default Path |
|----------|--------------|
| Linux | `~/.cache/idfkit/weather/files/` |
| macOS | `~/Library/Caches/idfkit/weather/files/` |
| Windows | `%LOCALAPPDATA%\idfkit\cache\weather\files\` |

### Custom Cache Directory

```python
from pathlib import Path

downloader = WeatherDownloader(cache_dir=Path("/data/weather_cache"))
```

### Clear Cache

```python
import shutil

shutil.rmtree(downloader.cache_dir)
```

## Download Process

The downloader:

1. Checks if files are already cached
2. Downloads the ZIP file from the station's URL
3. Extracts EPW and DDY files
4. Stores in the cache directory
5. Returns paths to the extracted files

## Error Handling

```python
from idfkit.weather import WeatherDownloader

downloader = WeatherDownloader()

try:
    files = downloader.download(station)
except Exception as e:
    print(f"Download failed: {e}")
```

Common errors:

- Network connectivity issues
- Invalid station URL
- Server temporarily unavailable

## Offline Usage

Once files are cached, no network is needed:

```python
# Pre-download files while online
downloader = WeatherDownloader()
for station in my_stations:
    downloader.download(station)

# Later, offline usage works
files = downloader.download(station)  # From cache
```

## Batch Downloads

Download files for multiple stations:

```python
from idfkit.weather import StationIndex, WeatherDownloader

index = StationIndex.load()
downloader = WeatherDownloader()

# Download for multiple cities
cities = ["chicago", "new york", "los angeles", "houston"]
weather_files = {}

for city in cities:
    station = index.search(city)[0].station
    files = downloader.download(station)
    weather_files[city] = files
    print(f"Downloaded: {station.display_name}")
```

## File Format Details

### EPW (EnergyPlus Weather)

- Hourly weather data for a typical meteorological year
- Contains temperature, humidity, solar radiation, wind, etc.
- Used by `simulate()` for annual simulations

### DDY (Design Day)

- ASHRAE design day conditions
- Contains `SizingPeriod:DesignDay` objects
- Used for HVAC sizing calculations

## Integration Example

Complete workflow:

```python
from idfkit import load_idf
from idfkit.weather import (
    StationIndex,
    WeatherDownloader,
    DesignDayManager,
    geocode,
)
from idfkit.simulation import simulate

# Load model
model = load_idf("building.idf")

# Find station near project site
index = StationIndex.load()
lat, lon = geocode("123 Main St, Chicago, IL")
station = index.nearest(lat, lon)[0].station

# Download weather files
downloader = WeatherDownloader()
files = downloader.download(station)

# Apply design days
if files.ddy:
    ddm = DesignDayManager(files.ddy)
    ddm.apply_to_model(model, heating="99.6%", cooling="1%")

# Run simulation
result = simulate(model, files.epw, design_day=True)
print(f"Success: {result.success}")
```

## See Also

- [Station Search](station-search.md) — Find weather stations
- [Design Days](design-days.md) — Apply design day conditions
- [Weather Pipeline](../concepts/weather-pipeline.md) — Architecture details
