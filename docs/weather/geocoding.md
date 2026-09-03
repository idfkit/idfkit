# How to geocode addresses

The weather module provides two ways to resolve coordinates without
hard-coding them:

- [`geocode(address)`](#basic-usage) — convert a known street address to
  `(lat, lon)` via the free Nominatim (OpenStreetMap) service.
- [`detect_location()`](#detect-location-from-ip) — auto-detect the
  current machine's approximate coordinates from its public IP.

Both return a `(latitude, longitude)` tuple and raise `GeocodingError` on
failure, so they compose interchangeably with
[`StationIndex.nearest()`](station-search.md).

{{ parity("geocoding") }}

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

## Basic Usage

```python
--8<-- "docs/snippets/weather/geocoding/basic_usage.py:example"
```

## With Station Search

Combine with `StationIndex.nearest()` for address-based weather station lookup:

```python
--8<-- "docs/snippets/weather/geocoding/with_station_search.py:example"
```

## Address Formats

The geocoder accepts various address formats:

```python
--8<-- "docs/snippets/weather/geocoding/address_formats.py:example"
```

## Error Handling

```python
--8<-- "docs/snippets/weather/geocoding/error_handling.py:example"
```

### Common Errors

| Situation | Behavior |
|-----------|----------|
| Address not found | Raises `GeocodingError` |
| Network error | Raises `GeocodingError` |
| Rate limiting | Avoided — calls are serialized to ≤1 request/second |

## Rate Limiting

The free Nominatim service allows at most one request per second. `geocode()`
serializes calls to honour that limit for you, so you don't have to throttle
calls yourself:

```python
--8<-- "docs/snippets/weather/geocoding/rate_limiting.py:example"
```

For bulk geocoding, and for why the limit exists, see
[About geocoding and IP-based location](../explanation/geocoding.md).

## Caching Results

For repeated lookups, cache the coordinates:

```python
--8<-- "docs/snippets/weather/geocoding/caching_results.py:example"
```

## Complete Workflow

```python
--8<-- "docs/snippets/weather/geocoding/complete_workflow.py:example"
```

## Alternative: Direct Coordinates

If you already know the coordinates, skip geocoding entirely:

```python
--8<-- "docs/snippets/weather/geocoding/alternative_direct_coordinates.py:example"
```

## Detect Location from IP

`detect_location()` resolves the running machine's approximate
coordinates from its public IP, so callers don't need to know or supply
an address. It's the "weather stations near me" companion to `geocode()`.

```python
--8<-- "docs/snippets/weather/geocoding/detect_location_basic.py:example"
```

### Combining with Station Search

Like `geocode()`, the result splats directly into
[`StationIndex.nearest()`](station-search.md):

```python
--8<-- "docs/snippets/weather/geocoding/detect_location_with_station_search.py:example"
```

The same flow is exposed on the CLI as
[`idfkit tmy --nearby`](../cli/tmy.md#detect-location-from-ip-nearby).

### Caching

Calls hit `ipapi.co` over HTTPS and the result is cached on disk for
**1 hour** by default. Repeated calls within that window return the
cached value with no network access. The cache file lives under the same
platform cache directory used by `WeatherDownloader` (e.g.
`~/.cache/idfkit/weather/ipgeo.json` on Linux), and the TTL and location
are both configurable:

```python
--8<-- "docs/snippets/weather/geocoding/detect_location_caching.py:example"
```

### Error Handling

`detect_location()` raises [`GeocodingError`][idfkit.weather.geocode.GeocodingError]
on any failure — network outage, ipapi.co rate limit, or an
unlocatable IP (e.g. some VPNs):

```python
--8<-- "docs/snippets/weather/geocoding/detect_location_error_handling.py:example"
```

Accuracy is city-level and the call discloses your public IP; see
[About geocoding and IP-based location](../explanation/geocoding.md) for what
that means and how to avoid it.

## See Also

- [About geocoding and IP-based location](../explanation/geocoding.md) — service limits, accuracy, and privacy
- [How to search for weather stations](station-search.md) — Find weather stations
- [How to download weather files](downloads.md) — Download weather files
- [Weather Overview](index.md) — Module overview
- [`idfkit tmy --nearby`](../cli/tmy.md#detect-location-from-ip-nearby) — CLI shortcut around `detect_location()`
