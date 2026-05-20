from __future__ import annotations

from idfkit.weather import StationIndex

index: StationIndex = ...  # type: ignore[assignment]
lat: float = ...  # type: ignore[assignment]
lon: float = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.weather import geocode

lat, lon = geocode("350 Fifth Avenue, New York, NY")
results = index.nearest(lat, lon)
# --8<-- [end:example]
