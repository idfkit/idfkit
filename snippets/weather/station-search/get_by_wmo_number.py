from __future__ import annotations

from idfkit.simulation import SimulationResult
from idfkit.weather import StationIndex, WeatherStation

index: StationIndex = ...  # type: ignore[assignment]
results: list[SimulationResult | None] = ...  # type: ignore[assignment]
station: WeatherStation = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Get specific station by WMO
results = index.get_by_wmo("725300")

for station in results:
    print(f"{station.display_name}: {station.source}")
# --8<-- [end:example]
