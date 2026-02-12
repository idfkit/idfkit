from __future__ import annotations

from idfkit import IDFDocument, IDFObject
from idfkit.weather import WeatherStation

added: list[IDFObject] = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
station: WeatherStation = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.weather import apply_ashrae_sizing

# Apply ASHRAE 90.1 design conditions
added = apply_ashrae_sizing(model, station, standard="90.1")
print(f"Added {len(added)} design days")
# --8<-- [end:example]
