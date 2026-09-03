from __future__ import annotations

from idfkit.weather import StationIndex

index: StationIndex = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Direct coordinate lookup
results = index.nearest(40.7484, -73.9857)  # Empire State Building
# --8<-- [end:example]
