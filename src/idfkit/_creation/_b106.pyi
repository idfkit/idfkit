"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

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
    ) -> None:
        """Create a new ``SizingPeriod:DesignDay`` and add it to the document.

        The design day object creates the parameters for the program to create the 24 hour weather profile that can be used for sizing as well as running to test the other simulation parameters. Parameters in this include a date (month and day), a day type (which uses the appropriate schedules for either sizing or simple tests), min/max temperatures, wind speeds, and solar radiation values.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sizingperioddesignday
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#scheduledayhourly
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialcomplexshade
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvacbaseboardconvectivewater
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-heaters/#thermalstoragechilledwaterstratified
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
        controllers: Sequence[
            _g.DemandManagerVentilationControllersItem | _g.DemandManagerVentilationControllersGroup
        ] = ...,
    ) -> None:
        """Create a new ``DemandManager:Ventilation`` and add it to the document.

        used for demand limiting Controller:OutdoorAir objects.

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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curveexponent
        """
