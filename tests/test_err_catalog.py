"""Tests for the EnergyPlus message catalogue, anchored on real EnergyPlus output."""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path

import pytest

from idfkit.schema import EpJSONSchema
from idfkit.simulation.parsers.err import ErrorReport
from idfkit.simulation.parsers.err_catalog import MESSAGE_KINDS, classify_message

FIXTURES = Path(__file__).parent / "fixtures" / "simulation"
LINKED = FIXTURES / "linked"


def _sql_messages(model: str, *, include_info: bool = False) -> list[str]:
    """Return the ``Errors.ErrorMessage`` texts of one linked fixture run."""
    floor = -1 if include_info else 0
    with sqlite3.connect(LINKED / f"{model}.sql") as conn:
        rows = conn.execute(
            "SELECT ErrorMessage FROM Errors WHERE ErrorType >= ? ORDER BY ErrorIndex", (floor,)
        ).fetchall()
    return [str(row[0]) for row in rows]


def _sql_message(model: str, contains: str) -> str:
    """Return the first non-info message of a fixture run that contains ``contains``."""
    for message in _sql_messages(model):
        if contains in message:
            return message
    msg = f"no message containing {contains!r} in {model}.sql"
    raise AssertionError(msg)


def _err_messages() -> list[str]:
    """Return the warning, severe and fatal first lines of every ``.err`` fixture."""
    messages: list[str] = []
    for path in sorted(FIXTURES.rglob("*.err")):
        report = ErrorReport.from_file(path)
        messages.extend(m.message for m in (*report.fatal, *report.severe, *report.warnings))
    return messages


def _all_fixture_messages() -> list[str]:
    messages: list[str] = []
    for path in sorted(LINKED.glob("*.sql")):
        messages.extend(_sql_messages(path.stem))
    messages.extend(_err_messages())
    return messages


# (model, substring locating the message, expected kind, expected pairs)
SQL_CASES: list[tuple[str, str, str, list[tuple[str | None, str]]]] = [
    (
        "MultiStory",
        '"MID WEST OA DX COIL" - Full load outlet',
        "dxcoil.low_outlet_temp",
        [("Coil:Cooling:DX:SingleSpeed", "MID WEST OA DX COIL")],
    ),
    (
        "ShopWithSimplePVT",
        "Air-cooled condenser inlet",
        "dxcoil.low_ambient",
        [("Coil:Cooling:DX:SingleSpeed", "ZN_1_FLR_1_SEC_2:SYSCOOLC DXCOIL")],
    ),
    (
        "MultiStory",
        '"GND WEST WINDOW AC" -- Exceeded',
        "zonehvac.max_iterations",
        [("ZoneHVAC:WindowAirConditioner", "GND WEST WINDOW AC")],
    ),
    ("5ZoneAirCooled", "FinalSystemSizing", "sizing.system_flow_ratio", [("AirLoop", "VAV SYS 1")]),
    (
        "1ZoneEvapCooler",
        "has no Controllers",
        "airloop.no_controllers",
        [("AirLoopHVAC", "EVAP COOLER SYSTEM")],
    ),
    (
        "1ZoneEvapCooler",
        "ANN HTG 99.6%",
        "designday.pressure",
        [(None, "DENVER CENTENNIAL ANN HTG 99.6% CONDNS DB")],
    ),
    (
        "1ZoneEvapCooler",
        "Weather file location",
        "location.weather_file",
        [(None, "DENVER CENTENNIAL CO USA WMO=724666")],
    ),
    ("PlantLoopChainCooling", "Report Variables", "output.variable_not_generated", []),
    ("DOASDualDuctSchool", "Unused Schedules", "schedule.unused", []),
    ("MultiStory", "inaccurate shadowing", "surface.shadowing", []),
    ("1ZoneUncontrolled", "Temperature out of range", "psychro.out_of_range", []),
    ("1ZoneUncontrolled", "WetBulb not converged", "psychro.not_converged", []),
    ("ShopWithSimplePVT", "Water heater =", "waterheater.ratings", [(None, "SHWSYS1 WATER HEATER")]),
    (
        "ShopWithSimplePVT",
        "ZN_1_FLR_1_SEC_1:SYSCOOLC  Cooling coil",
        "coilsystem.sensor_node",
        [("CoilSystem:Cooling:DX", "ZN_1_FLR_1_SEC_1:SYSCOOLC")],
    ),
    (
        "ShopWithSimplePVT",
        "ZN_1_FLR_1_SEC_1SHW_DEFAULT",
        "wateruse.target_temp",
        [(None, "ZN_1_FLR_1_SEC_1SHW_DEFAULT")],
    ),
]


@pytest.mark.parametrize(("model", "contains", "kind", "pairs"), SQL_CASES, ids=[c[2] for c in SQL_CASES])
def test_kind_matches_fixture_message(
    model: str, contains: str, kind: str, pairs: list[tuple[str | None, str]]
) -> None:
    found, names = classify_message(_sql_message(model, contains))
    assert found is not None
    assert found.kind == kind
    assert names == pairs


# (verbatim message, expected kind, expected pairs); see the comment on each for its provenance.
LITERAL_CASES: list[tuple[str, str, list[tuple[str | None, str]]]] = [
    # Verbatim EnergyPlus text, not in fixtures (ZoneEquipmentManager, SizingManager).
    (
        "Calculated design cooling load for zone=FRONTSTAIRSFLR1 ZN is zero.",
        "sizing.zero_load",
        [(None, "FRONTSTAIRSFLR1 ZN")],
    ),
    # Verbatim EnergyPlus text, not in fixtures (ScheduleManager).
    (
        'ProcessScheduleInput: Schedule:Day:Interval="WEEKDAY OCC", '
        "Blank Schedule Type Limits Name input -- will not be validated.",
        "schedule.day_interval",
        [("Schedule:Day:Interval", "WEEKDAY OCC")],
    ),
    # Verbatim EnergyPlus text, not in fixtures (ScheduleManager).
    (
        'ProcessScheduleInput: Schedule:Compact="OCC SCH", Schedule Type Limits Name="FRACTIONS" not found',
        "schedule.input",
        [("Schedule:Compact", "OCC SCH")],
    ),
    # Verbatim EnergyPlus text, not in fixtures (NodeInputManager / BranchNodeConnections).
    (
        'Node Connection Error, Node="SUPPLY INLET NODE", Inlet node did not find an appropriate matching "outlet" node.',
        "node.connection",
        [(None, "SUPPLY INLET NODE")],
    ),
]


@pytest.mark.parametrize(("text", "kind", "pairs"), LITERAL_CASES, ids=[c[1] for c in LITERAL_CASES])
def test_kind_matches_verbatim_message(text: str, kind: str, pairs: list[tuple[str | None, str]]) -> None:
    found, names = classify_message(text)
    assert found is not None
    assert found.kind == kind
    assert names == pairs


def test_err_fixture_kinds() -> None:
    """Kinds whose only real example lives in an ``.err`` fixture."""
    by_kind: dict[str, list[tuple[str | None, str]]] = {}
    for message in _err_messages():
        found, names = classify_message(message)
        if found is not None:
            by_kind[found.kind] = names
    assert by_kind["surface.ground_temperatures"] == []
    assert by_kind["surface.vertices"] == [(None, "WALL-1SOUTH")]
    assert by_kind["location.weather_file"] == []


def test_every_kind_is_exercised() -> None:
    exercised = {c[2] for c in SQL_CASES} | {c[1] for c in LITERAL_CASES}
    exercised |= {"surface.ground_temperatures", "surface.vertices"}
    assert exercised == {k.kind for k in MESSAGE_KINDS}


def test_unknown_text_has_no_kind() -> None:
    assert classify_message("Something EnergyPlus never says.") == (None, [])


def test_generic_pairs_without_a_kind() -> None:
    text = 'SomeRoutine: Coil:Heating:Fuel="MAIN HEATER" and AirLoop="VAV SYS 1" disagree; Fan:OnOff = SUPPLY FAN'
    kind, pairs = classify_message(text)
    assert kind is None
    assert pairs == [
        ("Coil:Heating:Fuel", "MAIN HEATER"),
        ("AirLoop", "VAV SYS 1"),
        ("Fan:OnOff", "SUPPLY FAN"),
    ]


def test_generic_pairs_ignore_unknown_plain_types() -> None:
    _, pairs = classify_message('Routine=PsyTwbFnTdbWPb, Name="NOT A TYPE", Environment=RUN PERIOD 1')
    assert pairs == []


def test_names_keep_case() -> None:
    _, pairs = classify_message('GetAirPathData: AirLoopHVAC="Evap Cooler System" has no Controllers.')
    assert pairs == [("AirLoopHVAC", "Evap Cooler System")]


def test_kind_ids_are_unique_and_dotted() -> None:
    ids = [k.kind for k in MESSAGE_KINDS]
    assert len(ids) == len(set(ids))
    for kind_id in ids:
        assert re.fullmatch(r"[a-z]+(?:\.[a-z_]+)+", kind_id), kind_id


def test_patterns_and_metadata() -> None:
    allowed_symptoms = {"unmet_heating", "unmet_cooling", "peak_outlier", "sizing_zero"}
    for kind in MESSAGE_KINDS:
        assert isinstance(kind.pattern, re.Pattern)
        assert set(kind.pattern.groupindex) <= {"type", "name", "key"}, kind.kind
        assert ("type" in kind.pattern.groupindex) == ("name" in kind.pattern.groupindex), kind.kind
        assert kind.hint.endswith("."), kind.kind
        assert kind.inspect, kind.kind
        assert set(kind.symptoms) <= allowed_symptoms, kind.kind


def test_inspect_types_exist_in_schema(schema: EpJSONSchema) -> None:
    missing = [(k.kind, t) for k in MESSAGE_KINDS for t in k.inspect if t not in schema]
    assert missing == []


def test_catalogue_covers_fixture_messages() -> None:
    messages = _all_fixture_messages()
    unmatched = [m for m in messages if classify_message(m)[0] is None]
    coverage = 1 - len(unmatched) / len(messages)
    assert coverage >= 0.8, f"coverage {coverage:.0%}; unmatched: {unmatched}"
