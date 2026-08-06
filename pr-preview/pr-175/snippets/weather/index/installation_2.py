from __future__ import annotations

from idfkit.weather import StationIndex

index: StationIndex = ...  # type: ignore[assignment]
# --8<-- [start:example]
if index.check_for_updates():
    index = StationIndex.refresh()  # Downloads latest data
# --8<-- [end:example]
