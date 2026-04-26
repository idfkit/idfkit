"""Tests for idfkit.weather.index (offline, no network)."""

from __future__ import annotations

import gzip
import json
import os
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from idfkit.weather.index import (
    StationIndex,
    _download_file,  # pyright: ignore[reportPrivateUsage]
    _ensure_index_file,  # pyright: ignore[reportPrivateUsage]
    _extract_wmo_from_filename,  # pyright: ignore[reportPrivateUsage]
    _head_last_modified,  # pyright: ignore[reportPrivateUsage]
    _is_epw_filename,  # pyright: ignore[reportPrivateUsage]
    _load_compressed_index,  # pyright: ignore[reportPrivateUsage]
    _parse_kml,  # pyright: ignore[reportPrivateUsage]
    _parse_url_metadata,  # pyright: ignore[reportPrivateUsage]
    _save_compressed_index,  # pyright: ignore[reportPrivateUsage]
    _score_station,  # pyright: ignore[reportPrivateUsage]
    _strip_weather_extension,  # pyright: ignore[reportPrivateUsage]
    default_cache_dir,
)
from idfkit.weather.station import WeatherStation


def _fixture_stations() -> list[WeatherStation]:
    """A small hand-crafted station list for search and spatial tests."""
    return [
        WeatherStation(
            country="USA",
            state="IL",
            city="Chicago.Ohare.Intl.AP",
            wmo="725300",
            source="TMYx.2009-2023",
            latitude=41.98,
            longitude=-87.92,
            timezone=-6.0,
            elevation=201.0,
            url="https://climate.onebuilding.org/WMO_Region_4_North_and_Central_America/USA_United_States_of_America/IL_Illinois/USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023.zip",
            ashrae_climate_zone="5A - Cool - Humid",
            heating_design_db_c=-17.4,
            cooling_design_db_c=32.5,
            hdd18=3454,
            cdd10=2103,
        ),
        WeatherStation(
            country="USA",
            state="IL",
            city="Chicago.Midway.AP",
            wmo="725340",
            source="TMYx.2009-2023",
            latitude=41.79,
            longitude=-87.75,
            timezone=-6.0,
            elevation=189.0,
            url="https://climate.onebuilding.org/WMO_Region_4_North_and_Central_America/USA_United_States_of_America/IL_Illinois/USA_IL_Chicago.Midway.AP.725340_TMYx.2009-2023.zip",
            ashrae_climate_zone="5A - Cool - Humid",
            heating_design_db_c=-17.0,
            cooling_design_db_c=32.6,
            hdd18=3380,
            cdd10=2155,
            design_conditions_source_wmo="725300",
        ),
        WeatherStation(
            country="USA",
            state="NY",
            city="New.York.J.F.Kennedy.Intl.AP",
            wmo="744860",
            source="TMYx",
            latitude=40.64,
            longitude=-73.76,
            timezone=-5.0,
            elevation=4.0,
            url="https://climate.onebuilding.org/WMO_Region_4_North_and_Central_America/USA_United_States_of_America/NY_New_York/USA_NY_New.York.J.F.Kennedy.Intl.AP.744860_TMYx.zip",
            ashrae_climate_zone="4A - Mixed - Humid",
            heating_design_db_c=-10.5,
            cooling_design_db_c=31.2,
            hdd18=2625,
            cdd10=1869,
        ),
        WeatherStation(
            country="GBR",
            state="",
            city="London.Heathrow.AP",
            wmo="037720",
            source="TMYx",
            latitude=51.48,
            longitude=-0.45,
            timezone=0.0,
            elevation=25.0,
            url="https://climate.onebuilding.org/WMO_Region_6_Europe/GBR_United_Kingdom/GBR_London.Heathrow.AP.037720_TMYx.zip",
            ashrae_climate_zone="4A - Mixed - Humid",
            heating_design_db_c=-3.4,
            cooling_design_db_c=27.4,
            hdd18=2387,
            cdd10=916,
        ),
        WeatherStation(
            country="FRA",
            state="",
            city="Paris.Orly.AP",
            wmo="071490",
            source="TMYx",
            latitude=48.73,
            longitude=2.40,
            timezone=1.0,
            elevation=89.0,
            url="https://climate.onebuilding.org/WMO_Region_6_Europe/FRA_France/FRA_Paris.Orly.AP.071490_TMYx.zip",
            ashrae_climate_zone="4A - Mixed - Humid",
            heating_design_db_c=-4.5,
            cooling_design_db_c=29.6,
            hdd18=2390,
            cdd10=1147,
        ),
    ]


# ---------------------------------------------------------------------------
# default_cache_dir (lines 46-54)
# ---------------------------------------------------------------------------


class TestDefaultCacheDir:
    def test_win32(self) -> None:
        with patch("idfkit.weather.index.sys") as mock_sys:
            mock_sys.platform = "win32"
            with patch.dict(os.environ, {"LOCALAPPDATA": "/tmp/appdata"}, clear=False):  # noqa: S108
                result = default_cache_dir()
                assert result == Path("/tmp/appdata/idfkit/cache/weather")  # noqa: S108

    def test_win32_fallback(self) -> None:
        with patch("idfkit.weather.index.sys") as mock_sys:
            mock_sys.platform = "win32"
            env = dict(os.environ)
            env.pop("LOCALAPPDATA", None)
            with patch.dict(os.environ, env, clear=True):
                result = default_cache_dir()
                assert "idfkit" in str(result)
                assert "cache" in str(result)

    def test_darwin(self) -> None:
        with patch("idfkit.weather.index.sys") as mock_sys:
            mock_sys.platform = "darwin"
            result = default_cache_dir()
            assert "Library/Caches/idfkit/weather" in result.as_posix()

    def test_linux_default(self) -> None:
        with patch("idfkit.weather.index.sys") as mock_sys:
            mock_sys.platform = "linux"
            env = dict(os.environ)
            env.pop("XDG_CACHE_HOME", None)
            with patch.dict(os.environ, env, clear=True):
                result = default_cache_dir()
                assert ".cache/idfkit/weather" in result.as_posix()

    def test_linux_xdg(self) -> None:
        with patch("idfkit.weather.index.sys") as mock_sys:
            mock_sys.platform = "linux"
            with patch.dict(os.environ, {"XDG_CACHE_HOME": "/tmp/xdg"}, clear=False):  # noqa: S108
                result = default_cache_dir()
                assert result == Path("/tmp/xdg/idfkit/weather")  # noqa: S108


# ---------------------------------------------------------------------------
# _download_file (lines 68-73)
# ---------------------------------------------------------------------------


class TestDownloadFile:
    def test_downloads_to_dest(self, tmp_path: Path) -> None:
        dest = tmp_path / "subdir" / "file.kml"
        mock_resp = MagicMock()
        mock_resp.read.return_value = b"data"
        mock_resp.headers.get.return_value = "Mon, 01 Jan 2024 00:00:00 GMT"
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)

        with patch("idfkit.weather.index.urlopen", return_value=mock_resp):
            lm = _download_file("https://example.com/file.kml", dest)

        assert dest.read_bytes() == b"data"
        assert lm == "Mon, 01 Jan 2024 00:00:00 GMT"

    def test_returns_none_when_no_header(self, tmp_path: Path) -> None:
        dest = tmp_path / "file.kml"
        mock_resp = MagicMock()
        mock_resp.read.return_value = b"data"
        mock_resp.headers.get.return_value = None
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)

        with patch("idfkit.weather.index.urlopen", return_value=mock_resp):
            lm = _download_file("https://example.com/file.kml", dest)

        assert lm is None


# ---------------------------------------------------------------------------
# _ensure_index_file (lines 82-91)
# ---------------------------------------------------------------------------


class TestEnsureIndexFile:
    def test_already_cached(self, tmp_path: Path) -> None:
        cached = tmp_path / "indexes" / "test.kml"
        cached.parent.mkdir(parents=True)
        cached.write_text("existing")
        path, lm = _ensure_index_file("test.kml", tmp_path)
        assert path == cached
        assert lm is None

    def test_downloads_on_miss(self, tmp_path: Path) -> None:
        mock_resp = MagicMock()
        mock_resp.read.return_value = b"<kml/>"
        mock_resp.headers.get.return_value = "Tue, 02 Jan 2024"
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)

        with patch("idfkit.weather.index.urlopen", return_value=mock_resp):
            path, lm = _ensure_index_file("Region1.kml", tmp_path)

        assert path.exists()
        assert lm == "Tue, 02 Jan 2024"

    def test_raises_on_download_error(self, tmp_path: Path) -> None:
        from urllib.error import URLError

        with (
            patch("idfkit.weather.index.urlopen", side_effect=URLError("connection failed")),
            pytest.raises(RuntimeError, match="Failed to download"),
        ):
            _ensure_index_file("Region1.kml", tmp_path)


# ---------------------------------------------------------------------------
# _parse_url_metadata
# ---------------------------------------------------------------------------


class TestParseUrlMetadata:
    def test_us_with_state(self) -> None:
        url = (
            "https://climate.onebuilding.org/WMO_Region_4_North_and_Central_America/"
            "USA_United_States_of_America/IL_Illinois/"
            "USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023.zip"
        )
        country, state, city, wmo = _parse_url_metadata(url)
        assert country == "USA"
        assert state == "IL"
        assert city == "Chicago.Ohare.Intl.AP"
        assert wmo == "725300"

    def test_non_us_no_state(self) -> None:
        url = (
            "https://climate.onebuilding.org/WMO_Region_6_Europe/"
            "GBR_United_Kingdom/GBR_London.Heathrow.AP.037720_TMYx.zip"
        )
        country, state, city, wmo = _parse_url_metadata(url)
        assert country == "GBR"
        assert state == ""
        assert city == "London.Heathrow.AP"
        assert wmo == "037720"  # Leading zero preserved

    def test_preserves_leading_zero(self) -> None:
        url = "https://example.com/FRA_Paris.Orly.AP.071490_TMYx.zip"
        _, _, _, wmo = _parse_url_metadata(url)
        assert wmo == "071490"


# ---------------------------------------------------------------------------
# _parse_kml
# ---------------------------------------------------------------------------


def _build_kml(placemarks_xml: str) -> str:
    """Wrap one or more placemark fragments in a minimal KML document."""
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<kml xmlns="http://earth.google.com/kml/2.1">'
        "<Document>"
        f"{placemarks_xml}"
        "</Document>"
        "</kml>"
    )


def _placemark(
    name: str,
    description: str | None,
    coords: str | None = "-87.92,41.98,201",
) -> str:
    parts = [f"<Placemark><name>{name}</name>"]
    if description is not None:
        parts.append(f"<description><![CDATA[{description}]]></description>")
    if coords is not None:
        parts.append(f"<Point><coordinates>{coords}</coordinates></Point>")
    parts.append("</Placemark>")
    return "".join(parts)


_FULL_DESCRIPTION = """<table>
<tr><td colspan="2"><b>USA IL Chicago.Ohare.Intl.AP.725300 TMYx.2009-2023</b></td></tr>
<tr><td><b>Data Source TMYx.2009-2023</td></tr>
<tr><td>WMO <b>725300</b></td></tr>
<tr><td>Elevation <b>201</b> m</td></tr>
<tr><td>Time Zone {GMT <b>-6.0</b> hours}</td></tr>
<tr><td>ASHRAE HOF 2025 Climate Zone <b>5A - Cool - Humid</b></td></tr>
<tr><td>99% Heating DB <b>-17.4 C</b>, <b>0.7 F</b></td></tr>
<tr><td>1% Cooling DB <b>32.5 C</b>, <b>90.5 F</b></td></tr>
<tr><td>HDD18 <b>3454</b>, CDD10 <b>2103</b></td></tr>
<tr><td>URL https://climate.onebuilding.org/WMO_Region_4_North_and_Central_America/USA_United_States_of_America/IL_Illinois/USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023.zip</td></tr>
</table>"""

_ALTERNATE_WMO_DESCRIPTION = """<table>
<tr><td><b>Data Source TMY3</td></tr>
<tr><td>Elevation <b>1</b> m</td></tr>
<tr><td>Time Zone {GMT <b>-10.0</b> hours}</td></tr>
<tr><td>ASHRAE HOF 2025 Climate Zone <b>0A - Extremely Hot - Humid</b></td></tr>
<tr><td>Design conditions from alternate WMO 911900</td></tr>
<tr><td>99% Heating DB <b>14.0 C</b>, <b>57.2 F</b></td></tr>
<tr><td>1% Cooling DB <b>30.0 C</b>, <b>86.0 F</b></td></tr>
<tr><td>HDD18 <b>0</b>, CDD10 <b>5444</b></td></tr>
<tr><td>URL https://climate.onebuilding.org/WMO_Region_5_Southwest_Pacific/USA_United_States_of_America/HI_Hawaii/USA_HI_Kapalua-West.Maui.AP.911900_TMY3.zip</td></tr>
</table>"""


class TestParseKml:
    def test_full_placemark(self, tmp_path: Path) -> None:
        kml = _build_kml(_placemark("Chicago O'Hare", _FULL_DESCRIPTION, "-87.92,41.98,201"))
        path = tmp_path / "test.kml"
        path.write_text(kml, encoding="utf-8")

        stations = _parse_kml(path)
        assert len(stations) == 1
        s = stations[0]
        assert s.country == "USA"
        assert s.state == "IL"
        assert s.city == "Chicago.Ohare.Intl.AP"
        assert s.wmo == "725300"
        assert s.source == "TMYx.2009-2023"
        assert s.latitude == 41.98
        assert s.longitude == -87.92
        assert s.timezone == -6.0
        assert s.elevation == 201.0
        assert s.ashrae_climate_zone == "5A - Cool - Humid"
        assert s.heating_design_db_c == -17.4
        assert s.cooling_design_db_c == 32.5
        assert s.hdd18 == 3454
        assert s.cdd10 == 2103
        assert s.design_conditions_source_wmo is None

    def test_alternate_wmo_annotation(self, tmp_path: Path) -> None:
        kml = _build_kml(_placemark("Kapalua", _ALTERNATE_WMO_DESCRIPTION, "-156.67,20.96,1"))
        path = tmp_path / "test.kml"
        path.write_text(kml, encoding="utf-8")

        stations = _parse_kml(path)
        assert len(stations) == 1
        assert stations[0].design_conditions_source_wmo == "911900"
        assert stations[0].ashrae_climate_zone == "0A - Extremely Hot - Humid"

    def test_sentinel_no_description(self, tmp_path: Path) -> None:
        """A region-label placemark with no description is skipped silently."""
        kml = _build_kml(
            _placemark("Region Label", description=None, coords="0,0,0")
            + _placemark("Chicago O'Hare", _FULL_DESCRIPTION, "-87.92,41.98,201")
        )
        path = tmp_path / "test.kml"
        path.write_text(kml, encoding="utf-8")

        stations = _parse_kml(path)
        assert len(stations) == 1
        assert stations[0].wmo == "725300"

    def test_sentinel_no_url(self, tmp_path: Path) -> None:
        """A placemark whose description has no download URL is skipped silently."""
        no_url = "<table><tr><td>Some metadata without a download link</td></tr></table>"
        kml = _build_kml(_placemark("Header", no_url, "0,0,0"))
        path = tmp_path / "test.kml"
        path.write_text(kml, encoding="utf-8")

        assert _parse_kml(path) == []

    def test_missing_required_field_raises(self, tmp_path: Path) -> None:
        """Real placemark missing a required climate field surfaces loudly."""
        broken = """<table>
<tr><td><b>Data Source TMYx</td></tr>
<tr><td>Elevation <b>10</b> m</td></tr>
<tr><td>Time Zone {GMT <b>0.0</b> hours}</td></tr>
<tr><td>99% Heating DB <b>-5.0 C</b>, <b>23.0 F</b></td></tr>
<tr><td>1% Cooling DB <b>30.0 C</b>, <b>86.0 F</b></td></tr>
<tr><td>HDD18 <b>2000</b>, CDD10 <b>1000</b></td></tr>
<tr><td>URL https://example.com/XYZ_Broken.Station.999999_TMYx.zip</td></tr>
</table>"""
        kml = _build_kml(_placemark("Broken Station", broken, "0,0,0"))
        path = tmp_path / "broken.kml"
        path.write_text(kml, encoding="utf-8")

        with pytest.raises(ValueError, match=r"climate_zone.*Broken Station|Broken Station.*climate_zone"):
            _parse_kml(path)

    def test_country_state_from_url(self, tmp_path: Path) -> None:
        """The non-US placemark exercises the no-state branch of URL parsing."""
        gbr_desc = """<table>
<tr><td><b>Data Source TMYx</td></tr>
<tr><td>Elevation <b>25</b> m</td></tr>
<tr><td>Time Zone {GMT <b>0.0</b> hours}</td></tr>
<tr><td>ASHRAE HOF 2025 Climate Zone <b>4A - Mixed - Humid</b></td></tr>
<tr><td>99% Heating DB <b>-3.4 C</b>, <b>25.9 F</b></td></tr>
<tr><td>1% Cooling DB <b>27.4 C</b>, <b>81.3 F</b></td></tr>
<tr><td>HDD18 <b>2387</b>, CDD10 <b>916</b></td></tr>
<tr><td>URL https://climate.onebuilding.org/WMO_Region_6_Europe/GBR_United_Kingdom/GBR_London.Heathrow.AP.037720_TMYx.zip</td></tr>
</table>"""
        kml = _build_kml(_placemark("London Heathrow", gbr_desc, "-0.45,51.48,25"))
        path = tmp_path / "gbr.kml"
        path.write_text(kml, encoding="utf-8")

        stations = _parse_kml(path)
        assert len(stations) == 1
        s = stations[0]
        assert s.country == "GBR"
        assert s.state == ""
        assert s.city == "London.Heathrow.AP"
        assert s.wmo == "037720"


# ---------------------------------------------------------------------------
# _head_last_modified (lines 190-195)
# ---------------------------------------------------------------------------


class TestHeadLastModified:
    def test_returns_header(self) -> None:
        mock_resp = MagicMock()
        mock_resp.headers.get.return_value = "Wed, 03 Jan 2024"
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)

        with patch("idfkit.weather.index.urlopen", return_value=mock_resp):
            result = _head_last_modified("https://example.com/file")
        assert result == "Wed, 03 Jan 2024"

    def test_returns_none_on_error(self) -> None:
        from urllib.error import URLError

        with patch("idfkit.weather.index.urlopen", side_effect=URLError("offline")):
            result = _head_last_modified("https://example.com/file")
        assert result is None


# ---------------------------------------------------------------------------
# EPW filename helpers (lines 249, etc.)
# ---------------------------------------------------------------------------


class TestEpwFilenameDetection:
    def test_us_filename(self) -> None:
        assert _is_epw_filename("USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023")

    def test_non_us_filename(self) -> None:
        assert _is_epw_filename("GBR_London.Heathrow.AP.037720_TMYx")

    def test_filename_with_extension(self) -> None:
        assert _is_epw_filename("USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023.zip")
        assert _is_epw_filename("USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023.epw")

    def test_plain_query_not_detected(self) -> None:
        assert not _is_epw_filename("chicago ohare")

    def test_wmo_only_not_detected(self) -> None:
        assert not _is_epw_filename("725300")

    def test_extract_wmo(self) -> None:
        assert _extract_wmo_from_filename("USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023") == "725300"

    def test_extract_wmo_leading_zeros(self) -> None:
        assert _extract_wmo_from_filename("GBR_London.Heathrow.AP.037720_TMYx") == "037720"

    def test_extract_wmo_with_extension(self) -> None:
        assert _extract_wmo_from_filename("USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023.zip") == "725300"

    def test_extract_wmo_no_underscore(self) -> None:
        """No underscore means rsplit gives < 2 parts -> None."""
        assert _extract_wmo_from_filename("nodots") is None

    def test_extract_wmo_no_digit_suffix(self) -> None:
        """Prefix has no digit-only last dot-part -> None (line 249)."""
        assert _extract_wmo_from_filename("USA_TMYx") is None

    def test_strip_weather_extension(self) -> None:
        assert _strip_weather_extension("file.zip") == "file"
        assert _strip_weather_extension("file.epw") == "file"
        assert _strip_weather_extension("file.ddy") == "file"
        assert _strip_weather_extension("file.stat") == "file"
        assert _strip_weather_extension("file.txt") == "file.txt"


# ---------------------------------------------------------------------------
# _score_station (lines 276-296)
# ---------------------------------------------------------------------------


class TestScoreStation:
    def test_exact_wmo_match(self) -> None:
        station = _fixture_stations()[0]
        score, field = _score_station(station, "725300", ["725300"])
        assert score == 1.0
        assert field == "wmo"

    def test_display_name_substring(self) -> None:
        station = _fixture_stations()[0]
        # "chicago ohare" is a substring of the display name
        score, field = _score_station(station, "chicago ohare", ["chicago", "ohare"])
        assert score > 0.85
        assert field == "name"

    def test_city_name_substring(self) -> None:
        """Query matches city (dots->spaces) but not display_name (lines 276-277).

        The city name (lowered, dots/dashes to spaces) is 'chicago ohare intl ap'.
        The display_name is 'Chicago Ohare Intl AP, IL, USA' -> lowered.
        Since city is always a prefix of display_name, signal 2 fires first.
        This signal is hard to reach independently, but we still test the path
        via a query that's a substring of city.
        """
        station = _fixture_stations()[0]
        score, field = _score_station(station, "ohare intl", ["ohare", "intl"])
        assert score > 0.85
        assert field == "name"

    def test_all_tokens_prefix_match(self) -> None:
        """All query tokens are prefixes of name tokens (lines 282-283).

        Station: New.York.J.F.Kennedy.Intl.AP -> name_lower = "new york j f kennedy intl ap" (28 chars)
        tokens: ["new", "ken"] -> total token length = 6
        coverage = 6/28; score = 0.6 + 0.3 * (6/28)
        """
        station = _fixture_stations()[2]  # New.York.J.F.Kennedy.Intl.AP
        # Tokens: "new", "ken" — "new" prefixes "new", "ken" prefixes "kennedy"
        score, field = _score_station(station, "new ken", ["new", "ken"])
        assert score == pytest.approx(0.6 + 0.3 * 6 / 28)
        assert field == "name"

    def test_partial_token_overlap(self) -> None:
        """Only some tokens match (lines 286->293, 288-290).

        Station: New.York.J.F.Kennedy.Intl.AP
        tokens: ["new", "zzz"] -> "new" matches, "zzz" does not -> matching=1, ratio=1/2
        score = 0.3 * (1/2) = 0.15
        """
        station = _fixture_stations()[2]  # New.York.J.F.Kennedy.Intl.AP
        score, field = _score_station(station, "new zzz", ["new", "zzz"])
        assert score == pytest.approx(0.15)
        assert field == "name"

    def test_no_match(self) -> None:
        station = _fixture_stations()[0]
        score, field = _score_station(station, "zzzzz", ["zzzzz"])
        assert score == 0.0
        assert field == ""


# ---------------------------------------------------------------------------
# StationIndex
# ---------------------------------------------------------------------------


class TestStationIndex:
    def test_len(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        assert len(idx) == 5

    def test_stations_property(self) -> None:
        """Property returns a copy (line 431)."""
        idx = StationIndex.from_stations(_fixture_stations())
        stations = idx.stations
        assert len(stations) == 5
        stations.clear()
        assert len(idx) == 5

    def test_get_by_wmo(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.get_by_wmo("725300")
        assert len(results) == 1
        assert results[0].city == "Chicago.Ohare.Intl.AP"

    def test_get_by_wmo_missing(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        assert idx.get_by_wmo("999999") == []


class TestSearch:
    def test_exact_wmo(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.search("725300")
        assert len(results) >= 1
        assert results[0].station.wmo == "725300"
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
        assert results[0].station.wmo == "725340"

    def test_country_filter(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.search("ap", country="GBR")
        assert all(r.station.country == "GBR" for r in results)

    def test_empty_query(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        assert idx.search("") == []

    def test_whitespace_only_query(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        assert idx.search("   ") == []

    def test_no_match(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.search("zzzznonexistent")
        assert results == []

    def test_search_epw_filename(self) -> None:
        """search() should recognize EPW filenames and return score 1.0 (line 511->519)."""
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.search("USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023")
        assert len(results) >= 1
        assert results[0].station.wmo == "725300"
        assert results[0].score == 1.0
        assert results[0].match_field == "filename"

    def test_search_epw_filename_with_extension(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.search("USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023.epw")
        assert len(results) >= 1
        assert results[0].score == 1.0

    def test_search_epw_filename_country_filter(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.search("GBR_London.Heathrow.AP.037720_TMYx", country="GBR")
        assert len(results) >= 1
        assert results[0].station.country == "GBR"

    def test_search_epw_filename_wrong_country_filter(self) -> None:
        """EPW filename match filtered out by country -> empty (line 515)."""
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.search("USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023", country="GBR")
        assert results == []

    def test_search_epw_filename_no_match_falls_through(self) -> None:
        """When EPW filename doesn't resolve, fall through to text search (line 511->519)."""
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.search("ZZZ_Fake.Station.999999_TMYx")
        assert len(results) == 0


class TestGetByFilename:
    def test_exact_filename_stem(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.get_by_filename("USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023")
        assert len(results) == 1
        assert results[0].wmo == "725300"

    def test_filename_with_zip_extension(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.get_by_filename("USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023.zip")
        assert len(results) == 1

    def test_filename_with_epw_extension(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.get_by_filename("USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023.epw")
        assert len(results) == 1

    def test_case_insensitive(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.get_by_filename("usa_il_chicago.ohare.intl.ap.725300_tmyx.2009-2023")
        assert len(results) == 1

    def test_non_us_station(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.get_by_filename("GBR_London.Heathrow.AP.037720_TMYx")
        assert len(results) == 1
        assert results[0].country == "GBR"

    def test_non_us_station_france(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.get_by_filename("FRA_Paris.Orly.AP.071490_TMYx")
        assert len(results) == 1
        assert results[0].country == "FRA"

    def test_wmo_fallback(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.get_by_filename("USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2007-2021")
        assert len(results) == 1
        assert results[0].wmo == "725300"

    def test_no_match_returns_empty(self) -> None:
        """Neither exact filename nor WMO extraction yields results (line 478)."""
        idx = StationIndex.from_stations(_fixture_stations())
        assert idx.get_by_filename("ZZZ_Nonexistent.Station.999999_TMYx") == []

    def test_no_wmo_no_exact_returns_empty(self) -> None:
        """Filename without extractable WMO and no exact match -> empty (line 478)."""
        idx = StationIndex.from_stations(_fixture_stations())
        assert idx.get_by_filename("no_match_here") == []


class TestNearest:
    def test_nearest_to_chicago(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.nearest(41.88, -87.63, limit=3)
        assert len(results) == 3
        assert results[0].station.wmo == "725340"
        assert results[1].station.wmo == "725300"
        assert results[0].distance_km < 30.0

    def test_max_distance_filter(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.nearest(41.88, -87.63, max_distance_km=50.0)
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

    def test_max_distance_excludes_all(self) -> None:
        """Very small max_distance excludes everything (line 580)."""
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.nearest(0.0, 0.0, max_distance_km=1.0)
        assert results == []

    def test_max_distance_haversine_exceeds(self) -> None:
        """Station passes bounding-box but fails haversine check (line 580).

        A station at (0.35, 0.35) from origin (0, 0) is ~55 km away by
        haversine, but falls well inside the bounding box for max_distance=50 km
        (which extends ~1.45 degrees in each direction). This exercises the
        haversine > max_distance branch on line 580.
        """
        corner_station = WeatherStation(
            country="TST",
            state="",
            city="Corner",
            wmo="000099",
            source="",
            latitude=0.35,
            longitude=0.35,
            timezone=0.0,
            elevation=0.0,
            url="",
            ashrae_climate_zone="0A - Extremely Hot - Humid",
            heating_design_db_c=15.0,
            cooling_design_db_c=35.0,
            hdd18=0,
            cdd10=5000,
        )
        idx = StationIndex.from_stations([corner_station])
        results = idx.nearest(0.0, 0.0, max_distance_km=50.0)
        assert results == []  # ~55 km > 50 km limit


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
        assert results[0].wmo == "744860"

    def test_filter_by_wmo_region(self) -> None:
        """Filter by WMO region number in URL (lines 607-609)."""
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.filter(wmo_region=4)
        assert len(results) == 3  # USA stations have WMO_Region_4 in URL
        results_eu = idx.filter(wmo_region=6)
        assert len(results_eu) == 2  # GBR + FRA have WMO_Region_6

    def test_filter_by_wmo_region_no_match(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        results = idx.filter(wmo_region=7)
        assert results == []

    def test_countries(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        assert idx.countries == ["FRA", "GBR", "USA"]


# ---------------------------------------------------------------------------
# Compressed index (bundled / cache) tests
# ---------------------------------------------------------------------------


class TestCompressedIndex:
    def test_save_and_load_round_trip(self, tmp_path: Path) -> None:
        stations = _fixture_stations()
        last_modified = {"file_a.kml": "Wed, 15 Jan 2026 10:30:00 GMT"}
        dest = tmp_path / "stations.json.gz"

        _save_compressed_index(stations, last_modified, dest)
        loaded_stations, loaded_lm, built_at = _load_compressed_index(dest)

        assert len(loaded_stations) == len(stations)
        assert loaded_stations[0] == stations[0]
        # New climate fields and the alternate-WMO override survive the round-trip.
        assert loaded_stations[0].ashrae_climate_zone == "5A - Cool - Humid"
        assert loaded_stations[0].heating_design_db_c == -17.4
        assert loaded_stations[1].design_conditions_source_wmo == "725300"
        assert loaded_stations[2].design_conditions_source_wmo is None
        assert loaded_lm == last_modified
        assert built_at

    def test_empty_index(self, tmp_path: Path) -> None:
        dest = tmp_path / "empty.json.gz"
        _save_compressed_index([], {}, dest)
        stations, lm, _ = _load_compressed_index(dest)
        assert stations == []
        assert lm == {}

    def test_load_missing_metadata(self, tmp_path: Path) -> None:
        """Load a file with no last_modified or built_at keys."""
        data: dict[str, Any] = {"stations": [_fixture_stations()[0].to_dict()]}
        dest = tmp_path / "minimal.json.gz"
        with gzip.open(dest, "wt", encoding="utf-8") as f:
            json.dump(data, f)
        stations, lm, built_at = _load_compressed_index(dest)
        assert len(stations) == 1
        assert lm == {}
        assert built_at == ""


class TestLoadBundled:
    def test_load_from_bundled(self) -> None:
        idx = StationIndex.load(cache_dir=Path("/nonexistent/cache/dir"))
        assert len(idx) > 0

    def test_load_from_cache_takes_priority(self, tmp_path: Path) -> None:
        stations = _fixture_stations()[:2]
        last_modified = {"test.kml": "Mon, 01 Jan 2026 00:00:00 GMT"}
        dest = tmp_path / "stations.json.gz"
        _save_compressed_index(stations, last_modified, dest)

        idx = StationIndex.load(cache_dir=tmp_path)
        assert len(idx) == 2

    def test_load_missing_raises(self, tmp_path: Path) -> None:
        with (
            patch("idfkit.weather.index._BUNDLED_INDEX", tmp_path / "nope.json.gz"),
            pytest.raises(FileNotFoundError, match="No station index found"),
        ):
            StationIndex.load(cache_dir=tmp_path)


class TestCheckForUpdates:
    def test_stale_returns_true(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        idx._last_modified = {  # pyright: ignore[reportPrivateUsage]
            "Region1_Africa_TMYx_EPW_Processing_locations.kml": "Wed, 01 Jan 2020 00:00:00 GMT",
        }
        with patch(
            "idfkit.weather.index._head_last_modified",
            return_value="Wed, 15 Jan 2026 10:30:00 GMT",
        ):
            assert idx.check_for_updates() is True

    def test_fresh_returns_false(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        same_date = "Wed, 15 Jan 2026 10:30:00 GMT"
        idx._last_modified = {  # pyright: ignore[reportPrivateUsage]
            "Region1_Africa_TMYx_EPW_Processing_locations.kml": same_date,
        }
        with patch("idfkit.weather.index._head_last_modified", return_value=same_date):
            assert idx.check_for_updates() is False

    def test_offline_returns_false(self) -> None:
        idx = StationIndex.from_stations(_fixture_stations())
        idx._last_modified = {  # pyright: ignore[reportPrivateUsage]
            "Region1_Africa_TMYx_EPW_Processing_locations.kml": "Wed, 01 Jan 2020 00:00:00 GMT",
        }
        with patch("idfkit.weather.index._head_last_modified", return_value=None):
            assert idx.check_for_updates() is False

    def test_no_metadata_returns_false(self) -> None:
        """Empty _last_modified -> returns False immediately (line 393->395)."""
        idx = StationIndex.from_stations(_fixture_stations())
        assert idx.check_for_updates() is False


class TestRefresh:
    def test_refresh_saves_and_loads(self, tmp_path: Path) -> None:
        stations = _fixture_stations()

        def mock_ensure(filename: str, cache_dir: Path) -> tuple[Path, str | None]:
            return tmp_path / filename, "Wed, 15 Jan 2026 10:30:00 GMT"

        with (
            patch("idfkit.weather.index._ensure_index_file", side_effect=mock_ensure),
            patch("idfkit.weather.index._parse_kml", return_value=stations),
        ):
            idx = StationIndex.refresh(cache_dir=tmp_path)

        assert len(idx) == len(stations) * 10

        cached = tmp_path / "stations.json.gz"
        assert cached.is_file()

        idx2 = StationIndex.load(cache_dir=tmp_path)
        assert len(idx2) == len(idx)
