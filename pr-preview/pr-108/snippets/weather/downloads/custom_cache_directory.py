from __future__ import annotations

from idfkit.weather import WeatherDownloader

# --8<-- [start:example]
from pathlib import Path

downloader = WeatherDownloader(cache_dir=Path("/data/weather_cache"))
# --8<-- [end:example]
