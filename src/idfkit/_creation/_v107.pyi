"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class RoomAirTemperaturePatternConstantGradient_v8_9_to_v22_1:
    def __call__(
        self,
        /,
        *,
        room_air_temperature_pattern_constant_gradient_name: str,
        control_integer_for_pattern_control_schedule_name: float,
        thermostat_offset: float | None = ...,
        return_air_offset: float | None = ...,
        exhaust_air_offset: float | None = ...,
        temperature_gradient: float | None = ...,
    ) -> None:
        """Create a new ``RoomAir:TemperaturePattern:ConstantGradient`` and add it to the document.

        Used to model room air with a fixed temperature gradient in the vertical direction. Used in combination with RoomAir:TemperaturePattern:UserDefined.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-room-air-models/#roomairtemperaturepatternconstantgradient
        """

class CoilCoolingWaterToAirHeatPumpVariableSpeedEquationFit_v22_2_to_v23_1:
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
        speed_1_reference_unit_gross_rated_total_cooling_capacity: float,
        speed_1_reference_unit_gross_rated_sensible_heat_ratio: float,
        speed_1_reference_unit_gross_rated_cooling_cop: float,
        speed_1_reference_unit_rated_air_flow_rate: float,
        speed_1_reference_unit_rated_water_flow_rate: float,
        speed_1_total_cooling_capacity_function_of_temperature_curve_name: str,
        speed_1_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str,
        speed_1_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_1_energy_input_ratio_function_of_air_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_water_flow_fraction_curve_name: str,
        speed_1_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float,
        speed_1_waste_heat_function_of_temperature_curve_name: str,
        number_of_speeds: int | None = 2,
        nominal_speed_level: int | None = 2,
        gross_rated_total_cooling_capacity_at_selected_nominal_speed_level: float
        | Literal["Autosize"]
        | None = "Autosize",
        rated_air_flow_rate_at_selected_nominal_speed_level: float | Literal["Autosize"] | None = "Autosize",
        rated_water_flow_rate_at_selected_nominal_speed_level: float | Literal["Autosize"] | None = "Autosize",
        nominal_time_for_condensate_to_begin_leaving_the_coil: float | None = 0,
        initial_moisture_evaporation_rate_divided_by_steady_state_ac_latent_capacity: float | None = 0,
        flag_for_using_hot_gas_reheat_0_or_1: float | None = 0,
        speed_2_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_2_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_2_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_2_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_2_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_2_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_2_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_2_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_2_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_3_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_3_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_3_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_3_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_3_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_3_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_3_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_3_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_3_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_4_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_4_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_4_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_4_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_4_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_4_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_4_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_4_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_4_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_5_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_5_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_5_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_5_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_5_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_5_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_5_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_5_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_5_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_6_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_6_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_6_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_6_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_6_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_6_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_6_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_6_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_6_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_7_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_7_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_7_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_7_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_7_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_7_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_7_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_7_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_7_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_8_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_8_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_8_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_8_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_8_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_8_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_8_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_8_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_8_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_9_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_9_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_9_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_9_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_9_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_9_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_9_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_9_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_9_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_10_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_10_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_10_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_10_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_10_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_10_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_10_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_10_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_10_waste_heat_function_of_temperature_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit`` and add it to the document.

        Direct expansion (DX) cooling coil for water-to-air heat pump (includes electric compressor), variable-speed, equation-fit model. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Equation-fit model uses normalized curves to describe the heat pump performance. Requires two to ten sets of performance data and will interpolate between speeds. Modeled as a single coil with variable-speed compressor.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwatertoairheatpumpvariablespeedequationfit
        """

class OutputControlFiles_v24_2_to_v25_1:
    def __call__(
        self,
        /,
        *,
        output_csv: Literal["No", "Yes"] | None = "No",
        output_mtr: Literal["No", "Yes"] | None = "Yes",
        output_eso: Literal["No", "Yes"] | None = "Yes",
        output_eio: Literal["No", "Yes"] | None = "Yes",
        output_tabular: Literal["No", "Yes"] | None = "Yes",
        output_sqlite: Literal["No", "Yes"] | None = "Yes",
        output_json: Literal["No", "Yes"] | None = "Yes",
        output_audit: Literal["No", "Yes"] | None = "Yes",
        output_space_sizing: Literal["No", "Yes"] | None = "Yes",
        output_zone_sizing: Literal["No", "Yes"] | None = "Yes",
        output_system_sizing: Literal["No", "Yes"] | None = "Yes",
        output_dxf: Literal["No", "Yes"] | None = "Yes",
        output_bnd: Literal["No", "Yes"] | None = "Yes",
        output_rdd: Literal["No", "Yes"] | None = "Yes",
        output_mdd: Literal["No", "Yes"] | None = "Yes",
        output_mtd: Literal["No", "Yes"] | None = "Yes",
        output_end: Literal["No", "Yes"] | None = "Yes",
        output_shd: Literal["No", "Yes"] | None = "Yes",
        output_dfs: Literal["No", "Yes"] | None = "Yes",
        output_glhe: Literal["No", "Yes"] | None = "Yes",
        output_delightin: Literal["No", "Yes"] | None = "Yes",
        output_delighteldmp: Literal["No", "Yes"] | None = "Yes",
        output_delightdfdmp: Literal["No", "Yes"] | None = "Yes",
        output_edd: Literal["No", "Yes"] | None = "Yes",
        output_dbg: Literal["No", "Yes"] | None = "Yes",
        output_perflog: Literal["No", "Yes"] | None = "Yes",
        output_sln: Literal["No", "Yes"] | None = "Yes",
        output_sci: Literal["No", "Yes"] | None = "Yes",
        output_wrl: Literal["No", "Yes"] | None = "Yes",
        output_screen: Literal["No", "Yes"] | None = "Yes",
        output_extshd: Literal["No", "Yes"] | None = "Yes",
        output_tarcog: Literal["No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``OutputControl:Files`` and add it to the document.

        Conditionally turn on/off output from EnergyPlus.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/input-for-output/#outputcontrolfiles
        """

class PhotovoltaicPerformanceEquivalentOneDiode_v22_2_to_v25_2:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        cell_type: Literal["AmorphousSilicon", "CrystallineSilicon"] | None = ...,
        number_of_cells_in_series: int | None = 36,
        active_area: float | None = 0.89,
        transmittance_absorptance_product: float | None = 0.95,
        semiconductor_bandgap: float | None = 1.12,
        shunt_resistance: float | None = 1000000,
        short_circuit_current: float | None = 6.5,
        open_circuit_voltage: float | None = 21.6,
        reference_temperature: float | None = 25,
        reference_insolation: float | None = 1000,
        module_current_at_maximum_power: float | None = 5.9,
        module_voltage_at_maximum_power: float | None = 17,
        temperature_coefficient_of_short_circuit_current: float | None = 0.02,
        temperature_coefficient_of_open_circuit_voltage: float | None = -0.079,
        nominal_operating_cell_temperature_test_ambient_temperature: float | None = 20,
        nominal_operating_cell_temperature_test_cell_temperature: float | None = 40,
        nominal_operating_cell_temperature_test_insolation: float | None = 800,
        module_heat_loss_coefficient: float | None = 30,
        total_heat_capacity: float | None = 50000,
    ) -> None:
        """Create a new ``PhotovoltaicPerformance:EquivalentOne-Diode`` and add it to the document.

        Describes the performance characteristics of Photovoltaic (PV) modules to be modeled using an equivalent one-diode circuit. This model is also known as the 4- or 5-parameter TRNSYS model for photovoltaics.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.2/io-reference/overview/group-electric-load-center-generator/#photovoltaicperformanceequivalentone-diode
        """

class ZoneHVACWaterToAirHeatPump_v9_2_to_v23_1:
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
        supply_air_fan_object_type: Literal["Fan:OnOff", "Fan:SystemModel"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:WaterToAirHeatPump:EquationFit", "Coil:Heating:WaterToAirHeatPump:VariableSpeedEquationFit"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:WaterToAirHeatPump:EquationFit", "Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit"
        ],
        cooling_coil_name: str,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        supplemental_heating_coil_name: str,
        availability_schedule_name: str | None = ...,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outdoor_air_mixer_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_cycling_rate: float | None = 2.5,
        heat_pump_time_constant: float | None = 60,
        fraction_of_on_cycle_power_use: float | None = 0.01,
        heat_pump_fan_delay_time: float | None = 60,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["Autosize"] | None = "Autosize",
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        outdoor_dry_bulb_temperature_sensor_node_name: str | None = ...,
        fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        heat_pump_coil_water_flow_mode: Literal["Constant", "ConstantOnDemand", "Cycling"] | None = "Cycling",
        design_specification_zonehvac_sizing_object_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:WaterToAirHeatPump`` and add it to the document.

        Water-to-air heat pump. Forced-convection heating-cooling unit with supply fan, water-to-air cooling and heating coils, supplemental heating coil (gas, electric, hot water, or steam), and fixed-position outdoor air mixer.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-zone-forced-air-units/#zonehvacwatertoairheatpump
        """
