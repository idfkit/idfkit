from __future__ import annotations

from idfkit import IDFDocument
from idfkit.weather import WeatherDownloader, WeatherFiles, WeatherStation

downloader: WeatherDownloader = ...  # type: ignore[assignment]
files: WeatherFiles = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
station: WeatherStation = ...  # type: ignore[assignment]
# --8<-- [start:example]
files = downloader.download(station)

# Use for simulation
from idfkit.simulation import simulate

result = simulate(model, files.epw)

# Use for design days
from idfkit.weather import DesignDayManager

ddm = DesignDayManager(files.ddy)
# --8<-- [end:example]
