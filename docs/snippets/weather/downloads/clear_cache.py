from __future__ import annotations

from idfkit.weather import WeatherDownloader

downloader: WeatherDownloader = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Removes the cached weather files. The station index is kept, so the next
# download resolves stations without going back to the network for the index.
downloader.clear_cache()
# --8<-- [end:example]
