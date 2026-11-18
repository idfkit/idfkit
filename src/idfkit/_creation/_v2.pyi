"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class ZoneVentilationWindandStackOpenArea_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        opening_area: float | None = 0,
        opening_area_fraction_schedule_name: str | None = ...,
        opening_effectiveness: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        effective_angle: float | None = 0,
        height_difference: float | None = 0,
        discharge_coefficient_for_opening: float | Literal["", "Autocalculate"] | None = "Autocalculate",
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
    ) -> None:
        """Create a new ``ZoneVentilation:WindandStackOpenArea`` and add it to the document.

        This object is specified as natural ventilation driven by wind and stack effect only: Ventilation Wind = Cw * Opening Area * Schedule * WindSpd Ventilation Stack = Cd * Opening Area * Schedule * SQRT(2*g*DH*(|(Tzone-Todb)|/Tzone)) Total Ventilation = SQRT((Ventilation Wind)^2 + (Ventilation Stack)^2)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-airflow/#zoneventilationwindandstackopenarea
        """

class WindowPropertyStormWindow_v8_9_to_v22_1:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        window_name: str,
        storm_glass_layer_name: str,
        month_that_storm_glass_layer_is_put_on: float,
        day_of_month_that_storm_glass_layer_is_put_on: float,
        month_that_storm_glass_layer_is_taken_off: float,
        day_of_month_that_storm_glass_layer_is_taken_off: float,
        distance_between_storm_glass_layer_and_adjacent_glass: float | None = 0.05,
    ) -> None:
        """Create a new ``WindowProperty:StormWindow`` and add it to the document.

        This is a movable exterior glass layer that is usually applied in the winter and removed in the summer.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-thermal-zone-description-geometry/#windowpropertystormwindow
        """

class OutputDiagnostics_v8_9_to_v9_3:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        key_1: Literal[
            "DisplayAdvancedReportVariables",
            "DisplayAllWarnings",
            "DisplayExtraWarnings",
            "DisplayUnusedObjects",
            "DisplayUnusedSchedules",
            "DisplayWeatherMissingDataWarnings",
            "DisplayZoneAirHeatBalanceOffBalance",
            "DoNotMirrorAttachedShading",
            "DoNotMirrorDetachedShading",
            "ReportDetailedWarmupConvergence",
            "ReportDuringHVACSizingSimulation",
            "ReportDuringWarmup",
        ]
        | None = ...,
        key_2: Literal[
            "DisplayAdvancedReportVariables",
            "DisplayAllWarnings",
            "DisplayExtraWarnings",
            "DisplayUnusedObjects",
            "DisplayUnusedSchedules",
            "DisplayWeatherMissingDataWarnings",
            "DisplayZoneAirHeatBalanceOffBalance",
            "DoNotMirrorAttachedShading",
            "DoNotMirrorDetachedShading",
            "ReportDetailedWarmupConvergence",
            "ReportDuringHVACSizingSimulation",
            "ReportDuringWarmup",
        ]
        | None = ...,
    ) -> None:
        """Create a new ``Output:Diagnostics`` and add it to the document.

        Special keys to produce certain warning messages or effect certain simulation characteristics.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.3/io-reference/overview/group-simulation-parameters/#outputdiagnostics
        """
