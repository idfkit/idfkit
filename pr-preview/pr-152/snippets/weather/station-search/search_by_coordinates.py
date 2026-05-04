from __future__ import annotations

from idfkit.simulation import SimulationResult
from idfkit.weather import StationIndex

index: StationIndex = ...  # type: ignore[assignment]
results: list[SimulationResult | None] = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Nearest to downtown Chicago
results = index.nearest(41.88, -87.63)

for r in results[:5]:
    print(f"{r.station.display_name}: {r.distance_km:.1f} km")
# --8<-- [end:example]
