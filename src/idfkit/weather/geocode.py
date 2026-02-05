"""Free address geocoding via the Nominatim (OpenStreetMap) API."""

from __future__ import annotations

import json
import threading
import time
import urllib.parse
import urllib.request
from urllib.error import URLError

_NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
_USER_AGENT = "idfkit (https://github.com/samuelduchesne/idfkit)"


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


def geocode(address: str) -> tuple[float, float]:
    """Convert a street address to ``(latitude, longitude)`` via Nominatim.

    Uses the free OpenStreetMap Nominatim geocoding service.  No API key is
    required.  Requests are rate-limited to one per second in compliance with
    Nominatim usage policy.

    This function is thread-safe. Concurrent calls from multiple threads will
    be serialized to respect the rate limit.

    **Composable with spatial search:** Use the splat operator to combine with
    :meth:`~idfkit.weather.index.StationIndex.nearest` for address-based
    weather station lookup::

        from idfkit.weather import StationIndex, geocode

        # Find weather stations near an address (one line!)
        results = StationIndex.load().nearest(*geocode("350 Fifth Avenue, New York, NY"))

        for r in results[:3]:
            print(f"{r.station.display_name}: {r.distance_km:.0f} km")

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
