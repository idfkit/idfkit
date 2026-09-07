"""Climate zone filtering over the shipped station index.

THESE READ THE REAL SHIPPED INDEX, NOT FIXTURES, AND THAT IS THE POINT.

A fixture carrying only A and B zones passes while the marine zones are silently
dropped. That is not hypothetical: matching the code as ``[0-9][AB]?`` loses 3C, 4C and
5C, which is 1,653 stations, leaves sixteen zones where there are nineteen, raises
nothing and looks correct. Two authors made that exact slip on this exact data before
these tests existed.
"""

from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

import pytest

from idfkit.weather import StationIndex
from idfkit.weather.index import _zone_code_of, _zone_is_undetermined

if TYPE_CHECKING:
    from collections.abc import Iterator

# Counts drawn from the shipped index at its current build, per FR-019b and SC-006.
# They are the assertion T018 asks for: a change that moves stations between two zones
# while preserving the total passes every other test in this file.
ZONE_COUNTS = {
    "0A": 6223,
    "0B": 926,
    "1A": 5122,
    "1B": 746,
    "2A": 6050,
    "2B": 1230,
    "3A": 9048,
    "3B": 1352,
    "3C": 739,
    "4A": 7952,
    "4B": 658,
    "4C": 462,
    "5A": 8641,
    "5B": 740,
    "5C": 452,
    "6A": 6296,
    "6B": 574,
    "7": 6847,
    "8": 3418,
}

ASHRAE_ZONES = list(ZONE_COUNTS)

UNDETERMINED = 2162


@pytest.fixture(scope="module")
def index(tmp_path_factory: pytest.TempPathFactory) -> Iterator[StationIndex]:
    """The index this package SHIPS, never the one the developer happens to have cached.

    ``StationIndex.load()`` prefers a refreshed cache over the bundled file, so the
    counts below would otherwise assert facts about whatever the machine last
    downloaded. An empty cache directory is what makes the bundled index the one loaded.

    The env var is set here rather than left to ``conftest``'s autouse fixture: that one
    is function-scoped, so pytest instantiates this module-scoped fixture BEFORE it, and
    ``load()`` would fire the freshness nudge — a network request, and a write into the
    developer's real cache directory — before anything suppressed it.
    """
    cache_dir = tmp_path_factory.mktemp("weather-cache")
    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setenv("IDFKIT_NO_WEATHER_UPDATE_CHECK", "1")
        yield StationIndex.load(cache_dir=cache_dir)


def test_index_carries_exactly_the_nineteen_ashrae_zones(index: StationIndex) -> None:
    """A twentieth code is an upstream change, and this is where it surfaces.

    It must fail a build rather than quietly alter what a filter returns.
    """
    found = {s.ashrae_climate_zone.split("-")[0].strip() for s in index.filter(climate_zone_determined=True)}
    assert sorted(found) == sorted(ASHRAE_ZONES)


def test_no_station_carries_a_code_outside_the_nineteen(index: StationIndex) -> None:
    """The assertion that names an upstream change instead of merely detecting one.

    The nineteen-zone test above does NOT catch this. A twentieth code is neither a
    zone nor undetermined, so it drops out of both filters and leaves nineteen zones
    standing. The reachability test below does catch it, as a total that no longer adds
    up, but reports it as ``expected 69638, got 69588``, which points at the wrong fact
    and has to be diagnosed.

    This one reports the code by name and how many stations carry it.
    """
    unrecognised = Counter(
        s.ashrae_climate_zone.split("-")[0].strip()
        for s in index.stations
        if _zone_code_of(s.ashrae_climate_zone) is None and not _zone_is_undetermined(s.ashrae_climate_zone)
    )
    assert not unrecognised, f"codes outside the nineteen: {unrecognised.most_common()}"


def test_every_zone_returns_its_expected_count(index: StationIndex) -> None:
    """Counted, not merely non-empty.

    A change that moves stations between two zones while preserving the total, such as
    a label parse that maps some 5B labels to 5A, passes a non-emptiness check, passes
    the prefix check for whatever survives, and passes the partition check below.
    """
    counted = {zone: len(index.filter(climate_zone=zone)) for zone in ASHRAE_ZONES}
    assert counted == ZONE_COUNTS


def test_every_zone_returns_only_its_own_stations(index: StationIndex) -> None:
    total = 0
    for zone in ASHRAE_ZONES:
        hits = index.filter(climate_zone=zone)
        assert hits, f"zone {zone} returned nothing"
        assert all(s.ashrae_climate_zone.startswith(zone) for s in hits)
        total += len(hits)
    # Every determined station is in exactly one zone, so the zones partition them.
    assert total == len(index.filter(climate_zone_determined=True))
    assert total + UNDETERMINED == len(index)


def test_undetermined_stations_never_appear_under_a_zone(index: StationIndex) -> None:
    assert len(index.filter(climate_zone_determined=False)) == UNDETERMINED
    for zone in ASHRAE_ZONES:
        for s in index.filter(climate_zone=zone):
            assert "could not be determined" not in s.ashrae_climate_zone.lower()
    # The label's first token looks like a code and is not one.
    assert index.filter(climate_zone="7A") == []
    assert index.filter(climate_zone="8A") == []


def test_undetermined_stations_stay_reachable(index: StationIndex) -> None:
    determined = len(index.filter(climate_zone_determined=True))
    undetermined = len(index.filter(climate_zone_determined=False))
    # Every station is reachable through one of the two, which is what stops the
    # undetermined ones becoming a hole nobody can query.
    assert determined + undetermined == len(index)


def test_zone_ignores_case_and_combines_with_other_keys(index: StationIndex) -> None:
    assert len(index.filter(climate_zone="5a")) == len(index.filter(climate_zone="5A"))
    combined = index.filter(climate_zone="5A", country="USA")
    assert all(s.country == "USA" for s in combined)
    assert all(s.ashrae_climate_zone.startswith("5A") for s in combined)
    assert len(combined) < len(index.filter(climate_zone="5A"))
    # With state too, which is the combination a station picker actually issues. The
    # marine zones are the ones a wrong suffix pattern loses, so 3C is the case chosen.
    assert len(index.filter(climate_zone="3C", country="USA", state="CA")) == 238
    assert len(index.filter(climate_zone="4C", country="USA", state="WA")) == 115


def test_empty_zone_is_no_constraint_like_country_and_state(index: StationIndex) -> None:
    """An empty select is no filter, not a filter matching nothing.

    A UI binding a blank dropdown to this key would otherwise get zero stations from it
    and every station from ``country`` and ``state`` given the same blank value.
    """
    assert len(index.filter(climate_zone="")) == len(index)
    assert len(index.filter(country="")) == len(index)
    assert len(index.filter(state="")) == len(index)


def test_undetermined_matches_the_zone_sentence_not_any_absence(index: StationIndex) -> None:
    """The guard is anchored on the subject, so it cannot swallow a different absence.

    A label reporting that something else about the station was undetermined must keep
    its zone: filing it under undetermined would report that upstream did not state a
    zone it did state.
    """
    assert _zone_is_undetermined("7A - ASHRAE Climate Zone could not be determined")
    assert _zone_is_undetermined("Climate Zone could not be determined")
    assert not _zone_is_undetermined("5A - Cool - Humid (elevation could not be determined)")
    assert _zone_code_of("5A - Cool - Humid (elevation could not be determined)") == "5A"
