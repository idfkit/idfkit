"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class WaterHeaterMixed_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        setpoint_temperature_schedule_name: str,
        heater_fuel_type: str,
        heater_thermal_efficiency: float,
        ambient_temperature_indicator: Literal["Outdoors", "Schedule", "Zone"],
        tank_volume: float | Literal["Autosize"] | None = 0,
        deadband_temperature_difference: float | None = 0,
        maximum_temperature_limit: float | None = ...,
        heater_control_type: Literal["Cycle", "Modulate"] | None = "Cycle",
        heater_maximum_capacity: float | Literal["Autosize"] | None = ...,
        heater_minimum_capacity: float | None = ...,
        heater_ignition_minimum_flow_rate: float | None = 0,
        heater_ignition_delay: float | None = 0,
        part_load_factor_curve_name: str | None = ...,
        off_cycle_parasitic_fuel_consumption_rate: float | None = 0,
        off_cycle_parasitic_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictHeating",
            "Electricity",
            "FuelOil#1",
            "FuelOil#2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "PropaneGas",
            "Steam",
        ]
        | None = ...,
        off_cycle_parasitic_heat_fraction_to_tank: float | None = 0,
        on_cycle_parasitic_fuel_consumption_rate: float | None = 0,
        on_cycle_parasitic_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictHeating",
            "Electricity",
            "FuelOil#1",
            "FuelOil#2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "PropaneGas",
            "Steam",
        ]
        | None = ...,
        on_cycle_parasitic_heat_fraction_to_tank: float | None = 0,
        ambient_temperature_schedule_name: str | None = ...,
        ambient_temperature_zone_name: str | None = ...,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        off_cycle_loss_coefficient_to_ambient_temperature: float | None = ...,
        off_cycle_loss_fraction_to_zone: float | None = 1,
        on_cycle_loss_coefficient_to_ambient_temperature: float | None = ...,
        on_cycle_loss_fraction_to_zone: float | None = 1,
        peak_use_flow_rate: float | None = ...,
        use_flow_rate_fraction_schedule_name: str | None = ...,
        cold_water_supply_temperature_schedule_name: str | None = ...,
        use_side_inlet_node_name: str | None = ...,
        use_side_outlet_node_name: str | None = ...,
        use_side_effectiveness: float | None = 1,
        source_side_inlet_node_name: str | None = ...,
        source_side_outlet_node_name: str | None = ...,
        source_side_effectiveness: float | None = 1,
        use_side_design_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        source_side_design_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        indirect_water_heating_recovery_time: float | None = 1.5,
        source_side_flow_control_mode: Literal[
            "IndirectHeatAlternateSetpoint", "IndirectHeatPrimarySetpoint", "StorageTank"
        ]
        | None = "IndirectHeatPrimarySetpoint",
        indirect_alternate_setpoint_temperature_schedule_name: str | None = ...,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``WaterHeater:Mixed`` and add it to the document.

        Water heater with well-mixed, single-node water tank. May be used to model a tankless water heater (small tank volume), a hot water storage tank (zero heater capacity), or a heat pump water heater (see WaterHeater:HeatPump:PumpedCondenser.)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-water-heaters/#waterheatermixed
        """

class CoilHeatingDesuperheater_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        heating_source_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:TwoSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
            "Refrigeration:CompressorRack",
            "Refrigeration:Condenser:AirCooled",
            "Refrigeration:Condenser:EvaporativeCooled",
            "Refrigeration:Condenser:WaterCooled",
        ],
        heating_source_name: str,
        availability_schedule_name: str | None = ...,
        heat_reclaim_recovery_efficiency: float | None = ...,
        temperature_setpoint_node_name: str | None = ...,
        parasitic_electric_load: float | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:Desuperheater`` and add it to the document.

        Desuperheater air heating coil. The heating energy provided by this coil is reclaimed from the superheated refrigerant gas leaving a compressor and does not impact the performance of the compressor. If the coil is located directly in an air loop branch or outdoor air equipment list, then it is controlled on leaving air temperature and the Temperature Setpoint Node Name must be specified. If the coil is contained within another component such as a unitary system, then the coil is controlled by the parent component and the setpoint node name is not entered.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-heating-and-cooling-coils/#coilheatingdesuperheater
        """

class SurfacePropertyLocalEnvironment_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        exterior_surface_name: str | None = ...,
        external_shading_fraction_schedule_name: str | None = ...,
        surrounding_surfaces_object_name: str | None = ...,
        outdoor_air_node_name: str | None = ...,
    ) -> None:
        """Create a new ``SurfaceProperty:LocalEnvironment`` and add it to the document.

        This object defines the local environment properties of an exterior surface. One or more environment properties have to be defined and linked to the exterior surface.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-advanced-surface-concepts/#surfacepropertylocalenvironment
        """

class CondenserEquipmentList_v8_9_to_v9_0:
    def __call__(
        self,
        name: str,
        /,
        *,
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
        """Create a new ``CondenserEquipmentList`` and add it to the document.

        List condenser equipment in order of operating priority, 1st in list will be used 1st, etc Use only condenser equipment in this list. If no equipment object types and equipment names are specified, then the corresponding PlantEquipmentOperation:* object will assume all available condenser equipment for the loop should be OFF (not operate) within the specified lower/upper limit.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.0/io-reference/overview/group-plant-condenser-control/#condenserequipmentlist
        """

class DemandManagerLights_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        limit_control: Literal["Fixed", "Off"],
        selection_control: Literal["All", "RotateMany", "RotateOne"],
        availability_schedule_name: str | None = ...,
        minimum_limit_duration: float | None = ...,
        maximum_limit_fraction: float | None = ...,
        limit_step_change: float | None = ...,
        rotation_duration: float | None = ...,
        lights: Sequence[_g.DemandManagerLightsLightsItem | _g.DemandManagerLightsLightsGroup] = ...,
    ) -> None:
        """Create a new ``DemandManager:Lights`` and add it to the document.

        used for demand limiting Lights objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-demand-limiting-controls/#demandmanagerlights
        """
