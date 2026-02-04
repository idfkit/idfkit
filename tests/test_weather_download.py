"""Tests for idfkit.weather.download (mocked, no network)."""

from __future__ import annotations

import io
import zipfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from idfkit.weather.download import WeatherDownloader
from idfkit.weather.station import WeatherStation


def _make_station() -> WeatherStation:
    return WeatherStation(
        country="USA",
        state="IL",
        city="Chicago.Ohare.Intl.AP",
        wmo=725300,
        source="SRC-TMYx",
        latitude=41.98,
        longitude=-87.92,
        timezone=-6.0,
        elevation=201.0,
        url="https://climate.onebuilding.org/WMO_Region_4/USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023.zip",
    )


def _make_zip_bytes(epw_content: str = "LOCATION,Chicago", ddy_content: str = "Version,25.2;") -> bytes:
    """Create a minimal ZIP archive in memory."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023.epw", epw_content)
        zf.writestr("USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023.ddy", ddy_content)
        zf.writestr("USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023.stat", "Stats")
    return buf.getvalue()


class TestWeatherDownloader:
    @patch("idfkit.weather.download.urlopen")
    def test_download_and_extract(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        mock_resp = MagicMock()
        mock_resp.read.return_value = _make_zip_bytes()
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        downloader = WeatherDownloader(cache_dir=tmp_path)
        station = _make_station()
        files = downloader.download(station)

        assert files.epw.exists()
        assert files.ddy.exists()
        assert files.stat is not None and files.stat.exists()
        assert files.station is station
        assert files.epw.suffix == ".epw"
        assert files.ddy.suffix == ".ddy"

    @patch("idfkit.weather.download.urlopen")
    def test_cache_hit_no_redownload(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        mock_resp = MagicMock()
        mock_resp.read.return_value = _make_zip_bytes()
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        downloader = WeatherDownloader(cache_dir=tmp_path)
        station = _make_station()

        # First download
        downloader.download(station)
        assert mock_urlopen.call_count == 1

        # Second download should be cached
        downloader.download(station)
        assert mock_urlopen.call_count == 1  # No additional call

    def test_clear_cache(self, tmp_path: Path) -> None:
        # Create a fake cached file
        files_dir = tmp_path / "files" / "725300"
        files_dir.mkdir(parents=True)
        (files_dir / "dummy.epw").write_text("test")

        downloader = WeatherDownloader(cache_dir=tmp_path)
        downloader.clear_cache()

        assert not files_dir.exists()

    @patch("idfkit.weather.download.urlopen")
    def test_get_epw(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        mock_resp = MagicMock()
        mock_resp.read.return_value = _make_zip_bytes()
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        downloader = WeatherDownloader(cache_dir=tmp_path)
        station = _make_station()
        epw = downloader.get_epw(station)
        assert epw.suffix == ".epw"

    @patch("idfkit.weather.download.urlopen")
    def test_download_failure_raises(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        from urllib.error import URLError

        mock_urlopen.side_effect = URLError("Connection refused")

        downloader = WeatherDownloader(cache_dir=tmp_path)
        station = _make_station()

        with pytest.raises(RuntimeError, match="Failed to download"):
            downloader.download(station)
