"""Weather station search, download, and design day injection.

This sub-package provides tools for:

* **Searching** the climate.onebuilding.org TMYx station index by name,
  coordinates, or metadata filters.
* **Downloading** EPW and DDY weather files with local caching.
* **Parsing** DDY files and injecting ASHRAE design day conditions into
  EnergyPlus models.
* **Geocoding** addresses to coordinates via the free Nominatim API.

Station Index
-------------

The bundled index contains **~55,000 dataset entries** representing
**~17,300 unique physical weather stations** worldwide. The difference
is because each station may have multiple TMYx year-range variants
(e.g., ``TMYx.2007-2021``, ``TMYx.2009-2023``), each stored as a
separate entry with its own download URL.

Quick Start
-----------

Search by name::

    from idfkit.weather import StationIndex, WeatherDownloader

    index = StationIndex.load()  # Instant, no network needed
    results = index.search("chicago ohare")
    station = results[0].station

    downloader = WeatherDownloader()
    files = downloader.download(station)
    print(files.epw, files.ddy)

Search by Address (Splat Pattern)
---------------------------------

Combine :func:`geocode` with :meth:`~StationIndex.nearest` using the splat
operator to find weather stations near any address::

    from idfkit.weather import StationIndex, geocode

    index = StationIndex.load()

    # Find stations near an address (one line!)
    results = index.nearest(*geocode("350 Fifth Avenue, New York, NY"))

    for r in results[:3]:
        print(f"{r.station.display_name}: {r.distance_km:.0f} km")

    # Output:
    # New York La Guardia AP, NY, USA: 10 km
    # New York J F Kennedy Intl AP, NY, USA: 18 km
    # Newark Liberty Intl AP, NJ, USA: 22 km

The :func:`geocode` function uses the free Nominatim (OpenStreetMap) service,
which requires no API key. Requests are rate-limited to 1 per second.

Apply Design Days
-----------------

Inject ASHRAE sizing design days into your model::

    from idfkit import load_idf
    from idfkit.weather import StationIndex, apply_ashrae_sizing

    model = load_idf("building.idf")
    station = StationIndex.load().search("chicago ohare")[0].station

    # Apply ASHRAE 90.1 design conditions
    added = apply_ashrae_sizing(model, station, standard="90.1")
    print(f"Added {len(added)} design days")

Index Freshness
---------------

``StationIndex.load()`` is purely local and requires no extra dependencies.
Use ``StationIndex.refresh()`` (requires ``openpyxl``) to re-download the
upstream Excel indexes and rebuild the local cache::

    if index.check_for_updates():
        index = StationIndex.refresh()  # requires openpyxl
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
