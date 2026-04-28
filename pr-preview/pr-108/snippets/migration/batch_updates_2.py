from __future__ import annotations

from idfkit import IDFDocument

doc: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
doc.update({
    "Zone.Office.x_origin": 10.0,
    "Zone.Office.y_origin": 5.0,
})
# --8<-- [end:example]
