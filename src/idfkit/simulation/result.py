"""Simulation result container.

Provides structured access to EnergyPlus output files and parsed error reports
after a simulation run.
"""

from __future__ import annotations

import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .parsers.err import ErrorReport

if TYPE_CHECKING:
    from .fs import AsyncFileSystem, FileSystem
    from .outputs import OutputVariableIndex
    from .parsers.csv import CSVResult
    from .parsers.html import HTMLResult
    from .parsers.sql import SQLResult

# Sentinel for "not yet computed" (distinct from None = "computed, no file found")
_UNSET: Any = object()


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
            Set automatically by :func:`async_simulate` when an
            :class:`~idfkit.simulation.fs.AsyncFileSystem` is provided.
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
    _cached_errors: Any = field(default=_UNSET, init=False, repr=False)
    _cached_sql: Any = field(default=_UNSET, init=False, repr=False)
    _cached_variables: Any = field(default=_UNSET, init=False, repr=False)
    _cached_csv: Any = field(default=_UNSET, init=False, repr=False)
    _cached_html: Any = field(default=_UNSET, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.fs is not None and self.async_fs is not None:
            msg = "fs and async_fs are mutually exclusive — provide one or neither"
            raise ValueError(msg)

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
            result: SQLResult = _SQLResult(Path(tmp_file.name))
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
    def csv_path(self) -> Path | None:
        """Path to the .csv output file, if present."""
        return self._find_output_file(".csv")

    @property
    def html_path(self) -> Path | None:
        """Path to the HTML tabular output file, if present."""
        return (
            self._find_output_file("Table.htm")
            or self._find_output_file("Table.html")
            or self._find_output_file(".htm")
            or self._find_output_file(".html")
        )

    @property
    def rdd_path(self) -> Path | None:
        """Path to the .rdd output file, if present."""
        return self._find_output_file(".rdd")

    @property
    def mdd_path(self) -> Path | None:
        """Path to the .mdd output file, if present."""
        return self._find_output_file(".mdd")

    def _find_output_file(self, suffix: str) -> Path | None:
        """Find an output file by suffix.

        Looks for ``{prefix}out{suffix}`` first, then falls back to
        scanning the run directory for any file with the given suffix.

        Args:
            suffix: File suffix to look for (e.g. ".sql", ".err").

        Returns:
            Path to the file, or None if not found.

        Raises:
            RuntimeError: If only :attr:`async_fs` is set (no sync access
                available).  Use the ``async_*`` methods instead.
        """
        if self.async_fs is not None and self.fs is None:
            msg = (
                "This SimulationResult was created with an AsyncFileSystem. "
                "Use the async accessors (e.g. async_errors(), async_sql()) "
                "instead of the sync properties."
            )
            raise RuntimeError(msg)

        primary = self.run_dir / f"{self.output_prefix}out{suffix}"

        if self.fs is not None:
            if self.fs.exists(str(primary)):
                return primary
            # Fallback: glob for matching files
            matches = self.fs.glob(str(self.run_dir), f"*{suffix}")
            if matches:
                return Path(matches[0])
            return None

        # Local path-based lookup
        if primary.is_file():
            return primary

        # Fallback: scan directory
        for p in self.run_dir.iterdir():
            if p.is_file() and p.name.endswith(suffix):
                return p

        return None

    # ------------------------------------------------------------------
    # Async accessors — non-blocking counterparts to the sync properties
    # ------------------------------------------------------------------

    async def async_errors(self) -> ErrorReport:
        """Parsed error report from the .err file (async, lazily cached).

        Non-blocking counterpart to :attr:`errors` that uses
        :attr:`async_fs` for file reads.

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

        Non-blocking counterpart to :attr:`sql` that uses
        :attr:`async_fs` for file reads.

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
            result: SQLResult = _SQLResult(Path(tmp_file.name))
        elif self.fs is not None:
            data = self.fs.read_bytes(str(path))
            with tempfile.NamedTemporaryFile(suffix=".sql", delete=False) as tmp_file:
                tmp_file.write(data)
            result = _SQLResult(Path(tmp_file.name))
        else:
            result = _SQLResult(path)
        object.__setattr__(self, "_cached_sql", result)
        return result

    async def async_variables(self) -> OutputVariableIndex | None:
        """Output variable/meter index (async, lazily cached).

        Non-blocking counterpart to :attr:`variables` that uses
        :attr:`async_fs` for file reads.

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

        Non-blocking counterpart to :attr:`csv` that uses
        :attr:`async_fs` for file reads.

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

        Non-blocking counterpart to :attr:`html` that uses
        :attr:`async_fs` for file reads.

        Returns:
            An HTMLResult with extracted tables and titles,
            or None if no HTML file was produced.
        """
        cached = object.__getattribute__(self, "_cached_html")
        if cached is not _UNSET:
            return cached  # type: ignore[no-any-return]
        path = (
            await self._async_find_output_file("Table.htm")
            or await self._async_find_output_file("Table.html")
            or await self._async_find_output_file(".htm")
            or await self._async_find_output_file(".html")
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

    async def _async_find_output_file(self, suffix: str) -> Path | None:
        """Async counterpart to :meth:`_find_output_file`.

        Uses :attr:`async_fs` for non-blocking file lookups, falling back
        to :attr:`fs` or local path checks.

        Args:
            suffix: File suffix to look for (e.g. ".sql", ".err").

        Returns:
            Path to the file, or None if not found.
        """
        primary = self.run_dir / f"{self.output_prefix}out{suffix}"

        if self.async_fs is not None:
            if await self.async_fs.exists(str(primary)):
                return primary
            matches = await self.async_fs.glob(str(self.run_dir), f"*{suffix}")
            if matches:
                return Path(matches[0])
            return None

        if self.fs is not None:
            if self.fs.exists(str(primary)):
                return primary
            matches = self.fs.glob(str(self.run_dir), f"*{suffix}")
            if matches:
                return Path(matches[0])
            return None

        # Local path-based lookup
        if primary.is_file():
            return primary

        for p in self.run_dir.iterdir():
            if p.is_file() and p.name.endswith(suffix):
                return p

        return None

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
