"""Tests for the SQL parser.

The SQL parser tests use a programmatically-generated SQLite fixture rather than
a pre-built binary file. This approach is preferred because:

1. **Self-documenting**: The fixture code shows exactly what schema and data are
   being tested, making test failures easier to understand.
2. **Fresh state**: Each test gets a clean database, avoiding state pollution.
3. **Version control friendly**: No binary files that are hard to review in PRs.
4. **Schema evolution**: Easy to update when EnergyPlus output schema changes.

The fixture creates a minimal EnergyPlus-schema database with:
- ReportDataDictionary: Variable and meter definitions
- Time: Timestamp entries with warmup/sizing/annual periods
- EnvironmentPeriods: Design day and run period definitions
- ReportData: Time-series values
- TabularDataWithStrings: Tabular report data

This mirrors the real EnergyPlus SQLite output structure documented at:
https://docs.idfkit.com/v25.2/output-details/output-files/eplusout-sql/
"""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

from idfkit.exceptions import ResultLookupError
from idfkit.simulation.parsers.sql import EnvironmentInfo, SQLResult, TabularRow, VariableInfo


@pytest.fixture()
def sql_db(tmp_path: Path) -> Path:
    """Create a minimal EnergyPlus-schema SQLite database for testing.

    This fixture creates a database with:
    - 3 variables (2 zone temps, 1 meter)
    - 2 environment periods (design day + annual)
    - 6 time entries (1 warmup, 1 sizing, 4 annual including Hour=24 edge case)
    - 11 data points
    - 3 tabular data rows
    """
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
        # Default environment=None returns all data (sizing + annual)
        assert len(ts.values) == 5
        assert ts.values[0] == -17.0  # Sizing data first
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
        # Default environment=None returns all data (sizing + annual)
        assert len(ts.values) == 5
        assert ts.key_value == "THERMAL ZONE 1"

    def test_variable_not_found(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql, pytest.raises(KeyError, match="'Nonexistent Variable' is not in this run"):
            sql.get_timeseries("Nonexistent Variable")

    def test_frequency(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("Site Outdoor Air Drybulb Temperature")
        assert ts.frequency == "Hourly"


def _add_multi_key_outputs(db_path: Path) -> None:
    """Add a variable reported for three zones and a meter reported at two frequencies."""
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    for index, key in ((10, "PLENUM-1"), (11, "SPACE1-1"), (12, "SPACE2-1")):
        cur.execute(
            "INSERT INTO ReportDataDictionary VALUES (?, 0, 'Zone', 'Facility', 'Zone', ?, "
            "'Zone Air Temperature', 'Hourly', '', 'C')",
            (index, key),
        )
        cur.execute(
            "INSERT INTO ReportData (TimeIndex, ReportDataDictionaryIndex, Value) VALUES (3, ?, ?)", (index, index)
        )
    for index, freq in ((20, "Hourly"), (21, "Monthly")):
        cur.execute(
            "INSERT INTO ReportDataDictionary VALUES (?, 1, 'Zone', 'Facility', 'Zone', NULL, "
            "'Electricity:Building', ?, '', 'J')",
            (index, freq),
        )
        cur.execute(
            "INSERT INTO ReportData (TimeIndex, ReportDataDictionaryIndex, Value) VALUES (3, ?, ?)", (index, index)
        )
    conn.commit()
    conn.close()


class TestSQLResultLookup:
    """get_timeseries() resolves to one series, case-insensitively, and explains a failed lookup."""

    def test_default_key_refuses_a_variable_reported_for_several_keys(self, sql_db: Path) -> None:
        _add_multi_key_outputs(sql_db)
        with SQLResult(sql_db) as sql, pytest.raises(ResultLookupError) as exc_info:
            sql.get_timeseries("Zone Air Temperature")
        assert str(exc_info.value) == (
            "Variable 'Zone Air Temperature' is reported for 3 keys (PLENUM-1, SPACE1-1, SPACE2-1); "
            "pass key_value= to pick one."
        )
        assert exc_info.value.available == ("PLENUM-1", "SPACE1-1", "SPACE2-1")

    def test_several_frequencies_ask_for_one(self, sql_db: Path) -> None:
        _add_multi_key_outputs(sql_db)
        with SQLResult(sql_db) as sql:
            with pytest.raises(ResultLookupError, match=r"at 2 frequencies \(Hourly, Monthly\); pass frequency="):
                sql.get_timeseries("Electricity:Building")
            ts = sql.get_timeseries("Electricity:Building", frequency="monthly")
        assert ts.frequency == "Monthly"
        assert ts.values == (21.0,)

    def test_default_key_still_reads_a_single_key_variable(self, sql_db: Path) -> None:
        _add_multi_key_outputs(sql_db)
        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("Zone Mean Air Temperature")
        assert ts.key_value == "THERMAL ZONE 1"

    def test_name_key_and_frequency_ignore_case(self, sql_db: Path) -> None:
        _add_multi_key_outputs(sql_db)
        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("zone air temperature", "space1-1", frequency="HOURLY")
        assert (ts.variable_name, ts.key_value, ts.values) == ("Zone Air Temperature", "SPACE1-1", (11.0,))

    def test_unknown_variable_suggests_the_closest_name(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql, pytest.raises(ResultLookupError) as exc_info:
            sql.get_timeseries("Zone Mean Air Temprature", "THERMAL ZONE 1")
        err = exc_info.value
        assert isinstance(err, KeyError)
        assert str(err).startswith(
            "Variable 'Zone Mean Air Temprature' is not in this run's output. "
            "Did you mean 'Zone Mean Air Temperature'? Request it with an Output:Variable"
        )
        assert err.suggestions == ("Zone Mean Air Temperature",)

    def test_unknown_key_lists_the_reported_keys(self, sql_db: Path) -> None:
        _add_multi_key_outputs(sql_db)
        with SQLResult(sql_db) as sql, pytest.raises(ResultLookupError) as exc_info:
            sql.get_timeseries("Zone Air Temperature", "SPACE9-1")
        assert str(exc_info.value) == (
            "Variable 'Zone Air Temperature' has no key 'SPACE9-1'. Did you mean 'SPACE2-1'? "
            "It is reported for 3 keys: PLENUM-1, SPACE1-1, SPACE2-1."
        )

    def test_unknown_frequency_lists_the_reported_ones(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql, pytest.raises(ResultLookupError) as exc_info:
            sql.get_timeseries("Zone Mean Air Temperature", "THERMAL ZONE 1", frequency="Daily")
        assert str(exc_info.value) == (
            "Variable 'Zone Mean Air Temperature' for key 'THERMAL ZONE 1' is not reported at frequency 'Daily'. "
            "It is reported at: Hourly."
        )

    def test_long_key_lists_are_truncated(self, tmp_path: Path, sql_db: Path) -> None:
        conn = sqlite3.connect(str(sql_db))
        for i in range(12):
            conn.execute(
                "INSERT INTO ReportDataDictionary VALUES (?, 0, 'Zone', 'Facility', 'Zone', ?, 'Surface Temp', 'Hourly', '', 'C')",
                (100 + i, f"WALL {i:02d}"),
            )
        conn.commit()
        conn.close()
        with (
            SQLResult(sql_db) as sql,
            pytest.raises(ResultLookupError, match=r"WALL 09 and 2 more\); pass key_value="),
        ):
            sql.get_timeseries("Surface Temp")

    def test_error_survives_pickling(self) -> None:
        import pickle

        err = ResultLookupError("Variable 'X' is not in this run's output.", suggestions=("Y",), available=("A",))
        copy = pickle.loads(pickle.dumps(err))  # noqa: S301
        assert (str(copy), copy.suggestions, copy.available) == (str(err), ("Y",), ("A",))


def _add_monthly_zone_temperature(db_path: Path, frequency: str = "Monthly") -> None:
    """Report 'Zone Mean Air Temperature' for THERMAL ZONE 1 at a second frequency."""
    conn = sqlite3.connect(str(db_path))
    conn.execute(
        "INSERT INTO ReportDataDictionary VALUES (30, 0, 'Zone', 'Facility', 'Zone', 'THERMAL ZONE 1', "
        "'Zone Mean Air Temperature', ?, '', 'C')",
        (frequency,),
    )
    conn.execute("INSERT INTO ReportData (TimeIndex, ReportDataDictionaryIndex, Value) VALUES (3, 30, 50.0)")
    conn.commit()
    conn.close()


class _HeatmapBackend:
    """Records the heatmap call made by plot_comfort_hours."""

    def __init__(self) -> None:
        self.data: list[list[float]] = []

    def heatmap(self, data: list[list[float]], **kwargs: Any) -> str:
        self.data = data
        return "heatmap"


class TestPlotComfortHoursWithSQLResult:
    """plot_comfort_hours() reads a real SQLResult whose temperature is reported at several frequencies."""

    def test_prefers_hourly_when_several_frequencies_are_reported(self, sql_db: Path) -> None:
        from idfkit.simulation.plotting.visualizations import plot_comfort_hours

        _add_monthly_zone_temperature(sql_db)
        backend = _HeatmapBackend()
        with SQLResult(sql_db) as sql:
            assert plot_comfort_hours(sql, ["THERMAL ZONE 1"], backend=backend) == "heatmap"  # type: ignore[arg-type]
        # The hourly series lies in 20-26 C; the monthly 50 C value would have given 0 %.
        assert backend.data[0][0] == 100.0

    def test_frequency_argument_picks_the_series(self, sql_db: Path) -> None:
        from idfkit.simulation.plotting.visualizations import plot_comfort_hours

        _add_monthly_zone_temperature(sql_db)
        backend = _HeatmapBackend()
        with SQLResult(sql_db) as sql:
            plot_comfort_hours(sql, ["THERMAL ZONE 1"], frequency="Monthly", backend=backend)  # type: ignore[arg-type]
        assert backend.data[0][0] == 0.0

    def test_no_hourly_series_still_asks_for_frequency(self, sql_db: Path) -> None:
        from idfkit.simulation.plotting.visualizations import plot_comfort_hours

        conn = sqlite3.connect(str(sql_db))
        conn.execute(
            "UPDATE ReportDataDictionary SET ReportingFrequency = 'Zone Timestep' WHERE ReportDataDictionaryIndex = 2"
        )
        conn.commit()
        conn.close()
        _add_monthly_zone_temperature(sql_db)
        with SQLResult(sql_db) as sql, pytest.raises(ResultLookupError, match="pass frequency="):
            plot_comfort_hours(sql, ["THERMAL ZONE 1"], backend=_HeatmapBackend())  # type: ignore[arg-type]


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

    def test_default_returns_all(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("Site Outdoor Air Drybulb Temperature")
        # Default environment=None returns all data (sizing + annual)
        assert len(ts.values) == 5
        assert ts.values[0] == -17.0  # Sizing data first

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

    def test_filter_by_row_name(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            rows = sql.get_tabular_data(row_name="Heating")
        assert len(rows) == 1
        assert rows[0].value == "12.50"

    def test_filter_by_column_name(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            rows = sql.get_tabular_data(column_name="Electricity")
        assert len(rows) == 2
        assert {r.row_name for r in rows} == {"Heating", "Cooling"}

    def test_filter_by_report_for(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            rows = sql.get_tabular_data(report_for="Entire Facility")
        assert len(rows) == 3  # All rows have "Entire Facility"

    def test_combined_filters(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            rows = sql.get_tabular_data(
                report_name="AnnualBuildingUtilityPerformanceSummary",
                row_name="Cooling",
                column_name="Electricity",
            )
        assert len(rows) == 1
        assert rows[0].value == "8.30"


class TestSQLResultGetTabularValue:
    """Tests for get_tabular_value()."""

    def test_found(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            val = sql.get_tabular_value(
                report_name="AnnualBuildingUtilityPerformanceSummary",
                table_name="End Uses",
                row_name="Heating",
                column_name="Electricity",
            )
        assert val == "12.50"

    def test_not_found_raises(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql, pytest.raises(KeyError, match="No tabular row 'Nonexistent'"):
            sql.get_tabular_value(
                report_name="AnnualBuildingUtilityPerformanceSummary",
                table_name="End Uses",
                row_name="Nonexistent",
                column_name="Electricity",
            )

    def test_custom_report_for(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql:
            val = sql.get_tabular_value(
                report_name="EnvelopeSummary",
                table_name="Opaque Exterior",
                row_name="Wall 1",
                column_name="U-Factor",
                report_for="Entire Facility",
            )
        assert val == "0.35"

    def test_multiple_matches_raises(self, tmp_path: Path) -> None:
        """get_tabular_value raises KeyError when more than one row matches."""
        db_path = tmp_path / "dup.sql"
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE TabularDataWithStrings ("
            "  TabularDataIndex INTEGER PRIMARY KEY,"
            "  ReportName TEXT, ReportForString TEXT,"
            "  TableName TEXT, RowName TEXT, ColumnName TEXT,"
            "  Units TEXT, Value TEXT)"
        )
        # Insert two rows that match the same report/table/row/column/reportFor
        cur.execute(
            "INSERT INTO TabularDataWithStrings VALUES (1, 'R', 'Entire Facility', 'T', 'Row', 'Col', 'W', '1.0')"
        )
        cur.execute(
            "INSERT INTO TabularDataWithStrings VALUES (2, 'R', 'Entire Facility', 'T', 'Row', 'Col', 'W', '2.0')"
        )
        conn.commit()
        conn.close()

        with SQLResult(db_path) as sql, pytest.raises(KeyError, match="Multiple rows found"):
            sql.get_tabular_value(
                report_name="R",
                table_name="T",
                row_name="Row",
                column_name="Col",
            )


class TestSQLResultGetTabularValueErrors:
    """get_tabular_value() names the argument that matches nothing, with the closest spelling."""

    def test_misspelt_report_suggests_the_report(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql, pytest.raises(ResultLookupError) as exc_info:
            sql.get_tabular_value("AnnualBuildingUtilityPerformanceSumary", "End Uses", "Heating", "Electricity")
        assert str(exc_info.value) == (
            "No tabular report 'AnnualBuildingUtilityPerformanceSumary'. "
            "Did you mean 'AnnualBuildingUtilityPerformanceSummary'? list_reports() lists them all."
        )

    def test_misspelt_table_lists_the_report_tables(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql, pytest.raises(ResultLookupError) as exc_info:
            sql.get_tabular_value("AnnualBuildingUtilityPerformanceSummary", "End Use", "Heating", "Electricity")
        assert str(exc_info.value) == (
            "No tabular table 'End Use' in report 'AnnualBuildingUtilityPerformanceSummary', "
            "report_for 'Entire Facility'. Did you mean 'End Uses'? Available: End Uses."
        )

    def test_unknown_column_is_named(self, sql_db: Path) -> None:
        with SQLResult(sql_db) as sql, pytest.raises(ResultLookupError, match="No tabular column 'Gas'"):
            sql.get_tabular_value("AnnualBuildingUtilityPerformanceSummary", "End Uses", "Heating", "Gas")


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


class TestTimeSeriesResultToDataframe:
    """Tests for TimeSeriesResult.to_dataframe() and SQLResult.to_dataframe()."""

    def test_no_pandas_raises_import_error(self, sql_db: Path) -> None:
        """to_dataframe() raises ImportError when pandas is not installed."""
        import sys

        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("Site Outdoor Air Drybulb Temperature")

        saved = sys.modules.get("pandas")
        sys.modules["pandas"] = None  # type: ignore[assignment]
        try:
            with pytest.raises(ImportError, match="pandas is required"):
                ts.to_dataframe()
        finally:
            if saved is None:
                del sys.modules["pandas"]
            else:
                sys.modules["pandas"] = saved

    def test_to_dataframe_with_pandas(self, sql_db: Path) -> None:
        """to_dataframe() returns a DataFrame when pandas is installed."""
        pytest.importorskip("pandas")
        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("Site Outdoor Air Drybulb Temperature", environment="annual")
        df = ts.to_dataframe()
        assert hasattr(df, "index")
        assert len(df) == 4

    def test_sql_result_to_dataframe_no_pandas(self, sql_db: Path) -> None:
        """SQLResult.to_dataframe() raises ImportError when pandas is not installed."""
        import sys

        saved = sys.modules.get("pandas")
        sys.modules["pandas"] = None  # type: ignore[assignment]
        try:
            with SQLResult(sql_db) as sql, pytest.raises(ImportError, match="pandas is required"):
                sql.to_dataframe("Site Outdoor Air Drybulb Temperature")
        finally:
            if saved is None:
                del sys.modules["pandas"]
            else:
                sys.modules["pandas"] = saved

    def test_sql_result_to_dataframe_with_pandas(self, sql_db: Path) -> None:
        """SQLResult.to_dataframe() returns a DataFrame when pandas is installed."""
        pytest.importorskip("pandas")
        with SQLResult(sql_db) as sql:
            df = sql.to_dataframe("Site Outdoor Air Drybulb Temperature", environment="annual")
        assert hasattr(df, "index")
        assert len(df) == 4


class TestTimeSeriesResultPlot:
    """Tests for TimeSeriesResult.plot()."""

    def test_plot_calls_backend(self, sql_db: Path) -> None:
        """plot() delegates to the backend's line() method."""
        from unittest.mock import MagicMock

        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("Site Outdoor Air Drybulb Temperature", environment="annual")

        backend = MagicMock()
        backend.line.return_value = MagicMock()
        ts.plot(backend=backend)
        backend.line.assert_called_once()
        call_kwargs = backend.line.call_args[1]
        assert "title" in call_kwargs
        assert "xlabel" in call_kwargs
        assert "ylabel" in call_kwargs

    def test_plot_auto_detects_backend(self, sql_db: Path) -> None:
        """plot() calls get_default_backend() when no backend is provided."""
        from unittest.mock import MagicMock, patch

        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries("Site Outdoor Air Drybulb Temperature", environment="annual")

        mock_backend = MagicMock()
        mock_backend.line.return_value = MagicMock()
        with patch("idfkit.simulation.plotting.get_default_backend", return_value=mock_backend) as mock_get:
            ts.plot()
        mock_get.assert_called_once()
        mock_backend.line.assert_called_once()


class TestGetTimeseriesInvalidEnvironment:
    """Tests for get_timeseries() with invalid environment parameter."""

    def test_invalid_environment_raises_value_error(self, sql_db: Path) -> None:
        """Passing an unrecognized environment string raises ValueError."""
        with SQLResult(sql_db) as sql, pytest.raises(ValueError, match="environment must be"):
            sql.get_timeseries(
                "Site Outdoor Air Drybulb Temperature",
                environment="bogus",  # type: ignore[arg-type]
            )

    def test_get_timeseries_with_frequency_filter(self, sql_db: Path) -> None:
        """Passing frequency filters by reporting frequency."""
        with SQLResult(sql_db) as sql:
            ts = sql.get_timeseries(
                "Site Outdoor Air Drybulb Temperature",
                environment="annual",
                frequency="Hourly",
            )
        assert len(ts.values) == 4
