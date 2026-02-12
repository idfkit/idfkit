from __future__ import annotations

from idfkit.weather import geocode

addresses: list[str] = ...  # type: ignore[assignment]
lat: float = ...  # type: ignore[assignment]
lon: float = ...  # type: ignore[assignment]
# --8<-- [start:example]
# These are automatically spaced 1 second apart
for address in addresses:
    lat, lon = geocode(address)  # Rate limited internally
    print(f"{address}: {lat:.2f}, {lon:.2f}")
# --8<-- [end:example]
