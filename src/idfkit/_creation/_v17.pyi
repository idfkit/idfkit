"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Any, Literal

class Version_v9_4:
    def __call__(self, /, *, version_identifier: str | None = "9.4") -> None: ...

class HVACSystemRootFindingAlgorithm_v8_9_to_v22_1:
    def __call__(
        self,
        /,
        *,
        algorithm: Literal[
            "", "Alternation", "Bisection", "BisectionThenRegulaFalsi", "RegulaFalsi", "RegulaFalsiThenBisection"
        ]
        | None = "RegulaFalsi",
        number_of_iterations_before_algorithm_switch: float | None = 5,
    ) -> None: ...

class ZoneAirMassFlowConservation_v8_9_to_v9_4:
    def __call__(
        self,
        /,
        *,
        adjust_zone_mixing_for_zone_air_mass_flow_balance: Literal["", "No", "Yes"] | None = "No",
        infiltration_balancing_method: Literal["", "AddInfiltrationFlow", "AdjustInfiltrationFlow", "None"]
        | None = "AddInfiltrationFlow",
        infiltration_balancing_zones: Literal["", "AllZones", "MixingSourceZonesOnly"] | None = "MixingSourceZonesOnly",
    ) -> None: ...

class AirLoopHVACUnitaryHeatPumpWaterToAir_v23_2_to_v25_1:
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

class Zone_v8_9_to_v9_4:
    def __call__(
        self,
        name: str,
        /,
        *,
        direction_of_relative_north: float | None = 0,
        x_origin: float | None = 0,
        y_origin: float | None = 0,
        z_origin: float | None = 0,
        type: float | None = 1,
        multiplier: float | None = 1,
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

class HVACTemplateZonePTHP_v8_9:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        template_thermostat_name: str | None = ...,
        cooling_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        heating_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        outdoor_air_method: Literal[
            "", "DetailedSpecification", "Flow/Area", "Flow/Person", "Flow/Zone", "Maximum", "Sum"
        ]
        | None = "Flow/Person",
        outdoor_air_flow_rate_per_person: float | None = 0.00944,
        outdoor_air_flow_rate_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_rate_per_zone: float | None = 0,
        system_availability_schedule_name: str | None = ...,
        supply_fan_operating_mode_schedule_name: str | None = ...,
        supply_fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 75,
        supply_fan_motor_efficiency: float | None = 0.9,
        cooling_coil_type: Literal["", "SingleSpeedDX"] | None = "SingleSpeedDX",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_coil_gross_rated_total_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_cop: float | None = 3,
        heat_pump_heating_coil_type: Literal["", "SingleSpeedDXHeatPump"] | None = "SingleSpeedDXHeatPump",
        heat_pump_heating_coil_availability_schedule_name: str | None = ...,
        heat_pump_heating_coil_gross_rated_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        heat_pump_heating_coil_gross_rated_cop: float | None = 2.75,
        heat_pump_heating_minimum_outdoor_dry_bulb_temperature: float | None = -8,
        heat_pump_defrost_maximum_outdoor_dry_bulb_temperature: float | None = 5,
        heat_pump_defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "ReverseCycle",
        heat_pump_defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        heat_pump_defrost_time_period_fraction: float | None = 0.058333,
        supplemental_heating_coil_type: Literal["", "Electric", "Gas", "HotWater"] | None = "Electric",
        supplemental_heating_coil_availability_schedule_name: str | None = ...,
        supplemental_heating_coil_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        supplemental_heating_coil_maximum_outdoor_dry_bulb_temperature: float | None = 21,
        supplemental_gas_heating_coil_efficiency: float | None = 0.8,
        supplemental_gas_heating_coil_parasitic_electric_load: float | None = 0,
        dedicated_outdoor_air_system_name: str | None = ...,
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_cooling_design_supply_air_temperature: float | None = 14,
        zone_cooling_design_supply_air_temperature_difference: float | None = 11.11,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = 50,
        zone_heating_design_supply_air_temperature_difference: float | None = 30,
        design_specification_outdoor_air_object_name: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        baseboard_heating_type: Literal["", "Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["", "Autosize"] | None = "Autosize",
    ) -> None: ...

class ChillerElectricReformulatedEIR_v24_2:
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
        condenser_minimum_flow_fraction: float | None = ...,
        thermosiphon_capacity_fraction_curve_name: str | None = ...,
        thermosiphon_minimum_temperature_difference: float | None = 0,
    ) -> None: ...

class SteamEquipment_v9_6_to_v23_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        design_level_calculation_method: Literal[
            "", "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_zone_floor_area: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class WaterHeaterStratified_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        tank_volume: float | Literal["Autosize"],
        tank_height: float | Literal["Autosize"],
        heater_1_setpoint_temperature_schedule_name: str,
        heater_2_setpoint_temperature_schedule_name: str,
        heater_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictHeating",
            "Electricity",
            "FuelOil#1",
            "FuelOil#2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "PropaneGas",
            "Steam",
        ],
        heater_thermal_efficiency: float,
        ambient_temperature_indicator: Literal["Outdoors", "Schedule", "Zone"],
        end_use_subcategory: str | None = "General",
        tank_shape: Literal["", "HorizontalCylinder", "Other", "VerticalCylinder"] | None = "VerticalCylinder",
        tank_perimeter: float | None = ...,
        maximum_temperature_limit: float | None = ...,
        heater_priority_control: Literal["", "MasterSlave", "Simultaneous"] | None = "MasterSlave",
        heater_1_deadband_temperature_difference: float | None = 0,
        heater_1_capacity: float | Literal["Autosize"] | None = ...,
        heater_1_height: float | None = ...,
        heater_2_deadband_temperature_difference: float | None = 0,
        heater_2_capacity: float | None = ...,
        heater_2_height: float | None = ...,
        off_cycle_parasitic_fuel_consumption_rate: float | None = 0,
        off_cycle_parasitic_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictHeating",
            "Electricity",
            "FuelOil#1",
            "FuelOil#2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "PropaneGas",
            "Steam",
        ]
        | None = ...,
        off_cycle_parasitic_heat_fraction_to_tank: float | None = 0,
        off_cycle_parasitic_height: float | None = 0,
        on_cycle_parasitic_fuel_consumption_rate: float | None = 0,
        on_cycle_parasitic_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictHeating",
            "Electricity",
            "FuelOil#1",
            "FuelOil#2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "PropaneGas",
            "Steam",
        ]
        | None = ...,
        on_cycle_parasitic_heat_fraction_to_tank: float | None = 0,
        on_cycle_parasitic_height: float | None = 0,
        ambient_temperature_schedule_name: str | None = ...,
        ambient_temperature_zone_name: str | None = ...,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        uniform_skin_loss_coefficient_per_unit_area_to_ambient_temperature: float | None = ...,
        skin_loss_fraction_to_zone: float | None = 1,
        off_cycle_flue_loss_coefficient_to_ambient_temperature: float | None = ...,
        off_cycle_flue_loss_fraction_to_zone: float | None = 1,
        peak_use_flow_rate: float | None = ...,
        use_flow_rate_fraction_schedule_name: str | None = ...,
        cold_water_supply_temperature_schedule_name: str | None = ...,
        use_side_inlet_node_name: str | None = ...,
        use_side_outlet_node_name: str | None = ...,
        use_side_effectiveness: float | None = 1,
        use_side_inlet_height: float | None = 0,
        use_side_outlet_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        source_side_inlet_node_name: str | None = ...,
        source_side_outlet_node_name: str | None = ...,
        source_side_effectiveness: float | None = 1,
        source_side_inlet_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        source_side_outlet_height: float | None = 0,
        inlet_mode: Literal["", "Fixed", "Seeking"] | None = "Fixed",
        use_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        source_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        indirect_water_heating_recovery_time: float | None = 1.5,
        number_of_nodes: float | None = 1,
        additional_destratification_conductivity: float | None = 0,
        node_1_additional_loss_coefficient: float | None = 0,
        node_2_additional_loss_coefficient: float | None = 0,
        node_3_additional_loss_coefficient: float | None = 0,
        node_4_additional_loss_coefficient: float | None = 0,
        node_5_additional_loss_coefficient: float | None = 0,
        node_6_additional_loss_coefficient: float | None = 0,
        node_7_additional_loss_coefficient: float | None = 0,
        node_8_additional_loss_coefficient: float | None = 0,
        node_9_additional_loss_coefficient: float | None = 0,
        node_10_additional_loss_coefficient: float | None = 0,
        node_11_additional_loss_coefficient: float | None = 0,
        node_12_additional_loss_coefficient: float | None = 0,
        source_side_flow_control_mode: Literal[
            "", "IndirectHeatAlternateSetpoint", "IndirectHeatPrimarySetpoint", "StorageTank"
        ]
        | None = "IndirectHeatPrimarySetpoint",
        indirect_alternate_setpoint_temperature_schedule_name: str | None = ...,
    ) -> None: ...

class EvaporativeFluidCoolerSingleSpeed_v8_9_to_v22_1:
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
        ]
        | None = ...,
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

class EvaporativeFluidCoolerSingleSpeed_v22_2_to_v25_1:
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

class AirLoopHVACUnitarySystem_v9_3_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        control_type: Literal["", "Load", "SetPoint", "SingleZoneVAV"] | None = "Load",
        controlling_zone_or_thermostat_location: str | None = ...,
        dehumidification_control_type: Literal["", "CoolReheat", "Multimode", "None"] | None = "None",
        availability_schedule_name: str | None = ...,
        supply_fan_object_type: Literal[
            "Fan:ComponentModel", "Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel", "Fan:VariableVolume"
        ]
        | None = ...,
        supply_fan_name: str | None = ...,
        fan_placement: Literal["BlowThrough", "DrawThrough"] | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        heating_coil_object_type: Literal[
            "Coil:Heating:DX:MultiSpeed",
            "Coil:Heating:DX:SingleSpeed",
            "Coil:Heating:DX:VariableSpeed",
            "Coil:Heating:Desuperheater",
            "Coil:Heating:Electric",
            "Coil:Heating:Electric:MultiStage",
            "Coil:Heating:Fuel",
            "Coil:Heating:Gas:MultiStage",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "Coil:Heating:WaterToAirHeatPump:EquationFit",
            "Coil:Heating:WaterToAirHeatPump:ParameterEstimation",
            "Coil:Heating:WaterToAirHeatPump:VariableSpeedEquationFit",
            "Coil:UserDefined",
        ]
        | None = ...,
        heating_coil_name: str | None = ...,
        dx_heating_coil_sizing_ratio: float | None = 1,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX",
            "Coil:Cooling:DX:MultiSpeed",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:SingleSpeed:ThermalStorage",
            "Coil:Cooling:DX:TwoSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Cooling:WaterToAirHeatPump:EquationFit",
            "Coil:Cooling:WaterToAirHeatPump:ParameterEstimation",
            "Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit",
            "Coil:UserDefined",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
            "CoilSystem:Cooling:Water:HeatExchangerAssisted",
        ]
        | None = ...,
        cooling_coil_name: str | None = ...,
        use_doas_dx_cooling_coil: Literal["", "No", "Yes"] | None = "No",
        minimum_supply_air_temperature: float | Literal["", "Autosize"] | None = 2,
        latent_load_control: Literal[
            "",
            "LatentOnlyLoadControl",
            "LatentOrSensibleLoadControl",
            "LatentWithSensibleLoadControl",
            "SensibleOnlyLoadControl",
        ]
        | None = "SensibleOnlyLoadControl",
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Desuperheater",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "Coil:UserDefined",
        ]
        | None = ...,
        supplemental_heating_coil_name: str | None = ...,
        cooling_supply_air_flow_rate_method: Literal[
            "FlowPerCoolingCapacity", "FlowPerFloorArea", "FractionOfAutosizedCoolingValue", "None", "SupplyAirFlowRate"
        ]
        | None = ...,
        cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        cooling_supply_air_flow_rate_per_floor_area: float | None = ...,
        cooling_fraction_of_autosized_cooling_supply_air_flow_rate: float | None = ...,
        cooling_supply_air_flow_rate_per_unit_of_capacity: float | None = ...,
        heating_supply_air_flow_rate_method: Literal[
            "FlowPerFloorArea", "FlowPerHeatingCapacity", "FractionOfAutosizedHeatingValue", "None", "SupplyAirFlowRate"
        ]
        | None = ...,
        heating_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_supply_air_flow_rate_per_floor_area: float | None = ...,
        heating_fraction_of_autosized_heating_supply_air_flow_rate: float | None = ...,
        heating_supply_air_flow_rate_per_unit_of_capacity: float | None = ...,
        no_load_supply_air_flow_rate_method: Literal[
            "FlowPerCoolingCapacity",
            "FlowPerFloorArea",
            "FlowPerHeatingCapacity",
            "FractionOfAutosizedCoolingValue",
            "FractionOfAutosizedHeatingValue",
            "None",
            "SupplyAirFlowRate",
        ]
        | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_supply_air_flow_rate_per_floor_area: float | None = ...,
        no_load_fraction_of_autosized_cooling_supply_air_flow_rate: float | None = ...,
        no_load_fraction_of_autosized_heating_supply_air_flow_rate: float | None = ...,
        no_load_supply_air_flow_rate_per_unit_of_capacity_during_cooling_operation: float | None = ...,
        no_load_supply_air_flow_rate_per_unit_of_capacity_during_heating_operation: float | None = ...,
        maximum_supply_air_temperature: float | Literal["", "Autosize"] | None = 80,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        outdoor_dry_bulb_temperature_sensor_node_name: str | None = ...,
        maximum_cycling_rate: float | None = 2.5,
        heat_pump_time_constant: float | None = 60,
        fraction_of_on_cycle_power_use: float | None = 0.01,
        heat_pump_fan_delay_time: float | None = 60,
        ancillary_on_cycle_electric_power: float | None = 0,
        ancillary_off_cycle_electric_power: float | None = 0,
        design_heat_recovery_water_flow_rate: float | None = 0,
        maximum_temperature_for_heat_recovery: float | None = 80,
        heat_recovery_water_inlet_node_name: str | None = ...,
        heat_recovery_water_outlet_node_name: str | None = ...,
        design_specification_multispeed_object_type: Literal["UnitarySystemPerformance:Multispeed"] | None = ...,
        design_specification_multispeed_object_name: str | None = ...,
    ) -> None: ...

class ConstructionInternalSource_v8_9_to_v9_3:
    def __call__(
        self,
        name: str,
        /,
        *,
        source_present_after_layer_number: float,
        temperature_calculation_requested_after_layer_number: float,
        dimensions_for_the_ctf_calculation: float,
        tube_spacing: float,
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

class AirflowNetworkMultiZoneComponentDetailedOpening_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_mass_flow_coefficient_when_opening_is_closed: float,
        number_of_sets_of_opening_factor_data: float,
        opening_factor_2: float,
        air_mass_flow_exponent_when_opening_is_closed: float | None = 0.65,
        type_of_rectangular_large_vertical_opening_lvo_: Literal["", "HorizontallyPivoted", "NonPivoted"]
        | None = "NonPivoted",
        extra_crack_length_or_height_of_pivoting_axis: float | None = 0,
        opening_factor_1: float | None = 0,
        discharge_coefficient_for_opening_factor_1: float | None = 0.001,
        width_factor_for_opening_factor_1: float | None = 0,
        height_factor_for_opening_factor_1: float | None = 0,
        start_height_factor_for_opening_factor_1: float | None = 0,
        discharge_coefficient_for_opening_factor_2: float | None = 1,
        width_factor_for_opening_factor_2: float | None = 1,
        height_factor_for_opening_factor_2: float | None = 1,
        start_height_factor_for_opening_factor_2: float | None = 0,
        opening_factor_3: float | None = ...,
        discharge_coefficient_for_opening_factor_3: float | None = 0,
        width_factor_for_opening_factor_3: float | None = 0,
        height_factor_for_opening_factor_3: float | None = 0,
        start_height_factor_for_opening_factor_3: float | None = 0,
        opening_factor_4: float | None = ...,
        discharge_coefficient_for_opening_factor_4: float | None = 0,
        width_factor_for_opening_factor_4: float | None = 0,
        height_factor_for_opening_factor_4: float | None = 0,
        start_height_factor_for_opening_factor_4: float | None = 0,
        type_of_rectangular_large_vertical_opening_lvo: Literal["", "HorizontallyPivoted", "NonPivoted"] | None = ...,
    ) -> None: ...

class WindowShadingControl_v9_0_to_v9_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        shading_type: Literal[
            "BetweenGlassBlind",
            "BetweenGlassShade",
            "ExteriorBlind",
            "ExteriorScreen",
            "ExteriorShade",
            "InteriorBlind",
            "InteriorShade",
            "SwitchableGlazing",
        ],
        shading_control_type: Literal[
            "AlwaysOff",
            "AlwaysOn",
            "MeetDaylightIlluminanceSetpoint",
            "OffNightAndOnDayIfCoolingAndHighSolarOnWindow",
            "OnIfHighGlare",
            "OnIfHighHorizontalSolar",
            "OnIfHighOutdoorAirTempAndHighHorizontalSolar",
            "OnIfHighOutdoorAirTempAndHighSolarOnWindow",
            "OnIfHighOutdoorAirTemperature",
            "OnIfHighSolarOnWindow",
            "OnIfHighZoneAirTempAndHighHorizontalSolar",
            "OnIfHighZoneAirTempAndHighSolarOnWindow",
            "OnIfHighZoneAirTemperature",
            "OnIfHighZoneCooling",
            "OnIfScheduleAllows",
            "OnNightAndOnDayIfCoolingAndHighSolarOnWindow",
            "OnNightIfHeatingAndOffDay",
            "OnNightIfHeatingAndOnDayIfCooling",
            "OnNightIfLowInsideTempAndOffDay",
            "OnNightIfLowOutdoorTempAndOffDay",
            "OnNightIfLowOutdoorTempAndOnDayIfCooling",
        ],
        shading_control_sequence_number: float | None = 1,
        construction_with_shading_name_: str | None = ...,
        schedule_name: str | None = ...,
        setpoint: float | None = ...,
        shading_control_is_scheduled: Literal["", "No", "Yes"] | None = "No",
        glare_control_is_active: Literal["", "No", "Yes"] | None = "No",
        shading_device_material_name: str | None = ...,
        type_of_slat_angle_control_for_blinds: Literal["", "BlockBeamSolar", "FixedSlatAngle", "ScheduledSlatAngle"]
        | None = "FixedSlatAngle",
        slat_angle_schedule_name: str | None = ...,
        setpoint_2: float | None = ...,
        daylighting_control_object_name: str | None = ...,
        multiple_surface_control_type: Literal["", "Group", "Sequential"] | None = "Sequential",
        construction_with_shading_name: str | None = ...,
        fenestration_surfaces: list[Any] = ...,
    ) -> None: ...

class HeatPumpPlantLoopEIRHeating_v23_2_to_v24_1:
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
        reference_coefficient_of_performance: float | None = 3,
        sizing_factor: float | None = 1,
        heating_to_cooling_capacity_sizing_ratio: float | None = 1,
        heat_pump_sizing_method: Literal["", "CoolingCapacity", "GreaterOfHeatingOrCooling", "HeatingCapacity"]
        | None = "CoolingCapacity",
        control_type: Literal["", "Load", "Setpoint"] | None = "Load",
        flow_mode: Literal["", "ConstantFlow", "VariableSpeedPumping"] | None = "ConstantFlow",
        minimum_part_load_ratio: float | None = 0,
        minimum_source_inlet_temperature: float | None = -100,
        maximum_source_inlet_temperature: float | None = 100,
        minimum_supply_water_temperature_curve_name: str | None = ...,
        maximum_supply_water_temperature_curve_name: str | None = ...,
        dry_outdoor_correction_factor_curve_name: str | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 10,
        heat_pump_defrost_control: Literal["None", "OnDemand", "Timed", "TimedEmpirical"] | None = ...,
        heat_pump_defrost_time_period_fraction: float | None = 0.058333,
        defrost_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        timed_empirical_defrost_frequency_curve_name: str | None = ...,
        timed_empirical_defrost_heat_load_penalty_curve_name: str | None = ...,
        timed_empirical_defrost_heat_input_energy_fraction_curve_name: str | None = ...,
    ) -> None: ...
