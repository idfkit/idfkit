"""Parser for EnergyPlus HTML tabular output files.

EnergyPlus produces an HTML file (``eplustbl.htm`` by default) containing
all tabular report summaries.  This module parses those tables into
structured Python data, providing an API compatible with eppy's
``readhtml`` module while being more convenient.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class HTMLTable:
    """A single table extracted from the EnergyPlus HTML output.

    Attributes:
        title: The bold title preceding the table (e.g.
            ``"Site and Source Energy"``).
        header: Column headers (first ``<tr>`` with ``<th>`` cells).
        rows: Data rows as lists of strings.
        report_name: The top-level report name (e.g.
            ``"Annual Building Utility Performance Summary"``).
        for_string: The ``"For:"`` qualifier (e.g. ``"Entire Facility"``).
    """

    title: str
    header: list[str]
    rows: list[list[str]]
    report_name: str = ""
    for_string: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to a dict mapping row headers to {col_header: value}.

        The first column is treated as the row key.  Remaining columns
        are keyed by the column headers.  This gives convenient
        dict-style access similar to ``readhtml.named_grid_h``.
        """
        result: dict[str, dict[str, str]] = {}
        for row in self.rows:
            if not row:
                continue
            row_key = row[0]
            entry: dict[str, str] = {}
            for i, hdr in enumerate(self.header):
                if i < len(row):
                    entry[hdr] = row[i]
            result[row_key] = entry
        return result


@dataclass(slots=True)
class HTMLResult:
    """Parsed HTML tabular output from an EnergyPlus simulation.

    Attributes:
        tables: All tables extracted from the file, in document order.
    """

    tables: list[HTMLTable] = field(default_factory=lambda: [])

    @classmethod
    def from_file(cls, path: Path | str, encoding: str = "latin-1") -> HTMLResult:
        """Parse an EnergyPlus HTML output file.

        Args:
            path: Path to the HTML file (typically ``eplustblTable.html``
                or ``eplusoutTable.html``).
            encoding: File encoding (default ``latin-1``).

        Returns:
            Parsed :class:`HTMLResult`.
        """
        with open(path, encoding=encoding, errors="replace") as f:
            return cls.from_string(f.read())

    @classmethod
    def from_string(cls, html: str) -> HTMLResult:
        """Parse an HTML string.

        Args:
            html: The raw HTML content.

        Returns:
            Parsed :class:`HTMLResult`.
        """
        parser = _EnergyPlusHTMLParser()
        parser.feed(html)
        return cls(tables=parser.tables)

    def __len__(self) -> int:
        return len(self.tables)

    def __getitem__(self, index: int) -> HTMLTable:
        return self.tables[index]

    def __iter__(self):  # type: ignore[override]
        return iter(self.tables)

    # ------------------------------------------------------------------
    # Convenience accessors (eppy-compatible patterns)
    # ------------------------------------------------------------------

    def titletable(self) -> list[tuple[str, list[list[str]]]]:
        """Return ``(title, rows)`` pairs like eppy's ``readhtml.titletable``.

        Each entry is ``(bold_title, [header_row, *data_rows])``.
        """
        result: list[tuple[str, list[list[str]]]] = []
        for t in self.tables:
            combined = [t.header, *t.rows] if t.header else list(t.rows)
            result.append((t.title, combined))
        return result

    def tablebyname(self, name: str) -> HTMLTable | None:
        """Find first table whose title contains *name* (case-insensitive)."""
        lower = name.lower()
        for t in self.tables:
            if lower in t.title.lower():
                return t
        return None

    def tablebyindex(self, index: int) -> HTMLTable | None:
        """Get a table by its zero-based position."""
        if 0 <= index < len(self.tables):
            return self.tables[index]
        return None

    def tablesbyreport(self, report_name: str) -> list[HTMLTable]:
        """Get all tables belonging to a specific report."""
        lower = report_name.lower()
        return [t for t in self.tables if lower in t.report_name.lower()]


# ---------------------------------------------------------------------------
# Internal HTML parser
# ---------------------------------------------------------------------------

# Tags that indicate "bold title" text in EnergyPlus output
_BOLD_TAGS = {"b", "strong"}


class _EnergyPlusHTMLParser(HTMLParser):
    """Low-level HTML parser for EnergyPlus tabular output."""

    def __init__(self) -> None:
        super().__init__()
        self.tables: list[HTMLTable] = []

        # State tracking
        self._in_table = False
        self._in_row = False
        self._in_cell = False
        self._in_header_cell = False
        self._in_bold = False

        # Accumulators
        self._current_cell_text = ""
        self._current_row: list[str] = []
        self._current_header: list[str] = []
        self._current_rows: list[list[str]] = []
        self._is_header_row = False

        # Title tracking
        self._bold_text = ""
        self._last_title = ""
        self._report_name = ""
        self._for_string = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()

        if tag == "table":
            self._in_table = True
            self._current_header = []
            self._current_rows = []

        elif tag == "tr":
            self._in_row = True
            self._current_row = []
            self._is_header_row = False

        elif tag == "th":
            self._in_cell = True
            self._in_header_cell = True
            self._current_cell_text = ""
            self._is_header_row = True

        elif tag == "td":
            self._in_cell = True
            self._in_header_cell = False
            self._current_cell_text = ""

        elif tag in _BOLD_TAGS:
            self._in_bold = True
            self._bold_text = ""

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()

        if tag == "table":
            if self._current_header or self._current_rows:
                table = HTMLTable(
                    title=self._last_title.strip(),
                    header=self._current_header,
                    rows=self._current_rows,
                    report_name=self._report_name,
                    for_string=self._for_string,
                )
                self.tables.append(table)
            self._in_table = False

        elif tag == "tr":
            if self._in_table:
                if self._is_header_row and not self._current_header:
                    self._current_header = self._current_row
                else:
                    if self._current_row:
                        self._current_rows.append(self._current_row)
            self._in_row = False

        elif tag in ("td", "th"):
            text = self._current_cell_text.strip()
            text = re.sub(r"\s+", " ", text)
            self._current_row.append(text)
            self._in_cell = False
            self._in_header_cell = False

        elif tag in _BOLD_TAGS:
            if self._in_bold and not self._in_table:
                trimmed = self._bold_text.strip()
                if trimmed:
                    self._last_title = trimmed
                    # Detect report-level headers vs table-level titles
                    if trimmed.endswith("Summary") or trimmed.endswith("Report"):
                        self._report_name = trimmed
                    elif trimmed.startswith("For:"):
                        self._for_string = trimmed[4:].strip()
            self._in_bold = False

    def handle_data(self, data: str) -> None:
        if self._in_cell:
            self._current_cell_text += data
        if self._in_bold:
            self._bold_text += data
