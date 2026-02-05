"""End-to-end simulation tests with a real EnergyPlus installation.

These tests require EnergyPlus to be installed and are skipped when it
is not available. They exercise the full workflow: load IDF → modify
model → simulate → query results.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from idfkit import load_idf
from idfkit.simulation import SimulationResult, find_energyplus
from idfkit.simulation.config import EnergyPlusConfig

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

EPLUS_DIR = Path.home() / ".local" / "EnergyPlus-24.1.0-9d7789a3ac-Linux-Ubuntu22.04-x86_64"


@pytest.fixture(scope="module")
def energyplus() -> EnergyPlusConfig:
    """Discover EnergyPlus or skip the entire module."""
    try:
        return find_energyplus(path=str(EPLUS_DIR))
    except Exception:
        pytest.skip("EnergyPlus not installed")
        raise  # unreachable, keeps type checker happy


@pytest.fixture(scope="module")
def example_idf(energyplus: EnergyPlusConfig) -> Path:
    return energyplus.install_dir / "ExampleFiles" / "1ZoneUncontrolled.idf"


@pytest.fixture(scope="module")
def weather_file(energyplus: EnergyPlusConfig) -> Path:
    return energyplus.install_dir / "WeatherData" / "USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw"


@pytest.fixture(scope="module")
def design_day_result(
    example_idf: Path,
    weather_file: Path,
    energyplus: EnergyPlusConfig,
) -> SimulationResult:
    """Run a design-day simulation once for the module."""
    from idfkit.simulation import simulate

    model = load_idf(str(example_idf))
    return simulate(model, weather_file, energyplus=energyplus, design_day=True)


@pytest.fixture(scope="module")
def annual_result(
    example_idf: Path,
    weather_file: Path,
    energyplus: EnergyPlusConfig,
) -> SimulationResult:
    """Run a full annual simulation with output variables, once for the module."""
    from idfkit.simulation import simulate

    model = load_idf(str(example_idf))

    # Add output variables for querying
    model.add(
        "Output:Variable",
        "",
        data={
            "key_value": "*",
            "variable_name": "Zone Mean Air Temperature",
            "reporting_frequency": "Hourly",
        },
    )
    model.add(
        "Output:Variable",
        "",
        data={
            "key_value": "*",
            "variable_name": "Site Outdoor Air Drybulb Temperature",
            "reporting_frequency": "Hourly",
        },
    )

    return simulate(model, weather_file, energyplus=energyplus, readvars=True)


# ---------------------------------------------------------------------------
# Tests: Model Loading
# ---------------------------------------------------------------------------


class TestModelLoading:
    """Verify the IDF roundtrip is accurate enough for EnergyPlus."""

    def test_load_example_idf(self, example_idf: Path) -> None:
        model = load_idf(str(example_idf))
        assert len(model) > 0

    def test_key_objects_present(self, example_idf: Path) -> None:
        model = load_idf(str(example_idf))
        assert len(model["Zone"]) == 1
        assert len(model["Timestep"]) == 1
        assert len(model["BuildingSurface:Detailed"]) == 6

    def test_nameless_objects_preserved(self, example_idf: Path) -> None:
        model = load_idf(str(example_idf))
        ts = model["Timestep"][0]
        assert ts.name == ""
        assert ts.data.get("number_of_timesteps_per_hour") == 4

    def test_output_variables_all_survive(self, example_idf: Path) -> None:
        model = load_idf(str(example_idf))
        assert len(model["Output:Variable"]) >= 10


# ---------------------------------------------------------------------------
# Tests: Design-Day Simulation
# ---------------------------------------------------------------------------


class TestDesignDaySimulation:
    """Design-day-only simulation (fast, ~0.5s)."""

    def test_simulation_succeeds(self, design_day_result: SimulationResult) -> None:
        assert design_day_result.success
        assert design_day_result.exit_code == 0

    def test_no_severe_errors(self, design_day_result: SimulationResult) -> None:
        assert not design_day_result.errors.has_severe
        assert not design_day_result.errors.has_fatal

    def test_runtime_reasonable(self, design_day_result: SimulationResult) -> None:
        assert design_day_result.runtime_seconds < 30

    def test_output_files_exist(self, design_day_result: SimulationResult) -> None:
        assert design_day_result.err_path is not None
        assert design_day_result.sql_path is not None

    def test_sql_has_variables(self, design_day_result: SimulationResult) -> None:
        sql = design_day_result.sql
        assert sql is not None
        variables = sql.list_variables()
        assert len(variables) > 0


# ---------------------------------------------------------------------------
# Tests: Annual Simulation
# ---------------------------------------------------------------------------


class TestAnnualSimulation:
    """Full annual simulation with output queries."""

    def test_simulation_succeeds(self, annual_result: SimulationResult) -> None:
        assert annual_result.success
        assert annual_result.exit_code == 0

    def test_no_severe_errors(self, annual_result: SimulationResult) -> None:
        assert not annual_result.errors.has_severe
        assert not annual_result.errors.has_fatal

    def test_sql_timeseries(self, annual_result: SimulationResult) -> None:
        sql = annual_result.sql
        assert sql is not None
        ts = sql.get_timeseries("Zone Mean Air Temperature")
        # 8760 hourly values for a full year
        assert len(ts.values) == 8760
        assert ts.units == "C"
        # Sanity check temperature range
        assert min(ts.values) > -50
        assert max(ts.values) < 60

    def test_sql_outdoor_temperature(self, annual_result: SimulationResult) -> None:
        sql = annual_result.sql
        assert sql is not None
        ts = sql.get_timeseries("Site Outdoor Air Drybulb Temperature")
        assert len(ts.values) == 8760

    def test_sql_tabular_data(self, annual_result: SimulationResult) -> None:
        sql = annual_result.sql
        assert sql is not None
        rows = sql.get_tabular_data(
            report_name="AnnualBuildingUtilityPerformanceSummary",
            table_name="End Uses",
        )
        assert len(rows) > 0

    def test_csv_output(self, annual_result: SimulationResult) -> None:
        csv = annual_result.csv
        assert csv is not None
        assert len(csv.timestamps) > 0
        assert len(csv.columns) > 0

    def test_variable_discovery(self, annual_result: SimulationResult) -> None:
        index = annual_result.variables
        assert index is not None
        assert len(index.meters) > 0

    def test_variable_search(self, annual_result: SimulationResult) -> None:
        index = annual_result.variables
        assert index is not None
        results = index.search("Electricity")
        assert len(results) > 0

    def test_variable_injection(self, annual_result: SimulationResult) -> None:
        """OutputVariableIndex.add_all_to_model injects variables into a fresh model."""
        from idfkit import new_document

        index = annual_result.variables
        assert index is not None

        model = new_document()
        count = index.add_all_to_model(model, frequency="Hourly")
        assert count > 0
        assert len(model["Output:Variable"]) + len(model["Output:Meter"]) == count
