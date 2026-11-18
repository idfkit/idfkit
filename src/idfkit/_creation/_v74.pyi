"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class CoilWaterHeatingAirToWaterHeatPumpVariableSpeed_v23_2_to_v25_1:
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
        crankcase_heater_capacity_function_of_temperature_curve_name: str | None = ...,
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
    ) -> None:
        """Create a new ``Coil:WaterHeating:AirToWaterHeatPump:VariableSpeed`` and add it to the document.

        variable-speed Heat pump water heater (VSHPWH) heating coil, air-to-water direct-expansion (DX) system which includes a variable-speed water heating coil, evaporator air coil, evaporator fan, electric compressor, and water pump. Part of a WaterHeater:HeatPump system.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-heating-and-cooling-coils/#coilwaterheatingairtowaterheatpumpvariablespeed
        """

class LifeCycleCostRecurringCosts_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        category: Literal[
            "Maintenance", "MajorOverhaul", "MinorOverhaul", "Operation", "OtherOperational", "Repair", "Replacement"
        ]
        | None = "Maintenance",
        cost: float | None = ...,
        start_of_costs: Literal["BasePeriod", "ServicePeriod"] | None = "ServicePeriod",
        years_from_start: float | None = ...,
        months_from_start: float | None = ...,
        repeat_period_years: float | None = 1,
        repeat_period_months: float | None = 0,
        annual_escalation_rate: float | None = ...,
    ) -> None:
        """Create a new ``LifeCycleCost:RecurringCosts`` and add it to the document.

        Recurring costs are costs that repeat over time on a regular schedule during the study period. If costs associated with equipment do repeat but not on a regular schedule, use LifeCycleCost:NonrecurringCost objects instead.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/energyplus-economics/lifecyclecost-recurringcosts/#lifecyclecostrecurringcosts
        """

class Roof_v8_9_to_v9_5:
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
    ) -> None:
        """Create a new ``Roof`` and add it to the document.

        Allows for simplified entry of roofs (exterior). View Factor to Ground is automatically calculated.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-thermal-zone-description-geometry/#roof
        """

class AirTerminalSingleDuctSeriesPIUReheat_v8_9_to_v24_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        maximum_air_flow_rate: float | Literal["Autosize"],
        maximum_primary_air_flow_rate: float | Literal["Autosize"],
        minimum_primary_air_flow_fraction: float | Literal["Autosize"],
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
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:SeriesPIU:Reheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume, series powered induction unit (PIU), with reheat coil (hot water, electric, gas, or steam).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.1/io-reference/overview/group-zone-hvac-air-loop-terminal-units/#airterminalsingleductseriespiureheat
        """
