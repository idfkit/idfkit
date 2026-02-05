"""Tests for idfkit.weather.geocode (mocked, no network)."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from idfkit.weather.geocode import GeocodingError, RateLimiter, _nominatim_limiter, geocode


def _mock_response(data: bytes) -> MagicMock:
    mock_resp = MagicMock()
    mock_resp.read.return_value = data
    mock_resp.__enter__ = MagicMock(return_value=mock_resp)
    mock_resp.__exit__ = MagicMock(return_value=False)
    return mock_resp


@pytest.fixture(autouse=True)
def reset_rate_limiter() -> None:
    """Reset the global rate limiter before each test."""
    _nominatim_limiter.reset()


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
