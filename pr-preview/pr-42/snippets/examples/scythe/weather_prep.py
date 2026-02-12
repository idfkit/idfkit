from __future__ import annotations

# --8<-- [start:example]
from idfkit.weather import StationIndex, WeatherDownloader

# Find the closest weather station
index = StationIndex.load()
stations = index.nearest(lat=42.36, lon=-71.06, limit=3)

# Download EPW and DDY files
downloader = WeatherDownloader()
for station in stations:
    files = downloader.download(station, output_dir="weather_files/")
    print(f"{station.name}: {files.epw}, {files.ddy}")

# Use these local paths (or upload to S3) as FileReference inputs to Scythe
# --8<-- [end:example]
