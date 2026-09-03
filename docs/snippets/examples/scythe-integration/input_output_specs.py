from __future__ import annotations

# --8<-- [start:example]
from typing import Literal

from pydantic import Field
from scythe.base import ExperimentInputSpec, ExperimentOutputSpec
from scythe.utils.filesys import FileReference


class BuildingSimInput(ExperimentInputSpec):
    """Input specification for a parametric building energy study."""

    r_value: float = Field(description="Wall insulation R-value [m2K/W]", ge=0, le=15)
    lpd: float = Field(description="Lighting power density [W/m2]", ge=0, le=20)
    setpoint: float = Field(description="Cooling setpoint [deg C]", ge=18, le=30)
    economizer: Literal["NoEconomizer", "DifferentialDryBulb", "DifferentialEnthalpy"] = Field(
        description="Economizer type"
    )
    idf_file: FileReference = Field(description="Base IDF model file")
    weather_file: FileReference = Field(description="EPW weather file")
    design_day_file: FileReference = Field(description="DDY design day file")


class BuildingSimOutput(ExperimentOutputSpec):
    """Output specification with scalar results and time-series data."""

    heating_kwh_m2: float = Field(description="Annual heating [kWh/m2]", ge=0)
    cooling_kwh_m2: float = Field(description="Annual cooling [kWh/m2]", ge=0)
    lighting_kwh_m2: float = Field(description="Annual lighting [kWh/m2]", ge=0)
    fans_kwh_m2: float = Field(description="Annual fan energy [kWh/m2]", ge=0)
    total_eui: float = Field(description="Total site EUI [kWh/m2]", ge=0)
    timeseries: FileReference = Field(description="Hourly results CSV")


# --8<-- [end:example]
