from __future__ import annotations

# --8<-- [start:example]
from idfkit import new_document

# Strict field access is on by default
doc = new_document()

zone = doc.add("Zone", "Office", x_origin=5.0)
print(zone.x_origin)  # 5.0 — known field, works fine

zone.x_orgin  # InvalidFieldError: 'Zone' object has no field 'x_orgin'
# --8<-- [end:example]
