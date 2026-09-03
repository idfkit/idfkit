from __future__ import annotations

from idfkit import IDFDocument

doc: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.geometry import set_wwr

# Apply 40% WWR to all exterior walls
set_wwr(doc, 0.4)

# Specify a window construction
set_wwr(doc, 0.4, construction="SimpleGlazing")

# Target only south-facing walls
set_wwr(doc, 0.25, orientation="south")
# --8<-- [end:example]
