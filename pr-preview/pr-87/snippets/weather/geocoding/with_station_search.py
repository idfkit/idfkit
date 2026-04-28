from __future__ import annotations

from idfkit.simulation import SimulationResult
from idfkit.weather import StationIndex, WeatherStation

index: StationIndex = ...  # type: ignore[assignment]
results: list[SimulationResult | None] = ...  # type: ignore[assignment]
station: WeatherStation = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.weather import StationIndex, geocode

index = StationIndex.load()

# One-liner using splat operator
results = index.nearest(*geocode("Willis Tower, Chicago, IL"))

# First result is the nearest station
station = results[0].station
print(f"Nearest: {station.display_name} ({results[0].distance_km:.1f} km)")
# --8<-- [end:example]
