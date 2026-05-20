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
results: list[SimulationResult | None] = ...  # type: ignore[assignment]
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

# Project location
project_address = "1600 Pennsylvania Avenue, Washington, DC"

# Find nearest weather station
index = StationIndex.load()
lat, lon = geocode(project_address)
results = index.nearest(lat, lon)

station = results[0].station
print(f"Project location: {lat:.4f}, {lon:.4f}")
print(f"Nearest station: {station.display_name} ({results[0].distance_km:.1f} km)")

# Download weather data
downloader = WeatherDownloader()
files = downloader.download(station)

# Load model and apply design days
model = load_idf("building.idf")
ddm = DesignDayManager(files.ddy)
ddm.apply_to_model(model, heating="99.6%", cooling="1%", update_location=True)

# Run simulation
result = simulate(model, files.epw, design_day=True)
# --8<-- [end:example]
