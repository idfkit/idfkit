from __future__ import annotations

lat: float = ...  # type: ignore[assignment]
lon: float = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.weather import detect_location

# Detect approximate coordinates from this machine's public IP.
# Sent over HTTPS to ipapi.co; result cached on disk for 1 hour.
lat, lon = detect_location()
print(f"Approximate location: {lat:.4f}, {lon:.4f}")
# --8<-- [end:example]
