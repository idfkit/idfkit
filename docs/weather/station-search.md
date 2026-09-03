# How to search for weather stations

The `StationIndex` provides fast searching and filtering of ~70,000 weather
station dataset entries (covering ~17,300 unique physical stations) from
climate.onebuilding.org.

{{ parity("weather-index") }}

## How weather is installed

=== "Python"

    Weather comes with the library. `pip install idfkit` installs the station
    index whether or not you asked for it, because a Python extra gates
    dependencies rather than files.

    ```bash
    pip install idfkit
    ```

=== "TypeScript"

    Weather is an opt-in install and the shared name does not reach it. `npm
    install idfkit` places no station index on disk and no weather code in your
    bundle; add the package by name.

    ```bash
    npm install @idfkit/weather
    ```

## Loading the Index

```python
--8<-- "docs/snippets/weather/station-search/loading_the_index.py:example"
```

## Search by Name

Fuzzy text search across station names, cities, and WMO numbers:

```python
--8<-- "docs/snippets/weather/station-search/search_by_name.py:example"
```

### SearchResult Attributes

::: idfkit.weather.SearchResult
    options:
      heading_level: 4
      show_root_heading: false
      show_source: false


### Search Tips

```python
--8<-- "docs/snippets/weather/station-search/search_tips.py:example"
```

## Search by EPW Filename

`search()` automatically detects canonical EPW filenames and resolves them:

```python
--8<-- "docs/snippets/weather/station-search/search_by_filename.py:example"
```

For exact lookups when you know the precise filename, use `get_by_filename()`:

```python
--8<-- "docs/snippets/weather/station-search/get_by_filename.py:example"
```

## Search by Coordinates

Find stations nearest to a location using great-circle distance:

```python
--8<-- "docs/snippets/weather/station-search/search_by_coordinates.py:example"
```

### Function Signature

```python
def nearest(
    self,
    latitude: float,
    longitude: float,
    *,
    limit: int = 5,
    max_distance_km: float | None = None,
    country: str | None = None,
) -> list[SpatialResult]:
```

### SpatialResult Attributes

::: idfkit.weather.SpatialResult
    options:
      heading_level: 4
      show_root_heading: false
      show_source: false


## Search by Address

Combine `geocode()` with `nearest()` for address-based search:

```python
--8<-- "docs/snippets/weather/station-search/search_by_address.py:example"
```

!!! tip "Climate-zone-aware search"
    Each `WeatherStation` carries its ASHRAE HOF climate zone, design
    dry-bulb temperatures, HDD18, and CDD10. See
    [Filter by Climate Zone](#filter-by-climate-zone) below.

## Filter by Country

```python
--8<-- "docs/snippets/weather/station-search/filter_by_country.py:example"
```

## Filter by Coordinates

Use `nearest()` with `max_distance_km` to find stations within a geographic area:

```python
--8<-- "docs/snippets/weather/station-search/filter_by_coordinates.py:example"
```

## Get by WMO Number

```python
--8<-- "docs/snippets/weather/station-search/get_by_wmo_number.py:example"
```

Note: WMO numbers are **not unique** — multiple entries can share a WMO
(different year ranges, data sources).

## WeatherStation Attributes

Every field of [`WeatherStation`][idfkit.weather.WeatherStation], with its type and its default, is in the API reference. It is generated from the source, so it cannot fall behind the way the table that used to sit here did.


The five climate metrics (`ashrae_climate_zone`, the two design DBs,
HDD18, and CDD10) are populated for every station in the bundled index.
`design_conditions_source_wmo` is only set when a station inherits its
design conditions from a neighbouring WMO station; otherwise it is
`None`.

## Filter by Climate Zone

Filter stations by ASHRAE climate zone using a plain list comprehension:

```python
--8<-- "docs/snippets/weather/station-search/filter_by_climate_zone.py:example"
```

## Listing Countries

```python
--8<-- "docs/snippets/weather/station-search/listing_countries.py:example"
```

## Refreshing the Index

The bundled index works without network access. To get the latest data:

```python
--8<-- "docs/snippets/weather/station-search/refreshing_the_index.py:example"
```

Refresh uses the Python standard library only — no third-party packages
required. The same operation is available from the shell as
`idfkit tmy --refresh` — see [`idfkit tmy`](../cli/tmy.md#refresh-the-station-index).

## Performance

The index uses efficient data structures for fast searching:

| Operation | Typical Time |
|-----------|--------------|
| `load()` | ~100ms |
| `search(query)` | ~10ms |
| `nearest(lat, lon)` | ~50ms |
| `filter(country=...)` | ~5ms |

## Best Practices

1. **Load once** — Keep the index in memory for multiple searches
2. **Use spatial search** — More accurate than name matching for locations
3. **Check multiple results** — First result isn't always the best match
4. **Verify WMO** — Same physical station may have multiple entries

## See Also

- [How to download weather files](downloads.md) — Download files for a station
- [How to geocode addresses](geocoding.md) — Convert addresses to coordinates
- [Weather Pipeline](../concepts/weather-pipeline.md) — Architecture details
