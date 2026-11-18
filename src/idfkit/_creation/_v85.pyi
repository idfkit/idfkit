"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g
from .. import versioned as _vd

class CoilSystemCoolingDXHeatExchangerAssisted_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        heat_exchanger_object_type: Literal[
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
            "HeatExchanger:Desiccant:BalancedFlow",
        ],
        heat_exchanger_name: str,
        cooling_coil_object_type: Literal["Coil:Cooling:DX:SingleSpeed", "Coil:Cooling:DX:VariableSpeed"],
        cooling_coil_name: str,
    ) -> None:
        """Create a new ``CoilSystem:Cooling:DX:HeatExchangerAssisted`` and add it to the document.

        Virtual component consisting of a direct expansion (DX) cooling coil and an air-to-air heat exchanger. The air-to-air heat exchanger precools the air entering the cooling coil and reuses this energy to reheat the supply air leaving the cooling coil. This heat exchange process improves the latent removal performance of the cooling coil (lower sensible heat ratio).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-heating-and-cooling-coils/#coilsystemcoolingdxheatexchangerassisted
        """

class ScheduleYear_v9_0_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        schedule_type_limits_name: str | None = ...,
        schedule_weeks: Sequence[
            _vd.ScheduleYearScheduleWeeksItem_v9_0_to_v22_1 | _vd.ScheduleYearScheduleWeeksGroup_v9_0_to_v22_1
        ] = ...,
    ) -> None:
        """Create a new ``Schedule:Year`` and add it to the document.

        A Schedule:Year contains from 1 to 52 week schedules

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-schedules/#scheduleyear
        """

class ZoneCoolTowerShower_v8_9_to_v24_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        pump_flow_rate_schedule_name: str,
        maximum_water_flow_rate: float,
        effective_tower_height: float,
        airflow_outlet_area: float,
        maximum_air_flow_rate: float,
        minimum_indoor_temperature: float,
        rated_power_consumption: float,
        availability_schedule_name: str | None = ...,
        water_supply_storage_tank_name: str | None = ...,
        flow_control_type: Literal["WaterFlowSchedule", "WindDrivenFlow"] | None = "WindDrivenFlow",
        fraction_of_water_loss: float | None = ...,
        fraction_of_flow_schedule: float | None = ...,
    ) -> None:
        """Create a new ``ZoneCoolTower:Shower`` and add it to the document.

        A cooltower (sometimes referred to as a wind tower or a shower cooling tower) models passive downdraught evaporative cooling (PDEC) that is designed to capture the wind at the top of a tower and cool the outdoor air using water evaporation before delivering it to a space.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.1/io-reference/overview/group-airflow/#zonecooltowershower
        """

class MeterCustom_v9_4_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        resource_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeating",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "Generic",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Steam",
            "Water",
        ]
        | None = ...,
        variable_details: Sequence[_g.MeterCustomVariableDetailsItem | _g.MeterCustomVariableDetailsGroup] = ...,
    ) -> None:
        """Create a new ``Meter:Custom`` and add it to the document.

        Used to allow users to combine specific variables and/or meters into 'custom' meter configurations. To access these meters by name, one must first run a simulation to generate the RDD/MDD files and names. A Meter:Custom cannot reference another Meter:Custom.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-simulation-parameters/#metercustom
        """
