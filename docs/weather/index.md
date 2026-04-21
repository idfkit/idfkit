# Weather Overview

The weather module provides tools for searching weather stations, downloading
weather files, and applying ASHRAE design day conditions to your models.

## Try It — Interactive Station Browser

The same Leaflet-based UI shipped by `idfkit tmy --browse` is embedded below. Click a marker to inspect a station, or use the filter panel to narrow the ~17,000 entries. [Open in a new tab ↗](browse/index.html)

<iframe
  src="browse/index.html"
  width="100%"
  height="600"
  loading="lazy"
  style="border: 1px solid var(--md-default-fg-color--lightest); border-radius: 4px;"
  title="idfkit tmy station browser">
</iframe>

!!! note "Docs-mode downloads"
    Clicking **Download** in this embed opens the upstream ZIP on climate.onebuilding.org in a new tab. When you run `idfkit tmy --browse` locally, the download flows through idfkit's Python server and lands in the shared cache (`~/Library/Caches/idfkit/weather/files/` on macOS) so the same file is reused by later Python code.

## Quick Start

```python
--8<-- "docs/snippets/weather/index/quick_start.py:example"
```

## Key Features

### 55,000+ Weather Stations

The bundled index contains data from climate.onebuilding.org, covering:

- **~55,000 dataset entries** from 10 world regions
- **~17,300 unique physical stations**
- **248 countries and territories**

### No Network Required

`StationIndex.load()` works instantly without network access — the index
is pre-compiled and bundled with the package.

### Address-Based Search

Find the nearest weather station to any address:

```python
--8<-- "docs/snippets/weather/index/address_based_search.py:example"
```

### ASHRAE Design Days

Apply standard design day conditions to your model:

```python
--8<-- "docs/snippets/weather/index/ashrae_design_days.py:example"
```

## Module Components

| Component | Description |
|-----------|-------------|
| [`StationIndex`](station-search.md) | Search and filter weather stations |
| [`WeatherDownloader`](downloads.md) | Download EPW and DDY files |
| [`DesignDayManager`](design-days.md) | Parse and apply design days |
| [`geocode()`](geocoding.md) | Convert addresses to coordinates |
| [`idfkit tmy`](../cli/tmy.md) | Search, download, and browse TMYx data from the shell |

## Installation

The core weather module requires no extra dependencies:

```python
--8<-- "docs/snippets/weather/index/installation.py:example"
```

To refresh the index from upstream:

```bash
pip install idfkit[weather]  # Adds openpyxl
```

```python
--8<-- "docs/snippets/weather/index/installation_2.py:example"
```

## Workflow Example

Complete workflow from address to simulation-ready model:

```python
--8<-- "docs/snippets/weather/index/workflow_example.py:example"
```

## Data Source

All weather data comes from [climate.onebuilding.org](https://climate.onebuilding.org),
which provides:

- TMYx (Typical Meteorological Year) files
- Multiple year ranges per station (2007-2021, 2009-2023, etc.)
- EPW format for EnergyPlus simulation
- DDY files with ASHRAE design day conditions

## Next Steps

- [Station Search](station-search.md) — Find weather stations
- [Weather Downloads](downloads.md) — Download EPW/DDY files
- [Design Days](design-days.md) — Apply ASHRAE conditions
- [Weather Pipeline Concepts](../concepts/weather-pipeline.md) — Architecture details
