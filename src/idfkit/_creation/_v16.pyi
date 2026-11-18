"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Any, Literal

class FanSystemModel_v8_9_to_v9_3:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        design_maximum_air_flow_rate: float | Literal["Autosize"],
        design_pressure_rise: float,
        availability_schedule_name: str | None = ...,
        speed_control_method: Literal["", "Continuous", "Discrete"] | None = "Discrete",
        electric_power_minimum_flow_rate_fraction: float | None = 0.2,
        motor_efficiency: float | None = 0.9,
        motor_in_air_stream_fraction: float | None = 1,
        design_electric_power_consumption: float | Literal["Autosize"] | None = ...,
        design_power_sizing_method: Literal["", "PowerPerFlow", "PowerPerFlowPerPressure", "TotalEfficiencyAndPressure"]
        | None = "PowerPerFlowPerPressure",
        electric_power_per_unit_flow_rate: float | None = ...,
        electric_power_per_unit_flow_rate_per_unit_pressure: float | None = 1.66667,
        fan_total_efficiency: float | None = 0.7,
        electric_power_function_of_flow_fraction_curve_name: str | None = ...,
        night_ventilation_mode_pressure_rise: float | None = ...,
        night_ventilation_mode_flow_fraction: float | None = ...,
        motor_loss_zone_name: str | None = ...,
        motor_loss_radiative_fraction: float | None = ...,
        end_use_subcategory: str | None = "General",
        number_of_speeds: float | None = 1,
        speed_fractions: list[Any] = ...,
    ) -> None: ...

class MaterialPropertyHeatAndMoistureTransferThermalConductivity_v8_9_to_v22_1:
    def __call__(
        self,
        /,
        *,
        material_name: str,
        number_of_thermal_coordinates: float,
        moisture_content_1: float,
        thermal_conductivity_1: float,
        moisture_content_2: float | None = ...,
        thermal_conductivity_2: float | None = ...,
        moisture_content_3: float | None = ...,
        thermal_conductivity_3: float | None = ...,
        moisture_content_4: float | None = ...,
        thermal_conductivity_4: float | None = ...,
        moisture_content_5: float | None = ...,
        thermal_conductivity_5: float | None = ...,
        moisture_content_6: float | None = ...,
        thermal_conductivity_6: float | None = ...,
        moisture_content_7: float | None = ...,
        thermal_conductivity_7: float | None = ...,
        moisture_content_8: float | None = ...,
        thermal_conductivity_8: float | None = ...,
        moisture_content_9: float | None = ...,
        thermal_conductivity_9: float | None = ...,
        moisture_content_10: float | None = ...,
        thermal_conductivity_10: float | None = ...,
        moisture_content_11: float | None = ...,
        thermal_conductivity_11: float | None = ...,
        moisture_content_12: float | None = ...,
        thermal_conductivity_12: float | None = ...,
        moisture_content_13: float | None = ...,
        thermal_conductivity_13: float | None = ...,
        moisture_content_14: float | None = ...,
        thermal_conductivity_14: float | None = ...,
        moisture_content_15: float | None = ...,
        thermal_conductivity_15: float | None = ...,
        moisture_content_16: float | None = ...,
        thermal_conductivity_16: float | None = ...,
        moisture_content_17: float | None = ...,
        thermal_conductivity_17: float | None = ...,
        moisture_content_18: float | None = ...,
        thermal_conductivity_18: float | None = ...,
        moisture_content_19: float | None = ...,
        thermal_conductivity_19: float | None = ...,
        moisture_content_20: float | None = ...,
        thermal_conductivity_20: float | None = ...,
        moisture_content_21: float | None = ...,
        thermal_conductivity_21: float | None = ...,
        moisture_content_22: float | None = ...,
        thermal_conductivity_22: float | None = ...,
        moisture_content_23: float | None = ...,
        thermal_conductivity_23: float | None = ...,
        moisture_content_24: float | None = ...,
        thermal_conductivity_24: float | None = ...,
        moisture_content_25: float | None = ...,
        thermal_conductivity_25: float | None = ...,
    ) -> None: ...

class EvaporativeFluidCoolerTwoSpeed_v8_9_to_v25_1:
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
        design_spray_water_flow_rate: float,
        performance_input_method: Literal[
            "StandardDesignCapacity", "UFactorTimesAreaAndDesignWaterFlowRate", "UserSpecifiedDesignCapacity"
        ],
        low_fan_speed_air_flow_rate_sizing_factor: float | None = 0.5,
        low_fan_speed_fan_power_sizing_factor: float | None = 0.16,
        outdoor_air_inlet_node_name: str | None = ...,
        heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None = 1.25,
        high_speed_standard_design_capacity: float | None = ...,
        low_speed_standard_design_capacity: float | Literal["Autocalculate"] | None = ...,
        low_speed_standard_capacity_sizing_factor: float | None = 0.5,
        high_fan_speed_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        low_fan_speed_u_factor_times_area_value: float | Literal["Autocalculate"] | None = ...,
        low_fan_speed_u_factor_times_area_sizing_factor: float | None = 0.6,
        design_water_flow_rate: float | Literal["Autosize"] | None = ...,
        high_speed_user_specified_design_capacity: float | None = ...,
        low_speed_user_specified_design_capacity: float | Literal["Autocalculate"] | None = ...,
        low_speed_user_specified_design_capacity_sizing_factor: float | None = 0.5,
        design_entering_water_temperature: float | None = ...,
        design_entering_air_temperature: float | None = ...,
        design_entering_air_wet_bulb_temperature: float | None = ...,
        high_speed_sizing_factor: float | None = 1,
        evaporation_loss_mode: Literal["", "LossFactor", "SaturatedExit"] | None = "SaturatedExit",
        evaporation_loss_factor: float | None = ...,
        drift_loss_percent: float | None = 0.008,
        blowdown_calculation_mode: Literal["", "ConcentrationRatio", "ScheduledRate"] | None = "ConcentrationRatio",
        blowdown_concentration_ratio: float | None = 3,
        blowdown_makeup_water_usage_schedule_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
    ) -> None: ...

class AirLoopHVACUnitaryHeatPumpWaterToAir_v8_9_to_v23_1:
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
        maximum_cycling_rate: float | None = 2.5,
        heat_pump_time_constant: float | None = 60,
        fraction_of_on_cycle_power_use: float | None = 0.01,
        heat_pump_fan_delay_time: float | None = 60,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        outdoor_dry_bulb_temperature_sensor_node_name: str | None = ...,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        dehumidification_control_type: Literal["", "CoolReheat", "None"] | None = "None",
        heat_pump_coil_water_flow_mode: Literal["", "Constant", "ConstantOnDemand", "Cycling"] | None = "Cycling",
    ) -> None: ...

class People_v22_2_to_v23_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        number_of_people_schedule_name: str,
        activity_level_schedule_name: str,
        number_of_people_calculation_method: Literal["", "Area/Person", "People", "People/Area"] | None = "People",
        number_of_people: float | None = ...,
        people_per_floor_area: float | None = ...,
        floor_area_per_person: float | None = ...,
        fraction_radiant: float | None = 0.3,
        sensible_heat_fraction: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        carbon_dioxide_generation_rate: float | None = ...,
        enable_ashrae_55_comfort_warnings: Literal["", "No", "Yes"] | None = "No",
        mean_radiant_temperature_calculation_type: Literal["", "AngleFactor", "SurfaceWeighted", "ZoneAveraged"]
        | None = "ZoneAveraged",
        surface_name_angle_factor_list_name: str | None = ...,
        work_efficiency_schedule_name: str | None = ...,
        clothing_insulation_calculation_method: Literal[
            "", "CalculationMethodSchedule", "ClothingInsulationSchedule", "DynamicClothingModelASHRAE55"
        ]
        | None = "ClothingInsulationSchedule",
        clothing_insulation_calculation_method_schedule_name: str | None = ...,
        clothing_insulation_schedule_name: str | None = ...,
        air_velocity_schedule_name: str | None = ...,
        thermal_comfort_model_1_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_2_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_3_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_4_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_5_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_6_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_7_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        ankle_level_air_velocity_schedule_name: str | None = ...,
        cold_stress_temperature_threshold: float | None = 15.56,
        heat_stress_temperature_threshold: float | None = 30,
    ) -> None: ...

class OutputIlluminanceMap_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        z_height: float | None = 0,
        x_minimum_coordinate: float | None = 0,
        x_maximum_coordinate: float | None = 1,
        number_of_x_grid_points: float | None = 2,
        y_minimum_coordinate: float | None = 0,
        y_maximum_coordinate: float | None = 1,
        number_of_y_grid_points: float | None = 2,
    ) -> None: ...

class AirLoopHVACUnitaryHeatPumpAirToAir_v8_9_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        controlling_zone_or_thermostat_location: str,
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:DX:SingleSpeed", "Coil:Heating:DX:VariableSpeed", "CoilSystem:IntegratedHeatPump:AirSource"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
            "CoilSystem:IntegratedHeatPump:AirSource",
        ],
        cooling_coil_name: str,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        supplemental_heating_coil_name: str,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        dehumidification_control_type: Literal["", "CoolReheat", "Multimode", "None"] | None = "None",
    ) -> None: ...

class Lights_v9_6_to_v23_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        design_level_calculation_method: Literal["", "LightingLevel", "Watts/Area", "Watts/Person"]
        | None = "LightingLevel",
        lighting_level: float | None = ...,
        watts_per_zone_floor_area: float | None = ...,
        watts_per_person: float | None = ...,
        return_air_fraction: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_visible: float | None = 0,
        fraction_replaceable: float | None = 1,
        end_use_subcategory: str | None = "General",
        return_air_fraction_calculated_from_plenum_temperature: Literal["", "No", "Yes"] | None = "No",
        return_air_fraction_function_of_plenum_temperature_coefficient_1: float | None = 0,
        return_air_fraction_function_of_plenum_temperature_coefficient_2: float | None = 0,
        return_air_heat_gain_node_name: str | None = ...,
        exhaust_air_heat_gain_node_name: str | None = ...,
    ) -> None: ...

class EnergyManagementSystemMeteredOutputVariable_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        ems_variable_name: str,
        update_frequency: Literal["SystemTimestep", "ZoneTimestep"],
        resource_type: Literal[
            "Coal",
            "CondensateWaterCollected",
            "Diesel",
            "DistrictCooling",
            "DistrictHeating",
            "Electricity",
            "ElectricityProducedOnSite",
            "EnergyTransfer",
            "FuelOil#1",
            "FuelOil#2",
            "Gasoline",
            "MainsWaterSupply",
            "NaturalGas",
            "OnSiteWaterProduced",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "RainWaterCollected",
            "SolarAirHeating",
            "SolarWaterHeating",
            "Steam",
            "WaterUse",
            "WellWaterDrawn",
        ],
        group_type: Literal["Building", "HVAC", "Plant", "System"],
        end_use_category: Literal[
            "Baseboard",
            "Boilers",
            "Chillers",
            "Cooling",
            "CoolingCoils",
            "ExteriorEquipment",
            "ExteriorLights",
            "Fans",
            "HeatRecovery",
            "HeatRecoveryForCooling",
            "HeatRecoveryForHeating",
            "HeatRejection",
            "Heating",
            "HeatingCoils",
            "Humidifier",
            "InteriorEquipment",
            "InteriorLights",
            "OnSiteGeneration",
            "Pumps",
            "Refrigeration",
            "WaterSystems",
        ],
        ems_program_or_subroutine_name: str | None = ...,
        end_use_subcategory: str | None = ...,
        units: str | None = ...,
    ) -> None: ...

class AirTerminalSingleDuctVAVReheatVariableSpeedFan_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        maximum_cooling_air_flow_rate: float | Literal["Autosize"],
        maximum_heating_air_flow_rate: float | Literal["Autosize"],
        zone_minimum_air_flow_fraction: float,
        fan_object_type: Literal["Fan:SystemModel", "Fan:VariableVolume"],
        fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        heating_coil_name: str,
        availability_schedule_name: str | None = ...,
        air_inlet_node_name: str | None = ...,
        air_outlet_node_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        heating_convergence_tolerance: float | None = 0.001,
    ) -> None: ...

class ZoneHVACEquipmentList_v9_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        load_distribution_scheme: Literal["", "SequentialLoad", "SequentialUniformPLR", "UniformLoad", "UniformPLR"]
        | None = "SequentialLoad",
        equipment: list[Any] = ...,
    ) -> None: ...

class DemandManagerAssignmentList_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        meter_name: str,
        demand_limit_safety_fraction: float,
        demand_window_length: float,
        demand_manager_priority: Literal["All", "Sequential"],
        demand_limit_schedule_name: str | None = ...,
        billing_period_schedule_name: str | None = ...,
        peak_period_schedule_name: str | None = ...,
        manager_data: list[Any] = ...,
    ) -> None: ...

class PlantComponentUserDefined_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        number_of_plant_loop_connections: float,
        plant_connection_1_inlet_node_name: str,
        plant_connection_1_outlet_node_name: str,
        plant_connection_1_loading_mode: Literal[
            "DemandsLoad",
            "MeetsLoadWithNominalCapacity",
            "MeetsLoadWithNominalCapacityHiOutLimit",
            "MeetsLoadWithNominalCapacityLowOutLimit",
            "MeetsLoadWithPassiveCapacity",
        ],
        plant_connection_1_loop_flow_request_mode: Literal[
            "NeedsFlowAndTurnsLoopOn", "NeedsFlowIfLoopOn", "ReceivesWhateverFlowAvailable"
        ],
        main_model_program_calling_manager_name: str | None = ...,
        plant_connection_1_initialization_program_calling_manager_name: str | None = ...,
        plant_connection_1_simulation_program_calling_manager_name: str | None = ...,
        plant_connection_2_inlet_node_name: str | None = ...,
        plant_connection_2_outlet_node_name: str | None = ...,
        plant_connection_2_loading_mode: Literal[
            "DemandsLoad",
            "MeetLoadWithNominalCapacity",
            "MeetLoadWithNominalCapacityHiOutLimit",
            "MeetLoadWithNominalCapacityLowOutLimit",
            "MeetLoadWithPassiveCapacity",
        ]
        | None = ...,
        plant_connection_2_loop_flow_request_mode: Literal[
            "NeedsFlowAndTurnsLoopOn", "NeedsFlowIfLoopOn", "ReceivesWhateverFlowAvailable"
        ]
        | None = ...,
        plant_connection_2_initialization_program_calling_manager_name: str | None = ...,
        plant_connection_2_simulation_program_calling_manager_name: str | None = ...,
        plant_connection_3_inlet_node_name: str | None = ...,
        plant_connection_3_outlet_node_name: str | None = ...,
        plant_connection_3_loading_mode: Literal[
            "DemandsLoad",
            "MeetLoadWithNominalCapacity",
            "MeetLoadWithNominalCapacityHiOutLimit",
            "MeetLoadWithNominalCapacityLowOutLimit",
            "MeetLoadWithPassiveCapacity",
        ]
        | None = ...,
        plant_connection_3_loop_flow_request_mode: Literal[
            "NeedsFlowAndTurnsLoopOn", "NeedsFlowIfLoopOn", "ReceivesWhateverFlowAvailable"
        ]
        | None = ...,
        plant_connection_3_initialization_program_calling_manager_name: str | None = ...,
        plant_connection_3_simulation_program_calling_manager_name: str | None = ...,
        plant_connection_4_inlet_node_name: str | None = ...,
        plant_connection_4_outlet_node_name: str | None = ...,
        plant_connection_4_loading_mode: Literal[
            "DemandsLoad",
            "MeetLoadWithNominalCapacity",
            "MeetLoadWithNominalCapacityHiOutLimit",
            "MeetLoadWithNominalCapacityLowOutLimit",
            "MeetLoadWithPassiveCapacity",
        ]
        | None = ...,
        plant_connection_4_loop_flow_request_mode: Literal[
            "NeedsFlowAndTurnsLoopOn", "NeedsFlowIfLoopOn", "ReceivesWhateverFlowAvailable"
        ]
        | None = ...,
        plant_connection_4_initialization_program_calling_manager_name: str | None = ...,
        plant_connection_4_simulation_program_calling_manager_name: str | None = ...,
        air_connection_inlet_node_name: str | None = ...,
        air_connection_outlet_node_name: str | None = ...,
        supply_inlet_water_storage_tank_name: str | None = ...,
        collection_outlet_water_storage_tank_name: str | None = ...,
        ambient_zone_name: str | None = ...,
    ) -> None: ...

class CoilHeatingWaterToAirHeatPumpParameterEstimation_v8_9_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        compressor_type: Literal["Reciprocating", "Rotary", "Scroll"],
        design_source_side_flow_rate: float,
        gross_rated_heating_capacity: float,
        high_pressure_cutoff: float,
        low_pressure_cutoff: float,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        load_side_total_heat_transfer_coefficient: float,
        superheat_temperature_at_the_evaporator_outlet: float,
        compressor_power_losses: float,
        compressor_efficiency: float,
        refrigerant_type: str | None = "R22",
        compressor_piston_displacement: float | None = ...,
        compressor_suction_discharge_pressure_drop: float | None = ...,
        compressor_clearance_factor: float | None = ...,
        refrigerant_volume_flow_rate: float | None = ...,
        volume_ratio: float | None = ...,
        leak_rate_coefficient: float | None = ...,
        source_side_heat_transfer_coefficient: float | None = ...,
        source_side_heat_transfer_resistance1: float | None = ...,
        source_side_heat_transfer_resistance2: float | None = ...,
    ) -> None: ...

class PythonPluginSearchPaths_v9_3:
    def __call__(
        self,
        name: str,
        /,
        *,
        add_current_working_directory_to_search_path: Literal["", "No", "Yes"] | None = "Yes",
        add_input_file_directory_to_search_path: Literal["", "No", "Yes"] | None = "Yes",
        search_path_1: str | None = ...,
        search_path_2: str | None = ...,
        search_path_3: str | None = ...,
        search_path_4: str | None = ...,
        search_path_5: str | None = ...,
    ) -> None: ...

class PythonPluginTrendVariable_v9_3_to_v22_1:
    def __call__(
        self, name: str, /, *, name_of_a_python_plugin_variable: str, number_of_timesteps_to_be_logged: float
    ) -> None: ...

class RunPeriod_v9_2_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        begin_month: float,
        begin_day_of_month: float,
        end_month: float,
        end_day_of_month: float,
        begin_year: float | None = ...,
        end_year: float | None = ...,
        day_of_week_for_start_day: Literal["Friday", "Monday", "Saturday", "Sunday", "Thursday", "Tuesday", "Wednesday"]
        | None = ...,
        use_weather_file_holidays_and_special_days: Literal["", "No", "Yes"] | None = "Yes",
        use_weather_file_daylight_saving_period: Literal["", "No", "Yes"] | None = "Yes",
        apply_weekend_holiday_rule: Literal["", "No", "Yes"] | None = "No",
        use_weather_file_rain_indicators: Literal["", "No", "Yes"] | None = "Yes",
        use_weather_file_snow_indicators: Literal["", "No", "Yes"] | None = "Yes",
        treat_weather_as_actual: Literal["", "No", "Yes"] | None = "No",
    ) -> None: ...

class ZoneHVACLowTemperatureRadiantConstantFlow_v9_5_to_v25_1:
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
        rated_flow_rate: float | Literal["Autosize"] | None = ...,
        pump_flow_rate_schedule_name: str | None = ...,
        rated_pump_head: float | None = 179352,
        rated_power_consumption: float | None = ...,
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
        number_of_circuits: Literal["", "CalculateFromCircuitLength", "OnePerSurface"] | None = "OnePerSurface",
        circuit_length: float | None = 106.7,
    ) -> None: ...
