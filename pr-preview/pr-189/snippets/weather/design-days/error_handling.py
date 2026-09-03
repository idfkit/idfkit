from __future__ import annotations

from idfkit import IDFDocument
from idfkit.weather import DesignDayManager

ddm: DesignDayManager = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.exceptions import NoDesignDaysError

try:
    ddm = DesignDayManager("incomplete.ddy")
    ddm.apply_to_model(model, heating="99.6%", cooling="1%")
except NoDesignDaysError as e:
    print(f"Missing design days: {e}")
# --8<-- [end:example]
