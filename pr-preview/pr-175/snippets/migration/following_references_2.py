from __future__ import annotations

from idfkit import IDFDocument, IDFObject

doc: IDFDocument = ...  # type: ignore[assignment]
surface: IDFObject = ...  # type: ignore[assignment]
# --8<-- [start:example]
surface = doc["BuildingSurface:Detailed"][0]
construction = surface.get_referenced_object("construction_name")
# --8<-- [end:example]
