"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Any, Literal

class Building:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        north_axis: float | None = 0,
        terrain: Literal["", "City", "Country", "Ocean", "Suburbs", "Urban"] | None = "Suburbs",
        loads_convergence_tolerance_value: float | None = 0.04,
        temperature_convergence_tolerance_value: float | None = 0.4,
        solar_distribution: Literal[
            "",
            "FullExterior",
            "FullExteriorWithReflections",
            "FullInteriorAndExterior",
            "FullInteriorAndExteriorWithReflections",
            "MinimalShadowing",
        ]
        | None = "FullExterior",
        maximum_number_of_warmup_days: int | None = 25,
        minimum_number_of_warmup_days: int | None = 1,
        construction_assignment_set_name: str | None = ...,
    ) -> None: ...

class SizingPeriodDesignDay:
    def __call__(
        self,
        name: str,
        /,
        *,
        month: int,
        day_of_month: int,
        day_type: Literal[
            "CustomDay1",
            "CustomDay2",
            "Friday",
            "Holiday",
            "Monday",
            "Saturday",
            "SummerDesignDay",
            "Sunday",
            "Thursday",
            "Tuesday",
            "Wednesday",
            "WinterDesignDay",
        ],
        wind_speed: float,
        wind_direction: float,
        maximum_dry_bulb_temperature: float | None = ...,
        daily_dry_bulb_temperature_range: float | None = 0,
        dry_bulb_temperature_range_modifier_type: Literal[
            "", "DefaultMultipliers", "DifferenceSchedule", "MultiplierSchedule", "TemperatureProfileSchedule"
        ]
        | None = "DefaultMultipliers",
        dry_bulb_temperature_range_modifier_day_schedule_name: str | None = ...,
        humidity_condition_type: Literal[
            "",
            "DewPoint",
            "Enthalpy",
            "HumidityRatio",
            "RelativeHumiditySchedule",
            "WetBulb",
            "WetBulbProfileDefaultMultipliers",
            "WetBulbProfileDifferenceSchedule",
            "WetBulbProfileMultiplierSchedule",
        ]
        | None = "WetBulb",
        wetbulb_or_dewpoint_at_maximum_dry_bulb: float | None = ...,
        humidity_condition_day_schedule_name: str | None = ...,
        humidity_ratio_at_maximum_dry_bulb: float | None = ...,
        enthalpy_at_maximum_dry_bulb: float | None = ...,
        daily_wet_bulb_temperature_range: float | None = ...,
        barometric_pressure: float | None = ...,
        rain_indicator: Literal["", "No", "Yes"] | None = "No",
        snow_indicator: Literal["", "No", "Yes"] | None = "No",
        daylight_saving_time_indicator: Literal["", "No", "Yes"] | None = "No",
        solar_model_indicator: Literal["", "ASHRAEClearSky", "ASHRAETau", "ASHRAETau2017", "Schedule", "ZhangHuang"]
        | None = "ASHRAEClearSky",
        beam_solar_day_schedule_name: str | None = ...,
        diffuse_solar_day_schedule_name: str | None = ...,
        ashrae_clear_sky_optical_depth_for_beam_irradiance_taub_: float | None = 0,
        ashrae_clear_sky_optical_depth_for_diffuse_irradiance_taud_: float | None = 0,
        sky_clearness: float | None = 0,
        maximum_number_warmup_days: int | None = ...,
        begin_environment_reset_mode: Literal["", "FullResetAtBeginEnvironment", "SuppressAllBeginEnvironmentResets"]
        | None = "FullResetAtBeginEnvironment",
        ashrae_clear_sky_optical_depth_for_beam_irradiance_taub: float | None = ...,
        ashrae_clear_sky_optical_depth_for_diffuse_irradiance_taud: float | None = ...,
    ) -> None: ...

class AnyZone:
    def __call__(
        self,
        name: str,
        /,
        *,
        direction_of_relative_north: float | None = 0,
        x_origin: float | None = 0,
        y_origin: float | None = 0,
        z_origin: float | None = 0,
        type: int | None = 1,
        multiplier: int | None = 1,
        ceiling_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        volume: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        floor_area: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        zone_inside_convection_algorithm: Literal[
            "", "AdaptiveConvectionAlgorithm", "CeilingDiffuser", "Simple", "TARP", "TrombeWall"
        ]
        | None = ...,
        zone_outside_convection_algorithm: Literal[
            "", "AdaptiveConvectionAlgorithm", "DOE-2", "MoWiTT", "SimpleCombined", "TARP"
        ]
        | None = ...,
        part_of_total_floor_area: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None: ...

class AnyFloorAdiabatic:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 180,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        width: float | None = ...,
    ) -> None: ...

class GroundHeatTransferBasementXFACE:
    def __call__(self, /) -> None: ...

class GroundHeatTransferBasementZFACE:
    def __call__(self, /) -> None: ...

class AnyRoomAirNodeAirflowNetworkInternalGains:
    def __call__(self, name: str = "", /, *, gains: list[Any] = ...) -> None: ...

class ElectricEquipmentInstance:
    def __call__(
        self,
        name: str,
        /,
        *,
        electric_equipment_definition_name: str,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        multiplier: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class SurfaceContaminantSourceAndSinkGenericPressureDriven:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_name: str,
        generation_schedule_name: str,
        design_generation_rate_coefficient: float | None = ...,
        generation_exponent: float | None = ...,
    ) -> None: ...

class ZoneInfiltrationFlowCoefficient:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_space_name: str,
        flow_coefficient: float,
        stack_coefficient: float,
        wind_coefficient: float,
        shelter_factor: float,
        schedule_name: str | None = ...,
        pressure_exponent: float | None = 0.67,
    ) -> None: ...

class AirflowNetworkZoneControlPressureController:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_zone_name: str,
        control_object_type: Literal[
            "AirflowNetwork:Distribution:Component:ReliefAirFlow", "AirflowNetwork:MultiZone:Component:ZoneExhaustFan"
        ],
        control_object_name: str,
        pressure_setpoint_schedule_name: str,
        pressure_control_availability_schedule_name: str | None = ...,
    ) -> None: ...

class AirflowNetworkIntraZoneNode:
    def __call__(
        self, name: str, /, *, roomair_node_airflownetwork_name: str, zone_name: str, node_height: float | None = 0
    ) -> None: ...

class AirflowNetworkIntraZoneLinkage:
    def __call__(
        self,
        name: str,
        /,
        *,
        node_1_name: str,
        node_2_name: str,
        component_name: str | None = ...,
        airflownetwork_multizone_surface_name: str | None = ...,
    ) -> None: ...

class HVACTemplateSystemDedicatedOutdoorAir:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        system_availability_schedule_name: str | None = ...,
        air_outlet_type: Literal["", "DirectIntoZone"] | None = "DirectIntoZone",
        supply_fan_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 1000,
        supply_fan_motor_efficiency: float | None = 0.9,
        supply_fan_motor_in_air_stream_fraction: float | None = 1,
        supply_fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "DrawThrough",
        cooling_coil_type: Literal[
            "",
            "ChilledWater",
            "ChilledWaterDetailedFlatModel",
            "HeatExchangerAssistedChilledWater",
            "HeatExchangerAssistedDX",
            "None",
            "TwoSpeedDX",
            "TwoStageDX",
            "TwoStageHumidityControlDX",
        ]
        | None = "ChilledWater",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_coil_setpoint_control_type: Literal["", "FixedSetpoint", "OutdoorAirTemperatureReset", "Scheduled"]
        | None = "FixedSetpoint",
        cooling_coil_design_setpoint: float | None = 12.8,
        cooling_coil_setpoint_schedule_name: str | None = ...,
        cooling_coil_setpoint_at_outdoor_dry_bulb_low: float | None = 15.6,
        cooling_coil_reset_outdoor_dry_bulb_low: float | None = 15.6,
        cooling_coil_setpoint_at_outdoor_dry_bulb_high: float | None = 12.8,
        cooling_coil_reset_outdoor_dry_bulb_high: float | None = 23.3,
        dx_cooling_coil_gross_rated_total_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        dx_cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["", "Autosize"] | None = "Autosize",
        dx_cooling_coil_gross_rated_cop: float | None = 3,
        heating_coil_type: Literal["", "Electric", "Gas", "HotWater", "None"] | None = "HotWater",
        heating_coil_availability_schedule_name: str | None = ...,
        heating_coil_setpoint_control_type: Literal["", "FixedSetpoint", "OutdoorAirTemperatureReset", "Scheduled"]
        | None = "FixedSetpoint",
        heating_coil_design_setpoint: float | None = 12.2,
        heating_coil_setpoint_schedule_name: str | None = ...,
        heating_coil_setpoint_at_outdoor_dry_bulb_low: float | None = 15,
        heating_coil_reset_outdoor_dry_bulb_low: float | None = 7.8,
        heating_coil_setpoint_at_outdoor_dry_bulb_high: float | None = 12.2,
        heating_coil_reset_outdoor_dry_bulb_high: float | None = 12.2,
        gas_heating_coil_efficiency: float | None = 0.8,
        gas_heating_coil_parasitic_electric_load: float | None = 0,
        heat_recovery_type: Literal["", "Enthalpy", "None", "Sensible"] | None = "None",
        heat_recovery_sensible_effectiveness: float | None = 0.7,
        heat_recovery_latent_effectiveness: float | None = 0.65,
        heat_recovery_heat_exchanger_type: Literal["", "Plate", "Rotary"] | None = "Plate",
        heat_recovery_frost_control_type: Literal[
            "", "ExhaustAirRecirculation", "ExhaustOnly", "MinimumExhaustTemperature", "None"
        ]
        | None = "None",
        dehumidification_control_type: Literal[
            "", "CoolReheatDesuperheater", "CoolReheatHeatingCoil", "Multimode", "None"
        ]
        | None = "None",
        dehumidification_setpoint: float | None = 0.00924,
        humidifier_type: Literal["", "ElectricSteam", "None"] | None = "None",
        humidifier_availability_schedule_name: str | None = ...,
        humidifier_rated_capacity: float | None = ...,
        humidifier_rated_electric_power: float | Literal["", "Autosize"] | None = "Autosize",
        humidifier_constant_setpoint: float | None = 0.003,
        dehumidification_setpoint_schedule_name: str | None = ...,
        humidifier_setpoint_schedule_name: str | None = ...,
    ) -> None: ...

class ZoneControlThermostatOperativeTemperature:
    def __call__(
        self,
        /,
        *,
        thermostat_name: str,
        radiative_fraction_input_mode: Literal["Constant", "Scheduled"],
        fixed_radiative_fraction: float | None = ...,
        radiative_fraction_schedule_name: str | None = ...,
        adaptive_comfort_model_type: Literal[
            "",
            "AdaptiveASH5580PercentUpperLine",
            "AdaptiveASH5590PercentUpperLine",
            "AdaptiveASH55CentralLine",
            "AdaptiveCEN15251CategoryIIIUpperLine",
            "AdaptiveCEN15251CategoryIIUpperLine",
            "AdaptiveCEN15251CategoryIUpperLine",
            "AdaptiveCEN15251CentralLine",
            "None",
        ]
        | None = "None",
    ) -> None: ...

class ZoneHVACEnergyRecoveryVentilatorController:
    def __call__(
        self,
        name: str,
        /,
        *,
        temperature_high_limit: float | None = ...,
        temperature_low_limit: float | None = ...,
        enthalpy_high_limit: float | None = ...,
        dewpoint_temperature_limit: float | None = ...,
        electronic_enthalpy_limit_curve_name: str | None = ...,
        exhaust_air_temperature_limit: Literal["", "ExhaustAirTemperatureLimit", "NoExhaustAirTemperatureLimit"]
        | None = "NoExhaustAirTemperatureLimit",
        exhaust_air_enthalpy_limit: Literal["", "ExhaustAirEnthalpyLimit", "NoExhaustAirEnthalpyLimit"]
        | None = "NoExhaustAirEnthalpyLimit",
        time_of_day_economizer_flow_control_schedule_name: str | None = ...,
        high_humidity_control_flag: Literal["", "No", "Yes"] | None = "No",
        humidistat_control_zone_name: str | None = ...,
        high_humidity_outdoor_air_flow_ratio: float | None = 1,
        control_high_indoor_humidity_based_on_outdoor_humidity_ratio: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None: ...

class AnyZoneHVACHybridUnitaryHVAC:
    def __call__(
        self,
        name: str,
        /,
        *,
        return_air_node_name: str,
        outdoor_air_node_name: str,
        supply_air_node_name: str,
        availability_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        minimum_supply_air_temperature_schedule_name: str | None = ...,
        maximum_supply_air_temperature_schedule_name: str | None = ...,
        minimum_supply_air_humidity_ratio_schedule_name: str | None = ...,
        maximum_supply_air_humidity_ratio_schedule_name: str | None = ...,
        method_to_choose_controlled_inputs_and_part_runtime_fraction: Literal["", "Automatic", "User Defined"]
        | None = "Automatic",
        relief_node_name: str | None = ...,
        system_maximum_supply_air_flow_rate: float | None = ...,
        external_static_pressure_at_system_maximum_supply_air_flow_rate: float | None = ...,
        scaling_factor: float | None = 1,
        minimum_time_between_mode_change: float | None = 10,
        first_fuel_type: Literal[
            "",
            "Coal",
            "Diesel",
            "DistrictCooling",
            "Electricity",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
        ]
        | None = "Electricity",
        second_fuel_type: Literal[
            "",
            "Coal",
            "Diesel",
            "DistrictCooling",
            "Electricity",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
        ]
        | None = "None",
        third_fuel_type: Literal[
            "",
            "Coal",
            "Diesel",
            "DistrictCooling",
            "Electricity",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
        ]
        | None = "None",
        objective_function_to_minimize: Literal["", "Electricity Use", "Second Fuel Use", "Third Fuel Use", "Water Use"]
        | None = "Electricity Use",
        design_specification_outdoor_air_object_name: str | None = ...,
        mode_0_name: str | None = ...,
        mode_0_supply_air_temperature_lookup_table_name: str | None = ...,
        mode_0_supply_air_humidity_ratio_lookup_table_name: str | None = ...,
        mode_0_system_electric_power_lookup_table_name: str | None = ...,
        mode_0_supply_fan_electric_power_lookup_table_name: str | None = ...,
        mode_0_external_static_pressure_lookup_table_name: str | None = ...,
        mode_0_system_second_fuel_consumption_lookup_table_name: str | None = ...,
        mode_0_system_third_fuel_consumption_lookup_table_name: str | None = ...,
        mode_0_system_water_use_lookup_table_name: str | None = ...,
        mode_0_outdoor_air_fraction: float | None = 0,
        mode_0_supply_air_mass_flow_rate_ratio: float | None = 0,
        modes: list[Any] = ...,
    ) -> None: ...

class AnyCoilCoolingWaterDetailedGeometry:
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
        maximum_water_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        tube_outside_surface_area: float | Literal["", "Autosize"] | None = "Autosize",
        total_tube_inside_area: float | Literal["", "Autosize"] | None = "Autosize",
        fin_surface_area: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_airflow_area: float | Literal["", "Autosize"] | None = "Autosize",
        coil_depth: float | Literal["", "Autosize"] | None = "Autosize",
        fin_diameter: float | Literal["", "Autosize"] | None = "Autosize",
        fin_thickness: float | None = 0.0015,
        tube_inside_diameter: float | None = 0.01445,
        tube_outside_diameter: float | None = 0.0159,
        tube_thermal_conductivity: float | None = 386,
        fin_thermal_conductivity: float | None = 204,
        fin_spacing: float | None = 0.0018,
        tube_depth_spacing: float | None = 0.026,
        number_of_tube_rows: float | None = 4,
        number_of_tubes_per_row: float | Literal["", "Autosize"] | None = "Autosize",
        condensate_collection_water_storage_tank_name: str | None = ...,
        design_water_temperature_difference: float | None = ...,
    ) -> None: ...

class CoilCoolingDXTwoStageWithHumidityControlMode:
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
        crankcase_heater_capacity_function_of_temperature_curve_name: str | None = ...,
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
    ) -> None: ...

class CoilHeatingElectric:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        efficiency: float | None = 1,
        nominal_capacity: float | Literal["Autosize"] | None = ...,
        temperature_setpoint_node_name: str | None = ...,
    ) -> None: ...

class CoilHeatingWaterToAirHeatPumpVariableSpeedEquationFit:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_to_refrigerant_hx_water_inlet_node_name: str,
        water_to_refrigerant_hx_water_outlet_node_name: str,
        indoor_air_inlet_node_name: str,
        indoor_air_outlet_node_name: str,
        energy_part_load_fraction_curve_name: str,
        speed_1_reference_unit_gross_rated_heating_capacity: float,
        speed_1_reference_unit_gross_rated_heating_cop: float,
        speed_1_reference_unit_rated_air_flow_rate: float,
        speed_1_reference_unit_rated_water_flow_rate: float,
        speed_1_heating_capacity_function_of_temperature_curve_name: str,
        speed_1_total_heating_capacity_function_of_air_flow_fraction_curve_name: str,
        speed_1_heating_capacity_function_of_water_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_1_energy_input_ratio_function_of_air_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_water_flow_fraction_curve_name: str,
        speed_1_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float,
        speed_1_waste_heat_function_of_temperature_curve_name: str,
        availability_schedule_name: str | None = ...,
        number_of_speeds: int | None = 2,
        nominal_speed_level: int | None = 2,
        rated_heating_capacity_at_selected_nominal_speed_level: float | Literal["", "Autosize"] | None = "Autosize",
        rated_air_flow_rate_at_selected_nominal_speed_level: float | Literal["", "Autosize"] | None = "Autosize",
        rated_water_flow_rate_at_selected_nominal_speed_level: float | Literal["", "Autosize"] | None = "Autosize",
        speed_2_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_2_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_2_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_2_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_2_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_2_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_heating_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_2_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_2_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_3_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_3_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_3_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_3_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_3_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_3_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_heating_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_3_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_3_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_4_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_4_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_4_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_4_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_4_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_4_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_heating_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_4_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_4_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_5_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_5_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_5_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_5_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_5_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_5_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_heating_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_5_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_5_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_6_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_6_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_6_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_6_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_6_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_6_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_heating_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_6_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_6_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_7_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_7_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_7_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_7_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_7_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_7_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_heating_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_7_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_7_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_8_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_8_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_8_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_8_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_8_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_8_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_heating_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_8_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_8_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_9_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_9_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_9_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_9_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_9_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_9_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_heating_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_9_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_9_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_10_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_10_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_10_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_10_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_10_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_10_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_heating_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_10_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_10_waste_heat_function_of_temperature_curve_name: str | None = ...,
    ) -> None: ...

class AnyAirLoopHVACUnitaryHeatPumpWaterToAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        supply_air_flow_rate: float | Literal["Autosize"],
        controlling_zone_or_thermostat_location: str,
        supply_air_fan_object_type: Literal["Fan:OnOff"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:WaterToAirHeatPump:EquationFit",
            "Coil:Heating:WaterToAirHeatPump:ParameterEstimation",
            "Coil:Heating:WaterToAirHeatPump:VariableSpeedEquationFit",
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:WaterToAirHeatPump:EquationFit",
            "Coil:Cooling:WaterToAirHeatPump:ParameterEstimation",
            "Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit",
        ],
        cooling_coil_name: str,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        supplemental_heating_coil_name: str,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        heating_convergence: float | None = 0.001,
        cooling_convergence: float | None = 0.001,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        outdoor_dry_bulb_temperature_sensor_node_name: str | None = ...,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        dehumidification_control_type: Literal["", "CoolReheat", "None"] | None = "None",
        heat_pump_coil_water_flow_mode: Literal["", "Constant", "ConstantOnDemand", "Cycling"] | None = "Cycling",
    ) -> None: ...

class AirLoopHVACOutdoorAirSystem:
    def __call__(
        self, name: str, /, *, outdoor_air_equipment_list_name: str, controller_list_name: str | None = ...
    ) -> None: ...

class PumpVariableSpeedCondensate:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        design_steam_volume_flow_rate: float | Literal["Autosize"] | None = ...,
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        coefficient_1_of_the_part_load_performance_curve: float | None = 0,
        coefficient_2_of_the_part_load_performance_curve: float | None = 1,
        coefficient_3_of_the_part_load_performance_curve: float | None = 0,
        coefficient_4_of_the_part_load_performance_curve: float | None = 0,
        pump_flow_rate_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["", "PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class ChillerElectricReformulatedEIR:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_capacity: float | Literal["Autosize"],
        reference_cop: float,
        cooling_capacity_function_of_temperature_curve_name: str,
        electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str,
        electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        condenser_inlet_node_name: str,
        condenser_outlet_node_name: str,
        reference_leaving_chilled_water_temperature: float | None = 6.67,
        reference_leaving_condenser_water_temperature: float | None = 35,
        reference_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        reference_condenser_water_flow_rate: float | Literal["Autosize"] | None = ...,
        electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_type: Literal[
            "", "LeavingCondenserWaterTemperature", "Lift"
        ]
        | None = "LeavingCondenserWaterTemperature",
        minimum_part_load_ratio: float | None = 0.1,
        maximum_part_load_ratio: float | None = 1,
        optimum_part_load_ratio: float | None = 1,
        minimum_unloading_ratio: float | None = 0.2,
        fraction_of_compressor_electric_consumption_rejected_by_condenser: float | None = 1,
        leaving_chilled_water_lower_temperature_limit: float | None = 2,
        chiller_flow_mode_type: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"]
        | None = "NotModulated",
        design_heat_recovery_water_flow_rate: float | Literal["", "Autosize"] | None = 0,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        sizing_factor: float | None = 1,
        condenser_heat_recovery_relative_capacity_fraction: float | None = ...,
        heat_recovery_inlet_high_temperature_limit_schedule_name: str | None = ...,
        heat_recovery_leaving_temperature_setpoint_node_name: str | None = ...,
        end_use_subcategory: str | None = "General",
        condenser_flow_control: Literal[
            "", "ConstantFlow", "ModulatedChillerPLR", "ModulatedDeltaTemperature", "ModulatedLoopPLR"
        ]
        | None = "ConstantFlow",
        condenser_loop_flow_rate_fraction_function_of_loop_part_load_ratio_curve_name: str | None = ...,
        temperature_difference_across_condenser_schedule_name: str | None = ...,
        condenser_minimum_flow_fraction: float | None = 0.2,
        thermosiphon_capacity_fraction_curve_name: str | None = ...,
        thermosiphon_minimum_temperature_difference: float | None = 0,
    ) -> None: ...

class ChillerEngineDriven:
    def __call__(
        self,
        name: str,
        /,
        *,
        nominal_capacity: float | Literal["Autosize"],
        nominal_cop: float,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        temperature_rise_coefficient: float,
        fuel_type: Literal[
            "Diesel", "FuelOilNo1", "FuelOilNo2", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2", "Propane"
        ],
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        design_condenser_inlet_temperature: float | None = ...,
        design_chilled_water_outlet_temperature: float | None = ...,
        design_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_condenser_water_flow_rate: float | Literal["Autosize"] | None = ...,
        coefficient_1_of_capacity_ratio_curve: float | None = ...,
        coefficient_2_of_capacity_ratio_curve: float | None = ...,
        coefficient_3_of_capacity_ratio_curve: float | None = ...,
        coefficient_1_of_power_ratio_curve: float | None = ...,
        coefficient_2_of_power_ratio_curve: float | None = ...,
        coefficient_3_of_power_ratio_curve: float | None = ...,
        coefficient_1_of_full_load_ratio_curve: float | None = ...,
        coefficient_2_of_full_load_ratio_curve: float | None = ...,
        coefficient_3_of_full_load_ratio_curve: float | None = ...,
        chilled_water_outlet_temperature_lower_limit: float | None = ...,
        fuel_use_curve_name: str | None = ...,
        jacket_heat_recovery_curve_name: str | None = ...,
        lube_heat_recovery_curve_name: str | None = ...,
        total_exhaust_energy_curve_name: str | None = ...,
        exhaust_temperature_curve_name: str | None = ...,
        coefficient_1_of_u_factor_times_area_curve: float | None = ...,
        coefficient_2_of_u_factor_times_area_curve: float | None = ...,
        maximum_exhaust_flow_per_unit_of_power_output: float | None = ...,
        design_minimum_exhaust_temperature: float | None = ...,
        fuel_higher_heating_value: float | None = ...,
        design_heat_recovery_water_flow_rate: float | Literal["", "Autosize"] | None = 0,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        chiller_flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"]
        | None = "NotModulated",
        maximum_temperature_for_heat_recovery_at_heat_recovery_outlet_node: float | None = 60,
        sizing_factor: float | None = 1,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        condenser_heat_recovery_relative_capacity_fraction: float | None = ...,
    ) -> None: ...

class CoolingTowerPerformanceCoolTools:
    def __call__(
        self,
        name: str,
        /,
        *,
        minimum_inlet_air_wet_bulb_temperature: float,
        maximum_inlet_air_wet_bulb_temperature: float,
        minimum_range_temperature: float,
        maximum_range_temperature: float,
        minimum_approach_temperature: float,
        maximum_approach_temperature: float,
        minimum_water_flow_rate_ratio: float,
        maximum_water_flow_rate_ratio: float,
        coefficient_1: float,
        coefficient_2: float,
        coefficient_3: float,
        coefficient_4: float,
        coefficient_5: float,
        coefficient_6: float,
        coefficient_7: float,
        coefficient_8: float,
        coefficient_9: float,
        coefficient_10: float,
        coefficient_11: float,
        coefficient_12: float,
        coefficient_13: float,
        coefficient_14: float,
        coefficient_15: float,
        coefficient_16: float,
        coefficient_17: float,
        coefficient_18: float,
        coefficient_19: float,
        coefficient_20: float,
        coefficient_21: float,
        coefficient_22: float,
        coefficient_23: float,
        coefficient_24: float,
        coefficient_25: float,
        coefficient_26: float,
        coefficient_27: float,
        coefficient_28: float,
        coefficient_29: float,
        coefficient_30: float,
        coefficient_31: float,
        coefficient_32: float,
        coefficient_33: float,
        coefficient_34: float,
        coefficient_35: float,
    ) -> None: ...

class AnyGroundHeatExchangerVerticalArray:
    def __call__(
        self,
        name: str,
        /,
        *,
        ghe_vertical_properties_object_name: str,
        number_of_boreholes_in_x_direction: int,
        number_of_boreholes_in_y_direction: int,
        borehole_spacing: float,
    ) -> None: ...

class GroundHeatExchangerVerticalSingle:
    def __call__(
        self, name: str, /, *, ghe_vertical_properties_object_name: str, x_location: float, y_location: float
    ) -> None: ...

class PlantEquipmentOperationOutdoorDewpoint:
    def __call__(
        self,
        name: str,
        /,
        *,
        dewpoint_temperature_range_1_lower_limit: float,
        dewpoint_temperature_range_1_upper_limit: float,
        range_1_equipment_list_name: str,
        dewpoint_temperature_range_2_lower_limit: float | None = ...,
        dewpoint_temperature_range_2_upper_limit: float | None = ...,
        range_2_equipment_list_name: str | None = ...,
        dewpoint_temperature_range_3_lower_limit: float | None = ...,
        dewpoint_temperature_range_3_upper_limit: float | None = ...,
        range_3_equipment_list_name: str | None = ...,
        dewpoint_temperature_range_4_lower_limit: float | None = ...,
        dewpoint_temperature_range_4_upper_limit: float | None = ...,
        range_4_equipment_list_name: str | None = ...,
        dewpoint_temperature_range_5_lower_limit: float | None = ...,
        dewpoint_temperature_range_5_upper_limit: float | None = ...,
        range_5_equipment_list_name: str | None = ...,
        dewpoint_temperature_range_6_lower_limit: float | None = ...,
        dewpoint_temperature_range_6_upper_limit: float | None = ...,
        range_6_equipment_list_name: str | None = ...,
        dewpoint_temperature_range_7_lower_limit: float | None = ...,
        dewpoint_temperature_range_7_upper_limit: float | None = ...,
        range_7_equipment_list_name: str | None = ...,
        dewpoint_temperature_range_8_lower_limit: float | None = ...,
        dewpoint_temperature_range_8_upper_limit: float | None = ...,
        range_8_equipment_list_name: str | None = ...,
        dewpoint_temperature_range_9_lower_limit: float | None = ...,
        dewpoint_temperature_range_9_upper_limit: float | None = ...,
        range_9_equipment_list_name: str | None = ...,
        dewpoint_temperature_range_10_lower_limit: float | None = ...,
        dewpoint_temperature_range_10_upper_limit: float | None = ...,
        range_10_equipment_list_name: str | None = ...,
    ) -> None: ...

class AnyCoilUserDefined:
    def __call__(
        self,
        name: str,
        /,
        *,
        model_setup_and_sizing_program_calling_manager_name: str,
        number_of_air_connections: int,
        air_connection_1_inlet_node_name: str,
        air_connection_1_outlet_node_name: str,
        overall_model_simulation_program_calling_manager_name: str | None = ...,
        air_connection_2_inlet_node_name: str | None = ...,
        air_connection_2_outlet_node_name: str | None = ...,
        plant_connection_is_used: Literal["No", "Yes"] | None = ...,
        plant_connection_inlet_node_name: str | None = ...,
        plant_connection_outlet_node_name: str | None = ...,
        supply_inlet_water_storage_tank_name: str | None = ...,
        collection_outlet_water_storage_tank_name: str | None = ...,
        ambient_zone_name: str | None = ...,
    ) -> None: ...

class SetpointManagerReturnTemperatureHotWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        plant_loop_supply_outlet_node: str,
        plant_loop_supply_inlet_node: str,
        return_temperature_setpoint_input_type: Literal["Constant", "ReturnTemperatureSetpoint", "Scheduled"],
        minimum_supply_temperature_setpoint: float | None = 77,
        maximum_supply_temperature_setpoint: float | None = 82,
        return_temperature_setpoint_constant_value: float | None = 71,
        return_temperature_setpoint_schedule_name: str | None = ...,
    ) -> None: ...

class OutputTableAnnual:
    def __call__(
        self,
        name: str,
        /,
        *,
        filter: str | None = ...,
        schedule_name: str | None = ...,
        variable_details: list[Any] = ...,
    ) -> None: ...

class PythonPluginTrendVariable:
    def __call__(
        self, name: str, /, *, name_of_a_python_plugin_variable: str, number_of_timesteps_to_be_logged: int
    ) -> None: ...
