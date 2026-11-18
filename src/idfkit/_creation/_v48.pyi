"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class Lights_v9_6_to_v23_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        design_level_calculation_method: Literal["", "LightingLevel", "Watts/Area", "Watts/Person"]
        | None = "LightingLevel",
        lighting_level: float | None = ...,
        watts_per_zone_floor_area: float | None = ...,
        watts_per_person: float | None = ...,
        return_air_fraction: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_visible: float | None = 0,
        fraction_replaceable: float | None = 1,
        end_use_subcategory: str | None = "General",
        return_air_fraction_calculated_from_plenum_temperature: Literal["", "No", "Yes"] | None = "No",
        return_air_fraction_function_of_plenum_temperature_coefficient_1: float | None = 0,
        return_air_fraction_function_of_plenum_temperature_coefficient_2: float | None = 0,
        return_air_heat_gain_node_name: str | None = ...,
        exhaust_air_heat_gain_node_name: str | None = ...,
    ) -> None:
        """Create a new ``Lights`` and add it to the document.

        Sets internal gains for lights in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.2/io-reference/energyplus-economics/cost-estimating/#lights
        """

class CoilHeatingWaterToAirHeatPumpParameterEstimation_v8_9_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        compressor_type: Literal["Reciprocating", "Rotary", "Scroll"],
        design_source_side_flow_rate: float,
        gross_rated_heating_capacity: float,
        high_pressure_cutoff: float,
        low_pressure_cutoff: float,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        load_side_total_heat_transfer_coefficient: float,
        superheat_temperature_at_the_evaporator_outlet: float,
        compressor_power_losses: float,
        compressor_efficiency: float,
        refrigerant_type: str | None = "R22",
        compressor_piston_displacement: float | None = ...,
        compressor_suction_discharge_pressure_drop: float | None = ...,
        compressor_clearance_factor: float | None = ...,
        refrigerant_volume_flow_rate: float | None = ...,
        volume_ratio: float | None = ...,
        leak_rate_coefficient: float | None = ...,
        source_side_heat_transfer_coefficient: float | None = ...,
        source_side_heat_transfer_resistance1: float | None = ...,
        source_side_heat_transfer_resistance2: float | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:WaterToAirHeatPump:ParameterEstimation`` and add it to the document.

        Direct expansion (DX) heating coil for water-to-air heat pump (includes electric compressor), single-speed, parameter estimation model. Parameter estimation model is a deterministic model that requires a consistent set of parameters to describe the operating conditions of the heat pump components.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-heating-and-cooling-coils/#coilheatingwatertoairheatpumpparameterestimation
        """

class PythonPluginTrendVariable_v9_3_to_v22_1:
    def __call__(
        self, name: str, /, *, name_of_a_python_plugin_variable: str, number_of_timesteps_to_be_logged: float
    ) -> None:
        """Create a new ``PythonPlugin:TrendVariable`` and add it to the document.

        This object sets up a Python plugin trend variable from an Python plugin variable A trend variable logs values across timesteps

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-python-plugins/#pythonplugintrendvariable
        """

class RunPeriod_v9_2_to_v9_5:
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
        use_weather_file_holidays_and_special_days: Literal["", "No", "Yes"] | None = "Yes",
        use_weather_file_daylight_saving_period: Literal["", "No", "Yes"] | None = "Yes",
        apply_weekend_holiday_rule: Literal["", "No", "Yes"] | None = "No",
        use_weather_file_rain_indicators: Literal["", "No", "Yes"] | None = "Yes",
        use_weather_file_snow_indicators: Literal["", "No", "Yes"] | None = "Yes",
        treat_weather_as_actual: Literal["", "No", "Yes"] | None = "No",
    ) -> None:
        """Create a new ``RunPeriod`` and add it to the document.

        Specify a range of dates and other parameters for a simulation. Multiple run periods may be input, but they may not overlap.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-location-climate-weather-file-access/#runperiod
        """
