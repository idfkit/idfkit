from __future__ import annotations

from idfkit.weather import StationIndex

index: StationIndex = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Check if upstream has updates
if index.check_for_updates():
    print("Updates available")

    # Refresh from climate.onebuilding.org (stdlib only, no extras)
    index = StationIndex.refresh()
# --8<-- [end:example]
