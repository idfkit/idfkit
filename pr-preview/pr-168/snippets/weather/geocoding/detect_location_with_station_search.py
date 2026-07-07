from __future__ import annotations

from idfkit.weather import StationIndex, WeatherStation

index: StationIndex = ...  # type: ignore[assignment]
station: WeatherStation = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.weather import StationIndex, detect_location

index = StationIndex.load()

# "Find weather stations near me" — one liner using the splat operator.
results = index.nearest(*detect_location())

station = results[0].station
print(f"Nearest: {station.display_name} ({results[0].distance_km:.1f} km)")
# --8<-- [end:example]
