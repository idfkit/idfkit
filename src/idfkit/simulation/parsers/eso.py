"""High-performance parser for EnergyPlus ESO/MTR standard-output files.

The ``.eso`` (Standard Output) and ``.mtr`` (Meter Output) files share an
identical grammar: a *data dictionary* mapping integer report ids to variable
metadata, followed by a *data section* of ``id,value`` records interleaved with
time/environment marker lines, terminated by ``End of Data``.

This parser is built for speed without leaving the standard library:

- It works on **bytes** and never decodes the (large) data section to ``str``.
- The data **dictionary is parsed eagerly** (cheap — at most a few hundred
  lines); the **data section is parsed lazily**. Asking for one variable runs a
  single scan that float-parses *only that variable's* lines, skipping every
  other record with a prefix test — so reading a handful of variables out of a
  large file does not pay to parse the whole file.
- An ``eager=True`` mode (or accessing ``ESOResult.columns``) materializes
  every variable in one pass, accumulating values into compact
  ``array.array`` buffers.

Example:
    >>> from idfkit.simulation.parsers.eso import ESOResult
    >>> eso = ESOResult.from_file("eplusout.eso")          # doctest: +SKIP
    >>> col = eso.get_column("Zone Mean Air Temperature", "ZONE ONE")  # doctest: +SKIP
    >>> col.values[:3]                                     # doctest: +SKIP
    (21.3, 21.1, 20.9)
"""

from __future__ import annotations

import re
from array import array
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from ._timeutil import FREQUENCY_MAP, REFERENCE_YEAR, make_timestamp

if TYPE_CHECKING:
    import pandas as pd

    from ..plotting import PlotBackend

# Report ids 1-6 are reserved time/environment markers in every ESO/MTR file;
# user variables start at id 7.
_ENV_MARKER = 1  # Environment Title, Latitude, Longitude, Time Zone, Elevation
_TIMESTEP_MARKER = 2  # Day of Sim, Month, Day, DST, Hour, StartMinute, EndMinute, DayType
_DAILY_MARKER = 3  # Cumulative Day, Month, Day of Month, DST, DayType
_MONTHLY_MARKER = 4  # Cumulative Days, Month
_RUNPERIOD_MARKER = 5  # Cumulative Days
_ANNUAL_MARKER = 6  # Calendar Year
_MARKER_IDS = frozenset((1, 2, 3, 4, 5, 6))

# Maps a normalized frequency label to the marker id that carries its timestamps.
_FREQ_TO_MARKER: dict[str, int] = {
    "Timestep": _TIMESTEP_MARKER,
    "Hourly": _TIMESTEP_MARKER,
    "Daily": _DAILY_MARKER,
    "Monthly": _MONTHLY_MARKER,
    "RunPeriod": _RUNPERIOD_MARKER,
    "Annual": _ANNUAL_MARKER,
}

# Dictionary line: "ReportID,NumValues,[KeyValue,]VariableName [Units] !Frequency [extra]".
# The "!"+word frequency token distinguishes a real variable line from the
# reserved marker comment lines ("... ! When Daily Report Variables Requested"),
# whose "!" is followed by a space.
_DICT_RE = re.compile(r"^(\d+),(\d+),(.+?)\s*\[([^\]]*)\]\s*!(\w+)")

_END_OF_DATA = b"End of Data"
_END_OF_DICT = b"End of Data Dictionary"


@dataclass(frozen=True, slots=True)
class ESOVariable:
    """A reporting variable declared in an ESO/MTR data dictionary.

    Attributes:
        report_id: The integer id that prefixes this variable's data records.
        variable_name: The output variable or meter name.
        key_value: The key (e.g. zone or surface name); empty for meters.
        units: The variable units (may be empty).
        frequency: Normalized reporting frequency (``"Hourly"``, ``"Daily"`` …).
        num_values: Number of numeric values each data record carries (1 for
            detailed/hourly; more for aggregated daily/monthly min/max records).
    """

    report_id: int
    variable_name: str
    key_value: str
    units: str
    frequency: str
    num_values: int


@dataclass(frozen=True, slots=True)
class ESOEnvironment:
    """One environment period (design day or run period) within the file.

    Environments appear in the order EnergyPlus ran them: sizing design days
    first (in IDF order), then the weather run period(s). ``index`` is that
    0-based order and is exactly the value used by ``environment_index``
    everywhere else (``ESOResult.get_column`` and
    ``ESOColumn.environment_index``); ``title`` is the human-readable name.
    To learn which index is which design day, read ``ESOResult.environments``
    and match on ``title`` — EnergyPlus does not encode an environment *type*
    code in the ESO format, so the title is the only discriminator (e.g.
    ``"... ANN HTG 99% CONDNS DB"`` vs ``"RUN PERIOD 1"``).

    Attributes:
        index: 0-based order of appearance; pass it as ``environment_index``.
        title: The environment title from the ``1,...`` marker line, e.g.
            ``"DENVER ... ANN HTG 99% CONDNS DB"`` or ``"RUN PERIOD 1"``.
        latitude: Site latitude in degrees.
        longitude: Site longitude in degrees.
        time_zone: Site time zone in hours from GMT.
        elevation: Site elevation in metres.
    """

    index: int
    title: str
    latitude: float
    longitude: float
    time_zone: float
    elevation: float


@dataclass(frozen=True, slots=True)
class ESOColumn:
    """One variable's time series within a single environment.

    Attributes:
        variable: The [ESOVariable][idfkit.simulation.parsers.eso.ESOVariable] this column belongs to.
        environment_index: Index of the environment these values belong to.
            Look it up in ``ESOResult.environments`` to get the design-day /
            run-period title: ``result.environments[col.environment_index].title``.
        timestamps: Timestamp for each data point.
        values: The reported value for each data point (the primary value for
            aggregated daily/monthly records).
    """

    variable: ESOVariable
    environment_index: int
    timestamps: tuple[datetime, ...]
    values: tuple[float, ...]

    def to_dataframe(self) -> pd.DataFrame:
        """Convert to a pandas DataFrame.

        Returns:
            A DataFrame with a ``timestamp`` index and a column named after the
            variable.

        Raises:
            ImportError: If pandas is not installed.
        """
        try:
            import pandas as _pd  # type: ignore[import-not-found]
        except ImportError:
            msg = "pandas is required for DataFrame conversion. Install it with: pip install idfkit[dataframes]"
            raise ImportError(msg) from None
        return _pd.DataFrame(  # type: ignore[no-any-return]
            {"timestamp": list(self.timestamps), self.variable.variable_name: list(self.values)}
        ).set_index("timestamp")

    def plot(self, *, backend: PlotBackend | None = None, title: str | None = None) -> Any:
        """Plot this time series as a line chart.

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
        var = self.variable
        plot_title = title or (f"{var.key_value}: {var.variable_name}" if var.key_value else var.variable_name)
        return backend.line(
            list(self.timestamps),
            list(self.values),
            title=plot_title,
            xlabel="Time",
            ylabel=f"{var.variable_name} ({var.units})" if var.units else var.variable_name,
            label=var.key_value or var.variable_name,
        )


def _parse_dictionary(data: bytes) -> tuple[str, dict[int, ESOVariable], int]:
    """Parse the data-dictionary section. Returns (program_version, by_id, data_start)."""
    end = data.find(_END_OF_DICT)
    if end == -1:
        # No dictionary terminator: treat the whole file as header.
        header = data
        data_start = len(data)
    else:
        header = data[:end]
        nl = data.find(b"\n", end)
        data_start = nl + 1 if nl != -1 else len(data)

    program_version = ""
    by_id: dict[int, ESOVariable] = {}
    for raw in header.split(b"\n"):
        line = raw.decode("latin-1").strip()
        if not line:
            continue
        if line.startswith("Program Version"):
            program_version = line
            continue
        comma = line.find(",")
        if comma == -1:
            continue
        try:
            report_id = int(line[:comma])
        except ValueError:
            continue
        if report_id in _MARKER_IDS:
            continue  # reserved time/environment markers — not user variables
        match = _DICT_RE.match(line)
        if match is None:
            continue
        num_values = int(match.group(2))
        body = match.group(3)
        units = match.group(4).strip()
        frequency = FREQUENCY_MAP.get(match.group(5), match.group(5))
        # body is "KeyValue,VariableName" for variables, or "VariableName" for meters.
        body_comma = body.find(",")
        if body_comma == -1:
            key_value = ""
            variable_name = body.strip()
        else:
            key_value = body[:body_comma].strip()
            variable_name = body[body_comma + 1 :].strip()
        by_id[report_id] = ESOVariable(report_id, variable_name, key_value, units, frequency, num_values)
    return program_version, by_id, data_start


def _marker_timestamp(marker: int, fields: list[bytes]) -> datetime:
    """Build a timestamp from a marker line's comma-split fields."""
    try:
        if marker == _TIMESTEP_MARKER:
            month = int(fields[2])
            day = int(fields[3])
            hour = int(fields[5])
            end_minute = int(float(fields[7]))
            minute = 0 if end_minute >= 60 else end_minute
            return make_timestamp(REFERENCE_YEAR, month, day, hour, minute)
        if marker == _DAILY_MARKER:
            return datetime(REFERENCE_YEAR, int(fields[2]), int(fields[3]))
        if marker == _MONTHLY_MARKER:
            return datetime(REFERENCE_YEAR, int(fields[2]), 1)
        if marker == _ANNUAL_MARKER:
            year = int(fields[1])
            return datetime(year if year > 0 else REFERENCE_YEAR, 1, 1)
    except (ValueError, IndexError):
        pass
    return datetime(REFERENCE_YEAR, 1, 1)


def _parse_environment(index: int, fields: list[bytes]) -> ESOEnvironment:
    """Parse a ``1,Title,Lat,Long,TZ,Elev`` environment marker line.

    The title is read as everything between the id and the trailing four
    numeric fields, so titles containing commas are handled.
    """
    try:
        latitude = float(fields[-4])
        longitude = float(fields[-3])
        time_zone = float(fields[-2])
        elevation = float(fields[-1])
        title = b",".join(fields[1:-4]).decode("latin-1").strip()
    except (ValueError, IndexError):
        title = b",".join(fields[1:]).decode("latin-1").strip()
        latitude = longitude = time_zone = elevation = 0.0
    return ESOEnvironment(index, title, latitude, longitude, time_zone, elevation)


class ESOResult:
    """Parsed EnergyPlus ``.eso`` / ``.mtr`` output file.

    The data dictionary is parsed on construction; the data section is scanned
    lazily on demand (see `get_column`). Pass ``eager=True`` to materialize
    every column up front.

    A file usually contains several *environments* — the sizing design days
    followed by the weather run period. `get_column` returns the last one
    (the run period) by default. To target a specific design day, read
    `environments` to map each ``index`` to its ``title`` and pass that index
    as ``environment_index``:

    ```python
    eso = ESOResult.from_file("eplusout.eso")
    for env in eso.environments:
        print(env.index, env.title)
    # 0  DENVER ... ANN HTG 99% CONDNS DB
    # 1  DENVER ... ANN CLG 1% CONDNS DB=>MWB
    # 2  RUN PERIOD 1

    # the heating design day is index 0:
    col = eso.get_column("Zone Mean Air Temperature", "ZONE ONE", environment_index=0)
    ```

    Attributes:
        program_version: The ``Program Version`` header line.
        variables: All variables declared in the data dictionary.
    """

    __slots__ = (
        "_by_id",
        "_data",
        "_data_start",
        "_eager_columns",
        "_env_cache",
        "_scan_cache",
        "program_version",
        "variables",
    )

    def __init__(self, data: bytes, *, eager: bool = False) -> None:
        # Normalize line endings once so the hot loops only deal with "\n".
        if b"\r\n" in data:
            data = data.replace(b"\r\n", b"\n")
        self._data = data
        self.program_version, self._by_id, self._data_start = _parse_dictionary(data)
        self.variables: tuple[ESOVariable, ...] = tuple(self._by_id.values())
        self._env_cache: tuple[ESOEnvironment, ...] | None = None
        self._scan_cache: dict[int, tuple[ESOColumn, ...]] = {}
        self._eager_columns: tuple[ESOColumn, ...] | None = None
        if eager:
            self._eager_columns = self._scan_all()

    @classmethod
    def from_bytes(cls, data: bytes, *, eager: bool = False) -> ESOResult:
        """Parse an ESO/MTR file from raw bytes (the fastest entry point)."""
        return cls(data, eager=eager)

    @classmethod
    def from_file(cls, path: str | Path, *, eager: bool = False) -> ESOResult:
        """Parse an ESO/MTR file from disk."""
        return cls(Path(path).read_bytes(), eager=eager)

    @classmethod
    def from_string(cls, text: str, *, eager: bool = False) -> ESOResult:
        """Parse ESO/MTR content from a string."""
        return cls(text.encode("latin-1"), eager=eager)

    @property
    def environments(self) -> tuple[ESOEnvironment, ...]:
        """All environment periods in the file (lazily scanned and cached).

        This is the index → title map for ``environment_index``: each
        [ESOEnvironment][idfkit.simulation.parsers.eso.ESOEnvironment] has an
        ``index`` (use it as ``environment_index`` in ``get_column``) and a
        ``title`` (the design-day / run-period name).
        """
        if self._env_cache is None:
            self._env_cache = self._scan_environments()
        return self._env_cache

    @property
    def columns(self) -> tuple[ESOColumn, ...]:
        """Every variable's time series across all environments (full parse).

        Accessing this triggers (and caches) a full parse of the data section.
        """
        if self._eager_columns is None:
            self._eager_columns = self._scan_all()
        return self._eager_columns

    def get_variable(
        self, variable_name: str, key_value: str | None = None, frequency: str | None = None
    ) -> ESOVariable | None:
        """Find a declared variable by name (case-insensitive) and optional key/frequency."""
        name_lower = variable_name.lower()
        for var in self.variables:
            if (
                var.variable_name.lower() == name_lower
                and (key_value is None or var.key_value.lower() == key_value.lower())
                and (frequency is None or var.frequency.lower() == frequency.lower())
            ):
                return var
        return None

    def get_column(
        self,
        variable_name: str,
        key_value: str | None = None,
        frequency: str | None = None,
        environment_index: int | None = None,
    ) -> ESOColumn | None:
        """Extract one variable's time series with a single targeted scan.

        Args:
            variable_name: Variable name to look up (case-insensitive).
            key_value: Optional key value filter (e.g. zone name).
            frequency: Optional frequency filter (e.g. ``"Hourly"``).
            environment_index: Which environment to return. Defaults to the last
                environment in the file (typically the run period), mirroring the
                most common intent. To pick a specific design day, find its index
                by title in ``environments`` (e.g.
                ``next(e.index for e in eso.environments if "HTG" in e.title)``)
                and pass it here.

        Returns:
            The matching [ESOColumn][idfkit.simulation.parsers.eso.ESOColumn], or
            ``None`` if the variable is not found or has no data. The returned
            column's ``environment_index`` cross-references back to ``environments``.
        """
        var = self.get_variable(variable_name, key_value, frequency)
        if var is None:
            return None
        cols = self._scan_variable(var.report_id)
        if not cols:
            return None
        if environment_index is None:
            return cols[-1]
        for col in cols:
            if col.environment_index == environment_index:
                return col
        return None

    def to_dataframe(
        self,
        variable_name: str,
        key_value: str | None = None,
        frequency: str | None = None,
        environment_index: int | None = None,
    ) -> pd.DataFrame:
        """Extract a variable and return it as a pandas DataFrame.

        Raises:
            KeyError: If the variable is not found.
            ImportError: If pandas is not installed.
        """
        col = self.get_column(variable_name, key_value, frequency, environment_index)
        if col is None:
            msg = f"Variable not found: {variable_name!r}"
            raise KeyError(msg)
        return col.to_dataframe()

    # -- internal scans ----------------------------------------------------

    def _scan_variable(self, report_id: int) -> tuple[ESOColumn, ...]:  # noqa: C901
        """Single targeted scan that float-parses only ``report_id``'s records."""
        cached = self._scan_cache.get(report_id)
        if cached is not None:
            return cached

        var = self._by_id[report_id]
        marker = _FREQ_TO_MARKER.get(var.frequency, _TIMESTEP_MARKER)
        data = self._data
        find = data.find
        startswith = data.startswith
        n = len(data)

        target_prefix = f"{report_id},".encode("latin-1")
        target_comma = len(target_prefix) - 1  # offset of the id's trailing comma
        env_prefix = b"1,"
        marker_prefix = f"{marker},".encode("latin-1")

        columns: list[ESOColumn] = []
        environments: list[ESOEnvironment] = []
        env_index = -1
        current_ts: datetime | None = None
        timestamps: list[datetime] = []
        values = array("d")

        # A single guard around the whole loop (not per line, so zero hot-loop
        # overhead) makes a truncated/garbled tail degrade gracefully: we stop
        # and keep whatever was parsed cleanly.
        start = self._data_start
        try:
            while start < n:
                end = find(b"\n", start)
                if end == -1:
                    end = n
                if startswith(target_prefix, start):
                    comma = start + target_comma
                    value_end = find(b",", comma + 1, end)
                    if value_end == -1:
                        value_end = end
                    values.append(float(data[comma + 1 : value_end]))
                    # current_ts is set by this variable's frequency marker; fall back
                    # to a stable sentinel if a value precedes any marker.
                    timestamps.append(current_ts if current_ts is not None else datetime(REFERENCE_YEAR, 1, 1))
                elif startswith(env_prefix, start):
                    if values:
                        columns.append(ESOColumn(var, env_index, tuple(timestamps[: len(values)]), tuple(values)))
                    env_index += 1
                    environments.append(_parse_environment(env_index, data[start:end].split(b",")))
                    timestamps = []
                    values = array("d")
                    current_ts = None
                elif startswith(marker_prefix, start):
                    current_ts = _marker_timestamp(marker, data[start:end].split(b","))
                start = end + 1
        except (ValueError, IndexError):
            pass

        if values:
            columns.append(ESOColumn(var, env_index, tuple(timestamps[: len(values)]), tuple(values)))

        if self._env_cache is None and environments:
            self._env_cache = tuple(environments)
        result = tuple(columns)
        self._scan_cache[report_id] = result
        return result

    def _scan_environments(self) -> tuple[ESOEnvironment, ...]:
        """Cheap scan that enumerates only the ``1,...`` environment markers."""
        data = self._data
        find = data.find
        startswith = data.startswith
        n = len(data)
        environments: list[ESOEnvironment] = []
        index = -1
        start = self._data_start
        while start < n:
            end = find(b"\n", start)
            if end == -1:
                end = n
            if startswith(b"1,", start):
                index += 1
                environments.append(_parse_environment(index, data[start:end].split(b",")))
            start = end + 1
        return tuple(environments)

    def _scan_all(self) -> tuple[ESOColumn, ...]:  # noqa: C901
        """Full single pass that materializes every variable's columns."""
        data = self._data
        find = data.find
        n = len(data)
        by_id = self._by_id
        var_marker = {rid: _FREQ_TO_MARKER.get(v.frequency, _TIMESTEP_MARKER) for rid, v in by_id.items()}

        columns: list[ESOColumn] = []
        environments: list[ESOEnvironment] = []
        env_index = -1
        ts_by_marker: dict[int, list[datetime]] = {}
        values_by_id: dict[int, array[float]] = {}

        def _flush() -> None:
            for rid, arr in values_by_id.items():
                if not arr:
                    continue
                ts = ts_by_marker.get(var_marker[rid], [])
                # Trim timestamps to the value count so a truncated final
                # record cannot misalign the column.
                columns.append(ESOColumn(by_id[rid], env_index, tuple(ts[: len(arr)]), tuple(arr)))

        # One guard around the whole loop keeps a truncated tail from raising.
        start = self._data_start
        try:
            while start < n:
                end = find(b"\n", start)
                if end == -1:
                    end = n
                comma = find(b",", start, end)
                if comma == -1:
                    if data[start:end].lstrip().startswith(_END_OF_DATA):
                        break
                    start = end + 1
                    continue
                try:
                    report_id = int(data[start:comma])
                except ValueError:
                    start = end + 1
                    continue
                if report_id == _ENV_MARKER:
                    _flush()
                    env_index += 1
                    environments.append(_parse_environment(env_index, data[start:end].split(b",")))
                    ts_by_marker = {}
                    values_by_id = {rid: array("d") for rid in by_id}
                elif report_id in _MARKER_IDS:
                    lst = ts_by_marker.get(report_id)
                    if lst is None:
                        lst = []
                        ts_by_marker[report_id] = lst
                    lst.append(_marker_timestamp(report_id, data[start:end].split(b",")))
                else:
                    arr = values_by_id.get(report_id)
                    if arr is None:
                        start = end + 1
                        continue
                    value_end = find(b",", comma + 1, end)
                    if value_end == -1:
                        value_end = end
                    arr.append(float(data[comma + 1 : value_end]))
                start = end + 1
        except (ValueError, IndexError):
            pass
        _flush()

        if self._env_cache is None:
            self._env_cache = tuple(environments)
        return tuple(columns)
