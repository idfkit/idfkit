from __future__ import annotations

# --8<-- [start:example]
from idfkit.weather import GeocodingError, detect_location

try:
    lat, lon = detect_location()
except GeocodingError as e:
    # Network failure, ipapi.co rate limit, or unrecognised IP.
    print(f"Could not detect location: {e}")
    # Fall back to an explicit prompt or a hard-coded default.
    lat, lon = 41.85, -87.65  # Chicago
# --8<-- [end:example]
