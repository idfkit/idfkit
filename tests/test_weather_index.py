"""Tests for idfkit.weather.index (offline, no network)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from idfkit.weather.index import (
    StationIndex,
    _load_compressed_index,
    _save_compressed_index,
)
from idfkit.weather.station import WeatherStation


def _fixture_stations() -> list[WeatherStation]:
    """A small hand-crafted station list for search and spatial tests."""
    return [
        WeatherStation(
            country="USA",
            state="IL",
            city="Chicago.Ohare.Intl.AP",
            wmo=725300,
            source="SRC-TMYx",
            latitude=41.98,
            longitude=-87.92,
            timezone=-6.0,
            elevation=201.0,
            url="https://climate.onebuilding.org/WMO_Region_4_North_and_Central_America/USA_United_States_of_America/IL_Illinois/USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023.zip",
        ),
        WeatherStation(
            country="USA",
            state="IL",
            city="Chicago.Midway.AP",
            wmo=725340,
            source="SRC-TMYx",
            latitude=41.79,
            longitude=-87.75,
            timezone=-6.0,
            elevation=189.0,
            url="https://climate.onebuilding.org/WMO_Region_4_North_and_Central_America/USA_United_States_of_America/IL_Illinois/USA_IL_Chicago.Midway.AP.725340_TMYx.2009-2023.zip",
        ),
        WeatherStation(
            country="USA",
            state="NY",
            city="New.York.J.F.Kennedy.Intl.AP",
            wmo=744860,
            source="SRC-TMYx",
            latitude=40.64,
            longitude=-73.76,
            timezone=-5.0,
            elevation=4.0,
            url="https://climate.onebuilding.org/WMO_Region_4_North_and_Central_America/USA_United_States_of_America/NY_New_York/USA_NY_New.York.J.F.Kennedy.Intl.AP.744860_TMYx.zip",
        ),
        WeatherStation(
            country="GBR",
            state="",
            city="London.Heathrow.AP",
            wmo=37720,
            source="SRC-TMYx",
            latitude=51.48,
            longitude=-0.45,
            timezone=0.0,
            elevation=25.0,
            url="https://climate.onebuilding.org/WMO_Region_6_Europe/GBR_United_Kingdom/GBR_London.Heathrow.AP.037720_TMYx.zip",
        ),
        WeatherStation(
            country="FRA",
            state="",
            city="Paris.Orly.AP",
            wmo=71490,
            source="SRC-TMYx",
            latitude=48.73,
            longitude=2.40,
            timezone=1.0,
            elevation=89.0,
            url="https://climate.onebuilding.org/WMO_Region_6_Europe/FRA_France/FRA_Paris.Orly.AP.071490_TMYx.zip",
        ),
    ]


class TestStationIndex:
    def test_len(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        assert len(idx) == 5

    def test_get_by_wmo(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.get_by_wmo(725300)
        assert len(results) == 1
        assert results[0].city == "Chicago.Ohare.Intl.AP"

    def test_get_by_wmo_missing(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        assert idx.get_by_wmo(999999) == []


class TestSearch:
    def test_exact_wmo(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.search("725300")
        assert len(results) >= 1
        assert results[0].station.wmo == 725300
        assert results[0].score == 1.0
        assert results[0].match_field == "wmo"

    def test_name_substring(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.search("ohare")
        assert len(results) >= 1
        assert results[0].station.city == "Chicago.Ohare.Intl.AP"
        assert results[0].score > 0.8

    def test_multi_token(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.search("chicago midway")
        assert len(results) >= 1
        assert results[0].station.wmo == 725340

    def test_country_filter(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.search("ap", country="GBR")
        assert all(r.station.country == "GBR" for r in results)

    def test_empty_query(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        assert idx.search("") == []

    def test_no_match(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.search("zzzznonexistent")
        assert results == []


class TestNearest:
    def test_nearest_to_chicago(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        # Downtown Chicago: 41.88, -87.63
        results = idx.nearest(41.88, -87.63, limit=3)
        assert len(results) == 3
        # Midway is closer to downtown than O'Hare
        assert results[0].station.wmo == 725340  # Midway
        assert results[1].station.wmo == 725300  # O'Hare
        # Distance should be reasonable
        assert results[0].distance_km < 30.0

    def test_max_distance_filter(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.nearest(41.88, -87.63, max_distance_km=50.0)
        # Only Chicago stations should be within 50 km
        assert all(r.station.state == "IL" for r in results)

    def test_country_filter(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.nearest(51.50, -0.10, country="GBR", limit=10)
        assert all(r.station.country == "GBR" for r in results)

    def test_results_sorted_by_distance(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.nearest(45.0, -75.0, limit=5)
        distances = [r.distance_km for r in results]
        assert distances == sorted(distances)


class TestFilter:
    def test_filter_by_country(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.filter(country="USA")
        assert len(results) == 3
        assert all(s.country == "USA" for s in results)

    def test_filter_by_state(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.filter(state="IL")
        assert len(results) == 2

    def test_filter_combined(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.filter(country="USA", state="NY")
        assert len(results) == 1
        assert results[0].wmo == 744860

    def test_countries(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        assert idx.countries == ["FRA", "GBR", "USA"]


# ---------------------------------------------------------------------------
# Compressed index (bundled / cache) tests
# ---------------------------------------------------------------------------


class TestCompressedIndex:
    """Round-trip tests for save/load of compressed JSON index."""

    def test_save_and_load_round_trip(self, tmp_path: Path) -> None:
        stations = _fixture_stations()
        last_modified = {"file_a.xlsx": "Wed, 15 Jan 2026 10:30:00 GMT"}
        dest = tmp_path / "stations.json.gz"

        _save_compressed_index(stations, last_modified, dest)
        loaded_stations, loaded_lm, built_at = _load_compressed_index(dest)

        assert len(loaded_stations) == len(stations)
        assert loaded_stations[0] == stations[0]
        assert loaded_lm == last_modified
        assert built_at  # non-empty ISO timestamp

    def test_empty_index(self, tmp_path: Path) -> None:
        dest = tmp_path / "empty.json.gz"
        _save_compressed_index([], {}, dest)
        stations, lm, _ = _load_compressed_index(dest)
        assert stations == []
        assert lm == {}


class TestLoadBundled:
    """Tests for StationIndex.load() with bundled and cached indexes."""

    def test_load_from_bundled(self) -> None:
        """load() should succeed using the bundled index."""
        idx = StationIndex.load(cache_dir=Path("/nonexistent/cache/dir"))
        assert len(idx) > 0

    def test_load_from_cache_takes_priority(self, tmp_path: Path) -> None:
        """A cached index in cache_dir should take priority over bundled."""
        stations = _fixture_stations()[:2]
        last_modified = {"test.xlsx": "Mon, 01 Jan 2026 00:00:00 GMT"}
        dest = tmp_path / "stations.json.gz"
        _save_compressed_index(stations, last_modified, dest)

        idx = StationIndex.load(cache_dir=tmp_path)
        assert len(idx) == 2

    def test_load_missing_raises(self, tmp_path: Path) -> None:
        """load() should raise FileNotFoundError if no index exists."""
        with (
            patch("idfkit.weather.index._BUNDLED_INDEX", tmp_path / "nope.json.gz"),
            pytest.raises(FileNotFoundError, match="No station index found"),
        ):
            StationIndex.load(cache_dir=tmp_path)


class TestCheckForUpdates:
    """Tests for StationIndex.check_for_updates()."""

    def test_stale_returns_true(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        idx._last_modified = {
            "Region1_Africa_TMYx_EPW_Processing_locations.xlsx": "Wed, 01 Jan 2020 00:00:00 GMT",
        }
        with patch(
            "idfkit.weather.index._head_last_modified",
            return_value="Wed, 15 Jan 2026 10:30:00 GMT",
        ):
            assert idx.check_for_updates() is True

    def test_fresh_returns_false(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        same_date = "Wed, 15 Jan 2026 10:30:00 GMT"
        idx._last_modified = {
            "Region1_Africa_TMYx_EPW_Processing_locations.xlsx": same_date,
        }
        with patch("idfkit.weather.index._head_last_modified", return_value=same_date):
            assert idx.check_for_updates() is False

    def test_offline_returns_false(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        idx._last_modified = {
            "Region1_Africa_TMYx_EPW_Processing_locations.xlsx": "Wed, 01 Jan 2020 00:00:00 GMT",
        }
        with patch("idfkit.weather.index._head_last_modified", return_value=None):
            assert idx.check_for_updates() is False

    def test_no_metadata_returns_false(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        assert idx.check_for_updates() is False


class TestRefresh:
    """Tests for StationIndex.refresh() with mocked network."""

    def test_refresh_saves_and_loads(self, tmp_path: Path) -> None:
        stations = _fixture_stations()

        def mock_ensure(filename: str, cache_dir: Path) -> tuple[Path, str | None]:
            # Write a tiny Excel-like file? No — just return a path.
            # We'll mock _parse_excel instead.
            return tmp_path / filename, "Wed, 15 Jan 2026 10:30:00 GMT"

        with (
            patch("idfkit.weather.index._ensure_index_file", side_effect=mock_ensure),
            patch("idfkit.weather.index._parse_excel", return_value=stations),
        ):
            idx = StationIndex.refresh(cache_dir=tmp_path)

        # The index should have stations (5 fixtures x 10 region files)
        assert len(idx) == len(stations) * 10

        # A compressed cache file should have been written
        cached = tmp_path / "stations.json.gz"
        assert cached.is_file()

        # Loading from cache should reproduce the same count
        idx2 = StationIndex.load(cache_dir=tmp_path)
        assert len(idx2) == len(idx)
