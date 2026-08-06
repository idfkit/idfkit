from __future__ import annotations

from idfkit.weather import DesignDayManager

ddm: DesignDayManager = ...  # type: ignore[assignment]
# --8<-- [start:example]
ddm = DesignDayManager("chicago.ddy")
print(ddm.summary())
# --8<-- [end:example]
