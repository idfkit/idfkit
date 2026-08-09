from __future__ import annotations

from idfkit import IDFDocument

idf: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
# geomeppy (extends eppy)
idf.set_wwr(0.4)
idf.set_wwr(0.4, construction="SimpleGlazing")
idf.set_wwr(0.25, orientation="south")
# --8<-- [end:example]
