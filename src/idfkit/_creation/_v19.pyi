"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Any, Literal

class MaterialNoMass_v8_9_to_v26_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        roughness: Literal["MediumRough", "MediumSmooth", "Rough", "Smooth", "VeryRough", "VerySmooth"],
        thermal_resistance: float,
        thermal_absorptance: float | None = 0.9,
        solar_absorptance: float | None = 0.7,
        visible_absorptance: float | None = 0.7,
    ) -> None: ...

class BoilerHotWater_v9_3_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        fuel_type: Literal[
            "Coal",
            "Diesel",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ],
        nominal_thermal_efficiency: float,
        boiler_water_inlet_node_name: str,
        boiler_water_outlet_node_name: str,
        nominal_capacity: float | Literal["Autosize"] | None = ...,
        efficiency_curve_temperature_evaluation_variable: Literal["EnteringBoiler", "LeavingBoiler"] | None = ...,
        normalized_boiler_efficiency_curve_name: str | None = ...,
        design_water_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_part_load_ratio: float | None = 0,
        maximum_part_load_ratio: float | None = 1,
        optimum_part_load_ratio: float | None = 1,
        water_outlet_upper_temperature_limit: float | None = 99.9,
        boiler_flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"]
        | None = "NotModulated",
        parasitic_electric_load: float | None = 0,
        sizing_factor: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class DaylightingControls_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        daylighting_method: Literal["", "DElight", "SplitFlux"] | None = "SplitFlux",
        availability_schedule_name: str | None = ...,
        lighting_control_type: Literal["", "Continuous", "ContinuousOff", "Stepped"] | None = "Continuous",
        minimum_input_power_fraction_for_continuous_or_continuousoff_dimming_control: float | None = 0.3,
        minimum_light_output_fraction_for_continuous_or_continuousoff_dimming_control: float | None = 0.2,
        number_of_stepped_control_steps: float | None = 1,
        probability_lighting_will_be_reset_when_needed_in_manual_stepped_control: float | None = 1,
        glare_calculation_daylighting_reference_point_name: str | None = ...,
        glare_calculation_azimuth_angle_of_view_direction_clockwise_from_zone_y_axis: float | None = 0,
        maximum_allowable_discomfort_glare_index: float | None = 22,
        delight_gridding_resolution: float | None = ...,
        control_data: list[Any] = ...,
    ) -> None: ...

class CoilHeatingWaterToAirHeatPumpEquationFit_v8_9_to_v9_4:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        rated_air_flow_rate: float | Literal["Autosize"],
        rated_water_flow_rate: float | Literal["Autosize"],
        gross_rated_heating_capacity: float | Literal["Autosize"],
        gross_rated_heating_cop: float,
        heating_capacity_coefficient_1: float,
        heating_capacity_coefficient_2: float,
        heating_capacity_coefficient_3: float,
        heating_capacity_coefficient_4: float,
        heating_capacity_coefficient_5: float,
        heating_power_consumption_coefficient_1: float,
        heating_power_consumption_coefficient_2: float,
        heating_power_consumption_coefficient_3: float,
        heating_power_consumption_coefficient_4: float,
        heating_power_consumption_coefficient_5: float,
    ) -> None: ...

class ChillerHeaterAbsorptionDirectFired_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        condenser_inlet_node_name: str,
        hot_water_inlet_node_name: str,
        hot_water_outlet_node_name: str,
        nominal_cooling_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        heating_to_cooling_capacity_ratio: float | None = 0.8,
        fuel_input_to_cooling_output_ratio: float | None = 0.97,
        fuel_input_to_heating_output_ratio: float | None = 1.25,
        electric_input_to_cooling_output_ratio: float | None = 0.01,
        electric_input_to_heating_output_ratio: float | None = 0,
        condenser_outlet_node_name: str | None = ...,
        minimum_part_load_ratio: float | None = 0.1,
        maximum_part_load_ratio: float | None = 1,
        optimum_part_load_ratio: float | None = 1,
        design_entering_condenser_water_temperature: float | None = 29,
        design_leaving_chilled_water_temperature: float | None = 7,
        design_chilled_water_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        design_condenser_water_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        design_hot_water_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        fuel_input_to_cooling_output_ratio_function_of_temperature_curve_name: str | None = ...,
        fuel_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str | None = ...,
        electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str | None = ...,
        electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str | None = ...,
        heating_capacity_function_of_cooling_capacity_curve_name: str | None = ...,
        fuel_input_to_heat_output_ratio_during_heating_only_operation_curve_name: str | None = ...,
        temperature_curve_input_variable: Literal["", "EnteringCondenser", "LeavingCondenser"]
        | None = "EnteringCondenser",
        condenser_type: Literal["", "AirCooled", "WaterCooled"] | None = "WaterCooled",
        chilled_water_temperature_lower_limit: float | None = 2,
        fuel_higher_heating_value: float | None = 0,
        fuel_type: Literal[
            "", "Diesel", "FuelOil#1", "FuelOil#2", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2", "PropaneGas"
        ]
        | None = "NaturalGas",
        sizing_factor: float | None = 1,
    ) -> None: ...

class ZoneControlThermostatStagedDualSetpoint_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_name: str,
        number_of_heating_stages: float,
        stage_1_heating_temperature_offset: float,
        number_of_cooling_stages: float,
        stage_1_cooling_temperature_offset: float,
        heating_temperature_setpoint_schedule_name: str | None = ...,
        heating_throttling_temperature_range: float | None = 1.1,
        stage_2_heating_temperature_offset: float | None = ...,
        stage_3_heating_temperature_offset: float | None = ...,
        stage_4_heating_temperature_offset: float | None = ...,
        cooling_temperature_setpoint_base_schedule_name: str | None = ...,
        cooling_throttling_temperature_range: float | None = 1.1,
        stage_2_cooling_temperature_offset: float | None = ...,
        stage_3_cooling_temperature_offset: float | None = ...,
        stage_4_cooling_temperature_offset: float | None = ...,
    ) -> None: ...

class AirTerminalSingleDuctParallelPIUReheat_v24_2_to_v25_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        maximum_primary_air_flow_rate: float | Literal["Autosize"],
        maximum_secondary_air_flow_rate: float | Literal["Autosize"],
        minimum_primary_air_flow_fraction: float | Literal["Autosize"],
        fan_on_flow_fraction: float | Literal["Autosize"],
        reheat_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        reheat_coil_name: str,
        availability_schedule_name: str | None = ...,
        supply_air_inlet_node_name: str | None = ...,
        secondary_air_inlet_node_name: str | None = ...,
        outlet_node_name: str | None = ...,
        reheat_coil_air_inlet_node_name: str | None = ...,
        zone_mixer_name: str | None = ...,
        fan_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        convergence_tolerance: float | None = 0.001,
        fan_control_type: Literal["", "ConstantSpeed", "VariableSpeed"] | None = "ConstantSpeed",
        minimum_fan_turn_down_ratio: float | None = 0.3,
        heating_control_type: Literal["Modulated", "Staged"] | None = ...,
        design_heating_discharge_air_temperature: float | None = 32.1,
        high_limit_heating_discharge_air_temperature: float | None = 37.7,
    ) -> None: ...

class CoilHeatingDXMultiSpeed_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        fuel_type: Literal[
            "Diesel",
            "Electricity",
            "FuelOil#1",
            "FuelOil#2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ],
        number_of_speeds: float,
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
        region_number_for_calculating_hspf: float | None = 4,
        speed_1_rated_supply_air_fan_power_per_volume_flow_rate: float | None = 773.3,
        speed_1_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_1_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_2_rated_supply_air_fan_power_per_volume_flow_rate: float | None = 773.3,
        speed_2_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_2_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_3_gross_rated_heating_capacity: float | Literal["Autosize"] | None = ...,
        speed_3_gross_rated_heating_cop: float | None = ...,
        speed_3_rated_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_3_rated_supply_air_fan_power_per_volume_flow_rate: float | None = 773.3,
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
        speed_4_rated_supply_air_fan_power_per_volume_flow_rate: float | None = 773.3,
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

class ZoneHVACPackagedTerminalAirConditioner_v8_9_to_v22_1:
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
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        availability_schedule_name: str | None = ...,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outdoor_air_mixer_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
        capacity_control_method: Literal["", "None", "SingleZoneVAV"] | None = "None",
        minimum_supply_air_temperature_in_cooling_mode: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_supply_air_temperature_in_heating_mode: float | Literal["", "Autosize"] | None = "Autosize",
    ) -> None: ...

class EnergyManagementSystemTrendVariable_v8_9_to_v22_1:
    def __call__(self, name: str, /, *, ems_variable_name: str, number_of_timesteps_to_be_logged: float) -> None: ...

class AirTerminalSingleDuctVAVReheat_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        damper_air_outlet_node_name: str,
        air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        reheat_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        reheat_coil_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        zone_minimum_air_flow_input_method: Literal["", "Constant", "FixedFlowRate", "Scheduled"] | None = "Constant",
        constant_minimum_air_flow_fraction: float | Literal["", "Autosize"] | None = "Autosize",
        fixed_minimum_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_air_flow_fraction_schedule_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        convergence_tolerance: float | None = 0.001,
        damper_heating_action: Literal["", "Normal", "Reverse", "ReverseWithLimits"] | None = "ReverseWithLimits",
        maximum_flow_per_zone_floor_area_during_reheat: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_flow_fraction_during_reheat: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_reheat_air_temperature: float | None = ...,
        design_specification_outdoor_air_object_name: str | None = ...,
    ) -> None: ...

class RoomAirNodeAirflowNetworkHVACEquipment_v9_3_to_v24_1:
    def __call__(self, name: str = "", /, *, equipment_fractions: list[Any] = ...) -> None: ...

class ZoneHVACLowTemperatureRadiantElectric_v8_9_to_v9_3:
    def __call__(
        self,
        name: str,
        /,
        *,
        heating_setpoint_temperature_schedule_name: str,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        surface_name_or_radiant_surface_group_name: str | None = ...,
        heating_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = 1,
        temperature_control_type: Literal[
            "",
            "MeanAirTemperature",
            "MeanRadiantTemperature",
            "OperativeTemperature",
            "OutdoorDryBulbTemperature",
            "OutdoorWetBulbTemperature",
        ]
        | None = "MeanAirTemperature",
        heating_throttling_range: float | None = 0,
    ) -> None: ...

class PythonPluginVariables_v9_3:
    def __call__(
        self,
        name: str,
        /,
        *,
        variable_name_1: str | None = ...,
        variable_name_2: str | None = ...,
        variable_name_3: str | None = ...,
        variable_name_4: str | None = ...,
        variable_name_5: str | None = ...,
    ) -> None: ...

class ZoneHVACLowTemperatureRadiantVariableFlow_v9_5_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        design_object: str | None = ...,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        surface_name_or_radiant_surface_group_name: str | None = ...,
        hydronic_tubing_length: float | Literal["", "Autosize"] | None = "Autosize",
        heating_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_hot_water_flow: float | Literal["Autosize"] | None = ...,
        heating_water_inlet_node_name: str | None = ...,
        heating_water_outlet_node_name: str | None = ...,
        cooling_design_capacity: float | Literal["Autosize"] | None = ...,
        maximum_cold_water_flow: float | Literal["Autosize"] | None = ...,
        cooling_water_inlet_node_name: str | None = ...,
        cooling_water_outlet_node_name: str | None = ...,
        number_of_circuits: Literal["", "CalculateFromCircuitLength", "OnePerSurface"] | None = "OnePerSurface",
        circuit_length: float | None = 106.7,
    ) -> None: ...

class TableTwoIndependentVariables_v9_0_to_v9_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        curve_type: Literal["BiQuadratic", "QuadraticLinear"] | None = ...,
        interpolation_method: Literal[
            "", "EvaluateCurveToLimits", "LagrangeInterpolationLinearExtrapolation", "LinearInterpolationOfTable"
        ]
        | None = "LagrangeInterpolationLinearExtrapolation",
        minimum_value_of_x: float | None = ...,
        maximum_value_of_x: float | None = ...,
        minimum_value_of_y: float | None = ...,
        maximum_value_of_y: float | None = ...,
        minimum_table_output: float | None = ...,
        maximum_table_output: float | None = ...,
        input_unit_type_for_x: Literal[
            "", "Angle", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        input_unit_type_for_y: Literal[
            "", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow", "Wavelength"
        ]
        | None = "Dimensionless",
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
        normalization_reference: float | None = ...,
        external_file_name: str | None = ...,
        values: list[Any] = ...,
    ) -> None: ...

class ExternalInterfaceFunctionalMockupUnitExportToSchedule_v8_9_to_v25_1:
    def __call__(
        self,
        /,
        *,
        schedule_name: str,
        fmu_variable_name: str,
        initial_value: float,
        schedule_type_limits_names: str | None = ...,
    ) -> None: ...
