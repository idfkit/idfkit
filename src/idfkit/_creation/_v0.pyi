"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class RunPeriodCustomRange_v8_9:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        begin_month: float,
        begin_day_of_month: float,
        begin_year: float,
        end_month: float,
        end_day_of_month: float,
        end_year: float,
        day_of_week_for_start_day: Literal[
            "", "Friday", "Monday", "Saturday", "Sunday", "Thursday", "Tuesday", "UseWeatherFile", "Wednesday"
        ]
        | None = "UseWeatherFile",
        use_weather_file_holidays_and_special_days: Literal["", "No", "Yes"] | None = "Yes",
        use_weather_file_daylight_saving_period: Literal["", "No", "Yes"] | None = "Yes",
        apply_weekend_holiday_rule: Literal["", "No", "Yes"] | None = "No",
        use_weather_file_rain_indicators: Literal["", "No", "Yes"] | None = "Yes",
        use_weather_file_snow_indicators: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``RunPeriod:CustomRange`` and add it to the document.

        run simulation for a custom created weather file
        """

class FenestrationSurfaceDetailed_v9_0_to_v26_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_type: Literal["Door", "GlassDoor", "TubularDaylightDiffuser", "TubularDaylightDome", "Window"],
        construction_name: str,
        building_surface_name: str,
        vertex_1_x_coordinate: float,
        vertex_1_y_coordinate: float,
        vertex_1_z_coordinate: float,
        vertex_2_x_coordinate: float,
        vertex_2_y_coordinate: float,
        vertex_2_z_coordinate: float,
        vertex_3_x_coordinate: float,
        vertex_3_y_coordinate: float,
        vertex_3_z_coordinate: float,
        outside_boundary_condition_object: str | None = ...,
        view_factor_to_ground: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        frame_and_divider_name: str | None = ...,
        multiplier: float | None = 1,
        number_of_vertices: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        vertex_4_x_coordinate: float | None = ...,
        vertex_4_y_coordinate: float | None = ...,
        vertex_4_z_coordinate: float | None = ...,
    ) -> None:
        """Create a new ``FenestrationSurface:Detailed`` and add it to the document.

        Allows for detailed entry of subsurfaces (windows, doors, glass doors, tubular daylighting devices).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.1/io-reference/overview/group-thermal-zone-description-geometry/#fenestrationsurfacedetailed
        """

class AirTerminalSingleDuctVAVHeatAndCoolNoReheat_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_outlet_node_name: str,
        air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        zone_minimum_air_flow_fraction: float,
        availability_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume for both cooling and heating, with no reheat coil.
        """

class PerformancePrecisionTradeoffs_v9_4_to_v9_5:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        use_coil_direct_solutions: Literal["", "No", "Yes"] | None = "No",
        zone_radiant_exchange_algorithm: Literal["", "CarrollMRT", "ScriptF"] | None = "ScriptF",
        override_mode: Literal[
            "", "Advanced", "Mode01", "Mode02", "Mode03", "Mode04", "Mode05", "Mode06", "Mode07", "Normal"
        ]
        | None = "Normal",
        maxzonetempdiff: float | None = 0.3,
        maxalloweddeltemp: float | None = 0.002,
    ) -> None:
        """Create a new ``PerformancePrecisionTradeoffs`` and add it to the document.

        This object enables users to choose certain options that speed up EnergyPlus simulation, but may lead to small decreases in accuracy of results.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-simulation-parameters/#performanceprecisiontradeoffs
        """
