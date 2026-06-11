from __future__ import annotations

from idfkit import IDFObject
from idfkit.weather import DesignDayManager

dd_obj: IDFObject = ...  # type: ignore[assignment]
ddm: DesignDayManager = ...  # type: ignore[assignment]
# --8<-- [start:example]
# All classified annual design days (returns a list of IDFObject)
for dd_obj in ddm.annual:
    print(dd_obj.name)

# Monthly design days
for dd_obj in ddm.monthly:
    print(dd_obj.name)
# --8<-- [end:example]
