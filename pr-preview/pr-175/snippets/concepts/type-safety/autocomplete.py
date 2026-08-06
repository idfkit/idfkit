from __future__ import annotations

from idfkit import IDFDocument, load_idf

model: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit import load_idf

model = load_idf("building.idf")

# Typed accessor — returns IDFCollection[Zone]
zones = model.zones

# O(1) lookup by name — returns Zone (typed IDFObject subclass)
zone = zones["Office"]

# Field access with IDE autocomplete and type info
print(zone.x_origin)  # float | None
print(zone.multiplier)  # int | None

# Subscript access also works
all_zones = model["Zone"]
# --8<-- [end:example]
