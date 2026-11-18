"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class MaterialAirGap:
    def __call__(self, name: str, /, *, thermal_resistance: float) -> None:
        """Create a new ``Material:AirGap`` and add it to the document.

        Air Space in Opaque Construction

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialairgap
        """

class WindowMaterialGapEquivalentLayer:
    def __call__(
        self,
        name: str,
        /,
        *,
        gas_type: Literal["AIR", "ARGON", "CUSTOM", "KRYPTON", "XENON"],
        thickness: float,
        gap_vent_type: Literal["Sealed", "VentedIndoor", "VentedOutdoor"],
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
    ) -> None:
        """Create a new ``WindowMaterial:Gap:EquivalentLayer`` and add it to the document.

        Gas material properties that are used in Windows Equivalent Layer References only WindowMaterial:Gas properties

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialgapequivalentlayer
        """

class WindowPropertyStormWindow:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        window_name: str,
        storm_glass_layer_name: str,
        month_that_storm_glass_layer_is_put_on: int,
        day_of_month_that_storm_glass_layer_is_put_on: int,
        month_that_storm_glass_layer_is_taken_off: int,
        day_of_month_that_storm_glass_layer_is_taken_off: int,
        distance_between_storm_glass_layer_and_adjacent_glass: float | None = 0.05,
    ) -> None:
        """Create a new ``WindowProperty:StormWindow`` and add it to the document.

        This is a movable exterior glass layer that is usually applied in the winter and removed in the summer.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#windowpropertystormwindow
        """

class AnyDesignSpecificationOutdoorAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        outdoor_air_method: Literal[
            "AirChanges/Hour",
            "Flow/Area",
            "Flow/Person",
            "Flow/Zone",
            "IndoorAirQualityProcedure",
            "Maximum",
            "ProportionalControlBasedOnDesignOccupancy",
            "Sum",
        ]
        | None = "Flow/Person",
        outdoor_air_flow_per_person: float | None = 0.00944,
        outdoor_air_flow_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_per_zone: float | None = 0,
        outdoor_air_flow_air_changes_per_hour: float | None = 0,
        outdoor_air_schedule_name: str | None = ...,
        proportional_control_minimum_outdoor_air_flow_rate_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``DesignSpecification:OutdoorAir`` and add it to the document.

        This object is used to describe general outdoor air requirements which are referenced by other objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-design-objects/#designspecificationoutdoorair
        """

class ThermostatSetpointSingleHeating:
    def __call__(self, name: str, /, *, setpoint_temperature_schedule_name: str | None = ...) -> None:
        """Create a new ``ThermostatSetpoint:SingleHeating`` and add it to the document.

        Used for a heating only thermostat. The setpoint can be scheduled and varied throughout the simulation but only heating is allowed with this control type.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-controls-thermostats/#thermostatsetpointsingleheating
        """

class AnyControllerMechanicalVentilation:
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
            "ZoneSum",
        ]
        | None = ...,
        zone_maximum_outdoor_air_fraction: float | None = 1,
        zone_specifications: Sequence[
            _g.AnyControllerMechanicalVentilationZoneSpecificationsItem
            | _g.AnyControllerMechanicalVentilationZoneSpecificationsGroup
        ] = ...,
    ) -> None:
        """Create a new ``Controller:MechanicalVentilation`` and add it to the document.

        This object is used in conjunction with Controller:OutdoorAir to specify outdoor ventilation air based on outdoor air specified in the DesignSpecification:OutdoorAir object The Controller:OutdoorAir object is associated with a specific air loop, so the outdoor air flow rates specified in Controller:MechanicalVentilation correspond to the zones attached to that specific air loop. Duplicate groups of Zone name, Design Specification Outdoor Air Object Name, and Design Specification Zone Air Distribution Object Name to increase allowable number of entries

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-controllers/#controllermechanicalventilation
        """

class PumpConstantSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        design_flow_rate: float | Literal["Autosize"] | None = ...,
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        pump_control_type: Literal["Continuous", "Intermittent"] | None = "Continuous",
        pump_flow_rate_schedule_name: str | None = ...,
        pump_curve_name: str | None = ...,
        impeller_diameter: float | None = ...,
        rotational_speed: float | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``Pump:ConstantSpeed`` and add it to the document.

        This pump model is described in the ASHRAE secondary HVAC toolkit.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-pumps/#pumpconstantspeed
        """

class AnyChillerElectricReformulatedEIR:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_capacity: float | Literal["Autosize"],
        reference_cop: float,
        cooling_capacity_function_of_temperature_curve_name: str,
        electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str,
        electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        condenser_inlet_node_name: str,
        condenser_outlet_node_name: str,
        reference_leaving_chilled_water_temperature: float | None = 6.67,
        reference_leaving_condenser_water_temperature: float | None = 35,
        reference_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        reference_condenser_water_flow_rate: float | Literal["Autosize"] | None = ...,
        electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_type: Literal[
            "LeavingCondenserWaterTemperature", "Lift"
        ]
        | None = "LeavingCondenserWaterTemperature",
        minimum_part_load_ratio: float | None = 0.1,
        maximum_part_load_ratio: float | None = 1,
        optimum_part_load_ratio: float | None = 1,
        minimum_unloading_ratio: float | None = 0.2,
        fraction_of_compressor_electric_consumption_rejected_by_condenser: float | None = 1,
        leaving_chilled_water_lower_temperature_limit: float | None = 2,
        chiller_flow_mode_type: Literal["ConstantFlow", "LeavingSetpointModulated", "NotModulated"]
        | None = "NotModulated",
        design_heat_recovery_water_flow_rate: float | Literal["Autosize"] | None = 0,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        sizing_factor: float | None = 1,
        condenser_heat_recovery_relative_capacity_fraction: float | None = ...,
        heat_recovery_inlet_high_temperature_limit_schedule_name: str | None = ...,
        heat_recovery_leaving_temperature_setpoint_node_name: str | None = ...,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``Chiller:Electric:ReformulatedEIR`` and add it to the document.

        This chiller model is an empirical model, a reformulated version of Chiller:Electric:EIR where the performance is a function of condenser leaving fluid Temperature instead of condenser entering fluid Temperature. Chiller performance at off-reference conditions is modeled using three polynomial equations. Three curve objects are required.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#chillerelectricreformulatedeir
        """

class PlantEquipmentOperationUserDefined:
    def __call__(
        self,
        name: str,
        /,
        *,
        main_model_program_calling_manager_name: str,
        initialization_program_calling_manager_name: str | None = ...,
        equipment_1_object_type: str | None = ...,
        equipment_1_name: str | None = ...,
        equipment_2_object_type: str | None = ...,
        equipment_2_name: str | None = ...,
        equipment_3_object_type: str | None = ...,
        equipment_3_name: str | None = ...,
        equipment_4_object_type: str | None = ...,
        equipment_4_name: str | None = ...,
        equipment_5_object_type: str | None = ...,
        equipment_5_name: str | None = ...,
        equipment_6_object_type: str | None = ...,
        equipment_6_name: str | None = ...,
        equipment_7_object_type: str | None = ...,
        equipment_7_name: str | None = ...,
        equipment_8_object_type: str | None = ...,
        equipment_8_name: str | None = ...,
        equipment_9_object_type: str | None = ...,
        equipment_9_name: str | None = ...,
        equipment_10_object_type: str | None = ...,
        equipment_10_name: str | None = ...,
    ) -> None:
        """Create a new ``PlantEquipmentOperation:UserDefined`` and add it to the document.

        Defines a generic plant operation scheme for custom supervisory control using Energy Management System or External Interface to dispatch loads

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-user-defined-hvac-and-plant-component/#plantequipmentoperationuserdefined
        """

class OutputControlReportingTolerances:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        tolerance_for_time_heating_setpoint_not_met: float | None = 0.2,
        tolerance_for_time_cooling_setpoint_not_met: float | None = 0.2,
    ) -> None:
        """Create a new ``OutputControl:ReportingTolerances`` and add it to the document.

        Calculations of the time that setpoints are not met use a tolerance of 0.2C. This object allows changing the tolerance used to determine when setpoints are being met.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#outputcontrolreportingtolerances
        """

class OutputMeterCumulativeMeterFileOnly:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        key_name: str,
        reporting_frequency: Literal[
            "Annual", "Daily", "Detailed", "Environment", "Hourly", "Monthly", "RunPeriod", "Timestep"
        ]
        | None = "Hourly",
    ) -> None:
        """Create a new ``Output:Meter:Cumulative:MeterFileOnly`` and add it to the document.

        Each Output:Meter:Cumulative:MeterFileOnly command picks meters to be reported cumulatively onto the standard output file (.eso) and meter file (.mtr). Not all meters are reported in every simulation. a list of meters that can be reported are available after a run on the meter dictionary file (.mdd) if the Output:VariableDictionary has been requested.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-output-reporting/#outputmetercumulativemeterfileonly
        """
