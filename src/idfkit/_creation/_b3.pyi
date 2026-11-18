"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class SiteHeightVariation:
    def __call__(
        self,
        /,
        *,
        wind_speed_profile_exponent: float | None = 0.22,
        wind_speed_profile_boundary_layer_thickness: float | None = 370,
        air_temperature_gradient_coefficient: float | None = 0.0065,
    ) -> None:
        """Create a new ``Site:HeightVariation`` and add it to the document.

        This object is used if the user requires advanced control over height-dependent variations in wind speed and temperature. When this object is not present, the default model for temperature dependence on height is used, and the wind speed is modeled according to the Terrain field of the BUILDING object.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#siteheightvariation
        """

class ConstructionAirBoundary:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_exchange_method: Literal["", "None", "SimpleMixing"] | None = "None",
        simple_mixing_air_changes_per_hour: float | None = 0.5,
        simple_mixing_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``Construction:AirBoundary`` and add it to the document.

        Indicates an open boundary between two zones. It may be used for base surfaces and fenestration surfaces. The two adjacent zones are grouped together for solar, daylighting and radiant exchange. When this construction type is used, the Outside Boundary Condition of the surface (or the base surface of a fenestration surface) must be either Surface or Zone. A base surface with Construction:AirBoundary cannot hold any fenestration surfaces.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#constructionairboundary
        """

class ZonePropertyLocalEnvironment:
    def __call__(self, name: str, /, *, zone_name: str | None = ..., outdoor_air_node_name: str | None = ...) -> None:
        """Create a new ``ZoneProperty:LocalEnvironment`` and add it to the document.

        This object defines the local environment properties of a zone object. A corresponding outdoor air node should be defined and linked to the zone object.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#zonepropertylocalenvironment
        """

class AnyRoomAirTemperaturePatternNondimensionalHeight:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_integer_for_pattern_control_schedule_name: int,
        thermostat_offset: float | None = ...,
        return_air_offset: float | None = ...,
        exhaust_air_offset: float | None = ...,
        pairs: Sequence[
            _g.RoomAirTemperaturePatternNondimensionalHeightPairsItem
            | _g.RoomAirTemperaturePatternNondimensionalHeightPairsGroup
        ] = ...,
    ) -> None:
        """Create a new ``RoomAir:TemperaturePattern:NondimensionalHeight`` and add it to the document.

        Defines a distribution pattern for air temperatures relative to the current mean air temperature as a function of height. The height, referred to as Zeta, is nondimensional by normalizing with the zone ceiling height. Used in combination with RoomAir:TemperaturePattern:UserDefined.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairtemperaturepatternnondimensionalheight
        """

class ZoneContaminantSourceAndSinkCarbonDioxide:
    def __call__(
        self, name: str, /, *, zone_name: str, schedule_name: str, design_generation_rate: float | None = ...
    ) -> None:
        """Create a new ``ZoneContaminantSourceAndSink:CarbonDioxide`` and add it to the document.

        Represents internal CO2 gains and sinks in the zone.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#zonecontaminantsourceandsinkcarbondioxide
        """

class AirflowNetworkOccupantVentilationControl:
    def __call__(
        self,
        name: str,
        /,
        *,
        minimum_opening_time: float | None = 0,
        minimum_closing_time: float | None = 0,
        thermal_comfort_low_temperature_curve_name: str | None = ...,
        thermal_comfort_temperature_boundary_point: float | None = 10,
        thermal_comfort_high_temperature_curve_name: str | None = ...,
        maximum_threshold_for_persons_dissatisfied_ppd: float | None = 10,
        occupancy_check: Literal["", "No", "Yes"] | None = "No",
        opening_probability_schedule_name: str | None = ...,
        closing_probability_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``AirflowNetwork:OccupantVentilationControl`` and add it to the document.

        This object is used to provide advanced thermal comfort control of window opening and closing for both exterior and interior windows.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkoccupantventilationcontrol
        """

class CoilSystemCoolingWaterHeatExchangerAssisted:
    def __call__(
        self,
        name: str,
        /,
        *,
        heat_exchanger_object_type: Literal[
            "HeatExchanger:AirToAir:FlatPlate", "HeatExchanger:AirToAir:SensibleAndLatent"
        ],
        heat_exchanger_name: str,
        cooling_coil_object_type: Literal["Coil:Cooling:Water", "Coil:Cooling:Water:DetailedGeometry"],
        cooling_coil_name: str,
    ) -> None:
        """Create a new ``CoilSystem:Cooling:Water:HeatExchangerAssisted`` and add it to the document.

        Virtual component consisting of a chilled-water cooling coil and an air-to-air heat exchanger. The air-to-air heat exchanger precools the air entering the cooling coil and reuses this energy to reheat the supply air leaving the cooling coil. This heat exchange process improves the latent removal performance of the cooling coil (lower sensible heat ratio).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilsystemcoolingwaterheatexchangerassisted
        """

class ConnectorSplitter:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_branch_name: str,
        branches: Sequence[_g.ConnectorSplitterBranchesItem | _g.ConnectorSplitterBranchesGroup] = ...,
    ) -> None:
        """Create a new ``Connector:Splitter`` and add it to the document.

        Split one air/water stream into N outlet streams. Branch names cannot be duplicated within a single Splitter list.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-node-branch-management/#connectorsplitter
        """

class AnyBoilerSteam:
    def __call__(
        self,
        name: str,
        /,
        *,
        fuel_type: Literal["Coal", "Diesel", "Electricity", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2"],
        maximum_operating_pressure: float | None = 160000,
        theoretical_efficiency: float | None = 0.8,
        design_outlet_steam_temperature: float | None = 100,
        nominal_capacity: float | Literal["Autosize"] | None = ...,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        coefficient_1_of_fuel_use_function_of_part_load_ratio_curve: float | None = ...,
        coefficient_2_of_fuel_use_function_of_part_load_ratio_curve: float | None = ...,
        coefficient_3_of_fuel_use_function_of_part_load_ratio_curve: float | None = ...,
        water_inlet_node_name: str | None = ...,
        steam_outlet_node_name: str | None = ...,
        sizing_factor: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``Boiler:Steam`` and add it to the document.

        This boiler model is an adaptation of the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Boiler performance curves are generated by fitting catalog data to third order polynomial equations. A constant efficiency boiler is modeled by setting the fuel use coefficients as follows: N9=1, N10=0, N11=0

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#boilersteam
        """

class AnyCentralHeatPumpSystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        cooling_loop_inlet_node_name: str,
        cooling_loop_outlet_node_name: str,
        source_loop_inlet_node_name: str,
        source_loop_outlet_node_name: str,
        heating_loop_inlet_node_name: str,
        heating_loop_outlet_node_name: str,
        chiller_heater_modules_performance_component_object_type_1: Literal["ChillerHeaterPerformance:Electric:EIR"],
        chiller_heater_modules_performance_component_name_1: str,
        chiller_heater_modules_control_schedule_name_1: str,
        ancillary_power: float | None = 0,
        ancillary_operation_schedule_name: str | None = ...,
        number_of_chiller_heater_modules_1: int | None = 1,
        chiller_heater_modules_performance_component_object_type_2: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_2: str | None = ...,
        chiller_heater_modules_control_schedule_name_2: str | None = ...,
        number_of_chiller_heater_modules_2: int | None = 1,
        chiller_heater_performance_component_object_type_3: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_performance_component_name_3: str | None = ...,
        chiller_heater_modules_control_schedule_name_3: str | None = ...,
        number_of_chiller_heater_modules_3: int | None = 1,
        chiller_heater_modules_performance_component_object_type_4: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_4: str | None = ...,
        chiller_heater_modules_control_schedule_name_4: str | None = ...,
        number_of_chiller_heater_modules_4: int | None = 1,
        chiller_heater_modules_performance_component_object_type_5: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_models_performance_component_name_5: str | None = ...,
        chiller_heater_modules_control_schedule_name_5: str | None = ...,
        number_of_chiller_heater_modules_5: int | None = 1,
        chiller_heater_modules_performance_component_object_type_6: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_6: str | None = ...,
        chiller_heater_modules_control_schedule_name_6: str | None = ...,
        number_of_chiller_heater_modules_6: int | None = 1,
        chiller_heater_modules_performance_component_object_type_7: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_7: str | None = ...,
        chiller_heater_modules_control_schedule_name_7: str | None = ...,
        number_of_chiller_heater_modules_7: int | None = 1,
        chiller_heater_modules_performance_component_object_type_8: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_8: str | None = ...,
        chiller_heater_modules_control_schedule_name_8: str | None = ...,
        number_of_chiller_heater_modules_8: int | None = 1,
        chiller_heater_modules_performance_component_object_type_9: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_9: str | None = ...,
        chiller_heater_modules_control_schedule_name_9: str | None = ...,
        number_of_chiller_heater_modules_9: int | None = 1,
        chiller_heater_modules_performance_component_object_type_10: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_10: str | None = ...,
        chiller_heater_modules_control_schedule_name_10: str | None = ...,
        number_of_chiller_heater_modules_10: int | None = 1,
        chiller_heater_modules_performance_component_object_type_11: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_11: str | None = ...,
        chiller_heater_module_control_schedule_name_11: str | None = ...,
        number_of_chiller_heater_modules_11: int | None = 1,
        chiller_heater_modules_performance_component_object_type_12: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_12: str | None = ...,
        chiller_heater_modules_control_schedule_name_12: str | None = ...,
        number_of_chiller_heater_modules_12: int | None = 1,
        chiller_heater_modules_performance_component_object_type_13: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_13: str | None = ...,
        chiller_heater_modules_control_schedule_name_13: str | None = ...,
        number_of_chiller_heater_modules_13: int | None = 1,
        chiller_heater_modules_performance_component_object_type_14: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_14: str | None = ...,
        chiller_heater_modules_control_schedule_name_14: str | None = ...,
        number_of_chiller_heater_modules_14: int | None = 1,
        chiller_heater_modules_performance_component_object_type_15: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_15: str | None = ...,
        chiller_heater_modules_control_schedule_name_15: str | None = ...,
        number_of_chiller_heater_modules_15: int | None = 1,
        chiller_heater_modules_performance_component_object_type_16: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_16: str | None = ...,
        chiller_heater_modules_control_schedule_name_16: str | None = ...,
        number_of_chiller_heater_modules_16: int | None = 1,
        chiller_heater_modules_performance_component_object_type_17: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_17: str | None = ...,
        chiller_heater_modules_control_schedule_name_17: str | None = ...,
        number_of_chiller_heater_modules_17: int | None = 1,
        chiller_heater_modules_performance_component_object_type_18: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_18: str | None = ...,
        chiller_heater_modules_control_control_schedule_name_18: str | None = ...,
        number_of_chiller_heater_modules_18: int | None = 1,
        chiller_heater_modules_performance_component_object_type_19: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_19: str | None = ...,
        chiller_heater_modules_control_schedule_name_19: str | None = ...,
        number_of_chiller_heater_modules_19: int | None = 1,
        chiller_heater_modules_performance_component_object_type_20: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_20: str | None = ...,
        chiller_heater_modules_control_schedule_name_20: str | None = ...,
        number_of_chiller_heater_modules_20: int | None = 1,
    ) -> None:
        """Create a new ``CentralHeatPumpSystem`` and add it to the document.

        This chiller bank can contain multiple chiller heaters and heat pump performance objects. Its function is to encapsulate the extra controls needed to turn individual modules on/off and whether they are to operate in cooling-only, heating-only or simultaneous cooling/heating mode and whether to connect the source water to the evaporator or condenser side.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#centralheatpumpsystem
        """

class EnergyManagementSystemOutputVariable:
    def __call__(
        self,
        name: str,
        /,
        *,
        ems_variable_name: str,
        type_of_data_in_variable: Literal["Averaged", "Summed"],
        update_frequency: Literal["SystemTimestep", "ZoneTimestep"],
        ems_program_or_subroutine_name: str | None = ...,
        units: str | None = ...,
    ) -> None:
        """Create a new ``EnergyManagementSystem:OutputVariable`` and add it to the document.

        This object sets up an EnergyPlus output variable from an Erl variable

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemoutputvariable
        """

class CurveQuintLinear:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_constant: float,
        coefficient2_v: float,
        coefficient3_w: float,
        coefficient4_x: float,
        coefficient5_y: float,
        coefficient6_z: float,
        minimum_value_of_v: float,
        maximum_value_of_v: float,
        minimum_value_of_w: float,
        maximum_value_of_w: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_value_of_y: float,
        maximum_value_of_y: float,
        minimum_value_of_z: float,
        maximum_value_of_z: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_v: Literal[
            "",
            "Dimensionless",
            "Distance",
            "MassFlow",
            "Power",
            "Temperature",
            "VolumetricFlow",
            "VolumetricFlowPerPower",
        ]
        | None = "Dimensionless",
        input_unit_type_for_w: Literal[
            "",
            "Dimensionless",
            "Distance",
            "MassFlow",
            "Power",
            "Temperature",
            "VolumetricFlow",
            "VolumetricFlowPerPower",
        ]
        | None = "Dimensionless",
        input_unit_type_for_x: Literal[
            "",
            "Dimensionless",
            "Distance",
            "MassFlow",
            "Power",
            "Temperature",
            "VolumetricFlow",
            "VolumetricFlowPerPower",
        ]
        | None = "Dimensionless",
        input_unit_type_for_y: Literal[
            "",
            "Dimensionless",
            "Distance",
            "MassFlow",
            "Power",
            "Temperature",
            "VolumetricFlow",
            "VolumetricFlowPerPower",
        ]
        | None = "Dimensionless",
        input_unit_type_for_z: Literal[
            "",
            "Dimensionless",
            "Distance",
            "MassFlow",
            "Power",
            "Temperature",
            "VolumetricFlow",
            "VolumetricFlowPerPower",
        ]
        | None = "Dimensionless",
    ) -> None:
        """Create a new ``Curve:QuintLinear`` and add it to the document.

        Linear curve with five independent variables. Input for the linear curve consists of a curve name, the two coefficients, and the maximum and minimum valid independent variable values. Optional inputs for curve minimum and maximum may be used to limit the output of the performance curve. curve = C1 + C2*v + C3*w + C4*x + C5*y + C6*z

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curvequintlinear
        """
