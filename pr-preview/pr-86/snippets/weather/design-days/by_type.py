from __future__ import annotations

from idfkit import IDFObject
from idfkit.weather import DesignDayManager

clg: IDFObject | None = ...  # type: ignore[assignment]
ddm: DesignDayManager = ...  # type: ignore[assignment]
htg: IDFObject | None = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.weather import DesignDayManager, DesignDayType

ddm = DesignDayManager("chicago.ddy")

# Get specific design day
htg = ddm.get(DesignDayType.HEATING_99_6)
if htg:
    print(f"Heating 99.6% DB: {htg.maximum_dry_bulb_temperature}°C")

clg = ddm.get(DesignDayType.COOLING_DB_1)
if clg:
    print(f"Cooling 1% DB: {clg.maximum_dry_bulb_temperature}°C")
# --8<-- [end:example]
