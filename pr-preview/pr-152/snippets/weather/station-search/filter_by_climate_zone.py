from __future__ import annotations

from idfkit.weather import StationIndex

index: StationIndex = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Each WeatherStation carries its ASHRAE HOF climate zone.
zone_4a = [s for s in index.stations if s.ashrae_climate_zone.startswith("4A")]
print(f"Zone 4A stations: {len(zone_4a)}")

# Combine with country/state via the existing filter() to narrow further:
us_zone_5 = [s for s in index.filter(country="USA") if s.ashrae_climate_zone.startswith("5")]

# Pick the warmest design dry-bulb in a given zone:
hottest = max(us_zone_5, key=lambda s: s.cooling_design_db_c)
print(f"{hottest.display_name}: {hottest.cooling_design_db_c} °C / {hottest.cooling_design_db_f:.1f} °F")
# --8<-- [end:example]
