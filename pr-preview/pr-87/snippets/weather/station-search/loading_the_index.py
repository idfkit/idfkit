from __future__ import annotations

from idfkit.weather import StationIndex

index: StationIndex = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.weather import StationIndex

# Instant load from bundled data (no network needed)
index = StationIndex.load()

print(f"Stations: {len(index)}")
print(f"Countries: {len(index.countries)}")
# --8<-- [end:example]
