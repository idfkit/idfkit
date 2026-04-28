"""Download EPW, DDY, and related weather files from climate.onebuilding.org."""

from __future__ import annotations

import logging
import shutil
import time
import zipfile
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .index import default_cache_dir
from .station import WeatherStation

if TYPE_CHECKING:
    from collections.abc import Iterable

    from .index import StationIndex

logger = logging.getLogger(__name__)

_USER_AGENT = "idfkit (https://github.com/idfkit/idfkit)"


def _normalise_suffixes(suffixes: Iterable[str] | None) -> frozenset[str] | None:
    """Normalise a user-supplied collection of suffixes to lowercased ``.ext`` form."""
    if suffixes is None:
        return None
    out: set[str] = set()
    for s in suffixes:
        token = s.lower()
        if not token.startswith("."):
            token = f".{token}"
        out.add(token)
    return frozenset(out)


@dataclass(frozen=True)
class WeatherFiles:
    """Paths to downloaded and extracted weather files.

    For a full extraction (``download(station)`` without ``only``), ``epw`` and
    ``ddy`` are guaranteed non-``None`` — a missing one raises during download.
    When a selective extraction is requested via ``only=``, any field whose
    suffix was not requested *and* not already cached on disk will be ``None``.

    Attributes:
        epw: Path to the ``.epw`` file, or ``None`` if not extracted.
        ddy: Path to the ``.ddy`` file, or ``None`` if not extracted.
        stat: Path to the ``.stat`` file, or ``None`` if not included or extracted.
        zip_path: Path to the original downloaded ZIP archive.
        station: The station this download corresponds to.
    """

    epw: Path | None
    ddy: Path | None
    stat: Path | None
    zip_path: Path
    station: WeatherStation


class WeatherDownloader:
    """Download and cache weather files from climate.onebuilding.org.

    Downloaded ZIP archives are extracted and cached locally so that
    subsequent requests for the same station and dataset are served from
    disk without a network call.

    Examples:
        ```python
        from idfkit.weather import StationIndex, WeatherDownloader

        station = StationIndex.load().search("chicago ohare")[0].station
        downloader = WeatherDownloader()
        files = downloader.download(station)
        print(files.epw)
        ```

    Args:
        cache_dir: Override the default cache directory.
        max_age: Maximum age of cached files before re-downloading.
            Can be a [timedelta][datetime.timedelta] or a number of seconds.
            If ``None`` (default), cached files never expire.

    Note:
        The cache has no size limit. For CI/CD environments with limited disk
        space, consider using [clear_cache][idfkit.weather.download.WeatherDownloader.clear_cache] periodically or setting
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

    def download(
        self,
        station: WeatherStation,
        *,
        only: Iterable[str] | None = None,
    ) -> WeatherFiles:
        """Download and extract weather files for *station*.

        If the files are already cached and not stale, no network request is made.

        Args:
            station: The weather station to download files for.
            only: If given, extract only members whose suffix matches one of
                these values (e.g. ``{".epw"}`` or ``[".epw", ".ddy"]``).
                Each entry is normalised to a lowercase suffix with a leading
                dot (``"epw"`` and ``".EPW"`` both match ``.epw`` members).
                When ``None`` (default), every member of the archive is
                extracted and the result is required to contain a ``.epw``
                and a ``.ddy``.

        Returns:
            A [WeatherFiles][idfkit.weather.download.WeatherFiles] with paths to the extracted files.

        Raises:
            RuntimeError: If the download or extraction fails, or if a full
                extraction is missing a required ``.epw`` or ``.ddy`` file.
        """
        # Derive a cache subdirectory from the ZIP filename
        zip_filename = station.url.rsplit("/", maxsplit=1)[-1]
        stem = zip_filename.removesuffix(".zip")
        station_dir = self._cache_dir / "files" / str(station.wmo) / stem
        zip_path = station_dir / zip_filename

        # Download if not cached or if stale
        if not zip_path.exists() or self._is_stale(zip_path):
            station_dir.mkdir(parents=True, exist_ok=True)
            logger.info("Downloading weather data for %s (WMO %s)", station.display_name, station.wmo)
            try:
                req = Request(station.url, headers={"User-Agent": _USER_AGENT})  # noqa: S310
                with urlopen(req, timeout=120) as resp:  # noqa: S310
                    zip_path.write_bytes(resp.read())
            except (HTTPError, URLError, TimeoutError, OSError) as exc:
                msg = f"Failed to download weather data from {station.url}: {exc}"
                raise RuntimeError(msg) from exc
        else:
            logger.debug("Cache hit for station %s (WMO %s)", station.display_name, station.wmo)

        only_set = _normalise_suffixes(only)
        self._ensure_extracted(zip_path, station_dir, only_set)

        epw_path = self._find_file(station_dir, ".epw")
        ddy_path = self._find_file(station_dir, ".ddy")
        stat_path = self._find_file(station_dir, ".stat")

        # When the caller asked for a full extraction, EPW and DDY are required.
        if only_set is None:
            if epw_path is None:
                msg = f"No .epw file found in downloaded archive for {station.display_name}"
                raise RuntimeError(msg)
            if ddy_path is None:
                msg = f"No .ddy file found in downloaded archive for {station.display_name}"
                raise RuntimeError(msg)

        return WeatherFiles(
            epw=epw_path,
            ddy=ddy_path,
            stat=stat_path,
            zip_path=zip_path,
            station=station,
        )

    @staticmethod
    def _ensure_extracted(
        zip_path: Path,
        station_dir: Path,
        only: frozenset[str] | None,
    ) -> None:
        """Extract members from *zip_path* into *station_dir*.

        If *only* is ``None``, every member is extracted (matching the
        historical ``extractall`` behaviour). Otherwise, only members whose
        lowercased suffix is in *only* are extracted. A member is skipped if
        an up-to-date copy already exists on disk (mtime ≥ ZIP mtime).
        """
        try:
            with zipfile.ZipFile(zip_path) as zf:
                # Compare against the ZIP's mtime rather than ``_is_stale`` —
                # ``zipfile`` preserves archive-internal timestamps, so the
                # extracted file's mtime can be arbitrarily old.
                zip_mtime = zip_path.stat().st_mtime
                for member in zf.namelist():
                    suffix = Path(member).suffix.lower()
                    if only is not None and suffix not in only:
                        continue
                    target = station_dir / Path(member).name
                    if target.exists() and target.stat().st_mtime >= zip_mtime:
                        continue
                    zf.extract(member, station_dir)
        except zipfile.BadZipFile as exc:
            msg = f"Downloaded file is not a valid ZIP archive: {zip_path}"
            raise RuntimeError(msg) from exc

    def get_epw(self, station: WeatherStation) -> Path:
        """Download and return the path to the EPW file.

        Extracts the full archive. To skip extraction of unwanted members,
        call ``download(station, only={".epw"}).epw`` directly.
        """
        epw = self.download(station).epw
        assert epw is not None  # noqa: S101 — guaranteed by full-extract validation
        return epw

    def get_ddy(self, station: WeatherStation) -> Path:
        """Download and return the path to the DDY file.

        Extracts the full archive. To skip extraction of unwanted members,
        call ``download(station, only={".ddy"}).ddy`` directly.
        """
        ddy = self.download(station).ddy
        assert ddy is not None  # noqa: S101 — guaranteed by full-extract validation
        return ddy

    def _resolve_filename(self, filename: str, index: StationIndex | None) -> WeatherStation:
        """Resolve an EPW filename to a station, raising on failure."""
        if index is None:
            from .index import StationIndex as _StationIndex

            index = _StationIndex.load()
        stations = index.get_by_filename(filename)
        if not stations:
            msg = f"No weather station found for filename: {filename!r}"
            raise ValueError(msg)
        return stations[0]

    def get_epw_by_filename(
        self,
        filename: str,
        *,
        index: StationIndex | None = None,
    ) -> Path:
        """Download and return the EPW path for an EPW filename.

        Resolves the canonical EPW filename to a station via
        [StationIndex.get_by_filename][idfkit.weather.index.StationIndex.get_by_filename]
        and downloads the corresponding weather files.

        Args:
            filename: EPW filename or stem (with or without extension).
            index: A pre-loaded station index.  If ``None``, loads the
                default index via
                [StationIndex.load][idfkit.weather.index.StationIndex.load].

        Raises:
            ValueError: If the filename does not match any station.
        """
        return self.get_epw(self._resolve_filename(filename, index))

    def get_ddy_by_filename(
        self,
        filename: str,
        *,
        index: StationIndex | None = None,
    ) -> Path:
        """Download and return the DDY path for an EPW filename.

        Same as
        [get_epw_by_filename][idfkit.weather.download.WeatherDownloader.get_epw_by_filename]
        but returns the DDY file path.

        Args:
            filename: EPW filename or stem (with or without extension).
            index: A pre-loaded station index.

        Raises:
            ValueError: If the filename does not match any station.
        """
        return self.get_ddy(self._resolve_filename(filename, index))

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
