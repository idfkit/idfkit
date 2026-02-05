# Weather API Overview

The weather module provides station search, file downloads, and design day management.

## Quick Reference

| Class/Function | Description |
|---------------|-------------|
| [`StationIndex`](station.md) | Weather station search and filtering |
| [`WeatherStation`](station.md) | Station metadata container |
| [`WeatherDownloader`](download.md) | EPW/DDY file downloads |
| [`WeatherFiles`](download.md) | Downloaded file paths |
| [`DesignDayManager`](designday.md) | Design day parsing and injection |
| [`DesignDayType`](designday.md) | Design day type enumeration |
| [`apply_ashrae_sizing()`](designday.md) | Quick design day application |
| [`geocode()`](station.md) | Address to coordinates |

## Module Contents

::: idfkit.weather
    options:
      show_root_heading: false
      show_source: false
      members_order: source
      filters:
        - "!^_"
