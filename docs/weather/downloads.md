# Weather Downloads

The `WeatherDownloader` downloads EPW and DDY weather files from
climate.onebuilding.org with automatic caching.

!!! tip "Prefer the shell?"
    The [`idfkit tmy`](../cli/tmy.md) CLI wraps this API for interactive use. Pass `--download DIR` to fetch the EPW/DDY/STAT bundle for a station without writing any Python.

## Basic Usage

```python
--8<-- "docs/snippets/weather/downloads/basic_usage.py:example"
```

## Download by Filename

If you have the canonical EPW filename, download directly without a manual
station lookup:

```python
--8<-- "docs/snippets/weather/downloads/download_by_filename.py:example"
```

## Selective Extraction

By default `download()` extracts the full bundle and requires both an EPW
and a DDY to be present. Pass `only={".epw"}` (or any iterable of suffixes)
to extract just the files you need — useful when you only want the EPW for
an annual run, or when iterating over thousands of stations and you want
to skip the STAT file entirely.

```python
--8<-- "docs/snippets/weather/downloads/selective_extraction.py:example"
```

When `only=` is set, `download()` returns a `PartialWeatherFiles` whose
`epw`, `ddy`, and `stat` fields are each `Path | None` — see below.

## WeatherFiles

The default `download()` call returns a `WeatherFiles` object:

| Attribute | Type | Description |
|-----------|------|-------------|
| `epw` | `Path` | Path to the EPW file |
| `ddy` | `Path` | Path to the DDY file |
| `stat` | <code>Path &#124; None</code> | Path to the STAT file (may be None) |
| `zip_path` | `Path` | Path to the original downloaded ZIP archive |
| `station` | `WeatherStation` | The station this download corresponds to |

```python
--8<-- "docs/snippets/weather/downloads/weatherfiles.py:example"
```

### PartialWeatherFiles

`download(station, only=...)` returns a `PartialWeatherFiles` instead.
Same shape, but `epw`, `ddy`, and `stat` are all optional — only the
suffixes you asked for are populated:

| Attribute | Type | Description |
|-----------|------|-------------|
| `epw` | <code>Path &#124; None</code> | Path to the EPW file, or `None` if not requested |
| `ddy` | <code>Path &#124; None</code> | Path to the DDY file, or `None` if not requested |
| `stat` | <code>Path &#124; None</code> | Path to the STAT file, or `None` if not requested |
| `zip_path` | `Path` | Path to the original downloaded ZIP archive |
| `station` | `WeatherStation` | The station this download corresponds to |

## Caching

Downloaded files are cached locally to avoid redundant downloads:

```python
--8<-- "docs/snippets/weather/downloads/caching.py:example"
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
--8<-- "docs/snippets/weather/downloads/custom_cache_directory.py:example"
```

### Clear Cache

```python
--8<-- "docs/snippets/weather/downloads/clear_cache.py:example"
```

## Download Process

The downloader:

1. Checks if files are already cached
2. Downloads the ZIP file from the station's URL
3. Extracts the requested files (full bundle by default; subset when `only=` is given)
4. Stores in the cache directory
5. Returns paths to the extracted files

## Error Handling

```python
--8<-- "docs/snippets/weather/downloads/error_handling.py:example"
```

Common errors:

- Network connectivity issues
- Invalid station URL
- Server temporarily unavailable

## Offline Usage

Once files are cached, no network is needed:

```python
--8<-- "docs/snippets/weather/downloads/offline_usage.py:example"
```

## Batch Downloads

Download files for multiple stations:

```python
--8<-- "docs/snippets/weather/downloads/batch_downloads.py:example"
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
--8<-- "docs/snippets/weather/downloads/integration_example.py:example"
```

## See Also

- [Station Search](station-search.md) — Find weather stations
- [Design Days](design-days.md) — Apply design day conditions
- [Weather Pipeline](../concepts/weather-pipeline.md) — Architecture details
