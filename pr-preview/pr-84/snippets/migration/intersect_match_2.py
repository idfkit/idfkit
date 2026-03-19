from __future__ import annotations

from idfkit import IDFDocument

doc: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.geometry import intersect_match

# Match coincident walls between zones and set boundary conditions
intersect_match(doc)
# --8<-- [end:example]
