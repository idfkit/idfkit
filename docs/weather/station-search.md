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

!!! note "No climate-zone filter"
    The upstream index on climate.onebuilding.org does not include climate-zone metadata, so `StationIndex` cannot filter by ASHRAE/Köppen zone. See [Weather Pipeline: No Climate Zone Filter](../concepts/weather-pipeline.md#no-climate-zone-filter) for the workaround.

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
| `source` | `str` | Data source identifier (e.g., "SRC-TMYx") |
| `latitude` | `float` | Station latitude |
| `longitude` | `float` | Station longitude |
| `timezone` | `float` | UTC offset (hours from GMT) |
| `elevation` | `float` | Elevation in meters |
| `url` | `str` | Download URL for weather files |
| `display_name` | `str` | Formatted name (city, state, country) |
| `filename_stem` | `str` | Canonical EPW filename stem from URL |
| `dataset_variant` | `str` | TMYx variant (e.g., "TMYx.2009-2023") |

## Listing Countries

```python
--8<-- "docs/snippets/weather/station-search/listing_countries.py:example"
```

## Refreshing the Index

The bundled index works without network access. To get the latest data:

```python
--8<-- "docs/snippets/weather/station-search/refreshing_the_index.py:example"
```

Refresh requires: `pip install idfkit[weather]`

The same operation is available from the shell as `idfkit tmy --refresh` — see [`idfkit tmy`](../cli/tmy.md#refresh-the-station-index).

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
