from __future__ import annotations

from idfkit.weather import StationIndex

index: StationIndex = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Check if upstream data has changed
if index.check_for_updates():
    index = StationIndex.refresh()  # Downloads ~10 Excel files
# --8<-- [end:example]
