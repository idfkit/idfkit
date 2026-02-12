from __future__ import annotations

from idfkit.simulation import SimulationResult
from idfkit.weather import StationIndex

index: StationIndex = ...  # type: ignore[assignment]
results: list[SimulationResult | None] = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Find nearest stations to a coordinate
results = index.nearest(41.88, -87.63, limit=5)

for r in results:
    print(f"{r.station.display_name}: {r.distance_km:.1f} km")
# --8<-- [end:example]
