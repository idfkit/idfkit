# Station Search

The `StationIndex` provides fast searching and filtering of 55,000+ weather
station entries from climate.onebuilding.org.

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

| Attribute | Type | Description |
|-----------|------|-------------|
| `station` | `WeatherStation` | The matching station |
| `score` | `float` | Match score (0.0 to 1.0) |

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

| Attribute | Type | Description |
|-----------|------|-------------|
| `station` | `WeatherStation` | The nearby station |
| `distance_km` | `float` | Distance in kilometers |

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

| Attribute | Type | Description |
|-----------|------|-------------|
| `city` | `str` | City/station name |
| `state` | `str` | State/province/region |
| `country` | `str` | Country name |
| `wmo` | `str` | WMO station number |
| `source` | `str` | Dataset source identifier (e.g., `"TMYx.2009-2023"`) |
| `latitude` | `float` | Station latitude |
| `longitude` | `float` | Station longitude |
| `timezone` | `float` | UTC offset (hours from GMT) |
| `elevation` | `float` | Elevation in meters |
| `url` | `str` | Download URL for weather files |
| `ashrae_climate_zone` | `str` | ASHRAE HOF climate zone (e.g., `"4A - Mixed - Humid"`) |
| `heating_design_db_c` | `float` | 99% heating design dry-bulb temperature (°C) |
| `cooling_design_db_c` | `float` | 1% cooling design dry-bulb temperature (°C) |
| `heating_design_db_f` | `float` | 99% heating design dry-bulb temperature (°F, computed) |
| `cooling_design_db_f` | `float` | 1% cooling design dry-bulb temperature (°F, computed) |
| `hdd18` | `int` | Heating degree-days, base 18 °C |
| `cdd10` | `int` | Cooling degree-days, base 10 °C |
| `design_conditions_source_wmo` | `str \| None` | WMO of a neighbouring station whose design conditions are inherited; `None` for stations with their own design data |
| `display_name` | `str` | Formatted name (city, state, country) |
| `filename_stem` | `str` | Canonical EPW filename stem from URL |
| `dataset_variant` | `str` | TMYx variant (e.g., `"TMYx.2009-2023"`) |

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

- [Weather Downloads](downloads.md) — Download files for a station
- [Geocoding](geocoding.md) — Convert addresses to coordinates
- [Weather Pipeline](../concepts/weather-pipeline.md) — Architecture details
