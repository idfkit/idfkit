from __future__ import annotations

from idfkit import IDFDocument
from idfkit.weather import WeatherStation

model: IDFDocument = ...  # type: ignore[assignment]
station: WeatherStation = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.weather import apply_ashrae_sizing

# Apply standard design conditions (downloads DDY from station automatically)
added = apply_ashrae_sizing(
    model,
    station,
    standard="90.1",  # ASHRAE 90.1 criteria
)
# --8<-- [end:example]
