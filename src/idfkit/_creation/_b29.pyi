"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class AnySimulationControl:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        do_zone_sizing_calculation: Literal["", "No", "Yes"] | None = "No",
        do_system_sizing_calculation: Literal["", "No", "Yes"] | None = "No",
        do_plant_sizing_calculation: Literal["", "No", "Yes"] | None = "No",
        run_simulation_for_sizing_periods: Literal["", "No", "Yes"] | None = "Yes",
        run_simulation_for_weather_file_run_periods: Literal["", "No", "Yes"] | None = "Yes",
        do_hvac_sizing_simulation_for_sizing_periods: Literal["", "No", "Yes"] | None = "No",
        maximum_number_of_hvac_sizing_simulation_passes: int | None = 1,
    ) -> None:
        """Create a new ``SimulationControl`` and add it to the document.

        Note that the following 3 fields are related to the Sizing:Zone, Sizing:System, and Sizing:Plant objects. Having these fields set to Yes but no corresponding Sizing object will not cause the sizing to be done. However, having any of these fields set to No, the corresponding Sizing object is ignored. Note also, if you want to do system sizing, you must also do zone sizing in the same run or an error will result.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#simulationcontrol
        """

class AnyTimestep:
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

class ConstructionFfactorGroundFloor:
    def __call__(self, name: str, /, *, f_factor: float, area: float, perimeterexposed: float) -> None:
        """Create a new ``Construction:FfactorGroundFloor`` and add it to the document.

        Alternate method of describing slab-on-grade or underground floor constructions

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#constructionffactorgroundfloor
        """

class AnyExteriorFuelEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        fuel_use_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "Electricity",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Water",
        ],
        schedule_name: str,
        design_level: float,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``Exterior:FuelEquipment`` and add it to the document.

        only used for Meter type reporting, does not affect building loads

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-exterior-energy-use-equipment/#exteriorfuelequipment
        """

class ZoneHVACVentilatedSlabSlabGroup:
    def __call__(
        self,
        name: str,
        /,
        *,
        data: Sequence[_g.ZoneHVACVentilatedSlabSlabGroupDataItem | _g.ZoneHVACVentilatedSlabSlabGroupDataGroup] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:VentilatedSlab:SlabGroup`` and add it to the document.

        This is used to allow the coordinate control of several ventilated slab system surfaces. Note that the flow fractions must sum up to 1.0. The number of surfaces can be expanded beyond 10, if necessary, by adding more groups to the end of the list

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvacventilatedslabslabgroup
        """

class AirTerminalSingleDuctVAVHeatAndCoolNoReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_outlet_node_name: str,
        air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        zone_minimum_air_flow_fraction: float,
        availability_schedule_name: str | None = ...,
        minimum_air_flow_turndown_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume for both cooling and heating, with no reheat coil.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-hvac-air-loop-terminal-units/#airterminalsingleductvavheatandcoolnoreheat
        """

class SolarCollectorUnglazedTranspiredMultisystem:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        solar_collector_name: str,
        systems: Sequence[
            _g.SolarCollectorUnglazedTranspiredMultisystemSystemsItem
            | _g.SolarCollectorUnglazedTranspiredMultisystemSystemsGroup
        ] = ...,
    ) -> None:
        """Create a new ``SolarCollector:UnglazedTranspired:Multisystem`` and add it to the document.

        quad-tuples of inlet, outlet, control, and zone nodes for multiple different outdoor air systems attached to same collector

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-solar-collectors/#solarcollectorunglazedtranspiredmultisystem
        """

class AnyMeterCustom:
    def __call__(
        self,
        name: str,
        /,
        *,
        variable_details: Sequence[_g.MeterCustomVariableDetailsItem | _g.MeterCustomVariableDetailsGroup] = ...,
    ) -> None:
        """Create a new ``Meter:Custom`` and add it to the document.

        Used to allow users to combine specific variables and/or meters into 'custom' meter configurations. To access these meters by name, one must first run a simulation to generate the RDD/MDD files and names. A Meter:Custom cannot reference another Meter:Custom or a Meter:CustomDecrement.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#metercustom
        """
