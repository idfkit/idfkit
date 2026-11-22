"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class WeatherPropertySkyTemperature:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        calculation_type: Literal[
            "BerdahlMartin",
            "Brunt",
            "ClarkAllen",
            "DifferenceScheduleDewPointValue",
            "DifferenceScheduleDryBulbValue",
            "Idso",
            "ScheduleValue",
        ]
        | None = "ClarkAllen",
        schedule_name: str | None = ...,
        use_weather_file_horizontal_ir: Literal["No", "Yes"] | None = "Yes",
        validate: bool = True,
    ) -> None:
        """Create a new ``WeatherProperty:SkyTemperature`` and add it to the document.

        This object is used to override internal sky temperature calculations.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#weatherpropertyskytemperature
        """

class WindowMaterialGas:
    def __call__(
        self,
        name: str,
        /,
        *,
        gas_type: Literal["Air", "Argon", "Custom", "Krypton", "Xenon"],
        thickness: float,
        conductivity_coefficient_a: float | None = ...,
        conductivity_coefficient_b: float | None = ...,
        conductivity_coefficient_c: float | None = ...,
        viscosity_coefficient_a: float | None = ...,
        viscosity_coefficient_b: float | None = ...,
        viscosity_coefficient_c: float | None = ...,
        specific_heat_coefficient_a: float | None = ...,
        specific_heat_coefficient_b: float | None = ...,
        specific_heat_coefficient_c: float | None = ...,
        molecular_weight: float | None = ...,
        specific_heat_ratio: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``WindowMaterial:Gas`` and add it to the document.

        Gas material properties that are used in Windows or Glass Doors

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialgas
        """

class AnyGlobalGeometryRules:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        starting_vertex_position: Literal["LowerLeftCorner", "LowerRightCorner", "UpperLeftCorner", "UpperRightCorner"],
        vertex_entry_direction: Literal["Clockwise", "Counterclockwise"],
        coordinate_system: Literal["Relative", "World"],
        daylighting_reference_point_coordinate_system: Literal["Relative", "World"] | None = "Relative",
        rectangular_surface_coordinate_system: Literal["Relative", "World"] | None = "Relative",
        validate: bool = True,
    ) -> None:
        """Create a new ``GlobalGeometryRules`` and add it to the document.

        Specifies the geometric rules used to describe the input of surface vertices and daylighting reference points.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#globalgeometryrules
        """

class RoofCeilingDetailed:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition: Literal[
            "Adiabatic",
            "Ground",
            "GroundBasementPreprocessorAverageFloor",
            "GroundBasementPreprocessorAverageWall",
            "GroundBasementPreprocessorLowerWall",
            "GroundBasementPreprocessorUpperWall",
            "GroundSlabPreprocessorAverage",
            "GroundSlabPreprocessorCore",
            "GroundSlabPreprocessorPerimeter",
            "OtherSideCoefficients",
            "OtherSideConditionsModel",
            "Outdoors",
            "Space",
            "Surface",
            "Zone",
        ],
        space_name: str | None = ...,
        outside_boundary_condition_object: str | None = ...,
        sun_exposure: Literal["NoSun", "SunExposed"] | None = "SunExposed",
        wind_exposure: Literal["NoWind", "WindExposed"] | None = "WindExposed",
        view_factor_to_ground: float | Literal["Autocalculate"] | None = "Autocalculate",
        number_of_vertices: float | Literal["Autocalculate"] | None = "Autocalculate",
        vertices: Sequence[_g.RoofCeilingDetailedVerticesItem | _g.RoofCeilingDetailedVerticesGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``RoofCeiling:Detailed`` and add it to the document.

        Allows for detailed entry of roof/ceiling heat transfer surfaces.

        ``vertices`` takes the extensible groups in order, one dict per group:

        ```python
        doc["RoofCeiling:Detailed"].add(
            "RoofCeiling Detailed 1",
            construction_name="Construction 1",
            zone_name="Zone 1",
            outside_boundary_condition="Adiabatic",
            vertices=[
                {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#roofceilingdetailed
        """

class RoomAirNodeAirflowNetwork:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        zone_name: str,
        fraction_of_zone_air_volume: float | None = ...,
        roomair_node_airflownetwork_adjacentsurfacelist_name: str | None = ...,
        roomair_node_airflownetwork_internalgains_name: str | None = ...,
        roomair_node_airflownetwork_hvacequipment_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``RoomAir:Node:AirflowNetwork`` and add it to the document.

        define an air node for some types of nodal air models

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairnodeairflownetwork
        """

class AirflowNetworkDistributionDuctSizing:
    def __call__(
        self,
        name: str,
        /,
        *,
        duct_sizing_method: Literal["MaximumVelocity", "PressureLoss", "PressureLossWithMaximumVelocity"]
        | None = "MaximumVelocity",
        duct_sizing_factor: float | None = 1,
        maximum_airflow_velocity: float | None = 5,
        total_pressure_loss_across_supply_trunk: float | None = ...,
        total_pressure_loss_across_supply_branch: float | None = ...,
        total_pressure_loss_across_return_trunk: float | None = ...,
        total_pressure_loss_across_return_branch: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:DuctSizing`` and add it to the document.

        This object defines required parameters for duct sizing in an Airflow Network simulation. To activate duct sizing, see AirflowNetwork:SimulationControl Do Distribution Duct Sizing Calculation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkdistributionductsizing
        """

class SolarCollectorFlatPlatePhotovoltaicThermal:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        surface_name: str,
        photovoltaic_thermal_model_performance_name: str | None = ...,
        photovoltaic_name: str | None = ...,
        thermal_working_fluid_type: Literal["Air", "Water"] | None = ...,
        water_inlet_node_name: str | None = ...,
        water_outlet_node_name: str | None = ...,
        air_inlet_node_name: str | None = ...,
        air_outlet_node_name: str | None = ...,
        design_flow_rate: float | Literal["Autosize"] | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``SolarCollector:FlatPlate:PhotovoltaicThermal`` and add it to the document.

        Models hybrid photovoltaic-thermal (PVT) solar collectors that convert incident solar energy into both electricity and useful thermal energy by heating air or water.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-solar-collectors/#solarcollectorflatplatephotovoltaicthermal
        """

class PlantEquipmentOperationSchemes:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_scheme_1_object_type: Literal[
            "PlantEquipmentOperation:ChillerHeaterChangeover",
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ],
        control_scheme_1_name: str,
        control_scheme_1_schedule_name: str,
        control_scheme_2_object_type: Literal[
            "PlantEquipmentOperation:ChillerHeaterChangeover",
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_2_name: str | None = ...,
        control_scheme_2_schedule_name: str | None = ...,
        control_scheme_3_object_type: Literal[
            "PlantEquipmentOperation:ChillerHeaterChangeover",
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_3_name: str | None = ...,
        control_scheme_3_schedule_name: str | None = ...,
        control_scheme_4_object_type: Literal[
            "PlantEquipmentOperation:ChillerHeaterChangeover",
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_4_name: str | None = ...,
        control_scheme_4_schedule_name: str | None = ...,
        control_scheme_5_object_type: Literal[
            "PlantEquipmentOperation:ChillerHeaterChangeover",
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_5_name: str | None = ...,
        control_scheme_5_schedule_name: str | None = ...,
        control_scheme_6_object_type: Literal[
            "PlantEquipmentOperation:ChillerHeaterChangeover",
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_6_name: str | None = ...,
        control_scheme_6_schedule_name: str | None = ...,
        control_scheme_7_object_type: Literal[
            "PlantEquipmentOperation:ChillerHeaterChangeover",
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_7_name: str | None = ...,
        control_scheme_7_schedule_name: str | None = ...,
        control_scheme_8_object_type: Literal[
            "PlantEquipmentOperation:ChillerHeaterChangeover",
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_8_name: str | None = ...,
        control_scheme_8_schedule_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``PlantEquipmentOperationSchemes`` and add it to the document.

        Operation schemes are listed in 'priority' order. Note that each scheme must address the entire load and/or condition ranges for the simulation. The actual one selected for use will be the first that is 'Scheduled' on. That is, if control scheme 1 is not 'on' and control scheme 2 is -- then control scheme 2 is selected. Only plant equipment should be listed on a Control Scheme for this item.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationschemes
        """

class AnyPlantComponentUserDefined:
    def __call__(
        self,
        name: str,
        /,
        *,
        number_of_plant_loop_connections: int,
        plant_connection_1_inlet_node_name: str,
        plant_connection_1_outlet_node_name: str,
        plant_connection_1_loading_mode: Literal[
            "DemandsLoad",
            "MeetsLoadWithNominalCapacity",
            "MeetsLoadWithNominalCapacityHiOutLimit",
            "MeetsLoadWithNominalCapacityLowOutLimit",
            "MeetsLoadWithPassiveCapacity",
        ],
        plant_connection_1_loop_flow_request_mode: Literal[
            "NeedsFlowAndTurnsLoopOn", "NeedsFlowIfLoopOn", "ReceivesWhateverFlowAvailable"
        ],
        main_model_program_calling_manager_name: str | None = ...,
        plant_connection_1_initialization_program_calling_manager_name: str | None = ...,
        plant_connection_1_simulation_program_calling_manager_name: str | None = ...,
        plant_connection_2_inlet_node_name: str | None = ...,
        plant_connection_2_outlet_node_name: str | None = ...,
        plant_connection_2_loading_mode: Literal[
            "DemandsLoad",
            "MeetLoadWithNominalCapacity",
            "MeetLoadWithNominalCapacityHiOutLimit",
            "MeetLoadWithNominalCapacityLowOutLimit",
            "MeetLoadWithPassiveCapacity",
        ]
        | None = ...,
        plant_connection_2_loop_flow_request_mode: Literal[
            "NeedsFlowAndTurnsLoopOn", "NeedsFlowIfLoopOn", "ReceivesWhateverFlowAvailable"
        ]
        | None = ...,
        plant_connection_2_initialization_program_calling_manager_name: str | None = ...,
        plant_connection_2_simulation_program_calling_manager_name: str | None = ...,
        plant_connection_3_inlet_node_name: str | None = ...,
        plant_connection_3_outlet_node_name: str | None = ...,
        plant_connection_3_loading_mode: Literal[
            "DemandsLoad",
            "MeetLoadWithNominalCapacity",
            "MeetLoadWithNominalCapacityHiOutLimit",
            "MeetLoadWithNominalCapacityLowOutLimit",
            "MeetLoadWithPassiveCapacity",
        ]
        | None = ...,
        plant_connection_3_loop_flow_request_mode: Literal[
            "NeedsFlowAndTurnsLoopOn", "NeedsFlowIfLoopOn", "ReceivesWhateverFlowAvailable"
        ]
        | None = ...,
        plant_connection_3_initialization_program_calling_manager_name: str | None = ...,
        plant_connection_3_simulation_program_calling_manager_name: str | None = ...,
        plant_connection_4_inlet_node_name: str | None = ...,
        plant_connection_4_outlet_node_name: str | None = ...,
        plant_connection_4_loading_mode: Literal[
            "DemandsLoad",
            "MeetLoadWithNominalCapacity",
            "MeetLoadWithNominalCapacityHiOutLimit",
            "MeetLoadWithNominalCapacityLowOutLimit",
            "MeetLoadWithPassiveCapacity",
        ]
        | None = ...,
        plant_connection_4_loop_flow_request_mode: Literal[
            "NeedsFlowAndTurnsLoopOn", "NeedsFlowIfLoopOn", "ReceivesWhateverFlowAvailable"
        ]
        | None = ...,
        plant_connection_4_initialization_program_calling_manager_name: str | None = ...,
        plant_connection_4_simulation_program_calling_manager_name: str | None = ...,
        air_connection_inlet_node_name: str | None = ...,
        air_connection_outlet_node_name: str | None = ...,
        supply_inlet_water_storage_tank_name: str | None = ...,
        collection_outlet_water_storage_tank_name: str | None = ...,
        ambient_zone_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``PlantComponent:UserDefined`` and add it to the document.

        Defines a generic plant component for custom modeling using Energy Management System or External Interface

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-user-defined-hvac-and-plant-component/#plantcomponentuserdefined
        """

class PhotovoltaicPerformanceSimple:
    def __call__(
        self,
        name: str,
        /,
        *,
        fraction_of_surface_area_with_active_solar_cells: float,
        conversion_efficiency_input_mode: Literal["Fixed", "Scheduled"] | None = ...,
        value_for_cell_efficiency_if_fixed: float | None = ...,
        efficiency_schedule_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``PhotovoltaicPerformance:Simple`` and add it to the document.

        Describes a simple model of photovoltaics that may be useful for early phase design analysis. In this model the user has direct access to the efficiency with which surfaces convert incident solar radiation to electricity and need not specify arrays of specific modules.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#photovoltaicperformancesimple
        """
