"""Download EPW, DDY, and related weather files from climate.onebuilding.org."""

from __future__ import annotations

import contextlib
import logging
import os
import shutil
import threading
import time
import zipfile
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import TYPE_CHECKING, overload
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .._atomic import write_bytes_atomically
from .._forksafe import ForkSafeLock
from .designday import sanitize_ddy_bytes
from .index import default_cache_dir
from .station import WeatherStation

if TYPE_CHECKING:
    from collections.abc import Iterable

    from .index import StationIndex

logger = logging.getLogger(__name__)

_USER_AGENT = "idfkit (https://github.com/idfkit/idfkit)"

# One lock per station directory, so threads of one process download and extract a station once.
_station_locks: dict[Path, ForkSafeLock] = {}
_station_locks_guard = ForkSafeLock()
# DDYs already checked for placeholders this process, by (path, mtime, size): a cache written by
# idfkit before 0.12.2 holds uncleaned DDYs, and checking each one once is enough.
_checked_ddys: set[tuple[str, int, int]] = set()


def _station_lock(station_dir: Path) -> threading.Lock | threading.RLock:
    """The lock that serialises downloads of the station cached in *station_dir*."""
    # Keyed by absolute path, so downloaders given the same cache directory by different
    # spellings (relative, absolute) share one lock.
    key = Path(os.path.abspath(station_dir))
    with _station_locks_guard.lock:
        lock = _station_locks.get(key)
        if lock is None:
            lock = _station_locks[key] = ForkSafeLock()
    return lock.lock


def _is_fresh(target: Path, zip_mtime_ns: int, expected_size: int | None) -> bool:
    """Whether *target* holds a complete copy extracted from the archive whose mtime is *zip_mtime_ns*."""
    try:
        st = target.stat()
    except FileNotFoundError:
        return False
    return st.st_mtime_ns >= zip_mtime_ns and (expected_size is None or st.st_size == expected_size)


def _clean_legacy_ddy(ddy_path: Path) -> None:
    """Clean a cached DDY written before idfkit cleaned DDYs at extraction; once per file per process."""
    st = ddy_path.stat()
    key = (str(ddy_path), st.st_mtime_ns, st.st_size)
    if key in _checked_ddys:
        return
    cleaned, patched = sanitize_ddy_bytes(ddy_path.read_bytes(), ddy_path.name)
    if patched:
        # Keep the mtime, so the cleaned DDY is still judged against the same archive.
        write_bytes_atomically(ddy_path, cleaned, mtime_ns=st.st_mtime_ns)
        st = ddy_path.stat()
    _checked_ddys.add((str(ddy_path), st.st_mtime_ns, st.st_size))


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
    """Paths to a fully extracted weather bundle.

    Returned by ``WeatherDownloader.download(station)`` (no ``only=``).
    ``epw`` and ``ddy`` are guaranteed non-``None`` — a missing one raises
    during download.

    Attributes:
        epw: Path to the ``.epw`` file.
        ddy: Path to the ``.ddy`` file.
        stat: Path to the ``.stat`` file, or ``None`` if not included.
        zip_path: Path to the original downloaded ZIP archive.
        station: The station this download corresponds to.
    """

    epw: Path
    ddy: Path
    stat: Path | None
    zip_path: Path
    station: WeatherStation


@dataclass(frozen=True)
class PartialWeatherFiles:
    """Paths to a selectively extracted weather bundle.

    Returned by ``WeatherDownloader.download(station, only=...)``. Any field
    whose suffix was not requested *and* not already cached on disk will be
    ``None``.

    Attributes:
        epw: Path to the ``.epw`` file, or ``None`` if not extracted.
        ddy: Path to the ``.ddy`` file, or ``None`` if not extracted.
        stat: Path to the ``.stat`` file, or ``None`` if not extracted.
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
        Extracted ``.ddy`` files are cleaned before they are first written:
        a non-numeric placeholder (``N``) in a numeric field of a
        ``SizingPeriod:DesignDay`` object is blanked, so EnergyPlus applies
        the field's default instead of failing with a type-constraint error.
        These placeholders appear in some upstream archives when source data
        is unavailable.

    Note:
        Several threads or processes may share one cache directory. Every
        file is written under a temporary name and renamed into place, so a
        reader sees either nothing or the complete file. Within one process,
        concurrent requests for the same station download it once; separate
        processes that miss the same station at the same moment may each
        download it. Do not call
        [clear_cache][idfkit.weather.download.WeatherDownloader.clear_cache]
        while other threads or processes are downloading into the cache.

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

    @overload
    def download(self, station: WeatherStation) -> WeatherFiles: ...
    @overload
    def download(self, station: WeatherStation, *, only: None) -> WeatherFiles: ...
    @overload
    def download(self, station: WeatherStation, *, only: Iterable[str]) -> PartialWeatherFiles: ...
    def download(
        self,
        station: WeatherStation,
        *,
        only: Iterable[str] | None = None,
    ) -> WeatherFiles | PartialWeatherFiles:
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
            [WeatherFiles][idfkit.weather.download.WeatherFiles] for a full
            extraction, or
            [PartialWeatherFiles][idfkit.weather.download.PartialWeatherFiles]
            when ``only=`` is set.

        Raises:
            RuntimeError: If the download or extraction fails, or if a full
                extraction is missing a required ``.epw`` or ``.ddy`` file.
        """
        # Derive a cache subdirectory from the ZIP filename
        zip_filename = station.url.rsplit("/", maxsplit=1)[-1]
        stem = zip_filename.removesuffix(".zip")
        station_dir = self._cache_dir / "files" / str(station.wmo) / stem
        zip_path = station_dir / zip_filename

        only_set = _normalise_suffixes(only)
        # One thread per station at a time in this process: the others wait, then find the
        # archive in the cache instead of each downloading it again.
        with _station_lock(station_dir):
            self._fetch_and_extract(station, zip_path, station_dir, only_set)
            epw_path = self._find_file(station_dir, ".epw")
            ddy_path = self._find_file(station_dir, ".ddy")
            stat_path = self._find_file(station_dir, ".stat")
            if ddy_path is not None:
                _clean_legacy_ddy(ddy_path)

        if only_set is not None:
            return PartialWeatherFiles(
                epw=epw_path,
                ddy=ddy_path,
                stat=stat_path,
                zip_path=zip_path,
                station=station,
            )

        # Full-extract path: EPW and DDY are required.
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

    def _fetch_and_extract(
        self,
        station: WeatherStation,
        zip_path: Path,
        station_dir: Path,
        only: frozenset[str] | None,
    ) -> None:
        """Download *station*'s archive unless a fresh copy is cached, then extract what is missing."""
        if not zip_path.exists() or self._is_stale(zip_path):
            station_dir.mkdir(parents=True, exist_ok=True)
            logger.info("Downloading weather data for %s (WMO %s)", station.display_name, station.wmo)
            try:
                req = Request(station.url, headers={"User-Agent": _USER_AGENT})  # noqa: S310
                with urlopen(req, timeout=120) as resp:  # noqa: S310
                    payload = resp.read()
                # Published in one rename: another thread or process checking this cache must
                # never open a half-written archive, and a failed download must leave none.
                write_bytes_atomically(zip_path, payload, keep_existing_if_locked=True)
                del payload
            except (HTTPError, URLError, TimeoutError, OSError) as exc:
                msg = f"Failed to download weather data from {station.url}: {exc}"
                raise RuntimeError(msg) from exc
        else:
            logger.debug("Cache hit for station %s (WMO %s)", station.display_name, station.wmo)
        self._ensure_extracted(zip_path, station_dir, only)

    @staticmethod
    def _ensure_extracted(
        zip_path: Path,
        station_dir: Path,
        only: frozenset[str] | None,
    ) -> None:
        """Extract members from *zip_path* into *station_dir*.

        If *only* is ``None``, every top-level member is extracted. Otherwise,
        only members whose lowercased suffix is in *only* are extracted.
        Members inside a folder of the archive (including the ``__MACOSX``
        resource forks a macOS Finder zip adds) are skipped: ``_find_file``
        looks only at the top of *station_dir*.

        Each member is written to a temporary file, stamped with the
        modification time of the archive it came from, and renamed into
        place, so a concurrent reader sees either the previous copy or the
        complete new one. A member is up to date when its mtime is at least
        the archive's and, for every member but the DDY, its size matches
        the archive's record; anything else (a member from an older archive,
        or one truncated by a crash or by an older idfkit) is extracted
        again. A ``.ddy`` member is cleaned of placeholder values before it
        is published, so a cached DDY is never rewritten under a reader.

        A corrupt archive is removed before the error is raised, so the next
        call downloads it again instead of failing on it for good.
        """
        read_stat: os.stat_result | None = None
        try:
            with open(zip_path, "rb") as fh:
                # The archive actually being read: another process may rename a newer archive over
                # the path while this one is open.
                read_stat = os.fstat(fh.fileno())
                zip_mtime_ns = read_stat.st_mtime_ns
                with zipfile.ZipFile(fh) as zf:
                    for info in zf.infolist():
                        member = info.filename
                        if info.is_dir() or "/" in member or "\\" in member or member.startswith("._"):
                            continue
                        suffix = Path(member).suffix.lower()
                        if only is not None and suffix not in only:
                            continue
                        target = station_dir / member
                        if _is_fresh(target, zip_mtime_ns, None if suffix == ".ddy" else info.file_size):
                            continue
                        data = zf.read(info)
                        if suffix == ".ddy":
                            data, _ = sanitize_ddy_bytes(data, member)
                        write_bytes_atomically(target, data, mtime_ns=zip_mtime_ns, keep_existing_if_locked=True)
        except zipfile.BadZipFile as exc:
            # Remove only the archive that was read: another process may already have renamed a
            # good one over the path, and deleting that would force a needless download.
            with contextlib.suppress(OSError):
                current = zip_path.stat()
                if read_stat is not None and (current.st_dev, current.st_ino) == (read_stat.st_dev, read_stat.st_ino):
                    zip_path.unlink()
            msg = f"Downloaded file is not a valid ZIP archive: {zip_path}"
            raise RuntimeError(msg) from exc

    def get_epw(self, station: WeatherStation) -> Path:
        """Download and return the path to the EPW file.

        Extracts the full archive. To skip extraction of unwanted members,
        call ``download(station, only={".epw"}).epw`` directly.
        """
        return self.download(station).epw

    def get_ddy(self, station: WeatherStation) -> Path:
        """Download and return the path to the DDY file.

        Extracts the full archive. To skip extraction of unwanted members,
        call ``download(station, only={".ddy"}).ddy`` directly.
        """
        return self.download(station).ddy

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
