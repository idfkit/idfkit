from __future__ import annotations

# --8<-- [start:example]
from pathlib import Path

from idfkit.weather import StationIndex, WeatherDownloader
from idfkit.weather.index import default_cache_dir

QUERIES = ("chicago ohare", "denver intl ap", "singapore changi")

cache: Path = default_cache_dir()
index = StationIndex.load()
downloader = WeatherDownloader()

missing: list[str] = []
for query in QUERIES:
    station = index.search(query)[0].station
    # download() returns from disk when the bundle is already cached, so a warm
    # cache makes this a no-op. Run it while the network is still available and
    # a miss is repairable, never as the isolated run's first act.
    files = downloader.download(station, only={".epw", ".ddy"})
    if files.epw is None or files.ddy is None:
        missing.append(station.display_name)

if missing:
    msg = f"cache at {cache} is missing EPW or DDY for: {', '.join(missing)}"
    raise SystemExit(msg)
print(f"cache at {cache} covers all {len(QUERIES)} stations")
# --8<-- [end:example]
