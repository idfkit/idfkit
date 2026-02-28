from __future__ import annotations

from idfkit.simulation import SimulationResult
from idfkit.weather import StationIndex

index: StationIndex = ...  # type: ignore[assignment]
results: list[SimulationResult | None] = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Multiple entries can have the same WMO
results = index.search("725300")  # Chicago O'Hare WMO
for r in results:
    print(f"{r.station.source_data}: {r.station.url}")
# --8<-- [end:example]
