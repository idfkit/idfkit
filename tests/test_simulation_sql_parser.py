"""Tests for the SQL parser."""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

import pytest

from idfkit.simulation.parsers.sql import EnvironmentInfo, SQLResult, TabularRow, VariableInfo


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
        "  Type TEXT,"
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
        "  EnvironmentPeriodIndex INTEGER,"
        "  WarmupFlag INTEGER"
        ")"
    )

    cur.execute(
        "CREATE TABLE EnvironmentPeriods ("
        "  EnvironmentPeriodIndex INTEGER PRIMARY KEY,"
        "  SimulationIndex INTEGER,"
        "  EnvironmentName TEXT,"
        "  EnvironmentType INTEGER"
        ")"
    )

    # Environment periods: 1 = DesignDay (sizing), 3 = WeatherFileRunPeriod (annual)
    cur.execute("INSERT INTO EnvironmentPeriods VALUES (1, 1, 'Winter Design Day', 1)")
    cur.execute("INSERT INTO EnvironmentPeriods VALUES (2, 1, 'RUN PERIOD 1', 3)")

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

    # Insert time entries (warmup + sizing + annual data)
    # Warmup entry (WarmupFlag=1, sizing env)
    cur.execute("INSERT INTO Time VALUES (1, 2017, 1, 1, 1, 0, 0, 60, 1, 1, 'SummerDesignDay', 1, 1)")
    # Sizing (design day) entry (WarmupFlag=0)
    cur.execute("INSERT INTO Time VALUES (2, 2017, 12, 21, 1, 0, 0, 60, 1, 1, 'WinterDesignDay', 1, 0)")
    # Annual (run period) entries (WarmupFlag=0)
    cur.execute("INSERT INTO Time VALUES (3, 2017, 1, 1, 1, 0, 0, 60, 1, 1, 'Monday', 2, 0)")
    cur.execute("INSERT INTO Time VALUES (4, 2017, 1, 1, 2, 0, 0, 60, 1, 1, 'Monday', 2, 0)")
    cur.execute("INSERT INTO Time VALUES (5, 2017, 1, 1, 3, 0, 0, 60, 1, 1, 'Monday', 2, 0)")
    # Hour=24 edge case (annual)
    cur.execute("INSERT INTO Time VALUES (6, 2017, 1, 1, 24, 0, 0, 60, 1, 1, 'Monday', 2, 0)")

    # Insert report data
    # Warmup data (should be filtered out)
    cur.execute("INSERT INTO ReportData VALUES (1, 1, 1, -99.0)")

    # Sizing (design day) data for outdoor temp
    cur.execute("INSERT INTO ReportData VALUES (2, 2, 1, -17.0)")

    # Annual data for outdoor temp
    cur.execute("INSERT INTO ReportData VALUES (3, 3, 1, -5.2)")
    cur.execute("INSERT INTO ReportData VALUES (4, 4, 1, -5.5)")
    cur.execute("INSERT INTO ReportData VALUES (5, 5, 1, -5.8)")
    cur.execute("INSERT INTO ReportData VALUES (6, 6, 1, -6.0)")

    # Sizing (design day) data for zone temp
    cur.execute("INSERT INTO ReportData VALUES (7, 2, 2, 18.0)")

    # Annual data for zone temp
    cur.execute("INSERT INTO ReportData VALUES (8, 3, 2, 21.3)")
    cur.execute("INSERT INTO ReportData VALUES (9, 4, 2, 21.1)")
    cur.execute("INSERT INTO ReportData VALUES (10, 5, 2, 20.9)")
    cur.execute("INSERT INTO ReportData VALUES (11, 6, 2, 20.7)")

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
        # Default environment="annual" returns only run-period data
        assert len(ts.values) == 4
        assert ts.values[0] == -5.2
        assert ts.units == "C"
        assert ts.variable_name == "Site Outdoor Air Drybulb Temperature"

    def test_warmup_filtered(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("Site Outdoor Air Drybulb Temperature")
        # Warmup entry (-99.0) should not appear
        assert -99.0 not in ts.values

    def test_null_warmup_flag_included(self, tmp_path: Path) -> None:
        """EnergyPlus 24.1+ may leave WarmupFlag as NULL; data should be included."""
        db_path = tmp_path / "null_warmup.sql"
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE ReportDataDictionary ("
            "  ReportDataDictionaryIndex INTEGER PRIMARY KEY,"
            "  IsMeter INTEGER, Type TEXT, IndexGroup TEXT, TimestepType TEXT,"
            "  KeyValue TEXT, Name TEXT, ReportingFrequency TEXT,"
            "  ScheduleName TEXT, Units TEXT)"
        )
        cur.execute(
            "CREATE TABLE Time ("
            "  TimeIndex INTEGER PRIMARY KEY, Year INTEGER, Month INTEGER,"
            "  Day INTEGER, Hour INTEGER, Minute INTEGER, Dst INTEGER,"
            "  Interval INTEGER, IntervalType INTEGER, SimulationDays INTEGER,"
            "  DayType TEXT, EnvironmentPeriodIndex INTEGER, WarmupFlag INTEGER)"
        )
        cur.execute(
            "CREATE TABLE ReportData ("
            "  ReportDataIndex INTEGER PRIMARY KEY, TimeIndex INTEGER,"
            "  ReportDataDictionaryIndex INTEGER, Value REAL)"
        )
        cur.execute(
            "CREATE TABLE EnvironmentPeriods ("
            "  EnvironmentPeriodIndex INTEGER PRIMARY KEY,"
            "  SimulationIndex INTEGER, EnvironmentName TEXT, EnvironmentType INTEGER)"
        )
        cur.execute(
            "INSERT INTO ReportDataDictionary VALUES "
            "(1, 0, 'Avg', 'Facility', 'Zone', '*', 'TestVar', 'Hourly', '', 'C')"
        )
        cur.execute("INSERT INTO EnvironmentPeriods VALUES (3, 1, 'RUN PERIOD 1', 3)")
        # NULL WarmupFlag (matches real EnergyPlus 24.1.0 behavior)
        cur.execute("INSERT INTO Time VALUES (1, 2013, 1, 1, 1, 0, 0, 60, 1, 1, 'Monday', 3, NULL)")
        cur.execute("INSERT INTO Time VALUES (2, 2013, 1, 1, 2, 0, 0, 60, 1, 1, 'Monday', 3, NULL)")
        cur.execute("INSERT INTO ReportData VALUES (1, 1, 1, 20.0)")
        cur.execute("INSERT INTO ReportData VALUES (2, 2, 1, 21.0)")
        conn.commit()
        conn.close()

        with SQLResult(db_path) as sql:
            ts = sql.get_timeseries("TestVar")
        assert len(ts.values) == 2
        assert ts.values == (20.0, 21.0)
        assert ts.timestamps[0] == datetime(2013, 1, 1, 1, 0)

    def test_timestamps(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("Site Outdoor Air Drybulb Temperature", environment="annual")
        assert ts.timestamps[0] == datetime(2017, 1, 1, 1, 0)
        assert ts.timestamps[1] == datetime(2017, 1, 1, 2, 0)

    def test_hour_24_rollover(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("Site Outdoor Air Drybulb Temperature", environment="annual")
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


class TestSQLResultEnvironmentFilter:
    """Tests for get_timeseries() with environment parameter."""

    def test_annual_only(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("Site Outdoor Air Drybulb Temperature", environment="annual")
        assert len(ts.values) == 4
        assert ts.values[0] == -5.2

    def test_sizing_only(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("Site Outdoor Air Drybulb Temperature", environment="sizing")
        assert len(ts.values) == 1
        assert ts.values[0] == -17.0
        assert ts.timestamps[0] == datetime(2017, 12, 21, 1, 0)

    def test_default_is_annual(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("Site Outdoor Air Drybulb Temperature")
        assert len(ts.values) == 4
        assert ts.values[0] == -5.2

    def test_none_returns_all(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("Site Outdoor Air Drybulb Temperature", environment=None)
        # 1 sizing + 4 annual = 5
        assert len(ts.values) == 5

    def test_invalid_environment(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql, pytest.raises(ValueError, match="environment must be"):
            sql.get_timeseries("Site Outdoor Air Drybulb Temperature", environment="invalid")  # type: ignore[arg-type]

    def test_zone_temp_annual(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("Zone Mean Air Temperature", environment="annual")
        assert len(ts.values) == 4
        assert ts.values == (21.3, 21.1, 20.9, 20.7)

    def test_zone_temp_sizing(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("Zone Mean Air Temperature", environment="sizing")
        assert len(ts.values) == 1
        assert ts.values[0] == 18.0


class TestSQLResultListEnvironments:
    """Tests for list_environments()."""

    def test_list_environments(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            envs = sql.list_environments()
        assert len(envs) == 2
        assert all(isinstance(e, EnvironmentInfo) for e in envs)

    def test_environment_info_fields(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            envs = sql.list_environments()
        assert envs[0].name == "Winter Design Day"
        assert envs[0].environment_type == 1
        assert envs[1].name == "RUN PERIOD 1"
        assert envs[1].environment_type == 3


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
        assert rows[0][0] == 11

    def test_parameterized_query(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            rows = sql.query("SELECT Value FROM ReportData WHERE Value < ?", (-5.5,))
        # Includes warmup (-99.0), sizing (-17.0), annual (-5.8, -6.0)
        assert len(rows) == 4


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
