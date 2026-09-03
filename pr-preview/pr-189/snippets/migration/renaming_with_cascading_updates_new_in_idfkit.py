from __future__ import annotations

from idfkit import IDFDocument, IDFObject

doc: IDFDocument = ...  # type: ignore[assignment]
zone: IDFObject = ...  # type: ignore[assignment]
# --8<-- [start:example]
zone = doc["Zone"]["Office"]
zone.name = "Open_Office"
# All fields across the document that pointed to "Office" now say "Open_Office"
# --8<-- [end:example]
