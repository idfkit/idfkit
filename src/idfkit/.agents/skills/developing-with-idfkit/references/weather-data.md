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

index = StationIndex.load()  # local, instant
results = index.search("chicago ohare")
station = results[0].station

downloader = WeatherDownloader()
files = downloader.download(station)
print(files.epw, files.ddy)
```

## Core API

```python
from idfkit.weather import (
    StationIndex,  # bundled station index
    WeatherStation,  # a single station
    WeatherDownloader,  # EPW/DDY fetcher with cache
    geocode,  # address → (lat, lon)
    detect_location,  # heuristic IP-based location
    DesignDayManager,  # DDY parser
    DesignDayType,  # ASHRAE 90.1 design conditions
    apply_ashrae_sizing,  # one-call ASHRAE design day injection
)
```

## Searching for a station

### By name (fuzzy)

```python
index = StationIndex.load()
hits = index.search("chicago ohare")
for hit in hits[:3]:
    print(hit.score, hit.station.display_name, hit.station.dataset_variant)

# One hit per physical station: .station is its newest dataset,
# .variants every TMYx year range of it, newest first.
for variant in hits[0].variants:
    print(variant.dataset_variant, variant.dataset_years)  # "TMYx.2011-2025" (2011, 2025) ... "TMYx" None
```

`search` splits the query on whitespace, commas, semicolons, dots and hyphens, and is case- and accent-insensitive (`"Montréal"` finds `Montreal`). A token equal to a station's state or country code qualifies the match instead of having to appear in its name, so `"Boulder, CO"` ranks Boulder, Colorado first; a token shorter than three characters must equal a whole word of the name rather than prefix one. A name that starts with the query outranks one that contains it later on, so `"london"` lists London City and Gatwick before East London, South Africa, and an exact WMO number scores 1.0. Use it for "I know roughly what the station is called."

A city name alone can match several countries (London is also in Ontario). Qualify it with a country or state code, or pass `country=`:

```python
index = StationIndex.load()
# Names starting with the query rank first: London City, Luton, Gatwick... before East London (ZAF).
# Add a country or state code to the query, or pass country=, to narrow further.
qualified = index.search("London, GBR")
print(qualified[0].station.display_name)  # "London City AP, ENG, GBR"
in_country = index.search("London", country="GBR")
print(in_country[0].station.display_name)  # "London City AP, ENG, GBR"
```

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

`geocode` and `detect_location` raise `GeocodingError` on failure. Branch on `exc.kind`, never on the message: `"not-found"` (the service answered, no such place; retrying will not help), `"unreachable"`, `"http"` (with `exc.status`), or `"invalid-response"`. The `Literal` of those four is `GeocodingErrorKind`, from `idfkit.weather`.

```python
from idfkit.weather import GeocodingError, geocode


def locate(query: str) -> tuple[float, float] | str:
    try:
        return geocode(query)
    except GeocodingError as exc:
        if exc.kind == "not-found":  # Nominatim answered: no such place
            return f"No place called {query!r} was found."
        # "unreachable", "http" (exc.status holds the code), or "invalid-response"
        return "The place-name service could not be reached; try again shortly."


```

### By coordinates

```python
hits = index.nearest(41.978, -87.904, limit=10)
```

### By distance

```python
# All stations within 200 km of a point
hits = index.nearest(41.0, -73.5, max_distance_km=200)
```

## Inspecting a station

```python
station = hits[0].station
station.display_name  # "Chicago O'Hare AP, IL, USA"
station.country  # "USA"
station.state  # "IL"
station.wmo  # "725300" (string, preserves leading zeros)
station.latitude, station.longitude
station.elevation  # metres above sea level
station.timezone  # hours offset from GMT, e.g. -6.0
station.dataset_variant  # which dataset, e.g. "TMYx.2011-2025" (or "TMYx")
station.dataset_years  # (2011, 2025), or None for a plain "TMYx"
station.source  # upstream source tag, e.g. "SRC-TMYx" -- not the dataset
station.url  # download URL for the ZIP (EPW + DDY)
```

Multiple `WeatherStation` entries can share the same `wmo` — each TMYx year-range variant is a separate entry, told apart by `dataset_variant`, not `source`. `search()` and `nearest()` return one hit per physical station: `hit.station` is its newest dataset and `hit.variants` all of them, newest first, so `results[0].station` downloads the latest TMYx window. An exact EPW filename passed to `search()` returns that dataset alone. `nearest()` measures each dataset at its own coordinates, which sometimes differ between a station's datasets: `hit.distance_km` is `hit.station`'s, `max_distance_km` applies to every dataset, and datasets of one station lying more than 5 km apart come back as separate hits.

## Downloading EPW + DDY

```python
from idfkit.weather import WeatherDownloader

downloader = WeatherDownloader(cache_dir=Path("~/.cache/idfkit/weather").expanduser())
files = downloader.download(station)  # downloads if absent, returns cached path otherwise
files.epw  # Path
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

`standard="90.1"` adds Heating 99.6% + Cooling 1% DB + Cooling 1% WB; the default `standard="general"` adds Heating 99.6% + Cooling 0.4% DB. Those are the only two presets.

Lower-level access — download a station's DDY, inspect it, and inject selected percentiles into a model:

```python
from idfkit.weather import DesignDayManager, DesignDayType

ddm = DesignDayManager.from_station(station)  # station's own dataset
older = DesignDayManager.from_station(station, dataset="2009-2023")  # another; ValueError lists them if absent
heating = ddm.get(DesignDayType.HEATING_99_6)  # IDFObject | None
cooling = ddm.get(DesignDayType.COOLING_DB_0_4)
added = ddm.apply_to_model(  # injects per the preset args
    doc,
    heating="99.6%",
    cooling="0.4%",
    include_wet_bulb=True,
)
```

`DesignDayType` members include `HEATING_99_6`, `HEATING_99`, `COOLING_DB_0_4`/`_1`/`_2`, `COOLING_WB_*`, `COOLING_ENTH_*`, `DEHUMID_*`, `HUMIDIFICATION_99_6`/`_99`, `HTG_WIND_*`, `WIND_*`. Use `ddm.summary()` to print everything the DDY classifies. `NoDesignDaysError` is raised by `ddm.raise_if_empty()` when a station's DDY contains no usable design days (rare, but possible for incomplete TMYx entries).

## Detecting the user's location

For interactive tooling that wants a sensible default:

```python
from idfkit.weather import detect_location

lat, lon = detect_location()  # IP-based geolocation, best-effort
nearest = StationIndex.load().nearest(lat, lon)[0]
```

## Refreshing the index

The bundled index ages well — TMYx datasets don't change often. To refresh from upstream:

```python
from idfkit.weather import StationIndex

if index.check_for_updates():
    index = StationIndex.refresh()  # re-download + rebuild
```

`refresh()` re-downloads the regional KML index files from climate.onebuilding.org and parses them with the Python standard library; it needs network access and no extra.

## Common mistakes

!!! failure "geocoding in a tight loop"

    ```python
    for addr in addresses:
        lat, lon = geocode(addr)               # Nominatim rate-limits, will start failing
    ```

!!! success "sleep, or pre-compute"

    ```python
    import time

    coords = []
    for addr in addresses:
        coords.append(geocode(addr))
        time.sleep(1.0)
    ```

!!! failure "simulating without design days"

    ```python
    doc = load_idf("building.idf")
    simulate(doc, "weather.epw")               # autosizing fails — no design days in the model
    ```

!!! success "apply design days first"

    ```python
    station = StationIndex.load().search("chicago ohare")[0].station
    apply_ashrae_sizing(doc, station, standard="90.1")
    simulate(doc, "weather.epw")
    ```

!!! failure "assuming `display_name` is unique"

    ```python
    station_by_name = {s.display_name: s for s in index.stations}
    # Collisions when multiple TMYx year-ranges exist for the same WMO ID.
    ```

!!! success "key on `filename_stem` (one per dataset) or `station_key` (one per station)"

    ```python
    station_by_key = {s.filename_stem: s for s in index.stations}  # one entry per dataset
    datasets_by_station = {s.station_key: s for s in index.stations}  # collapses the year ranges
    ```

## Related

- [simulation-execution.md](simulation-execution.md) — passing `weather.epw` to `simulate(...)`.
- [version-migration.md](version-migration.md) — design days from old DDY files may need updating.
- CLI: `idfkit tmy` searches and downloads TMYx files from the shell.
- API docs: [py.idfkit.com/weather/](https://py.idfkit.com/weather/)
