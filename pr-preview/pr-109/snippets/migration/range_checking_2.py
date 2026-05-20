from __future__ import annotations

from idfkit import IDFObject

obj: IDFObject = ...  # type: ignore[assignment]
# --8<-- [start:example]
obj.getrange("density")
# {'minimum': 0, 'type': 'real'}

obj.checkrange("density")  # True, or raises RangeError
# --8<-- [end:example]
