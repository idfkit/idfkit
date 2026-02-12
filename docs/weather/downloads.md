# Weather Downloads

The `WeatherDownloader` downloads EPW and DDY weather files from
climate.onebuilding.org with automatic caching.

## Basic Usage

```python
--8<-- "docs/snippets/weather/downloads/basic_usage.py:example"
```

## WeatherFiles

The `download()` method returns a `WeatherFiles` object:

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
3. Extracts EPW and DDY files
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
