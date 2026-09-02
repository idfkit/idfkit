from __future__ import annotations

# --8<-- [start:example]
from idfkit.weather import StationIndex, WeatherDownloader

index = StationIndex.load()  # the bundled index, read from disk
station = index.search("chicago ohare")[0].station

files = WeatherDownloader().download(station)  # served from the warm cache
print(files.epw)
# --8<-- [end:example]
