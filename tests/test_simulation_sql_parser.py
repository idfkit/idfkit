"""Tests for the SQL parser."""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

import pytest

from idfkit.simulation.parsers.sql import SQLResult, TabularRow, VariableInfo


@pytest.fixture()
def sql_db(tmp_path: Path) -> Path:
    """Create a minimal EnergyPlus-schema SQLite database for testing."""
    db_path = tmp_path / "eplusout.sql"
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    # Create EnergyPlus output tables
    cur.execute(
        "CREATE TABLE ReportDataDictionary ("
        "  ReportDataDictionaryIndex INTEGER PRIMARY KEY,"
        "  IsMeter INTEGER,"
        "  VariableType TEXT,"
        "  IndexGroup TEXT,"
        "  TimestepType TEXT,"
        "  KeyValue TEXT,"
        "  Name TEXT,"
        "  ReportingFrequency TEXT,"
        "  ScheduleName TEXT,"
        "  Units TEXT"
        ")"
    )

    cur.execute(
        "CREATE TABLE Time ("
        "  TimeIndex INTEGER PRIMARY KEY,"
        "  Year INTEGER,"
        "  Month INTEGER,"
        "  Day INTEGER,"
        "  Hour INTEGER,"
        "  Minute INTEGER,"
        "  Dst INTEGER,"
        "  Interval INTEGER,"
        "  IntervalType INTEGER,"
        "  SimulationDays INTEGER,"
        "  DayType TEXT,"
        "  WarmupFlag INTEGER,"
        "  Environment TEXT"
        ")"
    )

    cur.execute(
        "CREATE TABLE ReportData ("
        "  ReportDataIndex INTEGER PRIMARY KEY,"
        "  TimeIndex INTEGER,"
        "  ReportDataDictionaryIndex INTEGER,"
        "  Value REAL"
        ")"
    )

    cur.execute(
        "CREATE TABLE TabularDataWithStrings ("
        "  TabularDataIndex INTEGER PRIMARY KEY,"
        "  ReportName TEXT,"
        "  ReportForString TEXT,"
        "  TableName TEXT,"
        "  RowName TEXT,"
        "  ColumnName TEXT,"
        "  Units TEXT,"
        "  Value TEXT"
        ")"
    )

    # Insert variable definitions
    cur.execute(
        "INSERT INTO ReportDataDictionary VALUES (1, 0, 'Zone', 'Facility', "
        "'Zone', '*', 'Site Outdoor Air Drybulb Temperature', 'Hourly', '', 'C')"
    )
    cur.execute(
        "INSERT INTO ReportDataDictionary VALUES (2, 0, 'Zone', 'Facility', "
        "'Zone', 'THERMAL ZONE 1', 'Zone Mean Air Temperature', 'Hourly', '', 'C')"
    )
    cur.execute(
        "INSERT INTO ReportDataDictionary VALUES (3, 1, 'Zone', 'Facility', "
        "'Zone', '', 'Electricity:Facility', 'Hourly', '', 'J')"
    )

    # Insert time entries (warmup + real data)
    # Warmup entry
    cur.execute("INSERT INTO Time VALUES (1, 2017, 1, 1, 1, 0, 0, 60, 1, 1, 'SummerDesignDay', 1, 'WinterDesignDay')")
    # Real entries
    cur.execute("INSERT INTO Time VALUES (2, 2017, 1, 1, 1, 0, 0, 60, 1, 1, 'Monday', 0, 'Denver Centennial')")
    cur.execute("INSERT INTO Time VALUES (3, 2017, 1, 1, 2, 0, 0, 60, 1, 1, 'Monday', 0, 'Denver Centennial')")
    cur.execute("INSERT INTO Time VALUES (4, 2017, 1, 1, 3, 0, 0, 60, 1, 1, 'Monday', 0, 'Denver Centennial')")
    # Hour=24 edge case
    cur.execute("INSERT INTO Time VALUES (5, 2017, 1, 1, 24, 0, 0, 60, 1, 1, 'Monday', 0, 'Denver Centennial')")

    # Insert report data
    # Warmup data (should be filtered out)
    cur.execute("INSERT INTO ReportData VALUES (1, 1, 1, -99.0)")

    # Real data for outdoor temp
    cur.execute("INSERT INTO ReportData VALUES (2, 2, 1, -5.2)")
    cur.execute("INSERT INTO ReportData VALUES (3, 3, 1, -5.5)")
    cur.execute("INSERT INTO ReportData VALUES (4, 4, 1, -5.8)")
    cur.execute("INSERT INTO ReportData VALUES (5, 5, 1, -6.0)")

    # Real data for zone temp
    cur.execute("INSERT INTO ReportData VALUES (6, 2, 2, 21.3)")
    cur.execute("INSERT INTO ReportData VALUES (7, 3, 2, 21.1)")
    cur.execute("INSERT INTO ReportData VALUES (8, 4, 2, 20.9)")
    cur.execute("INSERT INTO ReportData VALUES (9, 5, 2, 20.7)")

    # Insert tabular data
    cur.execute(
        "INSERT INTO TabularDataWithStrings VALUES "
        "(1, 'AnnualBuildingUtilityPerformanceSummary', 'Entire Facility', "
        "'End Uses', 'Heating', 'Electricity', 'GJ', '12.50')"
    )
    cur.execute(
        "INSERT INTO TabularDataWithStrings VALUES "
        "(2, 'AnnualBuildingUtilityPerformanceSummary', 'Entire Facility', "
        "'End Uses', 'Cooling', 'Electricity', 'GJ', '8.30')"
    )
    cur.execute(
        "INSERT INTO TabularDataWithStrings VALUES "
        "(3, 'EnvelopeSummary', 'Entire Facility', "
        "'Opaque Exterior', 'Wall 1', 'U-Factor', 'W/m2-K', '0.35')"
    )

    conn.commit()
    conn.close()
    return db_path


class TestSQLResultTimeSeries:
    """Tests for get_timeseries()."""

    def test_get_outdoor_temp(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("Site Outdoor Air Drybulb Temperature")
        assert len(ts.values) == 4
        assert ts.values[0] == -5.2
        assert ts.units == "C"
        assert ts.variable_name == "Site Outdoor Air Drybulb Temperature"

    def test_warmup_filtered(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("Site Outdoor Air Drybulb Temperature")
        # Warmup entry (-99.0) should not appear
        assert -99.0 not in ts.values

    def test_timestamps(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("Site Outdoor Air Drybulb Temperature")
        assert ts.timestamps[0] == datetime(2017, 1, 1, 1, 0)
        assert ts.timestamps[1] == datetime(2017, 1, 1, 2, 0)

    def test_hour_24_rollover(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("Site Outdoor Air Drybulb Temperature")
        # Hour=24 should become next day hour=0
        assert ts.timestamps[3] == datetime(2017, 1, 2, 0, 0)

    def test_get_by_key_value(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("Zone Mean Air Temperature", "THERMAL ZONE 1")
        assert len(ts.values) == 4
        assert ts.key_value == "THERMAL ZONE 1"

    def test_variable_not_found(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql, pytest.raises(KeyError, match="Variable not found"):
            sql.get_timeseries("Nonexistent Variable")

    def test_frequency(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("Site Outdoor Air Drybulb Temperature")
        assert ts.frequency == "Hourly"


class TestSQLResultTabular:
    """Tests for get_tabular_data()."""

    def test_get_all(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            rows = sql.get_tabular_data()
        assert len(rows) == 3
        assert all(isinstance(r, TabularRow) for r in rows)

    def test_filter_by_report(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            rows = sql.get_tabular_data(report_name="AnnualBuildingUtilityPerformanceSummary")
        assert len(rows) == 2
        assert rows[0].row_name == "Heating"
        assert rows[1].row_name == "Cooling"

    def test_filter_by_table(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            rows = sql.get_tabular_data(table_name="Opaque Exterior")
        assert len(rows) == 1
        assert rows[0].value == "0.35"

    def test_filter_by_both(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            rows = sql.get_tabular_data(
                report_name="AnnualBuildingUtilityPerformanceSummary",
                table_name="End Uses",
            )
        assert len(rows) == 2


class TestSQLResultListVariables:
    """Tests for list_variables()."""

    def test_list_all(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            variables = sql.list_variables()
        assert len(variables) == 3
        assert all(isinstance(v, VariableInfo) for v in variables)

    def test_variable_info_fields(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            variables = sql.list_variables()
        temp = variables[0]
        assert temp.name == "Site Outdoor Air Drybulb Temperature"
        assert temp.units == "C"
        assert temp.is_meter is False
        assert temp.variable_type == "Zone"

    def test_meter_detected(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            variables = sql.list_variables()
        meter = variables[2]
        assert meter.name == "Electricity:Facility"
        assert meter.is_meter is True


class TestSQLResultListReports:
    """Tests for list_reports()."""

    def test_list_reports(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            reports = sql.list_reports()
        assert reports == ["AnnualBuildingUtilityPerformanceSummary", "EnvelopeSummary"]


class TestSQLResultRawQuery:
    """Tests for query()."""

    def test_raw_query(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            rows = sql.query("SELECT COUNT(*) FROM ReportData")
        assert rows[0][0] == 9

    def test_parameterized_query(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            rows = sql.query("SELECT Value FROM ReportData WHERE Value < ?", (-5.5,))
        # Includes warmup (-99.0), -5.8, and -6.0
        assert len(rows) == 3


class TestSQLResultContextManager:
    """Tests for context manager protocol."""

    def test_context_manager(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            variables = sql.list_variables()
        assert len(variables) == 3

    def test_close(self, sql_db: Path) -> None:
        sql = SQLResult(sql_db)
        sql.close()
        with pytest.raises(sqlite3.ProgrammingError):
            sql.list_variables()


class TestTimeSeriesResultFrozen:
    """Tests for TimeSeriesResult immutability."""

    def test_frozen(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("Site Outdoor Air Drybulb Temperature")
        with pytest.raises(AttributeError):
            ts.variable_name = "changed"  # type: ignore[misc]
