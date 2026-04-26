"""Searchable index of weather stations from climate.onebuilding.org."""

from __future__ import annotations

import gzip
import json
import logging
import math
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .spatial import haversine_km
from .station import SearchResult, SpatialResult, WeatherStation

logger = logging.getLogger(__name__)

# The main regional TMYx KML index files covering worldwide stations.
_INDEX_FILES: tuple[str, ...] = (
    "Region1_Africa_TMYx_EPW_Processing_locations.kml",
    "Region2_Asia_TMYx_EPW_Processing_locations.kml",
    "Region2_Region6_Russia_TMYx_EPW_Processing_locations.kml",
    "Region3_South_America_TMYx_EPW_Processing_locations.kml",
    "Region4_USA_TMYx_EPW_Processing_locations.kml",
    "Region4_Canada_TMYx_EPW_Processing_locations.kml",
    "Region4_NA_CA_Caribbean_TMYx_EPW_Processing_locations.kml",
    "Region5_Southwest_Pacific_TMYx_EPW_Processing_locations.kml",
    "Region6_Europe_TMYx_EPW_Processing_locations.kml",
    "Region7_Antarctica_TMYx_EPW_Processing_locations.kml",
)

_SOURCES_BASE_URL = "https://climate.onebuilding.org/sources"
_USER_AGENT = "idfkit (https://github.com/idfkit/idfkit)"

_BUNDLED_INDEX = Path(__file__).parent / "data" / "stations.json.gz"
_CACHED_INDEX = "stations.json.gz"

# Opt-out env var for the freshness nudge fired by `StationIndex.load()`.
_DISABLE_UPDATE_CHECK_ENV_VAR = "IDFKIT_NO_WEATHER_UPDATE_CHECK"
_UPDATE_CHECK_TIMESTAMP_FILE = "last_update_check"
_UPDATE_CHECK_INTERVAL_SECONDS = 7 * 24 * 60 * 60


def default_cache_dir() -> Path:
    """Return the platform-appropriate cache directory for idfkit weather data."""
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        return base / "idfkit" / "cache" / "weather"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Caches" / "idfkit" / "weather"
    # Linux / other POSIX
    xdg = os.environ.get("XDG_CACHE_HOME")
    base = Path(xdg) if xdg else Path.home() / ".cache"
    return base / "idfkit" / "weather"


# ---------------------------------------------------------------------------
# Download / parse helpers (used by refresh and build script)
# ---------------------------------------------------------------------------


def _download_file(url: str, dest: Path) -> str | None:
    """Download a file from *url* to *dest*, creating parent dirs as needed.

    Returns the ``Last-Modified`` response header value, or ``None`` if
    the header is absent.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = Request(url, headers={"User-Agent": _USER_AGENT})  # noqa: S310
    with urlopen(req, timeout=60) as resp:  # noqa: S310
        last_modified: str | None = resp.headers.get("Last-Modified")
        dest.write_bytes(resp.read())
    return last_modified


def _ensure_index_file(filename: str, cache_dir: Path) -> tuple[Path, str | None]:
    """Return the local path for a KML index file, downloading if absent.

    Returns ``(path, last_modified_header)``.  When the file already exists
    in the cache the header is ``None`` (we don't know it).
    """
    local = cache_dir / "indexes" / filename
    if local.exists():
        return local, None
    url = f"{_SOURCES_BASE_URL}/{filename}"
    try:
        last_modified = _download_file(url, local)
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        msg = f"Failed to download weather index {filename}: {exc}"
        raise RuntimeError(msg) from exc
    return local, last_modified


# Strip HTML tags from a string. The KML descriptions are <![CDATA[...]]>
# blocks containing a small HTML <table>; we don't want a real HTML parser.
_TAG_RE = re.compile(r"<[^>]+>")

# Field extractors. Each pattern runs against the description with HTML tags
# stripped (whitespace and newlines from the original <tr>/<td> structure are
# preserved, so per-row keys are separated by newlines).
_KML_PATTERNS: dict[str, re.Pattern[str]] = {
    "data_source": re.compile(r"Data Source\s+([A-Za-z0-9._-]+)"),
    "elevation": re.compile(r"Elevation\s+([-\d.]+)\s*m"),
    "timezone": re.compile(r"Time Zone\s*\{?\s*GMT\s+([-+\d.]+)\s*hours?\s*\}?"),
    "climate_zone": re.compile(r"ASHRAE\s+HOF\s+\d+\s+Climate\s+Zone\s+([^\n]+)"),
    "heating_db_c": re.compile(r"99%\s+Heating\s+DB\s+([-\d.]+)\s*C"),
    "cooling_db_c": re.compile(r"1%\s+Cooling\s+DB\s+([-\d.]+)\s*C"),
    "hdd18": re.compile(r"HDD18\s+(\d+)"),
    "cdd10": re.compile(r"CDD10\s+(\d+)"),
    "url": re.compile(r"(https?://\S+?\.zip)"),
    "alternate_wmo": re.compile(r"Design\s+conditions\s+from\s+alternate\s+WMO\s+(\d+)"),
}


def _parse_url_metadata(url: str) -> tuple[str, str, str, str]:
    """Extract ``(country, state, city, wmo)`` from a download URL.

    Examples:
        ``USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023.zip``
            → ``("USA", "IL", "Chicago.Ohare.Intl.AP", "725300")``
        ``GBR_London.Heathrow.AP.037720_TMYx.zip``
            → ``("GBR", "", "London.Heathrow.AP", "037720")``
    """
    filename = url.rsplit("/", maxsplit=1)[-1]
    stem = filename.removesuffix(".zip")
    parts = stem.split("_")
    if not parts:
        return "", "", "", ""
    country = parts[0]

    # parts[1] is a 2-3 letter alpha state code only when there are 4+ underscore-segments
    # (country, state, city.WMO, variant). For single-segment (country, city.WMO, variant)
    # there's no state.
    state = ""
    city_idx = 1
    if len(parts) >= 4 and parts[1].isalpha() and 1 <= len(parts[1]) <= 3:
        state = parts[1]
        city_idx = 2

    if city_idx >= len(parts):
        return country, state, "", ""

    city_with_wmo = parts[city_idx]
    dot_split = city_with_wmo.rsplit(".", maxsplit=1)
    if len(dot_split) == 2 and dot_split[1].isdigit():
        return country, state, dot_split[0], dot_split[1]
    return country, state, city_with_wmo, ""


def _strip_kml_namespace(root: ET.Element) -> None:
    """Remove KML namespace prefixes so element lookups don't need them."""
    for elem in root.iter():
        tag = elem.tag
        if "}" in tag:
            elem.tag = tag.split("}", 1)[1]


def _parse_kml(path: Path) -> list[WeatherStation]:
    """Parse a single climate.onebuilding.org KML index file.

    Each ``<Placemark>`` represents one downloadable weather entry. The
    placemark's ``<description>`` is a CDATA block containing a small
    HTML table with the station's metadata; coordinates are read from
    the ``<Point><coordinates>`` element.

    Sentinel placemarks (e.g. the region label that opens each KML and
    has no description / no download URL) are skipped silently. Real
    station placemarks missing any of the required climate metrics
    raise ``ValueError`` so the surprise is caught at index-rebuild time
    rather than at search time.

    The KMLs declare ``encoding="UTF-8"`` but occasionally contain a
    stray Latin-1 byte inside a URL or station name (e.g. the ``í`` in
    ``Potosí``). We decode tolerantly with ``errors="replace"`` so a
    handful of replacement characters in those fields don't bring down
    the rebuild.
    """
    text = path.read_bytes().decode("utf-8", errors="replace")
    root = ET.fromstring(text)  # noqa: S314 — input is a known KML from a trusted source
    _strip_kml_namespace(root)

    stations: list[WeatherStation] = []
    for placemark in root.iter("Placemark"):
        station = _parse_placemark(placemark, path.name)
        if station is not None:
            stations.append(station)
    return stations


def _parse_placemark(placemark: ET.Element, source_filename: str) -> WeatherStation | None:
    """Parse a single ``<Placemark>`` element. Returns ``None`` for sentinels."""
    description_elem = placemark.find("description")
    coords_elem = placemark.find(".//coordinates")
    name_elem = placemark.find("name")
    if description_elem is None or description_elem.text is None or coords_elem is None:
        return None

    plain = _TAG_RE.sub("", description_elem.text)

    url_match = _KML_PATTERNS["url"].search(plain)
    if url_match is None:
        return None
    url = url_match.group(1)

    coords_text = (coords_elem.text or "").strip()
    coords_parts = coords_text.split(",")
    if len(coords_parts) < 2:
        return None
    longitude = float(coords_parts[0])
    latitude = float(coords_parts[1])

    placemark_name = (name_elem.text or "?") if name_elem is not None else "?"

    def _required(key: str) -> str:
        match = _KML_PATTERNS[key].search(plain)
        if match is None:
            msg = f"Placemark {placemark_name!r} in {source_filename} is missing required field {key!r}"
            raise ValueError(msg)
        return match.group(1)

    climate_zone = _required("climate_zone").strip()
    heating_db_c = float(_required("heating_db_c"))
    cooling_db_c = float(_required("cooling_db_c"))
    hdd18 = int(_required("hdd18"))
    cdd10 = int(_required("cdd10"))

    elev_match = _KML_PATTERNS["elevation"].search(plain)
    elevation = float(elev_match.group(1)) if elev_match else 0.0

    tz_match = _KML_PATTERNS["timezone"].search(plain)
    timezone_offset = float(tz_match.group(1)) if tz_match else 0.0

    source_match = _KML_PATTERNS["data_source"].search(plain)
    source = source_match.group(1) if source_match else ""

    alt_match = _KML_PATTERNS["alternate_wmo"].search(plain)
    alternate_wmo = alt_match.group(1) if alt_match else None

    country, state, city, wmo = _parse_url_metadata(url)

    return WeatherStation(
        country=country,
        state=state,
        city=city,
        wmo=wmo,
        source=source,
        latitude=latitude,
        longitude=longitude,
        timezone=timezone_offset,
        elevation=elevation,
        url=url,
        ashrae_climate_zone=climate_zone,
        heating_design_db_c=heating_db_c,
        cooling_design_db_c=cooling_db_c,
        hdd18=hdd18,
        cdd10=cdd10,
        design_conditions_source_wmo=alternate_wmo,
    )


# ---------------------------------------------------------------------------
# Compressed index serialization
# ---------------------------------------------------------------------------


def _load_compressed_index(path: Path) -> tuple[list[WeatherStation], dict[str, str], str]:
    """Load a gzip-compressed JSON station index.

    Returns ``(stations, last_modified_headers, built_at_iso)``.
    """
    with gzip.open(path, "rt", encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)
    stations = [WeatherStation.from_dict(d) for d in data["stations"]]
    last_modified: dict[str, str] = data.get("last_modified", {})
    built_at: str = data.get("built_at", "")
    return stations, last_modified, built_at


def _save_compressed_index(
    stations: list[WeatherStation],
    last_modified: dict[str, str],
    dest: Path,
) -> None:
    """Serialize stations and metadata to a gzip-compressed JSON file."""
    data = {
        "built_at": datetime.now(tz=timezone.utc).isoformat(),
        "last_modified": last_modified,
        "stations": [s.to_dict() for s in stations],
    }
    dest.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(dest, "wt", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"))


def _head_last_modified(url: str) -> str | None:
    """Send a HEAD request and return the ``Last-Modified`` header, or ``None``."""
    req = Request(url, method="HEAD", headers={"User-Agent": _USER_AGENT})  # noqa: S310
    try:
        with urlopen(req, timeout=30) as resp:  # noqa: S310
            return resp.headers.get("Last-Modified")
    except (HTTPError, URLError, TimeoutError, OSError):
        return None


# ---------------------------------------------------------------------------
# EPW filename detection
# ---------------------------------------------------------------------------

# Matches canonical EPW filenames like:
#   USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023
#   GBR_London.Heathrow.AP.037720_TMYx
#   FRA_Paris.Orly.AP.071490_TMYx.epw
_EPW_FILENAME_RE = re.compile(
    r"^[A-Za-z]{2,3}_"  # Country code + underscore
    r".*"  # City/state segments
    r"\.\d{4,6}"  # .WMO (4-6 digits)
    r"_\w+"  # _Variant (TMYx, etc.)
    r"(?:\.\d{4}-\d{4})?"  # Optional year range
    r"(?:\.(?:zip|epw|ddy|stat))?$",  # Optional extension
)

_WEATHER_FILE_EXTENSIONS = (".zip", ".epw", ".ddy", ".stat")


def _is_epw_filename(query: str) -> bool:
    """Return ``True`` if *query* looks like a canonical EPW filename."""
    return _EPW_FILENAME_RE.match(query) is not None


def _strip_weather_extension(filename: str) -> str:
    """Remove a weather file extension (``.zip``, ``.epw``, etc.) if present."""
    lower = filename.lower()
    for ext in _WEATHER_FILE_EXTENSIONS:
        if lower.endswith(ext):
            return filename[: -len(ext)]
    return filename


def _extract_wmo_from_filename(filename: str) -> str | None:
    """Extract the WMO number from an EPW filename stem.

    Returns the WMO as a raw string (preserving leading zeros), or
    ``None`` if extraction fails.
    """
    stem = _strip_weather_extension(filename)
    # WMO is the last dot-separated group of digits before the final underscore.
    # e.g. "USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023"
    #   → prefix="USA_IL_Chicago.Ohare.Intl.AP.725300", variant="TMYx.2009-2023"
    parts = stem.rsplit("_", maxsplit=1)
    if len(parts) < 2:
        return None
    prefix = parts[0]
    dot_parts = prefix.rsplit(".", maxsplit=1)
    if len(dot_parts) == 2 and dot_parts[1].isdigit():
        return dot_parts[1]
    return None


# ---------------------------------------------------------------------------
# Fuzzy search scoring
# ---------------------------------------------------------------------------


def _score_station(station: WeatherStation, query: str, tokens: list[str]) -> tuple[float, str]:
    """Score a station against a search query.

    Returns ``(score, match_field)`` where score is 0.0-1.0.
    """
    name_lower = station.city.lower().replace(".", " ").replace("-", " ")
    display_lower = station.display_name.lower()

    # Signal 1: Exact WMO match
    if query.isdigit() and query == station.wmo:
        return 1.0, "wmo"

    # Signal 2: Full query is a substring of the display name
    if query in display_lower:
        coverage = len(query) / max(len(display_lower), 1)
        return 0.85 + 0.1 * coverage, "name"

    # Signal 3: Full query is a substring of the city name (dots -> spaces)
    if query in name_lower:
        coverage = len(query) / max(len(name_lower), 1)
        return 0.85 + 0.1 * coverage, "name"

    # Signal 4: All query tokens appear in the name
    name_tokens = set(name_lower.split())
    if tokens and all(any(t.startswith(qt) for t in name_tokens) for qt in tokens):
        coverage = sum(len(qt) for qt in tokens) / max(len(name_lower), 1)
        return 0.6 + 0.3 * min(coverage, 1.0), "name"

    # Signal 5: Partial token overlap (prefix matching)
    if tokens:
        matching = sum(1 for qt in tokens if any(t.startswith(qt) for t in name_tokens))
        if matching > 0:
            ratio = matching / len(tokens)
            return 0.3 * ratio, "name"

    # Signal 6: State or country match
    if query == station.state.lower():
        return 0.5, "state"
    if query == station.country.lower():
        return 0.4, "country"

    return 0.0, ""


# ---------------------------------------------------------------------------
# StationIndex
# ---------------------------------------------------------------------------


def _maybe_check_for_updates(index: StationIndex, cache_dir: Path) -> None:
    """Throttled, best-effort freshness check for the weather (TMYx) station index.

    Skipped silently when:
    - ``IDFKIT_NO_WEATHER_UPDATE_CHECK`` is set in the environment
    - A previous check ran less than ``_UPDATE_CHECK_INTERVAL_SECONDS`` ago
    - The loaded index has no ``last_modified`` metadata to compare against
    - The cache directory cannot be created or written to

    Logs a warning when upstream KML data is newer than the loaded index.
    Network errors are already swallowed by ``check_for_updates``.
    """
    if os.environ.get(_DISABLE_UPDATE_CHECK_ENV_VAR):
        return
    if not index._last_modified:  # pyright: ignore[reportPrivateUsage]
        return

    timestamp_path = cache_dir / _UPDATE_CHECK_TIMESTAMP_FILE
    try:
        if time.time() - timestamp_path.stat().st_mtime < _UPDATE_CHECK_INTERVAL_SECONDS:
            return
    except OSError:
        pass

    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
        timestamp_path.touch()
    except OSError:
        return

    if index.check_for_updates():
        logger.warning(
            "Weather (TMYx) station index from climate.onebuilding.org appears out of date. "
            "Run StationIndex.refresh() to rebuild it. Set %s=1 to silence this check.",
            _DISABLE_UPDATE_CHECK_ENV_VAR,
        )


class StationIndex:
    """Searchable index of weather stations from climate.onebuilding.org.

    Use [load][idfkit.weather.index.StationIndex.load] to load the bundled (or user-refreshed) station index.
    No network access or third-party dependencies are required for [load][idfkit.weather.index.StationIndex.load].

    Use [check_for_updates][idfkit.weather.index.StationIndex.check_for_updates] to see if upstream data has changed, and
    [refresh][idfkit.weather.index.StationIndex.refresh] to re-download and rebuild the index.

    Examples:
        ```python
        index = StationIndex.load()
        results = index.search("chicago ohare", limit=3)
        for r in results:
            print(r.station.display_name, r.score)
        ```
    """

    __slots__ = ("_by_filename", "_by_wmo", "_last_modified", "_stations")

    _stations: list[WeatherStation]
    _by_filename: dict[str, list[WeatherStation]]
    _by_wmo: dict[str, list[WeatherStation]]
    _last_modified: dict[str, str]

    def __init__(self, stations: list[WeatherStation]) -> None:
        self._stations = stations
        self._by_wmo: dict[str, list[WeatherStation]] = {}
        self._by_filename: dict[str, list[WeatherStation]] = {}
        for s in stations:
            self._by_wmo.setdefault(s.wmo, []).append(s)
            self._by_filename.setdefault(s.filename_stem.lower(), []).append(s)
        self._last_modified: dict[str, str] = {}

    # --- Construction -------------------------------------------------------

    @classmethod
    def load(cls, *, cache_dir: Path | None = None) -> StationIndex:
        """Load the station index from a local compressed file.

        Checks for a user-refreshed cache first, then falls back to the
        bundled index shipped with the package.  No network access is
        required.

        Args:
            cache_dir: Override the default cache directory.
        """
        cache = cache_dir or default_cache_dir()
        cached_path = cache / _CACHED_INDEX

        if cached_path.is_file():
            source = cached_path
        elif _BUNDLED_INDEX.is_file():
            source = _BUNDLED_INDEX
        else:
            msg = (
                "No station index found. The bundled index is missing and no "
                "cached index exists. Run StationIndex.refresh() to download one."
            )
            raise FileNotFoundError(msg)

        stations, last_modified, _ = _load_compressed_index(source)
        logger.info("Loaded station index with %d stations from %s", len(stations), source)
        instance = cls(stations)
        instance._last_modified = last_modified
        _maybe_check_for_updates(instance, cache)
        return instance

    @classmethod
    def from_stations(cls, stations: list[WeatherStation]) -> StationIndex:
        """Create an index from an explicit list of stations (useful for tests)."""
        return cls(stations)

    @classmethod
    def refresh(cls, *, cache_dir: Path | None = None) -> StationIndex:
        """Re-download the regional KML indexes from climate.onebuilding.org and rebuild the cache.

        Uses the Python standard library only — no third-party dependencies.

        Args:
            cache_dir: Override the default cache directory.
        """
        cache = cache_dir or default_cache_dir()

        all_stations: list[WeatherStation] = []
        last_modified: dict[str, str] = {}
        for fname in _INDEX_FILES:
            local_path, lm = _ensure_index_file(fname, cache)
            if lm is not None:
                last_modified[fname] = lm
            all_stations.extend(_parse_kml(local_path))

        dest = cache / _CACHED_INDEX
        _save_compressed_index(all_stations, last_modified, dest)

        instance = cls(all_stations)
        instance._last_modified = last_modified
        return instance

    # --- Freshness ----------------------------------------------------------

    def check_for_updates(self) -> bool:
        """Check if upstream KML files have changed since this index was built.

        Sends lightweight HEAD requests to climate.onebuilding.org.
        Returns ``True`` if any file has a newer ``Last-Modified`` date.
        Returns ``False`` if all files match or if the check fails (offline,
        timeout, etc.).
        """
        if not self._last_modified:
            return False
        for fname in _INDEX_FILES:
            stored = self._last_modified.get(fname)
            if stored is None:
                continue
            url = f"{_SOURCES_BASE_URL}/{fname}"
            upstream = _head_last_modified(url)
            if upstream is not None and upstream != stored:
                return True
        return False

    # --- Properties ---------------------------------------------------------

    @property
    def stations(self) -> list[WeatherStation]:
        """All stations in the index."""
        return list(self._stations)

    def __len__(self) -> int:
        return len(self._stations)

    # --- Exact lookups ------------------------------------------------------

    def get_by_wmo(self, wmo: str) -> list[WeatherStation]:
        """Look up stations by WMO number.

        Args:
            wmo: WMO station number as a string (e.g. ``"722950"``).

        Returns a list because a single WMO number can correspond to
        multiple stations or dataset variants.
        """
        return list(self._by_wmo.get(wmo, []))

    def get_by_filename(self, filename: str) -> list[WeatherStation]:
        """Look up stations by EPW filename.

        The *filename* can include or omit the extension (``.zip``,
        ``.epw``, ``.ddy``).  Matching is case-insensitive.

        When the exact filename matches an indexed entry, those stations
        are returned.  Otherwise the method extracts the WMO number from
        the filename and falls back to
        [get_by_wmo][idfkit.weather.index.StationIndex.get_by_wmo].

        Args:
            filename: An EPW filename or stem, e.g.
                ``"USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023"``
                or ``"GBR_London.Heathrow.AP.037720_TMYx.epw"``.

        Returns:
            Matching stations (may be empty).
        """
        key = _strip_weather_extension(filename).lower()

        exact = self._by_filename.get(key, [])
        if exact:
            return list(exact)

        wmo = _extract_wmo_from_filename(filename)
        if wmo:
            return self.get_by_wmo(wmo)

        return []

    # --- Fuzzy text search --------------------------------------------------

    def search(
        self,
        query: str,
        *,
        limit: int = 10,
        country: str | None = None,
    ) -> list[SearchResult]:
        """Fuzzy-search stations by name, city, state, WMO number, or EPW filename.

        Matching is case-insensitive and uses substring / token-prefix
        heuristics (no external NLP dependencies).  Canonical EPW
        filenames (e.g.
        ``"USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023"``) are
        detected automatically and resolved via
        [get_by_filename][idfkit.weather.index.StationIndex.get_by_filename].

        Args:
            query: Free-text search query or EPW filename.
            limit: Maximum number of results to return.
            country: If given, restrict to stations in this country code.
        """
        raw = query.strip()
        q = raw.lower()
        if not q:
            return []

        # Fast path: canonical EPW filename
        if _is_epw_filename(raw):
            stations = self.get_by_filename(raw)
            if stations:
                results = [
                    SearchResult(station=s, score=1.0, match_field="filename")
                    for s in stations
                    if not country or s.country.upper() == country.upper()
                ]
                return results[:limit]

        tokens = q.split()

        scored: list[SearchResult] = []
        for station in self._stations:
            if country and station.country.upper() != country.upper():
                continue
            score, match_field = _score_station(station, q, tokens)
            if score > 0:
                scored.append(SearchResult(station=station, score=score, match_field=match_field))

        scored.sort(key=lambda r: r.score, reverse=True)
        return scored[:limit]

    # --- Spatial search -----------------------------------------------------

    def nearest(
        self,
        latitude: float,
        longitude: float,
        *,
        limit: int = 5,
        max_distance_km: float | None = None,
        country: str | None = None,
    ) -> list[SpatialResult]:
        """Find stations nearest to a geographic coordinate.

        Uses the Haversine formula for great-circle distance.  A bounding-box
        pre-filter is applied when *max_distance_km* is specified to avoid
        computing distances for stations that are obviously too far.

        Args:
            latitude: Decimal degrees, north positive.
            longitude: Decimal degrees, east positive.
            limit: Maximum results to return.
            max_distance_km: Exclude stations farther than this.
            country: If given, restrict to this country code.
        """
        # Bounding-box pre-filter (~111 km per degree of latitude)
        if max_distance_km is not None:
            delta_deg = max_distance_km / 111.0 + 1.0  # small margin
            lat_min = latitude - delta_deg
            lat_max = latitude + delta_deg
            # Longitude degrees vary with latitude
            cos_lat = math.cos(math.radians(latitude))
            lon_delta = delta_deg / max(cos_lat, 0.01)
            lon_min = longitude - lon_delta
            lon_max = longitude + lon_delta
        else:
            lat_min = lat_max = lon_min = lon_max = 0.0  # unused

        results: list[SpatialResult] = []
        for station in self._stations:
            if country and station.country.upper() != country.upper():
                continue
            if max_distance_km is not None:
                if station.latitude < lat_min or station.latitude > lat_max:
                    continue
                if station.longitude < lon_min or station.longitude > lon_max:
                    continue
            dist = haversine_km(latitude, longitude, station.latitude, station.longitude)
            if max_distance_km is not None and dist > max_distance_km:
                continue
            results.append(SpatialResult(station=station, distance_km=dist))

        results.sort(key=lambda r: r.distance_km)
        return results[:limit]

    # --- Filtering ----------------------------------------------------------

    def filter(
        self,
        *,
        country: str | None = None,
        state: str | None = None,
        wmo_region: int | None = None,
    ) -> list[WeatherStation]:
        """Filter stations by metadata criteria.

        All specified criteria must match (logical AND).
        """
        result: list[WeatherStation] = []
        for s in self._stations:
            if country and s.country.upper() != country.upper():
                continue
            if state and s.state.upper() != state.upper():
                continue
            if wmo_region is not None:
                # Infer WMO region from the URL path
                url_lower = s.url.lower()
                if f"wmo_region_{wmo_region}" not in url_lower:
                    continue
            result.append(s)
        return result

    @property
    def countries(self) -> list[str]:
        """Sorted list of unique country codes in the index."""
        return sorted({s.country for s in self._stations})
