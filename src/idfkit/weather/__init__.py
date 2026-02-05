"""Weather station search, download, and design day injection.

This sub-package provides tools for:

* **Searching** the climate.onebuilding.org TMYx station index by name,
  coordinates, or metadata filters.
* **Downloading** EPW and DDY weather files with local caching.
* **Parsing** DDY files and injecting ASHRAE design day conditions into
  EnergyPlus models.
* **Geocoding** addresses to coordinates via the free Nominatim API.

Quick start::

    from idfkit.weather import StationIndex, WeatherDownloader, apply_ashrae_sizing

    # Instant — loads from bundled index, no network or openpyxl needed
    index = StationIndex.load()
    results = index.search("chicago ohare")
    station = results[0].station

    # Optional: check if upstream data has changed
    if index.check_for_updates():
        index = StationIndex.refresh()   # requires openpyxl

    downloader = WeatherDownloader()
    files = downloader.download(station)
    print(files.epw, files.ddy)

``StationIndex.load()`` is purely local and requires no extra dependencies.
Use ``StationIndex.refresh()`` (requires ``openpyxl``) to re-download the
upstream Excel indexes and rebuild the local cache.
"""

from __future__ import annotations

from ..exceptions import NoDesignDaysError
from .designday import DesignDayManager, DesignDayType, apply_ashrae_sizing
from .download import WeatherDownloader, WeatherFiles
from .geocode import GeocodingError, geocode
from .index import StationIndex
from .station import SearchResult, SpatialResult, WeatherStation

__all__ = [
    "DesignDayManager",
    "DesignDayType",
    "GeocodingError",
    "NoDesignDaysError",
    "SearchResult",
    "SpatialResult",
    "StationIndex",
    "WeatherDownloader",
    "WeatherFiles",
    "WeatherStation",
    "apply_ashrae_sizing",
    "geocode",
]
