"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class CoilCoolingWaterToAirHeatPumpEquationFit_v22_2_to_v23_1:
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
        gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        gross_rated_sensible_cooling_capacity: float | Literal["Autosize"],
        gross_rated_cooling_cop: float,
        total_cooling_capacity_curve_name: str,
        sensible_cooling_capacity_curve_name: str,
        cooling_power_consumption_curve_name: str,
        rated_entering_water_temperature: float | None = 30,
        rated_entering_air_dry_bulb_temperature: float | None = 27,
        rated_entering_air_wet_bulb_temperature: float | None = 19,
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
    ) -> None:
        """Create a new ``Coil:Cooling:WaterToAirHeatPump:EquationFit`` and add it to the document.

        Direct expansion (DX) cooling coil for water-to-air heat pump (includes electric compressor), single-speed, equation-fit model. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Equation-fit model uses normalized curves to describe the heat pump performance.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwatertoairheatpumpequationfit
        """

class CoilHeatingWaterToAirHeatPumpVariableSpeedEquationFit_v8_9_to_v22_1:
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
        speed_1_reference_unit_rated_air_flow: float,
        speed_1_reference_unit_rated_water_flow_rate: float,
        speed_1_heating_capacity_function_of_temperature_curve_name: str,
        speed_1_total_heating_capacity_function_of_air_flow_fraction_curve_name: str,
        speed_1_heating_capacity_function_of_water_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_1_energy_input_ratio_function_of_air_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_water_flow_fraction_curve_name: str,
        speed_1_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float,
        speed_1_waste_heat_function_of_temperature_curve_name: str,
        number_of_speeds: float | None = 2,
        nominal_speed_level: float | None = 2,
        rated_heating_capacity_at_selected_nominal_speed_level: float | Literal["Autosize"] | None = "Autosize",
        rated_air_flow_rate_at_selected_nominal_speed_level: float | Literal["Autosize"] | None = "Autosize",
        rated_water_flow_rate_at_selected_nominal_speed_level: float | Literal["Autosize"] | None = "Autosize",
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
    ) -> None:
        """Create a new ``Coil:Heating:WaterToAirHeatPump:VariableSpeedEquationFit`` and add it to the document.

        Direct expansion (DX) heating coil for water-to-air heat pump (includes electric compressor), variable-speed, equation-fit model. Equation-fit model uses normalized curves to describe the heat pump performance. Requires two to ten sets of performance data and will interpolate between speeds.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-heating-and-cooling-coils/#coilheatingwatertoairheatpumpvariablespeedequationfit
        """

class PlantEquipmentList_v8_9_to_v9_0:
    def __call__(
        self,
        name: str,
        /,
        *,
        equipment_1_object_type: str | None = ...,
        equipment_1_name: str | None = ...,
        equipment_2_object_type: str | None = ...,
        equipment_2_name: str | None = ...,
        equipment_3_object_type: str | None = ...,
        equipment_3_name: str | None = ...,
        equipment_4_object_type: str | None = ...,
        equipment_4_name: str | None = ...,
        equipment_5_object_type: str | None = ...,
        equipment_5_name: str | None = ...,
        equipment_6_object_type: str | None = ...,
        equipment_6_name: str | None = ...,
        equipment_7_object_type: str | None = ...,
        equipment_7_name: str | None = ...,
        equipment_8_object_type: str | None = ...,
        equipment_8_name: str | None = ...,
        equipment_9_object_type: str | None = ...,
        equipment_9_name: str | None = ...,
        equipment_10_object_type: str | None = ...,
        equipment_10_name: str | None = ...,
    ) -> None:
        """Create a new ``PlantEquipmentList`` and add it to the document.

        List plant equipment in order of operating priority, 1st in list will be used 1st, etc Use only plant equipment in this list. If no equipment object types and equipment names are specified, then the corresponding PlantEquipmentOperation:* object will assume all available plant equipment for the loop should be OFF (not operate) within the specified lower/upper limit.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.0/io-reference/overview/group-plant-condenser-control/#plantequipmentlist
        """

class AirTerminalSingleDuctVAVNoReheat_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_outlet_node_name: str,
        air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        zone_minimum_air_flow_input_method: Literal["Constant", "FixedFlowRate", "Scheduled"] | None = "Constant",
        constant_minimum_air_flow_fraction: float | Literal["Autosize"] | None = "Autosize",
        fixed_minimum_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        minimum_air_flow_fraction_schedule_name: str | None = ...,
        design_specification_outdoor_air_object_name: str | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:VAV:NoReheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume, with no reheat coil.
        """
