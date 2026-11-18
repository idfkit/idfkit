"""Simulation result container.

Provides structured access to EnergyPlus output files and parsed error reports
after a simulation run.
"""

from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .parsers.err import ErrorReport

if TYPE_CHECKING:
    from collections.abc import Iterable

    from ..migration.report import MigrationReport
    from .fs import AsyncFileSystem, FileSystem
    from .outputs import OutputVariableIndex
    from .parsers.csv import CSVResult
    from .parsers.eso import ESOResult
    from .parsers.html import HTMLResult
    from .parsers.sql import SQLResult

# Sentinel for "not yet computed" (distinct from None = "computed, no file found")
_UNSET: Any = object()

#: ``run_dir`` of the result for a batch job that failed before EnergyPlus ran
#: and that named no ``output_dir``. It lies under the null device, so it can
#: never be created, and the output accessors never look inside it: a batch of
#: refused jobs leaves nothing behind.
REFUSED_RUN_DIR = Path(os.devnull) / "idfkit-refused-job"

#: Name stems EnergyPlus gives its auxiliary outputs, lower-cased, in every
#: ``--output-suffix`` style: legacy (``eplustbl.csv``, ``sqlite.err``),
#: capital (``eplusTable.csv``, ``eplusSqlite.err``) and dash
#: (``eplus-table.csv``, ``eplus-sqlite.err``). Each shares an extension with a
#: main output (``.err``, ``.csv``), so the directory-scan fallback skips them:
#: ``eplusSqlite.err`` holds the SQLite log, not the simulation's errors.
_AUXILIARY_STEMS: tuple[str, ...] = (
    "map",
    "meter",
    "mtr",
    "psz",
    "screen",
    "shading",
    "spsz",
    "sqlite",
    "ssz",
    "table",
    "tbl",
    "zsz",
)

#: Infixes EnergyPlus puts before the extension of the tabular report, in the
#: legacy, capital and dash ``--output-suffix`` styles.
_TABLE_INFIXES: tuple[str, ...] = ("tbl", "Table", "-table")


def _output_names(prefix: str, suffix: str, *, table: bool) -> tuple[str, ...]:
    """Return the file names EnergyPlus may give an output, most likely first.

    The runner passes ``-s C`` by default, which names the main outputs
    ``{prefix}{suffix}`` (``eplus.err``). The legacy style ``-s L`` names them
    ``{prefix}out{suffix}`` (``eplusout.err``) and is what EnergyPlus uses
    when run by hand without ``-s``. The tabular report is
    ``{prefix}tbl``, ``{prefix}Table`` or ``{prefix}-table`` instead.

    Args:
        prefix: The run's output prefix (``-p``).
        suffix: File suffix including the dot (e.g. ``".err"``).
        table: Whether the wanted file is the tabular report.

    Returns:
        Candidate file names, in lookup order.
    """
    if table:
        return tuple(f"{prefix}{infix}{suffix}" for infix in _TABLE_INFIXES)
    return (f"{prefix}{suffix}", f"{prefix}out{suffix}")


def _is_auxiliary(name: str, suffix: str) -> bool:
    """Whether *name* is one of EnergyPlus' auxiliary outputs for *suffix*."""
    stem = name[: -len(suffix)].lower()
    return stem.endswith(_AUXILIARY_STEMS)


def _pick_fallback(paths: Iterable[str | Path], suffix: str, *, table: bool) -> str | Path | None:
    """Choose the output file among *paths* when no expected name exists.

    Only names ending with *suffix* qualify. For a main output, auxiliary
    files (``eplusSqlite.err``, ``eplusTable.csv``) never qualify; for the
    tabular report, files named like one are preferred. Ties break on the
    name, so the choice does not depend on the order the file system lists
    the directory in.

    Args:
        paths: Files in the run directory.
        suffix: File suffix including the dot (e.g. ``".err"``).
        table: Whether the wanted file is the tabular report.

    Returns:
        The chosen path, or ``None`` if none qualifies.
    """
    best: tuple[bool, str] | None = None
    chosen: str | Path | None = None
    for path in paths:
        name = Path(path).name
        if not name.endswith(suffix):
            continue
        auxiliary = _is_auxiliary(name, suffix)
        if auxiliary and not table:
            continue
        key = (not auxiliary, name)
        if best is None or key < best:
            best, chosen = key, path
    return chosen


@dataclass(slots=True)
class SimulationResult:
    """Result of an EnergyPlus simulation run.

    Attributes:
        run_dir: Directory containing all simulation output.
        success: Whether the simulation exited successfully.
        exit_code: Process exit code (None if timed out).
        stdout: Captured standard output.
        stderr: Captured standard error.
        runtime_seconds: Wall-clock execution time in seconds.
        output_prefix: Output file prefix (default "eplus").
        fs: Optional sync file system backend for reading output files.
        async_fs: Optional async file system backend for non-blocking reads.
            Set automatically by [async_simulate][idfkit.simulation.async_runner.async_simulate] when an
            [AsyncFileSystem][idfkit.simulation.fs.AsyncFileSystem] is provided.
        migration_report: Populated when ``simulate(..., auto_migrate=True)``
            forward-migrated the model before running. ``None`` when no
            migration occurred.
    """

    run_dir: Path
    success: bool
    exit_code: int | None
    stdout: str
    stderr: str
    runtime_seconds: float
    output_prefix: str = "eplus"
    fs: FileSystem | None = field(default=None, repr=False)
    async_fs: AsyncFileSystem | None = field(default=None, repr=False)
    migration_report: MigrationReport | None = field(default=None, repr=False)
    _cached_errors: Any = field(default=_UNSET, init=False, repr=False)
    _cached_sql: Any = field(default=_UNSET, init=False, repr=False)
    _cached_variables: Any = field(default=_UNSET, init=False, repr=False)
    _cached_csv: Any = field(default=_UNSET, init=False, repr=False)
    _cached_html: Any = field(default=_UNSET, init=False, repr=False)
    _cached_eso: Any = field(default=_UNSET, init=False, repr=False)
    _cached_mtr: Any = field(default=_UNSET, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.fs is not None and self.async_fs is not None:
            msg = "fs and async_fs are mutually exclusive — provide one or neither"
            raise ValueError(msg)

    def close(self) -> None:
        """Release any open file handles held by cached parsers.

        Closes the SQLite connection opened lazily by [sql][idfkit.simulation.result.SimulationResult.sql] /
        [async_sql][idfkit.simulation.result.SimulationResult.async_sql] (and removes the temporary copy made
        for remote file systems). The other parsers read their files eagerly
        and hold no handles, so this is currently a no-op for them.

        Call this — or use the result as a context manager — before deleting
        the run directory. On Windows an open SQLite connection locks
        ``eplus.sql`` and blocks ``shutil.rmtree`` / ``TemporaryDirectory``
        cleanup with ``PermissionError [WinError 32]``. Safe to call more
        than once; the cached connection is reopened on next access if needed.
        """
        cached = object.__getattribute__(self, "_cached_sql")
        if cached is not _UNSET and cached is not None:
            cached.close()
        object.__setattr__(self, "_cached_sql", _UNSET)

    def __enter__(self) -> SimulationResult:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    @property
    def errors(self) -> ErrorReport:
        """Parsed error report from the .err file (lazily cached).

        Returns:
            Parsed ErrorReport from the simulation's .err output.
        """
        cached = object.__getattribute__(self, "_cached_errors")
        if cached is not _UNSET:
            return cached  # type: ignore[no-any-return]
        err = self.err_path
        if err is None:
            report = ErrorReport.from_string("")
        elif self.fs is not None:
            text = self.fs.read_text(str(err), encoding="latin-1")
            report = ErrorReport.from_string(text)
        else:
            report = ErrorReport.from_file(err)
        object.__setattr__(self, "_cached_errors", report)
        return report

    @property
    def sql(self) -> SQLResult | None:
        """Parsed SQL output database (lazily cached).

        Returns:
            An SQLResult for querying time-series and tabular data,
            or None if no .sql file was produced.
        """
        cached = object.__getattribute__(self, "_cached_sql")
        if cached is not _UNSET:
            return cached  # type: ignore[no-any-return]
        path = self.sql_path
        if path is None:
            object.__setattr__(self, "_cached_sql", None)
            return None
        from .parsers.sql import SQLResult as _SQLResult

        if self.fs is not None:
            # sqlite3 requires a local file — download to a temp file
            data = self.fs.read_bytes(str(path))
            with tempfile.NamedTemporaryFile(suffix=".sql", delete=False) as tmp_file:
                tmp_file.write(data)
            result: SQLResult = _SQLResult(Path(tmp_file.name), _owns_file=True)
        else:
            result = _SQLResult(path)
        object.__setattr__(self, "_cached_sql", result)
        return result

    @property
    def variables(self) -> OutputVariableIndex | None:
        """Output variable/meter index from .rdd/.mdd files (lazily cached).

        Returns:
            An OutputVariableIndex for searching and injecting output
            variables, or None if no .rdd file was produced.
        """
        cached = object.__getattribute__(self, "_cached_variables")
        if cached is not _UNSET:
            return cached  # type: ignore[no-any-return]
        rdd = self.rdd_path
        if rdd is None:
            object.__setattr__(self, "_cached_variables", None)
            return None

        if self.fs is not None:
            from .parsers.rdd import parse_mdd, parse_rdd

            rdd_text = self.fs.read_text(str(rdd), encoding="latin-1")
            variables = parse_rdd(rdd_text)
            mdd = self.mdd_path
            meters = parse_mdd(self.fs.read_text(str(mdd), encoding="latin-1")) if mdd is not None else ()
            from .outputs import OutputVariableIndex as _OutputVariableIndex

            result: OutputVariableIndex = _OutputVariableIndex(variables=variables, meters=meters)
        else:
            from .outputs import OutputVariableIndex as _OutputVariableIndex

            result = _OutputVariableIndex.from_files(rdd, self.mdd_path)
        object.__setattr__(self, "_cached_variables", result)
        return result

    @property
    def csv(self) -> CSVResult | None:
        """Parsed CSV output (lazily cached).

        Returns:
            A CSVResult with extracted column metadata and values,
            or None if no .csv file was produced.
        """
        cached = object.__getattribute__(self, "_cached_csv")
        if cached is not _UNSET:
            return cached  # type: ignore[no-any-return]
        path = self.csv_path
        if path is None:
            object.__setattr__(self, "_cached_csv", None)
            return None
        from .parsers.csv import CSVResult as _CSVResult

        if self.fs is not None:
            text = self.fs.read_text(str(path), encoding="latin-1")
            result: CSVResult = _CSVResult.from_string(text)
        else:
            result = _CSVResult.from_file(path)
        object.__setattr__(self, "_cached_csv", result)
        return result

    @property
    def html(self) -> HTMLResult | None:
        """Parsed HTML tabular output (lazily cached).

        Returns:
            An HTMLResult with extracted tables and titles,
            or None if no HTML file was produced.
        """
        cached = object.__getattribute__(self, "_cached_html")
        if cached is not _UNSET:
            return cached  # type: ignore[no-any-return]
        path = self.html_path
        if path is None:
            object.__setattr__(self, "_cached_html", None)
            return None
        from .parsers.html import HTMLResult as _HTMLResult

        if self.fs is not None:
            text = self.fs.read_text(str(path), encoding="latin-1")
            result: HTMLResult = _HTMLResult.from_string(text)
        else:
            result = _HTMLResult.from_file(path)
        object.__setattr__(self, "_cached_html", result)
        return result

    def _load_eso_sync(self, path: Path) -> ESOResult:
        """Read and parse an ESO/MTR file from disk or the sync file system."""
        from .parsers.eso import ESOResult as _ESOResult

        if self.fs is not None:
            return _ESOResult.from_bytes(self.fs.read_bytes(str(path)))
        return _ESOResult.from_file(path)

    @property
    def eso(self) -> ESOResult | None:
        """Parsed ESO time-series output (lazily cached).

        Returns:
            An ESOResult for extracting variable time series, or None if no
            .eso file was produced.
        """
        cached = object.__getattribute__(self, "_cached_eso")
        if cached is not _UNSET:
            return cached  # type: ignore[no-any-return]
        path = self.eso_path
        if path is None:
            object.__setattr__(self, "_cached_eso", None)
            return None
        result = self._load_eso_sync(path)
        object.__setattr__(self, "_cached_eso", result)
        return result

    @property
    def mtr(self) -> ESOResult | None:
        """Parsed MTR meter time-series output (lazily cached).

        The .mtr meter file uses the same format as .eso, so it is parsed by the
        same reader.

        Returns:
            An ESOResult for extracting meter time series, or None if no .mtr
            file was produced.
        """
        cached = object.__getattribute__(self, "_cached_mtr")
        if cached is not _UNSET:
            return cached  # type: ignore[no-any-return]
        path = self.mtr_path
        if path is None:
            object.__setattr__(self, "_cached_mtr", None)
            return None
        result = self._load_eso_sync(path)
        object.__setattr__(self, "_cached_mtr", result)
        return result

    @property
    def sql_path(self) -> Path | None:
        """Path to the SQLite output file, if present."""
        return self._find_output_file(".sql")

    @property
    def err_path(self) -> Path | None:
        """Path to the .err output file, if present."""
        return self._find_output_file(".err")

    @property
    def eso_path(self) -> Path | None:
        """Path to the .eso output file, if present."""
        return self._find_output_file(".eso")

    @property
    def mtr_path(self) -> Path | None:
        """Path to the .mtr meter output file, if present."""
        return self._find_output_file(".mtr")

    @property
    def csv_path(self) -> Path | None:
        """Path to the .csv output file, if present."""
        return self._find_output_file(".csv")

    @property
    def html_path(self) -> Path | None:
        """Path to the HTML tabular output file, if present."""
        return self._find_output_file(".htm", table=True) or self._find_output_file(".html", table=True)

    @property
    def rdd_path(self) -> Path | None:
        """Path to the .rdd output file, if present."""
        return self._find_output_file(".rdd")

    @property
    def mdd_path(self) -> Path | None:
        """Path to the .mdd output file, if present."""
        return self._find_output_file(".mdd")

    def _find_output_file(self, suffix: str, *, table: bool = False) -> Path | None:
        """Find an output file by suffix.

        Tries each name EnergyPlus gives the output for
        [output_prefix][idfkit.simulation.result.SimulationResult.output_prefix]
        (``{prefix}{suffix}``, then ``{prefix}out{suffix}``), then falls back to
        the first matching file of the run directory in name order, never an
        auxiliary output such as ``eplusSqlite.err``.

        Args:
            suffix: File suffix to look for (e.g. ".sql", ".err").
            table: Look for the tabular report (``{prefix}Table.htm`` and its
                other spellings) rather than a main output.

        Returns:
            Path to the file, or None if not found.

        Raises:
            RuntimeError: If only [async_fs][idfkit.simulation.result.SimulationResult.async_fs] is set (no sync access
                available).  Use the ``async_*`` methods instead.
        """
        if self.async_fs is not None and self.fs is None:
            msg = (
                "This SimulationResult was created with an AsyncFileSystem. "
                "Use the async accessors (e.g. async_errors(), async_sql()) "
                "instead of the sync properties."
            )
            raise RuntimeError(msg)

        if self.run_dir == REFUSED_RUN_DIR:
            return None

        candidates = [self.run_dir / name for name in _output_names(self.output_prefix, suffix, table=table)]

        if self.fs is not None:
            fs = self.fs
            for candidate in candidates:
                if fs.exists(str(candidate)):
                    return candidate
            match = _pick_fallback(fs.glob(str(self.run_dir), f"*{suffix}"), suffix, table=table)
            return None if match is None else Path(match)

        # Local path-based lookup
        for candidate in candidates:
            if candidate.is_file():
                return candidate

        return self._scan_run_dir(suffix, table=table)

    def _scan_run_dir(self, suffix: str, *, table: bool = False) -> Path | None:
        """Return the local run directory's fallback file for *suffix*, if any."""
        if not self.run_dir.is_dir():
            return None
        files = (p for p in self.run_dir.iterdir() if p.is_file())
        match = _pick_fallback(files, suffix, table=table)
        return None if match is None else Path(match)

    # ------------------------------------------------------------------
    # Async accessors — non-blocking counterparts to the sync properties
    # ------------------------------------------------------------------

    async def async_errors(self) -> ErrorReport:
        """Parsed error report from the .err file (async, lazily cached).

        Non-blocking counterpart to [errors][idfkit.simulation.result.SimulationResult.errors] that uses
        [async_fs][idfkit.simulation.result.SimulationResult.async_fs] for file reads.

        Returns:
            Parsed ErrorReport from the simulation's .err output.
        """
        cached = object.__getattribute__(self, "_cached_errors")
        if cached is not _UNSET:
            return cached  # type: ignore[no-any-return]
        err = await self._async_find_output_file(".err")
        if err is None:
            report = ErrorReport.from_string("")
        elif self.async_fs is not None:
            text = await self.async_fs.read_text(str(err), encoding="latin-1")
            report = ErrorReport.from_string(text)
        elif self.fs is not None:
            text = self.fs.read_text(str(err), encoding="latin-1")
            report = ErrorReport.from_string(text)
        else:
            report = ErrorReport.from_file(err)
        object.__setattr__(self, "_cached_errors", report)
        return report

    async def async_sql(self) -> SQLResult | None:
        """Parsed SQL output database (async, lazily cached).

        Non-blocking counterpart to [sql][idfkit.simulation.result.SimulationResult.sql] that uses
        [async_fs][idfkit.simulation.result.SimulationResult.async_fs] for file reads.

        Returns:
            An SQLResult for querying time-series and tabular data,
            or None if no .sql file was produced.
        """
        cached = object.__getattribute__(self, "_cached_sql")
        if cached is not _UNSET:
            return cached  # type: ignore[no-any-return]
        path = await self._async_find_output_file(".sql")
        if path is None:
            object.__setattr__(self, "_cached_sql", None)
            return None
        from .parsers.sql import SQLResult as _SQLResult

        if self.async_fs is not None:
            data = await self.async_fs.read_bytes(str(path))
            with tempfile.NamedTemporaryFile(suffix=".sql", delete=False) as tmp_file:
                tmp_file.write(data)
            result: SQLResult = _SQLResult(Path(tmp_file.name), _owns_file=True)
        elif self.fs is not None:
            data = self.fs.read_bytes(str(path))
            with tempfile.NamedTemporaryFile(suffix=".sql", delete=False) as tmp_file:
                tmp_file.write(data)
            result = _SQLResult(Path(tmp_file.name), _owns_file=True)
        else:
            result = _SQLResult(path)
        object.__setattr__(self, "_cached_sql", result)
        return result

    async def async_variables(self) -> OutputVariableIndex | None:
        """Output variable/meter index (async, lazily cached).

        Non-blocking counterpart to [variables][idfkit.simulation.result.SimulationResult.variables] that uses
        [async_fs][idfkit.simulation.result.SimulationResult.async_fs] for file reads.

        Returns:
            An OutputVariableIndex for searching and injecting output
            variables, or None if no .rdd file was produced.
        """
        cached = object.__getattribute__(self, "_cached_variables")
        if cached is not _UNSET:
            return cached  # type: ignore[no-any-return]
        rdd = await self._async_find_output_file(".rdd")
        if rdd is None:
            object.__setattr__(self, "_cached_variables", None)
            return None

        if self.async_fs is not None:
            from .parsers.rdd import parse_mdd, parse_rdd

            rdd_text = await self.async_fs.read_text(str(rdd), encoding="latin-1")
            variables = parse_rdd(rdd_text)
            mdd = await self._async_find_output_file(".mdd")
            meters = parse_mdd(await self.async_fs.read_text(str(mdd), encoding="latin-1")) if mdd is not None else ()
            from .outputs import OutputVariableIndex as _OutputVariableIndex

            result: OutputVariableIndex = _OutputVariableIndex(variables=variables, meters=meters)
        elif self.fs is not None:
            from .parsers.rdd import parse_mdd, parse_rdd

            rdd_text = self.fs.read_text(str(rdd), encoding="latin-1")
            variables = parse_rdd(rdd_text)
            mdd = self._find_output_file(".mdd")
            meters = parse_mdd(self.fs.read_text(str(mdd), encoding="latin-1")) if mdd is not None else ()
            from .outputs import OutputVariableIndex as _OutputVariableIndex

            result = _OutputVariableIndex(variables=variables, meters=meters)
        else:
            from .outputs import OutputVariableIndex as _OutputVariableIndex

            result = _OutputVariableIndex.from_files(rdd, self.mdd_path)
        object.__setattr__(self, "_cached_variables", result)
        return result

    async def async_csv(self) -> CSVResult | None:
        """Parsed CSV output (async, lazily cached).

        Non-blocking counterpart to [csv][idfkit.simulation.result.SimulationResult.csv] that uses
        [async_fs][idfkit.simulation.result.SimulationResult.async_fs] for file reads.

        Returns:
            A CSVResult with extracted column metadata and values,
            or None if no .csv file was produced.
        """
        cached = object.__getattribute__(self, "_cached_csv")
        if cached is not _UNSET:
            return cached  # type: ignore[no-any-return]
        path = await self._async_find_output_file(".csv")
        if path is None:
            object.__setattr__(self, "_cached_csv", None)
            return None
        from .parsers.csv import CSVResult as _CSVResult

        if self.async_fs is not None:
            text = await self.async_fs.read_text(str(path), encoding="latin-1")
            result: CSVResult = _CSVResult.from_string(text)
        elif self.fs is not None:
            text = self.fs.read_text(str(path), encoding="latin-1")
            result = _CSVResult.from_string(text)
        else:
            result = _CSVResult.from_file(path)
        object.__setattr__(self, "_cached_csv", result)
        return result

    async def async_html(self) -> HTMLResult | None:
        """Parsed HTML tabular output (async, lazily cached).

        Non-blocking counterpart to [html][idfkit.simulation.result.SimulationResult.html] that uses
        [async_fs][idfkit.simulation.result.SimulationResult.async_fs] for file reads.

        Returns:
            An HTMLResult with extracted tables and titles,
            or None if no HTML file was produced.
        """
        cached = object.__getattribute__(self, "_cached_html")
        if cached is not _UNSET:
            return cached  # type: ignore[no-any-return]
        path = await self._async_find_output_file(".htm", table=True) or await self._async_find_output_file(
            ".html", table=True
        )
        if path is None:
            object.__setattr__(self, "_cached_html", None)
            return None
        from .parsers.html import HTMLResult as _HTMLResult

        if self.async_fs is not None:
            text = await self.async_fs.read_text(str(path), encoding="latin-1")
            result: HTMLResult = _HTMLResult.from_string(text)
        elif self.fs is not None:
            text = self.fs.read_text(str(path), encoding="latin-1")
            result = _HTMLResult.from_string(text)
        else:
            result = _HTMLResult.from_file(path)
        object.__setattr__(self, "_cached_html", result)
        return result

    async def _load_eso_async(self, path: Path) -> ESOResult:
        """Read and parse an ESO/MTR file via the async/sync file system or disk."""
        from .parsers.eso import ESOResult as _ESOResult

        if self.async_fs is not None:
            return _ESOResult.from_bytes(await self.async_fs.read_bytes(str(path)))
        if self.fs is not None:
            return _ESOResult.from_bytes(self.fs.read_bytes(str(path)))
        return _ESOResult.from_file(path)

    async def async_eso(self) -> ESOResult | None:
        """Parsed ESO time-series output (async, lazily cached).

        Non-blocking counterpart to [eso][idfkit.simulation.result.SimulationResult.eso] that uses
        [async_fs][idfkit.simulation.result.SimulationResult.async_fs] for file reads.

        Returns:
            An ESOResult, or None if no .eso file was produced.
        """
        cached = object.__getattribute__(self, "_cached_eso")
        if cached is not _UNSET:
            return cached  # type: ignore[no-any-return]
        path = await self._async_find_output_file(".eso")
        if path is None:
            object.__setattr__(self, "_cached_eso", None)
            return None
        result = await self._load_eso_async(path)
        object.__setattr__(self, "_cached_eso", result)
        return result

    async def async_mtr(self) -> ESOResult | None:
        """Parsed MTR meter time-series output (async, lazily cached).

        Non-blocking counterpart to [mtr][idfkit.simulation.result.SimulationResult.mtr] that uses
        [async_fs][idfkit.simulation.result.SimulationResult.async_fs] for file reads.

        Returns:
            An ESOResult, or None if no .mtr file was produced.
        """
        cached = object.__getattribute__(self, "_cached_mtr")
        if cached is not _UNSET:
            return cached  # type: ignore[no-any-return]
        path = await self._async_find_output_file(".mtr")
        if path is None:
            object.__setattr__(self, "_cached_mtr", None)
            return None
        result = await self._load_eso_async(path)
        object.__setattr__(self, "_cached_mtr", result)
        return result

    async def _async_find_output_file(self, suffix: str, *, table: bool = False) -> Path | None:
        """Async counterpart to [_find_output_file][].

        Uses [async_fs][idfkit.simulation.result.SimulationResult.async_fs] for non-blocking file lookups, falling back
        to [fs][] or local path checks. The names tried, and the fallback, are
        those of the sync lookup.

        Args:
            suffix: File suffix to look for (e.g. ".sql", ".err").
            table: Look for the tabular report rather than a main output.

        Returns:
            Path to the file, or None if not found.
        """
        if self.run_dir == REFUSED_RUN_DIR:
            return None

        if self.async_fs is not None:
            async_fs = self.async_fs
            for name in _output_names(self.output_prefix, suffix, table=table):
                candidate = self.run_dir / name
                if await async_fs.exists(str(candidate)):
                    return candidate
            matches = await async_fs.glob(str(self.run_dir), f"*{suffix}")
            match = _pick_fallback(matches, suffix, table=table)
            return None if match is None else Path(match)

        return self._find_output_file(suffix, table=table)

    @classmethod
    def from_directory(
        cls,
        path: str | Path,
        *,
        output_prefix: str = "eplus",
        fs: FileSystem | None = None,
        async_fs: AsyncFileSystem | None = None,
    ) -> SimulationResult:
        """Reconstruct a SimulationResult from an existing output directory.

        Useful for inspecting results from a previous simulation run.

        Args:
            path: Path to the simulation output directory.
            output_prefix: Output file prefix used during the run.
            fs: Optional sync file system backend for reading output files.
            async_fs: Optional async file system backend for non-blocking reads.

        Returns:
            SimulationResult pointing to the existing output.
        """
        run_dir = Path(path) if (fs is not None or async_fs is not None) else Path(path).resolve()
        return cls(
            run_dir=run_dir,
            success=True,
            exit_code=0,
            stdout="",
            stderr="",
            runtime_seconds=0.0,
            output_prefix=output_prefix,
            fs=fs,
            async_fs=async_fs,
        )
