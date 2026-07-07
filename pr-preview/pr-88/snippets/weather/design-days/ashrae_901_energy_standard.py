from __future__ import annotations

from idfkit import IDFDocument
from idfkit.weather import DesignDayManager, WeatherStation, apply_ashrae_sizing

ddm: DesignDayManager = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
station: WeatherStation = ...  # type: ignore[assignment]
# --8<-- [start:example]
added = ddm.apply_to_model(
    model,
    heating="99.6%",
    cooling="1%",
)

# Or use the convenience function (takes a WeatherStation, not a path)
added = apply_ashrae_sizing(model, station, standard="90.1")
# --8<-- [end:example]
