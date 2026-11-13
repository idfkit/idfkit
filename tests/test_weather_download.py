"""Tests for idfkit.weather.download (mocked, no network)."""

from __future__ import annotations

import io
import os
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
        source="TMYx.2009-2023",
        latitude=41.98,
        longitude=-87.92,
        timezone=-6.0,
        elevation=201.0,
        url="https://climate.onebuilding.org/WMO_Region_4/USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023.zip",
        ashrae_climate_zone="5A - Cool - Humid",
        heating_design_db_c=-17.4,
        cooling_design_db_c=32.5,
        hdd18=3454,
        cdd10=2103,
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


class TestSelectiveExtraction:
    """``download(only=...)`` extracts only the requested members."""

    @patch("idfkit.weather.download.urlopen")
    def test_only_epw_skips_ddy_and_stat(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        mock_resp = MagicMock()
        mock_resp.read.return_value = _make_zip_bytes()
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        downloader = WeatherDownloader(cache_dir=tmp_path)
        station = _make_station()
        files = downloader.download(station, only={".epw"})

        assert files.epw is not None and files.epw.exists()
        assert files.ddy is None
        assert files.stat is None
        # Only the EPW landed on disk next to the ZIP.
        siblings = sorted(p.suffix.lower() for p in files.zip_path.parent.iterdir() if p.is_file())
        assert siblings == [".epw", ".zip"]

    @patch("idfkit.weather.download.urlopen")
    def test_only_normalises_suffix_forms(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        """Bare extension, missing dot, and uppercase all match the same members."""
        mock_resp = MagicMock()
        mock_resp.read.return_value = _make_zip_bytes()
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        downloader = WeatherDownloader(cache_dir=tmp_path)
        station = _make_station()
        files = downloader.download(station, only=["EPW", ".DDY"])

        assert files.epw is not None and files.epw.exists()
        assert files.ddy is not None and files.ddy.exists()
        assert files.stat is None

    @patch("idfkit.weather.download.urlopen")
    def test_only_does_not_raise_when_member_missing(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        """A missing requested member yields ``None``; selective mode never raises for that."""
        mock_resp = MagicMock()
        mock_resp.read.return_value = _make_zip_without_ddy()  # has EPW, no DDY
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        downloader = WeatherDownloader(cache_dir=tmp_path)
        station = _make_station()
        files = downloader.download(station, only={".ddy"})

        assert files.ddy is None
        # Full-extract requirement does NOT apply in selective mode.

    @patch("idfkit.weather.download.urlopen")
    def test_selective_after_full_returns_already_extracted(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        """If a prior full download cached every file, selective still surfaces them."""
        mock_resp = MagicMock()
        mock_resp.read.return_value = _make_zip_bytes()
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        downloader = WeatherDownloader(cache_dir=tmp_path)
        station = _make_station()
        downloader.download(station)  # full extract populates the cache dir
        files = downloader.download(station, only={".epw"})

        # We didn't request the DDY/stat, but they're on disk from the prior call.
        assert files.epw is not None
        assert files.ddy is not None
        assert files.stat is not None


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


class TestCacheConsistency:
    """What the extractor does with archive members and with damaged cache entries."""

    @staticmethod
    def _serve(payload: bytes) -> MagicMock:
        mock = MagicMock(side_effect=lambda *_a, **_k: io.BytesIO(payload))
        return mock

    def test_nested_and_macos_resource_members_are_skipped(self, tmp_path: Path) -> None:
        # Flat extraction put __MACOSX/._x.epw beside the real file, where _find_file could pick it.
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("__MACOSX/._a.epw", b"\x00\x05\x16\x07 resource fork")
            zf.writestr("._a.ddy", b"\x00\x05\x16\x07 resource fork")
            zf.writestr("2004-2018/old.epw", "LOCATION,old")
            zf.writestr("a.epw", "LOCATION,Chicago")
            zf.writestr("a.ddy", "Version,25.2;")
        with patch("idfkit.weather.download.urlopen", self._serve(buf.getvalue())):
            files = WeatherDownloader(cache_dir=tmp_path).download(_make_station())

        assert files.epw.read_text() == "LOCATION,Chicago"
        assert {p.name for p in files.epw.parent.iterdir()} == {"a.ddy", "a.epw", files.zip_path.name}

    def test_members_carry_their_archives_mtime(self, tmp_path: Path) -> None:
        # Stamped with the archive's mtime, a member extracted from an archive another process has
        # since replaced is older than the new archive, so the next call extracts it again.
        downloader = WeatherDownloader(cache_dir=tmp_path)
        with patch("idfkit.weather.download.urlopen", self._serve(_make_zip_bytes(epw_content="LOCATION,v1"))):
            files = downloader.download(_make_station())
        assert files.epw.stat().st_mtime_ns == files.zip_path.stat().st_mtime_ns

        files.zip_path.write_bytes(_make_zip_bytes(epw_content="LOCATION,v2"))
        later = files.zip_path.stat().st_mtime_ns + 10**9
        os.utime(files.zip_path, ns=(later, later))

        assert downloader.download(_make_station()).epw.read_text() == "LOCATION,v2"

    def test_a_truncated_member_is_extracted_again(self, tmp_path: Path) -> None:
        # The old in-place writes could leave a truncated member newer than its archive, which the
        # mtime check alone kept serving for good.
        downloader = WeatherDownloader(cache_dir=tmp_path)
        epw = "LOCATION,Chicago\n" + "row\n" * 1000
        with patch("idfkit.weather.download.urlopen", self._serve(_make_zip_bytes(epw_content=epw))):
            files = downloader.download(_make_station())
        files.epw.write_text(epw[:100])

        assert downloader.download(_make_station()).epw.read_text() == epw

    def test_a_corrupt_archive_is_downloaded_again_next_time(self, tmp_path: Path) -> None:
        downloader = WeatherDownloader(cache_dir=tmp_path)
        urlopen = self._serve(_make_zip_bytes())
        with patch("idfkit.weather.download.urlopen", urlopen):
            files = downloader.download(_make_station())
            files.zip_path.write_bytes(b"PK\x03\x04 truncated")
            for member in files.epw.parent.glob("*.epw"):
                member.unlink()

            with pytest.raises(RuntimeError, match="not a valid ZIP"):
                downloader.download(_make_station())
            assert downloader.download(_make_station()).epw.read_text() == "LOCATION,Chicago"

        assert urlopen.call_count == 2

    def test_a_ddy_cached_uncleaned_by_an_old_version_is_cleaned_once(self, tmp_path: Path) -> None:
        downloader = WeatherDownloader(cache_dir=tmp_path)
        with patch("idfkit.weather.download.urlopen", self._serve(_make_zip_bytes())):
            files = downloader.download(_make_station())
        dirty = "SizingPeriod:DesignDay,\n  Chicago Ann Htg 99.6% Condns DB,  !- Name\n  N;  !- Wind Speed\n"
        files.ddy.write_text(dirty)
        stamp = files.zip_path.stat().st_mtime_ns
        os.utime(files.ddy, ns=(stamp, stamp))

        cleaned = downloader.download(_make_station()).ddy

        assert "N;" not in cleaned.read_text()
        assert cleaned.stat().st_mtime_ns == stamp, "cleaning must not make the DDY look newer than its archive"
