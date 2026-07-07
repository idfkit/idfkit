from __future__ import annotations

from idfkit.weather import StationIndex

index: StationIndex = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Get all available countries
countries = index.countries

for country in sorted(countries)[:10]:
    count = len(index.filter(country=country))
    print(f"{country}: {count} stations")
# --8<-- [end:example]
