#!/usr/bin/env python3
"""Build the bundled weather station index.

Downloads all 10 regional Excel index files from climate.onebuilding.org,
parses them, and writes a compressed JSON index to
``src/idfkit/weather/data/stations.json.gz``.

Requires ``openpyxl`` (install via ``pip install idfkit[weather]``).
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the source tree is importable when running from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from idfkit.weather.index import (
    _INDEX_FILES,
    _SOURCES_BASE_URL,
    _download_file,
    _parse_excel,
    _save_compressed_index,
)
from idfkit.weather.station import WeatherStation

_DEST = Path(__file__).resolve().parent.parent / "src" / "idfkit" / "weather" / "data" / "stations.json.gz"


def main() -> None:
    """Download Excel indexes, parse stations, and write compressed index."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        all_stations: list[WeatherStation] = []
        last_modified: dict[str, str] = {}

        for fname in _INDEX_FILES:
            url = f"{_SOURCES_BASE_URL}/{fname}"
            dest = tmp / fname
            print(f"Downloading {fname}...")
            lm = _download_file(url, dest)
            if lm is not None:
                last_modified[fname] = lm

            print(f"  Parsing {fname}...")
            stations = _parse_excel(dest)
            print(f"  Found {len(stations)} stations")
            all_stations.extend(stations)

        print(f"\nTotal stations: {len(all_stations)}")
        print(f"Writing {_DEST}...")
        _save_compressed_index(all_stations, last_modified, _DEST)
        print("Done.")


if __name__ == "__main__":
    main()
