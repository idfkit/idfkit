from __future__ import annotations

# --8<-- [start:example]
from idfkit.weather import StationIndex, WeatherDownloader

# Find the closest weather station
index = StationIndex.load()
results = index.nearest(latitude=42.36, longitude=-71.06, limit=3)

# Download EPW and DDY files
downloader = WeatherDownloader()
for result in results:
    files = downloader.download(result.station)
    print(f"{result.station.display_name} ({result.distance_km:.1f} km): {files.epw}, {files.ddy}")

# Use these local paths (or upload to S3) as FileReference inputs to Scythe
# --8<-- [end:example]
