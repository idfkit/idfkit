# Weather Data Pipeline

This page explains how idfkit's weather module works and the concepts
behind weather station data and design days.

## Data Source: climate.onebuilding.org

idfkit's weather station index is built from the **climate.onebuilding.org**
TMYx weather file collection. This is the most comprehensive free source
of EnergyPlus weather files, containing:

- **~55,000 dataset entries** from 10 world regions
- **~17,300 unique physical weather stations**
- Coverage of **248 countries and territories**

The difference between entries and stations exists because each physical
station may have multiple TMYx year-range variants (e.g., `TMYx.2007-2021`,
`TMYx.2009-2023`), each stored as a separate entry with its own download URL.

## Station Index Architecture

The `StationIndex` provides two modes of operation:

### Bundled Index (No Dependencies)

`StationIndex.load()` loads a **pre-compiled index** bundled with the package:

```python
from idfkit.weather import StationIndex

index = StationIndex.load()  # Instant, no network
print(f"{len(index)} entries, {len(index.countries)} countries")
```

This works without any extra dependencies or network access.

### Live Refresh (Requires openpyxl)

`StationIndex.refresh()` downloads the **latest Excel indexes** from
climate.onebuilding.org and rebuilds the index:

```python
# Check if upstream data has changed
if index.check_for_updates():
    index = StationIndex.refresh()  # Downloads ~10 Excel files
```

This requires the `openpyxl` package (`pip install idfkit[weather]`).

## Station vs Entry

Understanding the distinction:

| Concept | Description |
|---------|-------------|
| **Station** | A physical weather monitoring location (e.g., Chicago O'Hare) |
| **Entry** | A specific TMYx dataset for a station (e.g., TMYx.2007-2021) |

A single station often has multiple entries with different year ranges.
When searching, results include all matching entries. Use the station's
`wmo` number to identify the same physical location across entries.

## WMO Numbers

WMO (World Meteorological Organization) numbers identify weather stations
internationally. Important notes:

- WMO numbers are **not unique per station** — multiple stations can share one
- Use `display_name` for human-readable identification
- Use `url` for the exact dataset you want to download

```python
# Multiple entries can have the same WMO
results = index.search("725300")  # Chicago O'Hare WMO
for r in results:
    print(f"{r.station.source_data}: {r.station.url}")
```

## Spatial Search

The `nearest()` method uses the **Haversine formula** for great-circle
distance calculations:

```python
# Find nearest stations to a coordinate
results = index.nearest(41.88, -87.63, limit=5)

for r in results:
    print(f"{r.station.display_name}: {r.distance_km:.1f} km")
```

Combine with `geocode()` for address-based lookups:

```python
from idfkit.weather import geocode

lat, lon = geocode("350 Fifth Avenue, New York, NY")
results = index.nearest(lat, lon)
```

## Design Day Classification

DDY files contain `SizingPeriod:DesignDay` objects using ASHRAE naming
conventions. The `DesignDayManager` parses these and classifies each
design day by type:

| Type | Pattern | Example |
|------|---------|---------|
| `HEATING_99_6` | `Htg 99.6% Condns DB` | Chicago Ann Htg 99.6% Condns DB |
| `HEATING_99` | `Htg 99% Condns DB` | Chicago Ann Htg 99% Condns DB |
| `COOLING_DB_0_4` | `Clg .4% Condns DB=>MWB` | Chicago Ann Clg .4% Condns DB=>MWB |
| `COOLING_DB_1` | `Clg 1% Condns DB=>MWB` | Chicago Ann Clg 1% Condns DB=>MWB |
| `COOLING_WB_1` | `Clg 1% Condns WB=>MDB` | Chicago Ann Clg 1% Condns WB=>MDB |

Real DDY files typically contain **114+ design days**:

- 18 annual design days (heating, cooling, dehumidification, etc.)
- 96 monthly design days (12 months × 4 percentiles × 2 types)

## ASHRAE Standards

Different ASHRAE standards recommend different design day percentiles:

| Standard | Heating | Cooling |
|----------|---------|---------|
| **ASHRAE 90.1** | 99.6% | 1% |
| **ASHRAE 62.1** | 99% | 1% |

Use `apply_to_model()` or `apply_ashrae_sizing()` with the appropriate
percentiles:

```python
from idfkit.weather import DesignDayManager

ddm = DesignDayManager("chicago.ddy")

# ASHRAE 90.1 (stricter heating condition)
ddm.apply_to_model(model, heating="99.6%", cooling="1%")

# Or use the convenience function with standard presets
from idfkit.weather import apply_ashrae_sizing
apply_ashrae_sizing(model, station, standard="90.1")
```

## Caching

Weather data is cached to avoid redundant downloads:

| Data | Cache Location | Lifetime |
|------|----------------|----------|
| Station indexes | `~/.cache/idfkit/weather/indexes/` | Until refresh |
| Weather files (EPW, DDY) | `~/.cache/idfkit/weather/files/` | Permanent |

The cache location follows platform conventions:

- **Linux**: `~/.cache/idfkit/`
- **macOS**: `~/Library/Caches/idfkit/`
- **Windows**: `%LOCALAPPDATA%\idfkit\cache\`

## See Also

- [Station Search](../weather/station-search.md) — Practical search guide
- [Design Days](../weather/design-days.md) — Applying design days to models
- [Caching Strategy](caching.md) — General caching architecture
