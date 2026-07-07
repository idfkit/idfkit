from __future__ import annotations

from idfkit import IDFDocument, IDFObject
from idfkit.weather import DesignDayManager

added: list[IDFObject] = ...  # type: ignore[assignment]
ddm: DesignDayManager = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.weather import DesignDayManager

# Parse a DDY file and apply design days to your model
ddm = DesignDayManager("weather.ddy")
added = ddm.apply_to_model(
    model,
    heating="99.6%",
    cooling="1%",
    update_location=True,
)
print(f"Added {len(added)} design days")
# --8<-- [end:example]
