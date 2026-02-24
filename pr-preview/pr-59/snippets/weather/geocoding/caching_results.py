from __future__ import annotations

from idfkit.weather import geocode

# --8<-- [start:example]
from functools import lru_cache


@lru_cache(maxsize=100)
def cached_geocode(address: str) -> tuple[float, float]:
    return geocode(address)


# Subsequent calls are instant
lat, lon = cached_geocode("123 Main St")
lat, lon = cached_geocode("123 Main St")  # From cache
# --8<-- [end:example]
