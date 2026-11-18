"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class ZoneCapacitanceMultiplierResearchSpecial:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_name: str | None = ...,
        temperature_capacity_multiplier: float | None = 1,
        humidity_capacity_multiplier: float | None = 1,
        carbon_dioxide_capacity_multiplier: float | None = 1,
        generic_contaminant_capacity_multiplier: float | None = 1,
    ) -> None: ...

class RunPeriodControlSpecialDays:
    def __call__(
        self,
        name: str,
        /,
        *,
        start_date: str,
        duration: float | None = 1,
        special_day_type: Literal["", "CustomDay1", "CustomDay2", "Holiday", "SummerDesignDay", "WinterDesignDay"]
        | None = "Holiday",
    ) -> None: ...

class SiteGroundReflectance:
    def __call__(
        self,
        /,
        *,
        january_ground_reflectance: float | None = 0.2,
        february_ground_reflectance: float | None = 0.2,
        march_ground_reflectance: float | None = 0.2,
        april_ground_reflectance: float | None = 0.2,
        may_ground_reflectance: float | None = 0.2,
        june_ground_reflectance: float | None = 0.2,
        july_ground_reflectance: float | None = 0.2,
        august_ground_reflectance: float | None = 0.2,
        september_ground_reflectance: float | None = 0.2,
        october_ground_reflectance: float | None = 0.2,
        november_ground_reflectance: float | None = 0.2,
        december_ground_reflectance: float | None = 0.2,
    ) -> None: ...

class AnyMaterialPropertyPhaseChange:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        temperature_coefficient_for_thermal_conductivity: float | None = 0,
    ) -> None: ...

class ShadingOverhangProjection:
    def __call__(
        self,
        name: str,
        /,
        *,
        window_or_door_name: str,
        height_above_window_or_door: float | None = ...,
        tilt_angle_from_window_door: float | None = 90,
        left_extension_from_window_door_width: float | None = ...,
        right_extension_from_window_door_width: float | None = ...,
        depth_as_fraction_of_window_door_height: float | None = ...,
    ) -> None: ...

class SurfacePropertyHeatBalanceSourceTerm:
    def __call__(
        self,
        /,
        *,
        surface_name: str,
        inside_face_heat_source_term_schedule_name: str | None = ...,
        outside_face_heat_source_term_schedule_name: str | None = ...,
    ) -> None: ...

class SurfaceConvectionAlgorithmOutsideUserCurve:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        wind_speed_type_for_curve: Literal[
            "", "HeightAdjust", "ParallelComponent", "ParallelComponentHeightAdjust", "WeatherFile"
        ]
        | None = "HeightAdjust",
        hf_function_of_wind_speed_curve_name: str | None = ...,
        hn_function_of_temperature_difference_curve_name: str | None = ...,
        hn_function_of_temperature_difference_divided_by_height_curve_name: str | None = ...,
    ) -> None: ...

class AnySurfacePropertySurroundingSurfaces:
    def __call__(
        self,
        name: str,
        /,
        *,
        sky_view_factor: float | None = ...,
        sky_temperature_schedule_name: str | None = ...,
        ground_view_factor: float | None = ...,
        ground_temperature_schedule_name: str | None = ...,
        surfaces: list[_g.SurfacePropertySurroundingSurfacesSurfacesItem] = ...,
    ) -> None: ...

class SurfacePropertySurroundingSurfaces:
    def __call__(
        self,
        name: str,
        /,
        *,
        sky_view_factor: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        sky_temperature_schedule_name: str | None = ...,
        ground_view_factor: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        ground_temperature_schedule_name: str | None = ...,
        surfaces: list[_g.SurfacePropertySurroundingSurfacesSurfacesItem] = ...,
    ) -> None: ...

class RoomAirTemperaturePatternTwoGradient:
    def __call__(
        self,
        /,
        *,
        room_air_temperature_pattern_two_gradient_name: str,
        control_integer_for_pattern_control_schedule_name: int,
        thermostat_height: float | None = ...,
        return_air_height: float | None = ...,
        exhaust_air_height: float | None = ...,
        temperature_gradient_lower_bound: float | None = ...,
        temperature_gradient_upper_bound: float | None = ...,
        gradient_interpolation_mode: Literal[
            "OutdoorDryBulbTemperature",
            "SensibleCoolingLoad",
            "SensibleHeatingLoad",
            "ZoneAndOutdoorTemperatureDifference",
            "ZoneDryBulbTemperature",
        ]
        | None = ...,
        upper_temperature_bound: float | None = ...,
        lower_temperature_bound: float | None = ...,
        upper_heat_rate_bound: float | None = ...,
        lower_heat_rate_bound: float | None = ...,
    ) -> None: ...

class RoomAirSettingsUnderFloorAirDistributionInterior:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        number_of_diffusers: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        power_per_plume: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        design_effective_area_of_diffuser: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        diffuser_slot_angle_from_vertical: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        thermostat_height: float | None = 1.2,
        comfort_height: float | None = 1.1,
        temperature_difference_threshold_for_reporting: float | None = 0.4,
        floor_diffuser_type: Literal["", "Custom", "HorizontalSwirl", "LinearBarGrille", "Swirl", "VariableArea"]
        | None = "Swirl",
        transition_height: float | Literal["", "Autocalculate"] | None = 1.7,
        coefficient_a: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        coefficient_b: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        coefficient_c: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        coefficient_d: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        coefficient_e: float | Literal["", "Autocalculate"] | None = "Autocalculate",
    ) -> None: ...

class SteamEquipmentInstance:
    def __call__(
        self,
        name: str,
        /,
        *,
        steam_equipment_definition_name: str,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        multiplier: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class ZoneContaminantSourceAndSinkGenericDecaySource:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        schedule_name: str,
        initial_emission_rate: float | None = ...,
        delay_time_constant: float | None = ...,
    ) -> None: ...

class AnyAirflowNetworkSimulationControl:
    def __call__(
        self,
        name: str,
        /,
        *,
        airflownetwork_control: Literal[
            "",
            "MultizoneWithDistribution",
            "MultizoneWithDistributionOnlyDuringFanOperation",
            "MultizoneWithoutDistribution",
            "NoMultizoneOrDistribution",
        ]
        | None = "NoMultizoneOrDistribution",
        wind_pressure_coefficient_type: Literal["", "Input", "SurfaceAverageCalculation"]
        | None = "SurfaceAverageCalculation",
        height_selection_for_local_wind_pressure_calculation: Literal["", "ExternalNode", "OpeningHeight"]
        | None = "OpeningHeight",
        building_type: Literal["", "HighRise", "LowRise"] | None = "LowRise",
        maximum_number_of_iterations: int | None = 500,
        initialization_type: Literal["", "LinearInitializationMethod", "ZeroNodePressures"]
        | None = "ZeroNodePressures",
        relative_airflow_convergence_tolerance: float | None = 0.0001,
        absolute_airflow_convergence_tolerance: float | None = ...,
        convergence_acceleration_limit: float | None = -0.5,
        azimuth_angle_of_long_axis_of_building: float | None = 0,
        ratio_of_building_width_along_short_axis_to_width_along_long_axis: float | None = 1,
        height_dependence_of_external_node_temperature: Literal["", "No", "Yes"] | None = "No",
        solver: Literal["", "ConjugateGradient", "SkylineLU"] | None = "SkylineLU",
    ) -> None: ...

class AirflowNetworkMultiZoneExternalNode:
    def __call__(
        self,
        name: str,
        /,
        *,
        wind_pressure_coefficient_curve_name: str,
        external_node_height: float | None = 0,
        symmetric_wind_pressure_coefficient_curve: Literal["", "No", "Yes"] | None = "No",
        wind_angle_type: Literal["", "Absolute", "Relative"] | None = "Absolute",
    ) -> None: ...

class HVACTemplateSystemPackagedVAV:
    def __call__(
        self,
        name: str,
        /,
        *,
        system_availability_schedule_name: str | None = ...,
        supply_fan_maximum_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        supply_fan_minimum_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        supply_fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 1000,
        supply_fan_motor_efficiency: float | None = 0.9,
        supply_fan_motor_in_air_stream_fraction: float | None = 1,
        cooling_coil_type: Literal["", "TwoSpeedDX", "TwoSpeedHumidControlDX"] | None = "TwoSpeedDX",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_coil_setpoint_schedule_name: str | None = ...,
        cooling_coil_design_setpoint: float | None = 12.8,
        cooling_coil_gross_rated_total_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_cop: float | None = 3,
        heating_coil_type: Literal["", "Electric", "Gas", "HotWater", "None"] | None = "None",
        heating_coil_availability_schedule_name: str | None = ...,
        heating_coil_setpoint_schedule_name: str | None = ...,
        heating_coil_design_setpoint: float | None = 10,
        heating_coil_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        gas_heating_coil_efficiency: float | None = 0.8,
        gas_heating_coil_parasitic_electric_load: float | None = 0,
        maximum_outdoor_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_outdoor_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_outdoor_air_control_type: Literal["", "FixedMinimum", "ProportionalMinimum"]
        | None = "ProportionalMinimum",
        minimum_outdoor_air_schedule_name: str | None = ...,
        economizer_type: Literal[
            "",
            "DifferentialDryBulb",
            "DifferentialDryBulbAndEnthalpy",
            "DifferentialEnthalpy",
            "ElectronicEnthalpy",
            "FixedDewPointAndDryBulb",
            "FixedDryBulb",
            "FixedEnthalpy",
            "NoEconomizer",
        ]
        | None = "NoEconomizer",
        economizer_lockout: Literal["", "LockoutWithCompressor", "LockoutWithHeating", "NoLockout"]
        | None = "NoLockout",
        economizer_maximum_limit_dry_bulb_temperature: float | None = ...,
        economizer_maximum_limit_enthalpy: float | None = ...,
        economizer_maximum_limit_dewpoint_temperature: float | None = ...,
        economizer_minimum_limit_dry_bulb_temperature: float | None = ...,
        supply_plenum_name: str | None = ...,
        return_plenum_name: str | None = ...,
        supply_fan_part_load_power_coefficients: Literal[
            "",
            "ASHRAE90.1-2004AppendixG",
            "InletVaneDampers",
            "OutletDampers",
            "VariableSpeedMotor",
            "VariableSpeedMotorPressureReset",
        ]
        | None = "InletVaneDampers",
        night_cycle_control: Literal["", "CycleOnAny", "CycleOnAnyZoneFansOnly", "CycleOnControlZone", "StayOff"]
        | None = "StayOff",
        night_cycle_control_zone_name: str | None = ...,
        heat_recovery_type: Literal["", "Enthalpy", "None", "Sensible"] | None = "None",
        sensible_heat_recovery_effectiveness: float | None = 0.7,
        latent_heat_recovery_effectiveness: float | None = 0.65,
        cooling_coil_setpoint_reset_type: Literal[
            "", "None", "OutdoorAirTemperatureReset", "Warmest", "WarmestTemperatureFirst"
        ]
        | None = "None",
        heating_coil_setpoint_reset_type: Literal["", "None", "OutdoorAirTemperatureReset"] | None = "None",
        dehumidification_control_type: Literal["", "CoolReheat", "None"] | None = "None",
        dehumidification_control_zone_name: str | None = ...,
        dehumidification_setpoint: float | None = 60,
        humidifier_type: Literal["", "ElectricSteam", "None"] | None = "None",
        humidifier_availability_schedule_name: str | None = ...,
        humidifier_rated_capacity: float | None = ...,
        humidifier_rated_electric_power: float | Literal["", "Autosize"] | None = "Autosize",
        humidifier_control_zone_name: str | None = ...,
        humidifier_setpoint: float | None = 30,
        sizing_option: Literal["", "Coincident", "NonCoincident"] | None = "NonCoincident",
        return_fan: Literal["", "No", "Yes"] | None = "No",
        return_fan_total_efficiency: float | None = 0.7,
        return_fan_delta_pressure: float | None = 500,
        return_fan_motor_efficiency: float | None = 0.9,
        return_fan_motor_in_air_stream_fraction: float | None = 1,
        return_fan_part_load_power_coefficients: Literal[
            "",
            "ASHRAE90.1-2004AppendixG",
            "InletVaneDampers",
            "OutletDampers",
            "VariableSpeedMotor",
            "VariableSpeedMotorPressureReset",
        ]
        | None = "InletVaneDampers",
    ) -> None: ...

class HVACTemplatePlantChillerObjectReference:
    def __call__(
        self,
        name: str,
        /,
        *,
        chiller_name: str,
        chiller_object_type: Literal["", "Chiller:Electric:EIR", "Chiller:Electric:ReformulatedEIR"]
        | None = "Chiller:Electric:EIR",
        priority: float | None = ...,
    ) -> None: ...

class AnyZoneHVACCoolingPanelRadiantConvectiveWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        maximum_chilled_water_flow_rate: float | Literal["Autosize"],
        fraction_radiant: float,
        rated_inlet_water_temperature: float | None = 5,
        rated_inlet_space_temperature: float | None = 24,
        rated_water_mass_flow_rate: float | None = 0.063,
        cooling_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "CoolingDesignCapacity", "FractionOfAutosizedCoolingCapacity", "None"
        ]
        | None = "CoolingDesignCapacity",
        cooling_design_capacity: float | Literal["Autosize"] | None = ...,
        cooling_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_cooling_design_capacity: float | None = ...,
        control_type: Literal[
            "",
            "MeanAirTemperature",
            "MeanRadiantTemperature",
            "OperativeTemperature",
            "OutdoorDryBulbTemperature",
            "OutdoorWetBulbTemperature",
            "ZoneTotalLoad",
            "ZoneConvectiveLoad",
        ]
        | None = "MeanAirTemperature",
        cooling_control_throttling_range: float | None = 0.5,
        cooling_control_temperature_schedule_name: str | None = ...,
        condensation_control_type: Literal["", "Off", "SimpleOff", "VariableOff"] | None = "SimpleOff",
        condensation_control_dewpoint_offset: float | None = 1,
        fraction_of_radiant_energy_incident_on_people: float | None = ...,
        surface_fractions: list[_g.ZoneHVACCoolingPanelRadiantConvectiveWaterSurfaceFractionsItem] = ...,
    ) -> None: ...

class ZoneHVACLowTemperatureRadiantSurfaceGroup:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_fractions: list[_g.ZoneHVACLowTemperatureRadiantSurfaceGroupSurfaceFractionsItem] = ...,
    ) -> None: ...

class AnyAirTerminalSingleDuctVAVNoReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_outlet_node_name: str,
        air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        zone_minimum_air_flow_input_method: Literal["", "Constant", "FixedFlowRate", "Scheduled"] | None = "Constant",
        constant_minimum_air_flow_fraction: float | Literal["", "Autosize"] | None = "Autosize",
        fixed_minimum_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_air_flow_fraction_schedule_name: str | None = ...,
        design_specification_outdoor_air_object_name: str | None = ...,
    ) -> None: ...

class ZoneHVACAirDistributionUnit:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_distribution_unit_outlet_node_name: str,
        air_terminal_object_type: Literal[
            "AirTerminal:DualDuct:ConstantVolume",
            "AirTerminal:DualDuct:VAV",
            "AirTerminal:DualDuct:VAV:OutdoorAir",
            "AirTerminal:SingleDuct:ConstantVolume:CooledBeam",
            "AirTerminal:SingleDuct:ConstantVolume:FourPipeBeam",
            "AirTerminal:SingleDuct:ConstantVolume:FourPipeInduction",
            "AirTerminal:SingleDuct:ConstantVolume:NoReheat",
            "AirTerminal:SingleDuct:ConstantVolume:Reheat",
            "AirTerminal:SingleDuct:Mixer",
            "AirTerminal:SingleDuct:ParallelPIU:Reheat",
            "AirTerminal:SingleDuct:SeriesPIU:Reheat",
            "AirTerminal:SingleDuct:UserDefined",
            "AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat",
            "AirTerminal:SingleDuct:VAV:HeatAndCool:Reheat",
            "AirTerminal:SingleDuct:VAV:NoReheat",
            "AirTerminal:SingleDuct:VAV:Reheat",
            "AirTerminal:SingleDuct:VAV:Reheat:VariableSpeedFan",
        ],
        air_terminal_name: str,
        nominal_upstream_leakage_fraction: float | None = 0,
        constant_downstream_leakage_fraction: float | None = 0,
        design_specification_air_terminal_sizing_object_name: str | None = ...,
    ) -> None: ...

class AnyCoilHeatingDXMultiSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        fuel_type: Literal["Diesel", "Electricity", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2", "Propane"],
        number_of_speeds: int,
        speed_1_gross_rated_heating_capacity: float | Literal["Autosize"],
        speed_1_gross_rated_heating_cop: float,
        speed_1_rated_air_flow_rate: float | Literal["Autosize"],
        speed_1_heating_capacity_function_of_temperature_curve_name: str,
        speed_1_heating_capacity_function_of_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_1_energy_input_ratio_function_of_flow_fraction_curve_name: str,
        speed_1_part_load_fraction_correlation_curve_name: str,
        speed_2_gross_rated_heating_capacity: float | Literal["Autosize"],
        speed_2_gross_rated_heating_cop: float,
        speed_2_rated_air_flow_rate: float | Literal["Autosize"],
        speed_2_heating_capacity_function_of_temperature_curve_name: str,
        speed_2_heating_capacity_function_of_flow_fraction_curve_name: str,
        speed_2_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_2_energy_input_ratio_function_of_flow_fraction_curve_name: str,
        speed_2_part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -8,
        outdoor_dry_bulb_temperature_to_turn_on_compressor: float | None = ...,
        crankcase_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        defrost_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "ReverseCycle",
        defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["", "Autosize"] | None = 0,
        apply_part_load_fraction_to_speeds_greater_than_1: Literal["", "No", "Yes"] | None = "No",
        region_number_for_calculating_hspf: int | None = 4,
        speed_1_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_1_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_2_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_2_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_3_gross_rated_heating_capacity: float | Literal["Autosize"] | None = ...,
        speed_3_gross_rated_heating_cop: float | None = ...,
        speed_3_rated_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_3_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_3_heating_capacity_function_of_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        speed_3_part_load_fraction_correlation_curve_name: str | None = ...,
        speed_3_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_3_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_4_gross_rated_heating_capacity: float | Literal["Autosize"] | None = ...,
        speed_4_gross_rated_heating_cop: float | None = ...,
        speed_4_rated_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_4_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_4_heating_capacity_function_of_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        speed_4_part_load_fraction_correlation_curve_name: str | None = ...,
        speed_4_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_4_waste_heat_function_of_temperature_curve_name: str | None = ...,
        zone_name_for_evaporator_placement: str | None = ...,
        speed_1_secondary_coil_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_1_secondary_coil_fan_flow_scaling_factor: float | None = 1.25,
        speed_1_nominal_sensible_heat_ratio_of_secondary_coil: float | None = ...,
        speed_1_sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        speed_1_sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
        speed_2_secondary_coil_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_2_secondary_coil_fan_flow_scaling_factor: float | None = 1.25,
        speed_2_nominal_sensible_heat_ratio_of_secondary_coil: float | None = ...,
        speed_2_sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        speed_2_sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
        speed_3_secondary_coil_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_3_secondary_coil_fan_flow_scaling_factor: float | None = 1.25,
        speed_3_nominal_sensible_heat_ratio_of_secondary_coil: float | None = ...,
        speed_3_sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        speed_3_sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
        speed_4_secondary_coil_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_4_secondary_coil_fan_flow_scaling_factor: float | None = 1.25,
        speed_4_nominal_sensible_heat_ratio_of_secondary_coil: float | None = ...,
        speed_4_sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        speed_4_sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
    ) -> None: ...

class AnyHeatPumpWaterToWaterEquationFitHeating:
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
        reference_heating_capacity: float | Literal["Autosize"],
        reference_heating_power_consumption: float | Literal["Autosize"],
        reference_coefficient_of_performance: float | None = 7.5,
        sizing_factor: float | None = 1,
        companion_cooling_heat_pump_name: str | None = ...,
    ) -> None: ...

class GroundHeatExchangerSlinky:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        undisturbed_ground_temperature_model_type: Literal[
            "Site:GroundTemperature:Undisturbed:FiniteDifference",
            "Site:GroundTemperature:Undisturbed:KusudaAchenbach",
            "Site:GroundTemperature:Undisturbed:Xing",
        ],
        undisturbed_ground_temperature_model_name: str,
        design_flow_rate: float | None = 0.002,
        soil_thermal_conductivity: float | None = 1.08,
        soil_density: float | None = 962,
        soil_specific_heat: float | None = 2576,
        pipe_thermal_conductivity: float | None = 0.4,
        pipe_density: float | None = 641,
        pipe_specific_heat: float | None = 2405,
        pipe_outer_diameter: float | None = 0.02667,
        pipe_thickness: float | None = 0.002413,
        heat_exchanger_configuration: Literal["Horizontal", "Vertical"] | None = ...,
        coil_diameter: float | None = 1,
        coil_pitch: float | None = 0.2,
        trench_depth: float | None = 1.8,
        trench_length: float | None = 10,
        number_of_trenches: int | None = 1,
        horizontal_spacing_between_pipes: float | None = 2,
        maximum_length_of_simulation: float | None = ...,
    ) -> None: ...

class PlantEquipmentOperationThermalEnergyStorage:
    def __call__(
        self,
        name: str,
        /,
        *,
        on_peak_schedule: str,
        charging_availability_schedule: str,
        non_charging_chilled_water_temperature: float,
        charging_chilled_water_temperature: float,
        component_1_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ],
        component_1_name: str,
        component_1_demand_calculation_node_name: str,
        component_1_setpoint_node_name: str,
        component_1_flow_rate: float | Literal["Autosize"],
        component_1_operation_type: Literal["Cooling", "Dual", "Heating"],
        component_2_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_2_name: str | None = ...,
        component_2_demand_calculation_node_name: str | None = ...,
        component_2_setpoint_node_name: str | None = ...,
        component_2_flow_rate: float | Literal["Autosize"] | None = ...,
        component_2_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_3_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_3_name: str | None = ...,
        component_3_demand_calculation_node_name: str | None = ...,
        component_3_setpoint_node_name: str | None = ...,
        component_3_flow_rate: float | Literal["Autosize"] | None = ...,
        component_3_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_4_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:ASHRAE205",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_4_name: str | None = ...,
        component_4_demand_calculation_node_name: str | None = ...,
        component_4_setpoint_node_name: str | None = ...,
        component_4_flow_rate: float | Literal["Autosize"] | None = ...,
        component_4_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_5_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:ASHRAE205",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_5_name: str | None = ...,
        component_5_demand_calculation_node_name: str | None = ...,
        component_5_setpoint_node_name: str | None = ...,
        component_5_flow_rate: float | Literal["Autosize"] | None = ...,
        component_5_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_6_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:ASHRAE205",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_6_name: str | None = ...,
        component_6_demand_calculation_node_name: str | None = ...,
        component_6_setpoint_node_name: str | None = ...,
        component_6_flow_rate: float | Literal["Autosize"] | None = ...,
        component_6_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_7_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:ASHRAE205",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_7_name: str | None = ...,
        component_7_demand_calculation_node_name: str | None = ...,
        component_7_setpoint_node_name: str | None = ...,
        component_7_flow_rate: float | Literal["Autosize"] | None = ...,
        component_7_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_8_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:ASHRAE205",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_8_name: str | None = ...,
        component_8_demand_calculation_node_name: str | None = ...,
        component_8_setpoint_node_name: str | None = ...,
        component_8_flow_rate: float | Literal["Autosize"] | None = ...,
        component_8_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_9_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:ASHRAE205",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_9_name: str | None = ...,
        component_9_demand_calculation_node_name: str | None = ...,
        component_9_setpoint_node_name: str | None = ...,
        component_9_flow_rate: float | Literal["Autosize"] | None = ...,
        component_9_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_10_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:ASHRAE205",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_10_name: str | None = ...,
        component_10_demand_calculation_node_name: str | None = ...,
        component_10_setpoint_node_name: str | None = ...,
        component_10_flow_rate: float | Literal["Autosize"] | None = ...,
        component_10_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
    ) -> None: ...

class EnergyManagementSystemSubroutine:
    def __call__(self, name: str, /, *, lines: list[_g.EnergyManagementSystemSubroutineLinesItem] = ...) -> None: ...

class ExternalInterfaceActuator:
    def __call__(
        self,
        name: str,
        /,
        *,
        actuated_component_unique_name: str,
        actuated_component_type: str,
        actuated_component_control_type: str,
        optional_initial_value: float | None = ...,
    ) -> None: ...

class AvailabilityManagerScheduledOn:
    def __call__(self, name: str, /, *, schedule_name: str) -> None: ...

class SetpointManagerSingleZoneOneStageHeating:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_zone_name: str,
        setpoint_node_or_nodelist_name: str,
        heating_stage_on_supply_air_setpoint_temperature: float | None = 99,
        heating_stage_off_supply_air_setpoint_temperature: float | None = -99,
    ) -> None: ...

class RefrigerationSubcooler:
    def __call__(
        self,
        name: str,
        /,
        *,
        subcooler_type: Literal["", "LiquidSuction", "Mechanical"] | None = "LiquidSuction",
        liquid_suction_design_subcooling_temperature_difference: float | None = ...,
        design_liquid_inlet_temperature: float | None = ...,
        design_vapor_inlet_temperature: float | None = ...,
        capacity_providing_system: str | None = ...,
        outlet_control_temperature: float | None = ...,
    ) -> None: ...

class GeneratorFuelCellWaterSupply:
    def __call__(
        self,
        name: str,
        /,
        *,
        reformer_water_flow_rate_function_of_fuel_rate_curve_name: str | None = ...,
        reformer_water_pump_power_function_of_fuel_rate_curve_name: str | None = ...,
        pump_heat_loss_factor: float | None = ...,
        water_temperature_modeling_mode: Literal[
            "MainsWaterTemperature", "TemperatureFromAirNode", "TemperatureFromSchedule", "TemperatureFromWaterNode"
        ]
        | None = ...,
        water_temperature_reference_node_name: str | None = ...,
        water_temperature_schedule_name: str | None = ...,
    ) -> None: ...

class GeneratorFuelCellInverter:
    def __call__(
        self,
        name: str,
        /,
        *,
        inverter_efficiency_calculation_mode: Literal["Constant", "Quadratic"] | None = ...,
        inverter_efficiency: float | None = ...,
        efficiency_function_of_dc_power_curve_name: str | None = ...,
    ) -> None: ...

class ComponentCostAdjustments:
    def __call__(
        self,
        /,
        *,
        miscellaneous_cost_per_conditioned_area: float | None = ...,
        design_and_engineering_fees: float | None = ...,
        contractor_fee: float | None = ...,
        contingency: float | None = ...,
        permits_bonding_and_insurance: float | None = ...,
        commissioning_fee: float | None = ...,
        regional_adjustment_factor: float | None = ...,
    ) -> None: ...

class OutputControlResilienceSummaries:
    def __call__(
        self, /, *, heat_index_algorithm: Literal["", "Extended", "Simplified"] | None = "Simplified"
    ) -> None: ...

class OutputVariable:
    def __call__(
        self,
        /,
        *,
        variable_name: str,
        key_value: str | None = "*",
        reporting_frequency: Literal[
            "", "Annual", "Daily", "Detailed", "Environment", "Hourly", "Monthly", "RunPeriod", "Timestep"
        ]
        | None = "Hourly",
        schedule_name: str | None = ...,
    ) -> None: ...
