"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class SurfacePropertyConvectionCoefficients_v8_9_to_v9_4:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        surface_name: str,
        convection_coefficient_1_location: Literal["Inside", "Outside"],
        convection_coefficient_1_type: Literal[
            "ASHRAEVerticalWall",
            "AdaptiveConvectionAlgorithm",
            "AlamdariHammondStableHorizontal",
            "AlamdariHammondUnstableHorizontal",
            "AlamdariHammondVerticalWall",
            "AwbiHattonHeatedFloor",
            "AwbiHattonHeatedWall",
            "BeausoleilMorrisonMixedAssistedWall",
            "BeausoleilMorrisonMixedOpposingWall",
            "BeausoleilMorrisonMixedStableCeiling",
            "BeausoleilMorrisonMixedStableFloor",
            "BeausoleilMorrisonMixedUnstableCeiling",
            "BeausoleilMorrisonMixedUnstableFloor",
            "ClearRoof",
            "DOE-2",
            "EmmelRoof",
            "EmmelVertical",
            "FisherPedersenCeilingDiffuserCeiling",
            "FisherPedersenCeilingDiffuserFloor",
            "FisherPedersenCeilingDiffuserWalls",
            "FohannoPolidoriVerticalWall",
            "GoldsteinNovoselacCeilingDiffuserFloor",
            "GoldsteinNovoselacCeilingDiffuserWalls",
            "GoldsteinNovoselacCeilingDiffuserWindow",
            "ISO15099Windows",
            "KaradagChilledCeiling",
            "KhalifaEq3WallAwayFromHeat",
            "KhalifaEq4CeilingAwayFromHeat",
            "KhalifaEq5WallNearHeat",
            "KhalifaEq6NonHeatedWalls",
            "KhalifaEq7Ceiling",
            "McAdams",
            "Mitchell",
            "MoWitt",
            "NusseltJurges",
            "Schedule",
            "Simple",
            "SimpleCombined",
            "TARP",
            "UserCurve",
            "Value",
            "WaltonStableHorizontalOrTilt",
            "WaltonUnstableHorizontalOrTilt",
        ],
        convection_coefficient_1: float | None = ...,
        convection_coefficient_1_schedule_name: str | None = ...,
        convection_coefficient_1_user_curve_name: str | None = ...,
        convection_coefficient_2_location: Literal["Inside", "Outside"] | None = ...,
        convection_coefficient_2_type: Literal[
            "ASHRAEVerticalWall",
            "AdaptiveConvectionAlgorithm",
            "AlamdariHammondStableHorizontal",
            "AlamdariHammondUnstableHorizontal",
            "AlamdariHammondVerticalWall",
            "AwbiHattonHeatedFloor",
            "AwbiHattonHeatedWall",
            "BeausoleilMorrisonMixedAssistedWall",
            "BeausoleilMorrisonMixedOpposingWall",
            "BeausoleilMorrisonMixedStableCeiling",
            "BeausoleilMorrisonMixedStableFloor",
            "BeausoleilMorrisonMixedUnstableCeiling",
            "BeausoleilMorrisonMixedUnstableFloor",
            "ClearRoof",
            "DOE-2",
            "EmmelRoof",
            "EmmelVertical",
            "FisherPedersenCeilingDiffuserCeiling",
            "FisherPedersenCeilingDiffuserFloor",
            "FisherPedersenCeilingDiffuserWalls",
            "FohannoPolidoriVerticalWall",
            "GoldsteinNovoselacCeilingDiffuserFloor",
            "GoldsteinNovoselacCeilingDiffuserWalls",
            "GoldsteinNovoselacCeilingDiffuserWindow",
            "ISO15099Windows",
            "KaradagChilledCeiling",
            "KhalifaEq3WallAwayFromHeat",
            "KhalifaEq4CeilingAwayFromHeat",
            "KhalifaEq5WallNearHeat",
            "KhalifaEq6NonHeatedWalls",
            "KhalifaEq7Ceiling",
            "McAdams",
            "Mitchell",
            "MoWitt",
            "NusseltJurges",
            "Schedule",
            "Simple",
            "SimpleCombined",
            "TARP",
            "UserCurve",
            "Value",
            "WaltonStableHorizontalOrTilt",
            "WaltonUnstableHorizontalOrTilt",
        ]
        | None = ...,
        convection_coefficient_2: float | None = 0.1,
        convection_coefficient_2_schedule_name: str | None = ...,
        convection_coefficient_2_user_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``SurfaceProperty:ConvectionCoefficients`` and add it to the document.

        Allow user settable interior and/or exterior convection coefficients. Note that some other factors may limit the lower bounds for these values, such as for windows, the interior convection coefficient must be >.28, for trombe wall algorithm selection (zone), the interior convection coefficient must be >.1 for TARP interior convection, the lower limit is also .1 Minimum and maximum limits are set in HeatBalanceAlgorithm object. Defaults in HeatBalanceAlgorithm object are [.1,1000].

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyconvectioncoefficients
        """

class RunPeriod_v8_9:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        begin_month: float,
        begin_day_of_month: float,
        end_month: float,
        end_day_of_month: float,
        day_of_week_for_start_day: Literal[
            "Friday", "Monday", "Saturday", "Sunday", "Thursday", "Tuesday", "UseWeatherFile", "Wednesday"
        ]
        | None = "UseWeatherFile",
        use_weather_file_holidays_and_special_days: Literal["No", "Yes"] | None = "Yes",
        use_weather_file_daylight_saving_period: Literal["No", "Yes"] | None = "Yes",
        apply_weekend_holiday_rule: Literal["No", "Yes"] | None = "No",
        use_weather_file_rain_indicators: Literal["No", "Yes"] | None = "Yes",
        use_weather_file_snow_indicators: Literal["No", "Yes"] | None = "Yes",
        number_of_times_runperiod_to_be_repeated: float | None = 1,
        increment_day_of_week_on_repeat: Literal["No", "Yes"] | None = "Yes",
        start_year: float | None = ...,
    ) -> None:
        """Create a new ``RunPeriod`` and add it to the document.

        Specified a range of dates and other parameters for a weather file simulation. Multiple run periods may be input, but they may not overlap.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v8.9/io-reference/overview/group-location-climate-weather-file-access/#runperiod
        """

class Building_v8_9_to_v22_1:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        north_axis: float | None = 0,
        terrain: Literal["City", "Country", "Ocean", "Suburbs", "Urban"] | None = "Suburbs",
        loads_convergence_tolerance_value: float | None = 0.04,
        temperature_convergence_tolerance_value: float | None = 0.4,
        solar_distribution: Literal[
            "FullExterior",
            "FullExteriorWithReflections",
            "FullInteriorAndExterior",
            "FullInteriorAndExteriorWithReflections",
            "MinimalShadowing",
        ]
        | None = "FullExterior",
        maximum_number_of_warmup_days: float | None = 25,
        minimum_number_of_warmup_days: float | None = ...,
    ) -> None:
        """Create a new ``Building`` and add it to the document.

        Describes parameters that are used during the simulation of the building. There are necessary correlations between the entries for this object and some entries in the Site:WeatherStation and Site:HeightVariation objects, specifically the Terrain field.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-simulation-parameters/#building
        """

class ZoneBaseboardOutdoorTemperatureControlled_v9_6_to_v26_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        capacity_at_low_temperature: float,
        low_temperature: float,
        capacity_at_high_temperature: float,
        high_temperature: float,
        fraction_radiant: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``ZoneBaseboard:OutdoorTemperatureControlled`` and add it to the document.

        Specifies outside temperature-controlled electric baseboard heating. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.1/io-reference/overview/group-internal-gains-people-lights-other/#zonebaseboardoutdoortemperaturecontrolled
        """
