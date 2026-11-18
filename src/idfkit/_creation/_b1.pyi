"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class ScheduleYear:
    def __call__(
        self,
        name: str,
        /,
        *,
        schedule_type_limits_name: str | None = ...,
        schedule_weeks: Sequence[_g.ScheduleYearScheduleWeeksItem | _g.ScheduleYearScheduleWeeksGroup] = ...,
    ) -> None:
        """Create a new ``Schedule:Year`` and add it to the document.

        A Schedule:Year contains from 1 to 52 week schedules

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#scheduleyear
        """

class CoilCoolingDXSingleSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        gross_rated_sensible_heat_ratio: float | Literal["Autosize"],
        rated_air_flow_rate: float | Literal["Autosize"],
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        total_cooling_capacity_function_of_temperature_curve_name: str,
        total_cooling_capacity_function_of_flow_fraction_curve_name: str,
        energy_input_ratio_function_of_temperature_curve_name: str,
        energy_input_ratio_function_of_flow_fraction_curve_name: str,
        part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        gross_rated_cooling_cop: float | None = 3,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -25,
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        maximum_cycling_rate: float | None = 0,
        latent_capacity_time_constant: float | None = 0,
        condenser_air_inlet_node_name: str | None = ...,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        evaporative_condenser_effectiveness: float | None = 0.9,
        evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        evaporative_condenser_pump_rated_power_consumption: float | Literal["", "Autosize"] | None = 0,
        crankcase_heater_capacity: float | None = 0,
        crankcase_heater_capacity_function_of_temperature_curve_name: str | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        supply_water_storage_tank_name: str | None = ...,
        condensate_collection_water_storage_tank_name: str | None = ...,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        sensible_heat_ratio_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        report_ashrae_standard_127_performance_ratings: Literal["", "No", "Yes"] | None = "No",
        zone_name_for_condenser_placement: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:SingleSpeed`` and add it to the document.

        Direct expansion (DX) cooling coil and condensing unit (includes electric compressor and condenser fan), single-speed. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxsinglespeed
        """

class HeatPumpAirToWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        availability_schedule_name_heating: str | None = ...,
        availability_schedule_name_cooling: str | None = ...,
        operating_mode_control_method: Literal["", "EMSControlled", "Load", "ScheduledModes"] | None = "Load",
        operating_mode_control_option_for_multiple_unit: Literal[
            "", "Balanced", "CoolingPriority", "HeatingPriority", "SingleMode"
        ]
        | None = "SingleMode",
        operating_mode_control_schedule_name: str | None = ...,
        minimum_part_load_ratio: float | None = 0,
        rated_inlet_air_temperature_in_heating_mode: float | None = 8,
        rated_air_flow_rate_in_heating_mode: float | Literal["", "Autosize"] | None = "Autosize",
        rated_leaving_water_temperature_in_heating_mode: float | None = 40,
        rated_water_flow_rate_in_heating_mode: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_outdoor_air_temperature_in_heating_mode: float | None = -30,
        maximum_outdoor_air_temperature_in_heating_mode: float | None = 100,
        minimum_leaving_water_temperature_curve_name_in_heating_mode: str | None = ...,
        maximum_leaving_water_temperature_curve_name_in_heating_mode: str | None = ...,
        sizing_factor_for_heating: float | None = 1,
        rated_inlet_air_temperature_in_cooling_mode: float | None = 30,
        rated_air_flow_rate_in_cooling_mode: float | Literal["", "Autosize"] | None = "Autosize",
        rated_leaving_water_temperature_in_cooling_mode: float | None = 8,
        rated_water_flow_rate_in_cooling_mode: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_outdoor_air_temperature_in_cooling_mode: float | None = -30,
        maximum_outdoor_air_temperature_in_cooling_mode: float | None = 100,
        minimum_leaving_water_temperature_curve_name_in_cooling_mode: str | None = ...,
        maximum_leaving_water_temperature_curve_name_in_cooling_mode: str | None = ...,
        sizing_factor_for_cooling: float | None = 1,
        hot_water_inlet_node_name: str | None = ...,
        hot_water_outlet_node_name: str | None = ...,
        chilled_water_inlet_node_name: str | None = ...,
        chilled_water_outlet_node_name: str | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 10,
        heat_pump_defrost_control: Literal["", "None", "OnDemand", "Timed", "TimedEmpirical"] | None = "None",
        heat_pump_defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | None = 0,
        defrost_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        heat_pump_multiplier: int | None = 1,
        control_type: Literal["", "FixedSpeed", "VariableSpeed"] | None = "VariableSpeed",
        crankcase_heater_capacity: float | None = 0,
        crankcase_heater_capacity_function_of_temperature_curve_name: str | None = ...,
        maximum_ambient_temperature_for_crankcase_heater_operation: float | None = 10,
        number_of_speeds_for_heating: int | None = 1,
        rated_heating_capacity_at_speed_1: float | Literal["", "Autosize"] | None = "Autosize",
        rated_cop_for_heating_at_speed_1: float | None = 3,
        normalized_heating_capacity_function_of_temperature_curve_name_at_speed_1: str | None = ...,
        heating_energy_input_ratio_function_of_temperature_curve_name_at_speed_1: str | None = ...,
        heating_energy_input_ratio_function_of_plr_curve_name_at_speed_1: str | None = ...,
        rated_heating_capacity_at_speed_2: float | Literal["", "Autosize"] | None = "Autosize",
        rated_cop_for_heating_at_speed_2: float | None = ...,
        normalized_heating_capacity_function_of_temperature_curve_name_at_speed_2: str | None = ...,
        heating_energy_input_ratio_function_of_temperature_curve_name_at_speed_2: str | None = ...,
        heating_energy_input_ratio_function_of_plr_curve_name_at_speed_2: str | None = ...,
        rated_heating_capacity_at_speed_3: float | Literal["", "Autosize"] | None = "Autosize",
        rated_cop_for_heating_at_speed_3: float | None = ...,
        normalized_heating_capacity_function_of_temperature_curve_name_at_speed_3: str | None = ...,
        heating_energy_input_ratio_function_of_temperature_curve_name_at_speed_3: str | None = ...,
        heating_energy_input_ratio_function_of_plr_curve_name_at_speed_3: str | None = ...,
        rated_heating_capacity_at_speed_4: float | Literal["", "Autosize"] | None = "Autosize",
        rated_cop_for_heating_at_speed_4: float | None = ...,
        normalized_heating_capacity_function_of_temperature_curve_name_at_speed_4: str | None = ...,
        heating_energy_input_ratio_function_of_temperature_curve_name_at_speed_4: str | None = ...,
        heating_energy_input_ratio_function_of_plr_curve_name_at_speed_4: str | None = ...,
        rated_heating_capacity_at_speed_5: float | Literal["", "Autosize"] | None = "Autosize",
        rated_cop_for_heating_at_speed_5: float | None = ...,
        normalized_heating_capacity_function_of_temperature_curve_name_at_speed_5: str | None = ...,
        heating_energy_input_ratio_function_of_temperature_curve_name_at_speed_5: str | None = ...,
        heating_energy_input_ratio_function_of_plr_curve_name_at_speed_5: str | None = ...,
        booster_mode_on_heating: Literal["", "No", "Yes"] | None = "No",
        rated_heating_capacity_in_booster_mode: float | None = ...,
        rated_heating_cop_in_booster_mode: float | None = 3,
        normalized_heating_capacity_function_of_temperature_curve_name_in_booster_mode: str | None = ...,
        heating_energy_input_ratio_function_of_temperature_curve_name_in_booster_mode: str | None = ...,
        heating_energy_input_ratio_function_of_plr_curve_name_in_booster_mode: str | None = ...,
        number_of_speeds_for_cooling: int | None = 1,
        rated_cooling_capacity_at_speed_1: float | Literal["", "Autosize"] | None = "Autosize",
        rated_cop_for_cooling_at_speed_1: float | None = 3,
        normalized_cooling_capacity_function_of_temperature_curve_name_at_speed_1: str | None = ...,
        cooling_energy_input_ratio_function_of_temperature_curve_name_at_speed_1: str | None = ...,
        cooling_energy_input_ratio_function_of_plr_curve_name_at_speed_1: str | None = ...,
        rated_cooling_capacity_at_speed_2: float | Literal["", "Autosize"] | None = "Autosize",
        rated_cop_for_cooling_at_speed_2: float | None = ...,
        normalized_cooling_capacity_function_of_temperature_curve_name_at_speed_2: str | None = ...,
        cooling_energy_input_ratio_function_of_temperature_curve_name_at_speed_2: str | None = ...,
        cooling_energy_input_ratio_function_of_plr_curve_name_at_speed_2: str | None = ...,
        rated_cooling_capacity_at_speed_3: float | Literal["", "Autosize"] | None = "Autosize",
        rated_cop_for_cooling_at_speed_3: float | None = ...,
        normalized_cooling_capacity_function_of_temperature_curve_name_at_speed_3: str | None = ...,
        cooling_energy_input_ratio_function_of_temperature_curve_name_at_speed_3: str | None = ...,
        cooling_energy_input_ratio_function_of_plr_curve_name_at_speed_3: str | None = ...,
        rated_cooling_capacity_at_speed_4: float | Literal["", "Autosize"] | None = "Autosize",
        rated_cop_for_cooling_at_speed_4: float | None = ...,
        normalized_cooling_capacity_function_of_temperature_curve_name_at_speed_4: str | None = ...,
        cooling_energy_input_ratio_function_of_temperature_curve_name_at_speed_4: str | None = ...,
        cooling_energy_input_ratio_function_of_plr_curve_name_at_speed_4: str | None = ...,
        rated_cooling_capacity_at_speed_5: float | Literal["", "Autosize"] | None = "Autosize",
        rated_cop_for_cooling_at_speed_5: float | None = ...,
        normalized_cooling_capacity_function_of_temperature_curve_name_at_speed_5: str | None = ...,
        cooling_energy_input_ratio_function_of_temperature_curve_name_at_speed_5: str | None = ...,
        cooling_energy_input_ratio_function_of_plr_curve_name_at_speed_5: str | None = ...,
        booster_mode_on_cooling: Literal["", "No", "Yes"] | None = "No",
        rated_cooling_capacity_in_booster_mode: float | None = ...,
        rated_cooling_cop_in_booster_mode: float | None = 3,
        normalized_cooling_capacity_function_of_temperature_curve_name_in_booster_mode: str | None = ...,
        cooling_energy_input_ratio_function_of_temperature_curve_name_in_booster_mode: str | None = ...,
        cooling_energy_input_ratio_function_of_plr_curve_name_in_booster_mode: str | None = ...,
    ) -> None:
        """Create a new ``HeatPump:AirToWater`` and add it to the document.

        air-to-water heat pump system which provides either chilled or hot water with single- or variable speed compressors.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#heatpumpairtowater
        """

class AnyComponentCostLineItem:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        line_item_type: Literal[
            "Chiller:Electric",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:DX",
            "Coil:Heating:Fuel",
            "Construction",
            "Daylighting:Controls",
            "General",
            "Generator:Photovoltaic",
            "Lights",
            "Shading:Zone:Detailed",
        ],
        item_name: str,
        type: str | None = ...,
        object_end_use_key: str | None = ...,
        cost_per_each: float | None = ...,
        cost_per_area: float | None = ...,
        cost_per_unit_of_output_capacity: float | None = ...,
        cost_per_unit_of_output_capacity_per_cop: float | None = ...,
        cost_per_volume: float | None = ...,
        cost_per_volume_rate: float | None = ...,
        cost_per_energy_per_temperature_difference: float | None = ...,
        quantity: float | None = ...,
    ) -> None:
        """Create a new ``ComponentCost:LineItem`` and add it to the document.

        Each instance of this object creates a cost line item and will contribute to the total for a cost estimate.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/cost-estimating/#componentcostlineitem
        """

class AnyOutputTableReportPeriod:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        begin_month: int,
        begin_day_of_month: int,
        begin_hour_of_day: int,
        end_month: int,
        end_day_of_month: int,
        end_hour_of_day: int,
        begin_year: int | None = ...,
        end_year: int | None = ...,
    ) -> None:
        """Create a new ``Output:Table:ReportPeriod`` and add it to the document.

        This object allows the user to generate the resilience tabular reports over a subset of a run period. When it is defined, a series of reporting-period-specific resilience summary tables will be generated at the end of all tabular reports. Multiple reporting periods may be input.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/standard-output-reports/output-table-reportperiod/#outputtablereportperiod
        """
