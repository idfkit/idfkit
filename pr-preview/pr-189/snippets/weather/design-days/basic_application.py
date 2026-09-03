from __future__ import annotations

from idfkit import IDFDocument
from idfkit.weather import DesignDayManager

ddm: DesignDayManager = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
added = ddm.apply_to_model(
    model,
    heating="99.6%",  # Use 99.6% heating conditions
    cooling="1%",  # Use 1% cooling conditions
)
# --8<-- [end:example]
