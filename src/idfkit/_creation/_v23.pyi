"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class People_v9_6_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        number_of_people_schedule_name: str,
        activity_level_schedule_name: str,
        number_of_people_calculation_method: Literal["Area/Person", "People", "People/Area"] | None = "People",
        number_of_people: float | None = ...,
        people_per_floor_area: float | None = ...,
        floor_area_per_person: float | None = ...,
        fraction_radiant: float | None = 0.3,
        sensible_heat_fraction: float | Literal["Autocalculate"] | None = "Autocalculate",
        carbon_dioxide_generation_rate: float | None = ...,
        enable_ashrae_55_comfort_warnings: Literal["No", "Yes"] | None = "No",
        mean_radiant_temperature_calculation_type: Literal["AngleFactor", "SurfaceWeighted", "ZoneAveraged"]
        | None = "ZoneAveraged",
        surface_name_angle_factor_list_name: str | None = ...,
        work_efficiency_schedule_name: str | None = ...,
        clothing_insulation_calculation_method: Literal[
            "CalculationMethodSchedule", "ClothingInsulationSchedule", "DynamicClothingModelASHRAE55"
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
        validate: bool = True,
    ) -> None:
        """Create a new ``People`` and add it to the document.

        Sets internal gains and contaminant rates for occupants in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-internal-gains-people-lights-other/#people
        """

class CoilWaterHeatingAirToWaterHeatPumpVariableSpeed_v22_2_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_water_heating_capacity: float,
        evaporator_air_inlet_node_name: str,
        evaporator_air_outlet_node_name: str,
        condenser_water_inlet_node_name: str,
        condenser_water_outlet_node_name: str,
        rated_water_heating_capacity_at_speed_1: float,
        speed_1_reference_unit_rated_air_flow_rate: float,
        speed_1_reference_unit_rated_water_flow_rate: float,
        speed_1_reference_unit_water_pump_input_power_at_rated_conditions: float,
        speed_1_total_wh_capacity_function_of_temperature_curve_name: str,
        speed_1_total_wh_capacity_function_of_air_flow_fraction_curve_name: str,
        speed_1_total_wh_capacity_function_of_water_flow_fraction_curve_name: str,
        speed_1_cop_function_of_temperature_curve_name: str,
        speed_1_cop_function_of_air_flow_fraction_curve_name: str,
        speed_1_cop_function_of_water_flow_fraction_curve_name: str,
        number_of_speeds: int | None = 1,
        nominal_speed_level: int | None = 1,
        rated_evaporator_inlet_air_dry_bulb_temperature: float | None = 19.7,
        rated_evaporator_inlet_air_wet_bulb_temperature: float | None = 13.5,
        rated_condenser_inlet_water_temperature: float | None = 57.5,
        rated_evaporator_air_flow_rate: float | Literal["Autocalculate"] | None = ...,
        rated_condenser_water_flow_rate: float | Literal["Autocalculate"] | None = ...,
        evaporator_fan_power_included_in_rated_cop: Literal["No", "Yes"] | None = "Yes",
        condenser_pump_power_included_in_rated_cop: Literal["No", "Yes"] | None = "No",
        condenser_pump_heat_included_in_rated_heating_capacity_and_rated_cop: Literal["No", "Yes"] | None = "No",
        fraction_of_condenser_pump_heat_to_water: float | None = 0.2,
        crankcase_heater_capacity: float | None = 0,
        maximum_ambient_temperature_for_crankcase_heater_operation: float | None = 10,
        evaporator_air_temperature_type_for_curve_objects: Literal["DryBulbTemperature", "WetBulbTemperature"]
        | None = "WetBulbTemperature",
        part_load_fraction_correlation_curve_name: str | None = ...,
        rated_water_heating_cop_at_speed_1: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_1: float | None = 0.85,
        rated_water_heating_capacity_at_speed_2: float | None = ...,
        rated_water_heating_cop_at_speed_2: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_2: float | None = 0.85,
        speed_2_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_2_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_2_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_2_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_2_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_2_cop_function_of_temperature_curve_name: str | None = ...,
        speed_2_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_3: float | None = ...,
        rated_water_heating_cop_at_speed_3: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_3: float | None = 0.85,
        speed_3_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_3_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_3_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_3_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_3_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_3_cop_function_of_temperature_curve_name: str | None = ...,
        speed_3_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_4: float | None = ...,
        rated_water_heating_cop_at_speed_4: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_4: float | None = 0.85,
        speed_4_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_4_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_4_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_4_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_4_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_4_cop_function_of_temperature_curve_name: str | None = ...,
        speed_4_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_5: float | None = ...,
        rated_water_heating_cop_at_speed_5: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_5: float | None = 0.85,
        speed_5_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_5_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_5_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_5_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_5_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_5_cop_function_of_temperature_curve_name: str | None = ...,
        speed_5_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_6: float | None = ...,
        rated_water_heating_cop_at_speed_6: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_6: float | None = 0.85,
        speed_6_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_6_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_6_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_6_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_6_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_6_cop_function_of_temperature_curve_name: str | None = ...,
        speed_6_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_7: float | None = ...,
        rated_water_heating_cop_at_speed_7: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_7: float | None = 0.85,
        speed_7_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_7_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_7_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_7_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_7_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_7_cop_function_of_temperature_curve_name: str | None = ...,
        speed_7_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_8: float | None = ...,
        rated_water_heating_cop_at_speed_8: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_8: float | None = 0.85,
        speed_8_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_8_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_8_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_8_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_8_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_8_cop_function_of_temperature_curve_name: str | None = ...,
        speed_8_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_9: float | None = ...,
        rated_water_heating_cop_at_speed_9: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_9: float | None = 0.85,
        speed_9_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_9_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_9_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_9_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_9_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_9_cop_function_of_temperature_curve_name: str | None = ...,
        speed_9_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_10: float | None = ...,
        rated_water_heating_cop_at_speed_10: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_10: float | None = 0.85,
        speed_10_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_10_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_10_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_10_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_10_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_10_cop_function_of_temperature_curve_name: str | None = ...,
        speed_10_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:WaterHeating:AirToWaterHeatPump:VariableSpeed`` and add it to the document.

        vairlable-speed Heat pump water heater (VSHPWH) heating coil, air-to-water direct-expansion (DX) system which includes a variable-speed water heating coil, evaporator air coil, evaporator fan, electric compressor, and water pump. Part of a WaterHeater:HeatPump system.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-heating-and-cooling-coils/#coilwaterheatingairtowaterheatpumpvariablespeed
        """

class PythonPluginOutputVariable_v9_4_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        python_plugin_variable_name: str,
        type_of_data_in_variable: Literal["Averaged", "Metered", "Summed"],
        update_frequency: Literal["SystemTimestep", "ZoneTimestep"],
        units: str | None = ...,
        resource_type: Literal[
            "Coal",
            "CondensateWaterCollected",
            "Diesel",
            "DistrictCooling",
            "DistrictHeating",
            "Electricity",
            "ElectricityProducedOnSite",
            "EnergyTransfer",
            "FuelOilNo1",
            "FuelOilNo2",
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
        ]
        | None = ...,
        group_type: Literal["Building", "HVAC", "Plant", "System"] | None = ...,
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
        ]
        | None = ...,
        end_use_subcategory: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``PythonPlugin:OutputVariable`` and add it to the document.

        This object sets up an EnergyPlus output variable from a Python Plugin variable

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-python-plugin-system/#pythonpluginoutputvariable
        """
