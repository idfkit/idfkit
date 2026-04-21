"""Tests for idfkit.weather._cli (the ``idfkit tmy`` subcommand)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from idfkit.weather._cli import (
    EXIT_NETWORK,
    EXIT_NO_MATCHES,
    EXIT_OK,
    EXIT_USAGE,
    TmyAction,
    TmyFilters,
    _format_json,  # pyright: ignore[reportPrivateUsage]
    _format_tsv,  # pyright: ignore[reportPrivateUsage]
    _namespace_to_config,  # pyright: ignore[reportPrivateUsage]
    _resolve_action,  # pyright: ignore[reportPrivateUsage]
    _resolve_matches,  # pyright: ignore[reportPrivateUsage]
    _variant_matches,  # pyright: ignore[reportPrivateUsage]
    add_subparser,
    run_tmy,
)
from idfkit.weather.index import StationIndex
from idfkit.weather.station import WeatherStation

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _station(
    *,
    country: str = "USA",
    state: str = "IL",
    city: str = "Chicago.Ohare.Intl.AP",
    wmo: str = "725300",
    lat: float = 41.98,
    lon: float = -87.92,
    variant: str = "TMYx.2009-2023",
    source: str = "SRC-TMYx",
) -> WeatherStation:
    base = "https://climate.onebuilding.org/WMO_Region_4/"
    url = f"{base}{country}_{state}_{city}.{wmo}_{variant}.zip"
    return WeatherStation(
        country=country,
        state=state,
        city=city,
        wmo=wmo,
        source=source,
        latitude=lat,
        longitude=lon,
        timezone=-6.0,
        elevation=200.0,
        url=url,
    )


@pytest.fixture
def sample_index() -> StationIndex:
    return StationIndex.from_stations([
        _station(wmo="725300", variant="TMYx"),
        _station(wmo="725300", variant="TMYx.2009-2023"),
        _station(wmo="725300", variant="TMYx.2007-2021"),
        _station(city="Chicago.Midway.AP", wmo="725340", variant="TMYx.2009-2023", lat=41.79, lon=-87.75),
        _station(
            country="GBR",
            state="",
            city="London.Heathrow.AP",
            wmo="037720",
            variant="TMYx",
            lat=51.48,
            lon=-0.45,
        ),
    ])


def _parse(argv: list[str]) -> argparse.Namespace:
    """Build a parser with just the tmy subcommand and parse *argv*."""
    top = argparse.ArgumentParser()
    sub = top.add_subparsers(dest="command")
    add_subparser(sub)
    return top.parse_args(["tmy", *argv])


# ---------------------------------------------------------------------------
# Namespace → config translation
# ---------------------------------------------------------------------------


class TestNamespaceToConfig:
    def test_query_only_yields_list_action(self) -> None:
        ns = _parse(["chicago"])
        cfg = _namespace_to_config(ns)
        assert cfg.action is TmyAction.LIST
        assert cfg.filters.query == "chicago"

    def test_download_sentinel_means_cache(self) -> None:
        ns = _parse(["chicago", "--download"])
        cfg = _namespace_to_config(ns)
        assert cfg.action is TmyAction.DOWNLOAD
        assert cfg.download.use_cache is True
        assert cfg.download.dir is None

    def test_download_with_dir(self, tmp_path: Path) -> None:
        ns = _parse(["chicago", "--download", str(tmp_path)])
        cfg = _namespace_to_config(ns)
        assert cfg.action is TmyAction.DOWNLOAD
        assert cfg.download.use_cache is False
        assert cfg.download.dir == tmp_path

    def test_browse_action(self) -> None:
        ns = _parse(["--browse"])
        cfg = _namespace_to_config(ns)
        assert cfg.action is TmyAction.BROWSE

    def test_refresh_action(self) -> None:
        ns = _parse(["--refresh"])
        cfg = _namespace_to_config(ns)
        assert cfg.action is TmyAction.REFRESH

    def test_near_and_lat_lon_conflict(self) -> None:
        ns = _parse(["--near", "NYC", "--lat", "40.7", "--lon", "-74.0"])
        cfg = _namespace_to_config(ns)
        assert any("--near" in e for e in cfg.errors)

    def test_partial_lat_lon_errors(self) -> None:
        ns = _parse(["--lat", "40.7"])
        cfg = _namespace_to_config(ns)
        assert any("--lat and --lon" in e for e in cfg.errors)

    def test_max_km_without_spatial_errors(self) -> None:
        ns = _parse(["chicago", "--max-km", "50"])
        cfg = _namespace_to_config(ns)
        assert any("--max-km" in e for e in cfg.errors)

    def test_full_filters(self) -> None:
        ns = _parse([
            "chicago",
            "--country",
            "USA",
            "--state",
            "IL",
            "--variant",
            "2009-2023",
            "--limit",
            "3",
            "--json",
        ])
        cfg = _namespace_to_config(ns)
        assert cfg.filters.query == "chicago"
        assert cfg.filters.country == "USA"
        assert cfg.filters.state == "IL"
        assert cfg.filters.variant == "2009-2023"
        assert cfg.output.limit == 3
        assert cfg.output.json_output is True


class TestResolveAction:
    def test_refresh_beats_browse(self) -> None:
        # Mutex group prevents both via argparse; exercise internal precedence directly.
        ns = argparse.Namespace(refresh=True, browse=True, download=None)
        assert _resolve_action(ns) is TmyAction.REFRESH

    def test_browse_beats_download(self) -> None:
        ns = argparse.Namespace(refresh=False, browse=True, download="./dl")
        assert _resolve_action(ns) is TmyAction.BROWSE

    def test_default_is_list(self) -> None:
        ns = argparse.Namespace(refresh=False, browse=False, download=None)
        assert _resolve_action(ns) is TmyAction.LIST


# ---------------------------------------------------------------------------
# Filter resolution
# ---------------------------------------------------------------------------


class TestResolveMatches:
    def test_wmo_returns_all_variants(self, sample_index: StationIndex) -> None:
        matches = _resolve_matches(sample_index, TmyFilters(wmo="725300"), limit=10, quiet=True)
        assert len(matches) == 3
        assert all(m.station.wmo == "725300" for m in matches)
        assert all(m.match_field == "wmo" for m in matches)

    def test_wmo_plus_variant_narrows(self, sample_index: StationIndex) -> None:
        matches = _resolve_matches(
            sample_index,
            TmyFilters(wmo="725300", variant="2009-2023"),
            limit=10,
            quiet=True,
        )
        assert len(matches) == 1
        assert matches[0].station.dataset_variant == "TMYx.2009-2023"

    def test_query_returns_scored_results(self, sample_index: StationIndex) -> None:
        matches = _resolve_matches(sample_index, TmyFilters(query="chicago ohare"), limit=10, quiet=True)
        assert len(matches) >= 1
        assert all(m.score is not None for m in matches)
        # Top result should be Chicago Ohare
        assert "Ohare" in matches[0].station.city

    def test_spatial_uses_coords(self, sample_index: StationIndex) -> None:
        matches = _resolve_matches(
            sample_index,
            TmyFilters(lat=41.9, lon=-87.8, max_km=50),
            limit=10,
            quiet=True,
        )
        assert len(matches) >= 1
        assert all(m.distance_km is not None for m in matches)
        # All Chicago stations, none London
        for m in matches:
            assert m.station.country == "USA"
            assert m.station.state == "IL"

    def test_country_post_filter(self, sample_index: StationIndex) -> None:
        matches = _resolve_matches(sample_index, TmyFilters(country="GBR"), limit=10, quiet=True)
        assert len(matches) == 1
        assert matches[0].station.country == "GBR"

    def test_state_post_filter(self, sample_index: StationIndex) -> None:
        matches = _resolve_matches(
            sample_index,
            TmyFilters(country="USA", state="IL"),
            limit=10,
            quiet=True,
        )
        assert {m.station.city for m in matches} == {
            "Chicago.Ohare.Intl.AP",
            "Chicago.Midway.AP",
        }

    def test_variant_substring(self, sample_index: StationIndex) -> None:
        matches = _resolve_matches(sample_index, TmyFilters(variant="2009"), limit=10, quiet=True)
        # Only the TMYx.2009-2023 variants
        assert all("2009" in m.station.dataset_variant for m in matches)

    def test_filename_lookup(self, sample_index: StationIndex) -> None:
        # Pick a filename stem we know is indexed
        any_station = sample_index.stations[0]
        matches = _resolve_matches(
            sample_index,
            TmyFilters(filename=any_station.filename_stem),
            limit=10,
            quiet=True,
        )
        assert len(matches) >= 1
        assert all(m.match_field == "filename" for m in matches)


class TestVariantMatches:
    def test_substring_case_insensitive(self) -> None:
        s = _station(variant="TMYx.2009-2023")
        assert _variant_matches(s, "tmyx")
        assert _variant_matches(s, "2009-2023")
        assert _variant_matches(s, "TMYx.2009")
        assert not _variant_matches(s, "2007-2021")


# ---------------------------------------------------------------------------
# Formatters
# ---------------------------------------------------------------------------


class TestFormatters:
    def test_json_roundtrip(self, sample_index: StationIndex) -> None:
        matches = _resolve_matches(sample_index, TmyFilters(wmo="725300"), limit=10, quiet=True)
        out = _format_json(matches)
        parsed = json.loads(out)
        assert len(parsed) == 3
        assert parsed[0]["station"]["wmo"] == "725300"

    def test_tsv_header_and_rows(self, sample_index: StationIndex) -> None:
        matches = _resolve_matches(sample_index, TmyFilters(wmo="725300"), limit=10, quiet=True)
        out = _format_tsv(matches)
        lines = out.split("\n")
        assert lines[0].startswith("country\tstate\tcity\twmo")
        assert len(lines) == 4  # header + 3 variants


# ---------------------------------------------------------------------------
# End-to-end run_tmy via stubbed index
# ---------------------------------------------------------------------------


class TestRunTmy:
    def test_no_filters_errors(self, capsys: pytest.CaptureFixture[str]) -> None:
        ns = _parse([])
        code = run_tmy(ns)
        assert code == EXIT_USAGE
        err = capsys.readouterr().err
        assert "no filters given" in err

    def test_conflicting_flags_errors(self, capsys: pytest.CaptureFixture[str]) -> None:
        ns = _parse(["--near", "Paris", "--lat", "48.8", "--lon", "2.3"])
        code = run_tmy(ns)
        assert code == EXIT_USAGE
        assert "--near" in capsys.readouterr().err

    def test_wmo_json_output(
        self,
        sample_index: StationIndex,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        ns = _parse(["--wmo", "725300", "--json"])
        with patch.object(StationIndex, "load", return_value=sample_index):
            code = run_tmy(ns)
        assert code == EXIT_OK
        parsed = json.loads(capsys.readouterr().out)
        assert len(parsed) == 3

    def test_no_matches_returns_exit_1(
        self,
        sample_index: StationIndex,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        ns = _parse(["--wmo", "999999", "--json"])
        with patch.object(StationIndex, "load", return_value=sample_index):
            code = run_tmy(ns)
        assert code == EXIT_NO_MATCHES
        assert capsys.readouterr().out.strip() == "[]"

    def test_download_nontty_multiple_matches_errors(
        self,
        sample_index: StationIndex,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        ns = _parse(["--wmo", "725300", "--download"])
        with patch.object(StationIndex, "load", return_value=sample_index):
            code = run_tmy(ns)
        # 3 variants, no --first, not a TTY in pytest → usage error
        assert code == EXIT_USAGE
        err = capsys.readouterr().err
        assert "non-interactive" in err or "--first" in err

    def test_download_first_picks_top(
        self,
        sample_index: StationIndex,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        ns = _parse(["--wmo", "725300", "--first", "--download", str(tmp_path), "--json"])

        fake_files = MagicMock()
        fake_files.epw = tmp_path / "station.epw"
        fake_files.ddy = tmp_path / "station.ddy"
        fake_files.stat = tmp_path / "station.stat"
        fake_files.zip_path = tmp_path / "station.zip"

        with (
            patch.object(StationIndex, "load", return_value=sample_index),
            patch("idfkit.weather.download.WeatherDownloader.download", return_value=fake_files) as dl,
        ):
            code = run_tmy(ns)
        assert code == EXIT_OK
        dl.assert_called_once()
        parsed = json.loads(capsys.readouterr().out)
        assert parsed["station"]["wmo"] == "725300"
        assert parsed["epw"].endswith("station.epw")

    def test_download_network_failure_returns_exit_3(
        self,
        sample_index: StationIndex,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        ns = _parse(["--wmo", "725300", "--first", "--download", str(tmp_path)])
        with (
            patch.object(StationIndex, "load", return_value=sample_index),
            patch(
                "idfkit.weather.download.WeatherDownloader.download",
                side_effect=RuntimeError("boom"),
            ),
        ):
            code = run_tmy(ns)
        assert code == EXIT_NETWORK
        assert "boom" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# Browser server smoke test
# ---------------------------------------------------------------------------


class TestBrowserServer:
    def test_endpoints(self, sample_index: StationIndex) -> None:
        """Launch the server on a random port and hit the key endpoints."""
        import http.client
        import json as _json
        import threading
        import time
        from http.server import ThreadingHTTPServer

        from idfkit.weather._browser.server import (
            BrowserState,
            _make_handler,  # pyright: ignore[reportPrivateUsage]
        )
        from idfkit.weather._cli import TmyFilters

        state = BrowserState(
            index=sample_index,
            filters=TmyFilters(query="chicago"),
            cache_dir=None,
            quiet=True,
        )
        handler_cls = _make_handler(state)
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler_cls)
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        try:
            # Give the OS a tick to bind
            time.sleep(0.05)

            # /api/config returns the seeded filters
            conn = http.client.HTTPConnection("127.0.0.1", port, timeout=2)
            conn.request("GET", "/api/config")
            resp = conn.getresponse()
            assert resp.status == 200
            payload = _json.loads(resp.read().decode())
            assert payload["query"] == "chicago"
            conn.close()

            # /stations.json.gz serves gzip bytes (first two bytes are the gzip magic)
            conn = http.client.HTTPConnection("127.0.0.1", port, timeout=2)
            conn.request("GET", "/stations.json.gz")
            resp = conn.getresponse()
            assert resp.status == 200
            assert resp.getheader("Content-Encoding") == "gzip"
            body = resp.read()
            assert body[:2] == b"\x1f\x8b"
            conn.close()

            # / returns the HTML
            conn = http.client.HTTPConnection("127.0.0.1", port, timeout=2)
            conn.request("GET", "/")
            resp = conn.getresponse()
            assert resp.status == 200
            html = resp.read().decode()
            assert "<title>idfkit tmy" in html
            conn.close()

            # Unknown path → 404
            conn = http.client.HTTPConnection("127.0.0.1", port, timeout=2)
            conn.request("GET", "/nope")
            resp = conn.getresponse()
            assert resp.status == 404
            conn.close()
        finally:
            server.shutdown()
            server.server_close()

    def test_zip_endpoint_streams_attachment(
        self,
        sample_index: StationIndex,
        tmp_path: Path,
    ) -> None:
        """``GET /api/zip`` should stream the cached ZIP with an attachment header."""
        import http.client
        import threading
        import time
        from http.server import ThreadingHTTPServer
        from unittest.mock import MagicMock, patch

        from idfkit.weather._browser.server import (
            BrowserState,
            _make_handler,  # pyright: ignore[reportPrivateUsage]
        )
        from idfkit.weather._cli import TmyFilters

        zip_bytes = b"PK\x03\x04fake-zip-body"
        zip_path = tmp_path / "USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.zip"
        zip_path.write_bytes(zip_bytes)
        fake_files = MagicMock()
        fake_files.zip_path = zip_path

        state = BrowserState(
            index=sample_index,
            filters=TmyFilters(),
            cache_dir=tmp_path,
            quiet=True,
        )
        server = ThreadingHTTPServer(("127.0.0.1", 0), _make_handler(state))
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        try:
            time.sleep(0.05)
            with patch(
                "idfkit.weather.download.WeatherDownloader.download",
                return_value=fake_files,
            ) as dl:
                conn = http.client.HTTPConnection("127.0.0.1", port, timeout=2)
                conn.request("GET", "/api/zip?wmo=725300")
                resp = conn.getresponse()
                assert resp.status == 200
                assert resp.getheader("Content-Type") == "application/zip"
                disposition = resp.getheader("Content-Disposition") or ""
                assert "attachment" in disposition
                assert zip_path.name in disposition
                body = resp.read()
                assert body == zip_bytes
                conn.close()
                dl.assert_called_once()
        finally:
            server.shutdown()
            server.server_close()

    def test_zip_endpoint_missing_params(self, sample_index: StationIndex) -> None:
        import http.client
        import threading
        import time
        from http.server import ThreadingHTTPServer

        from idfkit.weather._browser.server import (
            BrowserState,
            _make_handler,  # pyright: ignore[reportPrivateUsage]
        )
        from idfkit.weather._cli import TmyFilters

        state = BrowserState(index=sample_index, filters=TmyFilters(), cache_dir=None, quiet=True)
        server = ThreadingHTTPServer(("127.0.0.1", 0), _make_handler(state))
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            time.sleep(0.05)
            conn = http.client.HTTPConnection("127.0.0.1", port, timeout=2)
            conn.request("GET", "/api/zip")
            resp = conn.getresponse()
            assert resp.status == 400
            conn.close()
        finally:
            server.shutdown()
            server.server_close()
