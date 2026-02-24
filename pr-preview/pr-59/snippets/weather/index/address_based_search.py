from __future__ import annotations

from idfkit.simulation import SimulationResult
from idfkit.weather import StationIndex

index: StationIndex = ...  # type: ignore[assignment]
results: list[SimulationResult | None] = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.weather import StationIndex, geocode

index = StationIndex.load()
results = index.nearest(*geocode("350 Fifth Avenue, New York, NY"))

for r in results[:3]:
    print(f"{r.station.display_name}: {r.distance_km:.0f} km")
# --8<-- [end:example]
