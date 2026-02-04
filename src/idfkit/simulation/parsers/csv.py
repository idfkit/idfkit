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

# Header format: "KeyValue:VariableName [Units](Frequency)"
# Example: "Environment:Site Outdoor Air Drybulb Temperature [C](Hourly)"
_HEADER_RE = re.compile(r"^(.+?):(.+?)\s*\[([^\]]*)\]\((\w+)\)$")


@dataclass(frozen=True, slots=True)
class CSVColumn:
    """A single data column from a CSV output file.

    Attributes:
        header: The raw column header string.
        variable_name: Parsed variable name.
        key_value: Parsed key value (e.g. ``"Environment"``).
        units: Parsed units string.
        values: The numeric values for this column.
    """

    header: str
    variable_name: str
    key_value: str
    units: str
    values: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class CSVResult:
    """Parsed EnergyPlus CSV output file.

    Attributes:
        timestamps: The timestamp strings from the Date/Time column.
        columns: Parsed data columns with extracted metadata.
    """

    timestamps: tuple[str, ...]
    columns: tuple[CSVColumn, ...]

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
            for i, val in enumerate(row[1:]):
                if i < len(col_values):
                    try:
                        col_values[i].append(float(val.strip()))
                    except ValueError:
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

    def get_column(self, variable_name: str, key_value: str | None = None) -> CSVColumn | None:
        """Find a column by variable name and optional key value.

        Args:
            variable_name: The variable name to search for (case-insensitive).
            key_value: Optional key value filter (case-insensitive).

        Returns:
            The matching CSVColumn, or None if not found.
        """
        name_lower = variable_name.lower()
        for col in self.columns:
            if col.variable_name.lower() == name_lower and (
                key_value is None or col.key_value.lower() == key_value.lower()
            ):
                return col
        return None
