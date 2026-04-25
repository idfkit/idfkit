"""Tests for idfkit.weather.geocode (mocked, no network)."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from idfkit.weather.geocode import (
    GeocodingError,
    RateLimiter,
    _ipapi_limiter,  # pyright: ignore[reportPrivateUsage]
    _nominatim_limiter,  # pyright: ignore[reportPrivateUsage]
    detect_location,
    geocode,
)


def _mock_response(data: bytes) -> MagicMock:
    mock_resp = MagicMock()
    mock_resp.read.return_value = data
    mock_resp.__enter__ = MagicMock(return_value=mock_resp)
    mock_resp.__exit__ = MagicMock(return_value=False)
    return mock_resp


@pytest.fixture(autouse=True)
def reset_rate_limiter() -> None:
    """Reset the global rate limiters before each test."""
    _nominatim_limiter.reset()
    _ipapi_limiter.reset()


class TestRateLimiter:
    """Tests for the RateLimiter class."""

    def test_first_call_no_wait(self) -> None:
        limiter = RateLimiter(min_interval=1.0)
        with patch("idfkit.weather.geocode.time") as mock_time:
            mock_time.monotonic.return_value = 100.0
            mock_time.sleep = MagicMock()
            limiter.wait()
            mock_time.sleep.assert_not_called()

    def test_subsequent_call_waits(self) -> None:
        limiter = RateLimiter(min_interval=1.0)
        with patch("idfkit.weather.geocode.time") as mock_time:
            # First call at t=100.0
            mock_time.monotonic.return_value = 100.0
            mock_time.sleep = MagicMock()
            limiter.wait()

            # Second call at t=100.3 (only 0.3s elapsed)
            mock_time.monotonic.return_value = 100.3
            limiter.wait()
            mock_time.sleep.assert_called_once()
            # Should sleep for 0.7s to reach the 1.0s interval
            sleep_duration = mock_time.sleep.call_args[0][0]
            assert abs(sleep_duration - 0.7) < 0.01

    def test_no_wait_after_interval(self) -> None:
        limiter = RateLimiter(min_interval=1.0)
        with patch("idfkit.weather.geocode.time") as mock_time:
            # First call at t=100.0
            mock_time.monotonic.return_value = 100.0
            mock_time.sleep = MagicMock()
            limiter.wait()

            # Second call at t=101.5 (1.5s elapsed, > 1.0s interval)
            mock_time.monotonic.return_value = 101.5
            limiter.wait()
            mock_time.sleep.assert_not_called()

    def test_reset(self) -> None:
        limiter = RateLimiter(min_interval=1.0)
        with patch("idfkit.weather.geocode.time") as mock_time:
            mock_time.monotonic.return_value = 100.0
            mock_time.sleep = MagicMock()
            limiter.wait()

            # After reset, no waiting should occur
            limiter.reset()
            mock_time.monotonic.return_value = 100.1
            limiter.wait()
            mock_time.sleep.assert_not_called()


class TestGeocode:
    @patch("urllib.request.urlopen")
    def test_successful_geocode(self, mock_urlopen: MagicMock) -> None:
        response_data = [{"lat": "41.8781", "lon": "-87.6298", "display_name": "Chicago"}]
        mock_urlopen.return_value = _mock_response(json.dumps(response_data).encode())

        lat, lon = geocode("Willis Tower, Chicago, IL")
        assert abs(lat - 41.8781) < 0.001
        assert abs(lon - (-87.6298)) < 0.001

    @patch("urllib.request.urlopen")
    def test_empty_response_raises(self, mock_urlopen: MagicMock) -> None:
        mock_urlopen.return_value = _mock_response(b"[]")

        with pytest.raises(GeocodingError, match="No results found"):
            geocode("zzzznonexistentplace")

    @patch("urllib.request.urlopen")
    def test_network_error_raises(self, mock_urlopen: MagicMock) -> None:
        from urllib.error import URLError

        mock_urlopen.side_effect = URLError("Network unreachable")

        with pytest.raises(GeocodingError, match="Failed to geocode"):
            geocode("Chicago, IL")

    @patch("urllib.request.urlopen")
    def test_invalid_json_raises(self, mock_urlopen: MagicMock) -> None:
        mock_urlopen.return_value = _mock_response(b"not valid json")

        with pytest.raises(GeocodingError, match="Failed to geocode"):
            geocode("Some address")

    @patch("urllib.request.urlopen")
    def test_missing_lat_lon_raises(self, mock_urlopen: MagicMock) -> None:
        response_data = [{"display_name": "Chicago"}]  # Missing lat/lon
        mock_urlopen.return_value = _mock_response(json.dumps(response_data).encode())

        with pytest.raises(GeocodingError, match="Failed to geocode"):
            geocode("Chicago, IL")


class TestDetectLocation:
    """Tests for detect_location() (mocked, no network)."""

    @patch("urllib.request.urlopen")
    def test_successful_detection(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        body = {"latitude": 41.85, "longitude": -87.65, "city": "Chicago"}
        mock_urlopen.return_value = _mock_response(json.dumps(body).encode())

        lat, lon = detect_location(cache_dir=tmp_path)

        assert abs(lat - 41.85) < 1e-6
        assert abs(lon - (-87.65)) < 1e-6
        # Cache file written
        cache_file = tmp_path / "ipgeo.json"
        assert cache_file.exists()
        cached = json.loads(cache_file.read_text())
        assert cached["latitude"] == pytest.approx(41.85)
        assert cached["longitude"] == pytest.approx(-87.65)

    @patch("urllib.request.urlopen")
    def test_network_failure_raises(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        from urllib.error import URLError

        mock_urlopen.side_effect = URLError("Network unreachable")

        with pytest.raises(GeocodingError, match="Failed to detect location"):
            detect_location(cache_dir=tmp_path)

    @patch("urllib.request.urlopen")
    def test_error_response_raises(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        body = {"error": True, "reason": "RateLimited", "message": "slow down"}
        mock_urlopen.return_value = _mock_response(json.dumps(body).encode())

        with pytest.raises(GeocodingError, match=r"could not locate"):
            detect_location(cache_dir=tmp_path)

    @patch("urllib.request.urlopen")
    def test_missing_lat_lon_raises(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        body = {"city": "somewhere"}  # No latitude/longitude
        mock_urlopen.return_value = _mock_response(json.dumps(body).encode())

        with pytest.raises(GeocodingError, match="missing latitude/longitude"):
            detect_location(cache_dir=tmp_path)

    @patch("urllib.request.urlopen")
    def test_invalid_json_raises(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        mock_urlopen.return_value = _mock_response(b"not valid json")

        with pytest.raises(GeocodingError, match="Failed to detect location"):
            detect_location(cache_dir=tmp_path)

    @patch("urllib.request.urlopen")
    def test_cache_hit_skips_network(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        # Pre-populate a fresh cache entry.
        cache_file = tmp_path / "ipgeo.json"
        cache_file.write_text(
            json.dumps({
                "latitude": 51.5,
                "longitude": -0.12,
                "fetched_at": datetime.now(tz=timezone.utc).isoformat(),
            })
        )
        mock_urlopen.side_effect = AssertionError("network should not be called on cache hit")

        lat, lon = detect_location(cache_dir=tmp_path, max_age=timedelta(hours=1))

        assert abs(lat - 51.5) < 1e-6
        assert abs(lon - (-0.12)) < 1e-6
        mock_urlopen.assert_not_called()

    @patch("urllib.request.urlopen")
    def test_cache_stale_refetches(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        cache_file = tmp_path / "ipgeo.json"
        # Write a 2-hour-old cache entry.
        old = datetime.now(tz=timezone.utc) - timedelta(hours=2)
        cache_file.write_text(json.dumps({"latitude": 0.0, "longitude": 0.0, "fetched_at": old.isoformat()}))
        body = {"latitude": 41.85, "longitude": -87.65}
        mock_urlopen.return_value = _mock_response(json.dumps(body).encode())

        lat, lon = detect_location(cache_dir=tmp_path, max_age=timedelta(hours=1))

        assert abs(lat - 41.85) < 1e-6
        assert abs(lon - (-87.65)) < 1e-6
        mock_urlopen.assert_called_once()

    @patch("urllib.request.urlopen")
    def test_max_age_zero_disables_cache(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        cache_file = tmp_path / "ipgeo.json"
        # Even a brand-new cache should be ignored when max_age=0.
        cache_file.write_text(
            json.dumps({
                "latitude": 0.0,
                "longitude": 0.0,
                "fetched_at": datetime.now(tz=timezone.utc).isoformat(),
            })
        )
        body = {"latitude": 12.34, "longitude": 56.78}
        mock_urlopen.return_value = _mock_response(json.dumps(body).encode())

        lat, lon = detect_location(cache_dir=tmp_path, max_age=0)

        assert abs(lat - 12.34) < 1e-6
        assert abs(lon - 56.78) < 1e-6
        mock_urlopen.assert_called_once()

    @patch("urllib.request.urlopen")
    def test_corrupt_cache_falls_through(self, mock_urlopen: MagicMock, tmp_path: Path) -> None:
        cache_file = tmp_path / "ipgeo.json"
        cache_file.write_text("{not valid json")
        body = {"latitude": 1.0, "longitude": 2.0}
        mock_urlopen.return_value = _mock_response(json.dumps(body).encode())

        lat, lon = detect_location(cache_dir=tmp_path)

        assert abs(lat - 1.0) < 1e-6
        assert abs(lon - 2.0) < 1e-6
        mock_urlopen.assert_called_once()
