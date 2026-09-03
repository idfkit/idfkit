from __future__ import annotations

# --8<-- [start:example]
from idfkit.weather import StationIndex, WeatherDownloader

# Every station the isolated run will later ask for.
QUERIES = ("chicago ohare", "denver intl ap", "singapore changi")

index = StationIndex.load()
downloader = WeatherDownloader()

for query in QUERIES:
    results = index.search(query)
    if not results:
        # Fail here, where there is still a network to fix the problem with.
        msg = f"no weather station matched {query!r}"
        raise LookupError(msg)
    station = results[0].station
    files = downloader.download(station, only={".epw", ".ddy"})
    print(f"warmed {station.display_name}: {files.epw}")
# --8<-- [end:example]
