from __future__ import annotations

from idfkit.weather import geocode

# --8<-- [start:example]
# Full address
lat, lon = geocode("123 Main Street, Springfield, IL 62701")

# Landmark
lat, lon = geocode("Eiffel Tower, Paris")

# City only
lat, lon = geocode("Tokyo, Japan")

# Partial address
lat, lon = geocode("Times Square, New York")
# --8<-- [end:example]
