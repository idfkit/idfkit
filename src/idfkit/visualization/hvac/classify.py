"""Classification helpers: node-field detection, categories, and template checks.

The graph builder leans on three questions answered here:

1. *Is this object a flow component, a structural definition, or a junction?*
   (``STRUCTURAL_TYPES``, ``NODE_JUNCTION_SPECS``, ``BRANCH_CONNECTOR_TYPES``)
2. *What are a component's inlet and outlet nodes?* (:func:`component_ports`)
3. *What color/shape category does it render as?* (:func:`category_for`)

EnergyPlus wires HVAC by plain-string node names, not schema references, so the
detection is heuristic: a field whose name ends in ``_name``, mentions ``node``,
is not a schema object reference, and is not a control field (``setpoint`` /
``sensor`` / ``actuator``) is treated as a flow node, with inlet/outlet decided
by substring. A short ``SPECIAL_PORTS`` table covers components whose node names
don't follow the inlet/outlet convention (e.g. ``OutdoorAir:Mixer``).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal

from .model import Category

if TYPE_CHECKING:
    from idfkit.document import IDFDocument
    from idfkit.objects import IDFObject
    from idfkit.schema import EpJSONSchema

#: ``(node_name, fluid_type)``.
Port = tuple[str, str]

_HVAC_TEMPLATE_GROUP = "HVAC Templates"
_HVAC_TEMPLATE_PREFIX = "HVACTemplate:"

#: Compound "container" components (unitary systems, coil systems) that hold a
#: fan/coil train internally, referenced by name fields rather than placed on a
#: branch. They are treated as structural: the container box is dropped and its
#: child components are pulled into the loop in sequence (see :mod:`.build`).
COMPOUND_CONTAINER_TYPES: frozenset[str] = frozenset({
    "AirLoopHVAC:UnitarySystem",
    "AirLoopHVAC:UnitaryHeatPump:AirToAir",
    "AirLoopHVAC:UnitaryHeatPump:WaterToAir",
    "AirLoopHVAC:UnitaryHeatPump:AirToAir:MultiSpeed",
    "AirLoopHVAC:UnitaryHeatCool",
    "AirLoopHVAC:UnitaryHeatOnly",
    "AirLoopHVAC:UnitaryHeatCool:VAVChangeoverBypass",
    "CoilSystem:Cooling:DX",
    "CoilSystem:Heating:DX",
    "CoilSystem:Cooling:Water",
    "CoilSystem:Cooling:DX:HeatExchangerAssisted",
    "CoilSystem:Cooling:Water:HeatExchangerAssisted",
})

#: Object types that define topology but are not component vertices themselves.
#: Junctions (connectors, zone splitters/mixers, plenums) appear here too — they
#: are turned into junction vertices by dedicated passes in :mod:`.build`.
_STRUCTURAL_BASE: frozenset[str] = frozenset({
    "Branch",
    "BranchList",
    "ConnectorList",
    "Connector:Splitter",
    "Connector:Mixer",
    "AirLoopHVAC",
    "PlantLoop",
    "CondenserLoop",
    "AirLoopHVAC:ZoneSplitter",
    "AirLoopHVAC:ZoneMixer",
    "AirLoopHVAC:SupplyPlenum",
    "AirLoopHVAC:ReturnPlenum",
    "AirLoopHVAC:SupplyPath",
    "AirLoopHVAC:ReturnPath",
    "AirLoopHVAC:OutdoorAirSystem",
    "AirLoopHVAC:OutdoorAirSystem:EquipmentList",
    "ZoneHVAC:EquipmentConnections",
    "ZoneHVAC:EquipmentList",
    "ZoneHVAC:AirDistributionUnit",
    "NodeList",
    "OutdoorAir:NodeList",
})

#: Schema groups whose objects are compound containers wrapping an internal
#: fan/coil train: zone forced-air units (fan coils, PTAC/PTHP, unit ventilators,
#: VRF terminal units). Like :data:`COMPOUND_CONTAINER_TYPES`, the container box is
#: dropped and its children are pulled out (here, grouped under their zone).
_CONTAINER_GROUPS: frozenset[str] = frozenset({"Zone HVAC Forced Air Units"})

#: All types the component-vertex pass skips. Compound containers are included so
#: they are not drawn as a box; :mod:`.build` expands them into their children.
STRUCTURAL_TYPES: frozenset[str] = _STRUCTURAL_BASE | COMPOUND_CONTAINER_TYPES


def is_expandable_container(obj_type: str, group: str | None) -> bool:
    """True if *obj_type* is a compound container to expand into its children.

    Covers the hardcoded unitary/coil-system types (:data:`COMPOUND_CONTAINER_TYPES`,
    e.g. ``CoilSystem:*`` which is schema group ``"Coils"``) plus any object in a
    container schema group (:data:`_CONTAINER_GROUPS` — zone forced-air units).
    Radiative/convective units (baseboards) are intentionally excluded: they are
    single components, not containers.
    """
    return obj_type in COMPOUND_CONTAINER_TYPES or (group is not None and group in _CONTAINER_GROUPS)


#: Branch-based connectors — ports are synthesized from branch inlet/outlet nodes.
BRANCH_CONNECTOR_TYPES: frozenset[str] = frozenset({"Connector:Splitter", "Connector:Mixer"})


@dataclass(frozen=True)
class JunctionSpec:
    """Field layout of a node-based junction (one side single, the other a list).

    Attributes:
        single_field: Top-level node field on the single side.
        single_dir: ``"inlet"`` or ``"outlet"`` — direction of *single_field*.
        many_inner: Extensible inner field name on the many side.
        many_dir: ``"inlet"`` or ``"outlet"`` — direction of *many_inner*.
    """

    single_field: str
    single_dir: Literal["inlet", "outlet"]
    many_inner: str
    many_dir: Literal["inlet", "outlet"]


#: Node-based junctions: a single inlet/outlet plus an extensible list on the
#: opposite side. Their ports are read directly from these fields.
NODE_JUNCTION_SPECS: dict[str, JunctionSpec] = {
    "AirLoopHVAC:ZoneSplitter": JunctionSpec("inlet_node_name", "inlet", "outlet_node_name", "outlet"),
    "AirLoopHVAC:ZoneMixer": JunctionSpec("outlet_node_name", "outlet", "inlet_node_name", "inlet"),
    "AirLoopHVAC:SupplyPlenum": JunctionSpec("inlet_node_name", "inlet", "outlet_node_name", "outlet"),
    "AirLoopHVAC:ReturnPlenum": JunctionSpec("outlet_node_name", "outlet", "inlet_node_name", "inlet"),
}


@dataclass(frozen=True)
class PortSpec:
    """Explicit inlet/outlet field lists for components with irregular node names."""

    inlets: tuple[str, ...]
    outlets: tuple[str, ...]


#: Components whose node names do not follow the inlet/outlet convention.
SPECIAL_PORTS: dict[str, PortSpec] = {
    "OutdoorAir:Mixer": PortSpec(
        inlets=("outdoor_air_stream_node_name", "return_air_stream_node_name"),
        outlets=("mixed_air_node_name", "relief_air_stream_node_name"),
    ),
}


#: Schema group -> render category.
_GROUP_CATEGORY: dict[str, Category] = {
    "Coils": "coil",
    "Fans": "fan",
    "Pumps": "pump",
    "Plant Heating and Cooling Equipment": "plant_equipment",
    "Condenser Equipment and Heat Exchangers": "plant_equipment",
    "Zone HVAC Air Loop Terminal Units": "terminal",
}

_CONTROL_TOKENS = ("setpoint", "sensor", "actuator")


def hvac_template_types(doc: IDFDocument) -> list[str]:
    """Return the sorted ``HVACTemplate:*`` object types present in *doc*.

    Uses the schema ``group`` field when a schema is loaded, falling back to a
    name-prefix match. An empty list means the document is fully expanded.
    """
    schema = doc.schema
    found: list[str] = []
    for obj_type in doc:
        if schema is not None:
            if schema.get_group(obj_type) == _HVAC_TEMPLATE_GROUP:
                found.append(obj_type)
        elif obj_type.startswith(_HVAC_TEMPLATE_PREFIX):
            found.append(obj_type)
    return sorted(found)


def category_for(obj_type: str, group: str | None) -> Category:
    """Return the render category for an object type."""
    if obj_type in BRANCH_CONNECTOR_TYPES or obj_type in NODE_JUNCTION_SPECS:
        return "junction"
    if obj_type.startswith("OutdoorAir:") or obj_type.startswith("AirLoopHVAC:OutdoorAir"):
        return "outdoor_air"
    if obj_type.startswith("Pipe"):
        return "pipe"
    if group is not None and group in _GROUP_CATEGORY:
        return _GROUP_CATEGORY[group]
    return "other"


def fluid_for_field(field_name: str) -> str:
    """Best-effort fluid type from a node field name."""
    low = field_name.lower()
    if "steam" in low:
        return "steam"
    if "water" in low or "chilled" in low or "condenser" in low or "glycol" in low:
        return "water"
    if "air" in low:
        return "air"
    return "unknown"


def _is_flow_node_field(obj_type: str, field_name: str, schema: EpJSONSchema | None) -> bool:
    """True if *field_name* names a free-string flow node (not a ref or control).

    Most node fields end in ``_node_name``, but some components (e.g. VRF DX coils)
    use a bare ``_node`` suffix (``coil_air_inlet_node``) — both are accepted.
    """
    low = field_name.lower()
    if not (low.endswith("_node_name") or low.endswith("_node")):
        return False
    if any(token in low for token in _CONTROL_TOKENS):
        return False
    if "schedule" in low or "availability" in low:
        return False
    # A schema object-list means this is a reference to another object, not a node.
    return schema is None or not schema.get_field_object_list(obj_type, field_name)


def _direction(field_name: str) -> Literal["inlet", "outlet"] | None:
    low = field_name.lower()
    if "inlet" in low:
        return "inlet"
    if "outlet" in low:
        return "outlet"
    return None


def _ports_from_fields(obj: IDFObject, field_names: tuple[str, ...]) -> list[Port]:
    """Collect ``(node, fluid)`` ports from an explicit list of node fields."""
    ports: list[Port] = []
    for fname in field_names:
        val = obj.data.get(fname)
        if isinstance(val, str) and val.strip():
            ports.append((val.strip(), fluid_for_field(fname)))
    return ports


def _generic_ports(obj: IDFObject, schema: EpJSONSchema | None) -> tuple[list[Port], list[Port]]:
    """Detect node ports by field-name heuristic for a regular component."""
    inlets: list[Port] = []
    outlets: list[Port] = []
    for fname, val in obj.data.items():
        if not isinstance(val, str) or not val.strip() or not _is_flow_node_field(obj.obj_type, fname, schema):
            continue
        port = (val.strip(), fluid_for_field(fname))
        direction = _direction(fname)
        if direction == "inlet":
            inlets.append(port)
        elif direction == "outlet":
            outlets.append(port)
    return inlets, outlets


def component_ports(obj: IDFObject, schema: EpJSONSchema | None) -> tuple[list[Port], list[Port]]:
    """Return ``(inlet_ports, outlet_ports)`` for a flow component.

    Each port is a ``(node_name, fluid_type)`` pair. Components in
    :data:`SPECIAL_PORTS` use their explicit field lists; everything else is
    detected by the node-field heuristic, with ambiguous fields skipped.
    """
    special = SPECIAL_PORTS.get(obj.obj_type)
    if special is not None:
        return _ports_from_fields(obj, special.inlets), _ports_from_fields(obj, special.outlets)
    return _generic_ports(obj, schema)


def _resolve_child(
    data: dict[str, Any], type_key: str, value: str, schema: EpJSONSchema | None
) -> tuple[str, str] | None:
    """Resolve one ``<prefix>_object_type`` field to a ``(canonical_type, name)`` pair.

    The paired name field is ``<prefix>_name`` (unitary/coil systems) or
    ``<prefix>_object_name`` (VRF terminal units). The type value may be miscased
    (e.g. ``COIL:Cooling:DX:...``), so it is canonicalised via the schema; a type
    the schema does not recognise is skipped as a non-component reference.
    """
    prefix = type_key[: -len("_object_type")]
    name_value = data.get(f"{prefix}_name")
    if not isinstance(name_value, str) or not name_value.strip():
        name_value = data.get(f"{prefix}_object_name")
    if not isinstance(name_value, str) or not name_value.strip():
        return None
    child_type = value.strip()
    if schema is not None:
        canonical = schema.resolve_type_name(child_type)
        if canonical is None:
            return None
        child_type = canonical
    return child_type, name_value.strip()


def child_component_refs(obj: IDFObject, schema: EpJSONSchema | None) -> list[tuple[str, str]]:
    """Return the ``(object_type, name)`` child references of a compound container.

    Unitary systems, coil systems, and zone forced-air units (fan coils, PTACs,
    VRF terminal units) name their internal fan and coils via
    ``<prefix>_object_type`` paired with ``<prefix>_name`` or
    ``<prefix>_object_name`` field pairs (e.g. ``cooling_coil_object_type`` +
    ``cooling_coil_name``/``cooling_coil_object_name``). This scans for those
    pairs and keeps the ones whose type is a real schema object type, so
    non-component references (performance specs, etc.) are skipped. Returned
    types are canonicalised to their schema form.
    """
    refs: list[tuple[str, str]] = []
    data = obj.data
    for key, value in data.items():
        if not key.endswith("_object_type") or not isinstance(value, str) or not value.strip():
            continue
        child = _resolve_child(data, key, value, schema)
        if child is not None:
            refs.append(child)
    return refs
