"""Free address geocoding via the Nominatim (OpenStreetMap) API."""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from urllib.error import URLError

_NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
_USER_AGENT = "idfkit (https://github.com/samuelduchesne/idfkit)"

# Module-level state for rate limiting (1 request per second).
_last_request_time: float = 0.0


class GeocodingError(Exception):
    """Raised when an address cannot be geocoded."""


def geocode(address: str) -> tuple[float, float]:
    """Convert a street address to ``(latitude, longitude)`` via Nominatim.

    Uses the free OpenStreetMap Nominatim geocoding service.  No API key is
    required.  Requests are rate-limited to one per second in compliance with
    Nominatim usage policy.

    Compose with :meth:`~idfkit.weather.index.StationIndex.nearest` for
    address-based weather station lookup::

        from idfkit.weather import StationIndex, geocode

        results = StationIndex.load().nearest(*geocode("350 Fifth Avenue, New York, NY"))

    Args:
        address: A free-form address string (e.g. ``"Willis Tower, Chicago"``).

    Returns:
        A ``(latitude, longitude)`` tuple.

    Raises:
        GeocodingError: If the address cannot be resolved or the service is
            unreachable.
    """
    global _last_request_time

    # Enforce rate limit
    elapsed = time.monotonic() - _last_request_time
    if elapsed < 1.0:
        time.sleep(1.0 - elapsed)

    params = urllib.parse.urlencode({"q": address, "format": "json", "limit": "1"})
    url = f"{_NOMINATIM_URL}?{params}"

    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})  # noqa: S310
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:  # noqa: S310
            _last_request_time = time.monotonic()
            data = json.loads(resp.read())
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])
    except (URLError, TimeoutError, json.JSONDecodeError, KeyError, IndexError) as exc:
        msg = f"Failed to geocode address: {address}"
        raise GeocodingError(msg) from exc
    msg = f"No results found for address: {address}"
    raise GeocodingError(msg)
