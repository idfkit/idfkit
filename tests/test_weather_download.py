"""Tests for idfkit.weather.download (mocked, no network)."""

from __future__ import annotations

import io
import time
import zipfile
from datetime import timedelta
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
        wmo="725300",
        source="SRC-TMYx",
        latitude=41.98,
        longitude=-87.92,
        timezone=-6.0,
        elevation=201.0,
        url="https://climate.onebuilding.org/WMO_Region_4/USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023.zip",
    )


def _make_zip_bytes(
    epw_content: str = "LOCATION,Chicago",
    ddy_content: str = "Version,25.2;",
    include_stat: bool = True,
) -> bytes:
    """Create a minimal ZIP archive in memory."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023.epw", epw_content)
        zf.writestr("USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023.ddy", ddy_content)
        if include_stat:
            zf.writestr("USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023.stat", "Stats")
    return buf.getvalue()


def _make_zip_without_epw() -> bytes:
    """Create a ZIP archive without an EPW file."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("readme.txt", "no weather files here")
    return buf.getvalue()


def _make_zip_without_ddy() -> bytes:
    """Create a ZIP archive with EPW but no DDY."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("station.epw", "LOCATION,Chicago")
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

        downloader.download(station)
        assert mock_urlopen.call_count == 1

        downloader.download(station)
        assert mock_urlopen.call_count == 1

    def test_clear_cache(self, tmp_path: Path) -> None:
        files_dir = tmp_path / "files" / "725300"
        files_dir.mkdir(parents=True)
        (files_dir / "dummy.epw").write_text("test")

        downloader = WeatherDownloader(cache_dir=tmp_path)
        downloader.clear_cache()

        assert not files_dir.exists()

    def test_clear_cache_no_files_dir(self, tmp_path: Path) -> None:
        """clear_cache when files dir doesn't exist is a no-op (line 240->exit)."""
        files_dir = tmp_path / "files"
        assert not files_dir.exists()
        downloader = WeatherDownloader(cache_dir=tmp_path)
        downloader.clear_cache()  # Should not raise
        assert not files_dir.exists()  # Still doesn't exist — no side effects

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

    @patch("idfkit.weather.download.urlopen")
    def test_bad_zip_raises(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        """BadZipFile during extraction raises RuntimeError (lines 145-147)."""
        mock_resp = MagicMock()
        mock_resp.read.return_value = b"this is not a zip file"
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        downloader = WeatherDownloader(cache_dir=tmp_path)
        station = _make_station()

        with pytest.raises(RuntimeError, match="not a valid ZIP"):
            downloader.download(station)

    @patch("idfkit.weather.download.urlopen")
    def test_no_epw_in_archive_raises(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        """No .epw file in archive raises RuntimeError (lines 151-152)."""
        mock_resp = MagicMock()
        mock_resp.read.return_value = _make_zip_without_epw()
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        downloader = WeatherDownloader(cache_dir=tmp_path)
        station = _make_station()

        with pytest.raises(RuntimeError, match=r"No .epw file found"):
            downloader.download(station)

    @patch("idfkit.weather.download.urlopen")
    def test_no_ddy_in_archive_raises(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        """No .ddy file in archive raises RuntimeError (lines 156-157)."""
        mock_resp = MagicMock()
        mock_resp.read.return_value = _make_zip_without_ddy()
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        downloader = WeatherDownloader(cache_dir=tmp_path)
        station = _make_station()

        with pytest.raises(RuntimeError, match=r"No .ddy file found"):
            downloader.download(station)


class TestWeatherDownloaderMaxAge:
    @patch("idfkit.weather.download.urlopen")
    def test_max_age_with_timedelta(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        mock_resp = MagicMock()
        mock_resp.read.return_value = _make_zip_bytes()
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        downloader = WeatherDownloader(cache_dir=tmp_path, max_age=timedelta(days=30))
        station = _make_station()

        files = downloader.download(station)
        assert files.epw.exists()
        assert mock_urlopen.call_count == 1

    @patch("idfkit.weather.download.urlopen")
    def test_max_age_with_seconds(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        mock_resp = MagicMock()
        mock_resp.read.return_value = _make_zip_bytes()
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        downloader = WeatherDownloader(cache_dir=tmp_path, max_age=3600.0)
        station = _make_station()

        files = downloader.download(station)
        assert files.epw.exists()

    @patch("idfkit.weather.download.urlopen")
    @patch("idfkit.weather.download.time")
    def test_stale_cache_redownloads(self, mock_time: MagicMock, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        mock_resp = MagicMock()
        mock_resp.read.return_value = _make_zip_bytes()
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        mock_time.time.return_value = time.time() + 86400 * 60

        downloader = WeatherDownloader(cache_dir=tmp_path, max_age=timedelta(days=30))
        station = _make_station()

        downloader.download(station)
        assert mock_urlopen.call_count == 1

        downloader.download(station)
        assert mock_urlopen.call_count == 2

    @patch("idfkit.weather.download.urlopen")
    def test_fresh_cache_no_redownload(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        mock_resp = MagicMock()
        mock_resp.read.return_value = _make_zip_bytes()
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        downloader = WeatherDownloader(cache_dir=tmp_path, max_age=timedelta(days=30))
        station = _make_station()

        downloader.download(station)
        assert mock_urlopen.call_count == 1

        downloader.download(station)
        assert mock_urlopen.call_count == 1

    def test_none_max_age_never_expires(self, tmp_path: Path) -> None:
        downloader = WeatherDownloader(cache_dir=tmp_path, max_age=None)
        files_dir = tmp_path / "files" / "test"
        files_dir.mkdir(parents=True)
        test_file = files_dir / "old.zip"
        test_file.write_text("test")

        assert not downloader._is_stale(test_file)  # pyright: ignore[reportPrivateUsage]

    def test_is_stale_nonexistent_path(self, tmp_path: Path) -> None:
        """_is_stale returns True for non-existent file when max_age is set (line 95)."""
        downloader = WeatherDownloader(cache_dir=tmp_path, max_age=3600.0)
        assert downloader._is_stale(tmp_path / "nonexistent.zip")  # pyright: ignore[reportPrivateUsage]


class TestGetEpwByFilename:
    @patch("idfkit.weather.download.urlopen")
    def test_download_by_filename(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        mock_resp = MagicMock()
        mock_resp.read.return_value = _make_zip_bytes()
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        from idfkit.weather.index import StationIndex

        index = StationIndex.from_stations([_make_station()])

        downloader = WeatherDownloader(cache_dir=tmp_path)
        epw = downloader.get_epw_by_filename(
            "USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023",
            index=index,
        )
        assert epw.suffix == ".epw"

    @patch("idfkit.weather.download.urlopen")
    def test_download_ddy_by_filename(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        mock_resp = MagicMock()
        mock_resp.read.return_value = _make_zip_bytes()
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        from idfkit.weather.index import StationIndex

        index = StationIndex.from_stations([_make_station()])

        downloader = WeatherDownloader(cache_dir=tmp_path)
        ddy = downloader.get_ddy_by_filename(
            "USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023",
            index=index,
        )
        assert ddy.suffix == ".ddy"

    def test_unknown_filename_raises(self, tmp_path: Path) -> None:
        from idfkit.weather.index import StationIndex

        index = StationIndex.from_stations([_make_station()])

        downloader = WeatherDownloader(cache_dir=tmp_path)
        with pytest.raises(ValueError, match="No weather station found"):
            downloader.get_epw_by_filename("ZZZ_Nonexistent.999999_TMYx", index=index)

    @patch("idfkit.weather.download.urlopen")
    def test_resolve_filename_loads_default_index(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        """_resolve_filename with index=None loads default StationIndex (lines 180-182)."""
        from idfkit.weather.index import StationIndex

        mock_resp = MagicMock()
        mock_resp.read.return_value = _make_zip_bytes()
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        controlled_index = StationIndex.from_stations([_make_station()])

        downloader = WeatherDownloader(cache_dir=tmp_path)
        with patch.object(StationIndex, "load", return_value=controlled_index) as mock_load:
            # Call with index=None to trigger the auto-load path
            epw = downloader.get_epw_by_filename(
                "USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023",
            )
        mock_load.assert_called_once()
        assert epw.suffix == ".epw"
