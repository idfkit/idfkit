"""Auto-generated table of fluid node fields per object type.

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_node_fields

Each entry maps an object type to ``(top-level node fields, extensible node fields)``: the union,
over every bundled schema, of the fields tagged ``"data_type": "node"`` in the 26.2 schema or named
like ``node(_or_nodelist)?_names?``, without AirflowNetwork, RoomAir, room-air model and electric
circuit nodes. A field listed here may be absent from an older schema; callers intersect with the
document's own schema.
"""

from __future__ import annotations

from typing import Final

NODE_FIELDS: Final[dict[str, tuple[tuple[str, ...], tuple[str, ...]]]] = {
    "AirConditioner:VariableRefrigerantFlow": (
        (
            "condenser_inlet_node_name",
            "condenser_outlet_node_name",
        ),
        (),
    ),
    "AirLoopHVAC": (
        (
            "supply_side_inlet_node_name",
            "demand_side_outlet_node_name",
            "demand_side_inlet_node_names",
            "supply_side_outlet_node_names",
        ),
        (),
    ),
    "AirLoopHVAC:Mixer": (
        ("outlet_node_name",),
        ("inlet_node_name",),
    ),
    "AirLoopHVAC:ReturnPath": (
        ("return_air_path_outlet_node_name",),
        (),
    ),
    "AirLoopHVAC:ReturnPlenum": (
        (
            "zone_node_name",
            "outlet_node_name",
            "induced_air_outlet_node_or_nodelist_name",
        ),
        ("inlet_node_name",),
    ),
    "AirLoopHVAC:Splitter": (
        ("inlet_node_name",),
        ("outlet_node_name",),
    ),
    "AirLoopHVAC:SupplyPath": (
        ("supply_air_path_inlet_node_name",),
        (),
    ),
    "AirLoopHVAC:SupplyPlenum": (
        (
            "zone_node_name",
            "inlet_node_name",
        ),
        ("outlet_node_name",),
    ),
    "AirLoopHVAC:Unitary:Furnace:HeatCool": (
        (
            "furnace_air_inlet_node_name",
            "furnace_air_outlet_node_name",
        ),
        (),
    ),
    "AirLoopHVAC:Unitary:Furnace:HeatOnly": (
        (
            "furnace_air_inlet_node_name",
            "furnace_air_outlet_node_name",
        ),
        (),
    ),
    "AirLoopHVAC:UnitaryHeatCool": (
        (
            "unitary_system_air_inlet_node_name",
            "unitary_system_air_outlet_node_name",
        ),
        (),
    ),
    "AirLoopHVAC:UnitaryHeatCool:VAVChangeoverBypass": (
        (
            "air_inlet_node_name",
            "bypass_duct_mixer_node_name",
            "bypass_duct_splitter_node_name",
            "air_outlet_node_name",
            "plenum_or_mixer_inlet_node_name",
        ),
        (),
    ),
    "AirLoopHVAC:UnitaryHeatOnly": (
        (
            "unitary_system_air_inlet_node_name",
            "unitary_system_air_outlet_node_name",
        ),
        (),
    ),
    "AirLoopHVAC:UnitaryHeatPump:AirToAir": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "AirLoopHVAC:UnitaryHeatPump:AirToAir:MultiSpeed": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
            "heat_recovery_water_inlet_node_name",
            "heat_recovery_water_outlet_node_name",
        ),
        (),
    ),
    "AirLoopHVAC:UnitaryHeatPump:WaterToAir": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
            "outdoor_dry_bulb_temperature_sensor_node_name",
        ),
        (),
    ),
    "AirLoopHVAC:UnitarySystem": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
            "outdoor_dry_bulb_temperature_sensor_node_name",
            "heat_recovery_water_inlet_node_name",
            "heat_recovery_water_outlet_node_name",
        ),
        (),
    ),
    "AirLoopHVAC:ZoneMixer": (
        ("outlet_node_name",),
        ("inlet_node_name",),
    ),
    "AirLoopHVAC:ZoneSplitter": (
        ("inlet_node_name",),
        ("outlet_node_name",),
    ),
    "AirTerminal:DualDuct:ConstantVolume": (
        (
            "air_outlet_node_name",
            "hot_air_inlet_node_name",
            "cold_air_inlet_node_name",
        ),
        (),
    ),
    "AirTerminal:DualDuct:VAV": (
        (
            "air_outlet_node_name",
            "hot_air_inlet_node_name",
            "cold_air_inlet_node_name",
        ),
        (),
    ),
    "AirTerminal:DualDuct:VAV:OutdoorAir": (
        (
            "air_outlet_node_name",
            "outdoor_air_inlet_node_name",
            "recirculated_air_inlet_node_name",
        ),
        (),
    ),
    "AirTerminal:SingleDuct:ConstantVolume:CooledBeam": (
        (
            "supply_air_inlet_node_name",
            "supply_air_outlet_node_name",
            "chilled_water_inlet_node_name",
            "chilled_water_outlet_node_name",
        ),
        (),
    ),
    "AirTerminal:SingleDuct:ConstantVolume:FourPipeBeam": (
        (
            "primary_air_inlet_node_name",
            "primary_air_outlet_node_name",
            "chilled_water_inlet_node_name",
            "chilled_water_outlet_node_name",
            "hot_water_inlet_node_name",
            "hot_water_outlet_node_name",
        ),
        (),
    ),
    "AirTerminal:SingleDuct:ConstantVolume:FourPipeInduction": (
        (
            "supply_air_inlet_node_name",
            "induced_air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "AirTerminal:SingleDuct:ConstantVolume:NoReheat": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "AirTerminal:SingleDuct:ConstantVolume:Reheat": (
        (
            "air_outlet_node_name",
            "air_inlet_node_name",
        ),
        (),
    ),
    "AirTerminal:SingleDuct:Mixer": (
        (
            "mixer_outlet_node_name",
            "mixer_primary_air_inlet_node_name",
            "mixer_secondary_air_inlet_node_name",
        ),
        (),
    ),
    "AirTerminal:SingleDuct:ParallelPIU:Reheat": (
        (
            "supply_air_inlet_node_name",
            "secondary_air_inlet_node_name",
            "outlet_node_name",
            "reheat_coil_air_inlet_node_name",
        ),
        (),
    ),
    "AirTerminal:SingleDuct:SeriesPIU:Reheat": (
        (
            "supply_air_inlet_node_name",
            "secondary_air_inlet_node_name",
            "outlet_node_name",
            "reheat_coil_air_inlet_node_name",
        ),
        (),
    ),
    "AirTerminal:SingleDuct:Uncontrolled": (
        ("zone_supply_air_node_name",),
        (),
    ),
    "AirTerminal:SingleDuct:UserDefined": (
        (
            "primary_air_inlet_node_name",
            "primary_air_outlet_node_name",
            "secondary_air_inlet_node_name",
            "secondary_air_outlet_node_name",
            "plant_connection_1_inlet_node_name",
            "plant_connection_1_outlet_node_name",
            "plant_connection_2_inlet_node_name",
            "plant_connection_2_outlet_node_name",
        ),
        (),
    ),
    "AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat": (
        (
            "air_outlet_node_name",
            "air_inlet_node_name",
        ),
        (),
    ),
    "AirTerminal:SingleDuct:VAV:HeatAndCool:Reheat": (
        (
            "damper_air_outlet_node_name",
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "AirTerminal:SingleDuct:VAV:NoReheat": (
        (
            "air_outlet_node_name",
            "air_inlet_node_name",
        ),
        (),
    ),
    "AirTerminal:SingleDuct:VAV:Reheat": (
        (
            "damper_air_outlet_node_name",
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "AirTerminal:SingleDuct:VAV:Reheat:VariableSpeedFan": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "AvailabilityManager:DifferentialThermostat": (
        (
            "hot_node_name",
            "cold_node_name",
        ),
        (),
    ),
    "AvailabilityManager:HighTemperatureTurnOff": (
        ("sensor_node_name",),
        (),
    ),
    "AvailabilityManager:HighTemperatureTurnOn": (
        ("sensor_node_name",),
        (),
    ),
    "AvailabilityManager:LowTemperatureTurnOff": (
        ("sensor_node_name",),
        (),
    ),
    "AvailabilityManager:LowTemperatureTurnOn": (
        ("sensor_node_name",),
        (),
    ),
    "Boiler:HotWater": (
        (
            "boiler_water_inlet_node_name",
            "boiler_water_outlet_node_name",
        ),
        (),
    ),
    "Boiler:Steam": (
        (
            "water_inlet_node_name",
            "steam_outlet_node_name",
        ),
        (),
    ),
    "Branch": (
        (),
        (
            "component_inlet_node_name",
            "component_outlet_node_name",
        ),
    ),
    "CentralHeatPumpSystem": (
        (
            "cooling_loop_inlet_node_name",
            "cooling_loop_outlet_node_name",
            "source_loop_inlet_node_name",
            "source_loop_outlet_node_name",
            "heating_loop_inlet_node_name",
            "heating_loop_outlet_node_name",
        ),
        (),
    ),
    "Chiller:Absorption": (
        (
            "chilled_water_inlet_node_name",
            "chilled_water_outlet_node_name",
            "condenser_inlet_node_name",
            "condenser_outlet_node_name",
            "generator_inlet_node_name",
            "generator_outlet_node_name",
        ),
        (),
    ),
    "Chiller:Absorption:Indirect": (
        (
            "chilled_water_inlet_node_name",
            "chilled_water_outlet_node_name",
            "condenser_inlet_node_name",
            "condenser_outlet_node_name",
            "generator_inlet_node_name",
            "generator_outlet_node_name",
        ),
        (),
    ),
    "Chiller:CombustionTurbine": (
        (
            "chilled_water_inlet_node_name",
            "chilled_water_outlet_node_name",
            "condenser_inlet_node_name",
            "condenser_outlet_node_name",
            "heat_recovery_inlet_node_name",
            "heat_recovery_outlet_node_name",
        ),
        (),
    ),
    "Chiller:ConstantCOP": (
        (
            "chilled_water_inlet_node_name",
            "chilled_water_outlet_node_name",
            "condenser_inlet_node_name",
            "condenser_outlet_node_name",
        ),
        (),
    ),
    "Chiller:Electric": (
        (
            "chilled_water_inlet_node_name",
            "chilled_water_outlet_node_name",
            "condenser_inlet_node_name",
            "condenser_outlet_node_name",
            "heat_recovery_inlet_node_name",
            "heat_recovery_outlet_node_name",
            "heat_recovery_leaving_temperature_setpoint_node_name",
        ),
        (),
    ),
    "Chiller:Electric:ASHRAE205": (
        (
            "ambient_temperature_outdoor_air_node_name",
            "chilled_water_inlet_node_name",
            "chilled_water_outlet_node_name",
            "condenser_inlet_node_name",
            "condenser_outlet_node_name",
            "oil_cooler_inlet_node_name",
            "oil_cooler_outlet_node_name",
            "auxiliary_inlet_node_name",
            "auxiliary_outlet_node_name",
            "heat_recovery_inlet_node_name",
            "heat_recovery_outlet_node_name",
        ),
        (),
    ),
    "Chiller:Electric:EIR": (
        (
            "chilled_water_inlet_node_name",
            "chilled_water_outlet_node_name",
            "condenser_inlet_node_name",
            "condenser_outlet_node_name",
            "heat_recovery_inlet_node_name",
            "heat_recovery_outlet_node_name",
            "heat_recovery_leaving_temperature_setpoint_node_name",
        ),
        (),
    ),
    "Chiller:Electric:ReformulatedEIR": (
        (
            "chilled_water_inlet_node_name",
            "chilled_water_outlet_node_name",
            "condenser_inlet_node_name",
            "condenser_outlet_node_name",
            "heat_recovery_inlet_node_name",
            "heat_recovery_outlet_node_name",
            "heat_recovery_leaving_temperature_setpoint_node_name",
        ),
        (),
    ),
    "Chiller:EngineDriven": (
        (
            "chilled_water_inlet_node_name",
            "chilled_water_outlet_node_name",
            "condenser_inlet_node_name",
            "condenser_outlet_node_name",
            "heat_recovery_inlet_node_name",
            "heat_recovery_outlet_node_name",
        ),
        (),
    ),
    "ChillerHeater:Absorption:DirectFired": (
        (
            "chilled_water_inlet_node_name",
            "chilled_water_outlet_node_name",
            "condenser_inlet_node_name",
            "condenser_outlet_node_name",
            "hot_water_inlet_node_name",
            "hot_water_outlet_node_name",
        ),
        (),
    ),
    "ChillerHeater:Absorption:DoubleEffect": (
        (
            "chilled_water_inlet_node_name",
            "chilled_water_outlet_node_name",
            "condenser_inlet_node_name",
            "condenser_outlet_node_name",
            "hot_water_inlet_node_name",
            "hot_water_outlet_node_name",
        ),
        (),
    ),
    "Coil:Cooling:DX": (
        (
            "evaporator_inlet_node_name",
            "evaporator_outlet_node_name",
            "condenser_inlet_node_name",
            "condenser_outlet_node_name",
        ),
        (),
    ),
    "Coil:Cooling:DX:MultiSpeed": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
            "condenser_air_inlet_node_name",
        ),
        (),
    ),
    "Coil:Cooling:DX:SingleSpeed": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
            "condenser_air_inlet_node_name",
        ),
        (),
    ),
    "Coil:Cooling:DX:SingleSpeed:ThermalStorage": (
        (
            "storage_tank_ambient_temperature_node_name",
            "evaporator_air_inlet_node_name",
            "evaporator_air_outlet_node_name",
            "condenser_air_inlet_node_name",
            "condenser_air_outlet_node_name",
            "storage_tank_plant_connection_inlet_node_name",
            "storage_tank_plant_connection_outlet_node_name",
        ),
        (),
    ),
    "Coil:Cooling:DX:TwoSpeed": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
            "condenser_air_inlet_node_name",
        ),
        (),
    ),
    "Coil:Cooling:DX:TwoStageWithHumidityControlMode": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "Coil:Cooling:DX:VariableRefrigerantFlow": (
        (
            "coil_air_inlet_node",
            "coil_air_outlet_node",
        ),
        (),
    ),
    "Coil:Cooling:DX:VariableRefrigerantFlow:FluidTemperatureControl": (
        (
            "coil_air_inlet_node",
            "coil_air_outlet_node",
        ),
        (),
    ),
    "Coil:Cooling:DX:VariableSpeed": (
        (
            "indoor_air_inlet_node_name",
            "indoor_air_outlet_node_name",
            "condenser_air_inlet_node_name",
        ),
        (),
    ),
    "Coil:Cooling:Water": (
        (
            "water_inlet_node_name",
            "water_outlet_node_name",
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "Coil:Cooling:Water:DetailedGeometry": (
        (
            "water_inlet_node_name",
            "water_outlet_node_name",
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "Coil:Cooling:WaterToAirHeatPump:EquationFit": (
        (
            "water_inlet_node_name",
            "water_outlet_node_name",
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "Coil:Cooling:WaterToAirHeatPump:ParameterEstimation": (
        (
            "water_inlet_node_name",
            "water_outlet_node_name",
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit": (
        (
            "water_to_refrigerant_hx_water_inlet_node_name",
            "water_to_refrigerant_hx_water_outlet_node_name",
            "indoor_air_inlet_node_name",
            "indoor_air_outlet_node_name",
        ),
        (),
    ),
    "Coil:Heating:DX:MultiSpeed": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "Coil:Heating:DX:SingleSpeed": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
            "evaporator_air_inlet_node_name",
        ),
        (),
    ),
    "Coil:Heating:DX:VariableRefrigerantFlow": (
        (
            "coil_air_inlet_node",
            "coil_air_outlet_node",
        ),
        (),
    ),
    "Coil:Heating:DX:VariableRefrigerantFlow:FluidTemperatureControl": (
        (
            "coil_air_inlet_node",
            "coil_air_outlet_node",
        ),
        (),
    ),
    "Coil:Heating:DX:VariableSpeed": (
        (
            "indoor_air_inlet_node_name",
            "indoor_air_outlet_node_name",
        ),
        (),
    ),
    "Coil:Heating:Desuperheater": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
            "temperature_setpoint_node_name",
        ),
        (),
    ),
    "Coil:Heating:Electric": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
            "temperature_setpoint_node_name",
        ),
        (),
    ),
    "Coil:Heating:Electric:MultiStage": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
            "temperature_setpoint_node_name",
        ),
        (),
    ),
    "Coil:Heating:Fuel": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
            "temperature_setpoint_node_name",
        ),
        (),
    ),
    "Coil:Heating:Gas:MultiStage": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
            "temperature_setpoint_node_name",
        ),
        (),
    ),
    "Coil:Heating:Steam": (
        (
            "water_inlet_node_name",
            "water_outlet_node_name",
            "air_inlet_node_name",
            "air_outlet_node_name",
            "temperature_setpoint_node_name",
        ),
        (),
    ),
    "Coil:Heating:Water": (
        (
            "water_inlet_node_name",
            "water_outlet_node_name",
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "Coil:Heating:WaterToAirHeatPump:EquationFit": (
        (
            "water_inlet_node_name",
            "water_outlet_node_name",
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "Coil:Heating:WaterToAirHeatPump:ParameterEstimation": (
        (
            "water_inlet_node_name",
            "water_outlet_node_name",
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "Coil:Heating:WaterToAirHeatPump:VariableSpeedEquationFit": (
        (
            "water_to_refrigerant_hx_water_inlet_node_name",
            "water_to_refrigerant_hx_water_outlet_node_name",
            "indoor_air_inlet_node_name",
            "indoor_air_outlet_node_name",
        ),
        (),
    ),
    "Coil:UserDefined": (
        (
            "air_connection_1_inlet_node_name",
            "air_connection_1_outlet_node_name",
            "air_connection_2_inlet_node_name",
            "air_connection_2_outlet_node_name",
            "plant_connection_inlet_node_name",
            "plant_connection_outlet_node_name",
        ),
        (),
    ),
    "Coil:WaterHeating:AirToWaterHeatPump:Pumped": (
        (
            "evaporator_air_inlet_node_name",
            "evaporator_air_outlet_node_name",
            "condenser_water_inlet_node_name",
            "condenser_water_outlet_node_name",
        ),
        (),
    ),
    "Coil:WaterHeating:AirToWaterHeatPump:VariableSpeed": (
        (
            "evaporator_air_inlet_node_name",
            "evaporator_air_outlet_node_name",
            "condenser_water_inlet_node_name",
            "condenser_water_outlet_node_name",
        ),
        (),
    ),
    "Coil:WaterHeating:AirToWaterHeatPump:Wrapped": (
        (
            "evaporator_air_inlet_node_name",
            "evaporator_air_outlet_node_name",
        ),
        (),
    ),
    "Coil:WaterHeating:Desuperheater": (
        (
            "water_inlet_node_name",
            "water_outlet_node_name",
        ),
        (),
    ),
    "CoilPerformance:DX:Cooling": (
        ("condenser_air_inlet_node_name",),
        (),
    ),
    "CoilSystem:Cooling:DX": (
        (
            "dx_cooling_coil_system_inlet_node_name",
            "dx_cooling_coil_system_outlet_node_name",
            "dx_cooling_coil_system_sensor_node_name",
        ),
        (),
    ),
    "CoilSystem:Cooling:Water": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "CoilSystem:IntegratedHeatPump:AirSource": (
        ("supply_hot_water_flow_sensor_node_name",),
        (),
    ),
    "CondenserLoop": (
        (
            "condenser_loop_temperature_setpoint_node_name",
            "condenser_side_inlet_node_name",
            "condenser_side_outlet_node_name",
            "demand_side_inlet_node_name",
            "demand_side_outlet_node_name",
        ),
        (),
    ),
    "Controller:OutdoorAir": (
        (
            "relief_air_outlet_node_name",
            "return_air_node_name",
            "mixed_air_node_name",
            "actuator_node_name",
        ),
        (),
    ),
    "Controller:WaterCoil": (
        (
            "sensor_node_name",
            "actuator_node_name",
        ),
        (),
    ),
    "CoolingTower:SingleSpeed": (
        (
            "water_inlet_node_name",
            "water_outlet_node_name",
            "outdoor_air_inlet_node_name",
        ),
        (),
    ),
    "CoolingTower:TwoSpeed": (
        (
            "water_inlet_node_name",
            "water_outlet_node_name",
            "outdoor_air_inlet_node_name",
        ),
        (),
    ),
    "CoolingTower:VariableSpeed": (
        (
            "water_inlet_node_name",
            "water_outlet_node_name",
            "outdoor_air_inlet_node_name",
        ),
        (),
    ),
    "CoolingTower:VariableSpeed:Merkel": (
        (
            "water_inlet_node_name",
            "water_outlet_node_name",
            "outdoor_air_inlet_node_name",
        ),
        (),
    ),
    "Dehumidifier:Desiccant:NoFans": (
        (
            "process_air_inlet_node_name",
            "process_air_outlet_node_name",
            "regeneration_air_inlet_node_name",
            "regeneration_fan_inlet_node_name",
        ),
        (),
    ),
    "Dehumidifier:Desiccant:System": (
        ("sensor_node_name",),
        (),
    ),
    "DistrictCooling": (
        (
            "chilled_water_inlet_node_name",
            "chilled_water_outlet_node_name",
        ),
        (),
    ),
    "DistrictHeating": (
        (
            "hot_water_inlet_node_name",
            "hot_water_outlet_node_name",
        ),
        (),
    ),
    "DistrictHeating:Steam": (
        (
            "steam_inlet_node_name",
            "steam_outlet_node_name",
        ),
        (),
    ),
    "DistrictHeating:Water": (
        (
            "hot_water_inlet_node_name",
            "hot_water_outlet_node_name",
        ),
        (),
    ),
    "Duct": (
        (
            "inlet_node_name",
            "outlet_node_name",
        ),
        (),
    ),
    "ElectricEquipment:ITE:AirCooled": (
        ("supply_air_node_name",),
        (),
    ),
    "ElectricEquipment:ITE:AirCooled:Instance": (
        ("supply_air_node_name",),
        (),
    ),
    "EvaporativeCooler:Direct:CelDekPad": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "EvaporativeCooler:Direct:ResearchSpecial": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
            "sensor_node_name",
        ),
        (),
    ),
    "EvaporativeCooler:Indirect:CelDekPad": (
        (
            "primary_air_inlet_node_name",
            "primary_air_outlet_node_name",
            "secondary_air_inlet_node_name",
        ),
        (),
    ),
    "EvaporativeCooler:Indirect:ResearchSpecial": (
        (
            "primary_air_inlet_node_name",
            "primary_air_outlet_node_name",
            "secondary_air_inlet_node_name",
            "secondary_air_outlet_node_name",
            "sensor_node_name",
            "relief_air_inlet_node_name",
        ),
        (),
    ),
    "EvaporativeCooler:Indirect:WetCoil": (
        (
            "primary_air_inlet_node_name",
            "primary_air_outlet_node_name",
            "secondary_air_inlet_node_name",
        ),
        (),
    ),
    "EvaporativeFluidCooler:SingleSpeed": (
        (
            "water_inlet_node_name",
            "water_outlet_node_name",
            "outdoor_air_inlet_node_name",
        ),
        (),
    ),
    "EvaporativeFluidCooler:TwoSpeed": (
        (
            "water_inlet_node_name",
            "water_outlet_node_name",
            "outdoor_air_inlet_node_name",
        ),
        (),
    ),
    "Fan:ComponentModel": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "Fan:ConstantVolume": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "Fan:OnOff": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "Fan:SystemModel": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "Fan:VariableVolume": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "Fan:ZoneExhaust": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "FluidCooler:SingleSpeed": (
        (
            "water_inlet_node_name",
            "water_outlet_node_name",
            "outdoor_air_inlet_node_name",
        ),
        (),
    ),
    "FluidCooler:TwoSpeed": (
        (
            "water_inlet_node_name",
            "water_outlet_node_name",
            "outdoor_air_inlet_node_name",
        ),
        (),
    ),
    "Generator:CombustionTurbine": (
        (
            "heat_recovery_inlet_node_name",
            "heat_recovery_outlet_node_name",
            "outdoor_air_inlet_node_name",
        ),
        (),
    ),
    "Generator:FuelCell:AirSupply": (
        ("air_inlet_node_name",),
        (),
    ),
    "Generator:FuelCell:ExhaustGasToWaterHeatExchanger": (
        (
            "heat_recovery_water_inlet_node_name",
            "heat_recovery_water_outlet_node_name",
            "exhaust_outlet_air_node_name",
        ),
        (),
    ),
    "Generator:FuelCell:PowerModule": (
        (
            "dilution_inlet_air_node_name",
            "dilution_outlet_air_node_name",
        ),
        (),
    ),
    "Generator:FuelCell:StackCooler": (
        (
            "heat_recovery_water_inlet_node_name",
            "heat_recovery_water_outlet_node_name",
        ),
        (),
    ),
    "Generator:FuelCell:WaterSupply": (
        ("water_temperature_reference_node_name",),
        (),
    ),
    "Generator:FuelSupply": (
        ("fuel_temperature_reference_node_name",),
        (),
    ),
    "Generator:InternalCombustionEngine": (
        (
            "heat_recovery_inlet_node_name",
            "heat_recovery_outlet_node_name",
        ),
        (),
    ),
    "Generator:MicroCHP": (
        (
            "cooling_water_inlet_node_name",
            "cooling_water_outlet_node_name",
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "Generator:MicroTurbine": (
        (
            "heat_recovery_water_inlet_node_name",
            "heat_recovery_water_outlet_node_name",
            "combustion_air_inlet_node_name",
            "combustion_air_outlet_node_name",
        ),
        (),
    ),
    "GroundHeatExchanger:HorizontalTrench": (
        (
            "inlet_node_name",
            "outlet_node_name",
        ),
        (),
    ),
    "GroundHeatExchanger:Pond": (
        (
            "fluid_inlet_node_name",
            "fluid_outlet_node_name",
        ),
        (),
    ),
    "GroundHeatExchanger:Slinky": (
        (
            "inlet_node_name",
            "outlet_node_name",
        ),
        (),
    ),
    "GroundHeatExchanger:Surface": (
        (
            "fluid_inlet_node_name",
            "fluid_outlet_node_name",
        ),
        (),
    ),
    "GroundHeatExchanger:System": (
        (
            "inlet_node_name",
            "outlet_node_name",
        ),
        (),
    ),
    "HeaderedPumps:ConstantSpeed": (
        (
            "inlet_node_name",
            "outlet_node_name",
        ),
        (),
    ),
    "HeaderedPumps:VariableSpeed": (
        (
            "inlet_node_name",
            "outlet_node_name",
        ),
        (),
    ),
    "HeatExchanger:AirToAir:FlatPlate": (
        (
            "supply_air_inlet_node_name",
            "supply_air_outlet_node_name",
            "secondary_air_inlet_node_name",
            "secondary_air_outlet_node_name",
        ),
        (),
    ),
    "HeatExchanger:AirToAir:SensibleAndLatent": (
        (
            "supply_air_inlet_node_name",
            "supply_air_outlet_node_name",
            "exhaust_air_inlet_node_name",
            "exhaust_air_outlet_node_name",
        ),
        (),
    ),
    "HeatExchanger:Desiccant:BalancedFlow": (
        (
            "regeneration_air_inlet_node_name",
            "regeneration_air_outlet_node_name",
            "process_air_inlet_node_name",
            "process_air_outlet_node_name",
        ),
        (),
    ),
    "HeatExchanger:FluidToFluid": (
        (
            "loop_demand_side_inlet_node_name",
            "loop_demand_side_outlet_node_name",
            "loop_supply_side_inlet_node_name",
            "loop_supply_side_outlet_node_name",
            "heat_exchanger_setpoint_node_name",
            "component_override_loop_supply_side_inlet_node_name",
            "component_override_loop_demand_side_inlet_node_name",
        ),
        (),
    ),
    "HeatPump:AirToWater": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
            "hot_water_inlet_node_name",
            "hot_water_outlet_node_name",
            "chilled_water_inlet_node_name",
            "chilled_water_outlet_node_name",
        ),
        (),
    ),
    "HeatPump:AirToWater:FuelFired:Cooling": (
        (
            "water_inlet_node_name",
            "water_outlet_node_name",
            "air_source_node_name",
        ),
        (),
    ),
    "HeatPump:AirToWater:FuelFired:Heating": (
        (
            "water_inlet_node_name",
            "water_outlet_node_name",
            "air_source_node_name",
        ),
        (),
    ),
    "HeatPump:PlantLoop:EIR:Cooling": (
        (
            "load_side_inlet_node_name",
            "load_side_outlet_node_name",
            "source_side_inlet_node_name",
            "source_side_outlet_node_name",
            "heat_recovery_inlet_node_name",
            "heat_recovery_outlet_node_name",
        ),
        (),
    ),
    "HeatPump:PlantLoop:EIR:Heating": (
        (
            "load_side_inlet_node_name",
            "load_side_outlet_node_name",
            "source_side_inlet_node_name",
            "source_side_outlet_node_name",
            "heat_recovery_inlet_node_name",
            "heat_recovery_outlet_node_name",
        ),
        (),
    ),
    "HeatPump:WaterToWater:EIR:Cooling": (
        (
            "source_side_outlet_node_name",
            "load_side_inlet_node_name",
            "source_side_inlet_node_name",
            "load_side_outlet_node_name",
        ),
        (),
    ),
    "HeatPump:WaterToWater:EIR:Heating": (
        (
            "source_side_outlet_node_name",
            "load_side_inlet_node_name",
            "source_side_inlet_node_name",
            "load_side_outlet_node_name",
        ),
        (),
    ),
    "HeatPump:WaterToWater:EquationFit:Cooling": (
        (
            "source_side_inlet_node_name",
            "source_side_outlet_node_name",
            "load_side_inlet_node_name",
            "load_side_outlet_node_name",
        ),
        (),
    ),
    "HeatPump:WaterToWater:EquationFit:Heating": (
        (
            "source_side_inlet_node_name",
            "source_side_outlet_node_name",
            "load_side_inlet_node_name",
            "load_side_outlet_node_name",
        ),
        (),
    ),
    "HeatPump:WaterToWater:ParameterEstimation:Cooling": (
        (
            "source_side_inlet_node_name",
            "source_side_outlet_node_name",
            "load_side_inlet_node_name",
            "load_side_outlet_node_name",
        ),
        (),
    ),
    "HeatPump:WaterToWater:ParameterEstimation:Heating": (
        (
            "source_side_inlet_node_name",
            "source_side_outlet_node_name",
            "load_side_inlet_node_name",
            "load_side_outlet_node_name",
        ),
        (),
    ),
    "Humidifier:Steam:Electric": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "Humidifier:Steam:Gas": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "Lights": (
        (
            "return_air_heat_gain_node_name",
            "exhaust_air_heat_gain_node_name",
        ),
        (),
    ),
    "Lights:Instance": (
        (
            "return_air_heat_gain_node_name",
            "exhaust_air_heat_gain_node_name",
        ),
        (),
    ),
    "LoadProfile:Plant": (
        (
            "inlet_node_name",
            "outlet_node_name",
        ),
        (),
    ),
    "NodeList": (
        (),
        ("node_name",),
    ),
    "OutdoorAir:Mixer": (
        (
            "mixed_air_node_name",
            "outdoor_air_stream_node_name",
            "relief_air_stream_node_name",
            "return_air_stream_node_name",
        ),
        (),
    ),
    "OutdoorAir:NodeList": (
        (),
        ("node_or_nodelist_name",),
    ),
    "Pipe:Adiabatic": (
        (
            "inlet_node_name",
            "outlet_node_name",
        ),
        (),
    ),
    "Pipe:Adiabatic:Steam": (
        (
            "inlet_node_name",
            "outlet_node_name",
        ),
        (),
    ),
    "Pipe:Indoor": (
        (
            "fluid_inlet_node_name",
            "fluid_outlet_node_name",
        ),
        (),
    ),
    "Pipe:Outdoor": (
        (
            "fluid_inlet_node_name",
            "fluid_outlet_node_name",
            "ambient_temperature_outdoor_air_node_name",
        ),
        (),
    ),
    "Pipe:Underground": (
        (
            "fluid_inlet_node_name",
            "fluid_outlet_node_name",
        ),
        (),
    ),
    "PipingSystem:Underground:PipeCircuit": (
        (
            "circuit_inlet_node",
            "circuit_outlet_node",
        ),
        (),
    ),
    "PlantComponent:TemperatureSource": (
        (
            "inlet_node",
            "outlet_node",
        ),
        (),
    ),
    "PlantComponent:UserDefined": (
        (
            "plant_connection_1_inlet_node_name",
            "plant_connection_1_outlet_node_name",
            "plant_connection_2_inlet_node_name",
            "plant_connection_2_outlet_node_name",
            "plant_connection_3_inlet_node_name",
            "plant_connection_3_outlet_node_name",
            "plant_connection_4_inlet_node_name",
            "plant_connection_4_outlet_node_name",
            "air_connection_inlet_node_name",
            "air_connection_outlet_node_name",
        ),
        (),
    ),
    "PlantEquipmentOperation:ComponentSetpoint": (
        (
            "demand_calculation_1_node_name",
            "setpoint_1_node_name",
            "demand_calculation_2_node_name",
            "setpoint_2_node_name",
            "demand_calculation_3_node_name",
            "setpoint_3_node_name",
            "demand_calculation_4_node_name",
            "setpoint_4_node_name",
            "demand_calculation_5_node_name",
            "setpoint_5_node_name",
            "demand_calculation_6_node_name",
            "setpoint_6_node_name",
            "demand_calculation_7_node_name",
            "setpoint_7_node_name",
            "demand_calculation_8_node_name",
            "setpoint_8_node_name",
            "demand_calculation_9_node_name",
            "setpoint_9_node_name",
            "demand_calculation_10_node_name",
            "setpoint_10_node_name",
        ),
        (),
    ),
    "PlantEquipmentOperation:OutdoorDewpointDifference": (
        ("reference_temperature_node_name",),
        (),
    ),
    "PlantEquipmentOperation:OutdoorDryBulbDifference": (
        ("reference_temperature_node_name",),
        (),
    ),
    "PlantEquipmentOperation:OutdoorWetBulbDifference": (
        ("reference_temperature_node_name",),
        (),
    ),
    "PlantEquipmentOperation:ThermalEnergyStorage": (
        (
            "component_1_demand_calculation_node_name",
            "component_1_setpoint_node_name",
            "component_2_demand_calculation_node_name",
            "component_2_setpoint_node_name",
            "component_3_demand_calculation_node_name",
            "component_3_setpoint_node_name",
            "component_4_demand_calculation_node_name",
            "component_4_setpoint_node_name",
            "component_5_demand_calculation_node_name",
            "component_5_setpoint_node_name",
            "component_6_demand_calculation_node_name",
            "component_6_setpoint_node_name",
            "component_7_demand_calculation_node_name",
            "component_7_setpoint_node_name",
            "component_8_demand_calculation_node_name",
            "component_8_setpoint_node_name",
            "component_9_demand_calculation_node_name",
            "component_9_setpoint_node_name",
            "component_10_demand_calculation_node_name",
            "component_10_setpoint_node_name",
        ),
        (),
    ),
    "PlantLoop": (
        (
            "loop_temperature_setpoint_node_name",
            "plant_side_inlet_node_name",
            "plant_side_outlet_node_name",
            "demand_side_inlet_node_name",
            "demand_side_outlet_node_name",
        ),
        (),
    ),
    "Pump:ConstantSpeed": (
        (
            "inlet_node_name",
            "outlet_node_name",
        ),
        (),
    ),
    "Pump:VariableSpeed": (
        (
            "inlet_node_name",
            "outlet_node_name",
        ),
        (),
    ),
    "Pump:VariableSpeed:Condensate": (
        (
            "inlet_node_name",
            "outlet_node_name",
        ),
        (),
    ),
    "Refrigeration:Case": (
        ("under_case_hvac_return_air_node_name",),
        (),
    ),
    "Refrigeration:CompressorRack": (
        (
            "water_cooled_condenser_inlet_node_name",
            "water_cooled_condenser_outlet_node_name",
            "condenser_air_inlet_node_name",
        ),
        (),
    ),
    "Refrigeration:Condenser:AirCooled": (
        ("air_inlet_node_name_or_zone_name",),
        (),
    ),
    "Refrigeration:Condenser:EvaporativeCooled": (
        ("air_inlet_node_name",),
        (),
    ),
    "Refrigeration:Condenser:WaterCooled": (
        (
            "water_inlet_node_name",
            "water_outlet_node_name",
        ),
        (),
    ),
    "Refrigeration:GasCooler:AirCooled": (
        ("air_inlet_node_name",),
        (),
    ),
    "SetpointManager:Coldest": (
        ("setpoint_node_or_nodelist_name",),
        (),
    ),
    "SetpointManager:CondenserEnteringReset": (
        ("setpoint_node_or_nodelist_name",),
        (),
    ),
    "SetpointManager:CondenserEnteringReset:Ideal": (
        ("setpoint_node_or_nodelist_name",),
        (),
    ),
    "SetpointManager:FollowGroundTemperature": (
        ("setpoint_node_or_nodelist_name",),
        (),
    ),
    "SetpointManager:FollowOutdoorAirTemperature": (
        ("setpoint_node_or_nodelist_name",),
        (),
    ),
    "SetpointManager:FollowSystemNodeTemperature": (
        (
            "reference_node_name",
            "setpoint_node_or_nodelist_name",
        ),
        (),
    ),
    "SetpointManager:MixedAir": (
        (
            "reference_setpoint_node_name",
            "fan_inlet_node_name",
            "fan_outlet_node_name",
            "setpoint_node_or_nodelist_name",
            "cooling_coil_inlet_node_name",
            "cooling_coil_outlet_node_name",
        ),
        (),
    ),
    "SetpointManager:MultiZone:Cooling:Average": (
        ("setpoint_node_or_nodelist_name",),
        (),
    ),
    "SetpointManager:MultiZone:Heating:Average": (
        ("setpoint_node_or_nodelist_name",),
        (),
    ),
    "SetpointManager:MultiZone:Humidity:Maximum": (
        ("setpoint_node_or_nodelist_name",),
        (),
    ),
    "SetpointManager:MultiZone:Humidity:Minimum": (
        ("setpoint_node_or_nodelist_name",),
        (),
    ),
    "SetpointManager:MultiZone:MaximumHumidity:Average": (
        ("setpoint_node_or_nodelist_name",),
        (),
    ),
    "SetpointManager:MultiZone:MinimumHumidity:Average": (
        ("setpoint_node_or_nodelist_name",),
        (),
    ),
    "SetpointManager:OutdoorAirPretreat": (
        (
            "reference_setpoint_node_name",
            "mixed_air_stream_node_name",
            "outdoor_air_stream_node_name",
            "return_air_stream_node_name",
            "setpoint_node_or_nodelist_name",
        ),
        (),
    ),
    "SetpointManager:OutdoorAirReset": (
        ("setpoint_node_or_nodelist_name",),
        (),
    ),
    "SetpointManager:ReturnTemperature:ChilledWater": (
        (
            "plant_loop_supply_outlet_node",
            "plant_loop_supply_inlet_node",
        ),
        (),
    ),
    "SetpointManager:ReturnTemperature:HotWater": (
        (
            "plant_loop_supply_outlet_node",
            "plant_loop_supply_inlet_node",
        ),
        (),
    ),
    "SetpointManager:Scheduled": (
        ("setpoint_node_or_nodelist_name",),
        (),
    ),
    "SetpointManager:Scheduled:DualSetpoint": (
        ("setpoint_node_or_nodelist_name",),
        (),
    ),
    "SetpointManager:SingleZone:Cooling": (
        (
            "zone_node_name",
            "zone_inlet_node_name",
            "setpoint_node_or_nodelist_name",
        ),
        (),
    ),
    "SetpointManager:SingleZone:Heating": (
        (
            "zone_node_name",
            "zone_inlet_node_name",
            "setpoint_node_or_nodelist_name",
        ),
        (),
    ),
    "SetpointManager:SingleZone:Humidity:Maximum": (
        (
            "setpoint_node_or_nodelist_name",
            "control_zone_air_node_name",
        ),
        (),
    ),
    "SetpointManager:SingleZone:Humidity:Minimum": (
        (
            "setpoint_node_or_nodelist_name",
            "control_zone_air_node_name",
        ),
        (),
    ),
    "SetpointManager:SingleZone:OneStageCooling": (
        ("setpoint_node_or_nodelist_name",),
        (),
    ),
    "SetpointManager:SingleZone:OneStageHeating": (
        ("setpoint_node_or_nodelist_name",),
        (),
    ),
    "SetpointManager:SingleZone:Reheat": (
        (
            "zone_node_name",
            "zone_inlet_node_name",
            "setpoint_node_or_nodelist_name",
        ),
        (),
    ),
    "SetpointManager:SystemNodeReset:Humidity": (
        (
            "reference_node_name",
            "setpoint_node_or_nodelist_name",
        ),
        (),
    ),
    "SetpointManager:SystemNodeReset:Temperature": (
        (
            "reference_node_name",
            "setpoint_node_or_nodelist_name",
        ),
        (),
    ),
    "SetpointManager:Warmest": (
        ("setpoint_node_or_nodelist_name",),
        (),
    ),
    "SetpointManager:WarmestTemperatureFlow": (
        ("setpoint_node_or_nodelist_name",),
        (),
    ),
    "SolarCollector:FlatPlate:PhotovoltaicThermal": (
        (
            "water_inlet_node_name",
            "water_outlet_node_name",
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "SolarCollector:FlatPlate:Water": (
        (
            "inlet_node_name",
            "outlet_node_name",
        ),
        (),
    ),
    "SolarCollector:IntegralCollectorStorage": (
        (
            "inlet_node_name",
            "outlet_node_name",
        ),
        (),
    ),
    "SolarCollector:UnglazedTranspired": (
        (
            "inlet_node_name",
            "outlet_node_name",
            "setpoint_node_name",
            "zone_node_name",
        ),
        (),
    ),
    "SolarCollector:UnglazedTranspired:Multisystem": (
        (),
        (
            "outdoor_air_system_collector_inlet_node",
            "outdoor_air_system_collector_outlet_node",
            "outdoor_air_system_mixed_air_node",
            "outdoor_air_system_zone_node",
        ),
    ),
    "SpaceHVAC:EquipmentConnections": (
        (
            "space_air_inlet_node_or_nodelist_name",
            "space_air_exhaust_node_or_nodelist_name",
            "space_air_node_name",
            "space_return_air_node_or_nodelist_name",
            "space_return_air_node_1_flow_rate_basis_node_or_nodelist_name",
        ),
        (),
    ),
    "SpaceHVAC:ZoneEquipmentMixer": (
        ("zone_equipment_inlet_node_name",),
        ("space_node_name",),
    ),
    "SpaceHVAC:ZoneEquipmentSplitter": (
        ("zone_equipment_outlet_node_name",),
        ("space_supply_node_name",),
    ),
    "SpaceHVAC:ZoneReturnMixer": (
        ("zone_return_air_node_name",),
        ("space_return_air_node_name",),
    ),
    "SurfaceProperty:LocalEnvironment": (
        ("outdoor_air_node_name",),
        (),
    ),
    "SwimmingPool:Indoor": (
        (
            "pool_water_inlet_node",
            "pool_water_outlet_node",
        ),
        (),
    ),
    "TemperingValve": (
        (
            "inlet_node_name",
            "outlet_node_name",
            "stream_2_source_node_name",
            "temperature_setpoint_node_name",
            "pump_outlet_node_name",
        ),
        (),
    ),
    "ThermalStorage:ChilledWater:Mixed": (
        (
            "ambient_temperature_outdoor_air_node_name",
            "use_side_inlet_node_name",
            "use_side_outlet_node_name",
            "source_side_inlet_node_name",
            "source_side_outlet_node_name",
        ),
        (),
    ),
    "ThermalStorage:ChilledWater:Stratified": (
        (
            "ambient_temperature_outdoor_air_node_name",
            "use_side_inlet_node_name",
            "use_side_outlet_node_name",
            "source_side_inlet_node_name",
            "source_side_outlet_node_name",
        ),
        (),
    ),
    "ThermalStorage:HotWater:Stratified": (
        (
            "ambient_temperature_outdoor_air_node_name",
            "use_side_inlet_node_name",
            "use_side_outlet_node_name",
            "source_side_inlet_node_name",
            "source_side_outlet_node_name",
        ),
        (),
    ),
    "ThermalStorage:Ice:Detailed": (
        (
            "inlet_node_name",
            "outlet_node_name",
        ),
        (),
    ),
    "ThermalStorage:Ice:Simple": (
        (
            "inlet_node_name",
            "outlet_node_name",
        ),
        (),
    ),
    "ThermalStorage:PCM": (
        (
            "plant_side_inlet_node_name",
            "plant_side_outlet_node_name",
            "use_side_inlet_node_name",
            "use_side_outlet_node_name",
        ),
        (),
    ),
    "WaterHeater:HeatPump:PumpedCondenser": (
        (
            "condenser_water_inlet_node_name",
            "condenser_water_outlet_node_name",
            "air_inlet_node_name",
            "air_outlet_node_name",
            "outdoor_air_node_name",
            "exhaust_air_node_name",
            "tank_use_side_inlet_node_name",
            "tank_use_side_outlet_node_name",
            "inlet_air_mixer_node_name",
            "outlet_air_splitter_node_name",
        ),
        (),
    ),
    "WaterHeater:HeatPump:WrappedCondenser": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
            "outdoor_air_node_name",
            "exhaust_air_node_name",
            "tank_use_side_inlet_node_name",
            "tank_use_side_outlet_node_name",
            "inlet_air_mixer_node_name",
            "outlet_air_splitter_node_name",
        ),
        (),
    ),
    "WaterHeater:Mixed": (
        (
            "ambient_temperature_outdoor_air_node_name",
            "use_side_inlet_node_name",
            "use_side_outlet_node_name",
            "source_side_inlet_node_name",
            "source_side_outlet_node_name",
        ),
        (),
    ),
    "WaterHeater:Stratified": (
        (
            "ambient_temperature_outdoor_air_node_name",
            "use_side_inlet_node_name",
            "use_side_outlet_node_name",
            "source_side_inlet_node_name",
            "source_side_outlet_node_name",
        ),
        (),
    ),
    "WaterUse:Connections": (
        (
            "inlet_node_name",
            "outlet_node_name",
        ),
        (),
    ),
    "WindowProperty:AirflowControl": (
        ("airflow_return_air_node_name",),
        (),
    ),
    "ZoneHVAC:AirDistributionUnit": (
        ("air_distribution_unit_outlet_node_name",),
        (),
    ),
    "ZoneHVAC:Baseboard:Convective:Water": (
        (
            "inlet_node_name",
            "outlet_node_name",
        ),
        (),
    ),
    "ZoneHVAC:Baseboard:RadiantConvective:Steam": (
        (
            "inlet_node_name",
            "outlet_node_name",
        ),
        (),
    ),
    "ZoneHVAC:Baseboard:RadiantConvective:Water": (
        (
            "inlet_node_name",
            "outlet_node_name",
        ),
        (),
    ),
    "ZoneHVAC:CoolingPanel:RadiantConvective:Water": (
        (
            "water_inlet_node_name",
            "water_outlet_node_name",
        ),
        (),
    ),
    "ZoneHVAC:Dehumidifier:DX": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "ZoneHVAC:EquipmentConnections": (
        (
            "zone_air_inlet_node_or_nodelist_name",
            "zone_air_exhaust_node_or_nodelist_name",
            "zone_air_node_name",
            "zone_return_air_node_or_nodelist_name",
            "zone_return_air_node_1_flow_rate_basis_node_or_nodelist_name",
        ),
        (),
    ),
    "ZoneHVAC:EvaporativeCoolerUnit": (
        (
            "outdoor_air_inlet_node_name",
            "cooler_outlet_node_name",
            "zone_relief_air_node_name",
        ),
        (),
    ),
    "ZoneHVAC:ExhaustControl": (
        (
            "inlet_node_name",
            "outlet_node_name",
            "supply_node_or_nodelist_name",
        ),
        (),
    ),
    "ZoneHVAC:ForcedAir:UserDefined": (
        (
            "primary_air_inlet_node_name",
            "primary_air_outlet_node_name",
            "secondary_air_inlet_node_name",
            "secondary_air_outlet_node_name",
            "plant_connection_1_inlet_node_name",
            "plant_connection_1_outlet_node_name",
            "plant_connection_2_inlet_node_name",
            "plant_connection_2_outlet_node_name",
            "plant_connection_3_inlet_node_name",
            "plant_connection_3_outlet_node_name",
        ),
        (),
    ),
    "ZoneHVAC:FourPipeFanCoil": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "ZoneHVAC:HybridUnitaryHVAC": (
        (
            "return_air_node_name",
            "outdoor_air_node_name",
            "supply_air_node_name",
            "relief_node_name",
        ),
        (),
    ),
    "ZoneHVAC:IdealLoadsAirSystem": (
        (
            "zone_supply_air_node_name",
            "zone_exhaust_air_node_name",
            "system_inlet_air_node_name",
            "outdoor_air_inlet_node_name",
        ),
        (),
    ),
    "ZoneHVAC:LowTemperatureRadiant:ConstantFlow": (
        (
            "heating_water_inlet_node_name",
            "heating_water_outlet_node_name",
            "cooling_water_inlet_node_name",
            "cooling_water_outlet_node_name",
        ),
        (),
    ),
    "ZoneHVAC:LowTemperatureRadiant:VariableFlow": (
        (
            "heating_water_inlet_node_name",
            "heating_water_outlet_node_name",
            "cooling_water_inlet_node_name",
            "cooling_water_outlet_node_name",
        ),
        (),
    ),
    "ZoneHVAC:OutdoorAirUnit": (
        (
            "outdoor_air_node_name",
            "airoutlet_node_name",
            "airinlet_node_name",
            "supply_fanoutlet_node_name",
        ),
        (),
    ),
    "ZoneHVAC:PackagedTerminalAirConditioner": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "ZoneHVAC:PackagedTerminalHeatPump": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "ZoneHVAC:RefrigerationChillerSet": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "ZoneHVAC:TerminalUnit:VariableRefrigerantFlow": (
        (
            "terminal_unit_air_inlet_node_name",
            "terminal_unit_air_outlet_node_name",
        ),
        (),
    ),
    "ZoneHVAC:UnitHeater": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "ZoneHVAC:UnitVentilator": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
            "outdoor_air_node_name",
            "exhaust_air_node_name",
            "mixed_air_node_name",
        ),
        (),
    ),
    "ZoneHVAC:VentilatedSlab": (
        (
            "return_air_node_name",
            "slab_in_node_name",
            "zone_supply_air_node_name",
            "outdoor_air_node_name",
            "relief_air_node_name",
            "outdoor_air_mixer_outlet_node_name",
            "fan_outlet_node_name",
            "hot_water_or_steam_inlet_node_name",
            "cold_water_inlet_node_name",
        ),
        (),
    ),
    "ZoneHVAC:VentilatedSlab:SlabGroup": (
        (),
        (
            "slab_inlet_node_name_for_surface",
            "slab_outlet_node_name_for_surface",
        ),
    ),
    "ZoneHVAC:WaterToAirHeatPump": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
            "outdoor_dry_bulb_temperature_sensor_node_name",
        ),
        (),
    ),
    "ZoneHVAC:WindowAirConditioner": (
        (
            "air_inlet_node_name",
            "air_outlet_node_name",
        ),
        (),
    ),
    "ZoneProperty:LocalEnvironment": (
        ("outdoor_air_node_name",),
        (),
    ),
}
