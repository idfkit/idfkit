"""Tests for the CSV parser."""

from __future__ import annotations

from pathlib import Path

import pytest

from idfkit.simulation.parsers.csv import CSVResult

FIXTURES = Path(__file__).parent / "fixtures" / "simulation"


class TestCSVResultFromFile:
    """Tests for CSVResult.from_file()."""

    def test_parse_file(self) -> None:
        result = CSVResult.from_file(FIXTURES / "sample.csv")
        assert len(result.timestamps) == 3
        assert len(result.columns) == 2

    def test_timestamps(self) -> None:
        result = CSVResult.from_file(FIXTURES / "sample.csv")
        assert result.timestamps[0] == "01/01  01:00:00"
        assert result.timestamps[2] == "01/01  03:00:00"

    def test_first_column_metadata(self) -> None:
        result = CSVResult.from_file(FIXTURES / "sample.csv")
        col = result.columns[0]
        assert col.variable_name == "Site Outdoor Air Drybulb Temperature"
        assert col.key_value == "Environment"
        assert col.units == "C"

    def test_first_column_values(self) -> None:
        result = CSVResult.from_file(FIXTURES / "sample.csv")
        col = result.columns[0]
        assert col.values == (-5.20, -5.50, -5.80)

    def test_second_column_metadata(self) -> None:
        result = CSVResult.from_file(FIXTURES / "sample.csv")
        col = result.columns[1]
        assert col.variable_name == "Zone Mean Air Temperature"
        assert col.key_value == "THERMAL ZONE 1"
        assert col.units == "C"


class TestCSVResultFromString:
    """Tests for CSVResult.from_string()."""

    def test_empty_string(self) -> None:
        result = CSVResult.from_string("")
        assert result.timestamps == ()
        assert result.columns == ()

    def test_headers_only(self) -> None:
        result = CSVResult.from_string("Date/Time,Env:Var [C](Hourly)\n")
        assert result.timestamps == ()
        assert len(result.columns) == 1

    def test_unrecognized_header(self) -> None:
        text = "Date/Time,Unknown Header\n 01/01  01:00:00,1.0\n"
        result = CSVResult.from_string(text)
        col = result.columns[0]
        assert col.variable_name == "Unknown Header"
        assert col.key_value == ""
        assert col.units == ""


class TestGetColumn:
    """Tests for CSVResult.get_column()."""

    def test_find_by_name(self) -> None:
        result = CSVResult.from_file(FIXTURES / "sample.csv")
        col = result.get_column("Site Outdoor Air Drybulb Temperature")
        assert col is not None
        assert col.key_value == "Environment"

    def test_find_by_name_case_insensitive(self) -> None:
        result = CSVResult.from_file(FIXTURES / "sample.csv")
        col = result.get_column("site outdoor air drybulb temperature")
        assert col is not None

    def test_find_by_name_and_key(self) -> None:
        result = CSVResult.from_file(FIXTURES / "sample.csv")
        col = result.get_column("Zone Mean Air Temperature", "THERMAL ZONE 1")
        assert col is not None

    def test_find_by_name_wrong_key(self) -> None:
        result = CSVResult.from_file(FIXTURES / "sample.csv")
        col = result.get_column("Zone Mean Air Temperature", "NONEXISTENT")
        assert col is None

    def test_not_found(self) -> None:
        result = CSVResult.from_file(FIXTURES / "sample.csv")
        col = result.get_column("Nonexistent Variable")
        assert col is None


class TestFrozen:
    """Tests for immutability."""

    def test_csv_result_frozen(self) -> None:
        result = CSVResult.from_file(FIXTURES / "sample.csv")
        with pytest.raises(AttributeError):
            result.timestamps = ()  # type: ignore[misc]

    def test_csv_column_frozen(self) -> None:
        result = CSVResult.from_file(FIXTURES / "sample.csv")
        with pytest.raises(AttributeError):
            result.columns[0].header = "changed"  # type: ignore[misc]
