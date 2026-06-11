from __future__ import annotations

from idfkit.weather import WeatherDownloader, WeatherStation
from typing import Any

downloader: WeatherDownloader = ...  # type: ignore[assignment]
my_stations: list[Any] = ...  # type: ignore[assignment]
station: WeatherStation = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Pre-download files while online
downloader = WeatherDownloader()
for station in my_stations:
    downloader.download(station)

# Later, offline usage works
files = downloader.download(station)  # From cache
# --8<-- [end:example]
