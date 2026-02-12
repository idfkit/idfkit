from __future__ import annotations

from idfkit import IDFDocument, IDFObject
from idfkit.weather import DesignDayManager, StationIndex, WeatherDownloader, WeatherFiles, WeatherStation

added: list[IDFObject] = ...  # type: ignore[assignment]
ddm: DesignDayManager = ...  # type: ignore[assignment]
downloader: WeatherDownloader = ...  # type: ignore[assignment]
files: WeatherFiles = ...  # type: ignore[assignment]
index: StationIndex = ...  # type: ignore[assignment]
lat: float = ...  # type: ignore[assignment]
lon: float = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
station: WeatherStation = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit import load_idf
from idfkit.weather import (
    StationIndex,
    WeatherDownloader,
    DesignDayManager,
    geocode,
)

# Load model
model = load_idf("building.idf")

# Find nearest station
index = StationIndex.load()
lat, lon = geocode("123 Main St, Chicago, IL")
station = index.nearest(lat, lon)[0].station

# Download weather files
downloader = WeatherDownloader()
files = downloader.download(station)

# Apply design days
ddm = DesignDayManager(files.ddy)
added = ddm.apply_to_model(
    model,
    heating="99.6%",
    cooling="1%",
    include_wet_bulb=True,
    update_location=True,
)

print(f"Added {len(added)} design days")
print(f"Location: {model['Site:Location'].values()[0].name}")
# --8<-- [end:example]
