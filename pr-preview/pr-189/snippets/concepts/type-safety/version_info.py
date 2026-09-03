from __future__ import annotations

from idfkit import IDFDocument

model: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit import new_document

doc = new_document(version=(25, 2, 0))

# SpaceHVAC:ZoneReturnMixer was added in EnergyPlus 24.2.0
# IDE docstring shows: "Since: 24.2.0"
mixer = doc.add("SpaceHVAC:ZoneReturnMixer", "Return Mixer 1")
mixer.zone_name = "Office"
# --8<-- [end:example]
