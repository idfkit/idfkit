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
def simulate_building(input_spec: BuildingSimInput, tempdir: Path) -> BuildingSimOutput:
    """Run a single parametric EnergyPlus simulation using idfkit."""
    from idfkit import load_idf
    from idfkit.simulation import simulate
    from idfkit.weather import DesignDayManager

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
    ddm = DesignDayManager(input_spec.design_day_file)
    ddm.apply_to_model(model)

    # Run the simulation
    result = simulate(
        model,
        weather=input_spec.weather_file,
        output_dir=tempdir / "run",
        annual=True,
    )

    # Extract end-use totals from the SQL output
    sql = result.sql
    rows = sql.get_tabular_data(
        report_name="AnnualBuildingUtilityPerformanceSummary",
        table_name="End Uses",
    )

    # Build a lookup: (row_name, column_name) -> value
    end_use = {(r.row_name, r.column_name): r.value for r in rows}

    # Get conditioned floor area from the building summary
    area_rows = sql.get_tabular_data(
        report_name="AnnualBuildingUtilityPerformanceSummary",
        table_name="Building Area",
    )
    floor_area = float(next(r.value for r in area_rows if r.row_name == "Net Conditioned Building Area"))

    # Write hourly time-series to CSV for the FileReference output
    csv_path = tempdir / "timeseries.csv"
    if result.csv is not None:
        with open(csv_path, "w") as f:
            f.write("timestamp," + ",".join(c.header for c in result.csv.columns) + "\n")
            for i, ts in enumerate(result.csv.timestamps):
                vals = ",".join(str(c.values[i]) for c in result.csv.columns)
                f.write(f"{ts},{vals}\n")

    return BuildingSimOutput(
        heating_kwh_m2=float(end_use.get(("Heating", "Electricity"), 0)) / floor_area,
        cooling_kwh_m2=float(end_use.get(("Cooling", "Electricity"), 0)) / floor_area,
        lighting_kwh_m2=float(end_use.get(("Interior Lighting", "Electricity"), 0)) / floor_area,
        fans_kwh_m2=float(end_use.get(("Fans", "Electricity"), 0)) / floor_area,
        total_eui=sum(float(v) for (row, col), v in end_use.items() if row == "Total End Uses" and col == "Electricity")
        / floor_area,
        timeseries=csv_path,
        dataframes={},
    )


# --8<-- [end:example]
