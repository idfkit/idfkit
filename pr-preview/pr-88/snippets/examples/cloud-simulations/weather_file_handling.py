from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import S3FileSystem, simulate
from idfkit.weather import StationIndex, WeatherDownloader, WeatherFiles, WeatherStation

downloader: WeatherDownloader = ...  # type: ignore[assignment]
files: WeatherFiles = ...  # type: ignore[assignment]
fs: S3FileSystem = ...  # type: ignore[assignment]
index: StationIndex = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
station: WeatherStation = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.weather import StationIndex, WeatherDownloader

# Download weather file locally
index = StationIndex.load()
station = index.search("chicago")[0].station
downloader = WeatherDownloader()
files = downloader.download(station)

# Then use local weather with S3 output
fs = S3FileSystem(bucket="results", prefix="study/")
result = simulate(
    model,
    files.epw,  # Local path
    output_dir="run-001",
    fs=fs,
)
# --8<-- [end:example]
