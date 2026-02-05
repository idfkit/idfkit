"""Tests for SimulationResult lazy properties."""

from __future__ import annotations

import shutil
import sqlite3
from pathlib import Path

import pytest
from conftest import InMemoryFileSystem

from idfkit.simulation.outputs import OutputVariableIndex
from idfkit.simulation.parsers.csv import CSVResult
from idfkit.simulation.parsers.sql import SQLResult
from idfkit.simulation.result import SimulationResult

FIXTURES = Path(__file__).parent / "fixtures" / "simulation"


def _create_minimal_sql(path: Path) -> None:
    """Create a minimal EnergyPlus SQLite database."""
    conn = sqlite3.connect(str(path))
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE ReportDataDictionary ("
        "  ReportDataDictionaryIndex INTEGER PRIMARY KEY,"
        "  IsMeter INTEGER, Type TEXT, IndexGroup TEXT,"
        "  TimestepType TEXT, KeyValue TEXT, Name TEXT,"
        "  ReportingFrequency TEXT, ScheduleName TEXT, Units TEXT)"
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
        "  ReportDataIndex INTEGER PRIMARY KEY,"
        "  TimeIndex INTEGER, ReportDataDictionaryIndex INTEGER, Value REAL)"
    )
    cur.execute(
        "CREATE TABLE TabularDataWithStrings ("
        "  TabularDataIndex INTEGER PRIMARY KEY, ReportName TEXT,"
        "  ReportForString TEXT, TableName TEXT, RowName TEXT,"
        "  ColumnName TEXT, Units TEXT, Value TEXT)"
    )
    cur.execute(
        "CREATE TABLE EnvironmentPeriods ("
        "  EnvironmentPeriodIndex INTEGER PRIMARY KEY,"
        "  SimulationIndex INTEGER, EnvironmentName TEXT, EnvironmentType INTEGER)"
    )
    cur.execute(
        "INSERT INTO ReportDataDictionary VALUES "
        "(1, 0, 'Zone', 'Facility', 'Zone', '*', "
        "'Site Outdoor Air Drybulb Temperature', 'Hourly', '', 'C')"
    )
    cur.execute("INSERT INTO EnvironmentPeriods VALUES (1, 1, 'RUN PERIOD 1', 3)")
    cur.execute("INSERT INTO Time VALUES (1, 2017, 1, 1, 1, 0, 0, 60, 1, 1, 'Monday', 1, 0)")
    cur.execute("INSERT INTO ReportData VALUES (1, 1, 1, -5.0)")
    conn.commit()
    conn.close()


@pytest.fixture()
def result_dir(tmp_path: Path) -> Path:
    """Create a simulation output directory with all file types."""
    shutil.copy(FIXTURES / "sample.rdd", tmp_path / "eplusout.rdd")
    shutil.copy(FIXTURES / "sample.mdd", tmp_path / "eplusout.mdd")
    shutil.copy(FIXTURES / "sample.csv", tmp_path / "eplusout.csv")
    shutil.copy(FIXTURES / "sample.err", tmp_path / "eplusout.err")
    _create_minimal_sql(tmp_path / "eplusout.sql")
    return tmp_path


@pytest.fixture()
def result(result_dir: Path) -> SimulationResult:
    """Create a SimulationResult from the test directory."""
    return SimulationResult(
        run_dir=result_dir,
        success=True,
        exit_code=0,
        stdout="",
        stderr="",
        runtime_seconds=1.0,
    )


class TestSqlProperty:
    """Tests for SimulationResult.sql."""

    def test_returns_sql_result(self, result: SimulationResult) -> None:
        sql = result.sql
        assert isinstance(sql, SQLResult)

    def test_is_cached(self, result: SimulationResult) -> None:
        sql1 = result.sql
        sql2 = result.sql
        assert sql1 is sql2

    def test_none_when_no_file(self, tmp_path: Path) -> None:
        r = SimulationResult(
            run_dir=tmp_path,
            success=True,
            exit_code=0,
            stdout="",
            stderr="",
            runtime_seconds=0.0,
        )
        assert r.sql is None

    def test_can_query(self, result: SimulationResult) -> None:
        sql = result.sql
        assert sql is not None
        ts = sql.get_timeseries("Site Outdoor Air Drybulb Temperature")
        assert len(ts.values) == 1
        assert ts.values[0] == -5.0


class TestVariablesProperty:
    """Tests for SimulationResult.variables."""

    def test_returns_index(self, result: SimulationResult) -> None:
        variables = result.variables
        assert isinstance(variables, OutputVariableIndex)

    def test_is_cached(self, result: SimulationResult) -> None:
        v1 = result.variables
        v2 = result.variables
        assert v1 is v2

    def test_variables_loaded(self, result: SimulationResult) -> None:
        variables = result.variables
        assert variables is not None
        assert len(variables.variables) == 7
        assert len(variables.meters) == 5

    def test_none_when_no_file(self, tmp_path: Path) -> None:
        r = SimulationResult(
            run_dir=tmp_path,
            success=True,
            exit_code=0,
            stdout="",
            stderr="",
            runtime_seconds=0.0,
        )
        assert r.variables is None


class TestCsvProperty:
    """Tests for SimulationResult.csv."""

    def test_returns_csv_result(self, result: SimulationResult) -> None:
        csv = result.csv
        assert isinstance(csv, CSVResult)

    def test_is_cached(self, result: SimulationResult) -> None:
        c1 = result.csv
        c2 = result.csv
        assert c1 is c2

    def test_columns_loaded(self, result: SimulationResult) -> None:
        csv = result.csv
        assert csv is not None
        assert len(csv.columns) == 2

    def test_none_when_no_file(self, tmp_path: Path) -> None:
        r = SimulationResult(
            run_dir=tmp_path,
            success=True,
            exit_code=0,
            stdout="",
            stderr="",
            runtime_seconds=0.0,
        )
        assert r.csv is None


class TestFromDirectory:
    """Tests for SimulationResult.from_directory()."""

    def test_lazy_properties_work(self, result_dir: Path) -> None:
        result = SimulationResult.from_directory(result_dir)
        assert result.sql is not None
        assert result.variables is not None
        assert result.csv is not None


# ---------------------------------------------------------------------------
# FileSystem integration tests
# ---------------------------------------------------------------------------


def _populate_memory_fs(fs: InMemoryFileSystem, run_dir: str, tmp_path: Path) -> None:
    """Load fixture files into an InMemoryFileSystem."""
    fixtures = Path(__file__).parent / "fixtures" / "simulation"
    for name, fixture_name in [
        ("eplusout.rdd", "sample.rdd"),
        ("eplusout.mdd", "sample.mdd"),
        ("eplusout.csv", "sample.csv"),
        ("eplusout.err", "sample.err"),
    ]:
        data = (fixtures / fixture_name).read_bytes()
        fs.write_bytes(f"{run_dir}/{name}", data)

    # SQL needs a real local file — write it to the fs as raw bytes
    sql_path = tmp_path / "temp.sql"
    _create_minimal_sql(sql_path)
    fs.write_bytes(f"{run_dir}/{name}", sql_path.read_bytes())
    fs.write_bytes(f"{run_dir}/eplusout.sql", sql_path.read_bytes())


class TestFsIntegration:
    """Tests for SimulationResult with an InMemoryFileSystem backend."""

    @pytest.fixture
    def mem_fs(self, tmp_path: Path) -> tuple[InMemoryFileSystem, str]:
        fs = InMemoryFileSystem()
        run_dir = "output/sim1"
        _populate_memory_fs(fs, run_dir, tmp_path)
        return fs, run_dir

    def test_from_directory_with_fs(self, mem_fs: tuple[InMemoryFileSystem, str]) -> None:
        fs, run_dir = mem_fs
        result = SimulationResult.from_directory(run_dir, fs=fs)
        assert result.fs is fs
        assert result.run_dir == Path(run_dir)

    def test_errors_via_fs(self, mem_fs: tuple[InMemoryFileSystem, str]) -> None:
        fs, run_dir = mem_fs
        result = SimulationResult.from_directory(run_dir, fs=fs)
        report = result.errors
        assert report is not None
        # The sample.err fixture should parse without errors
        assert report.raw_text != ""

    def test_csv_via_fs(self, mem_fs: tuple[InMemoryFileSystem, str]) -> None:
        fs, run_dir = mem_fs
        result = SimulationResult.from_directory(run_dir, fs=fs)
        csv = result.csv
        assert csv is not None
        assert isinstance(csv, CSVResult)
        assert len(csv.columns) == 2

    def test_variables_via_fs(self, mem_fs: tuple[InMemoryFileSystem, str]) -> None:
        fs, run_dir = mem_fs
        result = SimulationResult.from_directory(run_dir, fs=fs)
        variables = result.variables
        assert variables is not None
        assert isinstance(variables, OutputVariableIndex)
        assert len(variables.variables) == 7
        assert len(variables.meters) == 5

    def test_sql_via_fs_downloads_to_temp(self, mem_fs: tuple[InMemoryFileSystem, str]) -> None:
        fs, run_dir = mem_fs
        result = SimulationResult.from_directory(run_dir, fs=fs)
        sql = result.sql
        assert sql is not None
        assert isinstance(sql, SQLResult)
        ts = sql.get_timeseries("Site Outdoor Air Drybulb Temperature")
        assert len(ts.values) == 1
        assert ts.values[0] == -5.0

    def test_find_output_file_via_fs(self, mem_fs: tuple[InMemoryFileSystem, str]) -> None:
        fs, run_dir = mem_fs
        result = SimulationResult.from_directory(run_dir, fs=fs)
        assert result.err_path is not None
        assert result.csv_path is not None
        assert result.rdd_path is not None
        assert result.mdd_path is not None
        assert result.sql_path is not None

    def test_find_output_file_via_fs_none_when_missing(self) -> None:
        fs = InMemoryFileSystem()
        result = SimulationResult.from_directory("empty/dir", fs=fs)
        assert result.err_path is None
        assert result.csv_path is None
