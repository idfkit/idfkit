"""Simulation result container.

Provides structured access to EnergyPlus output files and parsed error reports
after a simulation run.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .parsers.err import ErrorReport

if TYPE_CHECKING:
    from .outputs import OutputVariableIndex
    from .parsers.csv import CSVResult
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
    """

    run_dir: Path
    success: bool
    exit_code: int | None
    stdout: str
    stderr: str
    runtime_seconds: float
    output_prefix: str = "eplus"
    _cached_errors: ErrorReport | None = field(default=None, init=False, repr=False)
    _cached_sql: Any = field(default=_UNSET, init=False, repr=False)
    _cached_variables: Any = field(default=_UNSET, init=False, repr=False)
    _cached_csv: Any = field(default=_UNSET, init=False, repr=False)

    @property
    def errors(self) -> ErrorReport:
        """Parsed error report from the .err file (lazily cached).

        Returns:
            Parsed ErrorReport from the simulation's .err output.
        """
        cached = object.__getattribute__(self, "_cached_errors")
        if cached is not None:
            return cached
        err = self.err_path
        report = ErrorReport.from_file(err) if err is not None else ErrorReport.from_string("")
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

        result: SQLResult = _SQLResult(path)
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
        from .outputs import OutputVariableIndex as _OutputVariableIndex

        result: OutputVariableIndex = _OutputVariableIndex.from_files(rdd, self.mdd_path)
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

        result: CSVResult = _CSVResult.from_file(path)
        object.__setattr__(self, "_cached_csv", result)
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
        return self._find_output_file("Table.html") or self._find_output_file(".html")

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
        """
        # Primary: prefixed name
        primary = self.run_dir / f"{self.output_prefix}out{suffix}"
        if primary.is_file():
            return primary

        # Fallback: scan directory
        for p in self.run_dir.iterdir():
            if p.is_file() and p.name.endswith(suffix):
                return p

        return None

    @classmethod
    def from_directory(cls, path: str | Path, *, output_prefix: str = "eplus") -> SimulationResult:
        """Reconstruct a SimulationResult from an existing output directory.

        Useful for inspecting results from a previous simulation run.

        Args:
            path: Path to the simulation output directory.
            output_prefix: Output file prefix used during the run.

        Returns:
            SimulationResult pointing to the existing output.
        """
        run_dir = Path(path).resolve()
        return cls(
            run_dir=run_dir,
            success=True,
            exit_code=0,
            stdout="",
            stderr="",
            runtime_seconds=0.0,
            output_prefix=output_prefix,
        )
