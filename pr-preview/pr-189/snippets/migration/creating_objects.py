from __future__ import annotations

from idfkit import IDFDocument, IDFObject

idf: IDFDocument = ...  # type: ignore[assignment]
zone: IDFObject = ...  # type: ignore[assignment]
# --8<-- [start:example]
zone = idf.newidfobject("ZONE")
zone.Name = "Office"
zone.X_Origin = 0.0
# --8<-- [end:example]
