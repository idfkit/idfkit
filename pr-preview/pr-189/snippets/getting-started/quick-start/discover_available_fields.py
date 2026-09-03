from __future__ import annotations

from idfkit import IDFDocument

model: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
# See all fields for a Zone
print(model.describe("Zone"))
# === Zone ===
# ...
# Fields (9):
#   direction_of_relative_north (number) [deg] default=0
#   x_origin (number) [m] default=0
#   ...

# See required fields for a Material
desc = model.describe("Material")
print(f"Required: {desc.required_fields}")
# Required: ['roughness', 'thickness', 'conductivity', 'density', 'specific_heat']
# --8<-- [end:example]
