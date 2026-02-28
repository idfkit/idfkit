from __future__ import annotations

from idfkit.simulation import SimulationResult
from idfkit.weather import StationIndex, WeatherStation

index: StationIndex = ...  # type: ignore[assignment]
results: list[SimulationResult | None] = ...  # type: ignore[assignment]
station: WeatherStation = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.weather import StationIndex, geocode

# Load the station index (instant, no network needed)
index = StationIndex.load()

# Search by name
results = index.search("chicago ohare")
print(results[0].station.display_name)

# Find nearest station to an address
results = index.nearest(*geocode("Willis Tower, Chicago, IL"))
station = results[0].station
print(f"{station.display_name}: {results[0].distance_km:.0f} km away")
# --8<-- [end:example]
