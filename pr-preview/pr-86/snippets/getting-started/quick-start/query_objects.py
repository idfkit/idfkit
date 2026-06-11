from __future__ import annotations

from idfkit import IDFDocument, IDFObject

model: IDFDocument = ...  # type: ignore[assignment]
office: IDFObject = ...  # type: ignore[assignment]
zone: IDFObject = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Get all zones
for zone in model["Zone"]:
    print(f"Zone: {zone.name}")

# Get a specific zone by name
office = model["Zone"]["Office"]
print(f"Origin: ({office.x_origin}, {office.y_origin}, {office.z_origin})")
# --8<-- [end:example]
