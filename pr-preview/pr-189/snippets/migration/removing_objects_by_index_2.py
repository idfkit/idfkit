from __future__ import annotations

from idfkit import IDFDocument

doc: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
removed = doc.popidfobject("Zone", 0)
# --8<-- [end:example]
