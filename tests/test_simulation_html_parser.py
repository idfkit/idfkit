"""Tests for the EnergyPlus HTML tabular output parser."""

from __future__ import annotations

from pathlib import Path

import pytest

from idfkit.simulation.parsers.html import HTMLResult, HTMLTable

# ---------------------------------------------------------------------------
# Sample HTML fixture
# ---------------------------------------------------------------------------

_SAMPLE_HTML = """\
<html>
<body>
<b>Annual Building Utility Performance Summary</b>
<b>For: Entire Facility</b>
<b>Site and Source Energy</b>
<table>
  <tr><th>Resource</th><th>Total Energy</th><th>Energy Per Area</th></tr>
  <tr><td>Electricity</td><td>12.50</td><td>3.40</td></tr>
  <tr><td>Gas</td><td>8.30</td><td>2.20</td></tr>
</table>
<b>End Uses</b>
<table>
  <tr><th>End Use</th><th>Electricity</th><th>Gas</th></tr>
  <tr><td>Heating</td><td>0.0</td><td>8.30</td></tr>
  <tr><td>Cooling</td><td>5.20</td><td>0.0</td></tr>
</table>
<b>Envelope Summary</b>
<b>Opaque Components</b>
<table>
  <tr><th>Component</th><th>U-Factor</th></tr>
  <tr><td>Wall 1</td><td>0.35</td></tr>
</table>
</body>
</html>
"""

# Minimal HTML with no tables
_EMPTY_HTML = "<html><body><p>No tables here.</p></body></html>"


@pytest.fixture()
def parsed() -> HTMLResult:
    return HTMLResult.from_string(_SAMPLE_HTML)


# ---------------------------------------------------------------------------
# from_string / from_file
# ---------------------------------------------------------------------------


class TestHTMLResultFromString:
    def test_table_count(self, parsed: HTMLResult) -> None:
        assert len(parsed) == 3

    def test_table_titles(self, parsed: HTMLResult) -> None:
        titles = [t.title for t in parsed.tables]
        assert "Site and Source Energy" in titles
        assert "End Uses" in titles
        assert "Opaque Components" in titles

    def test_report_name_populated(self, parsed: HTMLResult) -> None:
        """Tables inside a report block should carry the report name."""
        # The first table follows "Annual Building Utility Performance Summary"
        assert parsed.tables[0].report_name == "Annual Building Utility Performance Summary"

    def test_for_string_populated(self, parsed: HTMLResult) -> None:
        """for_string should be extracted from 'For:' bold text."""
        assert parsed.tables[0].for_string == "Entire Facility"

    def test_header_row(self, parsed: HTMLResult) -> None:
        site_table = parsed.tables[0]
        assert site_table.header == ["Resource", "Total Energy", "Energy Per Area"]

    def test_data_rows(self, parsed: HTMLResult) -> None:
        site_table = parsed.tables[0]
        assert len(site_table.rows) == 2
        assert site_table.rows[0] == ["Electricity", "12.50", "3.40"]

    def test_empty_html(self) -> None:
        result = HTMLResult.from_string(_EMPTY_HTML)
        assert len(result) == 0


class TestHTMLResultFromFile:
    def test_from_file(self, tmp_path: Path) -> None:
        html_file = tmp_path / "report.html"
        html_file.write_text(_SAMPLE_HTML, encoding="latin-1")
        result = HTMLResult.from_file(html_file)
        assert len(result) == 3


# ---------------------------------------------------------------------------
# __len__, __getitem__, __iter__
# ---------------------------------------------------------------------------


class TestHTMLResultProtocol:
    def test_len(self, parsed: HTMLResult) -> None:
        assert len(parsed) == 3

    def test_getitem(self, parsed: HTMLResult) -> None:
        first = parsed[0]
        assert isinstance(first, HTMLTable)
        assert first.title == "Site and Source Energy"

    def test_iter(self, parsed: HTMLResult) -> None:
        tables = list(parsed)
        assert len(tables) == 3
        assert all(isinstance(t, HTMLTable) for t in tables)


# ---------------------------------------------------------------------------
# titletable
# ---------------------------------------------------------------------------


class TestTitletable:
    def test_returns_pairs(self, parsed: HTMLResult) -> None:
        pairs = parsed.titletable()
        assert len(pairs) == 3
        for title, rows in pairs:
            assert isinstance(title, str)
            assert isinstance(rows, list)

    def test_header_included_as_first_row(self, parsed: HTMLResult) -> None:
        pairs = parsed.titletable()
        title, rows = pairs[0]
        assert title == "Site and Source Energy"
        # First row is the header
        assert rows[0] == ["Resource", "Total Energy", "Energy Per Area"]
        # Subsequent rows are data
        assert rows[1] == ["Electricity", "12.50", "3.40"]

    def test_table_without_header(self) -> None:
        """Tables with no header row should not prepend an empty header."""
        html = "<html><body><b>No Header Table</b><table><tr><td>A</td><td>B</td></tr></table></body></html>"
        result = HTMLResult.from_string(html)
        pairs = result.titletable()
        assert len(pairs) == 1
        title, rows = pairs[0]
        assert title == "No Header Table"
        # No header was parsed, so rows contains only data rows
        assert rows == [["A", "B"]]


# ---------------------------------------------------------------------------
# tablebyname
# ---------------------------------------------------------------------------


class TestTableByName:
    def test_finds_by_partial_name(self, parsed: HTMLResult) -> None:
        table = parsed.tablebyname("Site and Source")
        assert table is not None
        assert table.title == "Site and Source Energy"

    def test_case_insensitive(self, parsed: HTMLResult) -> None:
        table = parsed.tablebyname("site and source energy")
        assert table is not None

    def test_returns_none_when_not_found(self, parsed: HTMLResult) -> None:
        table = parsed.tablebyname("Nonexistent Table Name")
        assert table is None


# ---------------------------------------------------------------------------
# tablebyindex
# ---------------------------------------------------------------------------


class TestTableByIndex:
    def test_valid_index(self, parsed: HTMLResult) -> None:
        table = parsed.tablebyindex(0)
        assert table is not None
        assert table.title == "Site and Source Energy"

    def test_last_index(self, parsed: HTMLResult) -> None:
        table = parsed.tablebyindex(2)
        assert table is not None
        assert table.title == "Opaque Components"

    def test_out_of_range_returns_none(self, parsed: HTMLResult) -> None:
        table = parsed.tablebyindex(99)
        assert table is None

    def test_negative_index_returns_none(self, parsed: HTMLResult) -> None:
        table = parsed.tablebyindex(-1)
        assert table is None


# ---------------------------------------------------------------------------
# tablesbyreport
# ---------------------------------------------------------------------------


class TestTablesByReport:
    def test_finds_by_report_name(self, parsed: HTMLResult) -> None:
        tables = parsed.tablesbyreport("Annual Building Utility Performance Summary")
        assert len(tables) == 2

    def test_case_insensitive(self, parsed: HTMLResult) -> None:
        tables = parsed.tablesbyreport("annual building")
        assert len(tables) == 2

    def test_no_match_returns_empty(self, parsed: HTMLResult) -> None:
        tables = parsed.tablesbyreport("Nonexistent Report")
        assert tables == []


# ---------------------------------------------------------------------------
# HTMLTable.to_dict
# ---------------------------------------------------------------------------


class TestHTMLTableToDict:
    def test_to_dict(self, parsed: HTMLResult) -> None:
        site_table = parsed.tables[0]
        d = site_table.to_dict()
        assert "Electricity" in d
        assert d["Electricity"]["Total Energy"] == "12.50"
        assert d["Electricity"]["Energy Per Area"] == "3.40"

    def test_to_dict_empty_rows(self) -> None:
        table = HTMLTable(title="Empty", header=["H1", "H2"], rows=[])
        assert table.to_dict() == {}

    def test_to_dict_skips_empty_row_entries(self) -> None:
        """to_dict() skips rows that are empty lists."""
        table = HTMLTable(title="WithEmpty", header=["Key", "Val"], rows=[[], ["row1", "v1"]])
        d = table.to_dict()
        assert "row1" in d
        assert len(d) == 1

    def test_to_dict_row_shorter_than_header(self) -> None:
        """Rows shorter than the header should not include missing columns."""
        table = HTMLTable(title="Short", header=["A", "B", "C"], rows=[["Row1", "val"]])
        d = table.to_dict()
        assert "Row1" in d
        assert d["Row1"]["B"] == "val"
        # Column C is missing from this row
        assert "C" not in d["Row1"]


# ---------------------------------------------------------------------------
# Parser internals: _end_table and _end_row edge cases
# ---------------------------------------------------------------------------


class TestParserEdgeCases:
    def test_second_header_row_not_overwritten(self) -> None:
        """A table with multiple <th> rows should not overwrite the first header."""
        html = (
            "<html><body><b>Multi Header</b><table>"
            "<tr><th>Col1</th><th>Col2</th></tr>"
            "<tr><th>SubA</th><th>SubB</th></tr>"
            "<tr><td>Val1</td><td>Val2</td></tr>"
            "</table></body></html>"
        )
        result = HTMLResult.from_string(html)
        assert len(result) == 1
        table = result[0]
        assert table.header == ["Col1", "Col2"]
        # Second header row gets added as a data row since self._current_header is already set
        assert any("SubA" in row for row in table.rows)

    def test_empty_row_in_table_skipped(self) -> None:
        """A completely empty <tr> produces an empty row list which is not appended."""
        html = "<html><body><b>T</b><table><tr><th>H</th></tr><tr></tr><tr><td>v</td></tr></table></body></html>"
        result = HTMLResult.from_string(html)
        assert len(result) == 1
        # The empty row should not appear in rows
        assert result[0].rows == [["v"]]

    def test_table_with_no_rows_or_header_not_appended(self) -> None:
        """A table with no content should not appear in the output."""
        html = "<html><body><b>T</b><table></table></body></html>"
        result = HTMLResult.from_string(html)
        assert len(result) == 0

    def test_tr_outside_table_ignored(self) -> None:
        """A </tr> tag outside a <table> context should be silently ignored."""
        html = "<html><body><tr><td>outside</td></tr><b>T</b><table><tr><td>v</td></tr></table></body></html>"
        result = HTMLResult.from_string(html)
        assert len(result) == 1
        assert result[0].rows == [["v"]]

    def test_bold_inside_table_not_treated_as_title(self) -> None:
        """A <b> tag inside a <table> should not update the title."""
        html = (
            "<html><body><b>Real Title</b><table>"
            "<tr><th>H</th></tr>"
            "<tr><td><b>Bold cell</b></td></tr>"
            "</table></body></html>"
        )
        result = HTMLResult.from_string(html)
        assert len(result) == 1
        assert result[0].title == "Real Title"

    def test_empty_bold_outside_table_ignored(self) -> None:
        """An empty <b></b> outside a table should not change the title."""
        html = "<html><body><b></b><b>Title</b><table><tr><td>v</td></tr></table></body></html>"
        result = HTMLResult.from_string(html)
        assert len(result) == 1
        assert result[0].title == "Title"
