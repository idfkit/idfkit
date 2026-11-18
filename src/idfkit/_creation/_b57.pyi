"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class Zone:
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
        ceiling_height: float | Literal["Autocalculate"] | None = "Autocalculate",
        volume: float | Literal["Autocalculate"] | None = "Autocalculate",
        floor_area: float | Literal["Autocalculate"] | None = "Autocalculate",
        zone_inside_convection_algorithm: Literal[
            "ASTMC1340", "AdaptiveConvectionAlgorithm", "CeilingDiffuser", "Simple", "TARP", "TrombeWall"
        ]
        | None = ...,
        zone_outside_convection_algorithm: Literal[
            "AdaptiveConvectionAlgorithm", "DOE-2", "MoWiTT", "SimpleCombined", "TARP"
        ]
        | None = ...,
        part_of_total_floor_area: Literal["No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``Zone`` and add it to the document.

        Defines a thermal zone of the building. Every zone contains one or more Spaces. Space is an optional input. If a Zone has no Space(s) specified in input then a default Space named <Zone Name> will be created. If some surfaces in a Zone are assigned to a space and some are not, then a default Space named <Zone Name>-Remainder will be created. Input references to Space Names must have a matching Space object (default space names may not be referenced except in output variable keys).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#zone
        """

class ZoneEarthtubeParameters:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        earth_tube_model_parameters_name: str,
        nodes_above_earth_tube: int | None = 5,
        nodes_below_earth_tube: int | None = 3,
        earth_tube_dimensionless_boundary_above: float | None = 1,
        earth_tube_dimensionless_boundary_below: float | None = 0.25,
        earth_tube_solution_space_width: float | None = 4,
    ) -> None:
        """Create a new ``ZoneEarthtube:Parameters`` and add it to the document.

        Parameters that apply to the vertical model for an earth tube

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zoneearthtubeparameters
        """

class DesignSpecificationZoneAirDistribution:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_air_distribution_effectiveness_in_cooling_mode: float | None = 1,
        zone_air_distribution_effectiveness_in_heating_mode: float | None = 1,
        zone_air_distribution_effectiveness_schedule_name: str | None = ...,
        zone_secondary_recirculation_fraction: float | None = 0,
        minimum_zone_ventilation_efficiency: float | None = 0,
    ) -> None:
        """Create a new ``DesignSpecification:ZoneAirDistribution`` and add it to the document.

        This object is used to describe zone air distribution in terms of air distribution effectiveness and secondary recirculation fraction. It is referenced by Sizing:Zone and Controller:MechanicalVentilation objects

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-design-objects/#designspecificationzoneairdistribution
        """

class WaterHeaterHeatPumpPumpedCondenser:
    def __call__(
        self,
        name: str,
        /,
        *,
        compressor_setpoint_temperature_schedule_name: str,
        condenser_water_inlet_node_name: str,
        condenser_water_outlet_node_name: str,
        inlet_air_configuration: Literal["OutdoorAirOnly", "Schedule", "ZoneAirOnly", "ZoneAndOutdoorAir"],
        tank_name: str,
        dx_coil_name: str,
        compressor_location: Literal["Outdoors", "Schedule", "Zone"],
        fan_name: str,
        availability_schedule_name: str | None = ...,
        dead_band_temperature_difference: float | None = 5,
        condenser_water_flow_rate: float | Literal["Autocalculate"] | None = ...,
        evaporator_air_flow_rate: float | Literal["Autocalculate"] | None = ...,
        air_inlet_node_name: str | None = ...,
        air_outlet_node_name: str | None = ...,
        outdoor_air_node_name: str | None = ...,
        exhaust_air_node_name: str | None = ...,
        inlet_air_temperature_schedule_name: str | None = ...,
        inlet_air_humidity_schedule_name: str | None = ...,
        inlet_air_zone_name: str | None = ...,
        tank_object_type: Literal["WaterHeater:Mixed", "WaterHeater:Stratified"] | None = "WaterHeater:Mixed",
        tank_use_side_inlet_node_name: str | None = ...,
        tank_use_side_outlet_node_name: str | None = ...,
        dx_coil_object_type: Literal[
            "Coil:WaterHeating:AirToWaterHeatPump:Pumped",
            "Coil:WaterHeating:AirToWaterHeatPump:VariableSpeed",
            "CoilSystem:IntegratedHeatPump:AirSource",
        ]
        | None = ...,
        minimum_inlet_air_temperature_for_compressor_operation: float | None = 10,
        maximum_inlet_air_temperature_for_compressor_operation: float | None = 48.88888888889,
        compressor_ambient_temperature_schedule_name: str | None = ...,
        fan_object_type: Literal["Fan:OnOff", "Fan:SystemModel"] | None = "Fan:OnOff",
        fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "DrawThrough",
        on_cycle_parasitic_electric_load: float | None = 0,
        off_cycle_parasitic_electric_load: float | None = 0,
        parasitic_heat_rejection_location: Literal["Outdoors", "Zone"] | None = "Outdoors",
        inlet_air_mixer_node_name: str | None = ...,
        outlet_air_splitter_node_name: str | None = ...,
        inlet_air_mixer_schedule_name: str | None = ...,
        tank_element_control_logic: Literal["MutuallyExclusive", "Simultaneous"] | None = "Simultaneous",
        control_sensor_1_height_in_stratified_tank: float | None = ...,
        control_sensor_1_weight: float | None = 1,
        control_sensor_2_height_in_stratified_tank: float | None = ...,
    ) -> None:
        """Create a new ``WaterHeater:HeatPump:PumpedCondenser`` and add it to the document.

        This object models an air-source heat pump for water heating where the water is pumped out of the tank, through a heating coil and returned to the tank. For wrapped condenser HPWHs, see WaterHeater:HeatPump:WrappedCondenser. WaterHeater:HeatPump:PumpedCondenser is a compound object that references other component objects - Coil:WaterHeating:AirToWaterHeatPump:*, Fan:OnOff, WaterHeater:Mixed or WaterHeater:Stratified

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-heaters/#waterheaterheatpumppumpedcondenser
        """

class AirTerminalSingleDuctUserDefined:
    def __call__(
        self,
        name: str,
        /,
        *,
        primary_air_inlet_node_name: str,
        primary_air_outlet_node_name: str,
        number_of_plant_loop_connections: int,
        plant_connection_1_inlet_node_name: str,
        plant_connection_1_outlet_node_name: str,
        overall_model_simulation_program_calling_manager_name: str | None = ...,
        model_setup_and_sizing_program_calling_manager_name: str | None = ...,
        secondary_air_inlet_node_name: str | None = ...,
        secondary_air_outlet_node_name: str | None = ...,
        plant_connection_2_inlet_node_name: str | None = ...,
        plant_connection_2_outlet_node_name: str | None = ...,
        supply_inlet_water_storage_tank_name: str | None = ...,
        collection_outlet_water_storage_tank_name: str | None = ...,
        ambient_zone_name: str | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:UserDefined`` and add it to the document.

        Defines a generic single duct air terminal unit for custom modeling using Energy Management System or External Interface

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-user-defined-hvac-and-plant-component/#airterminalsingleductuserdefined
        """

class CurveChillerPartLoadWithLift:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_c1: float,
        coefficient2_c2: float,
        coefficient3_c3: float,
        coefficient4_c4: float,
        coefficient5_c5: float,
        coefficient6_c6: float,
        coefficient7_c7: float,
        coefficient8_c8: float,
        coefficient9_c9: float,
        coefficient10_c10: float,
        coefficient11_c11: float,
        coefficient12_c12: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_value_of_y: float,
        maximum_value_of_y: float,
        minimum_value_of_z: float,
        maximum_value_of_z: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal["Dimensionless"] | None = "Dimensionless",
        input_unit_type_for_y: Literal["Dimensionless"] | None = "Dimensionless",
        input_unit_type_for_z: Literal["Dimensionless"] | None = "Dimensionless",
        output_unit_type: Literal["Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None:
        """Create a new ``Curve:ChillerPartLoadWithLift`` and add it to the document.

        This chiller part-load performance curve has three independent variables. Input consists of the curve name, the twelve coefficients, and the maximum and minimum valid independent variable values. Optional inputs for the curve minimum and maximum may be used to limit the output of the performance curve. curve = C1 + C2*x + C3*x**2 + C4*y + C5*y**2 + C6*x*y + C7*x**3 + C8*y**3 + C9*x**2*y + C10*x*y**2 + C11*x**2*y**2 + C12*z*y**3 x = dT* = normalized fractional Lift = dT / dTref y = PLR = part load ratio (cooling load/steady state capacity) z = Tdev* = normalized Tdev = Tdev / dTref Where: dT = Lift = Leaving Condenser Water Temperature - Leaving Chilled Water Temperature dTref = dT at the reference condition Tdev = Leaving Chilled Water Temperature - Reference Chilled Water Temperature

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curvechillerpartloadwithlift
        """

class OutputDiagnostics:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        diagnostics: Sequence[_g.OutputDiagnosticsDiagnosticsItem | _g.OutputDiagnosticsDiagnosticsGroup] = ...,
    ) -> None:
        """Create a new ``Output:Diagnostics`` and add it to the document.

        Special keys to produce certain warning messages or effect certain simulation characteristics.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#outputdiagnostics
        """
