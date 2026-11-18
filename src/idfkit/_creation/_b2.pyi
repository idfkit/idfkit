"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class Building:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        north_axis: float | None = 0,
        terrain: Literal["", "City", "Country", "Ocean", "Suburbs", "Urban"] | None = "Suburbs",
        loads_convergence_tolerance_value: float | None = 0.04,
        temperature_convergence_tolerance_value: float | None = 0.4,
        solar_distribution: Literal[
            "",
            "FullExterior",
            "FullExteriorWithReflections",
            "FullInteriorAndExterior",
            "FullInteriorAndExteriorWithReflections",
            "MinimalShadowing",
        ]
        | None = "FullExterior",
        maximum_number_of_warmup_days: int | None = 25,
        minimum_number_of_warmup_days: int | None = 1,
        construction_assignment_set_name: str | None = ...,
    ) -> None:
        """Create a new ``Building`` and add it to the document.

        Describes parameters that are used during the simulation of the building. There are necessary correlations between the entries for this object and some entries in the Site:WeatherStation and Site:HeightVariation objects, specifically the Terrain field.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#building
        """

class AnyZone:
    def __call__(
        self,
        name: str,
        /,
        *,
        direction_of_relative_north: float | None = 0,
        x_origin: float | None = 0,
        y_origin: float | None = 0,
        z_origin: float | None = 0,
        type: int | None = 1,
        multiplier: int | None = 1,
        ceiling_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        volume: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        floor_area: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        zone_inside_convection_algorithm: Literal[
            "", "AdaptiveConvectionAlgorithm", "CeilingDiffuser", "Simple", "TARP", "TrombeWall"
        ]
        | None = ...,
        zone_outside_convection_algorithm: Literal[
            "", "AdaptiveConvectionAlgorithm", "DOE-2", "MoWiTT", "SimpleCombined", "TARP"
        ]
        | None = ...,
        part_of_total_floor_area: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``Zone`` and add it to the document.

        Defines a thermal zone of the building. Every zone contains one or more Spaces. Space is an optional input. If a Zone has no Space(s) specified in input then a default Space named <Zone Name> will be created. If some surfaces in a Zone are assigned to a space and some are not, then a default Space named <Zone Name>-Remainder will be created. Input references to Space Names must have a matching Space object (default space names may not be referenced except in output variable keys).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#zone
        """

class AirflowNetworkZoneControlPressureController:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_zone_name: str,
        control_object_type: Literal[
            "AirflowNetwork:Distribution:Component:ReliefAirFlow", "AirflowNetwork:MultiZone:Component:ZoneExhaustFan"
        ],
        control_object_name: str,
        pressure_setpoint_schedule_name: str,
        pressure_control_availability_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``AirflowNetwork:ZoneControl:PressureController`` and add it to the document.

        This object is used to control a zone to a specified indoor pressure using the AirflowNetwork model. The specified pressure setpoint is used to control the zone exhaust fan flow rate in a controlled zone or the relief air flow rate in an air loop.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkzonecontrolpressurecontroller
        """

class AnyZoneHVACHybridUnitaryHVAC:
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
        scaling_factor: float | None = 1,
        minimum_time_between_mode_change: float | None = 10,
        first_fuel_type: Literal[
            "",
            "Coal",
            "Diesel",
            "DistrictCooling",
            "Electricity",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
        ]
        | None = "Electricity",
        second_fuel_type: Literal[
            "",
            "Coal",
            "Diesel",
            "DistrictCooling",
            "Electricity",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
        ]
        | None = "None",
        third_fuel_type: Literal[
            "",
            "Coal",
            "Diesel",
            "DistrictCooling",
            "Electricity",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
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
        modes: Sequence[_g.ZoneHVACHybridUnitaryHVACModesItem | _g.ZoneHVACHybridUnitaryHVACModesGroup] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:HybridUnitaryHVAC`` and add it to the document.

        Hybrid Unitary HVAC. A black box model for multi-mode packaged forced air equipment. Independent variables include outdoor air conditions and indoor air conditions. Controlled inputs include operating mode, supply air flow rate, and outdoor air faction. Empirical lookup tables are required to map supply air temperature supply air humidity, electricity use, fuel uses, water use, fan electricity use, and external static pressure as a function of each independent variable and each controlled input. In each timestep the model will choose one or more combinations of settings for mode, supply air flow rate, outdoor air faction, and part runtime fraction so as to satisfy zone requests for sensible cooling, heating, ventilation, and/or dehumidification with the least resource consumption. Equipment in this class may consume electricity, water, and up to two additional fuel types.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvachybridunitaryhvac
        """

class GroundHeatExchangerVerticalSingle:
    def __call__(
        self, name: str, /, *, ghe_vertical_properties_object_name: str, x_location: float, y_location: float
    ) -> None:
        """Create a new ``GroundHeatExchanger:Vertical:Single`` and add it to the document.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#groundheatexchangerverticalsingle
        """

class PlantEquipmentOperationOutdoorDewpoint:
    def __call__(
        self,
        name: str,
        /,
        *,
        dewpoint_temperature_range_1_lower_limit: float,
        dewpoint_temperature_range_1_upper_limit: float,
        range_1_equipment_list_name: str,
        dewpoint_temperature_range_2_lower_limit: float | None = ...,
        dewpoint_temperature_range_2_upper_limit: float | None = ...,
        range_2_equipment_list_name: str | None = ...,
        dewpoint_temperature_range_3_lower_limit: float | None = ...,
        dewpoint_temperature_range_3_upper_limit: float | None = ...,
        range_3_equipment_list_name: str | None = ...,
        dewpoint_temperature_range_4_lower_limit: float | None = ...,
        dewpoint_temperature_range_4_upper_limit: float | None = ...,
        range_4_equipment_list_name: str | None = ...,
        dewpoint_temperature_range_5_lower_limit: float | None = ...,
        dewpoint_temperature_range_5_upper_limit: float | None = ...,
        range_5_equipment_list_name: str | None = ...,
        dewpoint_temperature_range_6_lower_limit: float | None = ...,
        dewpoint_temperature_range_6_upper_limit: float | None = ...,
        range_6_equipment_list_name: str | None = ...,
        dewpoint_temperature_range_7_lower_limit: float | None = ...,
        dewpoint_temperature_range_7_upper_limit: float | None = ...,
        range_7_equipment_list_name: str | None = ...,
        dewpoint_temperature_range_8_lower_limit: float | None = ...,
        dewpoint_temperature_range_8_upper_limit: float | None = ...,
        range_8_equipment_list_name: str | None = ...,
        dewpoint_temperature_range_9_lower_limit: float | None = ...,
        dewpoint_temperature_range_9_upper_limit: float | None = ...,
        range_9_equipment_list_name: str | None = ...,
        dewpoint_temperature_range_10_lower_limit: float | None = ...,
        dewpoint_temperature_range_10_upper_limit: float | None = ...,
        range_10_equipment_list_name: str | None = ...,
    ) -> None:
        """Create a new ``PlantEquipmentOperation:OutdoorDewpoint`` and add it to the document.

        Plant equipment operation scheme for outdoor dewpoint temperature range operation. Specifies one or more groups of equipment which are available to operate for successive outdoor dewpoint temperature ranges.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationoutdoordewpoint
        """

class OutputTableAnnual:
    def __call__(
        self,
        name: str,
        /,
        *,
        filter: str | None = ...,
        schedule_name: str | None = ...,
        variable_details: Sequence[
            _g.OutputTableAnnualVariableDetailsItem | _g.OutputTableAnnualVariableDetailsGroup
        ] = ...,
    ) -> None:
        """Create a new ``Output:Table:Annual`` and add it to the document.

        Provides a generic method of setting up tables of annual results with one row per object. The report has multiple columns that are each defined using a repeated group of fields for any number of columns. A single Output:Table:Annual produces a single table in the output.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/standard-output-reports/output-table-annual/#outputtableannual
        """

class PythonPluginTrendVariable:
    def __call__(
        self, name: str, /, *, name_of_a_python_plugin_variable: str, number_of_timesteps_to_be_logged: int
    ) -> None:
        """Create a new ``PythonPlugin:TrendVariable`` and add it to the document.

        This object sets up a Python plugin trend variable from an Python plugin variable A trend variable logs values across timesteps

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-python-plugins/#pythonplugintrendvariable
        """
