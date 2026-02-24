from __future__ import annotations

lat: float = ...  # type: ignore[assignment]
lon: float = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.weather import geocode

# Get coordinates for an address
lat, lon = geocode("350 Fifth Avenue, New York, NY")
print(f"Empire State Building: {lat:.4f}, {lon:.4f}")
# --8<-- [end:example]
