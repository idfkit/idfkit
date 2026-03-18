from __future__ import annotations

from idfkit import IDFDocument, IDFObject

idf: IDFDocument = ...  # type: ignore[assignment]
surface: IDFObject = ...  # type: ignore[assignment]
# --8<-- [start:example]
surface = idf.idfobjects["BuildingSurface:Detailed"][0]
construction = surface.get_referenced_object("Construction_Name")
# --8<-- [end:example]
