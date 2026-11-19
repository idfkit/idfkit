"""Spatial distance utilities for weather station search."""

from __future__ import annotations

import math

__all__ = [
    "haversine_km",
]


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two points in kilometres.

    Uses the Haversine formula. All arguments are in decimal degrees.
    Accuracy is within 0.5%, which is more than sufficient for
    station-to-site distance comparisons.

    Args:
        lat1: Latitude of point 1 (decimal degrees, north positive).
        lon1: Longitude of point 1 (decimal degrees, east positive).
        lat2: Latitude of point 2.
        lon2: Longitude of point 2.

    Returns:
        Distance in kilometres.
    """
    lat1_r = math.radians(lat1)
    lon1_r = math.radians(lon1)
    lat2_r = math.radians(lat2)
    lon2_r = math.radians(lon2)
    dlat = lat2_r - lat1_r
    dlon = lon2_r - lon1_r
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2
    # Clamp to 1.0 to avoid math domain error from floating-point
    # imprecision when computing distances for near-antipodal points.
    return 6371.0 * 2.0 * math.asin(math.sqrt(min(1.0, a)))
