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
    update_location=False,  # Keep existing Site:Location
)
# --8<-- [end:example]
