"""Tests for idfkit.weather.spatial."""

from __future__ import annotations

import math

from idfkit.weather.spatial import haversine_km


class TestHaversine:
    def test_same_point(self) -> None:
        assert haversine_km(41.98, -87.92, 41.98, -87.92) == 0.0

    def test_known_distance_chicago_to_new_york(self) -> None:
        # Chicago (41.88, -87.63) to NYC (40.71, -74.01) ~ 1145 km
        dist = haversine_km(41.88, -87.63, 40.71, -74.01)
        assert 1140.0 < dist < 1150.0

    def test_known_distance_london_to_paris(self) -> None:
        # London (51.51, -0.13) to Paris (48.86, 2.35) ~ 343 km
        dist = haversine_km(51.51, -0.13, 48.86, 2.35)
        assert 335.0 < dist < 350.0

    def test_antipodal_points(self) -> None:
        # North pole to south pole ~ half earth circumference ~ 20015 km
        dist = haversine_km(90.0, 0.0, -90.0, 0.0)
        assert math.isclose(dist, math.pi * 6371.0, rel_tol=1e-6)

    def test_symmetry(self) -> None:
        d1 = haversine_km(41.98, -87.92, 40.71, -74.01)
        d2 = haversine_km(40.71, -74.01, 41.98, -87.92)
        assert math.isclose(d1, d2, rel_tol=1e-10)

    def test_equator_one_degree_longitude(self) -> None:
        # At the equator, 1 degree of longitude ~ 111.2 km
        dist = haversine_km(0.0, 0.0, 0.0, 1.0)
        assert 110.0 < dist < 112.0
