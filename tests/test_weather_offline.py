"""SC-011: the weather surface works with no network, and does not reach for one.

These tests are the durable half of the offline verification behind
``docs/how-to/warm-the-weather-cache.md``. Working offline and never reaching
for the network are different claims, and only the second one is worth
documenting: a call that fails silently and slowly still "works". So every test
here counts socket attempts rather than only asserting a result.

The stub raises ``socket.gaierror``, an ``OSError`` subclass, because that is
what name resolution actually raises with no network. Raising anything else
would sail past the ``except (HTTPError, URLError, TimeoutError, OSError)``
handlers in ``idfkit.weather.index`` and turn a swallowed best-effort probe into
a crash, which would measure the stub rather than the library.
"""

from __future__ import annotations

import socket
from collections.abc import Iterator
from pathlib import Path

import pytest

from idfkit.weather import StationIndex
from idfkit.weather.index import (
    _CACHE_DIR_ENV_VAR,  # pyright: ignore[reportPrivateUsage]
    _DISABLE_UPDATE_CHECK_ENV_VAR,  # pyright: ignore[reportPrivateUsage]
    _INDEX_FILES,  # pyright: ignore[reportPrivateUsage]
)


class SocketLog:
    """Counts every attempt to reach the network while pretending to be offline."""

    def __init__(self) -> None:
        self.attempts = 0

    def refuse(self, *args: object, **kwargs: object) -> object:
        self.attempts += 1
        raise socket.gaierror(8, "nodename nor servname provided, or not known")


@pytest.fixture
def offline(monkeypatch: pytest.MonkeyPatch) -> Iterator[SocketLog]:
    """Make every socket entry point fail the way an offline machine fails."""
    log = SocketLog()
    for target in ("connect", "connect_ex"):
        monkeypatch.setattr(socket.socket, target, log.refuse, raising=True)
    monkeypatch.setattr(socket, "create_connection", log.refuse, raising=True)
    monkeypatch.setattr(socket, "getaddrinfo", log.refuse, raising=True)
    yield log


@pytest.fixture
def cold_cache(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """An empty, writable cache directory: what a fresh isolated container has."""
    cache = tmp_path / "cache"
    cache.mkdir()
    monkeypatch.setenv(_CACHE_DIR_ENV_VAR, str(cache))
    return cache


class TestLoadingTheIndexOffline:
    def test_load_needs_no_network_when_the_nudge_is_off(
        self, offline: SocketLog, cold_cache: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """The documented offline configuration: a cold cache and the nudge disabled."""
        monkeypatch.setenv(_DISABLE_UPDATE_CHECK_ENV_VAR, "1")

        index = StationIndex.load()

        assert len(index) > 0, "the bundled index must load with no network"
        assert offline.attempts == 0

    def test_a_cold_writable_cache_probes_once_per_index_file(
        self, offline: SocketLog, cold_cache: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """The nudge is best-effort, so it still returns an index, but it costs attempts.

        This is why the how-to tells an offline deployment to set
        ``IDFKIT_NO_WEATHER_UPDATE_CHECK`` rather than relying on a warm cache
        alone. If this count ever changes, the table on that page is stale.
        """
        monkeypatch.delenv(_DISABLE_UPDATE_CHECK_ENV_VAR, raising=False)

        index = StationIndex.load()

        assert len(index) > 0, "a failed freshness probe must not cost the caller their index"
        assert offline.attempts == len(_INDEX_FILES)

    def test_the_throttle_timestamp_suppresses_the_second_load(
        self, offline: SocketLog, cold_cache: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Once the check has run, the 24-hour throttle keeps the next load silent."""
        monkeypatch.delenv(_DISABLE_UPDATE_CHECK_ENV_VAR, raising=False)
        StationIndex.load()
        before = offline.attempts

        StationIndex.load()

        assert offline.attempts == before

    def test_a_read_only_cache_stops_the_nudge_without_the_env_var(
        self, offline: SocketLog, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A warm cache mounted read-only is a supported configuration.

        The nudge cannot write its throttle timestamp, so it gives up before
        reaching for the network. Nothing else about the load is affected.
        """
        cache = tmp_path / "read-only-cache"
        cache.mkdir()
        cache.chmod(0o500)
        monkeypatch.setenv(_CACHE_DIR_ENV_VAR, str(cache))
        monkeypatch.delenv(_DISABLE_UPDATE_CHECK_ENV_VAR, raising=False)
        try:
            index = StationIndex.load()
        finally:
            cache.chmod(0o700)

        assert len(index) > 0
        assert offline.attempts == 0


class TestSearchingOffline:
    def test_search_and_resolve_touch_nothing(
        self, offline: SocketLog, cold_cache: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv(_DISABLE_UPDATE_CHECK_ENV_VAR, "1")
        index = StationIndex.load()
        offline.attempts = 0

        results = index.search("chicago ohare")

        assert results, "the bundled index must be searchable offline"
        assert results[0].station.wmo
        assert offline.attempts == 0


class TestRetrievalFailsLoudly:
    """The calls that genuinely retrieve must fail, not silently return nothing."""

    def test_refresh_raises_rather_than_returning_an_empty_index(self, offline: SocketLog, cold_cache: Path) -> None:
        with pytest.raises(RuntimeError, match="Failed to download weather index"):
            StationIndex.refresh(cache_dir=cold_cache)

    def test_check_for_updates_reports_no_update_rather_than_raising(
        self, offline: SocketLog, cold_cache: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A freshness check that cannot reach upstream has learned nothing, not "no update".

        Returning ``False`` is the deliberate choice: it is the answer that
        changes nothing for the caller. It is documented rather than left to be
        discovered, because the alternative reading, "upstream confirmed you are
        current", is the one a reader would otherwise assume.
        """
        monkeypatch.setenv(_DISABLE_UPDATE_CHECK_ENV_VAR, "1")
        index = StationIndex.load()

        assert index.check_for_updates() is False
