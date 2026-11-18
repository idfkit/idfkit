"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class ComplianceBuilding:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        building_rotation_for_appendix_g: float | None = 0,
        validate: bool = True,
    ) -> None:
        """Create a new ``Compliance:Building`` and add it to the document.

        Building level inputs related to compliance to building standards, building codes, and beyond energy code programs.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-compliance-objects/#compliancebuilding
        """

class AnyScheduleFile:
    def __call__(
        self,
        name: str,
        /,
        *,
        file_name: str,
        column_number: int,
        rows_to_skip_at_top: int,
        schedule_type_limits_name: str | None = ...,
        number_of_hours_of_data: float | None = 8760,
        column_separator: Literal["Comma", "Semicolon", "Tab"] | None = "Comma",
        interpolate_to_timestep: Literal["No", "Yes"] | None = "No",
        minutes_per_item: int | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Schedule:File`` and add it to the document.

        A Schedule:File points to a text computer file that has 8760-8784 hours of data.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#schedulefile
        """

class AirflowNetworkMultiZoneSpecifiedFlowRate:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_flow_value: float,
        air_flow_units: Literal["MassFlow", "VolumetricFlow"] | None = "MassFlow",
        validate: bool = True,
    ) -> None:
        """Create a new ``AirflowNetwork:MultiZone:SpecifiedFlowRate`` and add it to the document.

        This object is used to define specified flow through a linkage.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkmultizonespecifiedflowrate
        """

class SizingZone:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        zone_or_zonelist_name: str,
        zone_cooling_design_supply_air_humidity_ratio: float,
        zone_heating_design_supply_air_humidity_ratio: float,
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_cooling_design_supply_air_temperature: float | None = ...,
        zone_cooling_design_supply_air_temperature_difference: float | None = ...,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = ...,
        zone_heating_design_supply_air_temperature_difference: float | None = ...,
        design_specification_outdoor_air_object_name: str | None = ...,
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        cooling_design_air_flow_method: Literal["DesignDay", "DesignDayWithLimit", "Flow/Zone"] | None = "DesignDay",
        cooling_design_air_flow_rate: float | None = 0,
        cooling_minimum_air_flow_per_zone_floor_area: float | None = 0.000762,
        cooling_minimum_air_flow: float | None = 0,
        cooling_minimum_air_flow_fraction: float | None = 0.2,
        heating_design_air_flow_method: Literal["DesignDay", "DesignDayWithLimit", "Flow/Zone"] | None = "DesignDay",
        heating_design_air_flow_rate: float | None = 0,
        heating_maximum_air_flow_per_zone_floor_area: float | None = 0.002032,
        heating_maximum_air_flow: float | None = 0.1415762,
        heating_maximum_air_flow_fraction: float | None = 0.3,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        account_for_dedicated_outdoor_air_system: Literal["No", "Yes"] | None = "No",
        dedicated_outdoor_air_system_control_strategy: Literal[
            "ColdSupplyAir", "NeutralDehumidifiedSupplyAir", "NeutralSupplyAir"
        ]
        | None = "NeutralSupplyAir",
        dedicated_outdoor_air_low_setpoint_temperature_for_design: float | Literal["Autosize"] | None = "Autosize",
        dedicated_outdoor_air_high_setpoint_temperature_for_design: float | Literal["Autosize"] | None = "Autosize",
        zone_load_sizing_method: Literal[
            "Latent Load", "Sensible And Latent Load", "Sensible Load", "Sensible Load Only No Latent Load"
        ]
        | None = "Sensible Load Only No Latent Load",
        zone_latent_cooling_design_supply_air_humidity_ratio_input_method: Literal[
            "HumidityRatioDifference", "SupplyAirHumidityRatio"
        ]
        | None = "HumidityRatioDifference",
        zone_dehumidification_design_supply_air_humidity_ratio: float | None = ...,
        zone_cooling_design_supply_air_humidity_ratio_difference: float | None = 0.005,
        zone_latent_heating_design_supply_air_humidity_ratio_input_method: Literal[
            "HumidityRatioDifference", "SupplyAirHumidityRatio"
        ]
        | None = "HumidityRatioDifference",
        zone_humidification_design_supply_air_humidity_ratio: float | None = ...,
        zone_humidification_design_supply_air_humidity_ratio_difference: float | None = 0.005,
        zone_humidistat_dehumidification_set_point_schedule_name: str | None = ...,
        zone_humidistat_humidification_set_point_schedule_name: str | None = ...,
        type_of_space_sum_to_use: Literal["Coincident", "NonCoincident"] | None = "Coincident",
        heating_coil_sizing_method: Literal["CoolingCapacity", "GreaterOfHeatingOrCooling", "HeatingCapacity", "None"]
        | None = "None",
        maximum_heating_capacity_to_cooling_load_sizing_ratio: float | None = 1,
        validate: bool = True,
    ) -> None:
        """Create a new ``Sizing:Zone`` and add it to the document.

        Specifies the data needed to perform a zone design air flow calculation. The calculation is done for every sizing period included in the input. The maximum cooling and heating load and cooling, heating, and ventilation air flows are then saved for system level and zone component design calculations.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-design-objects/#sizingzone
        """

class AnyCoilCoolingDXCurveFitSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        gross_total_cooling_capacity_fraction: float,
        evaporator_air_flow_rate_fraction: float,
        condenser_air_flow_rate_fraction: float | None = ...,
        gross_sensible_heat_ratio: float | Literal["Autosize"] | None = "Autosize",
        gross_cooling_cop: float | None = 3,
        active_fraction_of_coil_face_area: float | None = 1,
        evaporative_condenser_pump_power_fraction: float | None = 1,
        evaporative_condenser_effectiveness: float | None = 0.9,
        total_cooling_capacity_modifier_function_of_temperature_curve_name: str | None = ...,
        total_cooling_capacity_modifier_function_of_air_flow_fraction_curve_name: str | None = ...,
        energy_input_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        energy_input_ratio_modifier_function_of_air_flow_fraction_curve_name: str | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
        rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        waste_heat_modifier_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:CurveFit:Speed`` and add it to the document.

        DX cooling coil performance for a single speed within a single operating mode.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-coil-cooling-dx/#coilcoolingdxcurvefitspeed
        """

class CoilCoolingDXCurveFitSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        gross_total_cooling_capacity_fraction: float,
        evaporator_air_flow_rate_fraction: float,
        condenser_air_flow_rate_fraction: float | None = ...,
        gross_sensible_heat_ratio: float | Literal["Autosize"] | None = "Autosize",
        gross_cooling_cop: float | None = 3,
        active_fraction_of_coil_face_area: float | None = 1,
        evaporative_condenser_pump_power_fraction: float | None = 1,
        evaporative_condenser_effectiveness: float | None = 0.9,
        total_cooling_capacity_modifier_function_of_temperature_curve_name: str | None = ...,
        total_cooling_capacity_modifier_function_of_air_flow_fraction_curve_name: str | None = ...,
        energy_input_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        energy_input_ratio_modifier_function_of_air_flow_fraction_curve_name: str | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
        rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        waste_heat_modifier_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:CurveFit:Speed`` and add it to the document.

        DX cooling coil performance for a single speed within a single operating mode.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-coil-cooling-dx/#coilcoolingdxcurvefitspeed
        """

class OutdoorAirMixer:
    def __call__(
        self,
        name: str,
        /,
        *,
        mixed_air_node_name: str,
        outdoor_air_stream_node_name: str,
        relief_air_stream_node_name: str,
        return_air_stream_node_name: str,
        validate: bool = True,
    ) -> None:
        """Create a new ``OutdoorAir:Mixer`` and add it to the document.

        Outdoor air mixer. Node names cannot be duplicated within a single OutdoorAir:Mixer object or across all outdoor air mixers.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution/#outdoorairmixer
        """

class PlantEquipmentList:
    def __call__(
        self,
        name: str,
        /,
        *,
        equipment: Sequence[_g.PlantEquipmentListEquipmentItem | _g.PlantEquipmentListEquipmentGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``PlantEquipmentList`` and add it to the document.

        List plant equipment in order of operating priority, 1st in list will be used 1st, etc Use only plant equipment in this list. If no equipment object types and equipment names are specified, then the corresponding PlantEquipmentOperation:* object will assume all available plant equipment for the loop should be OFF (not operate) within the specified lower/upper limit.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentlist
        """

class ExternalInterfaceFunctionalMockupUnitExportToActuator:
    def __call__(
        self,
        name: str,
        /,
        *,
        actuated_component_unique_name: str,
        actuated_component_type: str,
        actuated_component_control_type: str,
        fmu_variable_name: str,
        initial_value: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ExternalInterface:FunctionalMockupUnitExport:To:Actuator`` and add it to the document.

        Hardware portion of EMS used to set up actuators in the model that are dynamically updated from the FMU.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-externalinterface/#externalinterfacefunctionalmockupunitexporttoactuator
        """

class AnyAirTerminalSingleDuctUserDefined:
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
        validate: bool = True,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:UserDefined`` and add it to the document.

        Defines a generic single duct air terminal unit for custom modeling using Energy Management System or External Interface

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-user-defined-hvac-and-plant-component/#airterminalsingleductuserdefined
        """

class SetpointManagerSingleZoneHeating:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_zone_name: str,
        zone_node_name: str,
        zone_inlet_node_name: str,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["Temperature"] | None = "Temperature",
        minimum_supply_air_temperature: float | None = -99,
        maximum_supply_air_temperature: float | None = 99,
        validate: bool = True,
    ) -> None:
        """Create a new ``SetpointManager:SingleZone:Heating`` and add it to the document.

        This setpoint manager detects the control zone load to meet the current heating setpoint, zone inlet node flow rate, and zone node temperature, and calculates a setpoint temperature for the supply air that will satisfy the zone heating load for the control zone.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagersinglezoneheating
        """

class SetpointManagerFollowSystemNodeTemperature:
    def __call__(
        self,
        name: str,
        /,
        *,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["MaximumTemperature", "MinimumTemperature", "Temperature"] | None = "Temperature",
        reference_node_name: str | None = ...,
        reference_temperature_type: Literal["NodeDryBulb", "NodeWetBulb"] | None = "NodeDryBulb",
        offset_temperature_difference: float | None = ...,
        maximum_limit_setpoint_temperature: float | None = ...,
        minimum_limit_setpoint_temperature: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``SetpointManager:FollowSystemNodeTemperature`` and add it to the document.

        This setpoint manager is used to place a temperature setpoint on a system node that is derived from the current temperatures at a separate system node. The current value of the temperature at a reference node is obtained and used to generate setpoint on a second system node. If the reference node is also designated to be an outdoor air (intake) node, then this setpoint manager can be used to follow outdoor air conditions that are adjusted for altitude.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagerfollowsystemnodetemperature
        """

class CurveLinear:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_constant: float,
        coefficient2_x: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal[
            "Dimensionless", "Distance", "MassFlow", "Power", "Pressure", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        output_unit_type: Literal["Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
        validate: bool = True,
    ) -> None:
        """Create a new ``Curve:Linear`` and add it to the document.

        Linear curve with one independent variable. Input for the linear curve consists of a curve name, the two coefficients, and the maximum and minimum valid independent variable values. Optional inputs for curve minimum and maximum may be used to limit the output of the performance curve. curve = C1 + C2*x

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curvelinear
        """
