from __future__ import annotations

from idfkit import IDFDocument

doc: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
zone = doc.add("Zone", "Office", x_origin=0.0)
# --8<-- [end:example]
