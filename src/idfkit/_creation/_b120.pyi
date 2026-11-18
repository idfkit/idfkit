"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class ZoneCapacitanceMultiplierResearchSpecial:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_name: str | None = ...,
        temperature_capacity_multiplier: float | None = 1,
        humidity_capacity_multiplier: float | None = 1,
        carbon_dioxide_capacity_multiplier: float | None = 1,
        generic_contaminant_capacity_multiplier: float | None = 1,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneCapacitanceMultiplier:ResearchSpecial`` and add it to the document.

        Multiplier altering the relative capacitance of the air compared to an empty zone

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#zonecapacitancemultiplierresearchspecial
        """

class ZoneHVACLowTemperatureRadiantSurfaceGroup:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_fractions: Sequence[
            _g.ZoneHVACLowTemperatureRadiantSurfaceGroupSurfaceFractionsItem
            | _g.ZoneHVACLowTemperatureRadiantSurfaceGroupSurfaceFractionsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneHVAC:LowTemperatureRadiant:SurfaceGroup`` and add it to the document.

        This is used to allow the coordinate control of several radiant system surfaces. Note that the following flow fractions must sum up to 1.0 The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvaclowtemperatureradiantsurfacegroup
        """

class PlantEquipmentOperationThermalEnergyStorage:
    def __call__(
        self,
        name: str,
        /,
        *,
        on_peak_schedule: str,
        charging_availability_schedule: str,
        non_charging_chilled_water_temperature: float,
        charging_chilled_water_temperature: float,
        component_1_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ],
        component_1_name: str,
        component_1_demand_calculation_node_name: str,
        component_1_setpoint_node_name: str,
        component_1_flow_rate: float | Literal["Autosize"],
        component_1_operation_type: Literal["Cooling", "Dual", "Heating"],
        component_2_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_2_name: str | None = ...,
        component_2_demand_calculation_node_name: str | None = ...,
        component_2_setpoint_node_name: str | None = ...,
        component_2_flow_rate: float | Literal["Autosize"] | None = ...,
        component_2_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_3_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_3_name: str | None = ...,
        component_3_demand_calculation_node_name: str | None = ...,
        component_3_setpoint_node_name: str | None = ...,
        component_3_flow_rate: float | Literal["Autosize"] | None = ...,
        component_3_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_4_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:ASHRAE205",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_4_name: str | None = ...,
        component_4_demand_calculation_node_name: str | None = ...,
        component_4_setpoint_node_name: str | None = ...,
        component_4_flow_rate: float | Literal["Autosize"] | None = ...,
        component_4_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_5_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:ASHRAE205",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_5_name: str | None = ...,
        component_5_demand_calculation_node_name: str | None = ...,
        component_5_setpoint_node_name: str | None = ...,
        component_5_flow_rate: float | Literal["Autosize"] | None = ...,
        component_5_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_6_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:ASHRAE205",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_6_name: str | None = ...,
        component_6_demand_calculation_node_name: str | None = ...,
        component_6_setpoint_node_name: str | None = ...,
        component_6_flow_rate: float | Literal["Autosize"] | None = ...,
        component_6_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_7_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:ASHRAE205",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_7_name: str | None = ...,
        component_7_demand_calculation_node_name: str | None = ...,
        component_7_setpoint_node_name: str | None = ...,
        component_7_flow_rate: float | Literal["Autosize"] | None = ...,
        component_7_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_8_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:ASHRAE205",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_8_name: str | None = ...,
        component_8_demand_calculation_node_name: str | None = ...,
        component_8_setpoint_node_name: str | None = ...,
        component_8_flow_rate: float | Literal["Autosize"] | None = ...,
        component_8_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_9_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:ASHRAE205",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_9_name: str | None = ...,
        component_9_demand_calculation_node_name: str | None = ...,
        component_9_setpoint_node_name: str | None = ...,
        component_9_flow_rate: float | Literal["Autosize"] | None = ...,
        component_9_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_10_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:ASHRAE205",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_10_name: str | None = ...,
        component_10_demand_calculation_node_name: str | None = ...,
        component_10_setpoint_node_name: str | None = ...,
        component_10_flow_rate: float | Literal["Autosize"] | None = ...,
        component_10_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``PlantEquipmentOperation:ThermalEnergyStorage`` and add it to the document.

        Plant equipment operation scheme for simpler input to control thermal (ice) energy storage systems. It replaces a host of setpoint managers with simple, single input values. For more complex controls, use the ComponentSetpoint scheme.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationthermalenergystorage
        """

class AvailabilityManagerScheduledOn:
    def __call__(self, name: str, /, *, schedule_name: str, validate: bool = True) -> None:
        """Create a new ``AvailabilityManager:ScheduledOn`` and add it to the document.

        Determines the availability of a loop or system: only controls the turn on action. Schedule overrides fan/pump schedule.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-system-availability-managers/#availabilitymanagerscheduledon
        """

class SetpointManagerSingleZoneOneStageHeating:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_zone_name: str,
        setpoint_node_or_nodelist_name: str,
        heating_stage_on_supply_air_setpoint_temperature: float | None = 99,
        heating_stage_off_supply_air_setpoint_temperature: float | None = -99,
        validate: bool = True,
    ) -> None:
        """Create a new ``SetpointManager:SingleZone:OneStageHeating`` and add it to the document.

        This object can be used with CoilSystem:Heating:DX, Coil:Heating:Fuel, Coil:Heating:Electric to model on/off cycling control of single stage air systems. Setpoints are modulated to run coil full on or full off depending on zone conditions. Intended for use with ZoneControl:Thermostat:StagedDualSetpoint.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagersinglezoneonestageheating
        """

class GeneratorFuelCellInverter:
    def __call__(
        self,
        name: str,
        /,
        *,
        inverter_efficiency_calculation_mode: Literal["Constant", "Quadratic"] | None = ...,
        inverter_efficiency: float | None = ...,
        efficiency_function_of_dc_power_curve_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Generator:FuelCell:Inverter`` and add it to the document.

        Used to describe the power condition unit subsystem of a fuel cell power generator. This object models an inverter system contained within a fuel cell system that converts from direct current (DC) to alternating current (AC).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatorfuelcellinverter
        """
