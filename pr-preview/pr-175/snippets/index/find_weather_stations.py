from __future__ import annotations

from idfkit.simulation import SimulationResult
from idfkit.weather import StationIndex

index: StationIndex = ...  # type: ignore[assignment]
results: list[SimulationResult | None] = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.weather import StationIndex, geocode

index = StationIndex.load()
results = index.nearest(*geocode("Chicago, IL"))
print(results[0].station.display_name)
# --8<-- [end:example]
