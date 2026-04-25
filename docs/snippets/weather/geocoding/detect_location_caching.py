from __future__ import annotations

from datetime import timedelta
from pathlib import Path

lat: float = ...  # type: ignore[assignment]
lon: float = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.weather import detect_location

# Default: cache for 1 hour in the platform weather cache directory.
lat, lon = detect_location()

# Cache for 24 hours instead.
lat, lon = detect_location(max_age=timedelta(hours=24))

# Always re-fetch (skip the cache).
lat, lon = detect_location(max_age=0)

# Cache forever (until the file is deleted).
lat, lon = detect_location(max_age=None)

# Use a custom cache directory.
lat, lon = detect_location(cache_dir=Path("/tmp/my-cache"))
# --8<-- [end:example]
