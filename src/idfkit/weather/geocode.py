"""Free address geocoding via the Nominatim (OpenStreetMap) API."""

from __future__ import annotations

import json
import threading
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.error import URLError

if TYPE_CHECKING:
    from collections.abc import Mapping

_NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
_USER_AGENT = "idfkit (https://github.com/idfkit/idfkit)"

# IP-geolocation endpoint used by detect_location().
#
# Provider rationale (evaluated April 2026):
#   * ipapi.co — HTTPS, no key, ~1000 req/IP/day free tier, JSON with
#     ``latitude``/``longitude`` keys. Picked as primary.
#   * ip-api.com — free tier is HTTP-only (HTTPS requires Pro), so unsuitable
#     for a tool that ships to users.
#   * freeipapi.com — HTTPS, no key, 60 req/min/IP. Reasonable fallback.
#   * ipinfo.io — needs a token for sustained use; free tier limited.
#
# A future maintainer can swap providers by changing _IPAPI_URL and the
# response-parsing keys in detect_location(); the rest of the contract
# (return type, GeocodingError on failure) is provider-agnostic.
_IPAPI_URL = "https://ipapi.co/json/"
_IPGEO_CACHE_FILENAME = "ipgeo.json"


class GeocodingError(Exception):
    """Raised when an address cannot be geocoded."""


class RateLimiter:
    """Thread-safe rate limiter enforcing a minimum interval between requests.

    Args:
        min_interval: Minimum seconds between requests (default 1.0).
    """

    __slots__ = ("_last_request_time", "_lock", "_min_interval")

    def __init__(self, min_interval: float = 1.0) -> None:
        self._lock = threading.Lock()
        self._last_request_time: float = 0.0
        self._min_interval = min_interval

    def wait(self) -> None:
        """Block until the rate limit allows the next request.

        This method is thread-safe. Concurrent calls will be serialized.
        """
        with self._lock:
            elapsed = time.monotonic() - self._last_request_time
            if elapsed < self._min_interval:
                time.sleep(self._min_interval - elapsed)
            # Update timestamp while holding the lock to prevent races
            self._last_request_time = time.monotonic()

    def reset(self) -> None:
        """Reset the rate limiter state (useful for testing)."""
        with self._lock:
            self._last_request_time = 0.0


# Global rate limiter instance for Nominatim (1 request per second)
_nominatim_limiter = RateLimiter(min_interval=1.0)

# Global rate limiter for ipapi.co (1 request per second is well under the
# free-tier ~1000/day limit and matches the courtesy used for Nominatim).
_ipapi_limiter = RateLimiter(min_interval=1.0)


def geocode(address: str) -> tuple[float, float]:
    """Convert a street address to ``(latitude, longitude)`` via Nominatim.

    Uses the free OpenStreetMap Nominatim geocoding service.  No API key is
    required.  Requests are rate-limited to one per second in compliance with
    Nominatim usage policy.

    This function is thread-safe. Concurrent calls from multiple threads will
    be serialized to respect the rate limit.

    **Composable with spatial search:** Use the splat operator to combine with
    [nearest][idfkit.weather.index.StationIndex.nearest] for address-based
    weather station lookup:

        ```python
        from idfkit.weather import StationIndex, geocode

        # Find weather stations near an address (one line!)
        results = StationIndex.load().nearest(*geocode("350 Fifth Avenue, New York, NY"))

        for r in results[:3]:
            print(f"{r.station.display_name}: {r.distance_km:.0f} km")
        ```

    Args:
        address: A free-form address string (e.g. ``"Willis Tower, Chicago"``).

    Returns:
        A ``(latitude, longitude)`` tuple in decimal degrees.

    Raises:
        GeocodingError: If the address cannot be resolved or the service is
            unreachable.

    Example:
        >>> lat, lon = geocode("Empire State Building, NYC")
        >>> print(f"{lat:.4f}, {lon:.4f}")
        40.7484, -73.9857
    """
    # Wait for rate limit
    _nominatim_limiter.wait()

    params = urllib.parse.urlencode({"q": address, "format": "json", "limit": "1"})
    url = f"{_NOMINATIM_URL}?{params}"

    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})  # noqa: S310
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:  # noqa: S310
            data = json.loads(resp.read())
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])
    except (URLError, TimeoutError, json.JSONDecodeError, KeyError, IndexError) as exc:
        msg = f"Failed to geocode address: {address}"
        raise GeocodingError(msg) from exc
    msg = f"No results found for address: {address}"
    raise GeocodingError(msg)


def _max_age_seconds(max_age: timedelta | float | None) -> float | None:
    if max_age is None:
        return None
    if isinstance(max_age, timedelta):
        return max_age.total_seconds()
    return float(max_age)


def _read_ipgeo_cache(path: Path, max_age_seconds: float | None) -> tuple[float, float] | None:
    """Return cached coordinates if present and fresh, else ``None``."""
    if max_age_seconds is not None and max_age_seconds <= 0:
        return None
    if not path.exists():
        return None
    try:
        payload: Mapping[str, object] = json.loads(path.read_text(encoding="utf-8"))
        fetched_at = datetime.fromisoformat(str(payload["fetched_at"]))
        if fetched_at.tzinfo is None:
            fetched_at = fetched_at.replace(tzinfo=timezone.utc)
        age = (datetime.now(tz=timezone.utc) - fetched_at).total_seconds()
        if max_age_seconds is not None and age > max_age_seconds:
            return None
        return float(payload["latitude"]), float(payload["longitude"])  # pyright: ignore[reportArgumentType]
    except (OSError, ValueError, KeyError, json.JSONDecodeError):
        return None


def _write_ipgeo_cache(path: Path, lat: float, lon: float) -> None:
    payload = {
        "latitude": lat,
        "longitude": lon,
        "fetched_at": datetime.now(tz=timezone.utc).isoformat(),
    }
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload), encoding="utf-8")
    except OSError:
        # A cache write failure should never break the caller.
        pass


def _default_ipgeo_cache_path() -> Path:
    """Cache file location for IP-geolocation results.

    Co-located with the weather cache (one platform-specific dir for all
    weather-related caches) to avoid scattering files across the filesystem.
    """
    # Imported lazily so this module stays importable when the index module
    # is being constructed (avoids any chance of a cycle).
    from .index import default_cache_dir

    return default_cache_dir() / _IPGEO_CACHE_FILENAME


def detect_location(
    *,
    cache_dir: Path | None = None,
    max_age: timedelta | float | None = timedelta(hours=1),
) -> tuple[float, float]:
    """Detect approximate ``(latitude, longitude)`` from this machine's public IP.

    Sends the machine's public IP to `ipapi.co <https://ipapi.co/>`_ over
    HTTPS and parses the response. Accuracy is **city-level** — sufficient
    for finding the nearest TMYx weather stations within a few tens of
    kilometres, but not for precise positioning.

    The result is cached to disk for ``max_age`` (default: 1 hour) so that
    repeated invocations don't hammer the upstream service. Pass
    ``max_age=None`` to cache indefinitely, or ``max_age=0`` to disable
    caching entirely.

    This function is thread-safe; concurrent calls are serialised by the
    same rate limiter pattern used for Nominatim.

    **Composable with spatial search:** Use the splat operator to combine
    with [nearest][idfkit.weather.index.StationIndex.nearest] for
    "weather stations near me" lookups:

        ```python
        from idfkit.weather import StationIndex, detect_location

        results = StationIndex.load().nearest(*detect_location())
        for r in results[:3]:
            print(f"{r.station.display_name}: {r.distance_km:.0f} km")
        ```

    Args:
        cache_dir: Directory for the cache file. Defaults to the platform
            weather cache directory (same as :class:`WeatherDownloader`).
        max_age: Maximum cache age before re-fetching. ``timedelta`` or
            seconds; ``None`` means cache forever; ``0`` means always
            re-fetch.

    Returns:
        A ``(latitude, longitude)`` tuple in decimal degrees.

    Raises:
        GeocodingError: If the IP cannot be located or the service is
            unreachable.

    Note:
        Calling this function sends your public IP address to ipapi.co
        over HTTPS. Use ``--lat`` / ``--lon`` (or ``--near ADDRESS``) on the
        CLI if you'd rather not.
    """
    cache_path = (cache_dir / _IPGEO_CACHE_FILENAME) if cache_dir is not None else _default_ipgeo_cache_path()
    age_limit = _max_age_seconds(max_age)

    cached = _read_ipgeo_cache(cache_path, age_limit)
    if cached is not None:
        return cached

    _ipapi_limiter.wait()

    req = urllib.request.Request(_IPAPI_URL, headers={"User-Agent": _USER_AGENT})  # noqa: S310
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:  # noqa: S310
            data: Mapping[str, object] = json.loads(resp.read())
        if data.get("error"):
            reason = data.get("reason") or data.get("message") or "unknown error"
            msg = f"ipapi.co could not locate this IP: {reason}"
            raise GeocodingError(msg)
        lat = data.get("latitude")
        lon = data.get("longitude")
        if lat is None or lon is None:
            msg = "ipapi.co response missing latitude/longitude"
            raise GeocodingError(msg)
        coords = (float(lat), float(lon))  # pyright: ignore[reportArgumentType]
    except (URLError, TimeoutError, json.JSONDecodeError, KeyError, ValueError, TypeError, AttributeError) as exc:
        msg = f"Failed to detect location from IP: {exc}"
        raise GeocodingError(msg) from exc

    _write_ipgeo_cache(cache_path, *coords)
    return coords
