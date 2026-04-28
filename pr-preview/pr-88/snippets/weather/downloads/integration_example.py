from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult
from idfkit.weather import DesignDayManager, StationIndex, WeatherDownloader, WeatherFiles, WeatherStation

ddm: DesignDayManager = ...  # type: ignore[assignment]
downloader: WeatherDownloader = ...  # type: ignore[assignment]
files: WeatherFiles = ...  # type: ignore[assignment]
index: StationIndex = ...  # type: ignore[assignment]
lat: float = ...  # type: ignore[assignment]
lon: float = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
station: WeatherStation = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit import load_idf
from idfkit.weather import (
    StationIndex,
    WeatherDownloader,
    DesignDayManager,
    geocode,
)
from idfkit.simulation import simulate

# Load model
model = load_idf("building.idf")

# Find station near project site
index = StationIndex.load()
lat, lon = geocode("123 Main St, Chicago, IL")
station = index.nearest(lat, lon)[0].station

# Download weather files
downloader = WeatherDownloader()
files = downloader.download(station)

# Apply design days
ddm = DesignDayManager(files.ddy)
ddm.apply_to_model(model, heating="99.6%", cooling="1%")

# Run simulation
result = simulate(model, files.epw, design_day=True)
print(f"Success: {result.success}")
# --8<-- [end:example]
