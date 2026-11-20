"""Tests for SimulationResult lazy properties."""

from __future__ import annotations

import pickle
import shutil
import sqlite3
from pathlib import Path

import pytest
from conftest import InMemoryAsyncFileSystem, InMemoryFileSystem

from idfkit.exceptions import OutputNotFoundError, SimulationError
from idfkit.simulation.outputs import OutputVariableIndex
from idfkit.simulation.parsers.csv import CSVResult
from idfkit.simulation.parsers.html import HTMLResult
from idfkit.simulation.parsers.sql import SQLResult
from idfkit.simulation.result import SimulationResult

FIXTURES = Path(__file__).parent / "fixtures" / "simulation"

_FIXTURE_FILES: list[tuple[str, str]] = [
    ("eplusout.rdd", "sample.rdd"),
    ("eplusout.mdd", "sample.mdd"),
    ("eplusout.csv", "sample.csv"),
    ("eplusout.err", "sample.err"),
]


def _make_result(run_dir: Path) -> SimulationResult:
    """Create a minimal SimulationResult pointing at run_dir with no I/O backends."""
    return SimulationResult(
        run_dir=run_dir,
        success=True,
        exit_code=0,
        stdout="",
        stderr="",
        runtime_seconds=0.0,
    )


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

    def test_raises_when_no_file(self, tmp_path: Path) -> None:
        with pytest.raises(OutputNotFoundError):
            _ = _make_result(tmp_path).sql

    def test_can_query(self, result: SimulationResult) -> None:
        sql = result.sql
        ts = sql.get_timeseries("Site Outdoor Air Drybulb Temperature")
        assert len(ts.values) == 1
        assert ts.values[0] == -5.0


class TestClose:
    """Tests for SimulationResult.close() / context manager releasing handles."""

    def test_close_releases_sql_connection_and_allows_rmtree(self, result_dir: Path) -> None:
        # Reproduces the Windows WinError 32 scenario: an open SQLite
        # connection must not keep the run directory locked after close().
        result = SimulationResult(
            run_dir=result_dir, success=True, exit_code=0, stdout="", stderr="", runtime_seconds=0.0
        )
        sql = result.sql
        _ = sql.get_timeseries("Site Outdoor Air Drybulb Temperature")  # force a real read

        result.close()

        # Connection is closed; querying it now raises.
        with pytest.raises(sqlite3.ProgrammingError):
            sql.get_timeseries("Site Outdoor Air Drybulb Temperature")

        # With the handle released, the directory can be removed (the failing
        # operation on Windows pre-fix).
        shutil.rmtree(result_dir)
        assert not result_dir.exists()

    def test_close_is_idempotent(self, result: SimulationResult) -> None:
        _ = result.sql  # open the connection
        result.close()
        result.close()  # must not raise

    def test_close_with_no_sql_accessed(self, tmp_path: Path) -> None:
        # close() before .sql was ever touched is a no-op.
        _make_result(tmp_path).close()

    def test_context_manager_closes_sql(self, result_dir: Path) -> None:
        with SimulationResult(
            run_dir=result_dir, success=True, exit_code=0, stdout="", stderr="", runtime_seconds=0.0
        ) as result:
            sql = result.sql
        with pytest.raises(sqlite3.ProgrammingError):
            sql.get_timeseries("Site Outdoor Air Drybulb Temperature")

    def test_sql_reopens_after_close(self, result: SimulationResult) -> None:
        first = result.sql
        result.close()
        second = result.sql
        assert second is not first  # a fresh connection

    def test_sqlresult_del_closes_connection(self, result_dir: Path) -> None:
        sql = SQLResult(result_dir / "eplusout.sql")
        assert not sql._closed
        sql.__del__()
        assert sql._closed


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
        assert len(variables.variables) == 7
        assert len(variables.meters) == 5

    def test_raises_when_no_file(self, tmp_path: Path) -> None:
        with pytest.raises(OutputNotFoundError):
            _ = _make_result(tmp_path).variables


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
        assert len(csv.columns) == 2

    def test_raises_when_no_file(self, tmp_path: Path) -> None:
        with pytest.raises(OutputNotFoundError):
            _ = _make_result(tmp_path).csv


class TestFromDirectory:
    """Tests for SimulationResult.from_directory()."""

    def test_lazy_properties_work(self, result_dir: Path) -> None:
        result = SimulationResult.from_directory(result_dir)
        assert isinstance(result.sql, SQLResult)
        assert isinstance(result.variables, OutputVariableIndex)
        assert isinstance(result.csv, CSVResult)


# ---------------------------------------------------------------------------
# FileSystem integration tests
# ---------------------------------------------------------------------------


def _populate_memory_fs(fs: InMemoryFileSystem, run_dir: str, tmp_path: Path) -> None:
    """Load fixture files into an InMemoryFileSystem."""
    for name, fixture_name in _FIXTURE_FILES:
        fs.write_bytes(f"{run_dir}/{name}", (FIXTURES / fixture_name).read_bytes())

    sql_path = tmp_path / "temp.sql"
    _create_minimal_sql(sql_path)
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
        assert isinstance(csv, CSVResult)
        assert len(csv.columns) == 2

    def test_variables_via_fs(self, mem_fs: tuple[InMemoryFileSystem, str]) -> None:
        fs, run_dir = mem_fs
        result = SimulationResult.from_directory(run_dir, fs=fs)
        variables = result.variables
        assert isinstance(variables, OutputVariableIndex)
        assert len(variables.variables) == 7
        assert len(variables.meters) == 5

    def test_sql_via_fs_downloads_to_temp(self, mem_fs: tuple[InMemoryFileSystem, str]) -> None:
        fs, run_dir = mem_fs
        result = SimulationResult.from_directory(run_dir, fs=fs)
        sql = result.sql
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


# ---------------------------------------------------------------------------
# Basic edge cases
# ---------------------------------------------------------------------------


class TestBasicEdgeCases:
    """Tests for validation, path properties, and error branches."""

    def test_post_init_raises_when_both_fs_provided(self, tmp_path: Path) -> None:
        fs = InMemoryFileSystem()
        async_fs = InMemoryAsyncFileSystem()
        with pytest.raises(ValueError, match="mutually exclusive"):
            SimulationResult(
                run_dir=tmp_path,
                success=True,
                exit_code=0,
                stdout="",
                stderr="",
                runtime_seconds=0.0,
                fs=fs,
                async_fs=async_fs,
            )

    def test_errors_returns_empty_when_no_err_file(self, tmp_path: Path) -> None:
        assert _make_result(tmp_path).errors.raw_text == ""

    def test_errors_from_local_file(self, result_dir: Path) -> None:
        assert _make_result(result_dir).errors.raw_text != ""

    def test_eso_path_none_when_missing(self, tmp_path: Path) -> None:
        assert _make_result(tmp_path).eso_path is None

    def test_eso_path_when_present(self, tmp_path: Path) -> None:
        (tmp_path / "eplusout.eso").write_text("eso content")
        assert _make_result(tmp_path).eso_path is not None

    def test_html_path_none_when_missing(self, tmp_path: Path) -> None:
        assert _make_result(tmp_path).html_path is None

    def test_html_path_with_htm_extension(self, tmp_path: Path) -> None:
        (tmp_path / "eplusout.htm").write_text("<html></html>")
        assert _make_result(tmp_path).html_path is not None

    def test_html_path_with_html_extension(self, tmp_path: Path) -> None:
        (tmp_path / "eplusout.html").write_text("<html></html>")
        assert _make_result(tmp_path).html_path is not None

    def test_find_output_file_glob_fallback(self, tmp_path: Path) -> None:
        """When primary name not found, scan directory for any matching file."""
        (tmp_path / "othernameout.err").write_text("err content")
        assert _make_result(tmp_path).err_path is not None

    def test_find_output_file_raises_for_async_fs_only(self, tmp_path: Path) -> None:
        result = SimulationResult(
            run_dir=tmp_path,
            success=True,
            exit_code=0,
            stdout="",
            stderr="",
            runtime_seconds=0.0,
            async_fs=InMemoryAsyncFileSystem(),
        )
        with pytest.raises(RuntimeError, match="AsyncFileSystem"):
            _ = result.err_path

    def test_errors_is_cached(self, result_dir: Path) -> None:
        result = _make_result(result_dir)
        e1 = result.errors
        e2 = result.errors
        assert e1 is e2

    def test_find_output_file_fs_glob_fallback(self) -> None:
        """When primary name not found in fs, glob fallback returns a match."""
        fs = InMemoryFileSystem()
        run_dir = "output/glob_fallback"
        fs.write_bytes(f"{run_dir}/othernameout.err", b"err content")
        result = SimulationResult.from_directory(run_dir, fs=fs)
        assert result.err_path is not None


# ---------------------------------------------------------------------------
# HTML property tests
# ---------------------------------------------------------------------------

_MINIMAL_HTML = """\
<html><body>
<p><b>Report: AnnualBuildingUtilityPerformanceSummary</b></p>
<p>For: Entire Facility</p>
<b>Site and Source Energy</b>
<table>
<tr><th>Category</th><th>Value</th></tr>
<tr><td>Total</td><td>100</td></tr>
</table>
</body></html>
"""


class TestHtmlProperty:
    """Tests for SimulationResult.html."""

    def test_raises_when_no_file(self, tmp_path: Path) -> None:
        with pytest.raises(OutputNotFoundError):
            _ = _make_result(tmp_path).html

    def test_missing_file_is_not_cached(self, tmp_path: Path) -> None:
        result = _make_result(tmp_path)
        with pytest.raises(OutputNotFoundError):
            _ = result.html
        (tmp_path / "eplusout.htm").write_text(_MINIMAL_HTML, encoding="latin-1")
        assert isinstance(result.html, HTMLResult)

    def test_returns_html_result_from_file(self, tmp_path: Path) -> None:
        (tmp_path / "eplusout.htm").write_text(_MINIMAL_HTML, encoding="latin-1")
        assert isinstance(_make_result(tmp_path).html, HTMLResult)

    def test_is_cached(self, tmp_path: Path) -> None:
        (tmp_path / "eplusout.htm").write_text(_MINIMAL_HTML, encoding="latin-1")
        result = _make_result(tmp_path)
        h1 = result.html
        h2 = result.html
        assert h1 is h2

    def test_html_via_fs(self, tmp_path: Path) -> None:
        fs = InMemoryFileSystem()
        run_dir = "output/sim_html"
        fs.write_text(f"{run_dir}/eplusout.htm", _MINIMAL_HTML, encoding="latin-1")
        result = SimulationResult.from_directory(run_dir, fs=fs)
        html = result.html
        assert isinstance(html, HTMLResult)


# ---------------------------------------------------------------------------
# Async accessor tests
# ---------------------------------------------------------------------------


def _populate_async_fs(async_fs: InMemoryAsyncFileSystem, run_dir: str, sql_path: Path) -> None:
    """Load fixture files directly into an InMemoryAsyncFileSystem's backing store."""
    files = async_fs._files  # pyright: ignore[reportPrivateUsage]
    norm = async_fs._norm  # pyright: ignore[reportPrivateUsage]
    for name, fixture_name in _FIXTURE_FILES:
        files[norm(f"{run_dir}/{name}")] = (FIXTURES / fixture_name).read_bytes()
    files[norm(f"{run_dir}/eplusout.sql")] = sql_path.read_bytes()
    files[norm(f"{run_dir}/eplusout.htm")] = _MINIMAL_HTML.encode("latin-1")


@pytest.mark.asyncio
class TestAsyncAccessors:
    """Tests for async methods on SimulationResult."""

    @pytest.fixture
    def async_fs_setup(self, tmp_path: Path) -> tuple[InMemoryAsyncFileSystem, str]:
        sql_path = tmp_path / "temp.sql"
        _create_minimal_sql(sql_path)
        async_fs = InMemoryAsyncFileSystem()
        run_dir = "output/async_sim"
        _populate_async_fs(async_fs, run_dir, sql_path)
        return async_fs, run_dir

    async def test_async_errors_no_file(self, tmp_path: Path) -> None:
        report = await _make_result(tmp_path).async_errors()
        assert report.raw_text == ""

    async def test_async_errors_cached(self, tmp_path: Path) -> None:
        result = _make_result(tmp_path)
        r1 = await result.async_errors()
        r2 = await result.async_errors()
        assert r1 is r2

    async def test_async_errors_with_async_fs(self, async_fs_setup: tuple[InMemoryAsyncFileSystem, str]) -> None:
        async_fs, run_dir = async_fs_setup
        result = SimulationResult.from_directory(run_dir, async_fs=async_fs)
        report = await result.async_errors()
        assert report.raw_text != ""

    async def test_async_errors_with_sync_fs(self, tmp_path: Path) -> None:
        fs = InMemoryFileSystem()
        run_dir = "output/sync_fallback"
        data = (FIXTURES / "sample.err").read_bytes()
        fs.write_bytes(f"{run_dir}/eplusout.err", data)
        result = SimulationResult.from_directory(run_dir, fs=fs)
        report = await result.async_errors()
        assert report.raw_text != ""

    async def test_async_errors_local_file(self, result_dir: Path) -> None:
        report = await _make_result(result_dir).async_errors()
        assert report.raw_text != ""

    async def test_async_sql_raises_when_no_file(self, tmp_path: Path) -> None:
        with pytest.raises(OutputNotFoundError):
            await _make_result(tmp_path).async_sql()

    async def test_async_sql_with_async_fs(self, async_fs_setup: tuple[InMemoryAsyncFileSystem, str]) -> None:
        async_fs, run_dir = async_fs_setup
        result = SimulationResult.from_directory(run_dir, async_fs=async_fs)
        sql = await result.async_sql()
        assert isinstance(sql, SQLResult)

    async def test_async_sql_with_sync_fs(self, tmp_path: Path) -> None:
        fs = InMemoryFileSystem()
        run_dir = "output/sync_sql"
        sql_path = tmp_path / "temp.sql"
        _create_minimal_sql(sql_path)
        fs.write_bytes(f"{run_dir}/eplusout.sql", sql_path.read_bytes())
        result = SimulationResult.from_directory(run_dir, fs=fs)
        sql = await result.async_sql()
        assert isinstance(sql, SQLResult)

    async def test_async_sql_local_file(self, result_dir: Path) -> None:
        assert isinstance(await _make_result(result_dir).async_sql(), SQLResult)

    async def test_async_variables_raises_when_no_file(self, tmp_path: Path) -> None:
        with pytest.raises(OutputNotFoundError):
            await _make_result(tmp_path).async_variables()

    async def test_async_variables_with_async_fs(self, async_fs_setup: tuple[InMemoryAsyncFileSystem, str]) -> None:
        async_fs, run_dir = async_fs_setup
        result = SimulationResult.from_directory(run_dir, async_fs=async_fs)
        variables = await result.async_variables()
        assert isinstance(variables, OutputVariableIndex)
        assert len(variables.variables) == 7

    async def test_async_variables_with_sync_fs(self, tmp_path: Path) -> None:
        fs = InMemoryFileSystem()
        run_dir = "output/sync_vars"
        fs.write_bytes(f"{run_dir}/eplusout.rdd", (FIXTURES / "sample.rdd").read_bytes())
        fs.write_bytes(f"{run_dir}/eplusout.mdd", (FIXTURES / "sample.mdd").read_bytes())
        result = SimulationResult.from_directory(run_dir, fs=fs)
        variables = await result.async_variables()
        assert isinstance(variables, OutputVariableIndex)

    async def test_async_variables_local_file(self, result_dir: Path) -> None:
        assert isinstance(await _make_result(result_dir).async_variables(), OutputVariableIndex)

    async def test_async_csv_raises_when_no_file(self, tmp_path: Path) -> None:
        with pytest.raises(OutputNotFoundError):
            await _make_result(tmp_path).async_csv()

    async def test_async_csv_with_async_fs(self, async_fs_setup: tuple[InMemoryAsyncFileSystem, str]) -> None:
        async_fs, run_dir = async_fs_setup
        result = SimulationResult.from_directory(run_dir, async_fs=async_fs)
        csv = await result.async_csv()
        assert isinstance(csv, CSVResult)

    async def test_async_csv_with_sync_fs(self, tmp_path: Path) -> None:
        fs = InMemoryFileSystem()
        run_dir = "output/sync_csv"
        fs.write_bytes(f"{run_dir}/eplusout.csv", (FIXTURES / "sample.csv").read_bytes())
        result = SimulationResult.from_directory(run_dir, fs=fs)
        csv = await result.async_csv()
        assert isinstance(csv, CSVResult)

    async def test_async_csv_local_file(self, result_dir: Path) -> None:
        assert isinstance(await _make_result(result_dir).async_csv(), CSVResult)

    async def test_async_html_raises_when_no_file(self, tmp_path: Path) -> None:
        with pytest.raises(OutputNotFoundError):
            await _make_result(tmp_path).async_html()

    async def test_async_html_with_async_fs(self, async_fs_setup: tuple[InMemoryAsyncFileSystem, str]) -> None:
        async_fs, run_dir = async_fs_setup
        result = SimulationResult.from_directory(run_dir, async_fs=async_fs)
        html = await result.async_html()
        assert isinstance(html, HTMLResult)

    async def test_async_html_with_sync_fs(self, tmp_path: Path) -> None:
        fs = InMemoryFileSystem()
        run_dir = "output/sync_html"
        fs.write_text(f"{run_dir}/eplusout.htm", _MINIMAL_HTML, encoding="latin-1")
        result = SimulationResult.from_directory(run_dir, fs=fs)
        html = await result.async_html()
        assert isinstance(html, HTMLResult)

    async def test_async_html_local_file(self, tmp_path: Path) -> None:
        (tmp_path / "eplusout.htm").write_text(_MINIMAL_HTML, encoding="latin-1")
        assert isinstance(await _make_result(tmp_path).async_html(), HTMLResult)

    async def test_async_find_output_file_async_fs_primary(
        self, async_fs_setup: tuple[InMemoryAsyncFileSystem, str]
    ) -> None:
        async_fs, run_dir = async_fs_setup
        result = SimulationResult.from_directory(run_dir, async_fs=async_fs)
        path = await result._async_find_output_file(".err")  # pyright: ignore[reportPrivateUsage]
        assert path is not None

    async def test_async_find_output_file_async_fs_glob_fallback(self, tmp_path: Path) -> None:
        async_fs = InMemoryAsyncFileSystem()
        run_dir = "output/glob_async"
        async_fs._files[async_fs._norm(f"{run_dir}/othernameout.err")] = b"err"  # pyright: ignore[reportPrivateUsage]
        result = SimulationResult.from_directory(run_dir, async_fs=async_fs)
        path = await result._async_find_output_file(".err")  # pyright: ignore[reportPrivateUsage]
        assert path is not None

    async def test_async_find_output_file_async_fs_none(self) -> None:
        async_fs = InMemoryAsyncFileSystem()
        result = SimulationResult.from_directory("empty/async", async_fs=async_fs)
        path = await result._async_find_output_file(".err")  # pyright: ignore[reportPrivateUsage]
        assert path is None

    async def test_async_find_output_file_sync_fs_fallback(self, tmp_path: Path) -> None:
        fs = InMemoryFileSystem()
        run_dir = "output/sync_find"
        fs.write_bytes(f"{run_dir}/eplusout.err", b"err")
        result = SimulationResult.from_directory(run_dir, fs=fs)
        path = await result._async_find_output_file(".err")  # pyright: ignore[reportPrivateUsage]
        assert path is not None

    async def test_async_find_output_file_sync_fs_glob_fallback(self, tmp_path: Path) -> None:
        fs = InMemoryFileSystem()
        run_dir = "output/sync_glob"
        fs.write_bytes(f"{run_dir}/othernameout.err", b"err")
        result = SimulationResult.from_directory(run_dir, fs=fs)
        path = await result._async_find_output_file(".err")  # pyright: ignore[reportPrivateUsage]
        assert path is not None

    async def test_async_find_output_file_sync_fs_none(self) -> None:
        fs = InMemoryFileSystem()
        result = SimulationResult.from_directory("empty/sync", fs=fs)
        path = await result._async_find_output_file(".err")  # pyright: ignore[reportPrivateUsage]
        assert path is None

    async def test_async_find_output_file_local_primary(self, tmp_path: Path) -> None:
        (tmp_path / "eplusout.err").write_text("err content")
        path = await _make_result(tmp_path)._async_find_output_file(".err")  # pyright: ignore[reportPrivateUsage]
        assert path is not None

    async def test_async_find_output_file_local_scan_fallback(self, tmp_path: Path) -> None:
        (tmp_path / "othernameout.err").write_text("err content")
        path = await _make_result(tmp_path)._async_find_output_file(".err")  # pyright: ignore[reportPrivateUsage]
        assert path is not None

    async def test_async_find_output_file_local_none(self, tmp_path: Path) -> None:
        path = await _make_result(tmp_path)._async_find_output_file(".err")  # pyright: ignore[reportPrivateUsage]
        assert path is None


# ---------------------------------------------------------------------------
# Output file naming: every --output-suffix style, auxiliary files skipped
# ---------------------------------------------------------------------------

#: The files each ``--output-suffix`` style writes with ``-p eplus`` and
#: ``Output:SQLite``, as observed from EnergyPlus 26.1. The auxiliary file is
#: listed first so a lookup that trusts listing order picks it.
_STYLE_FILES: dict[str, tuple[str, ...]] = {
    "C": ("eplusSqlite.err", "eplus.err", "eplusMeter.csv", "eplusTable.csv", "eplus.csv", "eplusTable.htm"),
    "L": ("sqlite.err", "eplusout.err", "eplusmtr.csv", "eplustbl.csv", "eplusout.csv", "eplustbl.htm"),
    "D": ("eplus-sqlite.err", "eplus.err", "eplus-meter.csv", "eplus-table.csv", "eplus.csv", "eplus-table.htm"),
}
_STYLE_EXPECTED: dict[str, tuple[str, str, str]] = {
    "C": ("eplus.err", "eplus.csv", "eplusTable.htm"),
    "L": ("eplusout.err", "eplusout.csv", "eplustbl.htm"),
    "D": ("eplus.err", "eplus.csv", "eplus-table.htm"),
}
_SEVERE_ERR = "   ** Severe  ** Weather file days requested without a weather file\n"


class TestOutputFileNaming:
    """The lookup finds the main output whatever the naming style and listing order."""

    @pytest.mark.parametrize("style", sorted(_STYLE_FILES))
    def test_local_run_dir(self, tmp_path: Path, style: str) -> None:
        for name in _STYLE_FILES[style]:
            (tmp_path / name).write_text(_SEVERE_ERR if name in _STYLE_EXPECTED[style] else "aux")
        result = _make_result(tmp_path)
        err, csv, htm = _STYLE_EXPECTED[style]
        assert result.err_path == tmp_path / err
        assert result.csv_path == tmp_path / csv
        assert result.html_path == tmp_path / htm

    @pytest.mark.parametrize("style", sorted(_STYLE_FILES))
    def test_sync_fs(self, style: str) -> None:
        fs = InMemoryFileSystem()
        run_dir = f"output/style_{style}"
        for name in _STYLE_FILES[style]:
            fs.write_text(f"{run_dir}/{name}", "x")
        result = SimulationResult.from_directory(run_dir, fs=fs)
        err, csv, htm = _STYLE_EXPECTED[style]
        assert result.err_path == Path(run_dir) / err
        assert result.csv_path == Path(run_dir) / csv
        assert result.html_path == Path(run_dir) / htm

    @pytest.mark.asyncio
    @pytest.mark.parametrize("style", sorted(_STYLE_FILES))
    async def test_async_fs(self, style: str) -> None:
        async_fs = InMemoryAsyncFileSystem()
        run_dir = f"output/async_style_{style}"
        for name in _STYLE_FILES[style]:
            await async_fs.write_text(f"{run_dir}/{name}", "x")
        result = SimulationResult.from_directory(run_dir, async_fs=async_fs)
        err, csv, htm = _STYLE_EXPECTED[style]
        assert await result._async_find_output_file(".err") == Path(run_dir) / err  # pyright: ignore[reportPrivateUsage]
        assert await result._async_find_output_file(".csv") == Path(run_dir) / csv  # pyright: ignore[reportPrivateUsage]
        assert await result._async_find_output_file(".htm", table=True) == Path(run_dir) / htm  # pyright: ignore[reportPrivateUsage]

    def test_errors_read_from_eplus_err_not_sqlite_err(self, tmp_path: Path) -> None:
        """The reported bug: ``eplusSqlite.err`` beside ``eplus.err`` hid the severe errors."""
        (tmp_path / "eplusSqlite.err").write_text("SQLite logging only\n")
        (tmp_path / "eplus.err").write_text(_SEVERE_ERR)
        assert len(_make_result(tmp_path).errors.severe) == 1

    @pytest.mark.asyncio
    async def test_async_errors_read_from_eplus_err_not_sqlite_err(self) -> None:
        async_fs = InMemoryAsyncFileSystem()
        run_dir = "output/async_sqlite"
        await async_fs.write_text(f"{run_dir}/eplusSqlite.err", "SQLite logging only\n")
        await async_fs.write_text(f"{run_dir}/eplus.err", _SEVERE_ERR)
        result = SimulationResult.from_directory(run_dir, async_fs=async_fs)
        assert len((await result.async_errors()).severe) == 1

    def test_custom_prefix(self, tmp_path: Path) -> None:
        (tmp_path / "fooSqlite.err").write_text("aux")
        (tmp_path / "foo.err").write_text(_SEVERE_ERR)
        result = SimulationResult.from_directory(tmp_path, output_prefix="foo")
        assert result.err_path == tmp_path / "foo.err"

    def test_fallback_skips_auxiliary_when_prefix_differs(self, tmp_path: Path) -> None:
        """With an unexpected prefix the scan still never returns the SQLite log."""
        (tmp_path / "runSqlite.err").write_text("aux")
        (tmp_path / "run.err").write_text(_SEVERE_ERR)
        assert _make_result(tmp_path).err_path == tmp_path / "run.err"

    def test_fallback_returns_none_when_only_auxiliary(self, tmp_path: Path) -> None:
        (tmp_path / "eplusSqlite.err").write_text("aux")
        assert _make_result(tmp_path).err_path is None

    def test_fallback_is_sorted(self, tmp_path: Path) -> None:
        (tmp_path / "zeta.err").write_text("z")
        (tmp_path / "alpha.err").write_text("a")
        assert _make_result(tmp_path).err_path == tmp_path / "alpha.err"

    def test_fs_fallback_is_sorted_and_skips_auxiliary(self) -> None:
        fs = InMemoryFileSystem()
        run_dir = "output/fs_fallback"
        for name in ("zeta.err", "aSqlite.err", "alpha.err"):
            fs.write_text(f"{run_dir}/{name}", "x")
        result = SimulationResult.from_directory(run_dir, fs=fs)
        assert result.err_path == Path(run_dir) / "alpha.err"

    def test_pick_fallback_ignores_listing_order(self) -> None:
        from idfkit.simulation.result import _pick_fallback  # pyright: ignore[reportPrivateUsage]

        names = ["eplusSqlite.err", "b.err", "a.err"]
        assert _pick_fallback(names, ".err", table=False) == Path("a.err")
        assert _pick_fallback(list(reversed(names)), ".err", table=False) == Path("a.err")

    def test_html_fallback_prefers_table_file(self, tmp_path: Path) -> None:
        (tmp_path / "other.htm").write_text("<html></html>")
        (tmp_path / "runTable.htm").write_text("<html></html>")
        assert _make_result(tmp_path).html_path == tmp_path / "runTable.htm"

    def test_default_style_report_wins_over_a_stale_legacy_one(self, tmp_path: Path) -> None:
        """A reused output directory may hold a legacy-style report from an earlier ``-s L`` run."""
        for name in ("eplustbl.htm", "eplusTable.htm"):
            (tmp_path / name).write_text("<html></html>")
        result = SimulationResult.from_directory(tmp_path)
        assert result.html_path == tmp_path / "eplusTable.htm"

    @pytest.mark.parametrize("style", sorted(_STYLE_FILES))
    def test_known_style_wins_over_stale_outputs_of_another(self, tmp_path: Path, style: str) -> None:
        """A run of a known style finds its own outputs, whatever another style left in the directory."""
        for files in _STYLE_FILES.values():
            for name in files:
                (tmp_path / name).write_text("x")
        result = SimulationResult.from_directory(tmp_path, output_suffix=style)  # type: ignore[arg-type]
        err, csv, htm = _STYLE_EXPECTED[style]
        assert result.err_path == tmp_path / err
        assert result.csv_path == tmp_path / csv
        assert result.html_path == tmp_path / htm

    def test_fallback_skips_perflog(self, tmp_path: Path) -> None:
        (tmp_path / "eplus_perflog.csv").write_text("x")
        assert _make_result(tmp_path).csv_path is None

    def test_missing_local_run_dir_raises(self, tmp_path: Path) -> None:
        """A run directory that does not exist is an error, not an empty result."""
        with pytest.raises(FileNotFoundError):
            _ = _make_result(tmp_path / "missing").err_path

    def test_html_fallback_prefers_table_over_other_auxiliary(self, tmp_path: Path) -> None:
        (tmp_path / "runMeter.htm").write_text("<html></html>")
        (tmp_path / "runtbl.htm").write_text("<html></html>")
        assert _make_result(tmp_path).html_path == tmp_path / "runtbl.htm"


def _failed_result(run_dir: Path, *, stderr: str = "") -> SimulationResult:
    return SimulationResult(
        run_dir=run_dir, success=False, exit_code=1, stdout="lots of output", stderr=stderr, runtime_seconds=0.1
    )


class TestRaiseForStatus:
    """``raise_for_status()`` fails fast on a failed run and names its cause."""

    def test_success_returns_self(self, tmp_path: Path) -> None:
        result = _make_result(tmp_path)
        assert result.raise_for_status() is result

    def test_failure_quotes_fatal_and_severe(self, tmp_path: Path) -> None:
        shutil.copy(FIXTURES / "sample_fatal.err", tmp_path / "eplus.err")
        result = _failed_result(tmp_path)
        with pytest.raises(SimulationError) as excinfo:
            result.raise_for_status()
        text = str(excinfo.value)
        assert text.startswith("EnergyPlus simulation failed (exit code 1)\n")
        assert "Fatal: GetSurfaceData: Errors too severe, program terminates." in text
        assert "Surface WALL-1SOUTH has 0 vertices" in text
        assert str(tmp_path / "eplus.err") in text
        assert excinfo.value.exit_code == 1
        assert excinfo.value.result is result

    def test_failure_without_err_reports_stderr(self, tmp_path: Path) -> None:
        result = _failed_result(tmp_path, stderr="weather file not found")
        with pytest.raises(SimulationError, match="weather file not found"):
            result.raise_for_status()

    @pytest.mark.asyncio
    async def test_async_failure(self, tmp_path: Path) -> None:
        shutil.copy(FIXTURES / "sample_fatal.err", tmp_path / "eplus.err")
        result = _failed_result(tmp_path)
        with pytest.raises(SimulationError, match="Errors too severe"):
            await result.async_raise_for_status()

    @pytest.mark.asyncio
    async def test_async_success_returns_self(self, tmp_path: Path) -> None:
        result = _make_result(tmp_path)
        assert await result.async_raise_for_status() is result

    @pytest.mark.asyncio
    async def test_async_failure_through_async_fs(self) -> None:
        async_fs = InMemoryAsyncFileSystem()
        run_dir = Path("output/async_fail")
        await async_fs.write_bytes(run_dir / "eplus.err", (FIXTURES / "sample_fatal.err").read_bytes())
        result = SimulationResult(
            run_dir=run_dir, success=False, exit_code=1, stdout="", stderr="", runtime_seconds=0.1, async_fs=async_fs
        )
        with pytest.raises(SimulationError) as excinfo:
            await result.async_raise_for_status()
        text = str(excinfo.value)
        assert "Fatal: GetSurfaceData: Errors too severe, program terminates." in text
        assert f"Full error report: {run_dir / 'eplus.err'}" in text
        assert excinfo.value.result is result

    def test_sync_raise_on_async_fs_result(self) -> None:
        result = SimulationResult(
            run_dir=Path("output/async_fail"),
            success=False,
            exit_code=1,
            stdout="",
            stderr="",
            runtime_seconds=0.1,
            async_fs=InMemoryAsyncFileSystem(),
        )
        with pytest.raises(RuntimeError, match="async"):
            result.raise_for_status()

    def test_repr_leaves_out_output_streams(self, tmp_path: Path) -> None:
        assert "lots of output" not in repr(_failed_result(tmp_path))


class TestMissingOutput:
    """A parsed-output accessor raises an actionable ``OutputNotFoundError`` when its file is missing."""

    @pytest.mark.parametrize(
        ("accessor", "remedy", "path_property"),
        [
            ("sql", "Output:SQLite", "sql_path"),
            ("eso", "Output:Variable", "eso_path"),
            ("mtr", "Output:Meter", "mtr_path"),
            ("csv", "readvars=True", "csv_path"),
            ("html", "OutputControl:Table:Style", "html_path"),
            ("variables", "Output:VariableDictionary", "rdd_path"),
        ],
    )
    def test_successful_run_names_output_object(
        self, tmp_path: Path, accessor: str, remedy: str, path_property: str
    ) -> None:
        result = _make_result(tmp_path)
        assert getattr(result, path_property) is None
        with pytest.raises(OutputNotFoundError) as excinfo:
            getattr(result, accessor)
        text = str(excinfo.value)
        assert remedy in text
        assert f"result.{path_property} is None" in text
        assert str(tmp_path) in text
        assert excinfo.value.output == accessor
        assert excinfo.value.run_dir == tmp_path

    @pytest.mark.asyncio
    @pytest.mark.parametrize("accessor", ["sql", "eso", "mtr", "csv", "html", "variables"])
    async def test_async_counterparts_raise_the_same(self, tmp_path: Path, accessor: str) -> None:
        result = _make_result(tmp_path)
        with pytest.raises(OutputNotFoundError) as sync_info:
            getattr(result, accessor)
        with pytest.raises(OutputNotFoundError) as async_info:
            await getattr(result, f"async_{accessor}")()
        assert str(async_info.value) == str(sync_info.value)

    def test_failed_run_points_to_err_file(self, tmp_path: Path) -> None:
        shutil.copy(FIXTURES / "sample_fatal.err", tmp_path / "eplus.err")
        with pytest.raises(OutputNotFoundError) as excinfo:
            _ = _failed_result(tmp_path).sql
        text = str(excinfo.value)
        assert "the simulation failed" in text
        assert "raise_for_status()" in text
        assert str(tmp_path / "eplus.err") in text
        assert "Output:SQLite" not in text

    @pytest.mark.asyncio
    async def test_failed_run_async_with_async_fs(self) -> None:
        async_fs = InMemoryAsyncFileSystem()
        await async_fs.write_text("run/eplus.err", "   ** Fatal  ** boom\n")
        result = SimulationResult(
            run_dir=Path("run"),
            success=False,
            exit_code=1,
            stdout="",
            stderr="",
            runtime_seconds=0.0,
            async_fs=async_fs,
        )
        with pytest.raises(OutputNotFoundError, match="the simulation failed") as excinfo:
            await result.async_sql()
        assert "eplus.err" in str(excinfo.value)

    def test_refused_job_gives_reason(self, tmp_path: Path) -> None:
        result = SimulationResult(
            run_dir=tmp_path,
            success=False,
            exit_code=None,
            stdout="",
            stderr="",
            runtime_seconds=0.0,
            refusal="A weather file is required",
        )
        with pytest.raises(OutputNotFoundError, match="refused before EnergyPlus ran") as excinfo:
            _ = result.csv
        assert "A weather file is required" in str(excinfo.value)

    def test_is_file_not_found_error(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            _ = _make_result(tmp_path).eso

    def test_pickles(self, tmp_path: Path) -> None:
        with pytest.raises(OutputNotFoundError) as excinfo:
            _ = _make_result(tmp_path).mtr
        clone = pickle.loads(pickle.dumps(excinfo.value))  # noqa: S301
        assert isinstance(clone, OutputNotFoundError)
        assert str(clone) == str(excinfo.value)
        assert clone.output == "mtr"
        assert clone.run_dir == tmp_path


class TestCleanup:
    """Tests for SimulationResult.cleanup() and the context managers that call it."""

    def _owned(self, result_dir: Path) -> SimulationResult:
        return SimulationResult(
            run_dir=result_dir,
            success=True,
            exit_code=0,
            stdout="",
            stderr="",
            runtime_seconds=0.0,
            owns_run_dir=True,
        )

    def test_owns_run_dir_defaults_to_false(self, tmp_path: Path) -> None:
        assert _make_result(tmp_path).owns_run_dir is False

    def test_deletes_owned_run_dir(self, result_dir: Path) -> None:
        result = self._owned(result_dir)
        result.cleanup()
        assert not result_dir.exists()

    def test_closes_sql_before_deleting(self, result_dir: Path) -> None:
        result = self._owned(result_dir)
        sql = result.sql
        _ = sql.get_timeseries("Site Outdoor Air Drybulb Temperature")
        result.cleanup()
        assert not result_dir.exists()
        with pytest.raises(sqlite3.ProgrammingError):
            sql.get_timeseries("Site Outdoor Air Drybulb Temperature")

    def test_is_idempotent(self, result_dir: Path) -> None:
        result = self._owned(result_dir)
        result.cleanup()
        result.cleanup()  # must not raise
        assert not result_dir.exists()

    def test_never_deletes_caller_dir(self, result_dir: Path) -> None:
        result = SimulationResult(
            run_dir=result_dir, success=True, exit_code=0, stdout="", stderr="", runtime_seconds=0.0
        )
        _ = result.sql
        result.cleanup()
        assert (result_dir / "eplusout.sql").exists()
        assert result.sql.get_timeseries("Site Outdoor Air Drybulb Temperature").values[0] == -5.0  # reopened

    def test_never_deletes_remote_dir(self) -> None:
        fs = InMemoryFileSystem()
        fs.write_text("remote/run/eplusout.err", "")
        result = SimulationResult(
            run_dir=Path("remote/run"), success=True, exit_code=0, stdout="", stderr="", runtime_seconds=0.0, fs=fs
        )
        result.cleanup()
        assert fs.exists("remote/run/eplusout.err")

    def test_parsed_outputs_survive_cleanup(self, result_dir: Path) -> None:
        result = self._owned(result_dir)
        errors = result.errors
        result.cleanup()
        assert result.errors is errors

    def test_context_manager_deletes_owned_run_dir(self, result_dir: Path) -> None:
        with self._owned(result_dir) as result:
            assert result.csv is not None
        assert not result_dir.exists()

    def test_context_manager_deletes_on_exception(self, result_dir: Path) -> None:
        with pytest.raises(RuntimeError), self._owned(result_dir):
            raise RuntimeError
        assert not result_dir.exists()

    def test_context_manager_keeps_caller_dir(self, result_dir: Path) -> None:
        with _make_result(result_dir):
            pass
        assert (result_dir / "eplusout.err").exists()

    @pytest.mark.asyncio
    async def test_async_cleanup(self, result_dir: Path) -> None:
        result = self._owned(result_dir)
        await result.async_cleanup()
        assert not result_dir.exists()

    @pytest.mark.asyncio
    async def test_async_context_manager(self, result_dir: Path) -> None:
        async with self._owned(result_dir) as result:
            _ = await result.async_errors()
        assert not result_dir.exists()

    @pytest.mark.asyncio
    async def test_async_context_manager_closes_async_sql(self, result_dir: Path) -> None:
        """A connection opened on the event loop thread is closed there, not in the delete's worker thread."""
        async with self._owned(result_dir) as result:
            sql = await result.async_sql()
            _ = sql.get_timeseries("Site Outdoor Air Drybulb Temperature")
        assert not result_dir.exists()
        with pytest.raises(sqlite3.ProgrammingError):
            sql.get_timeseries("Site Outdoor Air Drybulb Temperature")

    @pytest.mark.asyncio
    async def test_async_cleanup_closes_sync_sql(self, result_dir: Path) -> None:
        result = self._owned(result_dir)
        _ = result.sql.get_timeseries("Site Outdoor Air Drybulb Temperature")
        await result.async_cleanup()
        assert not result_dir.exists()

    @pytest.mark.asyncio
    async def test_async_context_manager_keeps_caller_dir(self, result_dir: Path) -> None:
        async with _make_result(result_dir):
            pass
        assert (result_dir / "eplusout.err").exists()
