# Station Search

The `StationIndex` provides fast searching and filtering of 55,000+ weather
station entries from climate.onebuilding.org.

## Loading the Index

```python
from idfkit.weather import StationIndex

# Instant load from bundled data (no network needed)
index = StationIndex.load()

print(f"Stations: {len(index)}")
print(f"Countries: {len(index.countries)}")
```

## Search by Name

Fuzzy text search across station names, cities, and WMO numbers:

```python
# Search by name
results = index.search("chicago ohare")

for r in results[:5]:
    print(f"{r.station.display_name} (score={r.score:.2f})")
```

### SearchResult Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `station` | `WeatherStation` | The matching station |
| `score` | `float` | Match score (0.0 to 1.0) |

### Search Tips

```python
# City name
results = index.search("New York")

# Airport code pattern
results = index.search("JFK")

# WMO number
results = index.search("725300")

# Country + city
results = index.search("London UK")
```

## Search by Coordinates

Find stations nearest to a location using great-circle distance:

```python
# Nearest to downtown Chicago
results = index.nearest(41.88, -87.63)

for r in results[:5]:
    print(f"{r.station.display_name}: {r.distance_km:.1f} km")
```

### Function Signature

```python
def nearest(
    self,
    latitude: float,
    longitude: float,
    limit: int = 10,
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
from idfkit.weather import StationIndex, geocode

index = StationIndex.load()

# One-liner using splat operator
results = index.nearest(*geocode("Willis Tower, Chicago, IL"))

# Or step by step
lat, lon = geocode("350 Fifth Avenue, New York, NY")
results = index.nearest(lat, lon)
```

## Filter by Country

```python
# Get all stations in a country
us_stations = index.filter(country="USA")
print(f"US stations: {len(us_stations)}")

# Get all stations in a state/region
california = [s for s in us_stations if s.state == "CA"]
```

## Filter by Coordinates

```python
# Bounding box filter
stations = index.filter(
    lat_min=40.0,
    lat_max=42.0,
    lon_min=-90.0,
    lon_max=-87.0,
)
```

## Get by WMO Number

```python
# Get specific station by WMO
results = index.get_by_wmo("725300")

for station in results:
    print(f"{station.display_name}: {station.source_data}")
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
| `source_data` | `str` | Data source (e.g., "TMYx.2009-2023") |
| `latitude` | `float` | Station latitude |
| `longitude` | `float` | Station longitude |
| `time_zone` | `float` | UTC offset |
| `elevation` | `float` | Elevation in meters |
| `url` | `str` | Download URL for weather files |
| `display_name` | `str` | Formatted name (city, state, country) |

## Listing Countries

```python
# Get all available countries
countries = index.countries

for country in sorted(countries)[:10]:
    count = len(index.filter(country=country))
    print(f"{country}: {count} stations")
```

## Refreshing the Index

The bundled index works without network access. To get the latest data:

```python
# Check if upstream has updates
if index.check_for_updates():
    print("Updates available")

    # Refresh from climate.onebuilding.org (requires openpyxl)
    index = StationIndex.refresh()
```

Refresh requires: `pip install idfkit[weather]`

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
