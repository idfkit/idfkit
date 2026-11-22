"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import versioned as _vd

class SizingPeriodWeatherFileDays_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        begin_month: float,
        begin_day_of_month: float,
        end_month: float,
        end_day_of_month: float,
        day_of_week_for_start_day: Literal[
            "CustomDay1",
            "CustomDay2",
            "Friday",
            "Monday",
            "Saturday",
            "SummerDesignDay",
            "Sunday",
            "Thursday",
            "Tuesday",
            "Wednesday",
            "WinterDesignDay",
        ]
        | None = "Monday",
        use_weather_file_daylight_saving_period: Literal["No", "Yes"] | None = "Yes",
        use_weather_file_rain_and_snow_indicators: Literal["No", "Yes"] | None = "Yes",
        validate: bool = True,
    ) -> None:
        """Create a new ``SizingPeriod:WeatherFileDays`` and add it to the document.

        Use a weather file period for design sizing calculations.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-location-climate-weather-file-access/#sizingperiodweatherfiledays
        """

class ControllerMechanicalVentilation_v9_3_to_v9_4:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        demand_controlled_ventilation: Literal["No", "Yes"] | None = "No",
        system_outdoor_air_method: Literal[
            "IndoorAirQualityProcedure",
            "IndoorAirQualityProcedureCombined",
            "IndoorAirQualityProcedureGenericContaminant",
            "ProportionalControlBasedOnDesignOARate",
            "ProportionalControlBasedOnDesignOccupancy",
            "ProportionalControlBasedonOccupancySchedule",
            "VentilationRateProcedure",
            "ZoneSum",
        ]
        | None = "VentilationRateProcedure",
        zone_maximum_outdoor_air_fraction: float | None = 1,
        zone_specifications: Sequence[
            _vd.ControllerMechanicalVentilationZoneSpecificationsItem_v9_3_to_v9_4
            | _vd.ControllerMechanicalVentilationZoneSpecificationsGroup_v9_3_to_v9_4
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Controller:MechanicalVentilation`` and add it to the document.

        This object is used in conjunction with Controller:OutdoorAir to specify outdoor ventilation air based on outdoor air specified in the DesignSpecification:OutdoorAir object The Controller:OutdoorAir object is associated with a specific air loop, so the outdoor air flow rates specified in Controller:MechanicalVentilation correspond to the zones attached to that specific air loop. Duplicate groups of Zone name, Design Specification Outdoor Air Object Name, and Design Specification Zone Air Distribution Object Name to increase allowable number of entries

        ``zone_specifications`` takes the extensible groups in order, one dict per group:

        ```python
        doc["Controller:MechanicalVentilation"].add(
            "Controller MechanicalVentilation 1",
            zone_specifications=[
                {
                    "zone_or_zonelist_name": "Zone or ZoneList 1",
                    "design_specification_outdoor_air_object_name": "Design Specification Outdoor Air Object 1",
                    "design_specification_zone_air_distribution_object_name": "Design Specification Zone Air Distribution Object 1",
                },
                {
                    "zone_or_zonelist_name": "Zone or ZoneList 2",
                    "design_specification_outdoor_air_object_name": "Design Specification Outdoor Air Object 2",
                    "design_specification_zone_air_distribution_object_name": "Design Specification Zone Air Distribution Object 2",
                },
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-controllers/#controllermechanicalventilation
        """

class WallAdiabatic_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 90,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Wall:Adiabatic`` and add it to the document.

        Allows for simplified entry of interior walls.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-thermal-zone-description-geometry/#walladiabatic
        """
