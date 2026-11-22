"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class Lights_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_name: str,
        schedule_name: str,
        design_level_calculation_method: Literal["LightingLevel", "Watts/Area", "Watts/Person"]
        | None = "LightingLevel",
        lighting_level: float | None = ...,
        watts_per_zone_floor_area: float | None = ...,
        watts_per_person: float | None = ...,
        return_air_fraction: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_visible: float | None = 0,
        fraction_replaceable: float | None = 1,
        end_use_subcategory: str | None = "General",
        return_air_fraction_calculated_from_plenum_temperature: Literal["No", "Yes"] | None = "No",
        return_air_fraction_function_of_plenum_temperature_coefficient_1: float | None = 0,
        return_air_fraction_function_of_plenum_temperature_coefficient_2: float | None = 0,
        return_air_heat_gain_node_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Lights`` and add it to the document.

        Sets internal gains for lights in the zone. If you use a ZoneList in the Zone or ZoneList name field then this definition applies to all the zones in the ZoneList.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/energyplus-economics/cost-estimating/#lights
        """

class FloorDetailed_v8_9_to_v9_5:
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
        outside_boundary_condition_object: str | None = ...,
        sun_exposure: Literal["NoSun", "SunExposed"] | None = "SunExposed",
        wind_exposure: Literal["NoWind", "WindExposed"] | None = "WindExposed",
        view_factor_to_ground: float | Literal["Autocalculate"] | None = "Autocalculate",
        number_of_vertices: float | Literal["Autocalculate"] | None = "Autocalculate",
        vertices: Sequence[_g.FloorDetailedVerticesItem | _g.FloorDetailedVerticesGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Floor:Detailed`` and add it to the document.

        Allows for detailed entry of floor heat transfer surfaces.

        ``vertices`` takes the extensible groups in order, one dict per group:

        ```python
        doc["Floor:Detailed"].add(
            "Floor Detailed 1",
            construction_name="Construction 1",
            zone_name="Zone 1",
            outside_boundary_condition="Outdoors",
            vertices=[
                {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 10.0, "vertex_z_coordinate": 0.0},
                {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 10.0, "vertex_z_coordinate": 0.0},
                {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-thermal-zone-description-geometry/#floordetailed
        """

class ZoneHVACLowTemperatureRadiantConstantFlow_v9_4:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        surface_name_or_radiant_surface_group_name: str | None = ...,
        fluid_to_radiant_surface_heat_transfer_model: Literal["ConvectionOnly", "ISOStandard"]
        | None = "ConvectionOnly",
        hydronic_tubing_inside_diameter: float | None = 0.013,
        hydronic_tubing_outside_diameter: float | None = 0.016,
        hydronic_tubing_length: float | Literal["Autosize"] | None = "Autosize",
        hydronic_tubing_conductivity: float | None = 0.35,
        temperature_control_type: Literal[
            "MeanAirTemperature",
            "MeanRadiantTemperature",
            "OperativeTemperature",
            "OutdoorDryBulbTemperature",
            "OutdoorWetBulbTemperature",
            "RunningMeanOutdoorDryBulbTemperature",
            "SurfaceFaceTemperature",
            "SurfaceInteriorTemperature",
        ]
        | None = "MeanAirTemperature",
        running_mean_outdoor_dry_bulb_temperature_weighting_factor: float | None = 0.8,
        rated_flow_rate: float | Literal["Autosize"] | None = ...,
        pump_flow_rate_schedule_name: str | None = ...,
        rated_pump_head: float | None = 179352,
        rated_power_consumption: float | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        heating_water_inlet_node_name: str | None = ...,
        heating_water_outlet_node_name: str | None = ...,
        heating_high_water_temperature_schedule_name: str | None = ...,
        heating_low_water_temperature_schedule_name: str | None = ...,
        heating_high_control_temperature_schedule_name: str | None = ...,
        heating_low_control_temperature_schedule_name: str | None = ...,
        cooling_water_inlet_node_name: str | None = ...,
        cooling_water_outlet_node_name: str | None = ...,
        cooling_high_water_temperature_schedule_name: str | None = ...,
        cooling_low_water_temperature_schedule_name: str | None = ...,
        cooling_high_control_temperature_schedule_name: str | None = ...,
        cooling_low_control_temperature_schedule_name: str | None = ...,
        condensation_control_type: Literal["Off", "SimpleOff", "VariableOff"] | None = "SimpleOff",
        condensation_control_dewpoint_offset: float | None = 1,
        number_of_circuits: Literal["CalculateFromCircuitLength", "OnePerSurface"] | None = "OnePerSurface",
        circuit_length: float | None = 106.7,
        changeover_delay_time_period_schedule: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneHVAC:LowTemperatureRadiant:ConstantFlow`` and add it to the document.

        Low temperature hydronic radiant heating and/or cooling system embedded in a building surface (wall, ceiling, or floor). Controlled by varying the hot or chilled water temperature circulating through the unit.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-radiative-convective-units/#zonehvaclowtemperatureradiantconstantflow
        """

class PhotovoltaicPerformanceSimple_v8_9_to_v25_2:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        fraction_of_surface_area_with_active_solar_cells: float,
        conversion_efficiency_input_mode: Literal["Fixed", "Scheduled"] | None = ...,
        value_for_cell_efficiency_if_fixed: float | None = ...,
        efficiency_schedule_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``PhotovoltaicPerformance:Simple`` and add it to the document.

        Describes a simple model of photovoltaics that may be useful for early phase design analysis. In this model the user has direct access to the efficiency with which surfaces convert incident solar radiation to electricity and need not specify arrays of specific modules.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.2/io-reference/overview/group-electric-load-center-generator/#photovoltaicperformancesimple
        """
