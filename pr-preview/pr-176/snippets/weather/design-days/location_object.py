from __future__ import annotations

from idfkit.weather import DesignDayManager
from typing import Any

ddm: DesignDayManager = ...  # type: ignore[assignment]
location: Any = ...  # type: ignore[assignment]
# --8<-- [start:example]
location = ddm.location
if location:
    print(f"Site: {location.name}")
    print(f"Latitude: {location.latitude}")
    print(f"Longitude: {location.longitude}")
    print(f"Time Zone: {location.time_zone}")
    print(f"Elevation: {location.elevation} m")
# --8<-- [end:example]
