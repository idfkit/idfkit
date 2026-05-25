# Weather data

`idfkit.weather` provides everything you need to attach realistic weather to a model: a bundled index of ~55,000 climate.onebuilding.org TMYx datasets across ~17,300 unique physical stations, an EPW/DDY downloader with local caching, ASHRAE design-day injection, and a Nominatim-backed geocoder.

## When to use

- You need an `.epw` weather file for a simulation.
- You're picking the nearest weather station to a building site (by name, address, or coordinates).
- You need to inject sizing design days into a model so EnergyPlus can autosize HVAC.
- You're building a batch over multiple climates.

## Quick start

```python
--8<-- "docs/snippets/agent_references/weather-data.py:quickstart"
```

## Core API

```python
--8<-- "docs/snippets/agent_references/weather-data.py:core-api"
```

## Searching for a station

### By name (fuzzy)

```python
--8<-- "docs/snippets/agent_references/weather-data.py:search-name"
```

`search` is whitespace-tokenised and case-insensitive. Use it for "I know roughly what the station is called."

### By address (geocode + nearest)

```python
--8<-- "docs/snippets/agent_references/weather-data.py:search-address"
```

`geocode` uses Nominatim (OpenStreetMap) — no API key, but rate-limited to 1 req/second. For batch geocoding, sleep between calls or pre-compute.

### By coordinates

```python
--8<-- "docs/snippets/agent_references/weather-data.py:search-coords"
```

### By distance

```python
--8<-- "docs/snippets/agent_references/weather-data.py:search-distance"
```

## Inspecting a station

```python
--8<-- "docs/snippets/agent_references/weather-data.py:inspect"
```

Multiple `WeatherStation` entries can share the same `wmo` — each TMYx year-range variant is a separate entry.

## Downloading EPW + DDY

```python
--8<-- "docs/snippets/agent_references/weather-data.py:download"
```

`WeatherDownloader` is idempotent — repeated `download()` calls hit the cache. To force re-download, pass `force=True`.

The cache directory defaults to `$XDG_CACHE_HOME/idfkit/weather` on Linux, `~/Library/Caches/idfkit/weather` on macOS, and `%LOCALAPPDATA%\idfkit\weather` on Windows.

## Design days

EnergyPlus autosizes HVAC equipment from "design day" conditions (typical hottest hour, typical coldest hour, etc.). They live in DDY files; `apply_ashrae_sizing` injects them into your model in one call:

```python
--8<-- "docs/snippets/agent_references/weather-data.py:design-days-ashrae"
```

`standard="90.1"` adds Heating 99.6% + Cooling 1% DB + Cooling 1% WB; the default `standard="general"` adds Heating 99.6% + Cooling 0.4% DB. Those are the only two presets.

Lower-level access — download a station's DDY, inspect it, and inject selected percentiles into a model:

```python
--8<-- "docs/snippets/agent_references/weather-data.py:design-days-lower"
```

`DesignDayType` members include `HEATING_99_6`, `HEATING_99`, `COOLING_DB_0_4`/`_1`/`_2`, `COOLING_WB_*`, `COOLING_ENTH_*`, `DEHUMID_*`, `HUMIDIFICATION_99_6`/`_99`, `HTG_WIND_*`, `WIND_*`. Use `ddm.summary()` to print everything the DDY classifies. `NoDesignDaysError` is raised by `ddm.raise_if_empty()` when a station's DDY contains no usable design days (rare, but possible for incomplete TMYx entries).

## Detecting the user's location

For interactive tooling that wants a sensible default:

```python
--8<-- "docs/snippets/agent_references/weather-data.py:detect-location"
```

## Refreshing the index

The bundled index ages well — TMYx datasets don't change often. To refresh from upstream:

```python
--8<-- "docs/snippets/agent_references/weather-data.py:refresh"
```

`refresh()` requires `idfkit[weather]` for the openpyxl extra (TMYx publishes the catalogue as `.xlsx`).

## Common mistakes

!!! failure "geocoding in a tight loop"

    ```python
    for addr in addresses:
        lat, lon = geocode(addr)               # Nominatim rate-limits, will start failing
    ```

!!! success "sleep, or pre-compute"

    ```python
    --8<-- "docs/snippets/agent_references/weather-data.py:mistake-geocode-good"
    ```

!!! failure "simulating without design days"

    ```python
    doc = load_idf("building.idf")
    simulate(doc, "weather.epw")               # autosizing fails — no design days in the model
    ```

!!! success "apply design days first"

    ```python
    --8<-- "docs/snippets/agent_references/weather-data.py:mistake-designday-good"
    ```

!!! failure "assuming `display_name` is unique"

    ```python
    station_by_name = {s.display_name: s for s in index.stations}
    # Collisions when multiple TMYx year-ranges exist for the same WMO ID.
    ```

!!! success "key on `(wmo, source)` if you need uniqueness"

    ```python
    --8<-- "docs/snippets/agent_references/weather-data.py:mistake-uniqueness-good"
    ```

## Related

- [simulation-execution.md](simulation-execution.md) — passing `weather.epw` to `simulate(...)`.
- [version-migration.md](version-migration.md) — design days from old DDY files may need updating.
- CLI: `idfkit tmy` searches and downloads TMYx files from the shell.
- API docs: [py.idfkit.com/weather/](https://py.idfkit.com/weather/)
