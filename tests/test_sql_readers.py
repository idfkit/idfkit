"""Tests for the SQL readers result linking uses.

``SQLResult.component_sizes()``, ``errors()``, ``zones()`` and ``report_keys()`` each read one table
of the EnergyPlus SQLite output. The tests build a small database with the tables' real EnergyPlus
DDL (copied from an EnergyPlus 26.x ``eplusout.sql``), so they need no EnergyPlus.

The committed linking fixtures under ``tests/fixtures/simulation/linked/`` are produced by
``scripts/build_linking_fixtures.py`` on a machine with EnergyPlus. When present, the same
invariants are checked against every one of them; until then those tests skip.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

import pytest

from idfkit.simulation.parsers.sql import ComponentSize, SQLErrorRow, SQLResult, VariableInfo, ZoneRow

LINKED_DIR = Path(__file__).parent / "fixtures" / "simulation" / "linked"

# DDL as EnergyPlus writes it.
_DDL = (
    "CREATE TABLE Simulations (SimulationIndex INTEGER PRIMARY KEY, EnergyPlusVersion TEXT, TimeStamp TEXT, "
    "NumTimestepsPerHour INTEGER, Completed BOOL, CompletedSuccessfully BOOL)",
    "CREATE TABLE Errors ( ErrorIndex INTEGER PRIMARY KEY, SimulationIndex INTEGER, ErrorType INTEGER, "
    "ErrorMessage TEXT, Count INTEGER, FOREIGN KEY(SimulationIndex) REFERENCES Simulations(SimulationIndex) "
    "ON DELETE CASCADE ON UPDATE CASCADE )",
    "CREATE TABLE Zones (ZoneIndex INTEGER PRIMARY KEY, ZoneName TEXT, RelNorth REAL, OriginX REAL, OriginY REAL, "
    "OriginZ REAL, CentroidX REAL, CentroidY REAL, CentroidZ REAL, OfType INTEGER, Multiplier REAL, "
    "ListMultiplier REAL, MinimumX REAL, MaximumX REAL, MinimumY REAL, MaximumY REAL, MinimumZ REAL, MaximumZ REAL, "
    "CeilingHeight REAL, Volume REAL, InsideConvectionAlgo INTEGER, OutsideConvectionAlgo INTEGER, FloorArea REAL, "
    "ExtGrossWallArea REAL, ExtNetWallArea REAL, ExtWindowArea REAL, IsPartOfTotalArea INTEGER)",
    "CREATE TABLE ComponentSizes (ComponentSizesIndex INTEGER PRIMARY KEY, CompType TEXT, CompName TEXT, "
    "Description TEXT, Value REAL, Units TEXT, StrValue TEXT)",
    "CREATE TABLE ReportDataDictionary(ReportDataDictionaryIndex INTEGER PRIMARY KEY, IsMeter INTEGER, Type TEXT, "
    "IndexGroup TEXT, TimestepType TEXT, KeyValue TEXT, Name TEXT, ReportingFrequency TEXT, ScheduleName TEXT, "
    "Units TEXT)",
    "CREATE TABLE ReportData (ReportDataIndex INTEGER PRIMARY KEY, TimeIndex INTEGER, "
    "ReportDataDictionaryIndex INTEGER, Value REAL)",
)

_ERRORS = (
    # (ErrorIndex, ErrorType, ErrorMessage, Count)
    (1, -1, "Testing Individual Branch Integrity", 0),
    (2, 0, "GetSurfaceData: CAUTION -- Interzone surfaces are not fully supported.", 1),
    (3, 0, "CalcDoe2DXCoil: Coil:Cooling:DX:SingleSpeed=MAIN COOLING COIL 1 - Full load outlet temperature", 37),
    (4, 1, "Node Connection Error, Node=SPACE1-1 IN NODE, ZoneHVAC:EquipmentConnections", 1),
    (5, 2, "Fatal error -- preceding conditions cause termination.", 1),
    (6, 7, "A message with a code EnergyPlus does not write.", None),
)

_ZONES = (
    # (ZoneIndex, ZoneName, Multiplier, ListMultiplier)
    (1, "PLENUM-1", 1.0, 1.0),
    (2, "SPACE1-1", 1.0, 1.0),
    (3, "MIDFLOOR", 10.0, 1.0),
    (4, "GROUPED ZONE", 2.0, 3.0),
)

_SIZES = (
    # (ComponentSizesIndex, CompType, CompName, Description, Value, Units)
    (1, "COIL:HEATING:ELECTRIC", "SPACE1-1 ZONE COIL", "Design Size Nominal Capacity", 3017.21, "W"),
    (2, "FAN:VARIABLEVOLUME", "SUPPLY FAN 1", "Design Size Maximum Flow Rate", 1.12, "m3/s"),
    (3, "AIRLOOPHVAC", "VAV SYS 1", "Design Supply Air Flow Rate", 1.12, "m3/s"),
    (4, "CONTROLLER:OUTDOORAIR", "OA CONTROLLER 1", "Maximum Outdoor Air Flow Rate", None, "m3/s"),
)

_DICTIONARY = (
    # (Index, IsMeter, Type, IndexGroup, TimestepType, KeyValue, Name, ReportingFrequency, ScheduleName, Units)
    (1, 0, "Avg", "Zone", "Zone", "SPACE1-1", "Zone Mean Air Temperature", "Hourly", None, "C"),
    (2, 0, "Avg", "Zone", "Zone", "MIDFLOOR", "Zone Mean Air Temperature", "Hourly", None, "C"),
    (3, 0, "Sum", "System", "HVAC System", "SUPPLY FAN 1", "Fan Electricity Energy", "Hourly", None, "J"),
    (4, 1, "Sum", "Facility:Electricity", "Zone", "", "Electricity:Facility", "Run Period", None, "J"),
)


@pytest.fixture()
def sql_db(tmp_path: Path) -> Path:
    """A database with the four tables the readers read, plus ``ReportData`` holding many values."""
    db_path = tmp_path / "eplusout.sql"
    conn = sqlite3.connect(str(db_path))
    for ddl in _DDL:
        conn.execute(ddl)
    conn.execute("INSERT INTO Simulations VALUES (1, 'EnergyPlus, Version 26.2.0', '2026.11.11', 4, 1, 1)")
    conn.executemany(
        "INSERT INTO Errors (ErrorIndex, SimulationIndex, ErrorType, ErrorMessage, Count) VALUES (?, 1, ?, ?, ?)",
        _ERRORS,
    )
    conn.executemany(
        "INSERT INTO Zones (ZoneIndex, ZoneName, Multiplier, ListMultiplier) VALUES (?, ?, ?, ?)",
        _ZONES,
    )
    conn.executemany(
        "INSERT INTO ComponentSizes (ComponentSizesIndex, CompType, CompName, Description, Value, Units) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        _SIZES,
    )
    conn.executemany("INSERT INTO ReportDataDictionary VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", _DICTIONARY)
    conn.executemany(
        "INSERT INTO ReportData (TimeIndex, ReportDataDictionaryIndex, Value) VALUES (?, ?, ?)",
        [(t, k, float(t)) for t in range(1, 201) for k in (1, 2, 3)],
    )
    conn.commit()
    conn.close()
    return db_path


@pytest.fixture()
def traced_statements(monkeypatch: pytest.MonkeyPatch) -> Iterator[list[str]]:
    """Record every SQL statement run on connections opened while the fixture is active."""
    statements: list[str] = []
    real_connect: Callable[..., sqlite3.Connection] = sqlite3.connect

    def connect(*args: Any, **kwargs: Any) -> sqlite3.Connection:
        conn = real_connect(*args, **kwargs)
        conn.set_trace_callback(statements.append)
        return conn

    monkeypatch.setattr(sqlite3, "connect", connect)
    yield statements


class TestComponentSizes:
    def test_row_count_and_order(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            rows = sql.component_sizes()
        assert len(rows) == len(_SIZES)
        assert [r.index for r in rows] == [1, 2, 3, 4]

    def test_fields(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            first = sql.component_sizes()[0]
        assert first == ComponentSize(
            index=1,
            component_type="COIL:HEATING:ELECTRIC",
            component_name="SPACE1-1 ZONE COIL",
            description="Design Size Nominal Capacity",
            value=3017.21,
            units="W",
        )

    def test_null_value_is_none(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            assert sql.component_sizes()[3].value is None

    def test_empty_table(self, tmp_path: Path) -> None:
        db = tmp_path / "empty.sql"
        conn = sqlite3.connect(str(db))
        conn.execute(_DDL[3])
        conn.close()
        with SQLResult(db) as sql:
            assert sql.component_sizes() == []


class TestErrors:
    def test_row_count(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            assert len(sql.errors()) == len(_ERRORS)

    def test_severity_mapping(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            severities = [row.severity for row in sql.errors()]
        # -1 info, 0 warning, 1 severe, 2 fatal; an unknown code above 2 is clamped to fatal.
        assert severities == ["info", "warning", "warning", "severe", "fatal", "fatal"]

    def test_count_carried(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            rows = sql.errors()
        assert rows[2] == SQLErrorRow(severity="warning", message=_ERRORS[2][2], count=37)
        assert rows[0].count == 0
        assert rows[5].count == 0  # NULL count reads as zero


class TestZones:
    def test_row_count(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            assert len(sql.zones()) == len(_ZONES)

    def test_multipliers_carried(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            zones = {z.name: z for z in sql.zones()}
        assert zones["MIDFLOOR"] == ZoneRow(index=3, name="MIDFLOOR", multiplier=10, list_multiplier=1)
        assert zones["GROUPED ZONE"].multiplier == 2
        assert zones["GROUPED ZONE"].list_multiplier == 3
        assert all(isinstance(z.multiplier, int) and isinstance(z.list_multiplier, int) for z in zones.values())


class TestReportKeys:
    def test_row_count_and_fields(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            keys = sql.report_keys()
        assert len(keys) == len(_DICTIONARY)
        assert keys[0] == VariableInfo(
            name="Zone Mean Air Temperature",
            key_value="SPACE1-1",
            frequency="Hourly",
            units="C",
            is_meter=False,
            variable_type="Avg",
        )
        meter = keys[3]
        assert meter.is_meter
        assert meter.key_value == ""

    def test_never_touches_report_data(self, sql_db: Path, traced_statements: list[str]) -> None:
        with SQLResult(sql_db) as sql:
            traced_statements.clear()
            sql.report_keys()
        assert traced_statements, "the trace callback recorded nothing"
        assert not any("ReportData " in s or s.rstrip().endswith("ReportData") for s in traced_statements)
        assert all("ReportDataDictionary" in s for s in traced_statements)

    def test_works_without_report_data_table(self, sql_db: Path) -> None:
        conn = sqlite3.connect(str(sql_db))
        conn.execute("DROP TABLE ReportData")
        conn.commit()
        conn.close()
        with SQLResult(sql_db) as sql:
            assert len(sql.report_keys()) == len(_DICTIONARY)


class TestOneQueryPerTable:
    @pytest.mark.parametrize(
        ("reader", "table"),
        [
            ("component_sizes", "ComponentSizes"),
            ("errors", "Errors"),
            ("zones", "Zones"),
            ("report_keys", "ReportDataDictionary"),
        ],
    )
    def test_single_statement(self, sql_db: Path, traced_statements: list[str], reader: str, table: str) -> None:
        with SQLResult(sql_db) as sql:
            traced_statements.clear()
            getattr(sql, reader)()
        assert len(traced_statements) == 1
        assert f"FROM {table} " in traced_statements[0]


class TestReadOnly:
    def test_write_to_file_refused(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql, pytest.raises(sqlite3.OperationalError):
            sql.query("DELETE FROM Errors")

    def test_temp_table_refused(self, sql_db: Path) -> None:
        # ``mode=ro`` alone allows temp tables; ``PRAGMA query_only`` refuses them too.
        with SQLResult(sql_db) as sql, pytest.raises(sqlite3.OperationalError):
            sql.query("CREATE TEMP TABLE scratch (x INTEGER)")

    def test_existing_readers_unaffected(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            assert len(sql.list_variables()) == len(_DICTIONARY)


def _linked_sql_files() -> list[Path]:
    return sorted(LINKED_DIR.glob("*.sql")) if LINKED_DIR.is_dir() else []


@pytest.mark.skipif(
    not _linked_sql_files(), reason="linking fixtures not built yet (scripts/build_linking_fixtures.py)"
)
@pytest.mark.parametrize("sql_path", _linked_sql_files(), ids=lambda p: p.stem)
class TestLinkedFixtures:
    def test_readers_match_tables(self, sql_path: Path) -> None:
        with SQLResult(sql_path) as sql:
            for reader, table in (
                (sql.component_sizes, "ComponentSizes"),
                (sql.errors, "Errors"),
                (sql.zones, "Zones"),
                (sql.report_keys, "ReportDataDictionary"),
            ):
                (count,) = sql.query(f"SELECT COUNT(*) FROM {table}")[0]  # noqa: S608
                assert len(reader()) == count, table

    def test_trimmed_and_multipliers_positive(self, sql_path: Path) -> None:
        with SQLResult(sql_path) as sql:
            assert not sql.query("SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'ReportData'")
            zones = sql.zones()
            assert zones
            assert all(z.multiplier >= 1 and z.list_multiplier >= 1 for z in zones)
            assert sql.report_keys()

    def test_triple_complete(self, sql_path: Path) -> None:
        assert sql_path.with_suffix(".idf").is_file()
        assert sql_path.with_suffix(".err").is_file()
