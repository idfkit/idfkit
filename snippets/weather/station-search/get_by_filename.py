from __future__ import annotations

from idfkit.weather import StationIndex, WeatherStation

index: StationIndex = ...  # type: ignore[assignment]
station: WeatherStation = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Exact lookup by EPW filename (case-insensitive, extension-tolerant)
stations = index.get_by_filename("USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023")

for station in stations:
    print(f"{station.display_name}: {station.dataset_variant}")
# --8<-- [end:example]
