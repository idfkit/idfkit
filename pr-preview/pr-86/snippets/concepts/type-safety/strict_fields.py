from __future__ import annotations

# --8<-- [start:example]
from idfkit import new_document

# Enable strict field access on a new document
doc = new_document(strict=True)

zone = doc.add("Zone", "Office")
zone.x_origin = 0.0  # OK — valid field

# zone.x_orgin = 0.0  # AttributeError! Typo caught immediately

# Also available when loading files
# model = load_idf("building.idf", strict_fields=True)
# model = load_epjson("building.epJSON", strict_fields=True)
# --8<-- [end:example]
