"""Tests for the RDD/MDD parser."""

from __future__ import annotations

from pathlib import Path

import pytest

from idfkit.simulation.parsers.rdd import (
    DictionaryParseWarning,
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

    def test_parse_rdd_idf_format_with_descriptor(self) -> None:
        text = (
            "Output:Variable,*,Site Outdoor Air Drybulb Temperature,hourly; !- Zone Average [C]\n"
            "Output:Variable,*,Zone Air System Sensible Heating Rate,hourly; !- HVAC Sum [W]\n"
        )
        variables = parse_rdd(text)
        assert len(variables) == 2
        assert variables[0].name == "Site Outdoor Air Drybulb Temperature"
        assert variables[0].units == "C"
        assert variables[1].name == "Zone Air System Sensible Heating Rate"
        assert variables[1].units == "W"

    def test_parse_rdd_without_descriptor(self) -> None:
        text = "Output:Variable,*,Test Variable,hourly; !- [C]\n"
        variables = parse_rdd(text)
        assert len(variables) == 1
        assert variables[0].units == "C"

    def test_parse_rdd_regular_format(self) -> None:
        # `Output:VariableDictionary, Regular` writes lines without a key
        # or frequency; both fields are synthesized to match the IDF form.
        text = (
            "Program Version,EnergyPlus, Version 24.1.0\n"
            "Var Type (reported time step),Var Report Type,Variable Name [Units]\n"
            "Zone,Average,Site Outdoor Air Drybulb Temperature [C]\n"
            "HVAC,Sum,Zone Ideal Loads Supply Air Total Heating Energy [J]\n"
            "Zone,Average,Site Outdoor Air Humidity Ratio [kgWater/kgDryAir]\n"
        )
        variables = parse_rdd(text)
        assert len(variables) == 3
        first = variables[0]
        assert first.key == "*"
        assert first.name == "Site Outdoor Air Drybulb Temperature"
        assert first.frequency == "hourly"
        assert first.units == "C"
        assert variables[1].name == "Zone Ideal Loads Supply Air Total Heating Energy"
        assert variables[1].units == "J"
        # Slash-bearing units round-trip.
        assert variables[2].units == "kgWater/kgDryAir"

    def test_warns_when_silently_empty(self) -> None:
        # Junk lines that match neither IDF nor Regular format.
        text = "! header\nthis is not a dictionary line at all\n"
        with pytest.warns(DictionaryParseWarning, match="Parsed 0 entries"):
            variables = parse_rdd(text)
        assert variables == ()

    def test_no_warning_for_empty_input(self) -> None:
        import warnings as _w

        with _w.catch_warnings():
            _w.simplefilter("error", DictionaryParseWarning)
            assert parse_rdd("") == ()
            assert parse_rdd("! only comments\n\n! more comments\n") == ()

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

    def test_parse_mdd_with_descriptor(self) -> None:
        # `Output:VariableDictionary, IDF` may also place a descriptor between
        # `!-` and `[` for meters in some EnergyPlus versions.
        text = "Output:Meter,Electricity:Facility,hourly; !- HVAC Sum [J]\n"
        meters = parse_mdd(text)
        assert len(meters) == 1
        assert meters[0].name == "Electricity:Facility"
        assert meters[0].units == "J"

    def test_parse_mdd_regular_format(self) -> None:
        # `Output:VariableDictionary, Regular` MDD lines have no frequency;
        # synthesized to "hourly" to match the IDF form.
        text = (
            "Program Version,EnergyPlus, Version 24.1.0\n"
            "Var Type (reported time step),Var Report Type,Variable Name [Units]\n"
            "Zone,Meter,Electricity:Facility [J]\n"
            "Zone,Meter,InteriorLights:Electricity:Zone:BLOCK CORE STOREY 1 [J]\n"
            "Zone,Meter,Carbon Equivalent:Facility [kg]\n"
        )
        meters = parse_mdd(text)
        assert len(meters) == 3
        assert meters[0].name == "Electricity:Facility"
        assert meters[0].frequency == "hourly"
        assert meters[0].units == "J"
        # Meter names with colons and spaces.
        assert meters[1].name == "InteriorLights:Electricity:Zone:BLOCK CORE STOREY 1"
        assert meters[2].name == "Carbon Equivalent:Facility"
        assert meters[2].units == "kg"

    def test_drops_cumulative_variants(self) -> None:
        # All four Output:Meter* variants are recognized; the two cumulative
        # forms are dropped (no warning), the two non-cumulative forms are
        # emitted as OutputMeter.
        text = (
            "Output:Meter,Electricity:Facility,hourly; !- [J]\n"
            "Output:Meter:Cumulative,Electricity:Facility,hourly; !- [J]\n"
            "Output:Meter:MeterFileOnly,InteriorLights:Electricity,hourly; !- [J]\n"
            "Output:Meter:Cumulative:MeterFileOnly,InteriorLights:Electricity,hourly; !- [J]\n"
        )
        import warnings as _w

        with _w.catch_warnings():
            _w.simplefilter("error", DictionaryParseWarning)
            meters = parse_mdd(text)
        assert [m.name for m in meters] == ["Electricity:Facility", "InteriorLights:Electricity"]

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
