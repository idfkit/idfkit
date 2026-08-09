from __future__ import annotations

from idfkit import IDFDocument
from idfkit.weather import DesignDayManager

ddm: DesignDayManager = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
added = ddm.apply_to_model(
    model,
    heating="99.6%",
    cooling="1%",
    include_wet_bulb=True,  # Also add WB=>MDB cooling design day
)
# --8<-- [end:example]
