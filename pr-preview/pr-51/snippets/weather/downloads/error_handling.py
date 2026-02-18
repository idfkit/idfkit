from __future__ import annotations

from idfkit.weather import WeatherDownloader, WeatherStation

downloader: WeatherDownloader = ...  # type: ignore[assignment]
station: WeatherStation = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.weather import WeatherDownloader

downloader = WeatherDownloader()

try:
    files = downloader.download(station)
except Exception as e:
    print(f"Download failed: {e}")
# --8<-- [end:example]
