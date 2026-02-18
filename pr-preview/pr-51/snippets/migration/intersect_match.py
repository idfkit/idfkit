from __future__ import annotations

from idfkit import IDFDocument

idf: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
# geomeppy (extends eppy)
idf.intersect_match()
# --8<-- [end:example]
