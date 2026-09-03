from __future__ import annotations

from idfkit.weather import WeatherDownloader, WeatherStation

downloader: WeatherDownloader = ...  # type: ignore[assignment]
station: WeatherStation = ...  # type: ignore[assignment]
# --8<-- [start:example]
# First download: fetches from internet
files1 = downloader.download(station)

# Second download: instant from cache
files2 = downloader.download(station)

assert files1.epw == files2.epw  # Same cached file
# --8<-- [end:example]
