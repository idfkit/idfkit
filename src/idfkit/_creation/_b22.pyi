"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Any, Literal

from typing_extensions import Never

class WindowGapDeflectionState:
    def __call__(
        self,
        name: str,
        /,
        *,
        deflected_thickness: float | None = 0,
        initial_temperature: float | None = 25,
        initial_pressure: float | None = 101325,
    ) -> None: ...

class AnyMaterialPropertyHeatAndMoistureTransferSorptionIsotherm:
    def __call__(
        self,
        /,
        *,
        material_name: str,
        number_of_isotherm_coordinates: int,
        relative_humidity_fraction_1: float,
        moisture_content_1: float,
        relative_humidity_fraction_2: float | None = ...,
        moisture_content_2: float | None = ...,
        relative_humidity_fraction_3: float | None = ...,
        moisture_content_3: float | None = ...,
        relative_humidity_fraction_4: float | None = ...,
        moisture_content_4: float | None = ...,
        relative_humidity_fraction_5: float | None = ...,
        moisture_content_5: float | None = ...,
        relative_humidity_fraction_6: float | None = ...,
        moisture_content_6: float | None = ...,
        relative_humidity_fraction_7: float | None = ...,
        moisture_content_7: float | None = ...,
        relative_humidity_fraction_8: float | None = ...,
        moisture_content_8: float | None = ...,
        relative_humidity_fraction_9: float | None = ...,
        moisture_content_9: float | None = ...,
        relative_humidity_fraction_10: float | None = ...,
        moisture_content_10: float | None = ...,
        relative_humidity_fraction_11: float | None = ...,
        moisture_content_11: float | None = ...,
        relative_humidity_fraction_12: float | None = ...,
        moisture_content_12: float | None = ...,
        relative_humidity_fraction_13: float | None = ...,
        moisture_content_13: float | None = ...,
        relative_humidity_fraction_14: float | None = ...,
        moisture_content_14: float | None = ...,
        relative_humidity_fraction_15: float | None = ...,
        moisture_content_15: float | None = ...,
        relative_humidity_fraction_16: float | None = ...,
        moisture_content_16: float | None = ...,
        relative_humidity_fraction_17: float | None = ...,
        moisture_content_17: float | None = ...,
        relative_humidity_fraction_18: float | None = ...,
        moisture_content_18: float | None = ...,
        relative_humidity_fraction_19: float | None = ...,
        moisture_content_19: float | None = ...,
        relative_humidity_fraction_20: float | None = ...,
        moisture_content_20: float | None = ...,
        relative_humidity_fraction_21: float | None = ...,
        moisture_content_21: float | None = ...,
        relative_humidity_fraction_22: float | None = ...,
        moisture_content_22: float | None = ...,
        relative_humidity_fraction_23: float | None = ...,
        moisture_content_23: float | None = ...,
        relative_humidity_fraction_24: float | None = ...,
        moisture_content_24: float | None = ...,
        relative_humidity_fraction_25: float | None = ...,
        moisture_content_25: float | None = ...,
    ) -> None: ...

class MaterialPropertyHeatAndMoistureTransferSuction:
    def __call__(
        self,
        /,
        *,
        material_name: str,
        number_of_suction_points: int,
        moisture_content_1: float,
        liquid_transport_coefficient_1: float,
        moisture_content_2: float | None = ...,
        liquid_transport_coefficient_2: float | None = ...,
        moisture_content_3: float | None = ...,
        liquid_transport_coefficient_3: float | None = ...,
        moisture_content_4: float | None = ...,
        liquid_transport_coefficient_4: float | None = ...,
        moisture_content_5: float | None = ...,
        liquid_transport_coefficient_5: float | None = ...,
        moisture_content_6: float | None = ...,
        liquid_transport_coefficient_6: float | None = ...,
        moisture_content_7: float | None = ...,
        liquid_transport_coefficient_7: float | None = ...,
        moisture_content_8: float | None = ...,
        liquid_transport_coefficient_8: float | None = ...,
        moisture_content_9: float | None = ...,
        liquid_transport_coefficient_9: float | None = ...,
        moisture_content_10: float | None = ...,
        liquid_transport_coefficient_10: float | None = ...,
        moisture_content_11: float | None = ...,
        liquid_transport_coefficient_11: float | None = ...,
        moisture_content_12: float | None = ...,
        liquid_transport_coefficient_12: float | None = ...,
        moisture_content_13: float | None = ...,
        liquid_transport_coefficient_13: float | None = ...,
        moisture_content_14: float | None = ...,
        liquid_transport_coefficient_14: float | None = ...,
        moisture_content_15: float | None = ...,
        liquid_transport_coefficient_15: float | None = ...,
        moisture_content_16: float | None = ...,
        liquid_transport_coefficient_16: float | None = ...,
        moisture_content_17: float | None = ...,
        liquid_transport_coefficient_17: float | None = ...,
        moisture_content_18: float | None = ...,
        liquid_transport_coefficient_18: float | None = ...,
        moisture_content_19: float | None = ...,
        liquid_transport_coefficient_19: float | None = ...,
        moisture_content_20: float | None = ...,
        liquid_transport_coefficient_20: float | None = ...,
        moisture_content_21: float | None = ...,
        liquid_transport_coefficient_21: float | None = ...,
        moisture_content_22: float | None = ...,
        liquid_transport_coefficient_22: float | None = ...,
        moisture_content_23: float | None = ...,
        liquid_transport_coefficient_23: float | None = ...,
        moisture_content_24: float | None = ...,
        liquid_transport_coefficient_24: float | None = ...,
        moisture_content_25: float | None = ...,
        liquid_transport_coefficient_25: float | None = ...,
    ) -> None: ...

class Construction:
    def __call__(
        self,
        name: str,
        /,
        *,
        outside_layer: str,
        layer_2: str | None = ...,
        layer_3: str | None = ...,
        layer_4: str | None = ...,
        layer_5: str | None = ...,
        layer_6: str | None = ...,
        layer_7: str | None = ...,
        layer_8: str | None = ...,
        layer_9: str | None = ...,
        layer_10: str | None = ...,
    ) -> None: ...

class SurfaceConstructionAssignments:
    def __call__(
        self,
        name: str,
        /,
        *,
        floor_construction_name: str | None = ...,
        wall_construction_name: str | None = ...,
        roof_ceiling_construction_name: str | None = ...,
    ) -> None: ...

class AnyRoof:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 0,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        width: float | None = ...,
    ) -> None: ...

class GroundHeatTransferSlabBldgProps:
    def __call__(
        self,
        /,
        *,
        iyrs_number_of_years_to_iterate: float | None = 10,
        shape_slab_shape: float | None = ...,
        hbldg_building_height: float | None = ...,
        tin1_january_indoor_average_temperature_setpoint: float | None = 22,
        tin2_february_indoor_average_temperature_setpoint: float | None = 22,
        tin3_march_indoor_average_temperature_setpoint: float | None = 22,
        tin4_april_indoor_average_temperature_setpoint: float | None = 22,
        tin5_may_indoor_average_temperature_setpoint: float | None = 22,
        tin6_june_indoor_average_temperature_setpoint: float | None = 22,
        tin7_july_indoor_average_temperature_setpoint: float | None = 22,
        tin8_august_indoor_average_temperature_setpoint: float | None = 22,
        tin9_september_indoor_average_temperature_setpoint: float | None = 22,
        tin10_october_indoor_average_temperature_setpoint: float | None = 22,
        tin11_november_indoor_average_temperature_setpoint: float | None = 22,
        tin12_december_indoor_average_temperature_setpoint: float | None = 22,
        tinamp_daily_indoor_sine_wave_variation_amplitude: float | None = 0,
        convtol_convergence_tolerance: float | None = 0.1,
    ) -> None: ...

class GroundHeatTransferBasementBldgData:
    def __call__(
        self,
        /,
        *,
        dwall_wall_thickness: float | None = 0.2,
        dslab_floor_slab_thickness: float | None = 0.1,
        dgravxy_width_of_gravel_pit_beside_basement_wall: float | None = 0.3,
        dgravzn_gravel_depth_extending_above_the_floor_slab: float | None = 0.2,
        dgravzp_gravel_depth_below_the_floor_slab: float | None = 0.1,
    ) -> None: ...

class LightsDefinition:
    def __call__(
        self,
        name: str,
        /,
        *,
        design_level_calculation_method: Literal["", "LightingLevel", "Watts/Area", "Watts/Person"]
        | None = "LightingLevel",
        lighting_level: float | None = ...,
        watts_per_floor_area: float | None = ...,
        watts_per_person: float | None = ...,
        return_air_fraction: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_visible: float | None = 0,
        return_air_fraction_calculated_from_plenum_temperature: Literal["", "No", "Yes"] | None = "No",
        return_air_fraction_function_of_plenum_temperature_coefficient_1: float | None = 0,
        return_air_fraction_function_of_plenum_temperature_coefficient_2: float | None = 0,
    ) -> None: ...

class ElectricEquipmentDefinition:
    def __call__(
        self,
        name: str,
        /,
        *,
        design_level_calculation_method: Literal["", "EquipmentLevel", "Watts/Area", "Watts/Person"]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        watts_per_floor_area: float | None = ...,
        watts_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
    ) -> None: ...

class AnyHotWaterEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        schedule_name: str,
        design_level_calculation_method: Literal[
            "", "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class AirflowNetworkMultiZoneComponentZoneExhaustFan:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_mass_flow_coefficient_when_the_zone_exhaust_fan_is_off_at_reference_conditions: float,
        air_mass_flow_exponent_when_the_zone_exhaust_fan_is_off: float | None = 0.65,
        reference_crack_conditions: str | None = ...,
    ) -> None: ...

class HVACTemplatePlantChilledWaterLoop:
    def __call__(
        self,
        name: str,
        /,
        *,
        pump_schedule_name: str | None = ...,
        pump_control_type: Literal["", "Continuous", "Intermittent"] | None = "Intermittent",
        chiller_plant_operation_scheme_type: Literal["", "Default", "UserDefined"] | None = "Default",
        chiller_plant_equipment_operation_schemes_name: str | None = ...,
        chilled_water_setpoint_schedule_name: str | None = ...,
        chilled_water_design_setpoint: float | None = 7.22,
        chilled_water_pump_configuration: Literal[
            "", "ConstantPrimaryNoSecondary", "ConstantPrimaryVariableSecondary", "VariablePrimaryNoSecondary"
        ]
        | None = "ConstantPrimaryNoSecondary",
        primary_chilled_water_pump_rated_head: float | None = 179352,
        secondary_chilled_water_pump_rated_head: float | None = 179352,
        condenser_plant_operation_scheme_type: Literal["", "Default", "UserDefined"] | None = "Default",
        condenser_equipment_operation_schemes_name: str | None = ...,
        condenser_water_temperature_control_type: Literal["OutdoorWetBulbTemperature", "SpecifiedSetpoint"]
        | None = ...,
        condenser_water_setpoint_schedule_name: str | None = ...,
        condenser_water_design_setpoint: float | None = 29.4,
        condenser_water_pump_rated_head: float | None = 179352,
        chilled_water_setpoint_reset_type: Literal["", "None", "OutdoorAirTemperatureReset"] | None = "None",
        chilled_water_setpoint_at_outdoor_dry_bulb_low: float | None = 12.2,
        chilled_water_reset_outdoor_dry_bulb_low: float | None = 15.6,
        chilled_water_setpoint_at_outdoor_dry_bulb_high: float | None = 6.7,
        chilled_water_reset_outdoor_dry_bulb_high: float | None = 26.7,
        chilled_water_primary_pump_type: Literal[
            "",
            "FiveHeaderedPumps",
            "FourHeaderedPumps",
            "PumpPerChiller",
            "SinglePump",
            "ThreeHeaderedPumps",
            "TwoHeaderedPumps",
        ]
        | None = "SinglePump",
        chilled_water_secondary_pump_type: Literal[
            "", "FiveHeaderedPumps", "FourHeaderedPumps", "SinglePump", "ThreeHeaderedPumps", "TwoHeaderedPumps"
        ]
        | None = "SinglePump",
        condenser_water_pump_type: Literal[
            "",
            "FiveHeaderedPumps",
            "FourHeaderedPumps",
            "PumpPerTower",
            "SinglePump",
            "ThreeHeaderedPumps",
            "TwoHeaderedPumps",
        ]
        | None = "SinglePump",
        chilled_water_supply_side_bypass_pipe: Literal["", "No", "Yes"] | None = "Yes",
        chilled_water_demand_side_bypass_pipe: Literal["", "No", "Yes"] | None = "Yes",
        condenser_water_supply_side_bypass_pipe: Literal["", "No", "Yes"] | None = "Yes",
        condenser_water_demand_side_bypass_pipe: Literal["", "No", "Yes"] | None = "Yes",
        fluid_type: Literal[
            "",
            "EthyleneGlycol30",
            "EthyleneGlycol40",
            "EthyleneGlycol50",
            "EthyleneGlycol60",
            "PropyleneGlycol30",
            "PropyleneGlycol40",
            "PropyleneGlycol50",
            "PropyleneGlycol60",
            "Water",
        ]
        | None = "Water",
        loop_design_delta_temperature: float | None = 6.67,
        minimum_outdoor_dry_bulb_temperature: float | None = ...,
        chilled_water_load_distribution_scheme: Literal[
            "", "Optimal", "SequentialLoad", "SequentialUniformPLR", "UniformLoad", "UniformPLR"
        ]
        | None = "SequentialLoad",
        condenser_water_load_distribution_scheme: Literal[
            "", "Optimal", "SequentialLoad", "SequentialUniformPLR", "UniformLoad", "UniformPLR"
        ]
        | None = "SequentialLoad",
    ) -> None: ...

class ZoneControlContaminantController:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        carbon_dioxide_setpoint_schedule_name: str,
        carbon_dioxide_control_availability_schedule_name: str | None = ...,
        minimum_carbon_dioxide_concentration_schedule_name: str | None = ...,
        maximum_carbon_dioxide_concentration_schedule_name: str | None = ...,
        generic_contaminant_control_availability_schedule_name: str | None = ...,
        generic_contaminant_setpoint_schedule_name: str | None = ...,
    ) -> None: ...

class AnyZoneHVACLowTemperatureRadiantElectric:
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

class AnyAirTerminalSingleDuctVAVReheat:
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

class SpaceHVACEquipmentConnections:
    def __call__(
        self,
        /,
        *,
        space_name: str,
        space_air_node_name: str,
        space_air_inlet_node_or_nodelist_name: str | None = ...,
        space_air_exhaust_node_or_nodelist_name: str | None = ...,
        space_return_air_node_or_nodelist_name: str | None = ...,
        space_return_air_node_1_flow_rate_fraction_schedule_name: str | None = ...,
        space_return_air_node_1_flow_rate_basis_node_or_nodelist_name: str | None = ...,
    ) -> None: ...

class FanVariableVolume:
    def __call__(
        self,
        name: str,
        /,
        *,
        pressure_rise: float,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        fan_total_efficiency: float | None = 0.7,
        maximum_flow_rate: float | Literal["Autosize"] | None = ...,
        fan_power_minimum_flow_rate_input_method: Literal["", "FixedFlowRate", "Fraction"] | None = "Fraction",
        fan_power_minimum_flow_fraction: float | None = 0.25,
        fan_power_minimum_air_flow_rate: float | None = ...,
        motor_efficiency: float | None = 0.9,
        motor_in_airstream_fraction: float | None = 1,
        fan_power_coefficient_1: float | None = ...,
        fan_power_coefficient_2: float | None = ...,
        fan_power_coefficient_3: float | None = ...,
        fan_power_coefficient_4: float | None = ...,
        fan_power_coefficient_5: float | None = ...,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class CoilCoolingDXCurveFitPerformance:
    def __call__(
        self,
        name: str,
        /,
        *,
        base_operating_mode: str,
        crankcase_heater_capacity: float | None = 0,
        crankcase_heater_capacity_function_of_temperature_curve_name: str | None = ...,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -25,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        unit_internal_static_air_pressure: float | None = ...,
        capacity_control_method: Literal["", "Continuous", "Discrete"] | None = "Discrete",
        evaporative_condenser_basin_heater_capacity: float | None = 0,
        evaporative_condenser_basin_heater_setpoint_temperature: float | None = 2,
        evaporative_condenser_basin_heater_operating_schedule_name: str | None = ...,
        compressor_fuel_type: Literal[
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
        alternative_operating_mode_1: str | None = ...,
        alternative_operating_mode_2: str | None = ...,
    ) -> None: ...

class CoilHeatingDXVariableRefrigerantFlow:
    def __call__(
        self,
        name: str,
        /,
        *,
        gross_rated_heating_capacity: float | Literal["Autosize"],
        rated_air_flow_rate: float | Literal["Autosize"],
        coil_air_inlet_node: str,
        coil_air_outlet_node: str,
        heating_capacity_ratio_modifier_function_of_temperature_curve_name: str,
        heating_capacity_modifier_function_of_flow_fraction_curve_name: str,
        availability_schedule: str | None = ...,
    ) -> None: ...

class CoilHeatingGasMultiStage:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        number_of_stages: int,
        stage_1_gas_burner_efficiency: float,
        stage_1_nominal_capacity: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        temperature_setpoint_node_name: str | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
        off_cycle_parasitic_gas_load: float | None = ...,
        stage_1_on_cycle_parasitic_electric_load: float | None = ...,
        stage_2_gas_burner_efficiency: float | None = ...,
        stage_2_nominal_capacity: float | Literal["Autosize"] | None = ...,
        stage_2_on_cycle_parasitic_electric_load: float | None = ...,
        stage_3_gas_burner_efficiency: float | None = ...,
        stage_3_nominal_capacity: float | Literal["Autosize"] | None = ...,
        stage_3_on_cycle_parasitic_electric_load: float | None = ...,
        stage_4_gas_burner_efficiency: float | None = ...,
        stage_4_nominal_capacity: float | Literal["Autosize"] | None = ...,
        stage_4_on_cycle_parasitic_electric_load: float | None = ...,
    ) -> None: ...

class CoilWaterHeatingAirToWaterHeatPumpWrapped:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_heating_capacity: float,
        evaporator_air_inlet_node_name: str,
        evaporator_air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        rated_cop: float | None = 3.2,
        rated_sensible_heat_ratio: float | None = 0.85,
        rated_evaporator_inlet_air_dry_bulb_temperature: float | None = 19.7,
        rated_evaporator_inlet_air_wet_bulb_temperature: float | None = 13.5,
        rated_condenser_water_temperature: float | None = 57.5,
        rated_evaporator_air_flow_rate: float | Literal["Autocalculate"] | None = ...,
        evaporator_fan_power_included_in_rated_cop: Literal["", "No", "Yes"] | None = "Yes",
        crankcase_heater_capacity: float | None = 0,
        crankcase_heater_capacity_function_of_temperature_curve_name: str | None = ...,
        maximum_ambient_temperature_for_crankcase_heater_operation: float | None = 10,
        evaporator_air_temperature_type_for_curve_objects: Literal["", "DryBulbTemperature", "WetBulbTemperature"]
        | None = "WetBulbTemperature",
        heating_capacity_function_of_temperature_curve_name: str | None = ...,
        heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        heating_cop_function_of_temperature_curve_name: str | None = ...,
        heating_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
    ) -> None: ...

class AirConditionerVariableRefrigerantFlowFluidTemperatureControl:
    def __call__(
        self,
        /,
        *,
        heat_pump_name: str,
        zone_terminal_unit_list_name: str,
        outdoor_unit_evaporating_temperature_function_of_superheating_curve_name: str,
        outdoor_unit_condensing_temperature_function_of_subcooling_curve_name: str,
        availability_schedule_name: str | None = ...,
        refrigerant_type: str | None = "R410A",
        rated_evaporative_capacity: float | Literal["", "Autosize"] | None = 40000,
        rated_compressor_power_per_unit_of_rated_evaporative_capacity: float | None = 0.35,
        minimum_outdoor_air_temperature_in_cooling_mode: float | None = -6,
        maximum_outdoor_air_temperature_in_cooling_mode: float | None = 43,
        minimum_outdoor_air_temperature_in_heating_mode: float | None = -20,
        maximum_outdoor_air_temperature_in_heating_mode: float | None = 16,
        reference_outdoor_unit_superheating: float | None = 3,
        reference_outdoor_unit_subcooling: float | None = 5,
        refrigerant_temperature_control_algorithm_for_indoor_unit: Literal["", "ConstantTemp", "VariableTemp"]
        | None = "VariableTemp",
        reference_evaporating_temperature_for_indoor_unit: float | None = 6,
        reference_condensing_temperature_for_indoor_unit: float | None = 44,
        variable_evaporating_temperature_minimum_for_indoor_unit: float | None = 4,
        variable_evaporating_temperature_maximum_for_indoor_unit: float | None = 13,
        variable_condensing_temperature_minimum_for_indoor_unit: float | None = 42,
        variable_condensing_temperature_maximum_for_indoor_unit: float | None = 46,
        outdoor_unit_fan_power_per_unit_of_rated_evaporative_capacity: float | None = 0.00425,
        outdoor_unit_fan_flow_rate_per_unit_of_rated_evaporative_capacity: float | None = ...,
        diameter_of_main_pipe_connecting_outdoor_unit_to_the_first_branch_joint: float | None = 0.0762,
        length_of_main_pipe_connecting_outdoor_unit_to_the_first_branch_joint: float | None = 30,
        equivalent_length_of_main_pipe_connecting_outdoor_unit_to_the_first_branch_joint: float | None = 36,
        height_difference_between_outdoor_unit_and_indoor_units: float | None = 5,
        main_pipe_insulation_thickness: float | None = 0.02,
        main_pipe_insulation_thermal_conductivity: float | None = 0.032,
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
        compressor_maximum_delta_pressure: float | None = 4500000,
        number_of_compressor_loading_index_entries: int | None = 2,
        loading_indices: list[Any] = ...,
    ) -> None: ...

class ControllerWaterCoil:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_variable: Literal["HumidityRatio", "Temperature", "TemperatureAndHumidityRatio"],
        actuator_variable: Literal["Flow"],
        sensor_node_name: str,
        actuator_node_name: str,
        action: Literal["Normal", "Reverse"] | None = ...,
        controller_convergence_tolerance: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_actuated_flow: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_actuated_flow: float | None = 0,
    ) -> None: ...

class AnyHeatPumpPlantLoopEIRCooling:
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
        condenser_type: Literal["", "AirSource", "WaterSource"] | None = "WaterSource",
        companion_heat_pump_name: str | None = ...,
        load_side_reference_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        source_side_reference_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        reference_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        reference_coefficient_of_performance: float | None = ...,
        sizing_factor: float | None = 1,
    ) -> None: ...

class AnyCoolingTowerTwoSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        high_fan_speed_air_flow_rate: float | Literal["Autosize"],
        high_fan_speed_fan_power: float | Literal["Autosize"],
        low_fan_speed_air_flow_rate: float | Literal["Autocalculate"],
        low_fan_speed_fan_power: float | Literal["Autocalculate"],
        design_water_flow_rate: float | Literal["Autosize"] | None = ...,
        high_fan_speed_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        low_fan_speed_air_flow_rate_sizing_factor: float | None = 0.5,
        low_fan_speed_fan_power_sizing_factor: float | None = 0.16,
        low_fan_speed_u_factor_times_area_value: float | Literal["Autocalculate"] | None = ...,
        low_fan_speed_u_factor_times_area_sizing_factor: float | None = 0.6,
        free_convection_regime_air_flow_rate: float | Literal["", "Autocalculate"] | None = 0,
        free_convection_regime_air_flow_rate_sizing_factor: float | None = 0.1,
        free_convection_regime_u_factor_times_area_value: float | Literal["", "Autocalculate"] | None = 0,
        free_convection_u_factor_times_area_value_sizing_factor: float | None = 0.1,
        performance_input_method: Literal["", "NominalCapacity", "UFactorTimesAreaAndDesignWaterFlowRate"]
        | None = "UFactorTimesAreaAndDesignWaterFlowRate",
        heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None = 1.25,
        high_speed_nominal_capacity: float | None = ...,
        low_speed_nominal_capacity: float | Literal["Autocalculate"] | None = ...,
        low_speed_nominal_capacity_sizing_factor: float | None = 0.5,
        free_convection_nominal_capacity: float | Literal["Autocalculate"] | None = ...,
        free_convection_nominal_capacity_sizing_factor: float | None = 0.1,
        design_inlet_air_dry_bulb_temperature: float | None = 35,
        design_inlet_air_wet_bulb_temperature: float | None = 25.6,
        design_approach_temperature: float | Literal["", "Autosize"] | None = "Autosize",
        design_range_temperature: float | Literal["", "Autosize"] | None = "Autosize",
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        evaporation_loss_mode: Literal["LossFactor", "SaturatedExit"] | None = ...,
        evaporation_loss_factor: float | None = 0.2,
        drift_loss_percent: float | None = 0.008,
        blowdown_calculation_mode: Literal["ConcentrationRatio", "ScheduledRate"] | None = ...,
        blowdown_concentration_ratio: float | None = 3,
        blowdown_makeup_water_usage_schedule_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        outdoor_air_inlet_node_name: str | None = ...,
        number_of_cells: int | None = 1,
        cell_control: Literal["", "MaximalCell", "MinimalCell"] | None = ...,
        cell_minimum_water_flow_rate_fraction: float | None = 0.33,
        cell_maximum_water_flow_rate_fraction: float | None = 2.5,
        sizing_factor: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class GroundHeatExchangerVerticalSizingRectangle:
    def __call__(
        self,
        name: str,
        /,
        *,
        sizingperiod_weatherfiledays_name: str,
        available_borehole_field_length: float,
        available_borehole_field_width: float,
        maximum_number_of_boreholes: float,
        design_flow_rate_per_borehole: float | None = 0.0005,
        minimum_borehole_spacing: float | None = 4,
        maximum_borehole_spacing: float | None = 6,
        minimum_borehole_vertical_length: float | None = 60,
        maximum_borehole_vertical_length: float | None = 135,
        minimum_exiting_fluid_temperature_for_sizing: float | None = 5,
        maximum_exiting_fluid_temperature_for_sizing: float | None = 35,
    ) -> None: ...

class GroundHeatExchangerPond:
    def __call__(
        self,
        name: str,
        /,
        *,
        fluid_inlet_node_name: str,
        fluid_outlet_node_name: str,
        pond_depth: float,
        pond_area: float,
        hydronic_tubing_inside_diameter: float,
        hydronic_tubing_outside_diameter: float,
        hydronic_tubing_thermal_conductivity: float,
        ground_thermal_conductivity: float,
        number_of_tubing_circuits: int,
        length_of_each_tubing_circuit: float,
    ) -> None: ...

class WaterHeaterMixed:
    def __call__(
        self,
        name: str,
        /,
        *,
        setpoint_temperature_schedule_name: str,
        heater_fuel_type: Literal[
            "Coal",
            "Diesel",
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
        ],
        heater_thermal_efficiency: float,
        ambient_temperature_indicator: Literal["Outdoors", "Schedule", "Zone"],
        tank_volume: float | Literal["", "Autosize"] | None = 0,
        deadband_temperature_difference: float | None = 0,
        maximum_temperature_limit: float | None = ...,
        heater_control_type: Literal["", "Cycle", "Modulate"] | None = "Cycle",
        heater_maximum_capacity: float | Literal["Autosize"] | None = ...,
        heater_minimum_capacity: float | None = ...,
        heater_ignition_minimum_flow_rate: float | None = 0,
        heater_ignition_delay: float | None = 0,
        part_load_factor_curve_name: str | None = ...,
        off_cycle_parasitic_fuel_consumption_rate: float | None = 0,
        off_cycle_parasitic_fuel_type: Literal[
            "Coal",
            "Diesel",
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
        ]
        | None = ...,
        off_cycle_parasitic_heat_fraction_to_tank: float | None = 0,
        on_cycle_parasitic_fuel_consumption_rate: float | None = 0,
        on_cycle_parasitic_fuel_type: Literal[
            "Coal",
            "Diesel",
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
        ]
        | None = ...,
        on_cycle_parasitic_heat_fraction_to_tank: float | None = 0,
        ambient_temperature_schedule_name: str | None = ...,
        ambient_temperature_zone_name: str | None = ...,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        off_cycle_loss_coefficient_to_ambient_temperature: float | None = ...,
        off_cycle_loss_fraction_to_zone: float | None = 1,
        on_cycle_loss_coefficient_to_ambient_temperature: float | None = ...,
        on_cycle_loss_fraction_to_zone: float | None = 1,
        peak_use_flow_rate: float | None = ...,
        use_flow_rate_fraction_schedule_name: str | None = ...,
        cold_water_supply_temperature_schedule_name: str | None = ...,
        use_side_inlet_node_name: str | None = ...,
        use_side_outlet_node_name: str | None = ...,
        use_side_effectiveness: float | None = 1,
        source_side_inlet_node_name: str | None = ...,
        source_side_outlet_node_name: str | None = ...,
        source_side_effectiveness: float | None = 1,
        use_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        source_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        indirect_water_heating_recovery_time: float | None = 1.5,
        source_side_flow_control_mode: Literal[
            "", "IndirectHeatAlternateSetpoint", "IndirectHeatPrimarySetpoint", "StorageTank"
        ]
        | None = "IndirectHeatPrimarySetpoint",
        indirect_alternate_setpoint_temperature_schedule_name: str | None = ...,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class PlantEquipmentOperationComponentSetpoint:
    def __call__(
        self,
        name: str,
        /,
        *,
        equipment_1_object_type: str,
        equipment_1_name: str,
        demand_calculation_1_node_name: str,
        setpoint_1_node_name: str,
        component_1_flow_rate: float | Literal["Autosize"],
        operation_1_type: Literal["Cooling", "Dual", "Heating"],
        equipment_2_object_type: str | None = ...,
        equipment_2_name: str | None = ...,
        demand_calculation_2_node_name: str | None = ...,
        setpoint_2_node_name: str | None = ...,
        component_2_flow_rate: float | Literal["Autosize"] | None = ...,
        operation_2_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        equipment_3_object_type: str | None = ...,
        equipment_3_name: str | None = ...,
        demand_calculation_3_node_name: str | None = ...,
        setpoint_3_node_name: str | None = ...,
        component_3_flow_rate: float | Literal["Autosize"] | None = ...,
        operation_3_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        equipment_4_object_type: str | None = ...,
        equipment_4_name: str | None = ...,
        demand_calculation_4_node_name: str | None = ...,
        setpoint_4_node_name: str | None = ...,
        component_4_flow_rate: float | Literal["Autosize"] | None = ...,
        operation_4_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        equipment_5_object_type: str | None = ...,
        equipment_5_name: str | None = ...,
        demand_calculation_5_node_name: str | None = ...,
        setpoint_5_node_name: str | None = ...,
        component_5_flow_rate: float | Literal["Autosize"] | None = ...,
        operation_5_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        equipment_6_object_type: str | None = ...,
        equipment_6_name: str | None = ...,
        demand_calculation_6_node_name: str | None = ...,
        setpoint_6_node_name: str | None = ...,
        component_6_flow_rate: float | Literal["Autosize"] | None = ...,
        operation_6_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        equipment_7_object_type: str | None = ...,
        equipment_7_name: str | None = ...,
        demand_calculation_7_node_name: str | None = ...,
        setpoint_7_node_name: str | None = ...,
        component_7_flow_rate: float | Literal["Autosize"] | None = ...,
        operation_7_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        equipment_8_object_type: str | None = ...,
        equipment_8_name: str | None = ...,
        demand_calculation_8_node_name: str | None = ...,
        setpoint_8_node_name: str | None = ...,
        component_8_flow_rate: float | Literal["Autosize"] | None = ...,
        operation_8_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        equipment_9_object_type: str | None = ...,
        equipment_9_name: str | None = ...,
        demand_calculation_9_node_name: str | None = ...,
        setpoint_9_node_name: str | None = ...,
        component_9_flow_rate: float | Literal["Autosize"] | None = ...,
        operation_9_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        equipment_10_object_type: str | None = ...,
        equipment_10_name: str | None = ...,
        demand_calculation_10_node_name: str | None = ...,
        setpoint_10_node_name: str | None = ...,
        component_10_flow_rate: float | Literal["Autosize"] | None = ...,
        operation_10_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
    ) -> None: ...

class CoilUserDefined:
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

class SetpointManagerMultiZoneHumidityMaximum:
    def __call__(
        self,
        name: str,
        /,
        *,
        hvac_air_loop_name: str,
        setpoint_node_or_nodelist_name: str,
        minimum_setpoint_humidity_ratio: float | None = 0.008,
        maximum_setpoint_humidity_ratio: float | None = 0.015,
    ) -> None: ...

class AnyDemandManagerElectricEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        limit_control: Literal["Fixed", "Off"],
        selection_control: Literal["All", "RotateMany", "RotateOne"],
        availability_schedule_name: str | None = ...,
        minimum_limit_duration: int | None = ...,
        maximum_limit_fraction: float | None = ...,
        limit_step_change: float | None = ...,
        rotation_duration: int | None = ...,
        equipment: list[Any] = ...,
    ) -> None: ...

class GeneratorFuelCellStackCooler:
    def __call__(
        self,
        name: str,
        /,
        *,
        heat_recovery_water_inlet_node_name: str | None = ...,
        heat_recovery_water_outlet_node_name: str | None = ...,
        nominal_stack_temperature: float | None = ...,
        actual_stack_temperature: float | None = ...,
        coefficient_r0: float | None = ...,
        coefficient_r1: float | None = ...,
        coefficient_r2: float | None = ...,
        coefficient_r3: float | None = ...,
        stack_coolant_flow_rate: float | None = ...,
        stack_cooler_u_factor_times_area_value: float | None = ...,
        fs_cogen_adjustment_factor: float | None = ...,
        stack_cogeneration_exchanger_area: float | None = ...,
        stack_cogeneration_exchanger_nominal_flow_rate: float | None = ...,
        stack_cogeneration_exchanger_nominal_heat_transfer_coefficient: float | None = ...,
        stack_cogeneration_exchanger_nominal_heat_transfer_coefficient_exponent: float | None = ...,
        stack_cooler_pump_power: float | None = ...,
        stack_cooler_pump_heat_loss_fraction: float | None = ...,
        stack_air_cooler_fan_coefficient_f0: float | None = ...,
        stack_air_cooler_fan_coefficient_f1: float | None = ...,
        stack_air_cooler_fan_coefficient_f2: float | None = ...,
    ) -> None: ...

class FaultModelEnthalpySensorOffsetOutdoorAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        controller_object_type: Literal["Controller:OutdoorAir"],
        controller_object_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        enthalpy_sensor_offset: float | None = 0,
    ) -> None: ...

class CurveExponentialSkewNormal:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_c1: float,
        coefficient2_c2: float,
        coefficient3_c3: float,
        coefficient4_c4: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal["", "Dimensionless"] | None = "Dimensionless",
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None: ...

class CurveExponentialDecay:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_c1: float,
        coefficient2_c2: float,
        coefficient3_c3: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal["", "Dimensionless"] | None = "Dimensionless",
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None: ...

class TableIndependentVariable:
    def __call__(
        self,
        name: str,
        /,
        *,
        interpolation_method: Literal["", "Cubic", "Linear"] | None = "Linear",
        extrapolation_method: Literal["", "Constant", "Linear"] | None = "Constant",
        minimum_value: float | None = ...,
        maximum_value: float | None = ...,
        normalization_reference_value: float | None = ...,
        unit_type: Literal[
            "", "Angle", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        external_file_name: str | None = ...,
        external_file_column_number: int | None = ...,
        external_file_starting_row_number: int | None = ...,
        values: list[Any] = ...,
    ) -> None: ...

class FluidPropertiesGlycolConcentration:
    def __call__(
        self,
        name: str,
        /,
        *,
        glycol_type: Literal["EthyleneGlycol", "PropyleneGlycol", "UserDefinedGlycolType"],
        user_defined_glycol_name: str | None = ...,
        glycol_concentration: float | None = ...,
    ) -> None: ...

class OutputControlFiles:
    def __call__(
        self,
        /,
        *,
        output_csv: Literal["", "No", "Yes"] | None = "No",
        output_mtr: Literal["", "No", "Yes"] | None = "Yes",
        output_eso: Literal["", "No", "Yes"] | None = "Yes",
        output_eio: Literal["", "No", "Yes"] | None = "Yes",
        output_tabular: Literal["", "No", "Yes"] | None = "Yes",
        output_sqlite: Literal["", "No", "Yes"] | None = "Yes",
        output_json: Literal["", "No", "Yes"] | None = "Yes",
        output_audit: Literal["", "No", "Yes"] | None = "Yes",
        output_space_sizing: Literal["", "No", "Yes"] | None = "Yes",
        output_zone_sizing: Literal["", "No", "Yes"] | None = "Yes",
        output_system_sizing: Literal["", "No", "Yes"] | None = "Yes",
        output_dxf: Literal["", "No", "Yes"] | None = "Yes",
        output_bnd: Literal["", "No", "Yes"] | None = "Yes",
        output_rdd: Literal["", "No", "Yes"] | None = "Yes",
        output_mdd: Literal["", "No", "Yes"] | None = "Yes",
        output_mtd: Literal["", "No", "Yes"] | None = "Yes",
        output_end: Literal["", "No", "Yes"] | None = "Yes",
        output_shd: Literal["", "No", "Yes"] | None = "Yes",
        output_dfs: Literal["", "No", "Yes"] | None = "Yes",
        output_glhe: Literal["", "No", "Yes"] | None = "Yes",
        output_delightin: Literal["", "No", "Yes"] | None = "Yes",
        output_delighteldmp: Literal["", "No", "Yes"] | None = "Yes",
        output_delightdfdmp: Literal["", "No", "Yes"] | None = "Yes",
        output_edd: Literal["", "No", "Yes"] | None = "Yes",
        output_dbg: Literal["", "No", "Yes"] | None = "Yes",
        output_perflog: Literal["", "No", "Yes"] | None = "Yes",
        output_sln: Literal["", "No", "Yes"] | None = "Yes",
        output_sci: Literal["", "No", "Yes"] | None = "Yes",
        output_wrl: Literal["", "No", "Yes"] | None = "Yes",
        output_screen: Literal["", "No", "Yes"] | None = "Yes",
        output_extshd: Literal["", "No", "Yes"] | None = "Yes",
        output_tarcog: Literal["", "No", "Yes"] | None = "Yes",
        output_plant_component_sizing: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None: ...

class OutputControlTimestamp:
    def __call__(
        self,
        /,
        *,
        iso_8601_format: Literal["", "No", "Yes"] | None = "No",
        timestamp_at_beginning_of_interval: Literal["", "No", "Yes"] | None = "No",
    ) -> None: ...

class AnyOutputDiagnostics:
    def __call__(self, /) -> None: ...
