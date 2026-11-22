"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class OutputTableMonthly_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        digits_after_decimal: float | None = 2,
        variable_details: Sequence[
            _g.OutputTableMonthlyVariableDetailsItem | _g.OutputTableMonthlyVariableDetailsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Output:Table:Monthly`` and add it to the document.

        Provides a generic method of setting up tables of monthly results. The report has multiple columns that are each defined using a repeated group of fields for any number of columns. A single Output:Table:Monthly object often produces multiple tables in the output. A table is produced for every instance of a particular output variable. For example, a table defined with zone variables will be produced once for every zone.

        ``variable_details`` takes the extensible groups in order, one dict per group:

        ```python
        doc["Output:Table:Monthly"].add(
            "Output Table Monthly 1",
            variable_details=[
                {
                    "variable_or_meter_name": "Variable or Meter 1",
                    "aggregation_type_for_variable_or_meter": "HoursNegative",
                },
                {
                    "variable_or_meter_name": "Variable or Meter 2",
                    "aggregation_type_for_variable_or_meter": "HoursNonNegative",
                },
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/standard-output-reports/output-table-monthly/#outputtablemonthly
        """

class RunPeriod_v9_6_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        begin_month: float,
        begin_day_of_month: float,
        end_month: float,
        end_day_of_month: float,
        begin_year: float | None = ...,
        end_year: float | None = ...,
        day_of_week_for_start_day: Literal["Friday", "Monday", "Saturday", "Sunday", "Thursday", "Tuesday", "Wednesday"]
        | None = ...,
        use_weather_file_holidays_and_special_days: Literal["No", "Yes"] | None = "Yes",
        use_weather_file_daylight_saving_period: Literal["No", "Yes"] | None = "Yes",
        apply_weekend_holiday_rule: Literal["No", "Yes"] | None = "No",
        use_weather_file_rain_indicators: Literal["No", "Yes"] | None = "Yes",
        use_weather_file_snow_indicators: Literal["No", "Yes"] | None = "Yes",
        treat_weather_as_actual: Literal["No", "Yes"] | None = "No",
        first_hour_interpolation_starting_values: Literal["Hour1", "Hour24"] | None = "Hour24",
        validate: bool = True,
    ) -> None:
        """Create a new ``RunPeriod`` and add it to the document.

        Specify a range of dates and other parameters for a simulation. Multiple run periods may be input, but they may not overlap.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-location-climate-weather-file-access/#runperiod
        """

class ZoneHVACPackagedTerminalHeatPump_v8_9_to_v22_1:
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
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal["Coil:Heating:DX:SingleSpeed", "Coil:Heating:DX:VariableSpeed"],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        supplemental_heating_coil_name: str,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outdoor_air_mixer_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_convergence_tolerance: float | None = 0.001,
        cooling_convergence_tolerance: float | None = 0.001,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
        capacity_control_method: Literal["None", "SingleZoneVAV"] | None = "None",
        minimum_supply_air_temperature_in_cooling_mode: float | Literal["Autosize"] | None = "Autosize",
        maximum_supply_air_temperature_in_heating_mode: float | Literal["Autosize"] | None = "Autosize",
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneHVAC:PackagedTerminalHeatPump`` and add it to the document.

        Packaged terminal heat pump (PTHP). Forced-convection heating-cooling unit with supply fan, direct expansion (DX) cooling coil, DX heating coil (air-to-air heat pump), supplemental heating coil (gas, electric, hot water, or steam), and fixed-position outdoor air mixer.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-zone-forced-air-units/#zonehvacpackagedterminalheatpump
        """

class CoilHeatingGasMultiStage_v22_2_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        number_of_stages: int,
        stage_1_gas_burner_efficiency: float,
        stage_1_nominal_capacity: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        temperature_setpoint_node_name: str | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
        parasitic_gas_load: float | None = ...,
        stage_1_parasitic_electric_load: float | None = ...,
        stage_2_gas_burner_efficiency: float | None = ...,
        stage_2_nominal_capacity: float | Literal["Autosize"] | None = ...,
        stage_2_parasitic_electric_load: float | None = ...,
        stage_3_gas_burner_efficiency: float | None = ...,
        stage_3_nominal_capacity: float | Literal["Autosize"] | None = ...,
        stage_3_parasitic_electric_load: float | None = ...,
        stage_4_gas_burner_efficiency: float | None = ...,
        stage_4_nominal_capacity: float | Literal["Autosize"] | None = ...,
        stage_4_parasitic_electric_load: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:Heating:Gas:MultiStage`` and add it to the document.

        Gas heating coil, multi-stage. If the coil is located directly in an air loop branch or outdoor air equipment list, then it is controlled on leaving air temperature and the Temperature Setpoint Node Name must be specified. If the coil is contained within another component such as an air terminal unit, zone HVAC equipment, or unitary system, then the coil is controlled by the parent component and the setpoint node name is not entered.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-heating-and-cooling-coils/#coilheatinggasmultistage
        """
