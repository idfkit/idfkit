from __future__ import annotations

from pathlib import Path

from idfkit.weather import WeatherDownloader

downloader: WeatherDownloader = ...  # type: ignore[assignment]
epw: Path = ...  # type: ignore[assignment]
ddy: Path = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.weather import WeatherDownloader

downloader = WeatherDownloader()

# Download directly by EPW filename — no manual station lookup needed
epw = downloader.get_epw_by_filename("USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023")
ddy = downloader.get_ddy_by_filename("USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023")

print(f"EPW: {epw}")
print(f"DDY: {ddy}")
# --8<-- [end:example]
