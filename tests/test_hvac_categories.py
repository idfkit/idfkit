"""The component category table (research R-36, FR-016a).

A category comes from the object type alone. This test lists every node-bearing type the table
leaves as ``other``, so a change to the table, or a new node-bearing type in a regenerated schema,
shows up in review instead of silently changing what a category filter matches.
"""

from __future__ import annotations

from idfkit import new_document
from idfkit.hvac import ComponentCategory, HVACTopology, category_of
from idfkit.hvac._node_fields import NODE_FIELDS
from idfkit.schema import get_schema

OTHER_26_2: frozenset[str] = frozenset({
    "AirConditioner:VariableRefrigerantFlow",
    "AirLoopHVAC",
    "AirLoopHVAC:Mixer",
    "AirLoopHVAC:ReturnPath",
    "AirLoopHVAC:ReturnPlenum",
    "AirLoopHVAC:Splitter",
    "AirLoopHVAC:SupplyPath",
    "AirLoopHVAC:SupplyPlenum",
    "AirLoopHVAC:ZoneMixer",
    "AirLoopHVAC:ZoneSplitter",
    "AvailabilityManager:DifferentialThermostat",
    "AvailabilityManager:HighTemperatureTurnOff",
    "AvailabilityManager:HighTemperatureTurnOn",
    "AvailabilityManager:LowTemperatureTurnOff",
    "AvailabilityManager:LowTemperatureTurnOn",
    "Branch",
    "CentralHeatPumpSystem",
    "Coil:UserDefined",
    "Coil:WaterHeating:AirToWaterHeatPump:Pumped",
    "Coil:WaterHeating:AirToWaterHeatPump:VariableSpeed",
    "Coil:WaterHeating:AirToWaterHeatPump:Wrapped",
    "Coil:WaterHeating:Desuperheater",
    "CoilPerformance:DX:Cooling",
    "CondenserLoop",
    "Dehumidifier:Desiccant:NoFans",
    "Dehumidifier:Desiccant:System",
    "DistrictCooling",
    "DistrictHeating:Steam",
    "DistrictHeating:Water",
    "Duct",
    "ElectricEquipment:ITE:AirCooled",
    "ElectricEquipment:ITE:AirCooled:Instance",
    "EvaporativeCooler:Direct:CelDekPad",
    "EvaporativeCooler:Direct:ResearchSpecial",
    "EvaporativeCooler:Indirect:CelDekPad",
    "EvaporativeCooler:Indirect:ResearchSpecial",
    "EvaporativeCooler:Indirect:WetCoil",
    "Generator:CombustionTurbine",
    "Generator:FuelCell:AirSupply",
    "Generator:FuelCell:ExhaustGasToWaterHeatExchanger",
    "Generator:FuelCell:PowerModule",
    "Generator:FuelCell:StackCooler",
    "Generator:FuelCell:WaterSupply",
    "Generator:FuelSupply",
    "Generator:InternalCombustionEngine",
    "Generator:MicroCHP",
    "Generator:MicroTurbine",
    "GroundHeatExchanger:HorizontalTrench",
    "GroundHeatExchanger:Pond",
    "GroundHeatExchanger:Slinky",
    "GroundHeatExchanger:Surface",
    "GroundHeatExchanger:System",
    "HeatPump:AirToWater",
    "HeatPump:AirToWater:FuelFired:Cooling",
    "HeatPump:AirToWater:FuelFired:Heating",
    "HeatPump:PlantLoop:EIR:Cooling",
    "HeatPump:PlantLoop:EIR:Heating",
    "HeatPump:WaterToWater:EquationFit:Cooling",
    "HeatPump:WaterToWater:EquationFit:Heating",
    "HeatPump:WaterToWater:ParameterEstimation:Cooling",
    "HeatPump:WaterToWater:ParameterEstimation:Heating",
    "Lights",
    "Lights:Instance",
    "LoadProfile:Plant",
    "NodeList",
    "Pipe:Adiabatic",
    "Pipe:Adiabatic:Steam",
    "Pipe:Indoor",
    "Pipe:Outdoor",
    "Pipe:Underground",
    "PipingSystem:Underground:PipeCircuit",
    "PlantComponent:TemperatureSource",
    "PlantComponent:UserDefined",
    "PlantEquipmentOperation:ComponentSetpoint",
    "PlantEquipmentOperation:OutdoorDewpointDifference",
    "PlantEquipmentOperation:OutdoorDryBulbDifference",
    "PlantEquipmentOperation:OutdoorWetBulbDifference",
    "PlantEquipmentOperation:ThermalEnergyStorage",
    "PlantLoop",
    "Refrigeration:Case",
    "Refrigeration:CompressorRack",
    "Refrigeration:Condenser:AirCooled",
    "Refrigeration:Condenser:EvaporativeCooled",
    "Refrigeration:Condenser:WaterCooled",
    "Refrigeration:GasCooler:AirCooled",
    "SolarCollector:FlatPlate:PhotovoltaicThermal",
    "SolarCollector:FlatPlate:Water",
    "SolarCollector:IntegralCollectorStorage",
    "SolarCollector:UnglazedTranspired",
    "SolarCollector:UnglazedTranspired:Multisystem",
    "SpaceHVAC:EquipmentConnections",
    "SpaceHVAC:ZoneEquipmentMixer",
    "SpaceHVAC:ZoneEquipmentSplitter",
    "SpaceHVAC:ZoneReturnMixer",
    "SurfaceProperty:LocalEnvironment",
    "SwimmingPool:Indoor",
    "TemperingValve",
    "ThermalStorage:ChilledWater:Mixed",
    "ThermalStorage:ChilledWater:Stratified",
    "ThermalStorage:HotWater:Stratified",
    "ThermalStorage:Ice:Detailed",
    "ThermalStorage:Ice:Simple",
    "ThermalStorage:PCM",
    "WaterHeater:HeatPump:PumpedCondenser",
    "WaterHeater:HeatPump:WrappedCondenser",
    "WaterHeater:Mixed",
    "WaterHeater:Stratified",
    "WaterUse:Connections",
    "WindowProperty:AirflowControl",
    "ZoneProperty:LocalEnvironment",
})
"""Node-bearing types in the 26.2 schema with no category. Reviewed with the rule table."""


def test_node_bearing_types_mapped_to_other_are_the_reviewed_list() -> None:
    schema = get_schema((26, 2, 0))
    other = {t for t in NODE_FIELDS if t in schema and category_of(t) is ComponentCategory.OTHER}
    assert other == OTHER_26_2


def test_prefixes_and_exact_types() -> None:
    assert category_of("Coil:Heating:Water") is ComponentCategory.HEATING_COIL
    assert category_of("Coil:Heating:WaterToAirHeatPump:EquationFit") is ComponentCategory.HEATING_COIL
    assert category_of("Coil:Cooling:DX:SingleSpeed") is ComponentCategory.COOLING_COIL
    assert category_of("Fan:VariableVolume") is ComponentCategory.FAN
    assert category_of("HeaderedPumps:VariableSpeed") is ComponentCategory.PUMP
    assert category_of("AirTerminal:SingleDuct:VAV:Reheat") is ComponentCategory.TERMINAL_UNIT
    assert category_of("ZoneHVAC:AirDistributionUnit") is ComponentCategory.TERMINAL_UNIT
    assert category_of("ZoneHVAC:FourPipeFanCoil") is ComponentCategory.ZONE_EQUIPMENT
    assert category_of("AirLoopHVAC:UnitarySystem") is ComponentCategory.UNITARY
    assert category_of("AirLoopHVAC:OutdoorAirSystem") is ComponentCategory.OUTDOOR_AIR
    assert category_of("OutdoorAir:Mixer") is ComponentCategory.OUTDOOR_AIR
    assert category_of("CoolingTower:SingleSpeed") is ComponentCategory.HEAT_REJECTION
    assert category_of("SetpointManager:Scheduled") is ComponentCategory.SETPOINT_MANAGER
    assert category_of("Controller:WaterCoil") is ComponentCategory.CONTROLLER


def test_category_is_case_insensitive_and_unknown_types_are_other() -> None:
    assert category_of("COIL:HEATING:WATER") is ComponentCategory.HEATING_COIL
    assert category_of("NotAType:AtAll") is ComponentCategory.OTHER


def test_category_never_comes_from_names() -> None:
    doc = new_document()
    for name, node_in, node_out in (("Main Heating Coil", "A", "B"), ("Supply Fan", "B", "C")):
        doc.add(
            "Branch",
            name,
            components=[
                {
                    "component_object_type": "Pipe:Adiabatic",
                    "component_name": f"{name} Pipe",
                    "component_inlet_node_name": node_in,
                    "component_outlet_node_name": node_out,
                }
            ],
            validate=False,
        )
    topo = HVACTopology.from_document(doc)
    branch_uses = [u for node in ("A", "B", "C") for u in topo.uses(node) if u.object.object_type == "Branch"]
    assert branch_uses
    assert {u.category for u in branch_uses} == {ComponentCategory.OTHER}
