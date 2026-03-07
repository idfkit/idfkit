from __future__ import annotations

from idfkit import IDFDocument

model: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import expand_objects

expanded = expand_objects(model)
# HVACTemplate:Zone:IdealLoadsAirSystem → ZoneHVAC:IdealLoadsAirSystem + ...
# --8<-- [end:example]
