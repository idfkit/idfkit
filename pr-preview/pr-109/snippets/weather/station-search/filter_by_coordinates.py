from __future__ import annotations

from idfkit.weather import StationIndex

index: StationIndex = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Find all stations within 100 km of a point
stations = index.nearest(
    41.0,
    -88.5,
    max_distance_km=100.0,
    limit=50,
)
# --8<-- [end:example]
