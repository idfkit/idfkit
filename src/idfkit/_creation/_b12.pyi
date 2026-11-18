"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class SizingPeriodWeatherFileConditionType:
    def __call__(
        self,
        name: str,
        /,
        *,
        period_selection: Literal[
            "AutumnTypical",
            "DrySeason",
            "NoDrySeason",
            "NoDrySeasonMax",
            "NoDrySeasonMin",
            "NoWetSeason",
            "NoWetSeasonMax",
            "NoWetSeasonMin",
            "SpringTypical",
            "SummerExtreme",
            "SummerTypical",
            "TropicalCold",
            "TropicalHot",
            "WetSeason",
            "WinterExtreme",
            "WinterTypical",
        ],
        day_of_week_for_start_day: Literal[
            "",
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
        use_weather_file_daylight_saving_period: Literal["", "No", "Yes"] | None = "Yes",
        use_weather_file_rain_and_snow_indicators: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``SizingPeriod:WeatherFileConditionType`` and add it to the document.

        Use a weather file period for design sizing calculations. EPW weather files are created with typical and extreme periods created heuristically from the weather file data. For more details on these periods, see AuxiliaryPrograms document.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sizingperiodweatherfileconditiontype
        """

class AnyMaterialPropertyHeatAndMoistureTransferSuction:
    def __call__(
        self,
        /,
        *,
        material_name: str,
        number_of_suction_points: int,
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
        """Create a new ``MaterialProperty:HeatAndMoistureTransfer:Suction`` and add it to the document.

        HeatBalanceAlgorithm = CombinedHeatAndMoistureFiniteElement solution algorithm only. Relationship between liquid suction transport coefficient and moisture content Has no effect with other HeatBalanceAlgorithm solution algorithms

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertyheatandmoisturetransfersuction
        """

class GroundHeatTransferControl:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        run_basement_preprocessor: Literal["", "No", "Yes"] | None = "No",
        run_slab_preprocessor: Literal["", "No", "Yes"] | None = "No",
    ) -> None:
        """Create a new ``GroundHeatTransfer:Control`` and add it to the document.

        Object determines if the Slab and Basement preprocessors are going to be executed.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransfercontrol
        """

class ZoneCoolTowerShower:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_space_name: str,
        pump_flow_rate_schedule_name: str,
        maximum_water_flow_rate: float,
        effective_tower_height: float,
        airflow_outlet_area: float,
        maximum_air_flow_rate: float,
        minimum_indoor_temperature: float,
        rated_power_consumption: float,
        availability_schedule_name: str | None = ...,
        water_supply_storage_tank_name: str | None = ...,
        flow_control_type: Literal["", "WaterFlowSchedule", "WindDrivenFlow"] | None = "WindDrivenFlow",
        fraction_of_water_loss: float | None = ...,
        fraction_of_flow_schedule: float | None = ...,
    ) -> None:
        """Create a new ``ZoneCoolTower:Shower`` and add it to the document.

        A cooltower (sometimes referred to as a wind tower or a shower cooling tower) models passive downdraught evaporative cooling (PDEC) that is designed to capture the wind at the top of a tower and cool the outdoor air using water evaporation before delivering it to a zone (or space).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zonecooltowershower
        """

class ZoneControlThermostatTemperatureAndHumidity:
    def __call__(
        self,
        /,
        *,
        thermostat_name: str,
        dehumidifying_relative_humidity_setpoint_schedule_name: str,
        dehumidification_control_type: Literal["", "None", "Overcool"] | None = "Overcool",
        overcool_range_input_method: Literal["", "Constant", "Scheduled"] | None = "Constant",
        overcool_constant_range: float | None = 1.7,
        overcool_range_schedule_name: str | None = ...,
        overcool_control_ratio: float | None = 3.6,
    ) -> None:
        """Create a new ``ZoneControl:Thermostat:TemperatureAndHumidity`` and add it to the document.

        This object modifies a ZoneControl:Thermostat object to effect temperature control based on zone air humidity conditions.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-controls-thermostats/#zonecontrolthermostattemperatureandhumidity
        """

class AirLoopHVACExhaustSystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_mixer_name: str,
        fan_object_type: Literal["Fan:ComponentModel", "Fan:SystemModel"],
        fan_name: str,
    ) -> None:
        """Create a new ``AirLoopHVAC:ExhaustSystem`` and add it to the document.

        Defines a general exhaust system with a central exhaust fan drawing from one or more ZoneHVAC:ExhaustControl outlet nodes via an AirLoopHVAC:ZoneMixer.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-path/#airloophvacexhaustsystem
        """

class Duct:
    def __call__(self, name: str, /, *, inlet_node_name: str, outlet_node_name: str) -> None:
        """Create a new ``Duct`` and add it to the document.

        Passes inlet node state variables to outlet node state variables

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-node-branch-management/#duct
        """

class AnyEnergyManagementSystemTrendVariable:
    def __call__(self, name: str, /, *, ems_variable_name: str, number_of_timesteps_to_be_logged: int) -> None:
        """Create a new ``EnergyManagementSystem:TrendVariable`` and add it to the document.

        This object sets up an EMS trend variable from an Erl variable A trend variable logs values across timesteps

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemtrendvariable
        """

class CurveTriquadratic:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_constant: float | None = ...,
        coefficient2_x_2: float | None = ...,
        coefficient3_x: float | None = ...,
        coefficient4_y_2: float | None = ...,
        coefficient5_y: float | None = ...,
        coefficient6_z_2: float | None = ...,
        coefficient7_z: float | None = ...,
        coefficient8_x_2_y_2: float | None = ...,
        coefficient9_x_y: float | None = ...,
        coefficient10_x_y_2: float | None = ...,
        coefficient11_x_2_y: float | None = ...,
        coefficient12_x_2_z_2: float | None = ...,
        coefficient13_x_z: float | None = ...,
        coefficient14_x_z_2: float | None = ...,
        coefficient15_x_2_z: float | None = ...,
        coefficient16_y_2_z_2: float | None = ...,
        coefficient17_y_z: float | None = ...,
        coefficient18_y_z_2: float | None = ...,
        coefficient19_y_2_z: float | None = ...,
        coefficient20_x_2_y_2_z_2: float | None = ...,
        coefficient21_x_2_y_2_z: float | None = ...,
        coefficient22_x_2_y_z_2: float | None = ...,
        coefficient23_x_y_2_z_2: float | None = ...,
        coefficient24_x_2_y_z: float | None = ...,
        coefficient25_x_y_2_z: float | None = ...,
        coefficient26_x_y_z_2: float | None = ...,
        coefficient27_x_y_z: float | None = ...,
        minimum_value_of_x: float | None = ...,
        maximum_value_of_x: float | None = ...,
        minimum_value_of_y: float | None = ...,
        maximum_value_of_y: float | None = ...,
        minimum_value_of_z: float | None = ...,
        maximum_value_of_z: float | None = ...,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal[
            "", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        input_unit_type_for_y: Literal[
            "", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        input_unit_type_for_z: Literal[
            "", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None:
        """Create a new ``Curve:Triquadratic`` and add it to the document.

        Quadratic curve with three independent variables. Input consists of the curve name, the twenty seven coefficients, and min and max values for each of the independent variables. Optional inputs for curve minimum and maximum may be used to limit the output of the performance curve. curve = a0 + a1*x**2 + a2*x + a3*y**2 + a4*y + a5*z**2 + a6*z + a7*x**2*y**2 + a8*x*y + a9*x*y**2 + a10*x**2*y + a11*x**2*z**2 + a12*x*z + a13*x*z**2 + a14*x**2*z + a15*y**2*z**2 + a16*y*z + a17*y*z**2 + a18*y**2*z + a19*x**2*y**2*z**2 + a20*x**2*y**2*z + a21*x**2*y*z**2 + a22*x*y**2*z**2 + a23*x**2*y*z + a24*x*y**2*z + a25*x*y*z**2 +a26*x*y*z

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curvetriquadratic
        """
