"""Parser for EnergyPlus CSV output files.

Parses CSV files produced by ReadVarsESO (via ``--readvars`` flag) into
structured columns with extracted variable metadata.
"""

from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass
from pathlib import Path

from ._lookup import resolve_series
from ._timeutil import summarize_series

__all__ = [
    "CSVColumn",
    "CSVResult",
]

# Header format: "KeyValue:VariableName [Units](Frequency)"
# Example: "Environment:Site Outdoor Air Drybulb Temperature [C](Hourly)"
_HEADER_RE = re.compile(r"^(.+?):(.+?)\s*\[([^\]]*)\]\((\w+)\)$")


@dataclass(frozen=True, slots=True, repr=False)
class CSVColumn:
    """A single data column from a CSV output file.

    Attributes:
        header: The raw column header string.
        variable_name: Parsed variable name.
        key_value: Parsed key value (e.g. ``"Environment"``).
        units: Parsed units string.
        values: The numeric values for this column, across every environment
            in the file (design days, then run periods), in run order.
        frequency: Parsed reporting frequency (e.g. ``"Hourly"``); empty when
            the header carries none.
    """

    header: str
    variable_name: str
    key_value: str
    units: str
    values: tuple[float, ...]
    frequency: str = ""

    def __repr__(self) -> str:
        # A summary, not the data: one hourly annual column would otherwise print every value.
        return f"CSVColumn({self.header!r}, {summarize_series(None, self.values)})"


@dataclass(frozen=True, slots=True, repr=False)
class CSVResult:
    """Parsed EnergyPlus CSV output file.

    The CSV file that ReadVarsESO writes carries no environment markers, so
    every series spans **every** environment the run simulated, joined in run
    order: the sizing design days first, then the weather run period(s). A
    day-of-year index or an annual sum over a column therefore counts the
    design days too. To read a single environment, use
    [SQLResult.get_timeseries][idfkit.simulation.parsers.sql.SQLResult.get_timeseries]
    (``result.sql``), which reads the run period by default, or
    [ESOResult.get_column][idfkit.simulation.parsers.eso.ESOResult.get_column]
    (``result.eso``), which takes ``environment_index=``.

    Attributes:
        timestamps: The timestamp strings from the Date/Time column.
        columns: Parsed data columns with extracted metadata.
    """

    timestamps: tuple[str, ...]
    columns: tuple[CSVColumn, ...]

    def __repr__(self) -> str:
        span = f", {self.timestamps[0].strip()} .. {self.timestamps[-1].strip()}" if self.timestamps else ""
        return f"CSVResult({len(self.timestamps)} rows, {len(self.columns)} columns{span})"

    @classmethod
    def from_file(cls, path: str | Path) -> CSVResult:
        """Parse a CSV output file from disk.

        Args:
            path: Path to the CSV file.

        Returns:
            Parsed CSVResult.
        """
        text = Path(path).read_text(encoding="latin-1")
        return cls.from_string(text)

    @classmethod
    def from_string(cls, text: str) -> CSVResult:
        """Parse CSV output from a string.

        Args:
            text: Raw CSV file contents.

        Returns:
            Parsed CSVResult.
        """
        reader = csv.reader(io.StringIO(text))
        headers = next(reader, None)
        if headers is None:
            return cls(timestamps=(), columns=())

        # First column is Date/Time
        data_headers = [h.strip() for h in headers[1:]]

        timestamps: list[str] = []
        col_values: list[list[float]] = [[] for _ in data_headers]

        for row in reader:
            if not row or not row[0].strip():
                continue
            timestamps.append(row[0].strip())
            data_cells = row[1:]
            for i in range(len(col_values)):
                if i < len(data_cells):
                    try:
                        col_values[i].append(float(data_cells[i].strip()))
                    except ValueError:
                        col_values[i].append(0.0)
                else:
                    # Short row: pad missing columns with 0.0 to keep
                    # all column value lists aligned with timestamps.
                    col_values[i].append(0.0)

        columns: list[CSVColumn] = []
        for header, values in zip(data_headers, col_values, strict=False):
            m = _HEADER_RE.match(header)
            if m:
                columns.append(
                    CSVColumn(
                        header=header,
                        variable_name=m.group(2).strip(),
                        key_value=m.group(1).strip(),
                        units=m.group(3).strip(),
                        values=tuple(values),
                        frequency=m.group(4),
                    )
                )
            else:
                columns.append(
                    CSVColumn(
                        header=header,
                        variable_name=header,
                        key_value="",
                        units="",
                        values=tuple(values),
                    )
                )

        return cls(timestamps=tuple(timestamps), columns=tuple(columns))

    def get_column(self, variable_name: str, key_value: str | None = None, frequency: str | None = None) -> CSVColumn:
        """Find the one column reported for a variable, key and frequency.

        The lookup must resolve to one column, as
        [SQLResult.get_timeseries][idfkit.simulation.parsers.sql.SQLResult.get_timeseries]
        does: when a variable is reported for several keys (one per zone, say) or
        at several frequencies, name the one you want, and the error lists them.

        Unlike the SQL and ESO readers, it cannot select an environment: the CSV
        file has no explicit environment markers and this parser does not split
        environments, so the column holds every environment the run simulated
        (design days and run period) joined end to end. For one environment, read
        ``result.sql`` (run period by default) or
        ``result.eso.get_column(..., environment_index=...)``.

        Args:
            variable_name: The variable name to search for (case-insensitive).
                A meter is found by its full name (``"Electricity:Facility"``),
                and reports no key.
            key_value: Key value (case-insensitive). Needed only when the
                variable is reported for more than one key.
            frequency: Frequency (e.g. ``"Hourly"``). Needed only when the
                variable is reported at more than one frequency.

        Returns:
            The matching CSVColumn. Its values span every environment in the
            file, in run order (design days, then run periods). The parser
            does not split them; only the Date/Time column, where the date
            jumps back at each new environment, hints at the boundaries.

        Raises:
            ResultLookupError: A ``KeyError`` subclass, if the variable, key or
                frequency is not in the file (with the closest names and the
                reported keys), or if several keys or frequencies match.
        """
        hint = " Request it with an Output:Variable (or Output:Meter) object."
        folded = variable_name.casefold()
        if ":" in variable_name and not any(c.variable_name.casefold() == folded for c in self.columns):
            # A meter header ("Electricity:Facility [J](Hourly)") has no key, but the
            # header parser splits it at the first colon. Match a colon-bearing name on
            # the whole "key:variable" text instead, with no key, as ESO and SQL do.
            return resolve_series(
                self.columns,
                variable_name,
                key_value,
                frequency,
                name_of=_full_name,
                key_of=lambda c: "",
                frequency_of=lambda c: c.frequency,
                not_found_hint=hint,
            )
        return resolve_series(
            self.columns,
            variable_name,
            key_value,
            frequency,
            name_of=lambda c: c.variable_name,
            key_of=lambda c: c.key_value,
            frequency_of=lambda c: c.frequency,
            not_found_hint=hint,
        )


def _full_name(column: CSVColumn) -> str:
    """The column's ``key:variable`` text, which for a meter column is the meter's name."""
    return f"{column.key_value}:{column.variable_name}" if column.key_value else column.variable_name
