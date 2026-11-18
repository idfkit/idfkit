"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class CoilHeatingDXVariableSpeed_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        indoor_air_inlet_node_name: str,
        indoor_air_outlet_node_name: str,
        energy_part_load_fraction_curve_name: str,
        speed_1_reference_unit_gross_rated_heating_capacity: float,
        speed_1_reference_unit_gross_rated_heating_cop: float,
        speed_1_reference_unit_rated_air_flow_rate: float,
        speed_1_heating_capacity_function_of_temperature_curve_name: str,
        speed_1_total_heating_capacity_function_of_air_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_1_energy_input_ratio_function_of_air_flow_fraction_curve_name: str,
        number_of_speeds: float | None = 2,
        nominal_speed_level: float | None = 2,
        rated_heating_capacity_at_selected_nominal_speed_level: float | Literal["Autosize"] | None = "Autosize",
        rated_air_flow_rate_at_selected_nominal_speed_level: float | Literal["Autosize"] | None = "Autosize",
        defrost_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -8,
        outdoor_dry_bulb_temperature_to_turn_on_compressor: float | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        crankcase_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        defrost_strategy: Literal["Resistive", "ReverseCycle"] | None = "ReverseCycle",
        defrost_control: Literal["OnDemand", "Timed"] | None = "Timed",
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["Autosize"] | None = 0,
        speed_2_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_2_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_2_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_2_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_2_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_3_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_3_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_3_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_3_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_4_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_4_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_4_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_4_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_5_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_5_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_5_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_5_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_6_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_6_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_6_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_6_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_7_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_7_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_7_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_7_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_8_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_8_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_8_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_8_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_9_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_9_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_9_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_9_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_10_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_10_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_10_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_10_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:DX:VariableSpeed`` and add it to the document.

        Direct expansion (DX) heating coil (air-to-air heat pump) and compressor unit (includes electric compressor and outdoor fan), variable-speed, with defrost controls. Requires two to ten sets of performance data and will interpolate between speeds.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-heating-and-cooling-coils/#coilheatingdxvariablespeed
        """

class MaterialPropertyHeatAndMoistureTransferRedistribution_v8_9_to_v22_1:
    def __call__(
        self,
        /,
        *,
        material_name: str,
        number_of_redistribution_points: float,
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
    ) -> None:
        """Create a new ``MaterialProperty:HeatAndMoistureTransfer:Redistribution`` and add it to the document.

        HeatBalanceAlgorithm = CombinedHeatAndMoistureFiniteElement solution algorithm only. Relationship between liquid transport coefficient and moisture content Has no effect with other HeatBalanceAlgorithm solution algorithms

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-surface-construction-elements/#materialpropertyheatandmoisturetransferredistribution
        """

class UnitarySystemPerformanceMultispeed_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        number_of_speeds_for_heating: float,
        number_of_speeds_for_cooling: float,
        single_mode_operation: Literal["No", "Yes"] | None = "No",
        no_load_supply_air_flow_rate_ratio: float | None = 1,
        flow_ratios: Sequence[
            _g.UnitarySystemPerformanceMultispeedFlowRatiosItem | _g.UnitarySystemPerformanceMultispeedFlowRatiosGroup
        ] = ...,
    ) -> None:
        """Create a new ``UnitarySystemPerformance:Multispeed`` and add it to the document.

        The UnitarySystemPerformance object is used to specify the air flow ratio at each operating speed. This object is primarily used for multispeed DX and water coils to allow operation at alternate flow rates different from those specified in the coil object.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-unitary-equipment/#unitarysystemperformancemultispeed
        """
