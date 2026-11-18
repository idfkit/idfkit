"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import versioned as _vd

class ScheduleFile_v8_9_to_v9_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        file_name: str,
        column_number: float,
        rows_to_skip_at_top: float,
        schedule_type_limits_name: str | None = ...,
        number_of_hours_of_data: float | None = 8760,
        column_separator: Literal["Comma", "Fixed", "Semicolon", "Tab"] | None = "Comma",
        interpolate_to_timestep: Literal["No", "Yes"] | None = "No",
        minutes_per_item: float | None = ...,
    ) -> None:
        """Create a new ``Schedule:File`` and add it to the document.

        A Schedule:File points to a text computer file that has 8760-8784 hours of data.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.1/io-reference/overview/group-schedules/#schedulefile
        """

class DaylightingControls_v9_6_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_space_name: str,
        daylighting_method: Literal["DElight", "SplitFlux"] | None = "SplitFlux",
        availability_schedule_name: str | None = ...,
        lighting_control_type: Literal["Continuous", "ContinuousOff", "Stepped"] | None = "Continuous",
        minimum_input_power_fraction_for_continuous_or_continuousoff_dimming_control: float | None = 0.3,
        minimum_light_output_fraction_for_continuous_or_continuousoff_dimming_control: float | None = 0.2,
        number_of_stepped_control_steps: float | None = 1,
        probability_lighting_will_be_reset_when_needed_in_manual_stepped_control: float | None = 1,
        glare_calculation_daylighting_reference_point_name: str | None = ...,
        glare_calculation_azimuth_angle_of_view_direction_clockwise_from_zone_y_axis: float | None = 0,
        maximum_allowable_discomfort_glare_index: float | None = 22,
        delight_gridding_resolution: float | None = ...,
        control_data: Sequence[
            _vd.DaylightingControlsControlDataItem_v9_6_to_v22_1 | _vd.DaylightingControlsControlDataGroup_v9_6_to_v22_1
        ] = ...,
    ) -> None:
        """Create a new ``Daylighting:Controls`` and add it to the document.

        Dimming of overhead electric lighting is determined from each reference point. Glare from daylighting is also calculated.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/energyplus-economics/cost-estimating/#daylightingcontrols
        """

class CoilWaterHeatingAirToWaterHeatPumpPumped_v23_2_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_heating_capacity: float,
        evaporator_air_inlet_node_name: str,
        evaporator_air_outlet_node_name: str,
        condenser_water_inlet_node_name: str,
        condenser_water_outlet_node_name: str,
        rated_cop: float | None = 3.2,
        rated_sensible_heat_ratio: float | None = 0.85,
        rated_evaporator_inlet_air_dry_bulb_temperature: float | None = 19.7,
        rated_evaporator_inlet_air_wet_bulb_temperature: float | None = 13.5,
        rated_condenser_inlet_water_temperature: float | None = 57.5,
        rated_evaporator_air_flow_rate: float | Literal["Autocalculate"] | None = ...,
        rated_condenser_water_flow_rate: float | Literal["Autocalculate"] | None = ...,
        evaporator_fan_power_included_in_rated_cop: Literal["No", "Yes"] | None = "Yes",
        condenser_pump_power_included_in_rated_cop: Literal["No", "Yes"] | None = "No",
        condenser_pump_heat_included_in_rated_heating_capacity_and_rated_cop: Literal["No", "Yes"] | None = "No",
        condenser_water_pump_power: float | None = 0,
        fraction_of_condenser_pump_heat_to_water: float | None = 0.2,
        crankcase_heater_capacity: float | None = 0,
        crankcase_heater_capacity_function_of_temperature_curve_name: str | None = ...,
        maximum_ambient_temperature_for_crankcase_heater_operation: float | None = 10,
        evaporator_air_temperature_type_for_curve_objects: Literal["DryBulbTemperature", "WetBulbTemperature"]
        | None = "WetBulbTemperature",
        heating_capacity_function_of_temperature_curve_name: str | None = ...,
        heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        heating_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        heating_cop_function_of_temperature_curve_name: str | None = ...,
        heating_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        heating_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:WaterHeating:AirToWaterHeatPump:Pumped`` and add it to the document.

        Heat pump water heater (HPWH) heating coil, air-to-water direct-expansion (DX) system which includes a water heating coil, evaporator air coil, evaporator fan, electric compressor, and water pump. Part of a WaterHeater:HeatPump:PumpedCondenser system.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-heating-and-cooling-coils/#coilwaterheatingairtowaterheatpumppumped
        """
