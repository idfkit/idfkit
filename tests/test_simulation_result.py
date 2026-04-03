"""Tests for SimulationResult lazy properties."""

from __future__ import annotations

import shutil
import sqlite3
from pathlib import Path

import pytest
from conftest import InMemoryAsyncFileSystem, InMemoryFileSystem

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

    def test_none_when_no_file(self, tmp_path: Path) -> None:
        assert _make_result(tmp_path).sql is None

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
        assert _make_result(tmp_path).variables is None


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
        assert _make_result(tmp_path).csv is None


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

    def test_none_when_no_file(self, tmp_path: Path) -> None:
        assert _make_result(tmp_path).html is None

    def test_cached_none(self, tmp_path: Path) -> None:
        result = _make_result(tmp_path)
        h1 = result.html
        h2 = result.html
        assert h1 is h2
        assert h1 is None

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

    async def test_async_sql_none_when_no_file(self, tmp_path: Path) -> None:
        assert await _make_result(tmp_path).async_sql() is None

    async def test_async_sql_cached_none(self, tmp_path: Path) -> None:
        result = _make_result(tmp_path)
        s1 = await result.async_sql()
        s2 = await result.async_sql()
        assert s1 is s2

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

    async def test_async_variables_none_when_no_file(self, tmp_path: Path) -> None:
        assert await _make_result(tmp_path).async_variables() is None

    async def test_async_variables_cached_none(self, tmp_path: Path) -> None:
        result = _make_result(tmp_path)
        v1 = await result.async_variables()
        v2 = await result.async_variables()
        assert v1 is v2

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

    async def test_async_csv_none_when_no_file(self, tmp_path: Path) -> None:
        assert await _make_result(tmp_path).async_csv() is None

    async def test_async_csv_cached_none(self, tmp_path: Path) -> None:
        result = _make_result(tmp_path)
        c1 = await result.async_csv()
        c2 = await result.async_csv()
        assert c1 is c2

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

    async def test_async_html_none_when_no_file(self, tmp_path: Path) -> None:
        assert await _make_result(tmp_path).async_html() is None

    async def test_async_html_cached_none(self, tmp_path: Path) -> None:
        result = _make_result(tmp_path)
        h1 = await result.async_html()
        h2 = await result.async_html()
        assert h1 is h2

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
