from __future__ import annotations

from pathlib import Path

from idfkit import IDFDocument
from idfkit.simulation import simulate
from idfkit.weather import StationIndex, WeatherStation

doc: IDFDocument = ...  # type: ignore[assignment]
index: StationIndex = ...  # type: ignore[assignment]
station: WeatherStation = ...  # type: ignore[assignment]
addresses: list[str] = ...  # type: ignore[assignment]

# --8<-- [start:quickstart]
from idfkit.weather import StationIndex, WeatherDownloader

index = StationIndex.load()  # local, instant
results = index.search("chicago ohare")
station = results[0].station

downloader = WeatherDownloader()
files = downloader.download(station)
print(files.epw, files.ddy)
# --8<-- [end:quickstart]


# --8<-- [start:core-api]
from idfkit.weather import (
    StationIndex,  # bundled station index
    WeatherStation,  # a single station
    WeatherDownloader,  # EPW/DDY fetcher with cache
    geocode,  # address → (lat, lon)
    detect_location,  # heuristic IP-based location
    DesignDayManager,  # DDY parser
    DesignDayType,  # ASHRAE 90.1 design conditions
    apply_ashrae_sizing,  # one-call ASHRAE design day injection
)
# --8<-- [end:core-api]


# --8<-- [start:search-name]
index = StationIndex.load()
hits = index.search("chicago ohare")
for hit in hits[:3]:
    print(hit.score, hit.station.display_name)
# --8<-- [end:search-name]


# --8<-- [start:search-address]
from idfkit.weather import StationIndex, geocode

index = StationIndex.load()
lat, lon = geocode("350 Fifth Avenue, New York, NY")
hits = index.nearest(lat, lon)
for hit in hits[:3]:
    print(f"{hit.station.display_name}: {hit.distance_km:.0f} km")

# Or one-liner:
results = index.nearest(*geocode("350 Fifth Avenue, New York, NY"))
# --8<-- [end:search-address]


# --8<-- [start:search-coords]
hits = index.nearest(41.978, -87.904, limit=10)
# --8<-- [end:search-coords]


# --8<-- [start:search-distance]
# All stations within 200 km of a point
hits = index.nearest(41.0, -73.5, max_distance_km=200)
# --8<-- [end:search-distance]


# --8<-- [start:inspect]
station = hits[0].station
station.display_name  # "Chicago O'Hare AP, IL, USA"
station.country  # "USA"
station.state  # "IL"
station.wmo  # "725300" (string, preserves leading zeros)
station.latitude, station.longitude
station.elevation  # metres above sea level
station.timezone  # hours offset from GMT, e.g. -6.0
station.source  # dataset source, e.g. "TMYx.2009-2023"
station.url  # download URL for the ZIP (EPW + DDY)
# --8<-- [end:inspect]


# --8<-- [start:download]
from idfkit.weather import WeatherDownloader

downloader = WeatherDownloader(cache_dir=Path("~/.cache/idfkit/weather").expanduser())
files = downloader.download(station)  # downloads if absent, returns cached path otherwise
files.epw  # Path
files.ddy
files.station
# --8<-- [end:download]


# --8<-- [start:design-days-ashrae]
from idfkit import load_idf
from idfkit.weather import StationIndex, apply_ashrae_sizing

doc = load_idf("building.idf")
station = StationIndex.load().search("chicago ohare")[0].station
added = apply_ashrae_sizing(doc, station, standard="90.1")
print(f"Added {len(added)} design days")
# --8<-- [end:design-days-ashrae]


# --8<-- [start:design-days-lower]
from idfkit.weather import DesignDayManager, DesignDayType

ddm = DesignDayManager.from_station(station)
heating = ddm.get(DesignDayType.HEATING_99_6)  # IDFObject | None
cooling = ddm.get(DesignDayType.COOLING_DB_0_4)
added = ddm.apply_to_model(  # injects per the preset args
    doc,
    heating="99.6%",
    cooling="0.4%",
    include_wet_bulb=True,
)
# --8<-- [end:design-days-lower]


# --8<-- [start:detect-location]
from idfkit.weather import detect_location

lat, lon = detect_location()  # IP-based geolocation, best-effort
nearest = StationIndex.load().nearest(lat, lon)[0]
# --8<-- [end:detect-location]


# --8<-- [start:refresh]
from idfkit.weather import StationIndex

if index.check_for_updates():
    index = StationIndex.refresh()  # re-download + rebuild
# --8<-- [end:refresh]


# --8<-- [start:mistake-geocode-good]
import time

coords = []
for addr in addresses:
    coords.append(geocode(addr))
    time.sleep(1.0)
# --8<-- [end:mistake-geocode-good]


# --8<-- [start:mistake-designday-good]
station = StationIndex.load().search("chicago ohare")[0].station
apply_ashrae_sizing(doc, station, standard="90.1")
simulate(doc, "weather.epw")
# --8<-- [end:mistake-designday-good]


# --8<-- [start:mistake-uniqueness-good]
station_by_key = {(s.wmo, s.source): s for s in index.stations}
# --8<-- [end:mistake-uniqueness-good]
