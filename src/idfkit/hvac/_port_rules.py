"""Auto-generated connection rules per object type, from EnergyPlus's node connection report.

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_port_rules --energyplus <EnergyPlus 26.2> --work-dir <dir>

Each rule records how one node field connects (connection type, fluid stream, fluid, parent flag)
and where the rule came from: ``eplus_examples`` (EnergyPlus's ``eplusout.bnd`` for the 26.2
example files), ``eplus_test_model`` (the same for a minimal model under
``codegen/port_rule_models/``) or ``hand_written`` (from the field's name, never reported by
EnergyPlus). Reviewed resolutions come from ``codegen/port_rule_overrides.toml``.

An extensible field is written ``group.field``; ``*.field`` matches any extensible group.
"""

from __future__ import annotations

from typing import Final

from idfkit.hvac._rule_types import PortRule
from idfkit.hvac.types import ConnectionType as C
from idfkit.hvac.types import Fluid as F

PORT_RULES: Final[dict[str, tuple[PortRule, ...]]] = {
    "AirConditioner:VariableRefrigerantFlow": (
        PortRule(
            "condenser_inlet_node_name",
            C.OUTSIDE_AIR,
            1,
            F.AIR,
            False,
            False,
            ("condenser_type", "AirCooled"),
            "eplus_examples",
        ),
        PortRule(
            "condenser_inlet_node_name",
            C.OUTSIDE_AIR,
            1,
            F.AIR,
            False,
            False,
            ("condenser_type", "EvaporativelyCooled"),
            "hand_written",
        ),
        PortRule(
            "condenser_inlet_node_name",
            C.INLET,
            2,
            F.WATER,
            False,
            False,
            ("condenser_type", "WaterCooled"),
            "eplus_examples",
        ),
        PortRule("condenser_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
    ),
    "AirLoopHVAC": (
        PortRule("demand_side_inlet_node_names", C.INLET, 1, F.AIR, True, True, None, "eplus_examples"),
        PortRule("demand_side_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("supply_side_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("supply_side_outlet_node_names", C.OUTLET, 1, F.AIR, True, True, None, "eplus_examples"),
    ),
    "AirLoopHVAC:Mixer": (
        PortRule("nodes.inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "AirLoopHVAC:ReturnPath": (
        PortRule("return_air_path_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "AirLoopHVAC:ReturnPlenum": (
        PortRule("induced_air_outlet_node_or_nodelist_name", C.OUTLET, 1, F.AIR, False, True, None, "eplus_examples"),
        PortRule("nodes.inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("zone_node_name", C.ZONE_NODE, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "AirLoopHVAC:Splitter": (
        PortRule("*.outlet_node_name", C.OUTLET, 1, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("inlet_node_name", C.INLET, 1, F.UNKNOWN, False, False, None, "hand_written"),
    ),
    "AirLoopHVAC:SupplyPath": (
        PortRule("supply_air_path_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "AirLoopHVAC:SupplyPlenum": (
        PortRule("inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("nodes.outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("zone_node_name", C.ZONE_NODE, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "AirLoopHVAC:Unitary:Furnace:HeatCool": (
        PortRule("furnace_air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("furnace_air_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "AirLoopHVAC:Unitary:Furnace:HeatOnly": (
        PortRule("furnace_air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("furnace_air_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "AirLoopHVAC:UnitaryHeatCool": (
        PortRule("unitary_system_air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("unitary_system_air_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "AirLoopHVAC:UnitaryHeatCool:VAVChangeoverBypass": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("bypass_duct_mixer_node_name", C.INTERNAL, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("bypass_duct_splitter_node_name", C.INTERNAL, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("plenum_or_mixer_inlet_node_name", C.INLET, 2, F.UNKNOWN, False, False, None, "hand_written"),
    ),
    "AirLoopHVAC:UnitaryHeatOnly": (
        PortRule("unitary_system_air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("unitary_system_air_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "AirLoopHVAC:UnitaryHeatPump:AirToAir": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "AirLoopHVAC:UnitaryHeatPump:AirToAir:MultiSpeed": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("heat_recovery_water_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "hand_written"),
        PortRule("heat_recovery_water_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "hand_written"),
    ),
    "AirLoopHVAC:UnitaryHeatPump:WaterToAir": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule(
            "outdoor_dry_bulb_temperature_sensor_node_name",
            C.OUTSIDE_AIR,
            1,
            F.AIR,
            False,
            False,
            None,
            "eplus_examples",
        ),
    ),
    "AirLoopHVAC:UnitarySystem": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("heat_recovery_water_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "hand_written"),
        PortRule("heat_recovery_water_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "hand_written"),
        PortRule(
            "outdoor_dry_bulb_temperature_sensor_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"
        ),
    ),
    "AirLoopHVAC:ZoneMixer": (
        PortRule("nodes.inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "AirLoopHVAC:ZoneSplitter": (
        PortRule("inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("nodes.outlet_node_name", C.OUTLET, 1, F.AIR, False, True, None, "eplus_examples"),
    ),
    "AirTerminal:DualDuct:ConstantVolume": (
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("cold_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("hot_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "AirTerminal:DualDuct:VAV": (
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("cold_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("hot_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "AirTerminal:DualDuct:VAV:OutdoorAir": (
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("outdoor_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("recirculated_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "AirTerminal:SingleDuct:ConstantVolume:CooledBeam": (
        PortRule("chilled_water_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("chilled_water_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("supply_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("supply_air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "AirTerminal:SingleDuct:ConstantVolume:FourPipeBeam": (
        PortRule("chilled_water_inlet_node_name", C.INLET, 2, F.WATER, True, False, None, "eplus_examples"),
        PortRule("chilled_water_outlet_node_name", C.OUTLET, 2, F.WATER, True, False, None, "eplus_examples"),
        PortRule("hot_water_inlet_node_name", C.INLET, 2, F.WATER, True, False, None, "eplus_examples"),
        PortRule("hot_water_outlet_node_name", C.OUTLET, 2, F.WATER, True, False, None, "eplus_examples"),
        PortRule("primary_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("primary_air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "AirTerminal:SingleDuct:ConstantVolume:FourPipeInduction": (
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("induced_air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("supply_air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "AirTerminal:SingleDuct:ConstantVolume:NoReheat": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "AirTerminal:SingleDuct:ConstantVolume:Reheat": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "AirTerminal:SingleDuct:Mixer": (
        PortRule("mixer_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("mixer_primary_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("mixer_secondary_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "AirTerminal:SingleDuct:ParallelPIU:Reheat": (
        PortRule("outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("reheat_coil_air_inlet_node_name", C.INLET, 2, F.AIR, False, False, None, "hand_written"),
        PortRule("secondary_air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("supply_air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "AirTerminal:SingleDuct:SeriesPIU:Reheat": (
        PortRule("outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("reheat_coil_air_inlet_node_name", C.INLET, 2, F.AIR, False, False, None, "hand_written"),
        PortRule("secondary_air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("supply_air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "AirTerminal:SingleDuct:UserDefined": (
        PortRule("plant_connection_1_inlet_node_name", C.INLET, 3, F.WATER, False, False, None, "eplus_examples"),
        PortRule("plant_connection_1_outlet_node_name", C.OUTLET, 3, F.WATER, False, False, None, "eplus_examples"),
        PortRule("plant_connection_2_inlet_node_name", C.INLET, 5, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("plant_connection_2_outlet_node_name", C.OUTLET, 5, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("primary_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("primary_air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("secondary_air_inlet_node_name", C.INLET, 4, F.AIR, False, False, None, "hand_written"),
        PortRule("secondary_air_outlet_node_name", C.OUTLET, 4, F.AIR, False, False, None, "hand_written"),
    ),
    "AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "AirTerminal:SingleDuct:VAV:HeatAndCool:Reheat": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("damper_air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "AirTerminal:SingleDuct:VAV:NoReheat": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "AirTerminal:SingleDuct:VAV:Reheat": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("damper_air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "AirTerminal:SingleDuct:VAV:Reheat:VariableSpeedFan": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "hand_written"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "hand_written"),
    ),
    "AvailabilityManager:DifferentialThermostat": (
        PortRule("cold_node_name", C.SENSOR, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("hot_node_name", C.SENSOR, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "AvailabilityManager:HighTemperatureTurnOff": (
        PortRule("sensor_node_name", C.SENSOR, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "AvailabilityManager:HighTemperatureTurnOn": (
        PortRule("sensor_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "AvailabilityManager:LowTemperatureTurnOff": (
        PortRule("sensor_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "AvailabilityManager:LowTemperatureTurnOn": (
        PortRule("sensor_node_name", C.SENSOR, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Boiler:HotWater": (
        PortRule("boiler_water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("boiler_water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Boiler:Steam": (
        PortRule("steam_outlet_node_name", C.OUTLET, 1, F.STEAM, False, False, None, "eplus_examples"),
        PortRule("water_inlet_node_name", C.INLET, 1, F.STEAM, False, False, None, "eplus_examples"),
    ),
    "Branch": (
        PortRule("components.component_inlet_node_name", C.INLET, 1, F.WATER, True, False, None, "eplus_examples"),
        PortRule("components.component_outlet_node_name", C.OUTLET, 1, F.WATER, True, False, None, "eplus_examples"),
    ),
    "CentralHeatPumpSystem": (
        PortRule("cooling_loop_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("cooling_loop_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("heating_loop_inlet_node_name", C.INLET, 3, F.WATER, False, False, None, "eplus_examples"),
        PortRule("heating_loop_outlet_node_name", C.OUTLET, 3, F.WATER, False, False, None, "eplus_examples"),
        PortRule("source_loop_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("source_loop_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Chiller:Absorption": (
        PortRule("chilled_water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("chilled_water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("condenser_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("condenser_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("generator_inlet_node_name", C.INLET, 3, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("generator_outlet_node_name", C.OUTLET, 3, F.UNKNOWN, False, False, None, "hand_written"),
    ),
    "Chiller:Absorption:Indirect": (
        PortRule("chilled_water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("chilled_water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("condenser_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("condenser_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("generator_inlet_node_name", C.INLET, 3, F.STEAM, False, False, None, "eplus_examples"),
        PortRule("generator_outlet_node_name", C.OUTLET, 3, F.STEAM, False, False, None, "eplus_examples"),
    ),
    "Chiller:CombustionTurbine": (
        PortRule("chilled_water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("chilled_water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("condenser_inlet_node_name", C.INLET, 2, F.UNKNOWN, False, False, None, "eplus_examples"),
        PortRule("condenser_outlet_node_name", C.OUTLET, 2, F.UNKNOWN, False, False, None, "eplus_examples"),
        PortRule("heat_recovery_inlet_node_name", C.INLET, 3, F.WATER, False, False, None, "eplus_examples"),
        PortRule("heat_recovery_outlet_node_name", C.OUTLET, 3, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Chiller:ConstantCOP": (
        PortRule("chilled_water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("chilled_water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule(
            "condenser_inlet_node_name",
            C.OUTSIDE_AIR,
            2,
            F.AIR,
            False,
            False,
            ("condenser_type", "AirCooled"),
            "eplus_examples",
        ),
        PortRule(
            "condenser_inlet_node_name",
            C.OUTSIDE_AIR,
            2,
            F.AIR,
            False,
            False,
            ("condenser_type", "EvaporativelyCooled"),
            "eplus_examples",
        ),
        PortRule(
            "condenser_inlet_node_name",
            C.INLET,
            2,
            F.WATER,
            False,
            False,
            ("condenser_type", "WaterCooled"),
            "eplus_examples",
        ),
        PortRule("condenser_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Chiller:Electric": (
        PortRule("chilled_water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("chilled_water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule(
            "condenser_inlet_node_name",
            C.OUTSIDE_AIR,
            2,
            F.AIR,
            False,
            False,
            ("condenser_type", "AirCooled"),
            "eplus_examples",
        ),
        PortRule(
            "condenser_inlet_node_name",
            C.OUTSIDE_AIR,
            2,
            F.AIR,
            False,
            False,
            ("condenser_type", "EvaporativelyCooled"),
            "hand_written",
        ),
        PortRule(
            "condenser_inlet_node_name",
            C.INLET,
            2,
            F.WATER,
            False,
            False,
            ("condenser_type", "WaterCooled"),
            "eplus_examples",
        ),
        PortRule("condenser_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("heat_recovery_inlet_node_name", C.INLET, 3, F.WATER, False, False, None, "eplus_examples"),
        PortRule(
            "heat_recovery_leaving_temperature_setpoint_node_name",
            C.SETPOINT,
            4,
            F.UNKNOWN,
            False,
            False,
            None,
            "hand_written",
        ),
        PortRule("heat_recovery_outlet_node_name", C.OUTLET, 3, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Chiller:Electric:ASHRAE205": (
        PortRule(
            "ambient_temperature_outdoor_air_node_name", C.OUTSIDE_AIR, 5, F.AIR, False, False, None, "hand_written"
        ),
        PortRule("auxiliary_inlet_node_name", C.INLET, 4, F.WATER, False, False, None, "hand_written"),
        PortRule("auxiliary_outlet_node_name", C.OUTLET, 4, F.WATER, False, False, None, "eplus_examples"),
        PortRule("chilled_water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("chilled_water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("condenser_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("condenser_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("heat_recovery_inlet_node_name", C.INLET, 6, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("heat_recovery_outlet_node_name", C.OUTLET, 6, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("oil_cooler_inlet_node_name", C.INLET, 3, F.WATER, False, False, None, "eplus_examples"),
        PortRule("oil_cooler_outlet_node_name", C.OUTLET, 3, F.WATER, False, False, None, "hand_written"),
    ),
    "Chiller:Electric:EIR": (
        PortRule("chilled_water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("chilled_water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule(
            "condenser_inlet_node_name",
            C.OUTSIDE_AIR,
            2,
            F.AIR,
            False,
            False,
            ("condenser_type", "AirCooled"),
            "eplus_examples",
        ),
        PortRule(
            "condenser_inlet_node_name",
            C.OUTSIDE_AIR,
            2,
            F.AIR,
            False,
            False,
            ("condenser_type", "EvaporativelyCooled"),
            "eplus_examples",
        ),
        PortRule(
            "condenser_inlet_node_name",
            C.INLET,
            2,
            F.WATER,
            False,
            False,
            ("condenser_type", "WaterCooled"),
            "eplus_examples",
        ),
        PortRule("condenser_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("heat_recovery_inlet_node_name", C.INLET, 3, F.WATER, False, False, None, "eplus_examples"),
        PortRule(
            "heat_recovery_leaving_temperature_setpoint_node_name",
            C.SETPOINT,
            4,
            F.UNKNOWN,
            False,
            False,
            None,
            "hand_written",
        ),
        PortRule("heat_recovery_outlet_node_name", C.OUTLET, 3, F.WATER, False, False, None, "hand_written"),
    ),
    "Chiller:Electric:ReformulatedEIR": (
        PortRule("chilled_water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("chilled_water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("condenser_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("condenser_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("heat_recovery_inlet_node_name", C.INLET, 3, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule(
            "heat_recovery_leaving_temperature_setpoint_node_name",
            C.SETPOINT,
            4,
            F.UNKNOWN,
            False,
            False,
            None,
            "hand_written",
        ),
        PortRule("heat_recovery_outlet_node_name", C.OUTLET, 3, F.UNKNOWN, False, False, None, "hand_written"),
    ),
    "Chiller:EngineDriven": (
        PortRule("chilled_water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("chilled_water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("condenser_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("condenser_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("heat_recovery_inlet_node_name", C.INLET, 3, F.WATER, False, False, None, "eplus_examples"),
        PortRule("heat_recovery_outlet_node_name", C.OUTLET, 3, F.WATER, False, False, None, "eplus_examples"),
    ),
    "ChillerHeater:Absorption:DirectFired": (
        PortRule("chilled_water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("chilled_water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("condenser_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("condenser_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("hot_water_inlet_node_name", C.INLET, 3, F.WATER, False, False, None, "eplus_examples"),
        PortRule("hot_water_outlet_node_name", C.OUTLET, 3, F.WATER, False, False, None, "eplus_examples"),
    ),
    "ChillerHeater:Absorption:DoubleEffect": (
        PortRule("chilled_water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("chilled_water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("condenser_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("condenser_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("hot_water_inlet_node_name", C.INLET, 3, F.WATER, False, False, None, "eplus_examples"),
        PortRule("hot_water_outlet_node_name", C.OUTLET, 3, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Coil:Cooling:DX": (
        PortRule("condenser_inlet_node_name", C.INLET, 2, F.AIR, False, False, None, "eplus_examples"),
        PortRule("condenser_outlet_node_name", C.OUTLET, 2, F.AIR, False, False, None, "eplus_examples"),
        PortRule("evaporator_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("evaporator_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Coil:Cooling:DX:MultiSpeed": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("condenser_air_inlet_node_name", C.OUTSIDE_AIR, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Coil:Cooling:DX:SingleSpeed": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("condenser_air_inlet_node_name", C.OUTSIDE_AIR, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Coil:Cooling:DX:SingleSpeed:ThermalStorage": (
        PortRule("condenser_air_inlet_node_name", C.INLET, 3, F.AIR, False, False, None, "hand_written"),
        PortRule("condenser_air_outlet_node_name", C.OUTLET, 3, F.AIR, False, False, None, "hand_written"),
        PortRule("evaporator_air_inlet_node_name", C.INLET, 2, F.AIR, False, False, None, "hand_written"),
        PortRule("evaporator_air_outlet_node_name", C.OUTLET, 2, F.AIR, False, False, None, "hand_written"),
        PortRule(
            "storage_tank_ambient_temperature_node_name",
            C.OUTSIDE_AIR,
            1,
            F.UNKNOWN,
            False,
            False,
            None,
            "hand_written",
        ),
        PortRule(
            "storage_tank_plant_connection_inlet_node_name", C.INLET, 4, F.UNKNOWN, False, False, None, "hand_written"
        ),
        PortRule(
            "storage_tank_plant_connection_outlet_node_name", C.OUTLET, 4, F.UNKNOWN, False, False, None, "hand_written"
        ),
    ),
    "Coil:Cooling:DX:TwoSpeed": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("condenser_air_inlet_node_name", C.OUTSIDE_AIR, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Coil:Cooling:DX:TwoStageWithHumidityControlMode": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Coil:Cooling:DX:VariableRefrigerantFlow": (
        PortRule("coil_air_inlet_node", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("coil_air_outlet_node", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Coil:Cooling:DX:VariableRefrigerantFlow:FluidTemperatureControl": (
        PortRule("coil_air_inlet_node", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("coil_air_outlet_node", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Coil:Cooling:DX:VariableSpeed": (
        PortRule("condenser_air_inlet_node_name", C.OUTSIDE_AIR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("indoor_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("indoor_air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Coil:Cooling:Water": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("water_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("water_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Coil:Cooling:Water:DetailedGeometry": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("water_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("water_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Coil:Cooling:WaterToAirHeatPump:EquationFit": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("water_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("water_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Coil:Cooling:WaterToAirHeatPump:ParameterEstimation": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("water_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("water_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit": (
        PortRule("indoor_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("indoor_air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule(
            "water_to_refrigerant_hx_water_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"
        ),
        PortRule(
            "water_to_refrigerant_hx_water_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"
        ),
    ),
    "Coil:Heating:DX:MultiSpeed": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Coil:Heating:DX:SingleSpeed": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("evaporator_air_inlet_node_name", C.OUTSIDE_AIR, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Coil:Heating:DX:VariableRefrigerantFlow": (
        PortRule("coil_air_inlet_node", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("coil_air_outlet_node", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Coil:Heating:DX:VariableRefrigerantFlow:FluidTemperatureControl": (
        PortRule("coil_air_inlet_node", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("coil_air_outlet_node", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Coil:Heating:DX:VariableSpeed": (
        PortRule("indoor_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("indoor_air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Coil:Heating:Desuperheater": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("temperature_setpoint_node_name", C.SETPOINT, 2, F.UNKNOWN, False, False, None, "hand_written"),
    ),
    "Coil:Heating:Electric": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("temperature_setpoint_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Coil:Heating:Electric:MultiStage": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("temperature_setpoint_node_name", C.SETPOINT, 2, F.UNKNOWN, False, False, None, "hand_written"),
    ),
    "Coil:Heating:Fuel": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("temperature_setpoint_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Coil:Heating:Gas:MultiStage": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("temperature_setpoint_node_name", C.SETPOINT, 2, F.UNKNOWN, False, False, None, "hand_written"),
    ),
    "Coil:Heating:Steam": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("temperature_setpoint_node_name", C.SETPOINT, 3, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("water_inlet_node_name", C.INLET, 2, F.STEAM, False, False, None, "eplus_examples"),
        PortRule("water_outlet_node_name", C.OUTLET, 2, F.STEAM, False, False, None, "eplus_examples"),
    ),
    "Coil:Heating:Water": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("water_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("water_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Coil:Heating:WaterToAirHeatPump:EquationFit": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("water_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("water_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Coil:Heating:WaterToAirHeatPump:ParameterEstimation": (
        PortRule("air_inlet_node_name", C.INLET, 2, F.AIR, False, False, None, "hand_written"),
        PortRule("air_outlet_node_name", C.OUTLET, 2, F.AIR, False, False, None, "hand_written"),
        PortRule("water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "hand_written"),
        PortRule("water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "hand_written"),
    ),
    "Coil:Heating:WaterToAirHeatPump:VariableSpeedEquationFit": (
        PortRule("indoor_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("indoor_air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule(
            "water_to_refrigerant_hx_water_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"
        ),
        PortRule(
            "water_to_refrigerant_hx_water_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"
        ),
    ),
    "Coil:UserDefined": (
        PortRule("air_connection_1_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_connection_1_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_connection_2_inlet_node_name", C.INLET, 4, F.AIR, False, False, None, "hand_written"),
        PortRule("air_connection_2_outlet_node_name", C.OUTLET, 4, F.AIR, False, False, None, "hand_written"),
        PortRule("plant_connection_inlet_node_name", C.INLET, 3, F.WATER, False, False, None, "eplus_examples"),
        PortRule("plant_connection_outlet_node_name", C.OUTLET, 3, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Coil:WaterHeating:AirToWaterHeatPump:Pumped": (
        PortRule("condenser_water_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("condenser_water_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("evaporator_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("evaporator_air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Coil:WaterHeating:AirToWaterHeatPump:VariableSpeed": (
        PortRule("condenser_water_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("condenser_water_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("evaporator_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("evaporator_air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Coil:WaterHeating:AirToWaterHeatPump:Wrapped": (
        PortRule("evaporator_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("evaporator_air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Coil:WaterHeating:Desuperheater": (
        PortRule("water_inlet_node_name", C.INLET, 1, F.WATER, True, False, None, "eplus_examples"),
        PortRule("water_outlet_node_name", C.OUTLET, 1, F.WATER, True, False, None, "eplus_examples"),
    ),
    "CoilPerformance:DX:Cooling": (
        PortRule("condenser_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "hand_written"),
    ),
    "CoilSystem:Cooling:DX": (
        PortRule("dx_cooling_coil_system_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("dx_cooling_coil_system_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("dx_cooling_coil_system_sensor_node_name", C.SENSOR, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "CoilSystem:Cooling:Water": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "CoilSystem:IntegratedHeatPump:AirSource": (
        PortRule("supply_hot_water_flow_sensor_node_name", C.SENSOR, 2, F.WATER, False, False, None, "eplus_examples"),
    ),
    "CondenserLoop": (
        PortRule(
            "condenser_loop_temperature_setpoint_node_name", C.SENSOR, 1, F.WATER, True, False, None, "eplus_examples"
        ),
        PortRule("condenser_side_inlet_node_name", C.INLET, 1, F.WATER, True, False, None, "eplus_examples"),
        PortRule("condenser_side_outlet_node_name", C.OUTLET, 1, F.WATER, True, False, None, "eplus_examples"),
        PortRule("demand_side_inlet_node_name", C.INLET, 1, F.WATER, True, False, None, "eplus_examples"),
        PortRule("demand_side_outlet_node_name", C.OUTLET, 1, F.WATER, True, False, None, "eplus_examples"),
    ),
    "Controller:OutdoorAir": (
        PortRule("actuator_node_name", C.ACTUATOR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("mixed_air_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("relief_air_outlet_node_name", C.ACTUATOR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("return_air_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Controller:WaterCoil": (
        PortRule("actuator_node_name", C.ACTUATOR, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("sensor_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "CoolingTower:SingleSpeed": (
        PortRule("outdoor_air_inlet_node_name", C.OUTSIDE_AIR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "CoolingTower:TwoSpeed": (
        PortRule("outdoor_air_inlet_node_name", C.OUTSIDE_AIR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "CoolingTower:VariableSpeed": (
        PortRule("outdoor_air_inlet_node_name", C.OUTSIDE_AIR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "CoolingTower:VariableSpeed:Merkel": (
        PortRule("outdoor_air_inlet_node_name", C.INLET, 2, F.AIR, False, False, None, "hand_written"),
        PortRule("water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Dehumidifier:Desiccant:NoFans": (
        PortRule("process_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("process_air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("regeneration_air_inlet_node_name", C.INLET, 2, F.AIR, False, False, None, "eplus_examples"),
        PortRule("regeneration_fan_inlet_node_name", C.INTERNAL, 2, F.AIR, True, False, None, "eplus_examples"),
    ),
    "Dehumidifier:Desiccant:System": (
        PortRule("sensor_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "DistrictCooling": (
        PortRule("chilled_water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("chilled_water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "DistrictHeating": (
        PortRule("hot_water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "hand_written"),
        PortRule("hot_water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "hand_written"),
    ),
    "DistrictHeating:Steam": (
        PortRule("steam_inlet_node_name", C.INLET, 1, F.STEAM, False, False, None, "eplus_examples"),
        PortRule("steam_outlet_node_name", C.OUTLET, 1, F.STEAM, False, False, None, "eplus_examples"),
    ),
    "DistrictHeating:Water": (
        PortRule("hot_water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("hot_water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Duct": (
        PortRule("inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "ElectricEquipment:ITE:AirCooled": (
        PortRule("supply_air_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "ElectricEquipment:ITE:AirCooled:Instance": (
        PortRule("supply_air_node_name", C.SENSOR, 1, F.AIR, False, False, None, "hand_written"),
    ),
    "EvaporativeCooler:Direct:CelDekPad": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "EvaporativeCooler:Direct:ResearchSpecial": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "hand_written"),
        PortRule("sensor_node_name", C.SENSOR, 2, F.UNKNOWN, False, False, None, "hand_written"),
    ),
    "EvaporativeCooler:Indirect:CelDekPad": (
        PortRule("primary_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("primary_air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("secondary_air_inlet_node_name", C.OUTSIDE_AIR, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "EvaporativeCooler:Indirect:ResearchSpecial": (
        PortRule("primary_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("primary_air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("relief_air_inlet_node_name", C.INLET, 3, F.AIR, False, False, None, "eplus_examples"),
        PortRule("secondary_air_inlet_node_name", C.INLET, 2, F.AIR, False, False, None, "eplus_examples"),
        PortRule("secondary_air_outlet_node_name", C.OUTLET, 2, F.AIR, False, False, None, "eplus_examples"),
        PortRule("sensor_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "EvaporativeCooler:Indirect:WetCoil": (
        PortRule("primary_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("primary_air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("secondary_air_inlet_node_name", C.OUTSIDE_AIR, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "EvaporativeFluidCooler:SingleSpeed": (
        PortRule("outdoor_air_inlet_node_name", C.INLET, 2, F.AIR, False, False, None, "hand_written"),
        PortRule("water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "EvaporativeFluidCooler:TwoSpeed": (
        PortRule("outdoor_air_inlet_node_name", C.INLET, 2, F.AIR, False, False, None, "hand_written"),
        PortRule("water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Fan:ComponentModel": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Fan:ConstantVolume": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Fan:OnOff": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Fan:SystemModel": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Fan:VariableVolume": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Fan:ZoneExhaust": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "FluidCooler:SingleSpeed": (
        PortRule("outdoor_air_inlet_node_name", C.INLET, 2, F.AIR, False, False, None, "hand_written"),
        PortRule("water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "FluidCooler:TwoSpeed": (
        PortRule("outdoor_air_inlet_node_name", C.INLET, 2, F.AIR, False, False, None, "hand_written"),
        PortRule("water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Generator:CombustionTurbine": (
        PortRule("heat_recovery_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("heat_recovery_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("outdoor_air_inlet_node_name", C.OUTSIDE_AIR, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Generator:FuelCell:AirSupply": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Generator:FuelCell:ExhaustGasToWaterHeatExchanger": (
        PortRule("exhaust_outlet_air_node_name", C.OUTLET, 2, F.AIR, False, False, None, "eplus_examples"),
        PortRule("heat_recovery_water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("heat_recovery_water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Generator:FuelCell:PowerModule": (
        PortRule("dilution_inlet_air_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("dilution_outlet_air_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Generator:FuelCell:StackCooler": (
        PortRule("heat_recovery_water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "hand_written"),
        PortRule("heat_recovery_water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "hand_written"),
    ),
    "Generator:FuelCell:WaterSupply": (
        PortRule("water_temperature_reference_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Generator:FuelSupply": (
        PortRule("fuel_temperature_reference_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Generator:InternalCombustionEngine": (
        PortRule("heat_recovery_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("heat_recovery_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Generator:MicroCHP": (
        PortRule("air_inlet_node_name", C.INLET, 2, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 2, F.AIR, False, False, None, "hand_written"),
        PortRule("cooling_water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("cooling_water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Generator:MicroTurbine": (
        PortRule("combustion_air_inlet_node_name", C.INLET, 2, F.AIR, False, False, None, "eplus_examples"),
        PortRule("combustion_air_outlet_node_name", C.OUTLET, 2, F.AIR, False, False, None, "eplus_examples"),
        PortRule("heat_recovery_water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("heat_recovery_water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "GroundHeatExchanger:HorizontalTrench": (
        PortRule("inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "GroundHeatExchanger:Pond": (
        PortRule("fluid_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("fluid_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "GroundHeatExchanger:Slinky": (
        PortRule("inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "GroundHeatExchanger:Surface": (
        PortRule("fluid_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("fluid_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "GroundHeatExchanger:System": (
        PortRule("inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "HeaderedPumps:ConstantSpeed": (
        PortRule("inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "HeaderedPumps:VariableSpeed": (
        PortRule("inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "HeatExchanger:AirToAir:FlatPlate": (
        PortRule("secondary_air_inlet_node_name", C.INLET, 2, F.AIR, False, False, None, "eplus_examples"),
        PortRule("secondary_air_outlet_node_name", C.OUTLET, 2, F.AIR, False, False, None, "eplus_examples"),
        PortRule("supply_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("supply_air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "HeatExchanger:AirToAir:SensibleAndLatent": (
        PortRule("exhaust_air_inlet_node_name", C.INLET, 2, F.AIR, False, False, None, "eplus_examples"),
        PortRule("exhaust_air_outlet_node_name", C.OUTLET, 2, F.AIR, False, False, None, "eplus_examples"),
        PortRule("supply_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("supply_air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "HeatExchanger:Desiccant:BalancedFlow": (
        PortRule("process_air_inlet_node_name", C.INLET, 2, F.AIR, False, False, None, "eplus_examples"),
        PortRule("process_air_outlet_node_name", C.OUTLET, 2, F.AIR, False, False, None, "eplus_examples"),
        PortRule("regeneration_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("regeneration_air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "HeatExchanger:FluidToFluid": (
        PortRule(
            "component_override_loop_demand_side_inlet_node_name",
            C.ACTUATOR,
            1,
            F.WATER,
            False,
            False,
            None,
            "eplus_examples",
        ),
        PortRule(
            "component_override_loop_supply_side_inlet_node_name",
            C.ACTUATOR,
            1,
            F.WATER,
            False,
            False,
            None,
            "eplus_examples",
        ),
        PortRule("heat_exchanger_setpoint_node_name", C.SENSOR, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("loop_demand_side_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("loop_demand_side_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("loop_supply_side_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("loop_supply_side_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
    ),
    "HeatPump:AirToWater": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "hand_written"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "hand_written"),
        PortRule("chilled_water_inlet_node_name", C.INLET, 3, F.WATER, False, False, None, "hand_written"),
        PortRule("chilled_water_outlet_node_name", C.OUTLET, 3, F.WATER, False, False, None, "hand_written"),
        PortRule("hot_water_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "hand_written"),
        PortRule("hot_water_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "hand_written"),
    ),
    "HeatPump:AirToWater:FuelFired:Cooling": (
        PortRule("air_source_node_name", C.OUTSIDE_AIR, 2, F.AIR, False, False, None, "eplus_examples"),
        PortRule("water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "HeatPump:AirToWater:FuelFired:Heating": (
        PortRule("air_source_node_name", C.OUTSIDE_AIR, 2, F.AIR, False, False, None, "eplus_examples"),
        PortRule("water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "HeatPump:PlantLoop:EIR:Cooling": (
        PortRule("heat_recovery_inlet_node_name", C.INLET, 3, F.WATER, False, False, None, "eplus_examples"),
        PortRule("heat_recovery_outlet_node_name", C.OUTLET, 3, F.WATER, False, False, None, "eplus_examples"),
        PortRule("load_side_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("load_side_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("source_side_inlet_node_name", C.INLET, 2, F.AIR, False, False, None, "eplus_examples"),
        PortRule("source_side_outlet_node_name", C.OUTLET, 2, F.AIR, False, False, None, "eplus_examples"),
    ),
    "HeatPump:PlantLoop:EIR:Heating": (
        PortRule("heat_recovery_inlet_node_name", C.INLET, 3, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("heat_recovery_outlet_node_name", C.OUTLET, 3, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("load_side_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("load_side_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("source_side_inlet_node_name", C.INLET, 2, F.AIR, False, False, None, "eplus_examples"),
        PortRule("source_side_outlet_node_name", C.OUTLET, 2, F.AIR, False, False, None, "eplus_examples"),
    ),
    "HeatPump:WaterToWater:EIR:Cooling": (
        PortRule("load_side_inlet_node_name", C.INLET, 2, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("load_side_outlet_node_name", C.OUTLET, 2, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("source_side_inlet_node_name", C.INLET, 1, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("source_side_outlet_node_name", C.OUTLET, 1, F.UNKNOWN, False, False, None, "hand_written"),
    ),
    "HeatPump:WaterToWater:EIR:Heating": (
        PortRule("load_side_inlet_node_name", C.INLET, 2, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("load_side_outlet_node_name", C.OUTLET, 2, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("source_side_inlet_node_name", C.INLET, 1, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("source_side_outlet_node_name", C.OUTLET, 1, F.UNKNOWN, False, False, None, "hand_written"),
    ),
    "HeatPump:WaterToWater:EquationFit:Cooling": (
        PortRule("load_side_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("load_side_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("source_side_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("source_side_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "HeatPump:WaterToWater:EquationFit:Heating": (
        PortRule("load_side_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("load_side_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("source_side_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("source_side_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "HeatPump:WaterToWater:ParameterEstimation:Cooling": (
        PortRule("load_side_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("load_side_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("source_side_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("source_side_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "HeatPump:WaterToWater:ParameterEstimation:Heating": (
        PortRule("load_side_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("load_side_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("source_side_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("source_side_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Humidifier:Steam:Electric": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Humidifier:Steam:Gas": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "Lights": (
        PortRule("exhaust_air_heat_gain_node_name", C.ZONE_EXHAUST, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("return_air_heat_gain_node_name", C.SENSOR, 1, F.AIR, False, False, None, "hand_written"),
    ),
    "Lights:Instance": (
        PortRule("exhaust_air_heat_gain_node_name", C.ZONE_EXHAUST, 1, F.AIR, False, False, None, "hand_written"),
        PortRule("return_air_heat_gain_node_name", C.SENSOR, 1, F.AIR, False, False, None, "hand_written"),
    ),
    "LoadProfile:Plant": (
        PortRule("inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "OutdoorAir:Mixer": (
        PortRule("mixed_air_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("outdoor_air_stream_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("relief_air_stream_node_name", C.RELIEF_AIR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("return_air_stream_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "OutdoorAir:NodeList": (
        PortRule("nodes.node_or_nodelist_name", C.OUTSIDE_AIR, 1, F.AIR, False, True, None, "eplus_examples"),
    ),
    "Pipe:Adiabatic": (
        PortRule("inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Pipe:Adiabatic:Steam": (
        PortRule("inlet_node_name", C.INLET, 1, F.STEAM, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.STEAM, False, False, None, "eplus_examples"),
    ),
    "Pipe:Indoor": (
        PortRule("fluid_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("fluid_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Pipe:Outdoor": (
        PortRule(
            "ambient_temperature_outdoor_air_node_name", C.OUTSIDE_AIR, 1, F.AIR, False, False, None, "eplus_examples"
        ),
        PortRule("fluid_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("fluid_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Pipe:Underground": (
        PortRule("fluid_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("fluid_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "PipingSystem:Underground:PipeCircuit": (
        PortRule("circuit_inlet_node", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("circuit_outlet_node", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "PlantComponent:TemperatureSource": (
        PortRule("inlet_node", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("outlet_node", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "PlantComponent:UserDefined": (
        PortRule("air_connection_inlet_node_name", C.OUTSIDE_AIR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_connection_outlet_node_name", C.RELIEF_AIR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("plant_connection_1_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("plant_connection_1_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("plant_connection_2_inlet_node_name", C.INLET, 2, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("plant_connection_2_outlet_node_name", C.OUTLET, 2, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("plant_connection_3_inlet_node_name", C.INLET, 3, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("plant_connection_3_outlet_node_name", C.OUTLET, 3, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("plant_connection_4_inlet_node_name", C.INLET, 4, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("plant_connection_4_outlet_node_name", C.OUTLET, 4, F.UNKNOWN, False, False, None, "hand_written"),
    ),
    "PlantEquipmentOperation:ComponentSetpoint": (
        PortRule("demand_calculation_10_node_name", C.SENSOR, 14, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("demand_calculation_1_node_name", C.SENSOR, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("demand_calculation_2_node_name", C.SENSOR, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("demand_calculation_3_node_name", C.SENSOR, 1, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("demand_calculation_4_node_name", C.SENSOR, 2, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("demand_calculation_5_node_name", C.SENSOR, 4, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("demand_calculation_6_node_name", C.SENSOR, 6, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("demand_calculation_7_node_name", C.SENSOR, 8, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("demand_calculation_8_node_name", C.SENSOR, 10, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("demand_calculation_9_node_name", C.SENSOR, 12, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("setpoint_10_node_name", C.SETPOINT, 15, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("setpoint_1_node_name", C.SENSOR, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("setpoint_2_node_name", C.SENSOR, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("setpoint_3_node_name", C.SENSOR, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("setpoint_4_node_name", C.SETPOINT, 3, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("setpoint_5_node_name", C.SETPOINT, 5, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("setpoint_6_node_name", C.SETPOINT, 7, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("setpoint_7_node_name", C.SETPOINT, 9, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("setpoint_8_node_name", C.SETPOINT, 11, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("setpoint_9_node_name", C.SETPOINT, 13, F.UNKNOWN, False, False, None, "hand_written"),
    ),
    "PlantEquipmentOperation:OutdoorDewpointDifference": (
        PortRule("reference_temperature_node_name", C.SENSOR, 1, F.UNKNOWN, False, False, None, "hand_written"),
    ),
    "PlantEquipmentOperation:OutdoorDryBulbDifference": (
        PortRule("reference_temperature_node_name", C.SENSOR, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "PlantEquipmentOperation:OutdoorWetBulbDifference": (
        PortRule("reference_temperature_node_name", C.SENSOR, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "PlantEquipmentOperation:ThermalEnergyStorage": (
        PortRule(
            "component_10_demand_calculation_node_name", C.SENSOR, 15, F.UNKNOWN, False, False, None, "hand_written"
        ),
        PortRule("component_10_setpoint_node_name", C.SETPOINT, 16, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule(
            "component_1_demand_calculation_node_name", C.SENSOR, 1, F.WATER, False, False, None, "eplus_examples"
        ),
        PortRule("component_1_setpoint_node_name", C.SENSOR, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule(
            "component_2_demand_calculation_node_name", C.SENSOR, 1, F.WATER, False, False, None, "eplus_examples"
        ),
        PortRule("component_2_setpoint_node_name", C.SENSOR, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule(
            "component_3_demand_calculation_node_name", C.SENSOR, 1, F.UNKNOWN, False, False, None, "hand_written"
        ),
        PortRule("component_3_setpoint_node_name", C.SETPOINT, 2, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule(
            "component_4_demand_calculation_node_name", C.SENSOR, 3, F.UNKNOWN, False, False, None, "hand_written"
        ),
        PortRule("component_4_setpoint_node_name", C.SETPOINT, 4, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule(
            "component_5_demand_calculation_node_name", C.SENSOR, 5, F.UNKNOWN, False, False, None, "hand_written"
        ),
        PortRule("component_5_setpoint_node_name", C.SETPOINT, 6, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule(
            "component_6_demand_calculation_node_name", C.SENSOR, 7, F.UNKNOWN, False, False, None, "hand_written"
        ),
        PortRule("component_6_setpoint_node_name", C.SETPOINT, 8, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule(
            "component_7_demand_calculation_node_name", C.SENSOR, 9, F.UNKNOWN, False, False, None, "hand_written"
        ),
        PortRule("component_7_setpoint_node_name", C.SETPOINT, 10, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule(
            "component_8_demand_calculation_node_name", C.SENSOR, 11, F.UNKNOWN, False, False, None, "hand_written"
        ),
        PortRule("component_8_setpoint_node_name", C.SETPOINT, 12, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule(
            "component_9_demand_calculation_node_name", C.SENSOR, 13, F.UNKNOWN, False, False, None, "hand_written"
        ),
        PortRule("component_9_setpoint_node_name", C.SETPOINT, 14, F.UNKNOWN, False, False, None, "hand_written"),
    ),
    "PlantLoop": (
        PortRule("demand_side_inlet_node_name", C.INLET, 1, F.WATER, True, False, None, "eplus_examples"),
        PortRule("demand_side_outlet_node_name", C.OUTLET, 1, F.WATER, True, False, None, "eplus_examples"),
        PortRule("loop_temperature_setpoint_node_name", C.SENSOR, 1, F.WATER, True, False, None, "eplus_examples"),
        PortRule("plant_side_inlet_node_name", C.INLET, 1, F.WATER, True, False, None, "eplus_examples"),
        PortRule("plant_side_outlet_node_name", C.OUTLET, 1, F.WATER, True, False, None, "eplus_examples"),
    ),
    "Pump:ConstantSpeed": (
        PortRule("inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Pump:VariableSpeed": (
        PortRule("inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Pump:VariableSpeed:Condensate": (
        PortRule("inlet_node_name", C.INLET, 1, F.STEAM, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.STEAM, False, False, None, "eplus_examples"),
    ),
    "Refrigeration:Case": (
        PortRule("under_case_hvac_return_air_node_name", C.SENSOR, 1, F.AIR, False, False, None, "hand_written"),
    ),
    "Refrigeration:CompressorRack": (
        PortRule("condenser_air_inlet_node_name", C.OUTSIDE_AIR, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("water_cooled_condenser_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("water_cooled_condenser_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Refrigeration:Condenser:AirCooled": (
        PortRule("air_inlet_node_name_or_zone_name", C.OUTSIDE_AIR, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "Refrigeration:Condenser:EvaporativeCooled": (
        PortRule("air_inlet_node_name", C.OUTSIDE_AIR, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "Refrigeration:Condenser:WaterCooled": (
        PortRule("water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "Refrigeration:GasCooler:AirCooled": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "hand_written"),
    ),
    "SetpointManager:Coldest": (
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.AIR, False, True, None, "eplus_examples"),
    ),
    "SetpointManager:CondenserEnteringReset": (
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.WATER, False, True, None, "eplus_examples"),
    ),
    "SetpointManager:CondenserEnteringReset:Ideal": (
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.WATER, False, True, None, "eplus_examples"),
    ),
    "SetpointManager:FollowGroundTemperature": (
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.WATER, False, True, None, "eplus_examples"),
    ),
    "SetpointManager:FollowOutdoorAirTemperature": (
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.WATER, False, True, None, "eplus_examples"),
    ),
    "SetpointManager:FollowSystemNodeTemperature": (
        PortRule("reference_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_test_model"),
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.AIR, False, True, None, "eplus_test_model"),
    ),
    "SetpointManager:MixedAir": (
        PortRule("cooling_coil_inlet_node_name", C.INLET, 1, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("cooling_coil_outlet_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("fan_inlet_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("fan_outlet_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("reference_setpoint_node_name", C.SENSOR, 1, F.AIR, False, True, None, "eplus_examples"),
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.AIR, False, True, None, "eplus_examples"),
    ),
    "SetpointManager:MultiZone:Cooling:Average": (
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.AIR, False, True, None, "eplus_test_model"),
    ),
    "SetpointManager:MultiZone:Heating:Average": (
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.AIR, False, True, None, "eplus_test_model"),
    ),
    "SetpointManager:MultiZone:Humidity:Maximum": (
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.AIR, False, True, None, "eplus_examples"),
    ),
    "SetpointManager:MultiZone:Humidity:Minimum": (
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.AIR, False, True, None, "eplus_examples"),
    ),
    "SetpointManager:MultiZone:MaximumHumidity:Average": (
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.AIR, False, True, None, "eplus_examples"),
    ),
    "SetpointManager:MultiZone:MinimumHumidity:Average": (
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.AIR, False, True, None, "eplus_examples"),
    ),
    "SetpointManager:OutdoorAirPretreat": (
        PortRule("mixed_air_stream_node_name", C.SENSOR, 2, F.AIR, False, False, None, "hand_written"),
        PortRule("outdoor_air_stream_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("reference_setpoint_node_name", C.SETPOINT, 1, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("return_air_stream_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.AIR, False, True, None, "eplus_examples"),
    ),
    "SetpointManager:OutdoorAirReset": (
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.WATER, False, True, None, "eplus_examples"),
    ),
    "SetpointManager:ReturnTemperature:ChilledWater": (
        PortRule("plant_loop_supply_inlet_node", C.SENSOR, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("plant_loop_supply_outlet_node", C.SETPOINT, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "SetpointManager:ReturnTemperature:HotWater": (
        PortRule("plant_loop_supply_inlet_node", C.SENSOR, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("plant_loop_supply_outlet_node", C.SETPOINT, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "SetpointManager:Scheduled": (
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.WATER, False, True, None, "eplus_examples"),
    ),
    "SetpointManager:Scheduled:DualSetpoint": (
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.WATER, False, True, None, "eplus_examples"),
    ),
    "SetpointManager:SingleZone:Cooling": (
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.AIR, False, True, None, "eplus_examples"),
        PortRule("zone_inlet_node_name", C.SENSOR, 1, F.AIR, False, True, None, "eplus_examples"),
        PortRule("zone_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "SetpointManager:SingleZone:Heating": (
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.AIR, False, True, None, "eplus_examples"),
        PortRule("zone_inlet_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("zone_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "SetpointManager:SingleZone:Humidity:Maximum": (
        PortRule("control_zone_air_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.AIR, False, True, None, "eplus_examples"),
    ),
    "SetpointManager:SingleZone:Humidity:Minimum": (
        PortRule("control_zone_air_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.AIR, False, True, None, "eplus_examples"),
    ),
    "SetpointManager:SingleZone:OneStageCooling": (
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.AIR, False, True, None, "eplus_examples"),
    ),
    "SetpointManager:SingleZone:OneStageHeating": (
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.AIR, False, True, None, "eplus_examples"),
    ),
    "SetpointManager:SingleZone:Reheat": (
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.AIR, False, True, None, "eplus_examples"),
        PortRule("zone_inlet_node_name", C.SENSOR, 1, F.AIR, False, True, None, "eplus_examples"),
        PortRule("zone_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "SetpointManager:SystemNodeReset:Humidity": (
        PortRule("reference_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.AIR, False, True, None, "eplus_examples"),
    ),
    "SetpointManager:SystemNodeReset:Temperature": (
        PortRule("reference_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.WATER, False, True, None, "eplus_examples"),
    ),
    "SetpointManager:Warmest": (
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.AIR, False, True, None, "eplus_examples"),
    ),
    "SetpointManager:WarmestTemperatureFlow": (
        PortRule("setpoint_node_or_nodelist_name", C.SETPOINT, 1, F.AIR, False, True, None, "eplus_examples"),
    ),
    "SolarCollector:FlatPlate:PhotovoltaicThermal": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "SolarCollector:FlatPlate:Water": (
        PortRule("inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "SolarCollector:IntegralCollectorStorage": (
        PortRule("inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "SolarCollector:UnglazedTranspired": (
        PortRule("inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("setpoint_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("zone_node_name", C.SENSOR, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "SolarCollector:UnglazedTranspired:Multisystem": (
        PortRule("*.outdoor_air_system_collector_inlet_node", C.INLET, 1, F.AIR, False, False, None, "hand_written"),
        PortRule("*.outdoor_air_system_collector_outlet_node", C.OUTLET, 1, F.AIR, False, False, None, "hand_written"),
        PortRule("*.outdoor_air_system_mixed_air_node", C.OUTSIDE_AIR, 2, F.AIR, False, False, None, "hand_written"),
        PortRule("*.outdoor_air_system_zone_node", C.OUTSIDE_AIR, 3, F.AIR, False, False, None, "hand_written"),
    ),
    "SpaceHVAC:EquipmentConnections": (
        PortRule(
            "space_air_exhaust_node_or_nodelist_name", C.ZONE_EXHAUST, 1, F.AIR, False, True, None, "eplus_examples"
        ),
        PortRule("space_air_inlet_node_or_nodelist_name", C.ZONE_INLET, 1, F.AIR, False, True, None, "eplus_examples"),
        PortRule("space_air_node_name", C.ZONE_NODE, 1, F.AIR, False, False, None, "hand_written"),
        PortRule(
            "space_return_air_node_or_nodelist_name", C.ZONE_RETURN, 1, F.AIR, False, True, None, "eplus_examples"
        ),
    ),
    "SpaceHVAC:ZoneEquipmentMixer": (
        PortRule("spaces.space_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("zone_equipment_inlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "SpaceHVAC:ZoneEquipmentSplitter": (
        PortRule("spaces.space_supply_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("zone_equipment_outlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "SpaceHVAC:ZoneReturnMixer": (
        PortRule("spaces.space_return_air_node_name", C.INLET, 1, F.AIR, True, False, None, "hand_written"),
        PortRule("zone_return_air_node_name", C.OUTLET, 1, F.AIR, True, False, None, "hand_written"),
    ),
    "SurfaceProperty:LocalEnvironment": (
        PortRule("outdoor_air_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "SwimmingPool:Indoor": (
        PortRule("pool_water_inlet_node", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("pool_water_outlet_node", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "TemperingValve": (
        PortRule("inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("pump_outlet_node_name", C.SENSOR, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("stream_2_source_node_name", C.SENSOR, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("temperature_setpoint_node_name", C.SETPOINT, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "ThermalStorage:ChilledWater:Mixed": (
        PortRule(
            "ambient_temperature_outdoor_air_node_name", C.OUTSIDE_AIR, 1, F.AIR, False, False, None, "eplus_examples"
        ),
        PortRule("source_side_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("source_side_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("use_side_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("use_side_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "ThermalStorage:ChilledWater:Stratified": (
        PortRule(
            "ambient_temperature_outdoor_air_node_name", C.OUTSIDE_AIR, 3, F.AIR, False, False, None, "hand_written"
        ),
        PortRule("source_side_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("source_side_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("use_side_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("use_side_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "ThermalStorage:HotWater:Stratified": (
        PortRule(
            "ambient_temperature_outdoor_air_node_name", C.OUTSIDE_AIR, 1, F.AIR, False, False, None, "hand_written"
        ),
        PortRule("source_side_inlet_node_name", C.INLET, 3, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("source_side_outlet_node_name", C.OUTLET, 3, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("use_side_inlet_node_name", C.INLET, 2, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("use_side_outlet_node_name", C.OUTLET, 2, F.UNKNOWN, False, False, None, "hand_written"),
    ),
    "ThermalStorage:Ice:Detailed": (
        PortRule("inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "ThermalStorage:Ice:Simple": (
        PortRule("inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "ThermalStorage:PCM": (
        PortRule("plant_side_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("plant_side_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("use_side_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("use_side_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
    ),
    "WaterHeater:HeatPump:PumpedCondenser": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("condenser_water_inlet_node_name", C.INLET, 2, F.WATER, True, False, None, "eplus_examples"),
        PortRule("condenser_water_outlet_node_name", C.OUTLET, 2, F.WATER, True, False, None, "eplus_examples"),
        PortRule("exhaust_air_node_name", C.RELIEF_AIR, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("inlet_air_mixer_node_name", C.INLET, 3, F.AIR, False, False, None, "hand_written"),
        PortRule("outdoor_air_node_name", C.OUTSIDE_AIR, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("outlet_air_splitter_node_name", C.OUTLET, 3, F.AIR, False, False, None, "hand_written"),
        PortRule("tank_use_side_inlet_node_name", C.INLET, 1, F.WATER, True, False, None, "eplus_examples"),
        PortRule("tank_use_side_outlet_node_name", C.OUTLET, 1, F.WATER, True, False, None, "eplus_examples"),
    ),
    "WaterHeater:HeatPump:WrappedCondenser": (
        PortRule("air_inlet_node_name", C.INLET, 2, F.AIR, False, False, None, "hand_written"),
        PortRule("air_outlet_node_name", C.OUTLET, 2, F.AIR, False, False, None, "hand_written"),
        PortRule("exhaust_air_node_name", C.RELIEF_AIR, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("inlet_air_mixer_node_name", C.INLET, 3, F.AIR, False, False, None, "hand_written"),
        PortRule("outdoor_air_node_name", C.OUTSIDE_AIR, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("outlet_air_splitter_node_name", C.OUTLET, 3, F.AIR, False, False, None, "hand_written"),
        PortRule("tank_use_side_inlet_node_name", C.INLET, 1, F.WATER, True, False, None, "eplus_examples"),
        PortRule("tank_use_side_outlet_node_name", C.OUTLET, 1, F.WATER, True, False, None, "eplus_examples"),
    ),
    "WaterHeater:Mixed": (
        PortRule(
            "ambient_temperature_outdoor_air_node_name", C.OUTSIDE_AIR, 1, F.AIR, False, False, None, "eplus_examples"
        ),
        PortRule("source_side_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("source_side_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("use_side_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("use_side_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "WaterHeater:Stratified": (
        PortRule("ambient_temperature_outdoor_air_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("source_side_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("source_side_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("use_side_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("use_side_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "WaterUse:Connections": (
        PortRule("inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "WindowProperty:AirflowControl": (
        PortRule("airflow_return_air_node_name", C.SENSOR, 1, F.AIR, False, False, None, "hand_written"),
    ),
    "ZoneHVAC:AirDistributionUnit": (
        PortRule("air_distribution_unit_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "ZoneHVAC:Baseboard:Convective:Water": (
        PortRule("inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "ZoneHVAC:Baseboard:RadiantConvective:Steam": (
        PortRule("inlet_node_name", C.INLET, 1, F.STEAM, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.STEAM, False, False, None, "eplus_examples"),
    ),
    "ZoneHVAC:Baseboard:RadiantConvective:Water": (
        PortRule("inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "ZoneHVAC:CoolingPanel:RadiantConvective:Water": (
        PortRule("water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "ZoneHVAC:Dehumidifier:DX": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "ZoneHVAC:EquipmentConnections": (
        PortRule(
            "zone_air_exhaust_node_or_nodelist_name", C.ZONE_EXHAUST, 1, F.AIR, False, True, None, "eplus_examples"
        ),
        PortRule("zone_air_inlet_node_or_nodelist_name", C.ZONE_INLET, 1, F.AIR, False, True, None, "eplus_examples"),
        PortRule("zone_air_node_name", C.ZONE_NODE, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("zone_return_air_node_or_nodelist_name", C.ZONE_RETURN, 1, F.AIR, False, True, None, "eplus_examples"),
    ),
    "ZoneHVAC:EvaporativeCoolerUnit": (
        PortRule("cooler_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("outdoor_air_inlet_node_name", C.OUTSIDE_AIR, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("zone_relief_air_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "ZoneHVAC:ExhaustControl": (
        PortRule("inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "ZoneHVAC:ForcedAir:UserDefined": (
        PortRule("plant_connection_1_inlet_node_name", C.INLET, 3, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("plant_connection_1_outlet_node_name", C.OUTLET, 3, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("plant_connection_2_inlet_node_name", C.INLET, 4, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("plant_connection_2_outlet_node_name", C.OUTLET, 4, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("plant_connection_3_inlet_node_name", C.INLET, 5, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("plant_connection_3_outlet_node_name", C.OUTLET, 5, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("primary_air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("primary_air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("secondary_air_inlet_node_name", C.INLET, 2, F.AIR, False, False, None, "eplus_examples"),
        PortRule("secondary_air_outlet_node_name", C.OUTLET, 2, F.AIR, False, False, None, "eplus_examples"),
    ),
    "ZoneHVAC:FourPipeFanCoil": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "ZoneHVAC:HybridUnitaryHVAC": (
        PortRule("outdoor_air_node_name", C.OUTSIDE_AIR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("relief_node_name", C.RELIEF_AIR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("return_air_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("supply_air_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "ZoneHVAC:IdealLoadsAirSystem": (
        PortRule("outdoor_air_inlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("system_inlet_air_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("zone_exhaust_air_node_name", C.OUTLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("zone_supply_air_node_name", C.OUTLET, 1, F.AIR, False, True, None, "eplus_examples"),
    ),
    "ZoneHVAC:LowTemperatureRadiant:ConstantFlow": (
        PortRule("cooling_water_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("cooling_water_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("heating_water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("heating_water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "ZoneHVAC:LowTemperatureRadiant:VariableFlow": (
        PortRule("cooling_water_inlet_node_name", C.INLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("cooling_water_outlet_node_name", C.OUTLET, 2, F.WATER, False, False, None, "eplus_examples"),
        PortRule("heating_water_inlet_node_name", C.INLET, 1, F.WATER, False, False, None, "eplus_examples"),
        PortRule("heating_water_outlet_node_name", C.OUTLET, 1, F.WATER, False, False, None, "eplus_examples"),
    ),
    "ZoneHVAC:OutdoorAirUnit": (
        PortRule("airinlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("airoutlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("outdoor_air_node_name", C.OUTSIDE_AIR, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("supply_fanoutlet_node_name", C.INTERNAL, 1, F.AIR, False, False, None, "eplus_examples"),
    ),
    "ZoneHVAC:PackagedTerminalAirConditioner": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "ZoneHVAC:PackagedTerminalHeatPump": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "ZoneHVAC:RefrigerationChillerSet": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, False, False, None, "hand_written"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, False, False, None, "hand_written"),
    ),
    "ZoneHVAC:TerminalUnit:VariableRefrigerantFlow": (
        PortRule("terminal_unit_air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("terminal_unit_air_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "ZoneHVAC:UnitHeater": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "ZoneHVAC:UnitVentilator": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("outdoor_air_node_name", C.OUTSIDE_AIR, 2, F.AIR, False, False, None, "hand_written"),
    ),
    "ZoneHVAC:VentilatedSlab": (
        PortRule("cold_water_inlet_node_name", C.ACTUATOR, 1, F.WATER, True, False, None, "eplus_examples"),
        PortRule("fan_outlet_node_name", C.INTERNAL, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("hot_water_or_steam_inlet_node_name", C.ACTUATOR, 1, F.WATER, True, False, None, "eplus_examples"),
        PortRule("outdoor_air_mixer_outlet_node_name", C.OUTLET, 4, F.AIR, False, False, None, "hand_written"),
        PortRule("outdoor_air_node_name", C.OUTSIDE_AIR, 2, F.AIR, False, False, None, "hand_written"),
        PortRule("relief_air_node_name", C.RELIEF_AIR, 3, F.AIR, False, False, None, "hand_written"),
        PortRule("return_air_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("slab_in_node_name", C.INLET, 1, F.AIR, False, False, None, "eplus_examples"),
        PortRule("zone_supply_air_node_name", C.OUTLET, 1, F.AIR, False, True, None, "eplus_examples"),
    ),
    "ZoneHVAC:VentilatedSlab:SlabGroup": (
        PortRule("*.slab_inlet_node_name_for_surface", C.INLET, 1, F.UNKNOWN, False, False, None, "hand_written"),
        PortRule("*.slab_outlet_node_name_for_surface", C.OUTLET, 1, F.UNKNOWN, False, False, None, "hand_written"),
    ),
    "ZoneHVAC:WaterToAirHeatPump": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule(
            "outdoor_dry_bulb_temperature_sensor_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"
        ),
    ),
    "ZoneHVAC:WindowAirConditioner": (
        PortRule("air_inlet_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
        PortRule("air_outlet_node_name", C.OUTLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
    "ZoneProperty:LocalEnvironment": (
        PortRule("outdoor_air_node_name", C.INLET, 1, F.AIR, True, False, None, "eplus_examples"),
    ),
}
