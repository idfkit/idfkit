from __future__ import annotations

from idfkit import IDFObject

zone: IDFObject = ...  # type: ignore[assignment]
# --8<-- [start:example]
print(zone.X_Origin)
zone.X_Origin = 5.0
# --8<-- [end:example]
