"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class Material_v8_9_to_v26_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        roughness: Literal["MediumRough", "MediumSmooth", "Rough", "Smooth", "VeryRough", "VerySmooth"],
        thickness: float,
        conductivity: float,
        density: float,
        specific_heat: float,
        thermal_absorptance: float | None = 0.9,
        solar_absorptance: float | None = 0.7,
        visible_absorptance: float | None = 0.7,
    ) -> None:
        """Create a new ``Material`` and add it to the document.

        Regular materials described with full set of thermal properties

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.1/io-reference/overview/group-surface-construction-elements/#material
        """

class OutputIlluminanceMap_v22_2_to_v24_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        z_height: float | None = 0,
        x_minimum_coordinate: float | None = 0,
        x_maximum_coordinate: float | None = 1,
        number_of_x_grid_points: int | None = 2,
        y_minimum_coordinate: float | None = 0,
        y_maximum_coordinate: float | None = 1,
        number_of_y_grid_points: int | None = 2,
    ) -> None:
        """Create a new ``Output:IlluminanceMap`` and add it to the document.

        reference points are given in coordinates specified in the GlobalGeometryRules object Daylighting Reference Point CoordinateSystem field

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.1/io-reference/overview/group-daylighting/#outputilluminancemap
        """

class EnergyManagementSystemMeteredOutputVariable_v9_3_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        ems_variable_name: str,
        update_frequency: Literal["SystemTimestep", "ZoneTimestep"],
        resource_type: Literal[
            "Coal",
            "CondensateWaterCollected",
            "Diesel",
            "DistrictCooling",
            "DistrictHeating",
            "Electricity",
            "ElectricityProducedOnSite",
            "EnergyTransfer",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "MainsWaterSupply",
            "NaturalGas",
            "OnSiteWaterProduced",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "RainWaterCollected",
            "SolarAirHeating",
            "SolarWaterHeating",
            "Steam",
            "WaterUse",
            "WellWaterDrawn",
        ],
        group_type: Literal["Building", "HVAC", "Plant", "System"],
        end_use_category: Literal[
            "Baseboard",
            "Boilers",
            "Chillers",
            "Cooling",
            "CoolingCoils",
            "ExteriorEquipment",
            "ExteriorLights",
            "Fans",
            "HeatRecovery",
            "HeatRecoveryForCooling",
            "HeatRecoveryForHeating",
            "HeatRejection",
            "Heating",
            "HeatingCoils",
            "Humidifier",
            "InteriorEquipment",
            "InteriorLights",
            "OnSiteGeneration",
            "Pumps",
            "Refrigeration",
            "WaterSystems",
        ],
        ems_program_or_subroutine_name: str | None = ...,
        end_use_subcategory: str | None = ...,
        units: str | None = ...,
    ) -> None:
        """Create a new ``EnergyManagementSystem:MeteredOutputVariable`` and add it to the document.

        This object sets up an EnergyPlus output variable from an Erl variable

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemmeteredoutputvariable
        """

class HeatExchangerFluidToFluid_v8_9_to_v25_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        loop_demand_side_inlet_node_name: str,
        loop_demand_side_outlet_node_name: str,
        loop_demand_side_design_flow_rate: float | Literal["Autosize"],
        loop_supply_side_inlet_node_name: str,
        loop_supply_side_outlet_node_name: str,
        loop_supply_side_design_flow_rate: float | Literal["Autosize"],
        heat_exchanger_u_factor_times_area_value: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        heat_exchange_model_type: Literal[
            "CounterFlow",
            "CrossFlowBothMixed",
            "CrossFlowBothUnMixed",
            "CrossFlowSupplyMixedDemandUnMixed",
            "CrossFlowSupplyUnMixedDemandMixed",
            "Ideal",
            "ParallelFlow",
        ]
        | None = "Ideal",
        control_type: Literal[
            "CoolingDifferentialOnOff",
            "CoolingSetpointModulated",
            "CoolingSetpointOnOff",
            "CoolingSetpointOnOffWithComponentOverride",
            "DualDeadbandSetpointModulated",
            "DualDeadbandSetpointOnOff",
            "HeatingSetpointModulated",
            "HeatingSetpointOnOff",
            "OperationSchemeModulated",
            "OperationSchemeOnOff",
            "UncontrolledOn",
        ]
        | None = "UncontrolledOn",
        heat_exchanger_setpoint_node_name: str | None = ...,
        minimum_temperature_difference_to_activate_heat_exchanger: float | None = 0.01,
        heat_transfer_metering_end_use_type: Literal[
            "FreeCooling",
            "HeatRecovery",
            "HeatRecoveryForCooling",
            "HeatRecoveryForHeating",
            "HeatRejection",
            "LoopToLoop",
        ]
        | None = "LoopToLoop",
        component_override_loop_supply_side_inlet_node_name: str | None = ...,
        component_override_loop_demand_side_inlet_node_name: str | None = ...,
        component_override_cooling_control_temperature_mode: Literal["DryBulbTemperature", "Loop", "WetBulbTemperature"]
        | None = "Loop",
        sizing_factor: float | None = 1,
        operation_minimum_temperature_limit: float | None = ...,
        operation_maximum_temperature_limit: float | None = ...,
    ) -> None:
        """Create a new ``HeatExchanger:FluidToFluid`` and add it to the document.

        A fluid/fluid heat exchanger designed to couple the supply side of one loop to the demand side of another loop Loops can be either plant or condenser loops but no air side connections are allowed

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.2/io-reference/overview/group-condenser-equipment/#heatexchangerfluidtofluid
        """

class AirLoopHVACDedicatedOutdoorAirSystem_v9_2_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        airloophvac_mixer_name: str,
        airloophvac_splitter_name: str,
        preheat_design_temperature: float,
        preheat_design_humidity_ratio: float,
        precool_design_temperature: float,
        precool_design_humidity_ratio: float,
        number_of_airloophvac: float,
        airloophvac_outdoorairsystem_name: str | None = ...,
        availability_schedule_name: str | None = ...,
        airloophvacs: Sequence[
            _g.AirLoopHVACDedicatedOutdoorAirSystemAirloophvacsItem
            | _g.AirLoopHVACDedicatedOutdoorAirSystemAirloophvacsGroup
        ] = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:DedicatedOutdoorAirSystem`` and add it to the document.

        Defines a central forced air system to provide dedicated outdoor air to multiple AirLoopHVACs.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-air-path/#airloophvacdedicatedoutdoorairsystem
        """
