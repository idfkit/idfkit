"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g
from .. import versioned as _vd

class ChillerConstantCOP_v8_9_to_v24_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        nominal_capacity: float | Literal["Autosize"],
        nominal_cop: float,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        design_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_condenser_water_flow_rate: float | Literal["Autosize"] | None = ...,
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        condenser_type: Literal["AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        chiller_flow_mode: Literal["ConstantFlow", "LeavingSetpointModulated", "NotModulated"] | None = "NotModulated",
        sizing_factor: float | None = 1,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``Chiller:ConstantCOP`` and add it to the document.

        This constant COP chiller model provides a means of quickly specifying a Chiller where performance data is not available.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.1/io-reference/overview/group-plant-equipment/#chillerconstantcop
        """

class ZonePropertyUserViewFactorsbySurfaceName_v8_9_to_v9_1:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        zone_name: str | None = ...,
        view_factors: Sequence[
            _vd.ZonePropertyUserViewFactorsbySurfaceNameViewFactorsItem_v8_9_to_v9_1
            | _vd.ZonePropertyUserViewFactorsbySurfaceNameViewFactorsGroup_v8_9_to_v9_1
        ] = ...,
    ) -> None:
        """Create a new ``ZoneProperty:UserViewFactors:bySurfaceName`` and add it to the document.

        View factors for Surface to Surface in a zone. (Number of Surfaces)**2 must be entered.
        """

class OutputTableSummaryReports_v8_9_to_v9_2:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        reports: Sequence[
            _vd.OutputTableSummaryReportsReportsItem_v8_9_to_v9_2
            | _vd.OutputTableSummaryReportsReportsGroup_v8_9_to_v9_2
        ] = ...,
    ) -> None:
        """Create a new ``Output:Table:SummaryReports`` and add it to the document.

        This object allows the user to call report types that are predefined and will appear with the other tabular reports. These predefined reports are sensitive to the OutputControl:Table:Style object and appear in the same files as the tabular reports. The entries for this object is a list of the predefined reports that should appear in the tabular report output file. There should be as many fields (A) in this object as there are keys in the following (minus AllSummary+AllMonthly+AllSummaryAndMonthly)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/standard-output-reports/output-table-summaryreports/#outputtablesummaryreports
        """

class CoolingTowerVariableSpeedMerkel_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        design_water_flow_rate: float | Literal["Autosize"],
        design_air_flow_rate: float | Literal["Autocalculate"],
        design_fan_power: float | Literal["Autocalculate"],
        fan_power_modifier_function_of_air_flow_rate_ratio_curve_name: str,
        u_factor_times_area_modifier_function_of_air_flow_ratio_curve_name: str,
        u_factor_times_area_modifier_function_of_wetbulb_temperature_difference_curve_name: str,
        u_factor_times_area_modifier_function_of_water_flow_ratio_curve_name: str,
        performance_input_method: Literal["NominalCapacity", "UFactorTimesAreaAndDesignWaterFlowRate"]
        | None = "NominalCapacity",
        heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None = 1.25,
        nominal_capacity: float | Literal["Autosize"] | None = ...,
        free_convection_nominal_capacity: float | Literal["Autocalculate"] | None = ...,
        free_convection_nominal_capacity_sizing_factor: float | None = 0.1,
        design_water_flow_rate_per_unit_of_nominal_capacity: float | None = ...,
        design_air_flow_rate_per_unit_of_nominal_capacity: float | None = ...,
        minimum_air_flow_rate_ratio: float | None = 0.2,
        design_fan_power_per_unit_of_nominal_capacity: float | None = 0.0105,
        free_convection_regime_air_flow_rate: float | Literal["Autocalculate"] | None = 0,
        free_convection_regime_air_flow_rate_sizing_factor: float | None = 0.1,
        design_air_flow_rate_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        free_convection_regime_u_factor_times_area_value: float | Literal["Autocalculate"] | None = 0,
        free_convection_u_factor_times_area_value_sizing_factor: float | None = 0.1,
        design_inlet_air_dry_bulb_temperature: float | None = 35,
        design_inlet_air_wet_bulb_temperature: float | None = 25.6,
        design_approach_temperature: float | Literal["Autosize"] | None = "Autosize",
        design_range_temperature: float | Literal["Autosize"] | None = "Autosize",
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
        number_of_cells: float | None = 1,
        cell_control: Literal["MaximalCell", "MinimalCell"] | None = "MinimalCell",
        cell_minimum_water_flow_rate_fraction: float | None = 0.33,
        cell_maximum_water_flow_rate_fraction: float | None = 2.5,
        sizing_factor: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``CoolingTower:VariableSpeed:Merkel`` and add it to the document.

        This tower model is based on Merkel's theory, which is also the basis for the tower model in ASHRAE's HVAC1 Toolkit. The open wet cooling tower is modeled as a counter flow heat exchanger with a variable-speed fan drawing air through the tower (induced-draft configuration). For a multi-cell tower, the capacity and air/water flow rate inputs are for the entire tower.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-condenser-equipment/#coolingtowervariablespeedmerkel
        """

class CoilHeatingWaterToAirHeatPumpVariableSpeedEquationFit_v22_2_to_v25_1:
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
        number_of_speeds: int | None = 2,
        nominal_speed_level: int | None = 2,
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-heating-and-cooling-coils/#coilheatingwatertoairheatpumpvariablespeedequationfit
        """

class AirLoopHVACOutdoorAirSystem_v8_9_to_v9_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        controller_list_name: str,
        outdoor_air_equipment_list_name: str,
        availability_manager_list_name: str | None = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:OutdoorAirSystem`` and add it to the document.

        Outdoor air subsystem for an AirLoopHVAC. Includes an outdoor air mixing box and optional outdoor air conditioning equipment such as heat recovery, preheat, and precool coils. From the perspective of the primary air loop the outdoor air system is treated as a single component.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.1/io-reference/overview/group-air-distribution/#airloophvacoutdoorairsystem
        """
