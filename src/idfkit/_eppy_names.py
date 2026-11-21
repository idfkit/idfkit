"""eppy's attribute spellings of EnergyPlus field names.

eppy derives an attribute name from the IDD field name by dropping every character that is not a
letter, a digit or a space, then turning spaces into underscores: ``"Vertex 1 X-coordinate"`` is
``Vertex_1_Xcoordinate`` and ``"U-Factor"`` is ``UFactor``. idfkit's keys keep the punctuation as a
word break (``vertex_1_x_coordinate``, ``u_factor``), so the two spellings differ wherever the IDD
name has punctuation inside a word. This module maps one to the other, and builds the IDD-style names
of extensible fields, whose group number the epJSON schema does not carry.
"""

from __future__ import annotations

import re
from collections.abc import Container, Mapping
from typing import Any, Final, cast

_NOT_EPPY_CHAR = re.compile(r"[^A-Za-z0-9 ]")
_NOT_KEY_CHAR = re.compile(r"[^a-z0-9]+")
_GROUP_NUMBER = re.compile(r"[1-9][0-9]*")
_NUMBER_INSIDE = re.compile(r"^(.+?)_([1-9][0-9]*)_(.+)$")


def eppy_field_name(idd_name: str) -> str:
    """eppy's attribute spelling of an IDD field name: ``"Vertex 1 X-coordinate"`` -> ``Vertex_1_Xcoordinate``.

    Examples:
        >>> eppy_field_name("Vertex 1 X-coordinate")
        'Vertex_1_Xcoordinate'
        >>> eppy_field_name("Outside Layer")
        'Outside_Layer'
    """
    return _NOT_EPPY_CHAR.sub("", idd_name).replace(" ", "_")


#: Where the IDD puts an extensible field's group number, as the count of words before it, for each
#: field that does not number after its first word: ``"Value Until Time 1"`` on
#: ``Schedule:Day:Interval`` is 3 words in, ``"Fenestration Surface 1 Name"`` on
#: ``WindowShadingControl`` 2. Read from EnergyPlus 26.2's ``Energy+.idd`` (26.1 numbers the same
#: fields the same way); a key an older release spells differently falls back to the first word.
_GROUP_NUMBER_POSITION: Final[Mapping[str, Mapping[str, int]]] = {
    "AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl": {
        "compressor_speed_at_loading_index": 5,
        "loading_index_evaporative_capacity_multiplier_function_of_temperature_curve_name": 2,
        "loading_index_compressor_power_multiplier_function_of_temperature_curve_name": 2,
    },
    "AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl:HR": {
        "compressor_speed_at_loading_index": 5,
        "loading_index_evaporative_capacity_multiplier_function_of_temperature_curve_name": 2,
        "loading_index_compressor_power_multiplier_function_of_temperature_curve_name": 2,
    },
    "AvailabilityManagerAssignmentList": {"availability_manager_object_type": 2, "availability_manager_name": 2},
    "ComfortViewFactorAngles": {"angle_factor": 2},
    "Connector:Mixer": {"inlet_branch_name": 2},
    "Connector:Splitter": {"outlet_branch_name": 2},
    "Controller:MechanicalVentilation": {
        "zone_or_zonelist_name": 3,
        "design_specification_outdoor_air_object_name": 6,
        "design_specification_zone_air_distribution_object_name": 7,
    },
    "Daylighting:Controls": {
        "daylighting_reference_point_name": 3,
        "fraction_of_lights_controlled_by_reference_point": 7,
        "illuminance_setpoint_at_reference_point": 5,
    },
    "DaylightingDevice:Tubular": {"transition_zone_name": 2, "transition_zone_length": 2},
    "DemandManager:ElectricEquipment": {"electric_equipment_name": 2},
    "DemandManager:ExteriorLights": {"exterior_lights_name": 2},
    "DemandManager:Ventilation": {"controller_outdoor_air_name": 3},
    "EnergyManagementSystem:GlobalVariable": {"erl_variable_name": 2},
    "EnergyManagementSystem:Program": {"program_line": 2},
    "EnergyManagementSystem:ProgramCallingManager": {"program_name": 2},
    "EnergyManagementSystem:Subroutine": {"program_line": 2},
    "Foundation:Kiva": {
        "custom_block_material_name": 2,
        "custom_block_depth": 2,
        "custom_block_x_position": 2,
        "custom_block_z_position": 2,
    },
    "Generator:FuelCell:AirSupply": {"molar_fraction": 2},
    "GroundHeatExchanger:ResponseFactors": {"g_function_ln_t_ts_value": 3, "g_function_g_value": 3},
    "GroundHeatExchanger:System": {"ghe_vertical_single_object_name": 3},
    "MaterialProperty:VariableThermalConductivity": {"thermal_conductivity": 2},
    "Meter:Custom": {"key_name": 2, "output_variable_or_meter_name": 5},
    "Meter:CustomDecrement": {"key_name": 2, "output_variable_or_meter_name": 5},
    "OutdoorAir:NodeList": {"node_or_nodelist_name": 4},
    "Output:Table:Annual": {
        "variable_or_meter_or_ems_variable_or_field_name": 8,
        "aggregation_type_for_variable_or_meter": 6,
        "digits_after_decimal": 3,
    },
    "Output:Table:Monthly": {"variable_or_meter_name": 3, "aggregation_type_for_variable_or_meter": 6},
    "Parametric:FileNameSuffix": {"suffix_for_file_name_in_run": 6},
    "Parametric:Logic": {"parametric_logic_line": 3},
    "Parametric:RunControl": {"perform_run": 2},
    "Parametric:SetValueForRun": {"value_for_run": 3},
    "PipingSystem:Underground:Domain": {"pipe_circuit": 2},
    "PipingSystem:Underground:PipeCircuit": {"pipe_segment": 2},
    "PythonPlugin:SearchPaths": {"search_path": 2},
    "PythonPlugin:Variables": {"variable_name": 2},
    "Refrigeration:CaseAndWalkInList": {"case_or_walkin_name": 3},
    "Refrigeration:CompressorList": {"refrigeration_compressor_name": 2},
    "Refrigeration:TransferLoadList": {"cascade_condenser_name_or_secondary_system_name": 6},
    "Refrigeration:WalkIn": {
        "total_insulated_surface_area_facing_zone": 6,
        "insulated_surface_u_value_facing_zone": 5,
        "area_of_glass_reach_in_doors_facing_zone": 8,
        "height_of_glass_reach_in_doors_facing_zone": 8,
        "glass_reach_in_door_u_value_facing_zone": 8,
        "glass_reach_in_door_opening_schedule_name_facing_zone": 9,
        "area_of_stocking_doors_facing_zone": 6,
        "height_of_stocking_doors_facing_zone": 6,
        "stocking_door_u_value_facing_zone": 6,
        "stocking_door_opening_schedule_name_facing_zone": 7,
        "stocking_door_opening_protection_type_facing_zone": 7,
    },
    "RoomAir:Node:AirflowNetwork:HVACEquipment": {
        "zonehvac_or_air_terminal_equipment_object_type": 7,
        "zonehvac_or_air_terminal_equipment_object_name": 7,
        "fraction_of_output_or_supply_air_from_hvac_equipment": 9,
        "fraction_of_input_or_return_air_to_hvac_equipment": 9,
    },
    "RoomAir:Node:AirflowNetwork:InternalGains": {
        "internal_gain_object_type": 3,
        "internal_gain_object_name": 3,
        "fraction_of_gains_to_node": 5,
    },
    "RoomAir:TemperaturePattern:SurfaceMapping": {"surface_name_pair": 3, "delta_adjacent_air_temperature_pair": 5},
    "RoomAirSettings:AirflowNetwork": {"roomairflownetwork_node_name": 2},
    "Schedule:Day:Interval": {"value_until_time": 3},
    "Schedule:Week:Compact": {"daytype_list": 2, "schedule_day_name": 2},
    "Schedule:Week:Rule": {"start_month": 2, "start_day": 2, "end_month": 2, "end_day": 2},
    "Schedule:Year": {"schedule_week_name": 2, "start_month": 2, "start_day": 2, "end_month": 2, "end_day": 2},
    "ShadowCalculation": {"shading_zone_group_zonelist_name": 3},
    "SolarCollector:UnglazedTranspired:Multisystem": {
        "outdoor_air_system_collector_inlet_node": 3,
        "outdoor_air_system_collector_outlet_node": 3,
        "outdoor_air_system_mixed_air_node": 3,
        "outdoor_air_system_zone_node": 3,
    },
    "SurfaceProperty:ExposedFoundationPerimeter": {"surface_segment_exposed": 2},
    "SurfaceProperty:GroundSurfaces": {
        "ground_surface_name": 2,
        "ground_surface_view_factor": 2,
        "ground_surface_temperature_schedule_name": 2,
        "ground_surface_reflectance_schedule_name": 2,
    },
    "SurfaceProperty:HeatTransferAlgorithm:SurfaceList": {"surface_name": 2},
    "SurfaceProperty:SurroundingSurfaces": {
        "surrounding_surface_name": 2,
        "surrounding_surface_view_factor": 2,
        "surrounding_surface_temperature_schedule_name": 2,
    },
    "Table:IndependentVariableList": {"independent_variable_name": 2},
    "Table:Lookup": {"output_value": 2},
    "UnitarySystemPerformance:Multispeed": {
        "heating_speed_supply_air_flow_ratio": 2,
        "cooling_speed_supply_air_flow_ratio": 2,
    },
    "WaterUse:Connections": {"water_use_equipment_name": 3},
    "WaterUse:RainCollector": {"collection_surface_name": 2},
    "WindowMaterial:GlazingGroup:Thermochromic": {"optical_data_temperature": 3, "window_material_glazing_name": 4},
    "WindowShadingControl": {"fenestration_surface_name": 2},
    "ZoneHVAC:Baseboard:RadiantConvective:Electric": {"fraction_of_radiant_energy_to_surface": 6},
    "ZoneHVAC:Baseboard:RadiantConvective:Steam": {"fraction_of_radiant_energy_to_surface": 6},
    "ZoneHVAC:Baseboard:RadiantConvective:Water": {"fraction_of_radiant_energy_to_surface": 6},
    "ZoneHVAC:CoolingPanel:RadiantConvective:Water": {"fraction_of_radiant_energy_to_surface": 6},
    "ZoneHVAC:EquipmentList": {
        "zone_equipment_object_type": 2,
        "zone_equipment_name": 2,
        "zone_equipment_cooling_sequence": 2,
        "zone_equipment_heating_or_no_load_sequence": 2,
        "zone_equipment_sequential_cooling_fraction_schedule_name": 2,
        "zone_equipment_sequential_heating_fraction_schedule_name": 2,
    },
    "ZoneHVAC:HighTemperatureRadiant": {"fraction_of_radiant_energy_to_surface": 6},
    "ZoneHVAC:LowTemperatureRadiant:SurfaceGroup": {"flow_fraction_for_surface": 4},
    "ZoneHVAC:RefrigerationChillerSet": {"air_chiller_name": 2},
    "ZoneHVAC:VentilatedSlab:SlabGroup": {
        "core_diameter_for_surface": 4,
        "core_length_for_surface": 4,
        "core_numbers_for_surface": 4,
        "slab_inlet_node_name_for_surface": 6,
        "slab_outlet_node_name_for_surface": 6,
    },
    "ZoneMRTCalculation": {"mrt_weighting_factor": 3},
    "ZoneProperty:UserViewFactors:BySurfaceName": {"from_surface": 2, "to_surface": 2, "view_factor": 2},
    "ZoneTerminalUnitList": {"zone_terminal_unit_name": 4},
}


def group_number_position(obj_type: str, key: str) -> int:
    """How many words of extensible field *key*'s IDD name come before its group number.

    Examples:
        >>> group_number_position("BuildingSurface:Detailed", "vertex_x_coordinate")
        1
        >>> group_number_position("Schedule:Day:Interval", "value_until_time")
        3
    """
    return _GROUP_NUMBER_POSITION.get(obj_type, {}).get(key, 1)


def numbered_idd_name(idd_name: str, group: int, position: int = 1) -> str:
    """The IDD name of extensible group *group*'s field, the number after *position* words.

    The epJSON schema names an extensible field once, without its group number (``"Vertex
    X-coordinate"``). The IDD numbers it after the first word in most types (``"Vertex 1
    X-coordinate"``, ``"Field 1"``, ``"Branch 1 Name"``) and elsewhere in others (``"Value Until
    Time 1"``, ``"Fenestration Surface 1 Name"``): ``group_number_position`` says where.

    Examples:
        >>> numbered_idd_name("Vertex X-coordinate", 2)
        'Vertex 2 X-coordinate'
        >>> numbered_idd_name("Field", 3)
        'Field 3'
        >>> numbered_idd_name("Value Until Time", 1, 3)
        'Value Until Time 1'
    """
    words = idd_name.split(" ")
    position = max(1, min(position, len(words)))
    return " ".join([*words[:position], str(group), *words[position:]])


def _key_spelling(name: str) -> str:
    """What [to_python_name][idfkit.objects.to_python_name] makes of *name*."""
    return _NOT_KEY_CHAR.sub("_", name.lower()).strip("_")


def idd_field_names(obj_schema: Mapping[str, Any] | None) -> dict[str, str]:
    """Each field key of a type to its IDD field name, from the schema's ``legacy_idd.field_info``."""
    if not obj_schema:
        return {}
    legacy: Any = obj_schema.get("legacy_idd")
    if not isinstance(legacy, dict):
        return {}
    info: Any = cast("dict[str, Any]", legacy).get("field_info")
    if not isinstance(info, dict):
        return {}
    names: dict[str, str] = {}
    for key, entry in cast("dict[str, Any]", info).items():
        if isinstance(entry, dict):
            idd_name: Any = cast("dict[str, Any]", entry).get("field_name")
            if isinstance(idd_name, str):
                names[key] = idd_name
    return names


def eppy_field_aliases(obj_schema: Mapping[str, Any] | None) -> dict[str, str]:
    """Map eppy's spelling of each field, as [to_python_name][idfkit.objects.to_python_name] reads it, to its key.

    Only spellings that differ from the key and name no other field are mapped:
    ``vertex_1_xcoordinate`` -> ``vertex_1_x_coordinate`` on ``FenestrationSurface:Detailed``, and
    the unnumbered ``vertex_xcoordinate`` -> ``vertex_x_coordinate`` for an extensible field, whose
    group number the caller strips first. Empty for most types.

    The result is shared by every object of the type and must not be changed.
    """
    names = idd_field_names(obj_schema)
    aliases: dict[str, str] = {}
    for key, idd_name in names.items():
        spelling = _key_spelling(eppy_field_name(idd_name))
        # ``name`` always means the object's name, even where a nameless type's IDD calls a field
        # ``Name`` (``name_`` on Output:Table:ReportPeriod).
        if spelling and spelling != key and spelling not in names and spelling != "name":
            aliases.setdefault(spelling, key)
    return aliases


def resolve_eppy_key(python_key: str, aliases: Mapping[str, str], extensibles: Container[str]) -> str | None:
    """The key eppy's spelling *python_key* names, or ``None`` when it is not one of them.

    *python_key* is eppy's name as [to_python_name][idfkit.objects.to_python_name] reads it
    (``Vertex_1_Xcoordinate`` is ``vertex_1_xcoordinate``), *aliases* the type's
    ``eppy_field_aliases``. A fixed field maps to its key (``vertex_1_x_coordinate`` on
    ``FenestrationSurface:Detailed``); a numbered extensible field maps to the flat spelling
    ``vertex_x_coordinate_1``, which the legacy flat-extensible paths route to its group.
    """
    if not aliases:
        return None
    key = aliases.get(python_key)
    if key is not None:
        return key
    last_underscore = python_key.rfind("_")
    if last_underscore > 0 and _GROUP_NUMBER.fullmatch(python_key, last_underscore + 1):
        base = aliases.get(python_key[:last_underscore])
        if base is not None and base in extensibles:
            return f"{base}{python_key[last_underscore:]}"
    m = _NUMBER_INSIDE.match(python_key)
    if m:
        base = aliases.get(f"{m.group(1)}_{m.group(3)}")
        if base is not None and base in extensibles:
            return f"{base}_{m.group(2)}"
    return None
