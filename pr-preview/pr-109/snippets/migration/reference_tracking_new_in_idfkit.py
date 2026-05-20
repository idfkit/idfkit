from __future__ import annotations

from idfkit import IDFDocument, IDFObject

doc: IDFDocument = ...  # type: ignore[assignment]
obj: IDFObject = ...  # type: ignore[assignment]
people_obj: IDFObject = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Find every object that points to the "Office" zone
for obj in doc.get_referencing("Office"):
    print(obj.obj_type, obj.name)

# Find every name that the People object references
names = doc.get_references(people_obj)
# --8<-- [end:example]
