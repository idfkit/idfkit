"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class AnyShadowCalculation:
    def __call__(
        self,
        /,
        *,
        maximum_figures_in_shadow_overlap_calculations: int | None = 15000,
        polygon_clipping_algorithm: Literal["", "ConvexWeilerAtherton", "SutherlandHodgman"]
        | None = "SutherlandHodgman",
        sky_diffuse_modeling_algorithm: Literal["", "DetailedSkyDiffuseModeling", "SimpleSkyDiffuseModeling"]
        | None = "SimpleSkyDiffuseModeling",
        output_external_shading_calculation_results: Literal["", "No", "Yes"] | None = "No",
        disable_self_shading_within_shading_zone_groups: Literal["", "No", "Yes"] | None = "No",
        disable_self_shading_from_shading_zone_groups_to_other_zones: Literal["", "No", "Yes"] | None = "No",
        shading_zone_groups: list[_g.ShadowCalculationShadingZoneGroupsItem] = ...,
    ) -> None: ...

class WindowMaterialSimpleGlazingSystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        u_factor: float,
        solar_heat_gain_coefficient: float,
        visible_transmittance: float | None = ...,
    ) -> None: ...

class AnyWindowMaterialGasMixture:
    def __call__(
        self,
        name: str,
        /,
        *,
        thickness: float,
        number_of_gases_in_mixture: int,
        gas_1_type: Literal["Air", "Argon", "Krypton", "Xenon"],
        gas_1_fraction: float,
        gas_2_type: Literal["Air", "Argon", "Krypton", "Xenon"],
        gas_2_fraction: float,
        gas_3_type: Literal["Air", "Argon", "Krypton", "Xenon"] | None = ...,
        gas_3_fraction: float | None = ...,
        gas_4_type: Literal["Air", "Argon", "Krypton", "Xenon"] | None = ...,
        gas_4_fraction: float | None = ...,
    ) -> None: ...

class AnyConstructionPropertyInternalHeatSource:
    def __call__(
        self,
        name: str,
        /,
        *,
        thermal_source_present_after_layer_number: int,
        temperature_calculation_requested_after_layer_number: int,
        dimensions_for_the_ctf_calculation: int,
        tube_spacing: float,
        construction_name: str | None = ...,
        two_dimensional_temperature_calculation_position: float | None = 0,
    ) -> None: ...

class WallExterior:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        space_name: str | None = ...,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 90,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None: ...

class AnyFloorInterzone:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition_object: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 180,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        width: float | None = ...,
    ) -> None: ...

class ShadingFin:
    def __call__(
        self,
        name: str,
        /,
        *,
        window_or_door_name: str,
        left_extension_from_window_door: float | None = ...,
        left_distance_above_top_of_window: float | None = ...,
        left_distance_below_bottom_of_window: float | None = ...,
        left_tilt_angle_from_window_door: float | None = 90,
        left_depth: float | None = ...,
        right_extension_from_window_door: float | None = ...,
        right_distance_above_top_of_window: float | None = ...,
        right_distance_below_bottom_of_window: float | None = ...,
        right_tilt_angle_from_window_door: float | None = 90,
        right_depth: float | None = ...,
    ) -> None: ...

class GroundHeatTransferBasementEquivSlab:
    def __call__(
        self, /, *, apratio_the_area_to_perimeter_ratio_for_this_slab: float, equivsizing_flag: Literal["FALSE", "TRUE"]
    ) -> None: ...

class RoomAirTemperaturePatternUserDefined:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        pattern_control_schedule_name: str,
        availability_schedule_name: str | None = ...,
    ) -> None: ...

class GasEquipmentDefinition:
    def __call__(
        self,
        name: str,
        /,
        *,
        design_level_calculation_method: Literal[
            "", "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_floor_area: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        carbon_dioxide_generation_rate: float | None = 0,
    ) -> None: ...

class OtherEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        fuel_type: Literal[
            "",
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = "None",
        design_level_calculation_method: Literal[
            "", "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_floor_area: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        carbon_dioxide_generation_rate: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class ElectricEquipmentITEAirCooledInstance:
    def __call__(
        self,
        name: str,
        /,
        *,
        electricequipment_ite_aircooled_definition_name: str,
        zone_or_space_name: str,
        multiplier: float | None = 1,
        design_power_input_schedule_name: str | None = ...,
        cpu_loading_schedule_name: str | None = ...,
        air_inlet_room_air_model_node_name: str | None = ...,
        air_outlet_room_air_model_node_name: str | None = ...,
        supply_air_node_name: str | None = ...,
        cpu_end_use_subcategory: str | None = "ITE-CPU",
        fan_end_use_subcategory: str | None = "ITE-Fans",
        electric_power_supply_end_use_subcategory: str | None = "ITE-UPS",
    ) -> None: ...

class AirflowNetworkMultiZoneZone:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        ventilation_control_mode: Literal[
            "", "ASHRAE55Adaptive", "CEN15251Adaptive", "Constant", "Enthalpy", "NoVent", "Temperature"
        ]
        | None = "NoVent",
        ventilation_control_zone_temperature_setpoint_schedule_name: str | None = ...,
        minimum_venting_open_factor: float | None = 0,
        indoor_and_outdoor_temperature_difference_lower_limit_for_maximum_venting_open_factor: float | None = 0,
        indoor_and_outdoor_temperature_difference_upper_limit_for_minimum_venting_open_factor: float | None = 100,
        indoor_and_outdoor_enthalpy_difference_lower_limit_for_maximum_venting_open_factor: float | None = 0,
        indoor_and_outdoor_enthalpy_difference_upper_limit_for_minimum_venting_open_factor: float | None = 300000,
        venting_availability_schedule_name: str | None = ...,
        single_sided_wind_pressure_coefficient_algorithm: Literal["", "Advanced", "Standard"] | None = "Standard",
        facade_width: float | None = 10,
        occupant_ventilation_control_name: str | None = ...,
    ) -> None: ...

class AirflowNetworkDistributionLinkage:
    def __call__(
        self,
        name: str,
        /,
        *,
        node_1_name: str,
        node_2_name: str,
        component_name: str,
        thermal_zone_name: str | None = ...,
    ) -> None: ...

class ExteriorFuelEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        fuel_use_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Water",
        ],
        schedule_name: str,
        design_level: float,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class ThermostatSetpointThermalComfortFangerSingleHeatingOrCooling:
    def __call__(self, name: str, /, *, fanger_thermal_comfort_schedule_name: str) -> None: ...

class ZoneHVACBaseboardRadiantConvectiveElectric:
    def __call__(
        self,
        name: str,
        /,
        *,
        fraction_radiant: float,
        availability_schedule_name: str | None = ...,
        heating_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = 1,
        efficiency: float | None = 1,
        fraction_of_radiant_energy_incident_on_people: float | None = ...,
        surface_fractions: list[_g.ZoneHVACBaseboardRadiantConvectiveElectricSurfaceFractionsItem] = ...,
    ) -> None: ...

class SpaceHVACZoneReturnMixer:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        zone_return_air_node_name: str,
        spaces: list[_g.SpaceHVACZoneReturnMixerSpacesItem] = ...,
    ) -> None: ...

class CoilCoolingWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        design_water_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        design_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        design_inlet_water_temperature: float | Literal["", "Autosize"] | None = "Autosize",
        design_inlet_air_temperature: float | Literal["", "Autosize"] | None = "Autosize",
        design_outlet_air_temperature: float | Literal["", "Autosize"] | None = "Autosize",
        design_inlet_air_humidity_ratio: float | Literal["", "Autosize"] | None = "Autosize",
        design_outlet_air_humidity_ratio: float | Literal["", "Autosize"] | None = "Autosize",
        type_of_analysis: Literal["", "DetailedAnalysis", "SimpleAnalysis"] | None = "SimpleAnalysis",
        heat_exchanger_configuration: Literal["", "CounterFlow", "CrossFlow"] | None = "CounterFlow",
        condensate_collection_water_storage_tank_name: str | None = ...,
        design_water_temperature_difference: float | None = ...,
    ) -> None: ...

class AnyCoilSystemCoolingDXHeatExchangerAssisted:
    def __call__(
        self,
        name: str,
        /,
        *,
        heat_exchanger_object_type: Literal[
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
            "HeatExchanger:Desiccant:BalancedFlow",
        ],
        heat_exchanger_name: str,
        cooling_coil_object_type: Literal["Coil:Cooling:DX:SingleSpeed", "Coil:Cooling:DX:VariableSpeed"],
        cooling_coil_name: str,
    ) -> None: ...

class AirConditionerVariableRefrigerantFlow:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        zone_terminal_unit_list_name: str,
        availability_schedule_name: str | None = ...,
        gross_rated_total_cooling_capacity: float | Literal["Autosize"] | None = ...,
        gross_rated_cooling_cop: float | None = 3.3,
        minimum_condenser_inlet_node_temperature_in_cooling_mode: float | None = -6,
        maximum_condenser_inlet_node_temperature_in_cooling_mode: float | None = 43,
        cooling_capacity_ratio_modifier_function_of_low_temperature_curve_name: str | None = ...,
        cooling_capacity_ratio_boundary_curve_name: str | None = ...,
        cooling_capacity_ratio_modifier_function_of_high_temperature_curve_name: str | None = ...,
        cooling_energy_input_ratio_modifier_function_of_low_temperature_curve_name: str | None = ...,
        cooling_energy_input_ratio_boundary_curve_name: str | None = ...,
        cooling_energy_input_ratio_modifier_function_of_high_temperature_curve_name: str | None = ...,
        cooling_energy_input_ratio_modifier_function_of_low_part_load_ratio_curve_name: str | None = ...,
        cooling_energy_input_ratio_modifier_function_of_high_part_load_ratio_curve_name: str | None = ...,
        cooling_combination_ratio_correction_factor_curve_name: str | None = ...,
        cooling_part_load_fraction_correlation_curve_name: str | None = ...,
        gross_rated_heating_capacity: float | Literal["Autosize"] | None = ...,
        rated_heating_capacity_sizing_ratio: float | None = 1,
        gross_rated_heating_cop: float | None = 3.4,
        minimum_condenser_inlet_node_temperature_in_heating_mode: float | None = -20,
        maximum_condenser_inlet_node_temperature_in_heating_mode: float | None = 16,
        heating_capacity_ratio_modifier_function_of_low_temperature_curve_name: str | None = ...,
        heating_capacity_ratio_boundary_curve_name: str | None = ...,
        heating_capacity_ratio_modifier_function_of_high_temperature_curve_name: str | None = ...,
        heating_energy_input_ratio_modifier_function_of_low_temperature_curve_name: str | None = ...,
        heating_energy_input_ratio_boundary_curve_name: str | None = ...,
        heating_energy_input_ratio_modifier_function_of_high_temperature_curve_name: str | None = ...,
        heating_performance_curve_outdoor_temperature_type: Literal["", "DryBulbTemperature", "WetBulbTemperature"]
        | None = "WetBulbTemperature",
        heating_energy_input_ratio_modifier_function_of_low_part_load_ratio_curve_name: str | None = ...,
        heating_energy_input_ratio_modifier_function_of_high_part_load_ratio_curve_name: str | None = ...,
        heating_combination_ratio_correction_factor_curve_name: str | None = ...,
        heating_part_load_fraction_correlation_curve_name: str | None = ...,
        minimum_heat_pump_part_load_ratio: float | None = 0.15,
        zone_name_for_master_thermostat_location: str | None = ...,
        master_thermostat_priority_control_type: Literal[
            "", "LoadPriority", "MasterThermostatPriority", "Scheduled", "ThermostatOffsetPriority", "ZonePriority"
        ]
        | None = "MasterThermostatPriority",
        thermostat_priority_schedule_name: str | None = ...,
        heat_pump_waste_heat_recovery: Literal["", "No", "Yes"] | None = "No",
        equivalent_piping_length_used_for_piping_correction_factor_in_cooling_mode: float | None = ...,
        vertical_height_used_for_piping_correction_factor: float | None = ...,
        piping_correction_factor_for_length_in_cooling_mode_curve_name: str | None = ...,
        piping_correction_factor_for_height_in_cooling_mode_coefficient: float | None = 0,
        equivalent_piping_length_used_for_piping_correction_factor_in_heating_mode: float | None = ...,
        piping_correction_factor_for_length_in_heating_mode_curve_name: str | None = ...,
        piping_correction_factor_for_height_in_heating_mode_coefficient: float | None = 0,
        crankcase_heater_power_per_compressor: float | None = 33,
        number_of_compressors: int | None = 2,
        ratio_of_compressor_size_to_total_compressor_capacity: float | None = 0.5,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater: float | None = 5,
        defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "Resistive",
        defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        defrost_energy_input_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["", "Autosize"] | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        water_condenser_volume_flow_rate: float | Literal["Autosize"] | None = ...,
        evaporative_condenser_effectiveness: float | None = 0.9,
        evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        evaporative_condenser_pump_rated_power_consumption: float | Literal["", "Autosize"] | None = 0,
        supply_water_storage_tank_name: str | None = ...,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        fuel_type: Literal[
            "",
            "Diesel",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = "Electricity",
        minimum_condenser_inlet_node_temperature_in_heat_recovery_mode: float | None = ...,
        maximum_condenser_inlet_node_temperature_in_heat_recovery_mode: float | None = ...,
        heat_recovery_cooling_capacity_modifier_curve_name: str | None = ...,
        initial_heat_recovery_cooling_capacity_fraction: float | None = 0.5,
        heat_recovery_cooling_capacity_time_constant: float | None = 0.15,
        heat_recovery_cooling_energy_modifier_curve_name: str | None = ...,
        initial_heat_recovery_cooling_energy_fraction: float | None = 1,
        heat_recovery_cooling_energy_time_constant: float | None = 0,
        heat_recovery_heating_capacity_modifier_curve_name: str | None = ...,
        initial_heat_recovery_heating_capacity_fraction: float | None = 1,
        heat_recovery_heating_capacity_time_constant: float | None = 0.15,
        heat_recovery_heating_energy_modifier_curve_name: str | None = ...,
        initial_heat_recovery_heating_energy_fraction: float | None = 1,
        heat_recovery_heating_energy_time_constant: float | None = 0,
    ) -> None: ...

class AirLoopHVACSupplyPlenum:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        zone_node_name: str,
        inlet_node_name: str,
        nodes: list[_g.AirLoopHVACSupplyPlenumNodesItem] = ...,
    ) -> None: ...

class AnyHeatPumpWaterToWaterEquationFitCooling:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        source_side_inlet_node_name: str,
        source_side_outlet_node_name: str,
        load_side_inlet_node_name: str,
        load_side_outlet_node_name: str,
        reference_load_side_flow_rate: float | Literal["Autosize"],
        reference_source_side_flow_rate: float | Literal["Autosize"],
        reference_cooling_capacity: float | Literal["Autosize"],
        reference_cooling_power_consumption: float | Literal["Autosize"],
        reference_coefficient_of_performance: float | None = 8,
        sizing_factor: float | None = 1,
        companion_heating_heat_pump_name: str | None = ...,
    ) -> None: ...

class AnyEvaporativeFluidCoolerSingleSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        design_air_flow_rate: float | Literal["Autosize"],
        design_air_flow_rate_fan_power: float | Literal["Autosize"],
        design_spray_water_flow_rate: float,
        performance_input_method: Literal[
            "StandardDesignCapacity", "UFactorTimesAreaAndDesignWaterFlowRate", "UserSpecifiedDesignCapacity"
        ],
        outdoor_air_inlet_node_name: str | None = ...,
        heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None = 1.25,
        standard_design_capacity: float | None = ...,
        design_air_flow_rate_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        design_water_flow_rate: float | Literal["Autosize"] | None = ...,
        user_specified_design_capacity: float | None = ...,
        design_entering_water_temperature: float | None = ...,
        design_entering_air_temperature: float | None = ...,
        design_entering_air_wet_bulb_temperature: float | None = ...,
        capacity_control: Literal["", "FanCycling", "FluidBypass"] | None = "FanCycling",
        sizing_factor: float | None = 1,
        evaporation_loss_mode: Literal["", "LossFactor", "SaturatedExit"] | None = "SaturatedExit",
        evaporation_loss_factor: float | None = ...,
        drift_loss_percent: float | None = 0.008,
        blowdown_calculation_mode: Literal["", "ConcentrationRatio", "ScheduledRate"] | None = "ConcentrationRatio",
        blowdown_concentration_ratio: float | None = 3,
        blowdown_makeup_water_usage_schedule_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
    ) -> None: ...

class PlantEquipmentOperationOutdoorWetBulb:
    def __call__(
        self,
        name: str,
        /,
        *,
        wet_bulb_temperature_range_1_lower_limit: float,
        wet_bulb_temperature_range_1_upper_limit: float,
        range_1_equipment_list_name: str,
        wet_bulb_temperature_range_2_lower_limit: float | None = ...,
        wet_bulb_temperature_range_2_upper_limit: float | None = ...,
        range_2_equipment_list_name: str | None = ...,
        wet_bulb_temperature_range_3_lower_limit: float | None = ...,
        wet_bulb_temperature_range_3_upper_limit: float | None = ...,
        range_3_equipment_list_name: str | None = ...,
        wet_bulb_temperature_range_4_lower_limit: float | None = ...,
        wet_bulb_temperature_range_4_upper_limit: float | None = ...,
        range_4_equipment_list_name: str | None = ...,
        wet_bulb_temperature_range_5_lower_limit: float | None = ...,
        wet_bulb_temperature_range_5_upper_limit: float | None = ...,
        range_5_equipment_list_name: str | None = ...,
        wet_bulb_temperature_range_6_lower_limit: float | None = ...,
        wet_bulb_temperature_range_6_upper_limit: float | None = ...,
        range_6_equipment_list_name: str | None = ...,
        wet_bulb_temperature_range_7_lower_limit: float | None = ...,
        wet_bulb_temperature_range_7_upper_limit: float | None = ...,
        range_7_equipment_list_name: str | None = ...,
        wet_bulb_temperature_range_8_lower_limit: float | None = ...,
        wet_bulb_temperature_range_8_upper_limit: float | None = ...,
        range_8_equipment_list_name: str | None = ...,
        wet_bulb_temperature_range_9_lower_limit: float | None = ...,
        wet_bulb_temperature_range_9_upper_limit: float | None = ...,
        range_9_equipment_list_name: str | None = ...,
        wet_bulb_temperature_range_10_lower_limit: float | None = ...,
        wet_bulb_temperature_range_10_upper_limit: float | None = ...,
        range_10_equipment_list_name: str | None = ...,
    ) -> None: ...

class PlantEquipmentOperationOutdoorWetBulbDifference:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_temperature_node_name: str,
        wet_bulb_temperature_difference_range_1_lower_limit: float,
        wet_bulb_temperature_difference_range_1_upper_limit: float,
        range_1_equipment_list_name: str,
        wet_bulb_temperature_difference_range_2_lower_limit: float | None = ...,
        wet_bulb_temperature_difference_range_2_upper_limit: float | None = ...,
        range_2_equipment_list_name: str | None = ...,
        wet_bulb_temperature_difference_range_3_lower_limit: float | None = ...,
        wet_bulb_temperature_difference_range_3_upper_limit: float | None = ...,
        range_3_equipment_list_name: str | None = ...,
        wet_bulb_temperature_difference_range_4_lower_limit: float | None = ...,
        wet_bulb_temperature_difference_range_4_upper_limit: float | None = ...,
        range_4_equipment_list_name: str | None = ...,
        wet_bulb_temperature_difference_range_5_lower_limit: float | None = ...,
        wet_bulb_temperature_difference_range_5_upper_limit: float | None = ...,
        range_5_equipment_list_name: str | None = ...,
        wet_bulb_temperature_difference_range_6_lower_limit: float | None = ...,
        wet_bulb_temperature_difference_range_6_upper_limit: float | None = ...,
        range_6_equipment_list_name: str | None = ...,
        wet_bulb_temperature_difference_range_7_lower_limit: float | None = ...,
        wet_bulb_temperature_difference_range_7_upper_limit: float | None = ...,
        range_7_equipment_list_name: str | None = ...,
        wet_bulb_temperature_difference_range_8_lower_limit: float | None = ...,
        wet_bulb_temperature_difference_range_8_upper_limit: float | None = ...,
        range_8_equipment_list_name: str | None = ...,
        wet_bulb_temperature_difference_range_9_lower_limit: float | None = ...,
        wet_bulb_temperature_difference_range_9_upper_limit: float | None = ...,
        range_9_equipment_list_name: str | None = ...,
        wet_bulb_temperature_difference_range_10_lower_limit: float | None = ...,
        wet_bulb_temperature_difference_range_10_upper_limit: float | None = ...,
        range_10_equipment_list_name: str | None = ...,
    ) -> None: ...

class SetpointManagerSingleZoneOneStageCooling:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_zone_name: str,
        setpoint_node_or_nodelist_name: str,
        cooling_stage_on_supply_air_setpoint_temperature: float | None = -99,
        cooling_stage_off_supply_air_setpoint_temperature: float | None = 99,
    ) -> None: ...

class RefrigerationCompressorRack:
    def __call__(
        self,
        name: str,
        /,
        *,
        compressor_rack_cop_function_of_temperature_curve_name: str,
        heat_rejection_location: Literal["", "Outdoors", "Zone"] | None = "Outdoors",
        design_compressor_rack_cop: float | None = 2,
        design_condenser_fan_power: float | None = 250,
        condenser_fan_power_function_of_temperature_curve_name: str | None = ...,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        water_cooled_condenser_inlet_node_name: str | None = ...,
        water_cooled_condenser_outlet_node_name: str | None = ...,
        water_cooled_loop_flow_type: Literal["", "ConstantFlow", "VariableFlow"] | None = "VariableFlow",
        water_cooled_condenser_outlet_temperature_schedule_name: str | None = ...,
        water_cooled_condenser_design_flow_rate: float | None = ...,
        water_cooled_condenser_maximum_flow_rate: float | None = ...,
        water_cooled_condenser_maximum_water_outlet_temperature: float | None = 55,
        water_cooled_condenser_minimum_water_inlet_temperature: float | None = 10,
        evaporative_condenser_availability_schedule_name: str | None = ...,
        evaporative_condenser_effectiveness: float | None = 0.9,
        evaporative_condenser_air_flow_rate: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        basin_heater_capacity: float | None = 200,
        basin_heater_setpoint_temperature: float | None = 2,
        design_evaporative_condenser_water_pump_power: float | Literal["", "Autocalculate"] | None = 1000,
        evaporative_water_supply_tank_name: str | None = ...,
        condenser_air_inlet_node_name: str | None = ...,
        end_use_subcategory: str | None = "General",
        refrigeration_case_name_or_walkin_name_or_caseandwalkinlist_name: str | None = ...,
        heat_rejection_zone_name: str | None = ...,
    ) -> None: ...

class ZoneHVACRefrigerationChillerSet:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        air_inlet_node_name: str | None = ...,
        air_outlet_node_name: str | None = ...,
        chillers: list[_g.ZoneHVACRefrigerationChillerSetChillersItem] = ...,
    ) -> None: ...

class AnyDemandManagerAssignmentList:
    def __call__(
        self,
        name: str,
        /,
        *,
        meter_name: str,
        demand_limit_safety_fraction: float,
        demand_window_length: int,
        demand_manager_priority: Literal["All", "Sequential"],
        demand_limit_schedule_name: str | None = ...,
        billing_period_schedule_name: str | None = ...,
        peak_period_schedule_name: str | None = ...,
        manager_data: list[_g.DemandManagerAssignmentListManagerDataItem] = ...,
    ) -> None: ...

class GeneratorFuelCell:
    def __call__(
        self,
        name: str,
        /,
        *,
        power_module_name: str,
        air_supply_name: str,
        fuel_supply_name: str,
        water_supply_name: str,
        auxiliary_heater_name: str,
        heat_exchanger_name: str,
        electrical_storage_name: str,
        inverter_name: str,
        stack_cooler_name: str | None = ...,
    ) -> None: ...

class GeneratorFuelCellAuxiliaryHeater:
    def __call__(
        self,
        name: str,
        /,
        *,
        excess_air_ratio: float | None = ...,
        ancillary_power_constant_term: float | None = ...,
        ancillary_power_linear_term: float | None = ...,
        skin_loss_u_factor_times_area_value: float | None = ...,
        skin_loss_destination: Literal["AirInletForFuelCell", "SurroundingZone"] | None = ...,
        zone_name_to_receive_skin_losses: str | None = ...,
        heating_capacity_units: Literal["Watts", "kmol/s"] | None = ...,
        maximum_heating_capacity_in_watts: float | None = ...,
        minimum_heating_capacity_in_watts: float | None = ...,
        maximum_heating_capacity_in_kmol_per_second: float | None = ...,
        minimum_heating_capacity_in_kmol_per_second: float | None = ...,
    ) -> None: ...

class UtilityCostVariable:
    def __call__(
        self,
        name: str,
        /,
        *,
        tariff_name: str,
        variable_type: Literal["", "Currency", "Demand", "Dimensionless", "Energy"] | None = "Dimensionless",
        january_value: float | None = ...,
        february_value: float | None = ...,
        march_value: float | None = ...,
        april_value: float | None = ...,
        may_value: float | None = ...,
        june_value: float | None = ...,
        july_value: float | None = ...,
        august_value: float | None = ...,
        september_value: float | None = ...,
        october_value: float | None = ...,
        november_value: float | None = ...,
        december_value: float | None = ...,
    ) -> None: ...

class LifeCycleCostUsePriceEscalation:
    def __call__(
        self,
        /,
        *,
        lcc_price_escalation_name: str,
        resource: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "ElectricityNet",
            "ElectricityProduced",
            "ElectricityPurchased",
            "ElectricitySurplusSold",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Water",
        ],
        escalation_start_year: int | None = ...,
        escalation_start_month: Literal[
            "",
            "April",
            "August",
            "December",
            "February",
            "January",
            "July",
            "June",
            "March",
            "May",
            "November",
            "October",
            "September",
        ]
        | None = "January",
        escalations: list[_g.LifeCycleCostUsePriceEscalationEscalationsItem] = ...,
    ) -> None: ...

class OutputDebuggingData:
    def __call__(
        self,
        /,
        *,
        report_debugging_data: Literal["", "No", "Yes"] | None = "No",
        report_during_warmup: Literal["", "No", "Yes"] | None = "No",
    ) -> None: ...
