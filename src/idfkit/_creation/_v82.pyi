"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class AirConditionerVariableRefrigerantFlow_v8_9_to_v9_2:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        zone_terminal_unit_list_name: str,
        availability_schedule_name: str | None = ...,
        gross_rated_total_cooling_capacity: float | Literal["Autosize"] | None = ...,
        gross_rated_cooling_cop: float | None = 3.3,
        minimum_outdoor_temperature_in_cooling_mode: float | None = -6,
        maximum_outdoor_temperature_in_cooling_mode: float | None = 43,
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
        minimum_outdoor_temperature_in_heating_mode: float | None = -20,
        maximum_outdoor_temperature_in_heating_mode: float | None = 16,
        heating_capacity_ratio_modifier_function_of_low_temperature_curve_name: str | None = ...,
        heating_capacity_ratio_boundary_curve_name: str | None = ...,
        heating_capacity_ratio_modifier_function_of_high_temperature_curve_name: str | None = ...,
        heating_energy_input_ratio_modifier_function_of_low_temperature_curve_name: str | None = ...,
        heating_energy_input_ratio_boundary_curve_name: str | None = ...,
        heating_energy_input_ratio_modifier_function_of_high_temperature_curve_name: str | None = ...,
        heating_performance_curve_outdoor_temperature_type: Literal["DryBulbTemperature", "WetBulbTemperature"]
        | None = "WetBulbTemperature",
        heating_energy_input_ratio_modifier_function_of_low_part_load_ratio_curve_name: str | None = ...,
        heating_energy_input_ratio_modifier_function_of_high_part_load_ratio_curve_name: str | None = ...,
        heating_combination_ratio_correction_factor_curve_name: str | None = ...,
        heating_part_load_fraction_correlation_curve_name: str | None = ...,
        minimum_heat_pump_part_load_ratio: float | None = 0.15,
        zone_name_for_master_thermostat_location: str | None = ...,
        master_thermostat_priority_control_type: Literal[
            "LoadPriority", "MasterThermostatPriority", "Scheduled", "ThermostatOffsetPriority", "ZonePriority"
        ]
        | None = "MasterThermostatPriority",
        thermostat_priority_schedule_name: str | None = ...,
        heat_pump_waste_heat_recovery: Literal["No", "Yes"] | None = "No",
        equivalent_piping_length_used_for_piping_correction_factor_in_cooling_mode: float | None = ...,
        vertical_height_used_for_piping_correction_factor: float | None = ...,
        piping_correction_factor_for_length_in_cooling_mode_curve_name: str | None = ...,
        piping_correction_factor_for_height_in_cooling_mode_coefficient: float | None = 0,
        equivalent_piping_length_used_for_piping_correction_factor_in_heating_mode: float | None = ...,
        piping_correction_factor_for_length_in_heating_mode_curve_name: str | None = ...,
        piping_correction_factor_for_height_in_heating_mode_coefficient: float | None = 0,
        crankcase_heater_power_per_compressor: float | None = 33,
        number_of_compressors: float | None = 2,
        ratio_of_compressor_size_to_total_compressor_capacity: float | None = 0.5,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater: float | None = 5,
        defrost_strategy: Literal["Resistive", "ReverseCycle"] | None = "Resistive",
        defrost_control: Literal["OnDemand", "Timed"] | None = "Timed",
        defrost_energy_input_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["Autosize"] | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        condenser_type: Literal["AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        water_condenser_volume_flow_rate: float | Literal["Autosize"] | None = ...,
        evaporative_condenser_effectiveness: float | None = 0.9,
        evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        evaporative_condenser_pump_rated_power_consumption: float | Literal["Autosize"] | None = 0,
        supply_water_storage_tank_name: str | None = ...,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        fuel_type: str | None = "Electricity",
        minimum_outdoor_temperature_in_heat_recovery_mode: float | None = ...,
        maximum_outdoor_temperature_in_heat_recovery_mode: float | None = ...,
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
    ) -> None:
        """Create a new ``AirConditioner:VariableRefrigerantFlow`` and add it to the document.

        Variable refrigerant flow (VRF) air-to-air heat pump condensing unit (includes one or more electric compressors and outdoor fan). Serves one or more VRF zone terminal units. See ZoneHVAC:TerminalUnit:VariableRefrigerantFlow and ZoneTerminalUnitList.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-variable-refrigerant-flow-equipment/#airconditionervariablerefrigerantflow
        """
