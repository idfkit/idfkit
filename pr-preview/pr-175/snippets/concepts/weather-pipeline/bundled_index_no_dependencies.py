from __future__ import annotations

from idfkit.weather import StationIndex

index: StationIndex = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.weather import StationIndex

index = StationIndex.load()  # Instant, no network
print(f"{len(index)} entries, {len(index.countries)} countries")
# --8<-- [end:example]
