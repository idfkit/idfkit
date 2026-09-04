"""Guard the redirect gate (FR-056, FR-086, SC-020, T113).

The gate lives in ``scripts/check_redirects.py`` and is loaded by path, as a maintainer script
rather than part of the distributed package. It reads ``redirects/path-map.json``, whose format
``redirects/README.md`` states, and the captured inventory in ``old-sitemaps/``.

Everything here is hermetic. Each test writes its own map, its own sitemap and its own tiny built
site under ``tmp_path``; the tests that read the committed inventory and the committed map read them
as files. No test opens a socket: live mode is exercised through a stubbed request, and one test
asserts that the default mode never reaches for the network at all.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPT = _REPO_ROOT / "scripts" / "check_redirects.py"
_OLD_SITEMAPS = _REPO_ROOT / "old-sitemaps"
_REAL_MAP = _REPO_ROOT / "redirects" / "path-map.json"


def _load(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


gate = _load("check_redirects", _SCRIPT)

HOST = "py.idfkit.com"
CAPTURED = ["/", "/moved/", "/concepts/caching/", "/simulation/running/"]


def write_sitemap(root: Path, host: str, paths: list[str]) -> Path:
    entries = "".join(f"  <url><loc>https://{host}{entry}</loc></url>\n" for entry in paths)
    path = root / gate.SITEMAP_DIR / f"{host}{gate.SITEMAP_SUFFIX}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}</urlset>\n',
        encoding="utf-8",
    )
    return path


def write_site(root: Path, paths: list[str]) -> Path:
    """A built site publishing exactly these addresses."""
    site = root / "site"
    for entry in paths:
        page = site / "index.html" if entry == "/" else site / entry.strip("/") / "index.html"
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text("<html></html>", encoding="utf-8")
    return site


def write_map(root: Path, hosts: dict[str, Any], **overrides: Any) -> Path:
    document: dict[str, Any] = {
        "map_version": 1,
        "unified_site": "https://developers.idfkit.com",
        "retired_hosts": hosts,
    }
    document.update(overrides)
    path = root / "redirects" / "path-map.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2), encoding="utf-8")
    return path


def host_entry(routes: dict[str, str], prefixes: dict[str, str] | None = None, fallback: str = "/") -> dict[str, Any]:
    return {"fallback": fallback, "prefix_fallbacks": prefixes or {}, "routes": routes}


def identity(paths: list[str]) -> dict[str, str]:
    return {path: path for path in paths}


def options(root: Path, **kwargs: Any) -> Any:
    return gate.Options(
        map_path=kwargs.get("map_path", root / "redirects" / "path-map.json"),
        package_root=root,
        site_dir=kwargs.get("site_dir", root / "site"),
        config_path=kwargs.get("config_path", root / "old-sitemaps" / "developers.idfkit.com.txt"),
        hosts=kwargs.get("hosts", ()),
        sitemaps=kwargs.get("sitemaps", ()),
        live=kwargs.get("live", False),
    )


def codes(report: Any) -> list[str]:
    return sorted(finding.code for finding in report.findings)


def resolution(report: Any, old_path: str) -> Any:
    return next(item for item in report.resolutions if item.old_path == old_path)


@pytest.fixture
def retired(tmp_path: Path) -> Path:
    """A retired host with four captured addresses and a built site that publishes them."""
    write_sitemap(tmp_path, HOST, CAPTURED)
    write_site(tmp_path, CAPTURED)
    return tmp_path


class TestResolution:
    def test_an_exact_route_wins(self, retired: Path) -> None:
        write_map(retired, {HOST: host_entry(identity(CAPTURED) | {"/moved/": "/simulation/running/"})})
        report = gate.run(options(retired))

        assert report.ok
        assert resolution(report, "/moved/").via is gate.Via.ROUTE
        assert resolution(report, "/moved/").target == "/simulation/running/"

    def test_the_longest_matching_prefix_wins_when_no_route_matches(self, retired: Path) -> None:
        write_map(
            retired,
            {
                HOST: host_entry(
                    identity(["/", "/moved/", "/simulation/running/"]),
                    prefixes={"/concepts/": "/", "/concepts/caching/": "/simulation/running/"},
                )
            },
        )
        report = gate.run(options(retired))

        landed = resolution(report, "/concepts/caching/")
        assert landed.via is gate.Via.PREFIX
        assert landed.target == "/simulation/running/"

    def test_a_prefix_lands_on_a_section_page_rather_than_carrying_the_path_across(self, retired: Path) -> None:
        write_map(
            retired,
            {HOST: host_entry(identity(["/", "/moved/", "/simulation/running/"]), prefixes={"/concepts/": "/"})},
        )
        report = gate.run(options(retired))

        assert resolution(report, "/concepts/caching/").target == "/"

    def test_the_host_fallback_catches_what_no_prefix_does(self, retired: Path) -> None:
        write_map(retired, {HOST: host_entry(identity(["/", "/moved/", "/simulation/running/"]))})
        report = gate.run(options(retired))

        assert resolution(report, "/concepts/caching/").via is gate.Via.FALLBACK
        assert resolution(report, "/concepts/caching/").target == "/"

    def test_an_address_that_moved_is_named_without_failing(self, retired: Path) -> None:
        write_map(retired, {HOST: host_entry(identity(CAPTURED) | {"/moved/": "/simulation/running/"})})
        report = gate.run(options(retired))

        assert report.ok
        assert report.warnings == [f"{HOST}/moved/ moved to /simulation/running/"]


class TestWhatFails:
    def test_a_route_pointing_at_a_page_that_does_not_exist_fails(self, retired: Path) -> None:
        write_map(retired, {HOST: host_entry(identity(CAPTURED) | {"/moved/": "/never-written/"})})
        report = gate.run(options(retired))

        assert codes(report) == ["dead-address", "route-target-missing"]
        assert 'routes["/moved/"]' in report.findings[0].detail[0] + report.findings[1].detail[0]

    def test_a_prefix_pointing_at_nothing_fails_even_when_nothing_uses_it(self, retired: Path) -> None:
        write_map(retired, {HOST: host_entry(identity(CAPTURED), prefixes={"/unused/": "/never-written/"})})
        report = gate.run(options(retired))

        assert codes(report) == ["route-target-missing"]
        assert report.findings[0].detail == ('prefix_fallbacks["/unused/"]',)

    def test_a_fallback_that_does_not_exist_fails(self, retired: Path) -> None:
        write_map(retired, {HOST: host_entry(identity(CAPTURED), fallback="/nowhere/")})
        report = gate.run(options(retired))

        assert codes(report) == ["route-target-missing"]
        assert report.findings[0].detail == ("fallback",)

    def test_a_captured_address_with_no_exact_route_fails(self, retired: Path) -> None:
        write_map(retired, {HOST: host_entry(identity(["/", "/moved/", "/simulation/running/"]))})
        report = gate.run(options(retired))

        assert codes(report) == ["unrouted-address"]
        assert report.findings[0].detail == ("/concepts/caching/",)

    def test_an_address_on_another_host_is_reported(self, tmp_path: Path) -> None:
        write_sitemap(tmp_path, HOST, ["/"])
        stray = tmp_path / gate.SITEMAP_DIR / f"{HOST}{gate.SITEMAP_SUFFIX}"
        stray.write_text(
            stray.read_text(encoding="utf-8").replace(
                "</urlset>", "  <url><loc>https://elsewhere.example/x/</loc></url>\n</urlset>"
            ),
            encoding="utf-8",
        )
        write_site(tmp_path, ["/"])
        write_map(tmp_path, {HOST: host_entry({"/": "/"})})
        report = gate.run(options(tmp_path))

        assert "host-mismatch" in codes(report)

    def test_an_inventory_for_a_host_the_map_does_not_declare_is_reported(self, tmp_path: Path) -> None:
        sitemap = write_sitemap(tmp_path, "js.idfkit.com", ["/"])
        write_site(tmp_path, ["/"])
        write_map(tmp_path, {HOST: host_entry({"/": "/"})})
        report = gate.run(options(tmp_path, sitemaps=(sitemap,)))

        assert codes(report) == ["unmapped-host"]


class TestWhatCountsAsExisting:
    def test_the_inventory_answers_when_there_is_no_built_site(self, tmp_path: Path) -> None:
        # The site lives in idfkit-developers now, so there is no mkdocs.yml here to read a
        # navigation out of. The captured inventory answers instead, and it is the better
        # authority: it lists what a build actually produced rather than what a nav means to.
        write_sitemap(tmp_path, HOST, ["/", "/simulation/running/"])
        inventory = tmp_path / "old-sitemaps" / "developers.idfkit.com.txt"
        inventory.parent.mkdir(parents=True, exist_ok=True)
        inventory.write_text("index.html\nsimulation/running/index.html\n", encoding="utf-8")
        write_map(tmp_path, {HOST: host_entry(identity(["/", "/simulation/running/"]))})
        report = gate.run(options(tmp_path))

        assert report.ok
        assert report.index.source_of("/simulation/running/") == "navigation"

    def test_the_built_site_answers_and_the_report_says_so(self, retired: Path) -> None:
        write_map(retired, {HOST: host_entry(identity(CAPTURED))})
        report = gate.run(options(retired))

        assert report.index.source_of("/simulation/running/") == "built site"
        assert "built site" in gate.render(report, verbose=False)

    def test_neither_source_available_refuses_to_run(self, retired: Path) -> None:
        write_map(retired, {HOST: host_entry(identity(CAPTURED))})

        with pytest.raises(gate.Refusal, match="nothing to resolve targets against"):
            gate.run(options(retired, site_dir=retired / "absent", config_path=retired / "absent.yml"))

    def test_a_source_file_maps_to_the_address_mkdocs_publishes(self) -> None:
        assert gate._nav_url("index.md") == "/"
        assert gate._nav_url("simulation/running.md") == "/simulation/running/"
        assert gate._nav_url("weather/index.md") == "/weather/"
        assert gate._nav_url("examples/sizing-workflow.ipynb") == "/examples/sizing-workflow/"

    def test_paths_normalise_to_the_published_form(self) -> None:
        assert gate.normalize_path("/simulation/running") == "/simulation/running/"
        assert gate.normalize_path("simulation/running/") == "/simulation/running/"
        assert gate.normalize_path("/page/#anchor") == "/page/"
        assert gate.normalize_path("/robots.txt") == "/robots.txt"


class TestTheMapItself:
    def test_a_missing_map_refuses_to_run(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        assert gate.main(["--map", str(tmp_path / "path-map.json")]) == gate.EXIT_REFUSED
        assert "no redirect map" in capsys.readouterr().err

    def test_a_map_version_this_gate_does_not_know_refuses_to_run(self, tmp_path: Path) -> None:
        map_path = write_map(tmp_path, {HOST: host_entry({"/": "/"})}, map_version=2)

        with pytest.raises(gate.Refusal, match="declares map_version 2"):
            gate.read_map(map_path)

    def test_a_map_with_no_retired_host_refuses_to_run(self, tmp_path: Path) -> None:
        map_path = write_map(tmp_path, {})

        with pytest.raises(gate.Refusal, match="`retired_hosts` must name at least one host"):
            gate.read_map(map_path)

    def test_a_host_without_a_fallback_refuses_to_run(self, tmp_path: Path) -> None:
        map_path = write_map(tmp_path, {HOST: {"routes": {"/": "/"}}})

        with pytest.raises(gate.Refusal, match="fallback` is required"):
            gate.read_map(map_path)

    def test_unreadable_json_refuses_to_run(self, tmp_path: Path) -> None:
        map_path = tmp_path / "path-map.json"
        map_path.write_text("{not json", encoding="utf-8")

        with pytest.raises(gate.Refusal, match="not readable JSON"):
            gate.read_map(map_path)

    def test_paths_are_normalised_as_they_are_read(self, tmp_path: Path) -> None:
        map_path = write_map(tmp_path, {HOST: host_entry({"api/document": "reference/document"})})
        entry = gate.read_map(map_path).host(HOST)

        assert entry is not None
        assert entry.routes[0].source == "/api/document/"
        assert entry.routes[0].target == "/reference/document/"

    def test_notes_are_read_but_route_nothing(self, retired: Path) -> None:
        write_map(
            retired,
            {HOST: host_entry(identity(CAPTURED))},
            notes=[{"host": HOST, "path": "/moved/", "note": "provisional"}],
        )
        report = gate.run(options(retired))

        assert report.ok
        assert report.redirect_map.notes[0].text == "provisional"
        assert "provisional" in gate.render(report, verbose=True)

    def test_a_missing_sitemap_refuses_to_run(self, tmp_path: Path) -> None:
        write_site(tmp_path, ["/"])
        write_map(tmp_path, {HOST: host_entry({"/": "/"})})

        with pytest.raises(gate.Refusal, match="must not be regenerated"):
            gate.run(options(tmp_path))

    def test_selecting_an_unknown_host_refuses_rather_than_passing_on_nothing(self, retired: Path) -> None:
        write_map(retired, {HOST: host_entry(identity(CAPTURED))})

        with pytest.raises(gate.Refusal, match="no retired host selected"):
            gate.run(options(retired, hosts=("nowhere.example",)))


class TestLiveMode:
    def test_the_default_mode_never_reaches_for_the_network(
        self, retired: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        reached = "offline mode must not reach for the network"

        def refuse(address: str) -> Any:
            raise AssertionError(reached)

        monkeypatch.setattr(gate, "request_live", refuse)
        write_map(retired, {HOST: host_entry(identity(CAPTURED))})
        report = gate.run(options(retired))

        assert report.mode == "offline"

    def _live(self, retired: Path, monkeypatch: pytest.MonkeyPatch, result: Any) -> Any:
        monkeypatch.setattr(gate, "request_live", result)
        write_map(retired, {HOST: host_entry(identity(CAPTURED))})
        return gate.run(options(retired, live=True))

    def test_a_redirect_chain_ending_in_200_on_the_unified_host_passes(
        self, retired: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        report = self._live(
            retired,
            monkeypatch,
            lambda address: gate.LiveResult(
                address=address, status=200, chain=("https://developers.idfkit.com/",), error=None
            ),
        )

        assert report.ok
        assert report.mode == "live"

    def test_a_200_with_no_redirect_means_the_old_site_is_still_publishing(
        self, retired: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        report = self._live(
            retired,
            monkeypatch,
            lambda address: gate.LiveResult(address=address, status=200, chain=(), error=None),
        )

        assert set(codes(report)) == {"still-publishing"}
        assert len(report.findings) == len(CAPTURED)

    def test_a_404_fails(self, retired: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        report = self._live(
            retired,
            monkeypatch,
            lambda address: gate.LiveResult(address=address, status=404, chain=(), error=None),
        )

        assert set(codes(report)) == {"live-not-ok"}

    def test_a_redirect_landing_off_the_unified_host_fails(
        self, retired: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        report = self._live(
            retired,
            monkeypatch,
            lambda address: gate.LiveResult(address=address, status=200, chain=("https://example.com/",), error=None),
        )

        assert set(codes(report)) == {"live-off-site"}

    def test_an_unreachable_address_fails(self, retired: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        report = self._live(
            retired,
            monkeypatch,
            lambda address: gate.LiveResult(address=address, status=None, chain=(), error="name not resolved"),
        )

        assert set(codes(report)) == {"live-unreachable"}

    def test_a_non_http_address_is_refused_without_a_request(self) -> None:
        assert gate.request_live("ftp://py.idfkit.com/").error == "not an http(s) address"


class TestTheCommittedInputs:
    """FR-086: the captured inventory is the input, and it is unrecoverable once publishing stops."""

    def test_both_sitemaps_are_present_at_the_captured_size(self) -> None:
        assert len(gate.read_sitemap(_OLD_SITEMAPS / f"py.idfkit.com{gate.SITEMAP_SUFFIX}")) == 89
        assert len(gate.read_sitemap(_OLD_SITEMAPS / f"js.idfkit.com{gate.SITEMAP_SUFFIX}")) == 28

    def test_every_captured_address_is_on_its_own_host(self) -> None:
        for host in ("py.idfkit.com", "js.idfkit.com"):
            addresses = gate.read_sitemap(_OLD_SITEMAPS / f"{host}{gate.SITEMAP_SUFFIX}")
            assert all(address.startswith(f"https://{host}/") for address in addresses)

    @pytest.mark.skipif(not _REAL_MAP.is_file(), reason="the redirect map has not been written yet")
    def test_the_committed_map_routes_every_captured_address(self) -> None:
        redirect_map = gate.read_map(_REAL_MAP)

        for host_name in ("py.idfkit.com", "js.idfkit.com"):
            host = redirect_map.host(host_name)
            assert host is not None, f"{host_name} has a captured inventory but no entry in the map"
            addresses = gate.read_sitemap(_OLD_SITEMAPS / f"{host_name}{gate.SITEMAP_SUFFIX}")
            unrouted = [
                address
                for address in addresses
                if gate.rule_for(host, gate.normalize_path(address.split(host_name, 1)[1])).via is not gate.Via.ROUTE
            ]
            assert unrouted == []
