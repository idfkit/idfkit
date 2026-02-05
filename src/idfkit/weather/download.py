"""Download EPW, DDY, and related weather files from climate.onebuilding.org."""

from __future__ import annotations

import shutil
import time
import zipfile
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .index import default_cache_dir
from .station import WeatherStation

_USER_AGENT = "idfkit (https://github.com/samuelduchesne/idfkit)"


@dataclass(frozen=True)
class WeatherFiles:
    """Paths to downloaded and extracted weather files.

    Attributes:
        epw: Path to the ``.epw`` file (always present after extraction).
        ddy: Path to the ``.ddy`` file (always present after extraction).
        stat: Path to the ``.stat`` file, or ``None`` if not included.
        zip_path: Path to the original downloaded ZIP archive.
        station: The station this download corresponds to.
    """

    epw: Path
    ddy: Path
    stat: Path | None
    zip_path: Path
    station: WeatherStation


class WeatherDownloader:
    """Download and cache weather files from climate.onebuilding.org.

    Downloaded ZIP archives are extracted and cached locally so that
    subsequent requests for the same station and dataset are served from
    disk without a network call.

    Example::

        from idfkit.weather import StationIndex, WeatherDownloader

        station = StationIndex.load().search("chicago ohare")[0].station
        downloader = WeatherDownloader()
        files = downloader.download(station)
        print(files.epw)

    Args:
        cache_dir: Override the default cache directory.
        max_age: Maximum age of cached files before re-downloading.
            Can be a :class:`~datetime.timedelta` or a number of seconds.
            If ``None`` (default), cached files never expire.

    Note:
        The cache has no size limit. For CI/CD environments with limited disk
        space, consider using :meth:`clear_cache` periodically or setting
        a ``max_age`` to force re-downloads of stale files.
    """

    __slots__ = ("_cache_dir", "_max_age_seconds")

    def __init__(
        self,
        cache_dir: Path | None = None,
        max_age: timedelta | float | None = None,
    ) -> None:
        self._cache_dir = cache_dir or default_cache_dir()
        if max_age is None:
            self._max_age_seconds: float | None = None
        elif isinstance(max_age, timedelta):
            self._max_age_seconds = max_age.total_seconds()
        else:
            self._max_age_seconds = float(max_age)

    def _is_stale(self, path: Path) -> bool:
        """Check if a cached file is older than max_age."""
        if self._max_age_seconds is None:
            return False
        if not path.exists():
            return True
        age = time.time() - path.stat().st_mtime
        return age > self._max_age_seconds

    def download(self, station: WeatherStation) -> WeatherFiles:
        """Download and extract weather files for *station*.

        If the files are already cached and not stale, no network request is made.

        Args:
            station: The weather station to download files for.

        Returns:
            A :class:`WeatherFiles` with paths to the extracted files.

        Raises:
            RuntimeError: If the download or extraction fails.
        """
        # Derive a cache subdirectory from the ZIP filename
        zip_filename = station.url.rsplit("/", maxsplit=1)[-1]
        stem = zip_filename.removesuffix(".zip")
        station_dir = self._cache_dir / "files" / str(station.wmo) / stem
        zip_path = station_dir / zip_filename

        # Download if not cached or if stale
        if not zip_path.exists() or self._is_stale(zip_path):
            station_dir.mkdir(parents=True, exist_ok=True)
            try:
                req = Request(station.url, headers={"User-Agent": _USER_AGENT})  # noqa: S310
                with urlopen(req, timeout=120) as resp:  # noqa: S310
                    zip_path.write_bytes(resp.read())
            except (HTTPError, URLError, TimeoutError, OSError) as exc:
                msg = f"Failed to download weather data from {station.url}: {exc}"
                raise RuntimeError(msg) from exc

        # Extract if EPW doesn't already exist or if we just downloaded a fresh ZIP
        epw_path = self._find_file(station_dir, ".epw")
        if epw_path is None or self._is_stale(epw_path):
            try:
                with zipfile.ZipFile(zip_path) as zf:
                    zf.extractall(station_dir)
            except zipfile.BadZipFile as exc:
                msg = f"Downloaded file is not a valid ZIP archive: {zip_path}"
                raise RuntimeError(msg) from exc
            epw_path = self._find_file(station_dir, ".epw")

        if epw_path is None:
            msg = f"No .epw file found in downloaded archive for {station.display_name}"
            raise RuntimeError(msg)

        ddy_path = self._find_file(station_dir, ".ddy")
        if ddy_path is None:
            msg = f"No .ddy file found in downloaded archive for {station.display_name}"
            raise RuntimeError(msg)

        stat_path = self._find_file(station_dir, ".stat")

        return WeatherFiles(
            epw=epw_path,
            ddy=ddy_path,
            stat=stat_path,
            zip_path=zip_path,
            station=station,
        )

    def get_epw(self, station: WeatherStation) -> Path:
        """Download and return the path to the EPW file."""
        return self.download(station).epw

    def get_ddy(self, station: WeatherStation) -> Path:
        """Download and return the path to the DDY file."""
        return self.download(station).ddy

    def clear_cache(self) -> None:
        """Remove all cached weather files.

        This removes the entire ``files/`` subdirectory within the cache,
        which contains all downloaded ZIP archives and extracted files.
        """
        files_dir = self._cache_dir / "files"
        if files_dir.exists():
            shutil.rmtree(files_dir)

    @staticmethod
    def _find_file(directory: Path, suffix: str) -> Path | None:
        """Find the first file with the given suffix in *directory*."""
        for p in directory.iterdir():
            if p.suffix.lower() == suffix.lower() and p.is_file():
                return p
        return None
