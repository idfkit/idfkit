"""Parser for EnergyPlus SQLite output files.

Provides structured access to time-series data, tabular reports, and variable
metadata from the ``eplusout.sql`` database produced by EnergyPlus when
``Output:SQLite`` is present in the model.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

# EnergyPlus uses a fixed reference year for timestamps. 2017 is the canonical
# non-leap year used by convention.
_REFERENCE_YEAR = 2017


@dataclass(frozen=True, slots=True)
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

    def to_dataframe(self) -> Any:
        """Convert to a pandas DataFrame.

        Requires pandas to be installed.

        Returns:
            A DataFrame with a ``timestamp`` index and a column for the values.

        Raises:
            ImportError: If pandas is not installed.
        """
        try:
            import pandas  # type: ignore[import-not-found]
        except ImportError:
            msg = "pandas is required for DataFrame conversion. Install it with: pip install idfkit[dataframes]"
            raise ImportError(msg) from None
        pd: Any = pandas
        return pd.DataFrame(  # type: ignore[no-any-return]
            {"timestamp": list(self.timestamps), self.variable_name: list(self.values)}
        ).set_index("timestamp")

    def plot(self, *, backend: Any = None, title: str | None = None) -> Any:
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
    by an ``IsMeter`` column.  Use the :attr:`is_meter` flag to tell them
    apart.

    For pre-simulation discovery from ``.rdd`` / ``.mdd`` files, see the
    separate :class:`~idfkit.simulation.parsers.rdd.OutputVariable` and
    :class:`~idfkit.simulation.parsers.rdd.OutputMeter` classes instead.

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


# EnergyPlus EnvironmentType values in the EnvironmentPeriods table.
_SIZING_ENV_TYPES = (1, 2)  # DesignDay, DesignRunPeriod
_ANNUAL_ENV_TYPE = 3  # WeatherFileRunPeriod

# Accepted string values for the ``environment`` parameter.
Environment = Literal["sizing", "annual"]


def _make_timestamp(year: int, month: int, day: int, hour: int, minute: int) -> datetime:
    """Build a datetime from EnergyPlus time components.

    EnergyPlus stores Hour=24 to mean midnight of the next day. This function
    handles that edge case, rolling over to the next day at hour 0.

    Args:
        year: Year value from the database (or ``_REFERENCE_YEAR`` fallback).
        month: Month (1-12).
        day: Day of month.
        hour: Hour (0-24, where 24 means next day hour 0).
        minute: Minute (0-59).

    Returns:
        A datetime for the given time components.
    """
    if hour == 24:
        dt = datetime(year, month, day, 0, minute)
        from datetime import timedelta

        dt += timedelta(days=1)
        return dt
    return datetime(year, month, day, hour, minute)


# Mapping from EnergyPlus ReportingFrequency string to a readable label
_FREQUENCY_MAP: dict[str, str] = {
    "TimeStep": "Timestep",
    "Hourly": "Hourly",
    "Daily": "Daily",
    "Monthly": "Monthly",
    "Run Period": "RunPeriod",
    "Annual": "Annual",
}


class SQLResult:
    """Query interface for an EnergyPlus SQLite output database.

    Opens the database in read-only mode and provides methods for retrieving
    time-series data, tabular reports, and variable metadata.

    Can be used as a context manager::

        with SQLResult("eplusout.sql") as sql:
            ts = sql.get_timeseries("Zone Mean Air Temperature", "ZONE 1")
    """

    def __init__(self, db_path: str | Path) -> None:
        """Open the SQLite database in read-only mode.

        Args:
            db_path: Path to the EnergyPlus ``.sql`` output file.
        """
        self._db_path = Path(db_path)
        self._conn = sqlite3.connect(f"file:{self._db_path}?mode=ro", uri=True)

    def close(self) -> None:
        """Close the database connection."""
        self._conn.close()

    def __enter__(self) -> SQLResult:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def get_timeseries(
        self,
        variable_name: str,
        key_value: str = "*",
        frequency: str | None = None,
        environment: Environment | None = None,
    ) -> TimeSeriesResult:
        """Retrieve a time series for a variable.

        Args:
            variable_name: The output variable name.
            key_value: The key value (e.g. zone name). Use ``"*"`` for
                environment-level variables. Case-insensitive matching.
            frequency: Optional frequency filter (e.g. ``"Hourly"``).
            environment: Filter by environment type. ``None`` (default)
                returns all data, ``"annual"`` returns only weather-file
                run period data, and ``"sizing"`` returns only design-day data.

        Returns:
            A TimeSeriesResult with timestamps and values.

        Raises:
            KeyError: If the variable is not found in the database.
            ValueError: If *environment* is not a recognized value.
        """
        cur = self._conn.cursor()

        # Find the matching ReportDataDictionary entry
        query = (
            "SELECT rdd.ReportDataDictionaryIndex, rdd.Name, rdd.KeyValue, rdd.Units "
            "FROM ReportDataDictionary rdd "
            "WHERE rdd.Name = ?"
        )
        params: list[object] = [variable_name]

        if key_value != "*":
            query += " AND UPPER(rdd.KeyValue) = UPPER(?)"
            params.append(key_value)

        if frequency is not None:
            query += " AND rdd.ReportingFrequency = ?"
            params.append(frequency)

        cur.execute(query, params)
        row = cur.fetchone()
        if row is None:
            raise KeyError(f"Variable not found: {variable_name!r} (key={key_value!r})")  # noqa: TRY003

        rdd_index, name, key_val, units = row

        # Get the reporting frequency
        cur.execute(
            "SELECT ReportingFrequency FROM ReportDataDictionary WHERE ReportDataDictionaryIndex = ?",
            (rdd_index,),
        )
        freq_row = cur.fetchone()
        raw_freq: str = str(freq_row[0]) if freq_row else ""
        freq: str = _FREQUENCY_MAP.get(raw_freq, raw_freq) if raw_freq else "Unknown"

        # Retrieve time-series data, filtering out warmup periods.
        # COALESCE handles EnergyPlus versions where WarmupFlag is NULL.
        ts_query = (
            "SELECT t.Year, t.Month, t.Day, t.Hour, t.Minute, rd.Value "
            "FROM ReportData rd "
            "JOIN Time t ON rd.TimeIndex = t.TimeIndex "
        )
        ts_params: list[object] = [rdd_index]
        conditions = [
            "rd.ReportDataDictionaryIndex = ?",
            "COALESCE(t.WarmupFlag, 0) = 0",
        ]

        if environment is not None:
            ts_query += "JOIN EnvironmentPeriods ep ON t.EnvironmentPeriodIndex = ep.EnvironmentPeriodIndex "
            if environment == "sizing":
                conditions.append(f"ep.EnvironmentType IN ({', '.join('?' for _ in _SIZING_ENV_TYPES)})")
                ts_params.extend(_SIZING_ENV_TYPES)
            elif environment == "annual":
                conditions.append("ep.EnvironmentType = ?")
                ts_params.append(_ANNUAL_ENV_TYPE)
            else:
                msg = f"environment must be 'sizing', 'annual', or None, got {environment!r}"
                raise ValueError(msg)

        ts_query += "WHERE " + " AND ".join(conditions) + " ORDER BY t.TimeIndex"
        cur.execute(ts_query, ts_params)

        timestamps: list[datetime] = []
        values: list[float] = []
        for year, month, day, hour, minute, value in cur.fetchall():
            ref_year = year if year and year > 0 else _REFERENCE_YEAR
            timestamps.append(_make_timestamp(ref_year, month, day, hour, minute))
            values.append(float(value))

        return TimeSeriesResult(
            variable_name=name,
            key_value=key_val,
            units=units,
            frequency=freq,
            timestamps=tuple(timestamps),
            values=tuple(values),
        )

    def get_tabular_data(
        self,
        report_name: str | None = None,
        table_name: str | None = None,
    ) -> list[TabularRow]:
        """Retrieve tabular report data.

        Args:
            report_name: Optional filter by report name.
            table_name: Optional filter by table name.

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

    def list_variables(self) -> list[VariableInfo]:
        """List all available variables in the database.

        Returns:
            List of VariableInfo entries describing each variable.
        """
        cur = self._conn.cursor()
        cur.execute("SELECT Name, KeyValue, ReportingFrequency, Units, IsMeter, Type FROM ReportDataDictionary")

        return [
            VariableInfo(
                name=str(row[0]),
                key_value=str(row[1]),
                frequency=_FREQUENCY_MAP.get(str(row[2]), str(row[2])),
                units=str(row[3]),
                is_meter=bool(row[4]),
                variable_type=str(row[5]) if row[5] else "",
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
    ) -> Any:
        """Retrieve a time series as a pandas DataFrame.

        This is a convenience wrapper around :meth:`get_timeseries` that
        directly returns a DataFrame.

        Args:
            variable_name: The output variable name.
            key_value: The key value. Use ``"*"`` for environment-level variables.
            frequency: Optional frequency filter.
            environment: Filter by environment type (``None`` by default
                for all data, ``"annual"`` for run periods, ``"sizing"`` for
                design days).

        Returns:
            A pandas DataFrame with a ``timestamp`` index.

        Raises:
            ImportError: If pandas is not installed.
            KeyError: If the variable is not found.
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
