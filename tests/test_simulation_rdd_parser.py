"""Tests for the RDD/MDD parser."""

from __future__ import annotations

from pathlib import Path

import pytest

from idfkit.simulation.parsers.rdd import (
    OutputMeter,
    OutputVariable,
    parse_mdd,
    parse_mdd_file,
    parse_rdd,
    parse_rdd_file,
)

FIXTURES = Path(__file__).parent / "fixtures" / "simulation"


class TestParseRdd:
    """Tests for parse_rdd() and parse_rdd_file()."""

    def test_parse_rdd_from_file(self) -> None:
        variables = parse_rdd_file(FIXTURES / "sample.rdd")
        assert len(variables) == 7
        assert all(isinstance(v, OutputVariable) for v in variables)

    def test_first_variable(self) -> None:
        variables = parse_rdd_file(FIXTURES / "sample.rdd")
        v = variables[0]
        assert v.key == "*"
        assert v.name == "Site Outdoor Air Drybulb Temperature"
        assert v.frequency == "hourly"
        assert v.units == "C"

    def test_variable_with_empty_units(self) -> None:
        variables = parse_rdd_file(FIXTURES / "sample.rdd")
        occupant = variables[6]
        assert occupant.name == "Zone People Occupant Count"
        assert occupant.units == ""

    def test_variable_with_watts(self) -> None:
        variables = parse_rdd_file(FIXTURES / "sample.rdd")
        heating = variables[3]
        assert heating.name == "Zone Air System Sensible Heating Rate"
        assert heating.units == "W"

    def test_parse_rdd_string(self) -> None:
        text = "Output:Variable,*,Test Variable,timestep; !- [kg/s]\n"
        variables = parse_rdd(text)
        assert len(variables) == 1
        assert variables[0].name == "Test Variable"
        assert variables[0].frequency == "timestep"
        assert variables[0].units == "kg/s"

    def test_skips_comments_and_blanks(self) -> None:
        text = "! This is a comment\n\n! Another comment\nOutput:Variable,*,Real Variable,hourly; !- [C]\n"
        variables = parse_rdd(text)
        assert len(variables) == 1

    def test_empty_string(self) -> None:
        variables = parse_rdd("")
        assert variables == ()

    def test_frozen(self) -> None:
        variables = parse_rdd("Output:Variable,*,Test,hourly; !- [C]\n")
        with pytest.raises(AttributeError):
            variables[0].name = "changed"  # type: ignore[misc]


class TestParseMdd:
    """Tests for parse_mdd() and parse_mdd_file()."""

    def test_parse_mdd_from_file(self) -> None:
        meters = parse_mdd_file(FIXTURES / "sample.mdd")
        assert len(meters) == 5
        assert all(isinstance(m, OutputMeter) for m in meters)

    def test_first_meter(self) -> None:
        meters = parse_mdd_file(FIXTURES / "sample.mdd")
        m = meters[0]
        assert m.name == "Electricity:Facility"
        assert m.frequency == "hourly"
        assert m.units == "J"

    def test_last_meter(self) -> None:
        meters = parse_mdd_file(FIXTURES / "sample.mdd")
        m = meters[4]
        assert m.name == "InteriorLights:Electricity"
        assert m.units == "J"

    def test_parse_mdd_string(self) -> None:
        text = "Output:Meter,CustomMeter:Zone1,timestep; !- [W]\n"
        meters = parse_mdd(text)
        assert len(meters) == 1
        assert meters[0].name == "CustomMeter:Zone1"
        assert meters[0].frequency == "timestep"
        assert meters[0].units == "W"

    def test_skips_comments_and_blanks(self) -> None:
        text = "! comment line\n\nOutput:Meter,Electricity:Facility,hourly; !- [J]\n"
        meters = parse_mdd(text)
        assert len(meters) == 1

    def test_empty_string(self) -> None:
        meters = parse_mdd("")
        assert meters == ()

    def test_frozen(self) -> None:
        meters = parse_mdd("Output:Meter,Test,hourly; !- [J]\n")
        with pytest.raises(AttributeError):
            meters[0].name = "changed"  # type: ignore[misc]
