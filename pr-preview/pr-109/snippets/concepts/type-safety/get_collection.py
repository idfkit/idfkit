from __future__ import annotations

from idfkit import IDFDocument

model: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Literal key — fully typed, IDE knows the return type
zones = model["Zone"]

# Dynamic key — use get_collection() for variable object types
obj_type = "Zone"
collection = model.get_collection(obj_type)  # IDFCollection[IDFObject]
# --8<-- [end:example]
