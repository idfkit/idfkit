# Geocoding

The `geocode()` function converts addresses to coordinates using the free
Nominatim (OpenStreetMap) service.

## Basic Usage

```python
from idfkit.weather import geocode

# Get coordinates for an address
lat, lon = geocode("350 Fifth Avenue, New York, NY")
print(f"Empire State Building: {lat:.4f}, {lon:.4f}")
```

## With Station Search

Combine with `StationIndex.nearest()` for address-based weather station lookup:

```python
from idfkit.weather import StationIndex, geocode

index = StationIndex.load()

# One-liner using splat operator
results = index.nearest(*geocode("Willis Tower, Chicago, IL"))

# First result is the nearest station
station = results[0].station
print(f"Nearest: {station.display_name} ({results[0].distance_km:.1f} km)")
```

## Address Formats

The geocoder accepts various address formats:

```python
# Full address
lat, lon = geocode("123 Main Street, Springfield, IL 62701")

# Landmark
lat, lon = geocode("Eiffel Tower, Paris")

# City only
lat, lon = geocode("Tokyo, Japan")

# Partial address
lat, lon = geocode("Times Square, New York")
```

## Error Handling

```python
from idfkit.weather import geocode, GeocodingError

try:
    lat, lon = geocode("Nonexistent Place XYZ123")
except GeocodingError as e:
    print(f"Geocoding failed: {e}")
```

### Common Errors

| Situation | Behavior |
|-----------|----------|
| Address not found | Raises `GeocodingError` |
| Network error | Raises `GeocodingError` |
| Rate limited | Automatically retries with delay |

## Rate Limiting

Nominatim requires a maximum of 1 request per second. The `geocode()`
function automatically handles rate limiting:

```python
# These are automatically spaced 1 second apart
for address in addresses:
    lat, lon = geocode(address)  # Rate limited internally
    print(f"{address}: {lat:.2f}, {lon:.2f}")
```

## No API Key Required

Nominatim is a free service that doesn't require an API key. However:

- Be respectful of usage limits
- Avoid bulk geocoding (use batch geocoding services for large datasets)
- Cache results when possible

## Caching Results

For repeated lookups, cache the coordinates:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_geocode(address: str) -> tuple[float, float]:
    return geocode(address)

# Subsequent calls are instant
lat, lon = cached_geocode("123 Main St")
lat, lon = cached_geocode("123 Main St")  # From cache
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
from idfkit.simulation import simulate

# Project location
project_address = "1600 Pennsylvania Avenue, Washington, DC"

# Find nearest weather station
index = StationIndex.load()
lat, lon = geocode(project_address)
results = index.nearest(lat, lon)

station = results[0].station
print(f"Project location: {lat:.4f}, {lon:.4f}")
print(f"Nearest station: {station.display_name} ({results[0].distance_km:.1f} km)")

# Download weather data
downloader = WeatherDownloader()
files = downloader.download(station)

# Load model and apply design days
model = load_idf("building.idf")
ddm = DesignDayManager(files.ddy)
ddm.apply_to_model(model, heating="99.6%", cooling="1%", update_location=True)

# Run simulation
result = simulate(model, files.epw, design_day=True)
```

## Accuracy Notes

- Geocoding accuracy varies by location and address specificity
- Results may vary slightly over time as OpenStreetMap data is updated
- For critical applications, verify coordinates manually

## Alternative: Direct Coordinates

If you already know the coordinates, skip geocoding entirely:

```python
# Direct coordinate lookup
results = index.nearest(40.7484, -73.9857)  # Empire State Building
```

## See Also

- [Station Search](station-search.md) — Find weather stations
- [Weather Downloads](downloads.md) — Download weather files
- [Weather Overview](index.md) — Module overview
