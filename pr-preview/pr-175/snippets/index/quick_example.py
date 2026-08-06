from __future__ import annotations

from idfkit import IDFDocument, IDFObject

doc: IDFDocument = ...  # type: ignore[assignment]
obj: IDFObject = ...  # type: ignore[assignment]
zone: IDFObject = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit import load_idf, write_idf

# Load an existing IDF file
doc = load_idf("in.idf")

# Query objects with O(1) lookups
zone = doc["Zone"]["Office"]
print(zone.x_origin, zone.y_origin)

# Modify a field
zone.x_origin = 10.0

# See what references the zone
for obj in doc.get_referencing("Office"):
    print(obj.obj_type, obj.name)

# Write back to IDF (or epJSON)
write_idf(doc, "out.idf")
# --8<-- [end:example]
