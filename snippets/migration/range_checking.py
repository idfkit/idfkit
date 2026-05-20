from __future__ import annotations

from idfkit import IDFObject

obj: IDFObject = ...  # type: ignore[assignment]
# --8<-- [start:example]
obj.getrange("Density")
# {'minimum': 0, 'type': 'real'}

obj.checkrange("Density")  # raises RangeError if out of range
# --8<-- [end:example]
