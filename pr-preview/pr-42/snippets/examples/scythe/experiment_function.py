from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field
from scythe.base import ExperimentInputSpec, ExperimentOutputSpec
from scythe.registry import ExperimentRegistry
from scythe.utils.filesys import FileReference


class BuildingSimInput(ExperimentInputSpec):
    r_value: float = Field(default=..., ge=0, le=15)
    lpd: float = Field(default=..., ge=0, le=20)
    setpoint: float = Field(default=..., ge=18, le=30)
    economizer: Literal["NoEconomizer", "DifferentialDryBulb", "DifferentialEnthalpy"] = Field(default=...)
    idf_file: FileReference = Field(default=...)
    weather_file: FileReference = Field(default=...)
    design_day_file: FileReference = Field(default=...)


class BuildingSimOutput(ExperimentOutputSpec):
    heating_kwh_m2: float = Field(default=..., ge=0)
    cooling_kwh_m2: float = Field(default=..., ge=0)
    lighting_kwh_m2: float = Field(default=..., ge=0)
    fans_kwh_m2: float = Field(default=..., ge=0)
    total_eui: float = Field(default=..., ge=0)
    timeseries: FileReference = Field(default=...)


# --8<-- [start:example]
@ExperimentRegistry.Register()
def simulate_building(
    input_spec: BuildingSimInput, tempdir: Path
) -> BuildingSimOutput:
    """Run a single parametric EnergyPlus simulation using idfkit."""
    from idfkit import load_idf
    from idfkit.simulation import simulate
    from idfkit.weather import apply_ashrae_sizing

    # Load the base IDF model (FileReference resolves to a local path)
    model = load_idf(input_spec.idf_file)

    # Apply parametric overrides
    for material in model["Material"]:
        if "wall_insulation" in material.Name.lower():
            material.Thermal_Resistance = input_spec.r_value

    for lights in model["Lights"]:
        lights.Watts_per_Zone_Floor_Area = input_spec.lpd

    for thermostat in model["ThermostatSetpoint:DualSetpoint"]:
        # Adjust cooling setpoint schedule
        pass  # modify as needed for your model

    # Inject ASHRAE design days from the DDY file
    apply_ashrae_sizing(model, input_spec.design_day_file)

    # Run the simulation
    result = simulate(
        model,
        weather=input_spec.weather_file,
        output_dir=tempdir / "run",
        annual=True,
    )

    # Extract end-use totals from the SQL output
    sql = result.sql
    end_use = sql.tabular_data_by_name(
        "AnnualBuildingUtilityPerformanceSummary",
        "End Uses",
    )

    floor_area = sql.total_conditioned_area()

    # Write hourly time-series to CSV
    csv_path = tempdir / "timeseries.csv"
    ts = result.csv
    ts.to_dataframe().to_csv(csv_path)

    return BuildingSimOutput(
        heating_kwh_m2=end_use["Heating"]["Total"] / floor_area,
        cooling_kwh_m2=end_use["Cooling"]["Total"] / floor_area,
        lighting_kwh_m2=end_use["Interior Lighting"]["Total"] / floor_area,
        fans_kwh_m2=end_use["Fans"]["Total"] / floor_area,
        total_eui=end_use["Total End Uses"]["Total"] / floor_area,
        timeseries=csv_path,
        dataframes={},
    )
# --8<-- [end:example]
