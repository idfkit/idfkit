"""Parser for EnergyPlus SQLite output files.

Provides structured access to time-series data, tabular reports, and variable
metadata from the ``eplusout.sql`` database produced by EnergyPlus when
``Output:SQLite`` is present in the model.
"""

from __future__ import annotations

import contextlib
import sqlite3
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, NoReturn, TypeAlias

from ...exceptions import ResultLookupError, closest_names
from ._lookup import did_you_mean, listing, resolve_series
from ._timeutil import FREQUENCY_MAP, REFERENCE_YEAR, make_timestamp, summarize_series

if TYPE_CHECKING:
    import pandas as pd

    from ..plotting import PlotBackend


@dataclass(frozen=True, slots=True, repr=False)
class TimeSeriesResult:
    """A single time series extracted from an EnergyPlus SQL database.

    Attributes:
        variable_name: The output variable name.
        key_value: The key value (e.g. zone or surface name).
        units: The variable units.
        frequency: The reporting frequency.
        timestamps: Timestamp for each data point.
        values: Numeric values for each data point.
    """

    variable_name: str
    key_value: str
    units: str
    frequency: str
    timestamps: tuple[datetime, ...]
    values: tuple[float, ...]

    def __repr__(self) -> str:
        # A summary, not the data: one hourly annual series would otherwise print about 500 KB.
        return (
            f"TimeSeriesResult({self.variable_name!r}, {self.key_value!r}, units={self.units!r}, "
            f"frequency={self.frequency!r}, {summarize_series(self.timestamps, self.values)})"
        )

    def to_dataframe(self) -> pd.DataFrame:
        """Convert to a pandas DataFrame.

        Requires pandas to be installed.

        Returns:
            A DataFrame with a ``timestamp`` index and a column for the values.

        Raises:
            ImportError: If pandas is not installed.
        """
        try:
            import pandas as _pd  # type: ignore[import-not-found]
        except ImportError:
            msg = "pandas is required for DataFrame conversion. Install it with: pip install idfkit[dataframes]"
            raise ImportError(msg) from None
        return _pd.DataFrame(  # type: ignore[no-any-return]
            {"timestamp": list(self.timestamps), self.variable_name: list(self.values)}
        ).set_index("timestamp")

    def plot(self, *, backend: PlotBackend | None = None, title: str | None = None) -> Any:
        """Plot this time series as a line chart.

        Auto-detects the plotting backend if not provided. Requires matplotlib
        or plotly to be installed.

        Args:
            backend: A PlotBackend instance. If not provided, auto-detects.
            title: Optional plot title. Defaults to ``"key_value: variable_name"``.

        Returns:
            A figure object from the backend.

        Raises:
            ImportError: If no plotting backend is available.
        """
        if backend is None:
            from ..plotting import get_default_backend

            backend = get_default_backend()
        plot_title = title or f"{self.key_value}: {self.variable_name}"
        return backend.line(
            list(self.timestamps),
            list(self.values),
            title=plot_title,
            xlabel="Time",
            ylabel=f"{self.variable_name} ({self.units})",
            label=self.key_value,
        )


@dataclass(frozen=True, slots=True)
class TabularRow:
    """A single row from an EnergyPlus tabular report.

    Attributes:
        report_name: The report name (e.g. ``"AnnualBuildingUtilityPerformanceSummary"``).
        report_for: The report scope (e.g. ``"Entire Facility"``).
        table_name: The table name within the report.
        row_name: The row label.
        column_name: The column label.
        units: The value units.
        value: The cell value as a string.
    """

    report_name: str
    report_for: str
    table_name: str
    row_name: str
    column_name: str
    units: str
    value: str


@dataclass(frozen=True, slots=True)
class VariableInfo:
    """Metadata about an available variable or meter in the SQL database.

    This class represents both regular variables and meters because EnergyPlus
    stores them in a single ``ReportDataDictionary`` table, distinguished only
    by an ``IsMeter`` column.  Use the [is_meter][idfkit.simulation.parsers.sql.VariableInfo.is_meter] flag to tell them
    apart.

    For pre-simulation discovery from ``.rdd`` / ``.mdd`` files, see the
    separate [OutputVariable][idfkit.simulation.parsers.rdd.OutputVariable] and
    [OutputMeter][idfkit.simulation.parsers.rdd.OutputMeter] classes instead.

    Attributes:
        name: The variable name.
        key_value: The key value.  Empty for meters.
        frequency: The reporting frequency.
        units: The variable units.
        is_meter: Whether this is a meter (vs. a regular variable).
        variable_type: The variable type string (e.g. ``"Zone"``, ``"HVAC"``).
    """

    name: str
    key_value: str
    frequency: str
    units: str
    is_meter: bool
    variable_type: str


@dataclass(frozen=True, slots=True)
class EnvironmentInfo:
    """Metadata about a simulation environment period.

    Attributes:
        index: The environment period index in the database.
        name: The environment name (e.g. ``"RUN PERIOD 1"``).
        environment_type: The type integer (1 = DesignDay, 2 = DesignRunPeriod,
            3 = WeatherFileRunPeriod).
    """

    index: int
    name: str
    environment_type: int


# Accepted string values for the ``environment`` parameter.
Environment = Literal["annual", "sizing", "all"]

# EnergyPlus EnvironmentType values in the EnvironmentPeriods table, per
# ``environment`` choice: 1 = DesignDay, 2 = DesignRunPeriod, 3 = WeatherFileRunPeriod.
_ENVIRONMENT_TYPES: dict[str, frozenset[int]] = {
    "annual": frozenset({3}),
    "sizing": frozenset({1, 2}),
}
_ENVIRONMENT_TYPES["all"] = _ENVIRONMENT_TYPES["annual"] | _ENVIRONMENT_TYPES["sizing"]


#: One series to read: a ``VariableInfo``, a variable name, or ``(name, key)`` / ``(name, key, frequency)``.
SeriesSpec: TypeAlias = VariableInfo | str | tuple[str, str] | tuple[str, str, str | None]

# One ReportData row: Year, Month, Day, Hour, Minute, Value, EnvironmentType.
_DataRow: TypeAlias = tuple[int, int, int, int, int, float, int | None]

# Series per ReportData query, under SQLite's oldest bound-parameter limit (999).
_MAX_PARAMS = 900


def _series_args(spec: SeriesSpec) -> tuple[str, str, str | None]:
    """The ``(name, key, frequency)`` a series spec names, with ``get_timeseries``'s defaults."""
    if isinstance(spec, VariableInfo):
        return spec.name, spec.key_value, spec.frequency
    if isinstance(spec, str):
        return spec, "*", None
    if len(spec) == 2:
        return spec[0], spec[1], None
    return spec[0], spec[1], spec[2]


def _environment_types(
    rows: Sequence[tuple[object, ...]], name: str, environment: Environment | None
) -> frozenset[int] | None:
    """The environment types to keep from *rows* (type last), or ``None`` to keep every row.

    ``None`` picks the weather-file run periods when the variable has data there, and
    otherwise the design days, so an annual run never mixes the two.

    Raises:
        ResultLookupError: If *environment* names a kind the variable has no data for.
    """
    present = {row[-1] for row in rows}
    if environment == "all":
        return None
    if environment is None:
        for choice in ("annual", "sizing"):
            if present & _ENVIRONMENT_TYPES[choice]:
                return _ENVIRONMENT_TYPES[choice]
        return None
    wanted = _ENVIRONMENT_TYPES[environment]
    if rows and not present & wanted:
        kinds = [choice for choice in ("annual", "sizing") if present & _ENVIRONMENT_TYPES[choice]]
        label = "run-period ('annual')" if environment == "annual" else "design-day ('sizing')"
        msg = f"Variable '{name}' has no {label} data in this run."
        if kinds:
            msg += f" It has data for environment={' and '.join(repr(k) for k in kinds)}."
        raise ResultLookupError(msg, available=kinds)
    return wanted


class SQLResult:
    """Query interface for an EnergyPlus SQLite output database.

    Opens the database in read-only mode and provides methods for retrieving
    time-series data, tabular reports, and variable metadata.

    Can be used as a context manager:

        ```python
        with SQLResult("eplusout.sql") as sql:
            ts = sql.get_timeseries("Zone Mean Air Temperature", "ZONE 1")
        ```
    """

    def __init__(self, db_path: str | Path, *, _owns_file: bool = False) -> None:
        """Open the SQLite database in read-only mode.

        Args:
            db_path: Path to the EnergyPlus ``.sql`` output file.
            _owns_file: Internal flag. When ``True``, [close][idfkit.simulation.parsers.sql.SQLResult.close]
                also unlinks ``db_path`` — used when the file is a temporary
                copy made for a remote file system backend.
        """
        self._db_path = Path(db_path)
        self._owns_file = _owns_file
        self._closed = False
        self._conn = sqlite3.connect(f"file:{self._db_path}?mode=ro", uri=True)

    def close(self) -> None:
        """Close the database connection.

        Releases the underlying OS file handle. This matters on Windows,
        where an open SQLite connection holds a lock that prevents the
        ``.sql`` file (and any directory containing it) from being deleted.
        Safe to call more than once.
        """
        if self._closed:
            return
        self._closed = True
        self._conn.close()
        if self._owns_file:
            with contextlib.suppress(OSError):
                self._db_path.unlink()

    def __enter__(self) -> SQLResult:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def __del__(self) -> None:
        # Safety net: release the file handle if the caller never closed the
        # connection. Guarded because __init__ may have failed before _conn
        # was assigned. Errors during interpreter shutdown are ignored.
        if getattr(self, "_closed", True):
            return
        with contextlib.suppress(Exception):
            self.close()

    def get_timeseries(
        self,
        variable_name: str,
        key_value: str = "*",
        frequency: str | None = None,
        environment: Environment | None = None,
    ) -> TimeSeriesResult:
        """Retrieve a time series for a variable.

        The variable name, key and frequency all match case-insensitively, as
        EnergyPlus matches them. The lookup must resolve to one reported series:
        when a variable is reported for several keys (one per zone, say) or at
        several frequencies, name the one you want, and the error lists them.

        Args:
            variable_name: The output variable name.
            key_value: The key value (e.g. zone name). The default ``"*"`` accepts
                any key, so it suits variables reported for a single key, such as
                the ``Environment`` site variables and meters.
            frequency: Optional frequency filter (e.g. ``"Hourly"``). Needed only
                when the variable is reported at more than one frequency.
            environment: Which simulation environments to read. ``None``
                (default) reads the weather-file run periods when the variable
                has data there, and the design days otherwise, so an annual
                run never mixes the two. ``"annual"`` reads only run periods,
                ``"sizing"`` only design days, and ``"all"`` both, in run order.

        Returns:
            A TimeSeriesResult with timestamps and values.

        Raises:
            ResultLookupError: A ``KeyError`` subclass, if the variable, key or
                frequency is not in the database (with the closest names and the
                reported keys), if several keys or frequencies match, if the
                variable has no data for the *environment* asked for, or if
                EnergyPlus simulated no environment at all (an ``annual=True``
                run of a model with no ``RunPeriod``, say).
            ValueError: If *environment* is not a recognized value.
        """
        return self.get_timeseries_many([(variable_name, key_value, frequency)], environment)[0]

    def get_timeseries_many(
        self,
        series: Iterable[SeriesSpec],
        environment: Environment | None = None,
    ) -> list[TimeSeriesResult]:
        """Retrieve several time series in one read of the database.

        EnergyPlus does not index ``ReportData`` by variable, so each
        [get_timeseries][idfkit.simulation.parsers.sql.SQLResult.get_timeseries]
        call scans the whole table. This reads every requested series in a
        single scan, which is much faster than a loop when reading more than
        one or two series from a large file.

        Args:
            series: The series to read, each a ``VariableInfo`` (as
                [list_variables][idfkit.simulation.parsers.sql.SQLResult.list_variables]
                returns), a variable name, or a ``(name, key)`` or
                ``(name, key, frequency)`` tuple, resolved as
                ``get_timeseries`` resolves its arguments.
            environment: Which simulation environments to read, as in
                ``get_timeseries``; it applies to every series.

        Returns:
            One [TimeSeriesResult][idfkit.simulation.parsers.sql.TimeSeriesResult]
            per item of *series*, in the same order.

        Raises:
            ResultLookupError: If any series does not resolve to exactly one
                reported series or has no data for *environment*, as in
                ``get_timeseries``.
            ValueError: If *environment* is not a recognized value.
        """
        if environment is not None and environment not in _ENVIRONMENT_TYPES:
            msg = f"environment must be 'annual', 'sizing', 'all', or None, got {environment!r}"
            raise ValueError(msg)
        resolved = [self._find_variable(*_series_args(spec)) for spec in series]
        rows_by_index = self._read_report_data(sorted({r[0] for r in resolved}))
        has_environments: bool | None = None
        results: list[TimeSeriesResult] = []
        for rdd_index, name, key_val, units, raw_freq in resolved:
            rows = rows_by_index[rdd_index]
            if not rows:
                if has_environments is None:
                    has_environments = bool(self.list_environments())
                if not has_environments:
                    raise ResultLookupError(self._no_environment_message(name))
            wanted = _environment_types(rows, name, environment)
            timestamps: list[datetime] = []
            values: list[float] = []
            for year, month, day, hour, minute, value, env_type in rows:
                if wanted is not None and env_type not in wanted:
                    continue
                ref_year = year if year and year > 0 else REFERENCE_YEAR
                timestamps.append(make_timestamp(ref_year, month, day, hour, minute))
                values.append(float(value))
            results.append(
                TimeSeriesResult(
                    variable_name=name,
                    key_value=key_val,
                    units=units,
                    frequency=FREQUENCY_MAP.get(raw_freq, raw_freq) if raw_freq else "Unknown",
                    timestamps=tuple(timestamps),
                    values=tuple(values),
                )
            )
        return results

    def _read_report_data(self, indexes: Sequence[int]) -> dict[int, list[_DataRow]]:
        """Read the non-warmup ``ReportData`` rows of *indexes*, each with its environment type, in time order."""
        rows_by_index: dict[int, list[_DataRow]] = {index: [] for index in indexes}
        cur = self._conn.cursor()
        # Each statement scans ReportData once; chunks keep under SQLite's bound-parameter limit.
        for start in range(0, len(indexes), _MAX_PARAMS):
            chunk = indexes[start : start + _MAX_PARAMS]
            placeholders = ",".join("?" * len(chunk))
            # COALESCE handles EnergyPlus versions where WarmupFlag is NULL; the
            # LEFT JOIN keeps rows with no environment.
            cur.execute(
                "SELECT rd.ReportDataDictionaryIndex, t.Year, t.Month, t.Day, t.Hour, t.Minute, rd.Value, "  # noqa: S608
                "ep.EnvironmentType "
                "FROM ReportData rd "
                "JOIN Time t ON rd.TimeIndex = t.TimeIndex "
                "LEFT JOIN EnvironmentPeriods ep ON t.EnvironmentPeriodIndex = ep.EnvironmentPeriodIndex "
                f"WHERE rd.ReportDataDictionaryIndex IN ({placeholders}) AND COALESCE(t.WarmupFlag, 0) = 0 "
                "ORDER BY t.TimeIndex",
                chunk,
            )
            for row in cur:
                rows_by_index[row[0]].append(row[1:])
        return rows_by_index

    @staticmethod
    def _no_environment_message(name: str) -> str:
        """Why *name* has no data in a run that simulated no environment, and what to do about it."""
        return (
            f"Variable '{name}' has no data: EnergyPlus simulated no environment in this run. "
            "An annual run (annual=True) needs a RunPeriod in the model; a design-day run needs "
            "SizingPeriod objects and SimulationControl's 'Run Simulation for Sizing Periods' set to Yes. "
            "The .err file says what EnergyPlus skipped."
        )

    def _find_variable(
        self, variable_name: str, key_value: str, frequency: str | None
    ) -> tuple[int, str, str, str, str]:
        """Resolve one ``ReportDataDictionary`` row: ``(index, name, key, units, raw frequency)``.

        Raises:
            ResultLookupError: If no row, or more than one, matches.
        """
        cur = self._conn.cursor()
        cur.execute(
            "SELECT ReportDataDictionaryIndex, Name, COALESCE(KeyValue, ''), COALESCE(Units, ''), "
            "COALESCE(ReportingFrequency, '') FROM ReportDataDictionary "
            "WHERE Name = ? COLLATE NOCASE ORDER BY ReportDataDictionaryIndex",
            (variable_name,),
        )
        rows: list[tuple[int, str, str, str, str]] = cur.fetchall()
        if not rows:
            cur.execute("SELECT DISTINCT Name FROM ReportDataDictionary")
            names = [str(r[0]) for r in cur.fetchall()]
            close = closest_names(variable_name, names, n=3)
            msg = f"Variable '{variable_name}' is not in this run's output."
            msg += did_you_mean(close)
            msg += " Request it with an Output:Variable (or Output:Meter) object; list_variables() shows what was reported."
            raise ResultLookupError(msg, suggestions=close)
        return resolve_series(
            rows,
            variable_name,
            key_value,
            frequency,
            name_of=lambda row: row[1],
            key_of=lambda row: row[2],
            frequency_of=lambda row: row[4],
            frequency_matches=lambda row, wanted: (
                wanted in (row[4].casefold(), FREQUENCY_MAP.get(row[4], row[4]).casefold())
            ),
            not_found_hint="",
        )

    def get_tabular_data(
        self,
        report_name: str | None = None,
        table_name: str | None = None,
        row_name: str | None = None,
        column_name: str | None = None,
        report_for: str | None = None,
    ) -> list[TabularRow]:
        """Retrieve tabular report data.

        Args:
            report_name: Optional filter by report name.
            table_name: Optional filter by table name.
            row_name: Optional filter by row label.
            column_name: Optional filter by column label.
            report_for: Optional filter by report scope (e.g. ``"Entire Facility"``).

        Returns:
            List of TabularRow entries matching the filters.
        """
        query = (
            "SELECT ReportName, ReportForString, TableName, RowName, "
            "ColumnName, Units, Value "
            "FROM TabularDataWithStrings"
        )
        conditions: list[str] = []
        params: list[str] = []

        if report_name is not None:
            conditions.append("ReportName = ?")
            params.append(report_name)
        if table_name is not None:
            conditions.append("TableName = ?")
            params.append(table_name)
        if row_name is not None:
            conditions.append("RowName = ?")
            params.append(row_name)
        if column_name is not None:
            conditions.append("ColumnName = ?")
            params.append(column_name)
        if report_for is not None:
            conditions.append("ReportForString = ?")
            params.append(report_for)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cur = self._conn.cursor()
        cur.execute(query, params)

        return [
            TabularRow(
                report_name=row[0],
                report_for=row[1],
                table_name=row[2],
                row_name=row[3],
                column_name=row[4],
                units=row[5],
                value=row[6],
            )
            for row in cur.fetchall()
        ]

    def get_tabular_value(
        self,
        report_name: str,
        table_name: str,
        row_name: str,
        column_name: str,
        report_for: str = "Entire Facility",
    ) -> str:
        """Retrieve a single tabular cell value.

        Convenience wrapper around [get_tabular_data][idfkit.simulation.parsers.sql.SQLResult.get_tabular_data] that returns
        exactly one cell value.

        Args:
            report_name: Report name (e.g. ``"AnnualBuildingUtilityPerformanceSummary"``).
            table_name: Table name (e.g. ``"End Uses"``).
            row_name: Row label (e.g. ``"Heating"``).
            column_name: Column label (e.g. ``"Electricity"``).
            report_for: Report scope (default ``"Entire Facility"``).

        Returns:
            The cell value as a string.

        Raises:
            ResultLookupError: A ``KeyError`` subclass, if no row matches (naming the
                first argument that matches nothing, with the closest spellings) or
                if several rows match.
        """
        rows = self.get_tabular_data(
            report_name=report_name,
            table_name=table_name,
            row_name=row_name,
            column_name=column_name,
            report_for=report_for,
        )
        if len(rows) == 0:
            self._raise_tabular_not_found({
                "ReportName": ("report", report_name),
                "ReportForString": ("report_for", report_for),
                "TableName": ("table", table_name),
                "RowName": ("row", row_name),
                "ColumnName": ("column", column_name),
            })
        if len(rows) > 1:
            msg = (
                f"Multiple rows found ({len(rows)}): report='{report_name}', table='{table_name}', "
                f"row='{row_name}', column='{column_name}', report_for='{report_for}'"
            )
            raise ResultLookupError(msg)
        return rows[0].value

    def _raise_tabular_not_found(self, filters: dict[str, tuple[str, str]]) -> NoReturn:
        """Name the first of *filters* (column -> (label, value)) that matches nothing, with its spellings.

        Raises:
            ResultLookupError: Always.
        """
        cur = self._conn.cursor()
        conditions: list[str] = []
        params: list[str] = []
        scope = ""
        for column, (label, value) in filters.items():
            where = f" WHERE {' AND '.join(conditions)}" if conditions else ""
            cur.execute(f"SELECT DISTINCT {column} FROM TabularDataWithStrings{where}", params)  # noqa: S608
            options = sorted(str(r[0]) for r in cur.fetchall() if r[0] is not None)
            if value not in options:
                close = closest_names(value, options, n=3)
                msg = f"No tabular {label} '{value}'{scope}." + did_you_mean(close)
                hint = "list_reports() lists them all" if label == "report" else f"Available: {listing(options)}"
                msg = f"{msg} {hint}."
                raise ResultLookupError(msg, suggestions=close, available=options)
            conditions.append(f"{column} = ?")
            params.append(value)
            scope = f" in {label} '{value}'" if not scope else f"{scope}, {label} '{value}'"
        msg = "No tabular data found for " + ", ".join(f"{label}='{value}'" for label, value in filters.values())
        raise ResultLookupError(msg)  # pragma: no cover -- every filter matched, so a row exists

    def list_variables(self) -> list[VariableInfo]:
        """List all available variables in the database.

        Each entry's ``name``, ``key_value`` and ``frequency`` can be passed
        straight to [get_timeseries][idfkit.simulation.parsers.sql.SQLResult.get_timeseries];
        a meter's ``key_value`` is ``""``.

        Returns:
            List of VariableInfo entries describing each variable.
        """
        cur = self._conn.cursor()
        cur.execute(
            "SELECT Name, COALESCE(KeyValue, ''), COALESCE(ReportingFrequency, ''), COALESCE(Units, ''), "
            "IsMeter, COALESCE(Type, '') FROM ReportDataDictionary ORDER BY ReportDataDictionaryIndex"
        )

        return [
            VariableInfo(
                name=str(row[0]),
                key_value=str(row[1]),
                frequency=FREQUENCY_MAP.get(str(row[2]), str(row[2])),
                units=str(row[3]),
                is_meter=bool(row[4]),
                variable_type=str(row[5]),
            )
            for row in cur.fetchall()
        ]

    def list_environments(self) -> list[EnvironmentInfo]:
        """List all environment periods in the database.

        Returns:
            List of EnvironmentInfo entries describing each period (e.g.
            design days and run periods).
        """
        cur = self._conn.cursor()
        cur.execute(
            "SELECT EnvironmentPeriodIndex, EnvironmentName, EnvironmentType "
            "FROM EnvironmentPeriods ORDER BY EnvironmentPeriodIndex"
        )
        return [EnvironmentInfo(index=row[0], name=str(row[1]), environment_type=row[2]) for row in cur.fetchall()]

    def list_reports(self) -> list[str]:
        """List all available tabular report names.

        Returns:
            Sorted list of unique report names.
        """
        cur = self._conn.cursor()
        cur.execute("SELECT DISTINCT ReportName FROM TabularDataWithStrings ORDER BY ReportName")
        return [row[0] for row in cur.fetchall()]

    def to_dataframe(
        self,
        variable_name: str,
        key_value: str = "*",
        frequency: str | None = None,
        environment: Environment | None = None,
    ) -> pd.DataFrame:
        """Retrieve a time series as a pandas DataFrame.

        This is a convenience wrapper around [get_timeseries][idfkit.simulation.parsers.sql.SQLResult.get_timeseries] that
        directly returns a DataFrame.

        Args:
            variable_name: The output variable name.
            key_value: The key value (case-insensitive). The default ``"*"``
                works only when the variable is reported for a single key
                (e.g. site variables and meters); pass the zone or object
                name otherwise.
            frequency: Optional frequency filter. Required when the variable
                is reported at more than one frequency.
            environment: Which environments to read: ``None`` (default) for the
                run periods, or the design days when the run has none;
                ``"annual"``, ``"sizing"`` or ``"all"`` to choose.

        Returns:
            A pandas DataFrame with a ``timestamp`` index.

        Raises:
            ImportError: If pandas is not installed.
            ResultLookupError: If the variable, key or frequency is not found,
                or if several keys or frequencies match (a ``KeyError``
                subclass, as in [get_timeseries][idfkit.simulation.parsers.sql.SQLResult.get_timeseries]).
        """
        ts = self.get_timeseries(variable_name, key_value, frequency, environment)
        return ts.to_dataframe()

    def query(self, sql: str, parameters: tuple[object, ...] = ()) -> list[tuple[object, ...]]:
        """Execute a raw SQL query.

        Args:
            sql: The SQL query string.
            parameters: Query parameters for parameterized queries.

        Returns:
            List of result tuples.
        """
        cur = self._conn.cursor()
        cur.execute(sql, parameters)
        return cur.fetchall()
