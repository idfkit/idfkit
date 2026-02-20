from __future__ import annotations

from idfkit.weather import StationIndex

index: StationIndex = ...  # type: ignore[assignment]
# --8<-- [start:example]
# City name
results = index.search("New York")

# Airport code pattern
results = index.search("JFK")

# WMO number
results = index.search("725300")

# Country + city
results = index.search("London UK")
# --8<-- [end:example]
