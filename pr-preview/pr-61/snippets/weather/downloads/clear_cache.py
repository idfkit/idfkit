from __future__ import annotations

from idfkit.weather import WeatherDownloader

downloader: WeatherDownloader = ...  # type: ignore[assignment]
# --8<-- [start:example]
import shutil

shutil.rmtree(downloader.cache_dir)
# --8<-- [end:example]
