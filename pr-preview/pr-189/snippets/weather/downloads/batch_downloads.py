from __future__ import annotations

from idfkit.weather import StationIndex, WeatherDownloader, WeatherFiles, WeatherStation

downloader: WeatherDownloader = ...  # type: ignore[assignment]
files: WeatherFiles = ...  # type: ignore[assignment]
index: StationIndex = ...  # type: ignore[assignment]
station: WeatherStation = ...  # type: ignore[assignment]
weather_files: dict[str, WeatherFiles] = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.weather import StationIndex, WeatherDownloader

index = StationIndex.load()
downloader = WeatherDownloader()

# Download for multiple cities
cities = ["chicago", "new york", "los angeles", "houston"]
weather_files = {}

for city in cities:
    station = index.search(city)[0].station
    files = downloader.download(station)
    weather_files[city] = files
    print(f"Downloaded: {station.display_name}")
# --8<-- [end:example]
