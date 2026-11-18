"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class ZoneThermalChimney_v8_9_to_v24_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        width_of_the_absorber_wall: float,
        cross_sectional_area_of_air_channel_outlet: float,
        zone_1_name: str,
        distance_from_top_of_thermal_chimney_to_inlet_1: float,
        cross_sectional_areas_of_air_channel_inlet_1: float,
        availability_schedule_name: str | None = ...,
        discharge_coefficient: float | None = 0.8,
        relative_ratios_of_air_flow_rates_passing_through_zone_1: float | None = 1,
        zone_2_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_2: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_2: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_2: float | None = ...,
        zone_3_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_3: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_3: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_3: float | None = ...,
        zone_4_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_4: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_4: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_4: float | None = ...,
        zone_5_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_5: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_5: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_5: float | None = ...,
        zone_6_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_6: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_6: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_6: float | None = ...,
        zone_7_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_7: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_7: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_7: float | None = ...,
        zone_8_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_8: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_8: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_8: float | None = ...,
        zone_9_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_9: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_9: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_9: float | None = ...,
        zone_10_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_10: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_10: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_10: float | None = ...,
        zone_11_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_11: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_11: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_11: float | None = ...,
        zone_12_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_12: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_12: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_12: float | None = ...,
        zone_13_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_13: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_13: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_13: float | None = ...,
        zone_14_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_14: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_14: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_14: float | None = ...,
        zone_15_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_15: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_15: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_15: float | None = ...,
        zone_16_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_16: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_16: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_16: float | None = ...,
        zone_17_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_17: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_17: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_17: float | None = ...,
        zone_18_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_18: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_18: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_18: float | None = ...,
        zone_19_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_19: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_19: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_19: float | None = ...,
        zone_20_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_20: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_20: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_20: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneThermalChimney`` and add it to the document.

        A thermal chimney is a vertical shaft utilizing solar radiation to enhance natural ventilation. It consists of an absorber wall, air gap and glass cover with high solar transmissivity.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.1/io-reference/overview/group-airflow/#zonethermalchimney
        """

class MaterialPropertyHeatAndMoistureTransferSorptionIsotherm_v8_9_to_v22_1:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        material_name: str,
        number_of_isotherm_coordinates: float,
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
        validate: bool = True,
    ) -> None:
        """Create a new ``MaterialProperty:HeatAndMoistureTransfer:SorptionIsotherm`` and add it to the document.

        HeatBalanceAlgorithm = CombinedHeatAndMoistureFiniteElement solution algorithm only. Relationship between moisture content and relative humidity fraction. Has no effect with other HeatBalanceAlgorithm solution algorithms

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-surface-construction-elements/#materialpropertyheatandmoisturetransfersorptionisotherm
        """

class ZoneVentilationDesignFlowRate_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_name: str,
        schedule_name: str,
        design_flow_rate_calculation_method: Literal["AirChanges/Hour", "Flow/Area", "Flow/Person", "Flow/Zone"]
        | None = "Flow/Zone",
        design_flow_rate: float | None = ...,
        flow_rate_per_zone_floor_area: float | None = ...,
        flow_rate_per_person: float | None = ...,
        air_changes_per_hour: float | None = ...,
        ventilation_type: Literal["Balanced", "Exhaust", "Intake", "Natural"] | None = "Natural",
        fan_pressure_rise: float | None = 0,
        fan_total_efficiency: float | None = 1,
        constant_term_coefficient: float | None = 1,
        temperature_term_coefficient: float | None = 0,
        velocity_term_coefficient: float | None = 0,
        velocity_squared_term_coefficient: float | None = 0,
        minimum_indoor_temperature: float | None = -100,
        minimum_indoor_temperature_schedule_name: str | None = ...,
        maximum_indoor_temperature: float | None = 100,
        maximum_indoor_temperature_schedule_name: str | None = ...,
        delta_temperature: float | None = -100,
        delta_temperature_schedule_name: str | None = ...,
        minimum_outdoor_temperature: float | None = -100,
        minimum_outdoor_temperature_schedule_name: str | None = ...,
        maximum_outdoor_temperature: float | None = 100,
        maximum_outdoor_temperature_schedule_name: str | None = ...,
        maximum_wind_speed: float | None = 40,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneVentilation:DesignFlowRate`` and add it to the document.

        Ventilation is specified as a design level which is modified by a schedule fraction, temperature difference and wind speed: Ventilation=Vdesign * Fschedule * (A + B*|(Tzone-Todb)| + C*WindSpd + D * WindSpd**2) If you use a ZoneList in the Zone or ZoneList name field then this definition applies to all the zones in the ZoneList.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-airflow/#zoneventilationdesignflowrate
        """

class TableLookup_v9_2_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        independent_variable_list_name: str,
        normalization_method: Literal["AutomaticWithDivisor", "DivisorOnly", "None"] | None = "None",
        normalization_divisor: float | None = 1,
        minimum_output: float | None = ...,
        maximum_output: float | None = ...,
        output_unit_type: Literal["Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
        external_file_name: str | None = ...,
        external_file_column_number: float | None = ...,
        external_file_starting_row_number: float | None = ...,
        values: Sequence[_g.TableLookupValuesItem | _g.TableLookupValuesGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Table:Lookup`` and add it to the document.

        Lookup tables are used in place of curves and can represent any number of independent variables (defined as Table:IndependentVariable objects in a Table:IndependentVariableList). Output values are interpolated within the bounds defined by each independent variable and extrapolated beyond the bounds according to the interpolation/extrapolation methods defined by each independent variable.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-performance-tables/#tablelookup
        """
