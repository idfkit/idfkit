from __future__ import annotations

from idfkit import IDFDocument
from idfkit.weather import DesignDayManager, WeatherStation

ddm: DesignDayManager = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
station: WeatherStation = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.weather import DesignDayManager

ddm = DesignDayManager("chicago.ddy")

# ASHRAE 90.1 (stricter heating condition)
ddm.apply_to_model(model, heating="99.6%", cooling="1%")

# Or use the convenience function with standard presets
from idfkit.weather import apply_ashrae_sizing

apply_ashrae_sizing(model, station, standard="90.1")
# --8<-- [end:example]
