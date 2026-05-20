from __future__ import annotations

# --8<-- [start:example]
from idfkit import new_document

# Strict field access is on by default
doc = new_document()

zone = doc.add("Zone", "Office")
zone.x_origin = 0.0  # OK — valid field

# zone.x_orgin = 0.0  # InvalidFieldError! Typo caught immediately

# Also the default when loading files
# model = load_idf("building.idf")
# model = load_epjson("building.epJSON")
# --8<-- [end:example]
