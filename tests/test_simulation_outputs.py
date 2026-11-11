"""Tests for OutputVariableIndex."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from idfkit import new_document, write_epjson, write_idf
from idfkit.simulation.outputs import OutputVariableIndex
from idfkit.simulation.parsers.rdd import OutputMeter, OutputVariable

FIXTURES = Path(__file__).parent / "fixtures" / "simulation"


@pytest.fixture()
def index() -> OutputVariableIndex:
    """Create an index from the sample fixtures."""
    return OutputVariableIndex.from_files(
        FIXTURES / "sample.rdd",
        FIXTURES / "sample.mdd",
    )


class TestFromFiles:
    """Tests for OutputVariableIndex.from_files()."""

    def test_variables_loaded(self, index: OutputVariableIndex) -> None:
        assert len(index.variables) == 7

    def test_meters_loaded(self, index: OutputVariableIndex) -> None:
        assert len(index.meters) == 5

    def test_rdd_only(self) -> None:
        idx = OutputVariableIndex.from_files(FIXTURES / "sample.rdd")
        assert len(idx.variables) == 7
        assert len(idx.meters) == 0

    def test_frozen(self, index: OutputVariableIndex) -> None:
        with pytest.raises(AttributeError):
            index.variables = ()  # type: ignore[misc]


class TestSearch:
    """Tests for OutputVariableIndex.search()."""

    def test_search_temperature(self, index: OutputVariableIndex) -> None:
        results = index.search("Temperature")
        names = [r.name for r in results]
        assert "Site Outdoor Air Drybulb Temperature" in names
        assert "Site Outdoor Air Wetbulb Temperature" in names
        assert "Zone Mean Air Temperature" in names

    def test_search_case_insensitive(self, index: OutputVariableIndex) -> None:
        results = index.search("temperature")
        assert len(results) == 3

    def test_search_electricity(self, index: OutputVariableIndex) -> None:
        results = index.search("Electricity")
        assert len(results) >= 1
        assert any(isinstance(r, OutputMeter) for r in results)

    def test_search_regex(self, index: OutputVariableIndex) -> None:
        results = index.search(r"Heating|Cooling")
        # Matches: Heating Rate, Cooling Rate, Heating Energy (variables) +
        # DistrictHeating, DistrictCooling (meters)
        assert len(results) == 5

    def test_search_no_match(self, index: OutputVariableIndex) -> None:
        results = index.search("Nonexistent")
        assert results == []


class TestFilterByUnits:
    """Tests for OutputVariableIndex.filter_by_units()."""

    def test_filter_celsius(self, index: OutputVariableIndex) -> None:
        results = index.filter_by_units("C")
        assert len(results) == 3
        assert all(isinstance(r, OutputVariable) for r in results)

    def test_filter_watts(self, index: OutputVariableIndex) -> None:
        results = index.filter_by_units("W")
        assert len(results) == 2

    def test_filter_joules(self, index: OutputVariableIndex) -> None:
        results = index.filter_by_units("J")
        # 1 variable (heating energy) + 5 meters
        assert len(results) == 6

    def test_filter_case_insensitive(self, index: OutputVariableIndex) -> None:
        results = index.filter_by_units("c")
        assert len(results) == 3

    def test_filter_no_match(self, index: OutputVariableIndex) -> None:
        results = index.filter_by_units("kg")
        assert results == []


class TestAddAllToModel:
    """Tests for OutputVariableIndex.add_all_to_model()."""

    def test_add_all(self, index: OutputVariableIndex) -> None:
        model = new_document()
        count = index.add_all_to_model(model)
        assert count == 12  # 7 variables + 5 meters

    def test_add_all_creates_output_variables(self, index: OutputVariableIndex) -> None:
        model = new_document()
        index.add_all_to_model(model)
        output_vars = list(model["Output:Variable"])
        assert len(output_vars) == 7

    def test_add_all_creates_output_meters(self, index: OutputVariableIndex) -> None:
        model = new_document()
        index.add_all_to_model(model)
        output_meters = list(model["Output:Meter"])
        assert len(output_meters) == 5

    def test_add_all_meters_store_key_name(self, index: OutputVariableIndex) -> None:
        model = new_document()
        index.add_all_to_model(model, frequency="Hourly")
        expected = {m.name for m in index.meters}
        assert {m.key_name for m in model["Output:Meter"]} == expected
        # Both writers must emit the meter name, and the requested frequency.
        compressed = write_idf(model, output_type="compressed")
        for name in expected:
            assert f"Output:Meter,{name},Hourly;" in compressed
        epjson_meters = json.loads(write_epjson(model))["Output:Meter"].values()
        assert {(m["key_name"], m["reporting_frequency"]) for m in epjson_meters} == {(n, "Hourly") for n in expected}

    def test_removing_added_meter_keeps_equal_existing_meter(self) -> None:
        model = new_document()
        existing = model.add("Output:Meter", key_name="Electricity:Facility", reporting_frequency="Timestep")
        index = OutputVariableIndex(
            variables=(), meters=(OutputMeter(name="Electricity:Facility", units="J", frequency="hourly"),)
        )
        index.add_all_to_model(model, frequency="Timestep")
        added = model["Output:Meter"][1]
        assert added == existing and added is not existing

        model.removeidfobject(added)
        remaining = list(model["Output:Meter"])
        assert len(remaining) == 1
        assert remaining[0] is existing

    def test_add_with_filter(self, index: OutputVariableIndex) -> None:
        model = new_document()
        count = index.add_all_to_model(model, filter_pattern="Temperature")
        assert count == 3

    def test_add_with_frequency(self, index: OutputVariableIndex) -> None:
        model = new_document()
        index.add_all_to_model(model, frequency="Hourly", filter_pattern="Site Outdoor Air Drybulb")
        output_vars = list(model["Output:Variable"])
        assert len(output_vars) == 1
        assert output_vars[0].variable_name == "Site Outdoor Air Drybulb Temperature"
        assert output_vars[0].reporting_frequency == "Hourly"


class TestFromSimulation:
    """Tests for OutputVariableIndex.from_simulation()."""

    def test_no_rdd_file(self, tmp_path: Path) -> None:
        from idfkit.simulation.result import SimulationResult

        result = SimulationResult(
            run_dir=tmp_path,
            success=True,
            exit_code=0,
            stdout="",
            stderr="",
            runtime_seconds=0.0,
        )
        with pytest.raises(FileNotFoundError, match=r"No \.rdd file"):
            OutputVariableIndex.from_simulation(result)

    def test_from_simulation_with_files(self, tmp_path: Path) -> None:
        import shutil

        from idfkit.simulation.result import SimulationResult

        # Copy fixture files into the tmp_path as if they were simulation output
        shutil.copy(FIXTURES / "sample.rdd", tmp_path / "eplusout.rdd")
        shutil.copy(FIXTURES / "sample.mdd", tmp_path / "eplusout.mdd")

        result = SimulationResult(
            run_dir=tmp_path,
            success=True,
            exit_code=0,
            stdout="",
            stderr="",
            runtime_seconds=0.0,
        )
        idx = OutputVariableIndex.from_simulation(result)
        assert len(idx.variables) == 7
        assert len(idx.meters) == 5
