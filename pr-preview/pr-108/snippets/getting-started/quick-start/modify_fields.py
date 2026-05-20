from __future__ import annotations

from idfkit import IDFDocument, IDFObject

model: IDFDocument = ...  # type: ignore[assignment]
obj: IDFObject = ...  # type: ignore[assignment]
office: IDFObject = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Update a field
office.x_origin = 10.0

# See what references this zone
for obj in model.get_referencing("Office"):
    print(f"  {obj.obj_type}: {obj.name}")
# --8<-- [end:example]
