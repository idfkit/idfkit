from __future__ import annotations

from idfkit.weather import StationIndex

index: StationIndex = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Search by name
results = index.search("chicago ohare")

for r in results[:5]:
    print(f"{r.station.display_name} (score={r.score:.2f})")
# --8<-- [end:example]
