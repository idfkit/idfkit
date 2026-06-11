from __future__ import annotations

from idfkit.weather import StationIndex

index: StationIndex = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Get all stations in a country
us_stations = index.filter(country="USA")
print(f"US stations: {len(us_stations)}")

# Get all stations in a state/region
california = [s for s in us_stations if s.state == "CA"]
# --8<-- [end:example]
