from __future__ import annotations

# --8<-- [start:example]
from idfkit import new_document

# Enable strict mode to catch field-name typos during migration
doc = new_document()
doc.strict = True

zone = doc.add("Zone", "Office", x_origin=5.0)
print(zone.x_origin)  # 5.0 — known field, works fine

zone.x_orgin  # AttributeError: 'Zone' object has no field 'x_orgin'
# --8<-- [end:example]
