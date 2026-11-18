"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class WallDetailed_v9_6_to_v24_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition: Literal[
            "Adiabatic",
            "Foundation",
            "Ground",
            "GroundBasementPreprocessorAverageFloor",
            "GroundBasementPreprocessorAverageWall",
            "GroundBasementPreprocessorLowerWall",
            "GroundBasementPreprocessorUpperWall",
            "GroundFCfactorMethod",
            "GroundSlabPreprocessorAverage",
            "GroundSlabPreprocessorCore",
            "GroundSlabPreprocessorPerimeter",
            "OtherSideCoefficients",
            "OtherSideConditionsModel",
            "Outdoors",
            "Surface",
            "Zone",
        ],
        space_name: str | None = ...,
        outside_boundary_condition_object: str | None = ...,
        sun_exposure: Literal["NoSun", "SunExposed"] | None = "SunExposed",
        wind_exposure: Literal["NoWind", "WindExposed"] | None = "WindExposed",
        view_factor_to_ground: float | Literal["Autocalculate"] | None = "Autocalculate",
        number_of_vertices: float | Literal["Autocalculate"] | None = "Autocalculate",
        vertices: Sequence[_g.WallDetailedVerticesItem | _g.WallDetailedVerticesGroup] = ...,
    ) -> None:
        """Create a new ``Wall:Detailed`` and add it to the document.

        Allows for detailed entry of wall heat transfer surfaces.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.2/io-reference/overview/group-thermal-zone-description-geometry/#walldetailed
        """

class CoilCoolingDXTwoStageWithHumidityControlMode_v22_2_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        normal_mode_stage_1_coil_performance_object_type: Literal["CoilPerformance:DX:Cooling"],
        normal_mode_stage_1_coil_performance_name: str,
        availability_schedule_name: str | None = ...,
        crankcase_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        number_of_capacity_stages: int | None = 1,
        number_of_enhanced_dehumidification_modes: int | None = 0,
        normal_mode_stage_1_2_coil_performance_object_type: Literal["CoilPerformance:DX:Cooling"] | None = ...,
        normal_mode_stage_1_2_coil_performance_name: str | None = ...,
        dehumidification_mode_1_stage_1_coil_performance_object_type: Literal["CoilPerformance:DX:Cooling"]
        | None = ...,
        dehumidification_mode_1_stage_1_coil_performance_name: str | None = ...,
        dehumidification_mode_1_stage_1_2_coil_performance_object_type: Literal["CoilPerformance:DX:Cooling"]
        | None = ...,
        dehumidification_mode_1_stage_1_2_coil_performance_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        condensate_collection_water_storage_tank_name: str | None = ...,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -25,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:TwoStageWithHumidityControlMode`` and add it to the document.

        Direct expansion (DX) cooling coil and condensing unit (includes electric compressor and condenser fan), two-stage with humidity control mode (e.g. sub-cool or hot gas reheat). Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Requires two to four sets of performance data, see CoilPerformance:DX:Cooling. Stages are modeled as a face-split coil.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxtwostagewithhumiditycontrolmode
        """
