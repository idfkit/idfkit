from __future__ import annotations

from idfkit.weather import StationIndex, WeatherDownloader, WeatherFiles, WeatherStation

downloader: WeatherDownloader = ...  # type: ignore[assignment]
files: WeatherFiles = ...  # type: ignore[assignment]
index: StationIndex = ...  # type: ignore[assignment]
station: WeatherStation = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.weather import StationIndex, WeatherDownloader

# Find a station
index = StationIndex.load()
station = index.search("chicago ohare")[0].station

# Download weather files
downloader = WeatherDownloader()
files = downloader.download(station)

print(f"EPW: {files.epw}")
print(f"DDY: {files.ddy}")
# --8<-- [end:example]
