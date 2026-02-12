from __future__ import annotations

from idfkit import IDFDocument

idf: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
removed = idf.popidfobject("ZONE", 0)
# --8<-- [end:example]
