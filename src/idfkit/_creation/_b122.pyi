"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class Timestep:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        number_of_timesteps_per_hour: int | None = 6,
    ) -> None:
        """Create a new ``Timestep`` and add it to the document.

        Specifies the 'basic' timestep for the simulation. The value entered here is also known as the Zone Timestep. This is used in the Zone Heat Balance Model calculation as the driving timestep for heat transfer and load calculations.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#timestep
        """

class AirLoopHVAC:
    def __call__(
        self,
        name: str,
        /,
        *,
        branch_list_name: str,
        supply_side_inlet_node_name: str,
        demand_side_inlet_node_names: str,
        supply_side_outlet_node_names: str,
        controller_list_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        design_supply_air_flow_rate: float | Literal["Autosize"] | None = 0,
        connector_list_name: str | None = ...,
        demand_side_outlet_node_name: str | None = ...,
        design_return_air_flow_fraction_of_supply_air_flow: float | None = 1,
    ) -> None:
        """Create a new ``AirLoopHVAC`` and add it to the document.

        Defines a central forced air system.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution/#airloophvac
        """

class PlantComponentTemperatureSource:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node: str,
        outlet_node: str,
        design_volume_flow_rate: float | Literal["Autosize"],
        temperature_specification_type: Literal["Constant", "Scheduled"] | None = ...,
        source_temperature: float | None = ...,
        source_temperature_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``PlantComponent:TemperatureSource`` and add it to the document.

        Simulates an object of pre-determined (constant or scheduled) source temperature The object introduces fluid into the plant loop at the specified temperature and at the same flow rate as the fluid enters the component Fluid entering the component vanishes equivalent to the relief air in an air system

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#plantcomponenttemperaturesource
        """

class DemandManagerExteriorLights:
    def __call__(
        self,
        name: str,
        /,
        *,
        limit_control: Literal["Fixed", "Off"],
        selection_control: Literal["All", "RotateMany", "RotateOne"],
        availability_schedule_name: str | None = ...,
        minimum_limit_duration: int | None = ...,
        maximum_limit_fraction: float | None = ...,
        limit_step_change: float | None = ...,
        rotation_duration: int | None = ...,
        lights: Sequence[_g.DemandManagerExteriorLightsLightsItem | _g.DemandManagerExteriorLightsLightsGroup] = ...,
    ) -> None:
        """Create a new ``DemandManager:ExteriorLights`` and add it to the document.

        used for demand limiting Exterior:Lights objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-demand-limiting-controls/#demandmanagerexteriorlights
        """
