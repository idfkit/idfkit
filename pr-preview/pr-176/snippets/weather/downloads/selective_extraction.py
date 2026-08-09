from __future__ import annotations

from idfkit.weather import WeatherDownloader, WeatherStation

downloader: WeatherDownloader = ...  # type: ignore[assignment]
station: WeatherStation = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Pull just the EPW out of the bundle — skip DDY and STAT extraction.
files = downloader.download(station, only={".epw"})

print(f"EPW: {files.epw}")
assert files.ddy is None
assert files.stat is None

# Pass an iterable of any-case suffixes; ".EPW" and "epw" both match ".epw".
both = downloader.download(station, only=[".epw", ".ddy"])
assert both.epw is not None
assert both.ddy is not None
# --8<-- [end:example]
