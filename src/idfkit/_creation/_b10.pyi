"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class AnySizingPeriodDesignDay:
    def __call__(
        self,
        name: str,
        /,
        *,
        month: int,
        day_of_month: int,
        day_type: Literal[
            "CustomDay1",
            "CustomDay2",
            "Friday",
            "Holiday",
            "Monday",
            "Saturday",
            "SummerDesignDay",
            "Sunday",
            "Thursday",
            "Tuesday",
            "Wednesday",
            "WinterDesignDay",
        ],
        wind_speed: float,
        wind_direction: float,
        maximum_dry_bulb_temperature: float | None = ...,
        daily_dry_bulb_temperature_range: float | None = 0,
        dry_bulb_temperature_range_modifier_type: Literal[
            "", "DefaultMultipliers", "DifferenceSchedule", "MultiplierSchedule", "TemperatureProfileSchedule"
        ]
        | None = "DefaultMultipliers",
        dry_bulb_temperature_range_modifier_day_schedule_name: str | None = ...,
        humidity_condition_type: Literal[
            "",
            "DewPoint",
            "Enthalpy",
            "HumidityRatio",
            "RelativeHumiditySchedule",
            "WetBulb",
            "WetBulbProfileDefaultMultipliers",
            "WetBulbProfileDifferenceSchedule",
            "WetBulbProfileMultiplierSchedule",
        ]
        | None = "WetBulb",
        wetbulb_or_dewpoint_at_maximum_dry_bulb: float | None = ...,
        humidity_condition_day_schedule_name: str | None = ...,
        humidity_ratio_at_maximum_dry_bulb: float | None = ...,
        enthalpy_at_maximum_dry_bulb: float | None = ...,
        daily_wet_bulb_temperature_range: float | None = ...,
        barometric_pressure: float | None = ...,
        rain_indicator: Literal["", "No", "Yes"] | None = "No",
        snow_indicator: Literal["", "No", "Yes"] | None = "No",
        daylight_saving_time_indicator: Literal["", "No", "Yes"] | None = "No",
        solar_model_indicator: Literal["", "ASHRAEClearSky", "ASHRAETau", "Schedule", "ZhangHuang"]
        | None = "ASHRAEClearSky",
        beam_solar_day_schedule_name: str | None = ...,
        diffuse_solar_day_schedule_name: str | None = ...,
        ashrae_clear_sky_optical_depth_for_beam_irradiance_taub_: float | None = 0,
        ashrae_clear_sky_optical_depth_for_diffuse_irradiance_taud_: float | None = 0,
        sky_clearness: float | None = 0,
        ashrae_clear_sky_optical_depth_for_beam_irradiance_taub: float | None = ...,
        ashrae_clear_sky_optical_depth_for_diffuse_irradiance_taud: float | None = ...,
    ) -> None:
        """Create a new ``SizingPeriod:DesignDay`` and add it to the document.

        The design day object creates the parameters for the program to create the 24 hour weather profile that can be used for sizing as well as running to test the other simulation parameters. Parameters in this include a date (month and day), a day type (which uses the appropriate schedules for either sizing or simple tests), min/max temperatures, wind speeds, and solar radiation values.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sizingperioddesignday
        """

class SiteGroundTemperatureShallow:
    def __call__(
        self,
        /,
        *,
        january_surface_ground_temperature: float | None = 13,
        february_surface_ground_temperature: float | None = 13,
        march_surface_ground_temperature: float | None = 13,
        april_surface_ground_temperature: float | None = 13,
        may_surface_ground_temperature: float | None = 13,
        june_surface_ground_temperature: float | None = 13,
        july_surface_ground_temperature: float | None = 13,
        august_surface_ground_temperature: float | None = 13,
        september_surface_ground_temperature: float | None = 13,
        october_surface_ground_temperature: float | None = 13,
        november_surface_ground_temperature: float | None = 13,
        december_surface_ground_temperature: float | None = 13,
    ) -> None:
        """Create a new ``Site:GroundTemperature:Shallow`` and add it to the document.

        These temperatures are specifically for the Surface Ground Heat Exchanger and should probably be close to the average outdoor air temperature for the location. They are not used in other models.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitegroundtemperatureshallow
        """

class AnySiteGroundTemperatureUndisturbedXing:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        soil_thermal_conductivity: float,
        soil_density: float,
        soil_specific_heat: float,
        soil_surface_temperature_amplitude_1: float,
        soil_surface_temperature_amplitude_2: float,
        phase_shift_of_temperature_amplitude_1: float,
        phase_shift_of_temperature_amplitude_2: float,
    ) -> None:
        """Create a new ``Site:GroundTemperature:Undisturbed:Xing`` and add it to the document.

        Undisturbed ground temperature object using the Xing 2014 2 harmonic parameter model.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitegroundtemperatureundisturbedxing
        """

class ScheduleDayHourly:
    def __call__(
        self,
        name: str,
        /,
        *,
        schedule_type_limits_name: str | None = ...,
        hour_1: float | None = 0,
        hour_2: float | None = 0,
        hour_3: float | None = 0,
        hour_4: float | None = 0,
        hour_5: float | None = 0,
        hour_6: float | None = 0,
        hour_7: float | None = 0,
        hour_8: float | None = 0,
        hour_9: float | None = 0,
        hour_10: float | None = 0,
        hour_11: float | None = 0,
        hour_12: float | None = 0,
        hour_13: float | None = 0,
        hour_14: float | None = 0,
        hour_15: float | None = 0,
        hour_16: float | None = 0,
        hour_17: float | None = 0,
        hour_18: float | None = 0,
        hour_19: float | None = 0,
        hour_20: float | None = 0,
        hour_21: float | None = 0,
        hour_22: float | None = 0,
        hour_23: float | None = 0,
        hour_24: float | None = 0,
    ) -> None:
        """Create a new ``Schedule:Day:Hourly`` and add it to the document.

        A Schedule:Day:Hourly contains 24 values for each hour of the day.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#scheduledayhourly
        """

class ScheduleWeekDaily:
    def __call__(
        self,
        name: str,
        /,
        *,
        sunday_schedule_day_name: str,
        monday_schedule_day_name: str,
        tuesday_schedule_day_name: str,
        wednesday_schedule_day_name: str,
        thursday_schedule_day_name: str,
        friday_schedule_day_name: str,
        saturday_schedule_day_name: str,
        holiday_schedule_day_name: str,
        summerdesignday_schedule_day_name: str,
        winterdesignday_schedule_day_name: str,
        customday1_schedule_day_name: str,
        customday2_schedule_day_name: str,
    ) -> None:
        """Create a new ``Schedule:Week:Daily`` and add it to the document.

        A Schedule:Week:Daily contains 12 Schedule:Day:Hourly objects, one for each day type.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#scheduleweekdaily
        """

class ScheduleWeekCompact:
    def __call__(self, name: str, /, *, data: list[_g.ScheduleWeekCompactDataItem] = ...) -> None:
        """Create a new ``Schedule:Week:Compact`` and add it to the document.

        Compact definition for Schedule:Day:List

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#scheduleweekcompact
        """

class AnyWindowMaterialComplexShade:
    def __call__(
        self,
        name: str,
        /,
        *,
        layer_type: Literal["", "BSDF", "OtherShadingType", "Perforated", "Woven"] | None = "OtherShadingType",
        thickness: float | None = 0.002,
        conductivity: float | None = 1,
        ir_transmittance: float | None = 0,
        front_emissivity: float | None = 0.84,
        back_emissivity: float | None = 0.84,
        top_opening_multiplier: float | None = 0,
        bottom_opening_multiplier: float | None = 0,
        left_side_opening_multiplier: float | None = 0,
        right_side_opening_multiplier: float | None = 0,
        front_opening_multiplier: float | None = 0.05,
        slat_width: float | None = 0.016,
        slat_spacing: float | None = 0.012,
        slat_thickness: float | None = 0.0006,
        slat_angle: float | None = 90,
        slat_conductivity: float | None = 160,
        slat_curve: float | None = 0,
    ) -> None:
        """Create a new ``WindowMaterial:ComplexShade`` and add it to the document.

        Complex window shading layer thermal properties

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialcomplexshade
        """

class WindowMaterialComplexShade:
    def __call__(
        self,
        name: str,
        /,
        *,
        layer_type: Literal[
            "", "BSDF", "OtherShadingType", "Perforated", "VenetianHorizontal", "VenetianVertical", "Woven"
        ]
        | None = "OtherShadingType",
        thickness: float | None = 0.002,
        conductivity: float | None = 1,
        ir_transmittance: float | None = 0,
        front_emissivity: float | None = 0.84,
        back_emissivity: float | None = 0.84,
        top_opening_multiplier: float | None = 0,
        bottom_opening_multiplier: float | None = 0,
        left_side_opening_multiplier: float | None = 0,
        right_side_opening_multiplier: float | None = 0,
        front_opening_multiplier: float | None = 0.05,
        slat_width: float | None = 0.016,
        slat_spacing: float | None = 0.012,
        slat_thickness: float | None = 0.0006,
        slat_angle: float | None = 90,
        slat_conductivity: float | None = 160,
        slat_curve: float | None = 0,
    ) -> None:
        """Create a new ``WindowMaterial:ComplexShade`` and add it to the document.

        Complex window shading layer thermal properties

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialcomplexshade
        """

class AnyMaterialPropertyHeatAndMoistureTransferRedistribution:
    def __call__(
        self,
        /,
        *,
        material_name: str,
        number_of_redistribution_points: int,
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertyheatandmoisturetransferredistribution
        """

class ConstructionWindowEquivalentLayer:
    def __call__(
        self,
        name: str,
        /,
        *,
        outside_layer: str,
        layer_2: str | None = ...,
        layer_3: str | None = ...,
        layer_4: str | None = ...,
        layer_5: str | None = ...,
        layer_6: str | None = ...,
        layer_7: str | None = ...,
        layer_8: str | None = ...,
        layer_9: str | None = ...,
        layer_10: str | None = ...,
        layer_11: str | None = ...,
    ) -> None:
        """Create a new ``Construction:WindowEquivalentLayer`` and add it to the document.

        Start with outside layer and work your way to the inside Layer Up to 11 layers total. Up to six solid layers and up to five gaps. Enter the material name for each layer

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#constructionwindowequivalentlayer
        """

class ConstructionWindowDataFile:
    def __call__(self, name: str, /, *, file_name: str | None = ...) -> None:
        """Create a new ``Construction:WindowDataFile`` and add it to the document.

        Initiates search of the Window data file for a window called Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#constructionwindowdatafile
        """

class WallAdiabatic:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        space_name: str | None = ...,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 90,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None:
        """Create a new ``Wall:Adiabatic`` and add it to the document.

        Allows for simplified entry of interior walls.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#walladiabatic
        """

class ShadingFinProjection:
    def __call__(
        self,
        name: str,
        /,
        *,
        window_or_door_name: str,
        left_extension_from_window_door: float | None = ...,
        left_distance_above_top_of_window: float | None = ...,
        left_distance_below_bottom_of_window: float | None = ...,
        left_tilt_angle_from_window_door: float | None = 90,
        left_depth_as_fraction_of_window_door_width: float | None = ...,
        right_extension_from_window_door: float | None = ...,
        right_distance_above_top_of_window: float | None = ...,
        right_distance_below_bottom_of_window: float | None = ...,
        right_tilt_angle_from_window_door: float | None = 90,
        right_depth_as_fraction_of_window_door_width: float | None = ...,
    ) -> None:
        """Create a new ``Shading:Fin:Projection`` and add it to the document.

        Fins are usually shading surfaces that are perpendicular to a window or door.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#shadingfinprojection
        """

class AnySwimmingPoolIndoor:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_name: str,
        average_depth: float,
        activity_factor_schedule_name: str,
        make_up_water_supply_schedule_name: str,
        cover_schedule_name: str,
        pool_water_inlet_node: str,
        pool_water_outlet_node: str,
        setpoint_temperature_schedule: str,
        maximum_number_of_people: float,
        cover_evaporation_factor: float | None = 0,
        cover_convection_factor: float | None = 0,
        cover_short_wavelength_radiation_factor: float | None = 0,
        cover_long_wavelength_radiation_factor: float | None = 0,
        pool_heating_system_maximum_water_flow_rate: float | None = ...,
        pool_miscellaneous_equipment_power: float | None = ...,
        people_schedule: str | None = ...,
        people_heat_gain_schedule: str | None = ...,
    ) -> None:
        """Create a new ``SwimmingPool:Indoor`` and add it to the document.

        Specifies an indoor swimming pools linked to a floor surface. The pool is assumed to cover the entire floor to which it is linked.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#swimmingpoolindoor
        """

class AirflowNetworkMultiZoneReferenceCrackConditions:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_temperature: float,
        reference_barometric_pressure: float | None = 101325,
        reference_humidity_ratio: float | None = 0,
    ) -> None:
        """Create a new ``AirflowNetwork:MultiZone:ReferenceCrackConditions`` and add it to the document.

        This object specifies the conditions under which the air mass flow coefficient was measured.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkmultizonereferencecrackconditions
        """

class AnyHVACTemplateZonePTHP:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        template_thermostat_name: str | None = ...,
        cooling_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        heating_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        outdoor_air_method: Literal[
            "", "DetailedSpecification", "Flow/Area", "Flow/Person", "Flow/Zone", "Maximum", "Sum"
        ]
        | None = "Flow/Person",
        outdoor_air_flow_rate_per_person: float | None = 0.00944,
        outdoor_air_flow_rate_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_rate_per_zone: float | None = 0,
        system_availability_schedule_name: str | None = ...,
        supply_fan_operating_mode_schedule_name: str | None = ...,
        supply_fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 75,
        supply_fan_motor_efficiency: float | None = 0.9,
        cooling_coil_type: Literal["", "SingleSpeedDX"] | None = "SingleSpeedDX",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_coil_gross_rated_total_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_cop: float | None = 3,
        heat_pump_heating_coil_type: Literal["", "SingleSpeedDXHeatPump"] | None = "SingleSpeedDXHeatPump",
        heat_pump_heating_coil_availability_schedule_name: str | None = ...,
        heat_pump_heating_coil_gross_rated_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        heat_pump_heating_coil_gross_rated_cop: float | None = 2.75,
        heat_pump_heating_minimum_outdoor_dry_bulb_temperature: float | None = -8,
        heat_pump_defrost_maximum_outdoor_dry_bulb_temperature: float | None = 5,
        heat_pump_defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "ReverseCycle",
        heat_pump_defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        heat_pump_defrost_time_period_fraction: float | None = 0.058333,
        supplemental_heating_coil_type: Literal["", "Electric", "Gas", "HotWater"] | None = "Electric",
        supplemental_heating_coil_availability_schedule_name: str | None = ...,
        supplemental_heating_coil_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        supplemental_heating_coil_maximum_outdoor_dry_bulb_temperature: float | None = 21,
        supplemental_gas_heating_coil_efficiency: float | None = 0.8,
        supplemental_gas_heating_coil_parasitic_electric_load: float | None = 0,
        dedicated_outdoor_air_system_name: str | None = ...,
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_cooling_design_supply_air_temperature: float | None = 14,
        zone_cooling_design_supply_air_temperature_difference: float | None = 11.11,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = 50,
        zone_heating_design_supply_air_temperature_difference: float | None = 30,
        design_specification_outdoor_air_object_name: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        baseboard_heating_type: Literal["", "Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["", "Autosize"] | None = "Autosize",
    ) -> None:
        """Create a new ``HVACTemplate:Zone:PTHP`` and add it to the document.

        Packaged Terminal Heat Pump

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezonepthp
        """

class HVACTemplateSystemUnitary:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_zone_or_thermostat_location_name: str,
        heating_coil_type: Literal["Electric", "Gas", "HotWater"],
        system_availability_schedule_name: str | None = ...,
        supply_fan_maximum_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        supply_fan_operating_mode_schedule_name: str | None = ...,
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 600,
        supply_fan_motor_efficiency: float | None = 0.9,
        supply_fan_motor_in_air_stream_fraction: float | None = 1,
        cooling_coil_type: Literal["", "None", "SingleSpeedDX"] | None = "SingleSpeedDX",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_design_supply_air_temperature: float | None = 12.8,
        cooling_coil_gross_rated_total_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_cop: float | None = 3,
        heating_coil_availability_schedule_name: str | None = ...,
        heating_design_supply_air_temperature: float | None = 50,
        heating_coil_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        gas_heating_coil_efficiency: float | None = 0.8,
        gas_heating_coil_parasitic_electric_load: float | None = 0,
        maximum_outdoor_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_outdoor_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_outdoor_air_schedule_name: str | None = ...,
        economizer_type: Literal[
            "",
            "DifferentialDryBulb",
            "DifferentialDryBulbAndEnthalpy",
            "DifferentialEnthalpy",
            "ElectronicEnthalpy",
            "FixedDewPointAndDryBulb",
            "FixedDryBulb",
            "FixedEnthalpy",
            "NoEconomizer",
        ]
        | None = "NoEconomizer",
        economizer_lockout: Literal["", "LockoutWithCompressor", "LockoutWithHeating", "NoLockout"]
        | None = "NoLockout",
        economizer_upper_temperature_limit: float | None = ...,
        economizer_lower_temperature_limit: float | None = ...,
        economizer_upper_enthalpy_limit: float | None = ...,
        economizer_maximum_limit_dewpoint_temperature: float | None = ...,
        supply_plenum_name: str | None = ...,
        return_plenum_name: str | None = ...,
        supply_fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
        night_cycle_control: Literal["", "CycleOnAny", "CycleOnControlZone", "StayOff"] | None = "StayOff",
        night_cycle_control_zone_name: str | None = ...,
        heat_recovery_type: Literal["", "Enthalpy", "None", "Sensible"] | None = "None",
        sensible_heat_recovery_effectiveness: float | None = 0.7,
        latent_heat_recovery_effectiveness: float | None = 0.65,
        dehumidification_control_type: Literal["", "CoolReheatDesuperheater", "CoolReheatHeatingCoil", "None"]
        | None = "None",
        dehumidification_setpoint: float | None = 60,
        humidifier_type: Literal["", "ElectricSteam", "None"] | None = "None",
        humidifier_availability_schedule_name: str | None = ...,
        humidifier_rated_capacity: float | None = ...,
        humidifier_rated_electric_power: float | Literal["", "Autosize"] | None = "Autosize",
        humidifier_control_zone_name: str | None = ...,
        humidifier_setpoint: float | None = 30,
        return_fan: Literal["", "No", "Yes"] | None = "No",
        return_fan_total_efficiency: float | None = 0.7,
        return_fan_delta_pressure: float | None = 500,
        return_fan_motor_efficiency: float | None = 0.9,
        return_fan_motor_in_air_stream_fraction: float | None = 1,
    ) -> None:
        """Create a new ``HVACTemplate:System:Unitary`` and add it to the document.

        Unitary furnace with air conditioner

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatesystemunitary
        """

class ThermostatSetpointDualSetpoint:
    def __call__(
        self,
        name: str,
        /,
        *,
        heating_setpoint_temperature_schedule_name: str | None = ...,
        cooling_setpoint_temperature_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``ThermostatSetpoint:DualSetpoint`` and add it to the document.

        Used for a heating and cooling thermostat with dual setpoints. The setpoints can be scheduled and varied throughout the simulation for both heating and cooling.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-controls-thermostats/#thermostatsetpointdualsetpoint
        """

class ZoneHVACHybridUnitaryHVAC:
    def __call__(
        self,
        name: str,
        /,
        *,
        return_air_node_name: str,
        outdoor_air_node_name: str,
        supply_air_node_name: str,
        availability_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        minimum_supply_air_temperature_schedule_name: str | None = ...,
        maximum_supply_air_temperature_schedule_name: str | None = ...,
        minimum_supply_air_humidity_ratio_schedule_name: str | None = ...,
        maximum_supply_air_humidity_ratio_schedule_name: str | None = ...,
        method_to_choose_controlled_inputs_and_part_runtime_fraction: Literal["", "Automatic", "User Defined"]
        | None = "Automatic",
        relief_node_name: str | None = ...,
        system_maximum_supply_air_flow_rate: float | None = ...,
        external_static_pressure_at_system_maximum_supply_air_flow_rate: float | None = ...,
        fan_heat_included_in_lookup_tables: Literal["", "No", "Yes"] | None = "No",
        fan_heat_gain_location: Literal["", "MixedAirStream", "SupplyAirStream"] | None = "SupplyAirStream",
        fan_heat_in_air_stream_fraction: float | None = 1,
        scaling_factor: float | None = 1,
        minimum_time_between_mode_change: float | None = 10,
        first_fuel_type: Literal[
            "",
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = "Electricity",
        second_fuel_type: Literal[
            "",
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = "None",
        third_fuel_type: Literal[
            "",
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = "None",
        objective_function_to_minimize: Literal["", "Electricity Use", "Second Fuel Use", "Third Fuel Use", "Water Use"]
        | None = "Electricity Use",
        design_specification_outdoor_air_object_name: str | None = ...,
        mode_0_name: str | None = ...,
        mode_0_supply_air_temperature_lookup_table_name: str | None = ...,
        mode_0_supply_air_humidity_ratio_lookup_table_name: str | None = ...,
        mode_0_system_electric_power_lookup_table_name: str | None = ...,
        mode_0_supply_fan_electric_power_lookup_table_name: str | None = ...,
        mode_0_external_static_pressure_lookup_table_name: str | None = ...,
        mode_0_system_second_fuel_consumption_lookup_table_name: str | None = ...,
        mode_0_system_third_fuel_consumption_lookup_table_name: str | None = ...,
        mode_0_system_water_use_lookup_table_name: str | None = ...,
        mode_0_outdoor_air_fraction: float | None = 0,
        mode_0_supply_air_mass_flow_rate_ratio: float | None = 0,
        modes: list[_g.ZoneHVACHybridUnitaryHVACModesItem] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:HybridUnitaryHVAC`` and add it to the document.

        Hybrid Unitary HVAC. A black box model for multi-mode packaged forced air equipment. Independent variables include outdoor air conditions and indoor air conditions. Controlled inputs include operating mode, supply air flow rate, and outdoor air faction. Empirical lookup tables are required to map supply air temperature supply air humidity, electricity use, fuel uses, water use, fan electricity use, and external static pressure as a function of each independent variable and each controlled input. In each timestep the model will choose one or more combinations of settings for mode, supply air flow rate, outdoor air faction, and part runtime fraction so as to satisfy zone requests for sensible cooling, heating, ventilation, and/or dehumidification with the least resource consumption. Equipment in this class may consume electricity, water, and up to two additional fuel types.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvachybridunitaryhvac
        """

class ZoneHVACBaseboardConvectiveWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        u_factor_times_area_value: float | Literal["Autosize"],
        maximum_water_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        heating_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = 1,
        convergence_tolerance: float | None = 0.001,
    ) -> None:
        """Create a new ``ZoneHVAC:Baseboard:Convective:Water`` and add it to the document.

        Hot water baseboard heater, convection-only. Natural convection hydronic heating unit.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvacbaseboardconvectivewater
        """

class AirTerminalSingleDuctConstantVolumeNoReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        design_specification_outdoor_air_object_name: str | None = ...,
        per_person_ventilation_rate_mode: Literal["", "CurrentOccupancy", "DesignOccupancy"]
        | None = "CurrentOccupancy",
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:ConstantVolume:NoReheat`` and add it to the document.

        Central air system terminal unit, single duct, constant volume, without reheat coil

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminalsingleductconstantvolumenoreheat
        """

class FanZoneExhaust:
    def __call__(
        self,
        name: str,
        /,
        *,
        pressure_rise: float,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        fan_total_efficiency: float | None = 0.6,
        maximum_flow_rate: float | None = ...,
        end_use_subcategory: str | None = "General",
        flow_fraction_schedule_name: str | None = ...,
        system_availability_manager_coupling_mode: Literal["", "Coupled", "Decoupled"] | None = "Coupled",
        minimum_zone_temperature_limit_schedule_name: str | None = ...,
        balanced_exhaust_fraction_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``Fan:ZoneExhaust`` and add it to the document.

        Models a fan that exhausts air from a zone.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-fans/#fanzoneexhaust
        """

class CoilCoolingWaterToAirHeatPumpVariableSpeedEquationFit:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_to_refrigerant_hx_water_inlet_node_name: str,
        water_to_refrigerant_hx_water_outlet_node_name: str,
        indoor_air_inlet_node_name: str,
        indoor_air_outlet_node_name: str,
        energy_part_load_fraction_curve_name: str,
        speed_1_reference_unit_gross_rated_total_cooling_capacity: float,
        speed_1_reference_unit_gross_rated_sensible_heat_ratio: float,
        speed_1_reference_unit_gross_rated_cooling_cop: float,
        speed_1_reference_unit_rated_air_flow_rate: float,
        speed_1_reference_unit_rated_water_flow_rate: float,
        speed_1_total_cooling_capacity_function_of_temperature_curve_name: str,
        speed_1_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str,
        speed_1_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_1_energy_input_ratio_function_of_air_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_water_flow_fraction_curve_name: str,
        speed_1_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float,
        speed_1_waste_heat_function_of_temperature_curve_name: str,
        availability_schedule_name: str | None = ...,
        number_of_speeds: int | None = 2,
        nominal_speed_level: int | None = 2,
        gross_rated_total_cooling_capacity_at_selected_nominal_speed_level: float
        | Literal["", "Autosize"]
        | None = "Autosize",
        rated_air_flow_rate_at_selected_nominal_speed_level: float | Literal["", "Autosize"] | None = "Autosize",
        rated_water_flow_rate_at_selected_nominal_speed_level: float | Literal["", "Autosize"] | None = "Autosize",
        nominal_time_for_condensate_to_begin_leaving_the_coil: float | None = 0,
        initial_moisture_evaporation_rate_divided_by_steady_state_ac_latent_capacity: float | None = 0,
        maximum_cycling_rate: float | None = 0,
        latent_capacity_time_constant: float | None = 0,
        fan_delay_time: float | None = 60,
        flag_for_using_hot_gas_reheat_0_or_1: float | None = 0,
        speed_2_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_2_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_2_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_2_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_2_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_2_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_2_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_2_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_2_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_3_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_3_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_3_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_3_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_3_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_3_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_3_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_3_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_3_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_4_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_4_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_4_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_4_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_4_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_4_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_4_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_4_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_4_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_5_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_5_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_5_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_5_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_5_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_5_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_5_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_5_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_5_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_6_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_6_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_6_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_6_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_6_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_6_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_6_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_6_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_6_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_7_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_7_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_7_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_7_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_7_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_7_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_7_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_7_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_7_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_8_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_8_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_8_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_8_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_8_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_8_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_8_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_8_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_8_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_9_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_9_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_9_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_9_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_9_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_9_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_9_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_9_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_9_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_10_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_10_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_10_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_10_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_10_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_10_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_10_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_10_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_10_waste_heat_function_of_temperature_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit`` and add it to the document.

        Direct expansion (DX) cooling coil for water-to-air heat pump (includes electric compressor), variable-speed, equation-fit model. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Equation-fit model uses normalized curves to describe the heat pump performance. Requires two to ten sets of performance data and will interpolate between speeds. Modeled as a single coil with variable-speed compressor.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwatertoairheatpumpvariablespeedequationfit
        """

class AnyUnitarySystemPerformanceMultispeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        number_of_speeds_for_heating: int,
        number_of_speeds_for_cooling: int,
        single_mode_operation: Literal["", "No", "Yes"] | None = "No",
        no_load_supply_air_flow_rate_ratio: float | None = 1,
        flow_ratios: list[_g.UnitarySystemPerformanceMultispeedFlowRatiosItem] = ...,
    ) -> None:
        """Create a new ``UnitarySystemPerformance:Multispeed`` and add it to the document.

        The UnitarySystemPerformance object is used to specify the air flow ratio at each operating speed. This object is primarily used for multispeed DX and water coils to allow operation at alternate flow rates different from those specified in the coil object.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#unitarysystemperformancemultispeed
        """

class UnitarySystemPerformanceMultispeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        number_of_speeds_for_heating: int,
        number_of_speeds_for_cooling: int,
        single_mode_operation: Literal["", "No", "Yes"] | None = "No",
        no_load_supply_air_flow_rate_ratio: float | None = 1,
        flow_ratios: list[_g.UnitarySystemPerformanceMultispeedFlowRatiosItem] = ...,
    ) -> None:
        """Create a new ``UnitarySystemPerformance:Multispeed`` and add it to the document.

        The UnitarySystemPerformance object is used to specify the air flow ratio at each operating speed. This object is primarily used for multispeed DX and water coils to allow operation at alternate flow rates different from those specified in the coil object.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#unitarysystemperformancemultispeed
        """

class PipeAdiabatic:
    def __call__(self, name: str, /, *, inlet_node_name: str, outlet_node_name: str) -> None:
        """Create a new ``Pipe:Adiabatic`` and add it to the document.

        Passes Inlet Node state variables to Outlet Node state variables

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-node-branch-management/#pipeadiabatic
        """

class PipeIndoor:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        fluid_inlet_node_name: str,
        fluid_outlet_node_name: str,
        environment_type: Literal["", "Schedule", "Zone"] | None = "Zone",
        ambient_temperature_zone_name: str | None = ...,
        ambient_temperature_schedule_name: str | None = ...,
        ambient_air_velocity_schedule_name: str | None = ...,
        pipe_inside_diameter: float | None = ...,
        pipe_length: float | None = ...,
    ) -> None:
        """Create a new ``Pipe:Indoor`` and add it to the document.

        Pipe model with transport delay and heat transfer to the environment.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-node-branch-management/#pipeindoor
        """

class AnyChillerConstantCOP:
    def __call__(
        self,
        name: str,
        /,
        *,
        nominal_capacity: float | Literal["Autosize"],
        nominal_cop: float,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        design_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_condenser_water_flow_rate: float | Literal["Autosize"] | None = ...,
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        chiller_flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"]
        | None = "NotModulated",
        sizing_factor: float | None = 1,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``Chiller:ConstantCOP`` and add it to the document.

        This constant COP chiller model provides a means of quickly specifying a Chiller where performance data is not available.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#chillerconstantcop
        """

class ChillerCombustionTurbine:
    def __call__(
        self,
        name: str,
        /,
        *,
        nominal_capacity: float | Literal["Autosize"],
        nominal_cop: float,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        temperature_rise_coefficient: float,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        design_condenser_inlet_temperature: float | None = ...,
        design_chilled_water_outlet_temperature: float | None = ...,
        design_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_condenser_water_flow_rate: float | Literal["Autosize"] | None = ...,
        coefficient_1_of_capacity_ratio_curve: float | None = ...,
        coefficient_2_of_capacity_ratio_curve: float | None = ...,
        coefficient_3_of_capacity_ratio_curve: float | None = ...,
        coefficient_1_of_power_ratio_curve: float | None = ...,
        coefficient_2_of_power_ratio_curve: float | None = ...,
        coefficient_3_of_power_ratio_curve: float | None = ...,
        coefficient_1_of_full_load_ratio_curve: float | None = ...,
        coefficient_2_of_full_load_ratio_curve: float | None = ...,
        coefficient_3_of_full_load_ratio_curve: float | None = ...,
        chilled_water_outlet_temperature_lower_limit: float | None = ...,
        coefficient_1_of_fuel_input_curve: float | None = ...,
        coefficient_2_of_fuel_input_curve: float | None = ...,
        coefficient_3_of_fuel_input_curve: float | None = ...,
        coefficient_1_of_temperature_based_fuel_input_curve: float | None = ...,
        coefficient_2_of_temperature_based_fuel_input_curve: float | None = ...,
        coefficient_3_of_temperature_based_fuel_input_curve: float | None = ...,
        coefficient_1_of_exhaust_flow_curve: float | None = ...,
        coefficient_2_of_exhaust_flow_curve: float | None = ...,
        coefficient_3_of_exhaust_flow_curve: float | None = ...,
        coefficient_1_of_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_2_of_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_3_of_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_1_of_temperature_based_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_2_of_temperature_based_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_3_of_temperature_based_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_1_of_recovery_lube_heat_curve: float | None = ...,
        coefficient_2_of_recovery_lube_heat_curve: float | None = ...,
        coefficient_3_of_recovery_lube_heat_curve: float | None = ...,
        coefficient_1_of_u_factor_times_area_curve: float | None = ...,
        coefficient_2_of_u_factor_times_area_curve: float | None = ...,
        gas_turbine_engine_capacity: float | Literal["Autosize"] | None = ...,
        maximum_exhaust_flow_per_unit_of_power_output: float | None = ...,
        design_steam_saturation_temperature: float | None = ...,
        fuel_higher_heating_value: float | None = ...,
        design_heat_recovery_water_flow_rate: float | Literal["", "Autosize"] | None = 0,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        chiller_flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"]
        | None = "NotModulated",
        fuel_type: Literal[
            "", "Diesel", "FuelOilNo1", "FuelOilNo2", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2", "Propane"
        ]
        | None = "NaturalGas",
        heat_recovery_maximum_temperature: float | None = 80,
        sizing_factor: float | None = 1,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        condenser_heat_recovery_relative_capacity_fraction: float | None = ...,
        turbine_engine_efficiency: float | None = 0.35,
    ) -> None:
        """Create a new ``Chiller:CombustionTurbine`` and add it to the document.

        This chiller model is the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Chiller performance curves are generated by fitting catalog data to third order polynomial equations. Three sets of coefficients are required.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#chillercombustionturbine
        """

class ThermalStorageIceSimple:
    def __call__(
        self,
        name: str,
        /,
        *,
        ice_storage_type: Literal["IceOnCoilExternal", "IceOnCoilInternal"],
        capacity: float | Literal["Autosize"],
        inlet_node_name: str,
        outlet_node_name: str,
        thermal_storage_sizing_object_name: str | None = ...,
    ) -> None:
        """Create a new ``ThermalStorage:Ice:Simple`` and add it to the document.

        This ice storage model is a simplified model It requires a setpoint placed on the Chilled Water Side Outlet Node It should be placed in the chilled water supply side outlet branch followed by a pipe. Use the PlantEquipmentOperation:ComponentSetpoint plant operation scheme.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-heaters/#thermalstorageicesimple
        """

class ThermalStorageChilledWaterStratified:
    def __call__(
        self,
        name: str,
        /,
        *,
        tank_volume: float,
        tank_height: float,
        ambient_temperature_indicator: Literal["Outdoors", "Schedule", "Zone"],
        tank_shape: Literal["", "HorizontalCylinder", "Other", "VerticalCylinder"] | None = "VerticalCylinder",
        tank_perimeter: float | None = ...,
        setpoint_temperature_schedule_name: str | None = ...,
        deadband_temperature_difference: float | None = 0.0001,
        temperature_sensor_height: float | None = ...,
        minimum_temperature_limit: float | None = ...,
        nominal_cooling_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        ambient_temperature_schedule_name: str | None = ...,
        ambient_temperature_zone_name: str | None = ...,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        uniform_skin_loss_coefficient_per_unit_area_to_ambient_temperature: float | None = ...,
        use_side_inlet_node_name: str | None = ...,
        use_side_outlet_node_name: str | None = ...,
        use_side_heat_transfer_effectiveness: float | None = 1,
        use_side_availability_schedule_name: str | None = ...,
        use_side_inlet_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        use_side_outlet_height: float | None = 0,
        use_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        source_side_inlet_node_name: str | None = ...,
        source_side_outlet_node_name: str | None = ...,
        source_side_heat_transfer_effectiveness: float | None = 1,
        source_side_availability_schedule_name: str | None = ...,
        source_side_inlet_height: float | None = 0,
        source_side_outlet_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        source_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        tank_recovery_time: float | None = 4,
        inlet_mode: Literal["", "Fixed", "Seeking"] | None = "Fixed",
        number_of_nodes: int | None = 1,
        additional_destratification_conductivity: float | None = 0,
        node_1_additional_loss_coefficient: float | None = 0,
        node_2_additional_loss_coefficient: float | None = 0,
        node_3_additional_loss_coefficient: float | None = 0,
        node_4_additional_loss_coefficient: float | None = 0,
        node_5_additional_loss_coefficient: float | None = 0,
        node_6_additional_loss_coefficient: float | None = 0,
        node_7_additional_loss_coefficient: float | None = 0,
        node_8_additional_loss_coefficient: float | None = 0,
        node_9_additional_loss_coefficient: float | None = 0,
        node_10_additional_loss_coefficient: float | None = 0,
    ) -> None:
        """Create a new ``ThermalStorage:ChilledWater:Stratified`` and add it to the document.

        Chilled water storage with a stratified, multi-node tank. The chilled water is 'used' by drawing from the 'Use Side' of the water tank. The tank is indirectly charged by circulating cold water through the 'Source Side' of the water tank.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-heaters/#thermalstoragechilledwaterstratified
        """

class CondenserEquipmentList:
    def __call__(self, name: str, /, *, equipment: list[_g.CondenserEquipmentListEquipmentItem] = ...) -> None:
        """Create a new ``CondenserEquipmentList`` and add it to the document.

        List condenser equipment in order of operating priority, 1st in list will be used 1st, etc Use only condenser equipment in this list. If no equipment object types and equipment names are specified, then the corresponding PlantEquipmentOperation:* object will assume all available condenser equipment for the loop should be OFF (not operate) within the specified lower/upper limit.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#condenserequipmentlist
        """

class ExternalInterfaceFunctionalMockupUnitImportFromVariable:
    def __call__(
        self,
        /,
        *,
        output_variable_index_key_name: str,
        output_variable_name: str,
        fmu_file_name: str,
        fmu_instance_name: str,
        fmu_variable_name: str,
    ) -> None:
        """Create a new ``ExternalInterface:FunctionalMockupUnitImport:From:Variable`` and add it to the document.

        This object declares an FMU input variable

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-externalinterface/#externalinterfacefunctionalmockupunitimportfromvariable
        """

class DemandManagerVentilation:
    def __call__(
        self,
        name: str,
        /,
        *,
        limit_control: Literal["FixedRate", "Off", "ReductionRatio"],
        availability_schedule_name: str | None = ...,
        minimum_limit_duration: int | None = ...,
        fixed_rate: float | None = ...,
        reduction_ratio: float | None = ...,
        limit_step_change: float | None = ...,
        selection_control: Literal["", "All", "RotateMany", "RotateOne"] | None = "All",
        rotation_duration: int | None = ...,
        controllers: list[_g.DemandManagerVentilationControllersItem] = ...,
    ) -> None:
        """Create a new ``DemandManager:Ventilation`` and add it to the document.

        used for demand limiting Controller:OutdoorAir objects.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-demand-limiting-controls/#demandmanagerventilation
        """

class CurveExponent:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_constant: float,
        coefficient2_constant: float,
        coefficient3_constant: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal[
            "", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None:
        """Create a new ``Curve:Exponent`` and add it to the document.

        Exponent curve with one independent variable. Input for a exponent curve consists of the curve name, the 3 coefficients, and the maximum and minimum valid independent variable values. Optional inputs for curve minimum and maximum may be used to limit the output of the performance curve. curve = C1 + C2*x**C3 The independent variable x is raised to the C3 power, multiplied by C2, and C1 is added to the result.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curveexponent
        """

class AnyCurveDoubleExponentialDecay:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        coefficient1_c1: float,
        coefficient2_c2: float,
        coefficient3_c3: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal["", "Dimensionless"] | None = "Dimensionless",
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None:
        """Create a new ``Curve:DoubleExponentialDecay`` and add it to the document.

        Double exponential decay curve with one independent variable. Input consists of the curve name, the five coefficients, and the maximum and minimum valid independent variable values. Optional inputs for the curve minimum and maximum may be used to limit the output of the performance curve. curve = C1+C2*exp(C3*x)+C4*exp(C5*x)

        No call suits every release: narrow the document with ``as_version`` first.
        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curvedoubleexponentialdecay
        """

class AnyOutputJSON:
    def __call__(
        self,
        /,
        *,
        option_type: Literal["TimeSeries", "TimeSeriesAndTabular"],
        output_json: Literal["", "No", "Yes"] | None = "Yes",
        output_cbor: Literal["", "No", "Yes"] | None = "No",
        output_messagepack: Literal["", "No", "Yes"] | None = "No",
    ) -> None:
        """Create a new ``Output:JSON`` and add it to the document.

        Output from EnergyPlus can be written to JSON format files.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#outputjson
        """

class PythonPluginInstance:
    def __call__(
        self,
        name: str,
        /,
        *,
        python_module_name: str,
        plugin_class_name: str,
        run_during_warmup_days: Literal["", "No", "Yes"] | None = "No",
    ) -> None:
        """Create a new ``PythonPlugin:Instance`` and add it to the document.

        A single plugin to be executed during the simulation, which can contain multiple calling points for the same class instance by overriding multiple calling point methods.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-python-plugins/#pythonplugininstance
        """

class AnyPythonPluginTrendVariable:
    def __call__(
        self, name: str, /, *, name_of_a_python_plugin_variable: str, number_of_timesteps_to_be_logged: int
    ) -> None:
        """Create a new ``PythonPlugin:TrendVariable`` and add it to the document.

        This object sets up a Python plugin trend variable from an Python plugin variable A trend variable logs values across timesteps

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-python-plugins/#pythonplugintrendvariable
        """
