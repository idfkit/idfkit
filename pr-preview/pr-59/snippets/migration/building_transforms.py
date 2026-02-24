from __future__ import annotations

from idfkit import IDFDocument

doc: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.geometry import translate_building, rotate_building, Vector3D

# Shift the entire building 10m east and 5m north
translate_building(doc, Vector3D(10.0, 5.0, 0.0))

# Rotate 45 degrees counter-clockwise around the origin
rotate_building(doc, 45.0)

# Rotate around a custom anchor point
rotate_building(doc, 90.0, anchor=Vector3D(5.0, 5.0, 0.0))
# --8<-- [end:example]
