"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class ZoneHVACLowTemperatureRadiantVariableFlow_v9_4:
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
            "SurfaceFaceTemperature",
            "SurfaceInteriorTemperature",
        ]
        | None = "MeanAirTemperature",
        setpoint_control_type: Literal["HalfFlowPower", "ZeroFlowPower"] | None = "HalfFlowPower",
        heating_design_capacity_method: Literal[
            "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity: float | Literal["Autosize"] | None = "Autosize",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = 1,
        maximum_hot_water_flow: float | Literal["Autosize"] | None = ...,
        heating_water_inlet_node_name: str | None = ...,
        heating_water_outlet_node_name: str | None = ...,
        heating_control_throttling_range: float | None = 0.5,
        heating_control_temperature_schedule_name: str | None = ...,
        cooling_design_capacity_method: Literal[
            "CapacityPerFloorArea", "CoolingDesignCapacity", "FractionOfAutosizedCoolingCapacity", "None"
        ]
        | None = "CoolingDesignCapacity",
        cooling_design_capacity: float | Literal["Autosize"] | None = ...,
        cooling_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_cooling_design_capacity: float | None = ...,
        maximum_cold_water_flow: float | Literal["Autosize"] | None = ...,
        cooling_water_inlet_node_name: str | None = ...,
        cooling_water_outlet_node_name: str | None = ...,
        cooling_control_throttling_range: float | None = 0.5,
        cooling_control_temperature_schedule_name: str | None = ...,
        condensation_control_type: Literal["Off", "SimpleOff", "VariableOff"] | None = "SimpleOff",
        condensation_control_dewpoint_offset: float | None = 1,
        number_of_circuits: Literal["CalculateFromCircuitLength", "OnePerSurface"] | None = "OnePerSurface",
        circuit_length: float | None = 106.7,
        changeover_delay_time_period_schedule: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:LowTemperatureRadiant:VariableFlow`` and add it to the document.

        Low temperature hydronic radiant heating and/or cooling system embedded in a building surface (wall, ceiling, or floor). Controlled by varying the hot or chilled water flow to the unit.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-radiative-convective-units/#zonehvaclowtemperatureradiantvariableflow
        """

class HeatPumpWaterToWaterEIRCooling_v9_1_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        load_side_inlet_node_name: str,
        load_side_outlet_node_name: str,
        source_side_inlet_node_name: str,
        source_side_outlet_node_name: str,
        capacity_modifier_function_of_temperature_curve_name: str,
        electric_input_to_output_ratio_modifier_function_of_temperature_curve_name: str,
        electric_input_to_output_ratio_modifier_function_of_part_load_ratio_curve_name: str,
        companion_heat_pump_name: str | None = ...,
        load_side_reference_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        source_side_reference_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        reference_capacity: float | Literal["Autosize"] | None = "Autosize",
        reference_coefficient_of_performance: float | None = 7.5,
        sizing_factor: float | None = 1,
    ) -> None:
        """Create a new ``HeatPump:WaterToWater:EIR:Cooling`` and add it to the document.

        An EIR formulated water to water heat pump model, cooling operation.
        """

class ZoneHVACWaterToAirHeatPump_v8_9_to_v9_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        cooling_outdoor_air_flow_rate: float | Literal["Autosize"],
        heating_outdoor_air_flow_rate: float | Literal["Autosize"],
        supply_air_fan_object_type: Literal["Fan:OnOff", "Fan:SystemModel"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:WaterToAirHeatPump:EquationFit", "Coil:Heating:WaterToAirHeatPump:VariableSpeedEquationFit"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:WaterToAirHeatPump:EquationFit", "Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit"
        ],
        cooling_coil_name: str,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        supplemental_heating_coil_name: str,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outdoor_air_mixer_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_cycling_rate: float | None = 2.5,
        heat_pump_time_constant: float | None = 60,
        fraction_of_on_cycle_power_use: float | None = 0.01,
        heat_pump_fan_delay_time: float | None = 60,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        outdoor_dry_bulb_temperature_sensor_node_name: str | None = ...,
        fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        heat_pump_coil_water_flow_mode: Literal["Constant", "ConstantOnDemand", "Cycling"] | None = "Cycling",
        design_specification_zonehvac_sizing_object_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:WaterToAirHeatPump`` and add it to the document.

        Water-to-air heat pump. Forced-convection heating-cooling unit with supply fan, water-to-air cooling and heating coils, supplemental heating coil (gas, electric, hot water, or steam), and fixed-position outdoor air mixer.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.1/io-reference/overview/group-zone-forced-air-units/#zonehvacwatertoairheatpump
        """
