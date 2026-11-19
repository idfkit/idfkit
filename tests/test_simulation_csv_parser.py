"""Tests for the CSV parser."""

from __future__ import annotations

from pathlib import Path

import pytest

from idfkit.exceptions import ResultLookupError
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
        with pytest.raises(ResultLookupError, match="has no key 'NONEXISTENT'") as exc:
            result.get_column("Zone Mean Air Temperature", "NONEXISTENT")
        assert exc.value.available == ("THERMAL ZONE 1",)

    def test_not_found_suggests_closest(self) -> None:
        result = CSVResult.from_file(FIXTURES / "sample.csv")
        with pytest.raises(ResultLookupError, match="Did you mean 'Zone Mean Air Temperature'") as exc:
            result.get_column("Zone Mean Air Temprature")
        assert exc.value.suggestions == ("Zone Mean Air Temperature",)

    def test_several_keys_refused(self) -> None:
        text = (
            "Date/Time,ZONE A:Zone Mean Air Temperature [C](Hourly),ZONE B:Zone Mean Air Temperature [C](Hourly)\n"
            " 01/01  01:00:00,20.0,22.0\n"
        )
        result = CSVResult.from_string(text)
        with pytest.raises(ResultLookupError, match=r"2 keys \(ZONE A, ZONE B\); pass key_value=") as exc:
            result.get_column("Zone Mean Air Temperature")
        assert exc.value.available == ("ZONE A", "ZONE B")
        assert result.get_column("Zone Mean Air Temperature", "zone b").values == (22.0,)

    def test_several_frequencies_refused(self) -> None:
        text = "Date/Time,Env:Var [C](Hourly),Env:Var [C](Daily)\n 01/01  01:00:00,1.0,2.0\n"
        result = CSVResult.from_string(text)
        with pytest.raises(ResultLookupError, match="pass frequency="):
            result.get_column("Var")
        col = result.get_column("Var", frequency="daily")
        assert col.frequency == "Daily"
        assert col.values == (2.0,)

    def test_meter_by_full_name(self) -> None:
        text = (
            "Date/Time,Electricity:Facility [J](Hourly),NaturalGas:Facility [J](Hourly),"
            "InteriorLights:Electricity:Zone:SPACE1-1 [J](Hourly)\n"
            " 01/01  01:00:00,1.0,2.0,3.0\n"
        )
        result = CSVResult.from_string(text)
        col = result.get_column("Electricity:Facility")
        assert col.values == (1.0,)
        assert col.units == "J"
        assert result.get_column("naturalgas:facility", frequency="Hourly").values == (2.0,)
        assert result.get_column("InteriorLights:Electricity:Zone:SPACE1-1").values == (3.0,)

    def test_meter_typo_suggests_full_name(self) -> None:
        text = "Date/Time,Electricity:Facility [J](Hourly)\n 01/01  01:00:00,1.0\n"
        result = CSVResult.from_string(text)
        with pytest.raises(ResultLookupError, match="Did you mean 'Electricity:Facility'") as exc:
            result.get_column("Electricity:Facilty")
        assert exc.value.suggestions == ("Electricity:Facility",)
        with pytest.raises(ResultLookupError, match="reported with no key"):
            result.get_column("Electricity:Facility", "Building")


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


class TestRepr:
    """A repr summarizes the data instead of listing it."""

    def test_csv_result_repr(self) -> None:
        result = CSVResult.from_file(FIXTURES / "sample.csv")
        assert repr(result).startswith(f"CSVResult({len(result.timestamps)} rows, {len(result.columns)} columns, ")

    def test_csv_column_repr(self) -> None:
        column = CSVResult.from_file(FIXTURES / "sample.csv").columns[0]
        assert repr(column).startswith(f"CSVColumn({column.header!r}, {len(column.values)} points")


class TestEdgeCases:
    """Tests for edge cases not covered by the main tests."""

    def test_empty_row_skipped(self) -> None:
        """Empty rows (L87) should be silently skipped."""
        text = "Date/Time,Env:Var [C](Hourly)\n 01/01  01:00:00,1.0\n\n 01/01  02:00:00,2.0\n"
        result = CSVResult.from_string(text)
        # The empty row is skipped; only two data rows
        assert len(result.timestamps) == 2

    def test_non_numeric_value_becomes_zero(self) -> None:
        """Non-numeric cell values (L94-95) should be stored as 0.0."""
        text = "Date/Time,Env:Var [C](Hourly)\n 01/01  01:00:00,N/A\n"
        result = CSVResult.from_string(text)
        assert result.columns[0].values == (0.0,)

    def test_short_row_pads_with_zero(self) -> None:
        """Rows shorter than the header (L96-99) should be padded with 0.0."""
        text = "Date/Time,ColA [C](Hourly),ColB [C](Hourly)\n 01/01  01:00:00,1.5\n"
        result = CSVResult.from_string(text)
        assert result.columns[0].values == (1.5,)
        # ColB has no value in the short row — should be padded with 0.0
        assert result.columns[1].values == (0.0,)
