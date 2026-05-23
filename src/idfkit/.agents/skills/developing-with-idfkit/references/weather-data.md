# Weather data

`idfkit.weather` provides everything you need to attach realistic weather to a model: a bundled index of ~55,000 climate.onebuilding.org TMYx datasets across ~17,300 unique physical stations, an EPW/DDY downloader with local caching, ASHRAE design-day injection, and a Nominatim-backed geocoder.

## When to use

- You need an `.epw` weather file for a simulation.
- You're picking the nearest weather station to a building site (by name, address, or coordinates).
- You need to inject sizing design days into a model so EnergyPlus can autosize HVAC.
- You're building a batch over multiple climates.

## Quick start

```python
from idfkit.weather import StationIndex, WeatherDownloader

index = StationIndex.load()                # local, instant
results = index.search("chicago ohare")
station = results[0].station

downloader = WeatherDownloader()
files = downloader.download(station)
print(files.epw, files.ddy)
```

## Core API

```python
from idfkit.weather import (
    StationIndex,            # bundled station index
    WeatherStation,          # a single station
    SearchResult,            # search hit with score
    SpatialResult,           # nearest-neighbour hit with distance_km
    WeatherDownloader,       # EPW/DDY fetcher with cache
    WeatherFiles,            # paths to downloaded files
    geocode,                 # address → (lat, lon)
    detect_location,         # heuristic IP-based location
    DesignDayManager,        # DDY parser
    DesignDayType,           # ASHRAE 90.1 design conditions
    apply_ashrae_sizing,     # one-call ASHRAE design day injection
)
```

## Searching for a station

### By name (fuzzy)

```python
index = StationIndex.load()
hits = index.search("chicago ohare")
for hit in hits[:3]:
    print(hit.score, hit.station.display_name)
```

`search` is whitespace-tokenised and case-insensitive. Use it for "I know roughly what the station is called."

### By address (geocode + nearest)

```python
from idfkit.weather import StationIndex, geocode

index = StationIndex.load()
lat, lon = geocode("350 Fifth Avenue, New York, NY")
hits = index.nearest(lat, lon)
for hit in hits[:3]:
    print(f"{hit.station.display_name}: {hit.distance_km:.0f} km")

# Or one-liner:
results = index.nearest(*geocode("350 Fifth Avenue, New York, NY"))
```

`geocode` uses Nominatim (OpenStreetMap) — no API key, but rate-limited to 1 req/second. For batch geocoding, sleep between calls or pre-compute.

### By coordinates

```python
hits = index.nearest(lat=41.978, lon=-87.904, max_results=10)
```

### By bounding box

```python
hits = index.search_box(min_lat=40, min_lon=-75, max_lat=42, max_lon=-72)
```

## Inspecting a station

```python
station = hits[0].station
station.display_name                       # "Chicago O'Hare AP, IL, USA"
station.country_code                       # "USA"
station.region                             # "IL"
station.wmo_id                             # "725300"
station.latitude, station.longitude
station.elevation_m
station.time_zone_offset_hours
station.tmyx_range                         # e.g. "TMYx.2009-2023"
station.epw_url                            # download URL
station.ddy_url
```

Multiple `WeatherStation` entries can share the same `wmo_id` — each TMYx year-range variant is a separate entry.

## Downloading EPW + DDY

```python
from idfkit.weather import WeatherDownloader

downloader = WeatherDownloader(cache_dir="~/.cache/idfkit/weather")
files = downloader.download(station)       # downloads if absent, returns cached path otherwise
files.epw                                  # Path
files.ddy
files.station
```

`WeatherDownloader` is idempotent — repeated `download()` calls hit the cache. To force re-download, pass `force=True`.

The cache directory defaults to `$XDG_CACHE_HOME/idfkit/weather` on Linux, `~/Library/Caches/idfkit/weather` on macOS, and `%LOCALAPPDATA%\idfkit\weather` on Windows.

## Design days

EnergyPlus autosizes HVAC equipment from "design day" conditions (typical hottest hour, typical coldest hour, etc.). They live in DDY files; `apply_ashrae_sizing` injects them into your model in one call:

```python
from idfkit import load_idf
from idfkit.weather import StationIndex, apply_ashrae_sizing

doc = load_idf("building.idf")
station = StationIndex.load().search("chicago ohare")[0].station
added = apply_ashrae_sizing(doc, station, standard="90.1")
print(f"Added {len(added)} design days")
```

The default `standard="90.1"` covers ASHRAE 90.1 99.6% and 0.4% conditions. Other choices: `"169"` for ASHRAE 169 climate zones, `"custom"` to pass your own DDY content.

Lower-level access:

```python
from idfkit.weather import DesignDayManager, DesignDayType

ddm = DesignDayManager.from_ddy_url(station.ddy_url)
heating = ddm.get(DesignDayType.HEATING_99_6)
cooling = ddm.get(DesignDayType.COOLING_0_4)
ddm.inject(doc, [heating, cooling])
```

`NoDesignDaysError` is raised when a station's DDY contains no usable design days (rare, but possible for incomplete TMYx entries).

## Detecting the user's location

For interactive tooling that wants a sensible default:

```python
from idfkit.weather import detect_location

lat, lon = detect_location()               # IP-based geolocation, best-effort
nearest = StationIndex.load().nearest(lat, lon)[0]
```

## Refreshing the index

The bundled index ages well — TMYx datasets don't change often. To refresh from upstream:

```python
from idfkit.weather import StationIndex

if index.check_for_updates():
    index = StationIndex.refresh()         # re-download + rebuild
```

`refresh()` requires `idfkit[weather]` for the openpyxl extra (TMYx publishes the catalogue as `.xlsx`).

## Common mistakes

**BAD — geocoding in a tight loop**

```python
for addr in addresses:
    lat, lon = geocode(addr)               # Nominatim rate-limits, will start failing
```

**GOOD — sleep, or pre-compute**

```python
import time
coords = []
for addr in addresses:
    coords.append(geocode(addr))
    time.sleep(1.0)
```

**BAD — simulating without design days**

```python
doc = load_idf("building.idf")
simulate(doc, "weather.epw")               # autosizing fails — no design days in the model
```

**GOOD — apply design days first**

```python
station = StationIndex.load().search("chicago ohare")[0].station
apply_ashrae_sizing(doc, station, standard="90.1")
simulate(doc, "weather.epw")
```

**BAD — assuming `display_name` is unique**

```python
station_by_name = {s.display_name: s for s in index.stations}
# Collisions when multiple TMYx year-ranges exist for the same WMO ID.
```

**GOOD — key on `(wmo_id, tmyx_range)` if you need uniqueness**

```python
station_by_key = {(s.wmo_id, s.tmyx_range): s for s in index.stations}
```

## Related

- [simulation-execution.md](simulation-execution.md) — passing `weather.epw` to `simulate(...)`.
- [version-migration.md](version-migration.md) — design days from old DDY files may need updating.
- CLI: `idfkit tmy` searches and downloads TMYx files from the shell.
- API docs: [py.idfkit.com/weather/](https://py.idfkit.com/weather/)
