"""Reconstruct an HVAC topology graph from an :class:`~idfkit.IDFDocument`.

The builder mirrors how the EnergyPlus ``eplusout.bnd`` report wires a system,
but works directly from IDF objects with no simulation run. Components declare
inlet/outlet node names; a component whose *outlet* is node N feeds the component
whose *inlet* is node N. Branches order components in series, connectors and zone
splitters/mixers create parallel junctions, and the loop objects partition
everything into supply/demand sides.

The single public entry point is :func:`build_hvac_graph`. Building never raises
on odd topology — it accumulates :class:`~.model.HVACWarning` records instead —
except for the precondition that the document must be expanded (no
``HVACTemplate:*`` objects).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

from idfkit.exceptions import HVACDiagramError

from .classify import (
    NODE_JUNCTION_SPECS,
    SPECIAL_PORTS,
    STRUCTURAL_TYPES,
    Port,
    category_for,
    child_component_refs,
    component_ports,
    hvac_template_types,
    is_expandable_container,
)
from .model import (
    Category,
    HVACEdge,
    HVACGraph,
    HVACLoop,
    HVACNode,
    HVACRefrigerantEdge,
    HVACVertex,
    HVACWarning,
    HVACZone,
    LoopMembership,
    LoopType,
    Side,
)

if TYPE_CHECKING:
    from idfkit.document import IDFDocument
    from idfkit.objects import IDFObject
    from idfkit.schema import EpJSONSchema

_EXCLUDED_GROUPS: frozenset[str] = frozenset({"Setpoint Managers", "Controllers"})

#: Port direction (distinct from :data:`~.model.Side`, which is supply/demand).
_Direction = Literal["inlet", "outlet"]

# Per-loop-type field names. CondenserLoop uses ``condenser_side_*`` /
# ``condenser_demand_side_*`` where Plant/Air use ``plant_side_*`` / ``branch_list_name``.
_LOOP_SPECS: dict[LoopType, dict[str, str | None]] = {
    "AirLoopHVAC": {
        "fluid": "air",
        "supply_bl": "branch_list_name",
        "demand_bl": None,
        "demand_inlet": "demand_side_inlet_node_names",
        "demand_outlet": "demand_side_outlet_node_name",
        "supply_inlet": "supply_side_inlet_node_name",
        "supply_outlet": "supply_side_outlet_node_names",
    },
    "PlantLoop": {
        "fluid": "water",
        "supply_bl": "plant_side_branch_list_name",
        "demand_bl": "demand_side_branch_list_name",
        "demand_inlet": "demand_side_inlet_node_name",
        "demand_outlet": "demand_side_outlet_node_name",
        "supply_inlet": "plant_side_inlet_node_name",
        "supply_outlet": "plant_side_outlet_node_name",
    },
    "CondenserLoop": {
        "fluid": "water",
        "supply_bl": "condenser_side_branch_list_name",
        "demand_bl": "condenser_demand_side_branch_list_name",
        "demand_inlet": "demand_side_inlet_node_name",
        "demand_outlet": "demand_side_outlet_node_name",
        "supply_inlet": "condenser_side_inlet_node_name",
        "supply_outlet": "condenser_side_outlet_node_name",
    },
}

_LOOP_ORDER: dict[LoopType, int] = {"AirLoopHVAC": 0, "PlantLoop": 1, "CondenserLoop": 2}

# Every VRF outdoor unit type shares this prefix: the base unit plus the
# FluidTemperatureControl and FluidTemperatureControl:HR (heat-recovery) variants.
_VRF_MASTER_PREFIX = "AirConditioner:VariableRefrigerantFlow"
_VRF_TERMINAL_TYPE = "ZoneHVAC:TerminalUnit:VariableRefrigerantFlow"
#: VRF terminal-unit DX coils (canonical schema names) — the refrigerant-bearing
#: children the outdoor unit drives.
_VRF_COIL_TYPES: frozenset[str] = frozenset({
    "Coil:Cooling:DX:VariableRefrigerantFlow",
    "Coil:Heating:DX:VariableRefrigerantFlow",
    "Coil:Cooling:DX:VariableRefrigerantFlow:FluidTemperatureControl",
    "Coil:Heating:DX:VariableRefrigerantFlow:FluidTemperatureControl",
})


def _vkey(obj_type: str, name: str) -> str:
    return f"{obj_type.upper()}::{name.strip().upper()}"


@dataclass
class _VBuild:
    """Mutable working vertex; frozen into :class:`HVACVertex` at the end."""

    key: str
    obj_type: str
    name: str
    category: Category
    inlets: dict[str, str] = field(default_factory=lambda: {})  # node-key -> display
    outlets: dict[str, str] = field(default_factory=lambda: {})
    memberships: list[LoopMembership] = field(default_factory=lambda: [])
    seen_memberships: set[tuple[str, str]] = field(default_factory=lambda: set[tuple[str, str]]())
    zone: str | None = None


@dataclass
class _LoopBuild:
    loop_id: str
    name: str
    loop_type: LoopType
    is_air: bool
    demand_inlets: set[str] = field(default_factory=lambda: set[str]())
    demand_outlets: set[str] = field(default_factory=lambda: set[str]())


@dataclass
class _ZoneBuild:
    name: str
    air_node: str | None
    inlet_nodes: list[str]
    exhaust_nodes: list[str]
    return_nodes: list[str]
    equipment_keys: list[str]


class _GraphBuilder:
    def __init__(self, doc: IDFDocument) -> None:
        self.doc = doc
        self.schema: EpJSONSchema | None = doc.schema
        self.present: set[str] = set(doc)
        self.vertices: dict[str, _VBuild] = {}
        self.node_fluid: dict[str, str] = {}
        self.node_display: dict[str, str] = {}
        self.node_parent: dict[str, str] = {}  # union-find for loop supply<->demand links
        self.warnings: list[HVACWarning] = []
        self.loops: list[_LoopBuild] = []
        self.branch_inlet: dict[str, str] = {}  # branch-key -> inlet node-key
        self.branch_outlet: dict[str, str] = {}
        self.branch_loopside: dict[str, tuple[str, Side, str]] = {}  # branch-key -> (loop_id, side, fluid)
        self.oa_system_loop: dict[str, tuple[str, Side]] = {}  # OA-system-name-upper -> (loop_id, side)
        self.boundary_nodes: set[str] = set()
        self.branch_names: set[str] = {b.name.strip().upper() for b in self._objs("Branch")}
        self.nodelist_map: dict[str, list[str]] = self._build_nodelist_map()
        self.zones: list[_ZoneBuild] = []
        self.refrigerant_links: list[tuple[str, str]] = []  # (master-key, terminal-coil-key)

    # -- small helpers -----------------------------------------------------

    def _objs(self, obj_type: str) -> list[IDFObject]:
        if obj_type not in self.present:
            return []
        return list(self.doc.get_collection(obj_type))

    def _group(self, obj_type: str) -> str | None:
        return self.schema.get_group(obj_type) if self.schema is not None else None

    def _build_nodelist_map(self) -> dict[str, list[str]]:
        out: dict[str, list[str]] = {}
        for nl in self._objs("NodeList"):
            names = [it.get("node_name") for it in nl.extensible_items()]
            out[nl.name.strip().upper()] = [n.strip() for n in names if isinstance(n, str) and n.strip()]
        return out

    def _resolve_nodes(self, value: object) -> list[str]:
        if not isinstance(value, str) or not value.strip():
            return []
        up = value.strip().upper()
        if up in self.nodelist_map:
            return list(self.nodelist_map[up])
        return [value.strip()]

    def _vertex(self, obj_type: str, name: str, category: Category | None = None) -> _VBuild:
        key = _vkey(obj_type, name)
        vb = self.vertices.get(key)
        if vb is None:
            cat = category if category is not None else category_for(obj_type, self._group(obj_type))
            vb = _VBuild(key=key, obj_type=obj_type, name=name, category=cat)
            self.vertices[key] = vb
        return vb

    def _reg(self, vb: _VBuild, node: object, direction: _Direction, fluid: str) -> None:
        if not isinstance(node, str) or not node.strip():
            return
        display = node.strip()
        nk = display.upper()
        self.node_display.setdefault(nk, display)
        if fluid != "unknown" and self.node_fluid.get(nk, "unknown") == "unknown":
            self.node_fluid[nk] = fluid
        else:
            self.node_fluid.setdefault(nk, "unknown")
        target = vb.inlets if direction == "inlet" else vb.outlets
        target.setdefault(nk, display)

    def _find(self, nk: str) -> str:
        parent = self.node_parent
        root = nk
        while parent.get(root, root) != root:
            root = parent[root]
        node = nk
        while parent.get(node, node) != root:
            nxt = parent[node]
            parent[node] = root
            node = nxt
        return root

    def _union(self, a: str, b: str) -> None:
        ra, rb = self._find(a), self._find(b)
        if ra != rb:
            self.node_parent[rb] = ra

    def _member(self, vb: _VBuild, loop_id: str, side: Side) -> None:
        marker = (loop_id, side)
        if marker in vb.seen_memberships:
            return
        vb.seen_memberships.add(marker)
        vb.memberships.append(LoopMembership(loop_id=loop_id, side=side))

    def _branch_fluid(self, branch_name: str) -> str:
        ls = self.branch_loopside.get(branch_name.strip().upper())
        return ls[2] if ls is not None else "unknown"

    def _assign_branch_membership(self, vb: _VBuild, branch_name: object) -> None:
        if not isinstance(branch_name, str):
            return
        ls = self.branch_loopside.get(branch_name.strip().upper())
        if ls is not None:
            self._member(vb, ls[0], ls[1])

    # -- passes ------------------------------------------------------------

    def _pass_loops(self) -> None:
        for loop_type in ("AirLoopHVAC", "PlantLoop", "CondenserLoop"):
            spec = _LOOP_SPECS[loop_type]
            for obj in self._objs(loop_type):
                loop_id = _vkey(loop_type, obj.name)
                lb = _LoopBuild(loop_id=loop_id, name=obj.name, loop_type=loop_type, is_air=loop_type == "AirLoopHVAC")
                fluid = spec["fluid"] or "unknown"
                self._map_branchlist(obj.data.get(spec["supply_bl"] or ""), loop_id, "supply", fluid)
                demand_bl = spec["demand_bl"]
                if demand_bl is not None:
                    self._map_branchlist(obj.data.get(demand_bl), loop_id, "demand", fluid)
                boundary: dict[str, set[str]] = {}
                for key in ("demand_inlet", "demand_outlet", "supply_inlet", "supply_outlet"):
                    field_name = spec[key]
                    nodes = {n.upper() for n in (self._resolve_nodes(obj.data.get(field_name)) if field_name else [])}
                    boundary[key] = nodes
                    self.boundary_nodes |= nodes
                lb.demand_inlets |= boundary["demand_inlet"]
                lb.demand_outlets |= boundary["demand_outlet"]
                # A loop links its supply outlet to its demand inlet and its demand
                # outlet back to its supply inlet (EnergyPlus joins these implicitly,
                # under different node names) — alias them so edges span both sides.
                for a in boundary["supply_outlet"]:
                    for b in boundary["demand_inlet"]:
                        self._union(a, b)
                for a in boundary["demand_outlet"]:
                    for b in boundary["supply_inlet"]:
                        self._union(a, b)
                self.loops.append(lb)

    def _map_branchlist(self, bl_name: object, loop_id: str, side: Side, fluid: str) -> None:
        if not isinstance(bl_name, str) or not bl_name.strip():
            return
        bl = self.doc.get_collection("BranchList").get(bl_name) if "BranchList" in self.present else None
        if bl is None:
            self.warnings.append(HVACWarning("missing_object", f"BranchList '{bl_name}' not found", bl_name))
            return
        for item in bl.extensible_items():
            branch_name = item.get("branch_name")
            if not isinstance(branch_name, str) or not branch_name.strip():
                continue
            bkey = branch_name.strip().upper()
            self.branch_loopside[bkey] = (loop_id, side, fluid)
            if bkey not in self.branch_names:
                self.warnings.append(
                    HVACWarning("missing_branch", f"Branch '{branch_name}' referenced but not defined", branch_name)
                )

    def _pass_components(self) -> None:
        for obj_type, collection in self.doc.objects_by_type():
            group = self._group(obj_type)
            # Skip structural definitions and compound containers (unitary systems,
            # zone forced-air units): the box is dropped and its children — separate
            # objects with the real nodes — become the vertices instead.
            if obj_type in STRUCTURAL_TYPES or is_expandable_container(obj_type, group):
                continue
            if group in _EXCLUDED_GROUPS:
                continue
            category = category_for(obj_type, group)
            for obj in collection:
                inlets, outlets = component_ports(obj, self.schema)
                if not inlets and not outlets:
                    continue
                vb = self._vertex(obj_type, obj.name, category)
                self._register_ports(vb, inlets, outlets)

    def _register_ports(self, vb: _VBuild, inlets: list[Port], outlets: list[Port]) -> None:
        for node, fluid in inlets:
            self._reg(vb, node, "inlet", fluid)
        for node, fluid in outlets:
            self._reg(vb, node, "outlet", fluid)

    def _pass_branches(self) -> None:
        for br in self._objs("Branch"):
            bkey = br.name.strip().upper()
            ls = self.branch_loopside.get(bkey)
            loop_id = ls[0] if ls is not None else None
            side: Side = ls[1] if ls is not None else "other"
            fluid = ls[2] if ls is not None else "unknown"
            first_in: str | None = None
            last_out: str | None = None
            for item in br.extensible_items():
                in_k, out_k = self._add_branch_component(item, loop_id, side, fluid)
                if in_k is not None and first_in is None:
                    first_in = in_k
                if out_k is not None:
                    last_out = out_k
            if first_in is not None:
                self.branch_inlet[bkey] = first_in
            if last_out is not None:
                self.branch_outlet[bkey] = last_out

    def _add_branch_component(
        self, item: dict[str, object], loop_id: str | None, side: Side, fluid: str
    ) -> tuple[str | None, str | None]:
        """Register one branch component; return its (inlet, outlet) node keys."""
        ct = item.get("component_object_type")
        cn = item.get("component_name")
        inn = item.get("component_inlet_node_name")
        outn = item.get("component_outlet_node_name")
        in_k = inn.strip().upper() if isinstance(inn, str) and inn.strip() else None
        out_k = outn.strip().upper() if isinstance(outn, str) and outn.strip() else None
        if not isinstance(ct, str) or not isinstance(cn, str):
            return in_k, out_k
        expandable = is_expandable_container(ct, self._group(ct))
        if ct in STRUCTURAL_TYPES or expandable:
            # A container — its internal equipment carries the real nodes, so the
            # container box is dropped and its children are pulled into the loop.
            if ct == "AirLoopHVAC:OutdoorAirSystem" and loop_id is not None:
                self.oa_system_loop[cn.strip().upper()] = (loop_id, side)
            elif expandable and loop_id is not None:
                self._expand_container(ct, cn, loop_id, side)
            return in_k, out_k
        vb = self._vertex(ct, cn, category_for(ct, self._group(ct)))
        self._reg(vb, inn, "inlet", fluid)
        self._reg(vb, outn, "outlet", fluid)
        if loop_id is not None:
            self._member(vb, loop_id, side)
        return in_k, out_k

    def _expand_container(self, obj_type: str, name: str, loop_id: str, side: Side) -> None:
        """Assign a compound container's internal fan/coil children to a loop side.

        The children are independent objects (already vertices from the component
        pass) named by the container's fields; they only lack loop membership.
        """
        for child_type, child_name in self._container_children(obj_type, name):
            vb = self.vertices.get(_vkey(child_type, child_name))
            if vb is not None:
                self._member(vb, loop_id, side)

    def _container_children(self, obj_type: str, name: str) -> list[tuple[str, str]]:
        if obj_type not in self.present:
            return []
        container = self.doc.get_collection(obj_type).get(name)
        if container is None:
            return []
        return child_component_refs(container, self.schema)

    def _pass_node_junctions(self) -> None:
        for obj_type, spec in NODE_JUNCTION_SPECS.items():
            for obj in self._objs(obj_type):
                vb = self._vertex(obj_type, obj.name, "junction")
                self._reg(vb, obj.data.get(spec.single_field), spec.single_dir, "air")
                for item in obj.extensible_items():
                    self._reg(vb, item.get(spec.many_inner), spec.many_dir, "air")

    def _pass_connectors(self) -> None:
        for obj in self._objs("Connector:Splitter"):
            vb = self._vertex("Connector:Splitter", obj.name, "junction")
            inb = obj.data.get("inlet_branch_name")
            self._connector_port(vb, inb, self.branch_outlet, "inlet")
            self._assign_branch_membership(vb, inb)
            for item in obj.extensible_items():
                outb = item.get("outlet_branch_name")
                self._connector_port(vb, outb, self.branch_inlet, "outlet")
                self._assign_branch_membership(vb, outb)
        for obj in self._objs("Connector:Mixer"):
            vb = self._vertex("Connector:Mixer", obj.name, "junction")
            outb = obj.data.get("outlet_branch_name")
            self._connector_port(vb, outb, self.branch_inlet, "outlet")
            self._assign_branch_membership(vb, outb)
            for item in obj.extensible_items():
                inb = item.get("inlet_branch_name")
                self._connector_port(vb, inb, self.branch_outlet, "inlet")
                self._assign_branch_membership(vb, inb)

    def _connector_port(
        self, vb: _VBuild, branch_name: object, endpoints: dict[str, str], direction: _Direction
    ) -> None:
        if not isinstance(branch_name, str) or not branch_name.strip():
            return
        nk = endpoints.get(branch_name.strip().upper())
        if nk is None:
            return
        self._reg(vb, self.node_display.get(nk, nk), direction, self._branch_fluid(branch_name))

    def _pass_oa_systems(self) -> None:
        for oas in self._objs("AirLoopHVAC:OutdoorAirSystem"):
            link = self.oa_system_loop.get(oas.name.strip().upper())
            if link is None:
                continue
            loop_id, side = link
            eqlist_name = oas.data.get("outdoor_air_equipment_list_name")
            if not isinstance(eqlist_name, str) or "AirLoopHVAC:OutdoorAirSystem:EquipmentList" not in self.present:
                continue
            eqlist = self.doc.get_collection("AirLoopHVAC:OutdoorAirSystem:EquipmentList").get(eqlist_name)
            if eqlist is None:
                continue
            for i in range(1, 50):
                ct = eqlist.data.get(f"component_{i}_object_type")
                cn = eqlist.data.get(f"component_{i}_name")
                if not isinstance(ct, str) or not isinstance(cn, str):
                    break
                group = self._group(ct)
                if is_expandable_container(ct, group):
                    # e.g. a VRF terminal unit sitting in the OA-system equipment list.
                    self._expand_container(ct, cn, loop_id, side)
                    continue
                vb = self._vertex(ct, cn, category_for(ct, group))
                self._member(vb, loop_id, side)

    def _collect_oa_boundary(self) -> None:
        """Outdoor-air source/relief nodes are legitimate single-reference endpoints."""
        for node in self._objs("OutdoorAir:Node"):
            self.boundary_nodes.add(node.name.strip().upper())
        for nl in self._objs("OutdoorAir:NodeList"):
            for item in nl.extensible_items():
                value = item.get("node_or_nodelist_name")
                if isinstance(value, str) and value.strip():
                    self.boundary_nodes.add(value.strip().upper())
        # An OA mixer's outdoor-air inlet and relief-air outlet open to outside, so
        # they are referenced by a single component by design — not suspicious.
        oa_boundary_fields = (
            *SPECIAL_PORTS["OutdoorAir:Mixer"].inlets[:1],
            *SPECIAL_PORTS["OutdoorAir:Mixer"].outlets[1:],
        )
        for mixer in self._objs("OutdoorAir:Mixer"):
            for fname in oa_boundary_fields:
                value = mixer.data.get(fname)
                if isinstance(value, str) and value.strip():
                    self.boundary_nodes.add(value.strip().upper())

    def _pass_zones(self) -> None:
        for ec in self._objs("ZoneHVAC:EquipmentConnections"):
            zname = ec.data.get("zone_name")
            if not isinstance(zname, str):
                continue
            air_node = ec.data.get("zone_air_node_name")
            equipment_keys = self._zone_equipment_keys(ec.data.get("zone_conditioning_equipment_list_name"), zname)
            inlet_nodes = self._resolve_nodes(ec.data.get("zone_air_inlet_node_or_nodelist_name"))
            exhaust_nodes = self._resolve_nodes(ec.data.get("zone_air_exhaust_node_or_nodelist_name"))
            return_nodes = self._resolve_nodes(ec.data.get("zone_return_air_node_or_nodelist_name"))
            # The zone itself is not a vertex, so its boundary nodes are referenced
            # by a single component — that is expected, not suspicious.
            for n in (*inlet_nodes, *exhaust_nodes, *return_nodes):
                self.boundary_nodes.add(n.upper())
            if isinstance(air_node, str) and air_node.strip():
                self.boundary_nodes.add(air_node.strip().upper())
            self.zones.append(
                _ZoneBuild(
                    name=zname,
                    air_node=air_node if isinstance(air_node, str) else None,
                    inlet_nodes=inlet_nodes,
                    exhaust_nodes=exhaust_nodes,
                    return_nodes=return_nodes,
                    equipment_keys=equipment_keys,
                )
            )

    def _zone_equipment_keys(self, eqlist_name: object, zone_name: str) -> list[str]:
        """Resolve a zone's equipment list to vertex keys, tagging each with the zone."""
        keys: list[str] = []
        if not isinstance(eqlist_name, str) or "ZoneHVAC:EquipmentList" not in self.present:
            return keys
        eqlist = self.doc.get_collection("ZoneHVAC:EquipmentList").get(eqlist_name)
        if eqlist is None:
            return keys
        for item in eqlist.extensible_items():
            ct = item.get("zone_equipment_object_type")
            cn = item.get("zone_equipment_name")
            if not isinstance(ct, str) or not isinstance(cn, str):
                continue
            for key in self._resolve_equipment_keys(ct, cn):
                keys.append(key)
                vb = self.vertices.get(key)
                if vb is not None:
                    vb.zone = zone_name
        return keys

    def _resolve_equipment(self, obj_type: str, name: str) -> str:
        """Resolve a ZoneHVAC:AirDistributionUnit to its contained air terminal."""
        if obj_type == "ZoneHVAC:AirDistributionUnit" and "ZoneHVAC:AirDistributionUnit" in self.present:
            adu = self.doc.get_collection("ZoneHVAC:AirDistributionUnit").get(name)
            if adu is not None:
                tt = adu.data.get("air_terminal_object_type")
                tn = adu.data.get("air_terminal_name")
                if isinstance(tt, str) and isinstance(tn, str):
                    return _vkey(tt, tn)
        return _vkey(obj_type, name)

    def _resolve_equipment_keys(self, obj_type: str, name: str) -> list[str]:
        """Resolve a zone-equipment entry to the vertex key(s) representing it.

        ADUs resolve to their contained terminal; compound containers (unitary
        systems, zone forced-air units) expand to their internal fan/coils so the
        unit is not a dead box.
        """
        if is_expandable_container(obj_type, self._group(obj_type)):
            child_keys = [
                _vkey(ct, cn)
                for ct, cn in self._container_children(obj_type, name)
                if self.vertices.get(_vkey(ct, cn)) is not None
            ]
            if child_keys:
                return child_keys
        return [self._resolve_equipment(obj_type, name)]

    def _pass_vrf(self) -> None:
        """Link each VRF outdoor unit to its terminal-unit coils (refrigerant net).

        VRF couples its condensing unit to the zone terminal units through a named
        ``ZoneTerminalUnitList``, not through air/water nodes — so it is tracked as
        a separate refrigerant edge from the master to each terminal's DX coil.
        """
        for master_type in (t for t in self.present if t.startswith(_VRF_MASTER_PREFIX)):
            for ac in self._objs(master_type):
                master = self._vertex(master_type, ac.name)
                for tu_name in self._vrf_terminal_unit_names(ac.data.get("zone_terminal_unit_list_name")):
                    for coil_key in self._vrf_terminal_coils(tu_name):
                        self.refrigerant_links.append((master.key, coil_key))

    def _vrf_terminal_unit_names(self, list_name: object) -> list[str]:
        # ZoneTerminalUnitList's identifier is the ``zone_terminal_unit_list_name``
        # field (not a standard ``name``), so match on the field rather than .get().
        if not isinstance(list_name, str) or not list_name.strip():
            return []
        want = list_name.strip().upper()
        names: list[str] = []
        for lst in self._objs("ZoneTerminalUnitList"):
            field_name = lst.data.get("zone_terminal_unit_list_name")
            if not isinstance(field_name, str) or field_name.strip().upper() != want:
                continue
            for item in lst.extensible_items():
                n = item.get("zone_terminal_unit_name")
                if isinstance(n, str) and n.strip():
                    names.append(n.strip())
        return names

    def _vrf_terminal_coils(self, tu_name: str) -> list[str]:
        """Vertex keys of a VRF terminal unit's DX cooling/heating coils."""
        if _VRF_TERMINAL_TYPE not in self.present:
            return []
        tu = self.doc.get_collection(_VRF_TERMINAL_TYPE).get(tu_name)
        if tu is None:
            return []
        coils = (_vkey(ct, cn) for ct, cn in child_component_refs(tu, self.schema) if ct in _VRF_COIL_TYPES)
        return [k for k in coils if self.vertices.get(k) is not None]

    def _pass_air_demand(self) -> None:
        air_loops = [lb for lb in self.loops if lb.is_air]
        # Supply/return paths -> air-loop demand membership for their junction components.
        for sp in self._objs("AirLoopHVAC:SupplyPath"):
            loop_id = self._airloop_for(sp.data.get("supply_air_path_inlet_node_name"), demand_inlet=True)
            self._assign_path_components(sp, loop_id)
        for rp in self._objs("AirLoopHVAC:ReturnPath"):
            loop_id = self._airloop_for(rp.data.get("return_air_path_outlet_node_name"), demand_inlet=False)
            self._assign_path_components(rp, loop_id)
        # Terminals: assign to the air loop whose demand junctions feed their inlet.
        loop_supply_outlets = self._loop_demand_junction_outlets()
        single_air = air_loops[0].loop_id if len(air_loops) == 1 else None
        for vb in self.vertices.values():
            if vb.category != "terminal" or vb.memberships:
                continue
            assigned = False
            for loop_id, outlet_keys in loop_supply_outlets.items():
                if any(nk in outlet_keys for nk in vb.inlets):
                    self._member(vb, loop_id, "demand")
                    assigned = True
                    break
            if not assigned and single_air is not None:
                self._member(vb, single_air, "demand")
        self._attach_terminal_children()

    def _attach_terminal_children(self) -> None:
        """Pull an air terminal's reheat coil onto the terminal's air-loop side.

        A single-loop reheat coil (electric/gas) inside an ``AirTerminal:*:Reheat``
        would otherwise have no membership and land in "Other equipment"; a water
        reheat coil already on a plant branch simply gains the air-demand side too.
        """
        for vb in list(self.vertices.values()):
            if vb.category != "terminal" or not vb.memberships or vb.obj_type not in self.present:
                continue
            terminal = self.doc.get_collection(vb.obj_type).get(vb.name)
            if terminal is None:
                continue
            pm = vb.memberships[0]
            for ct, cn in child_component_refs(terminal, self.schema):
                child = self.vertices.get(_vkey(ct, cn))
                if child is not None:
                    self._member(child, pm.loop_id, pm.side)
                    if child.zone is None:
                        child.zone = vb.zone

    def _assign_path_components(self, path: IDFObject, loop_id: str | None) -> None:
        if loop_id is None:
            return
        for item in path.extensible_items():
            ct = item.get("component_object_type")
            cn = item.get("component_name")
            if isinstance(ct, str) and isinstance(cn, str):
                vb = self.vertices.get(_vkey(ct, cn))
                if vb is not None:
                    self._member(vb, loop_id, "demand")

    def _airloop_for(self, node: object, *, demand_inlet: bool) -> str | None:
        if not isinstance(node, str) or not node.strip():
            return None
        nk = node.strip().upper()
        for lb in self.loops:
            if not lb.is_air:
                continue
            pool = lb.demand_inlets if demand_inlet else lb.demand_outlets
            if nk in pool:
                return lb.loop_id
        return None

    def _loop_demand_junction_outlets(self) -> dict[str, set[str]]:
        out: dict[str, set[str]] = {}
        for vb in self.vertices.values():
            if vb.category != "junction":
                continue
            for m in vb.memberships:
                if m.side == "demand":
                    out.setdefault(m.loop_id, set()).update(vb.outlets)
        return out

    # -- assembly ----------------------------------------------------------

    def build(self) -> HVACGraph:
        self._pass_loops()
        self._pass_components()
        self._pass_branches()
        self._pass_node_junctions()
        self._pass_connectors()
        self._pass_oa_systems()
        self._collect_oa_boundary()
        self._pass_zones()
        self._pass_vrf()
        self._pass_air_demand()
        return self._finalize()

    def _finalize(self) -> HVACGraph:
        producers: dict[str, list[str]] = {}
        consumers: dict[str, list[str]] = {}
        for vb in self.vertices.values():
            for nk in vb.outlets:
                producers.setdefault(self._find(nk), []).append(vb.key)
            for nk in vb.inlets:
                consumers.setdefault(self._find(nk), []).append(vb.key)

        edges = self._build_edges(producers, consumers)
        connected: set[str] = set()
        for e in edges:
            connected.add(e.src)
            connected.add(e.dst)

        vertices = tuple(
            HVACVertex(
                key=vb.key,
                obj_type=vb.obj_type,
                name=vb.name,
                category=vb.category,
                inlet_nodes=tuple(vb.inlets[nk] for nk in vb.inlets),
                outlet_nodes=tuple(vb.outlets[nk] for nk in vb.outlets),
                memberships=tuple(vb.memberships),
                zone=vb.zone,
            )
            for vb in sorted(self.vertices.values(), key=lambda v: v.key)
        )

        nodes = self._build_nodes(producers, consumers)
        loops = self._build_loops()
        zones = self._build_zones()
        refrigerant = self._build_refrigerant_edges()
        # A VRF outdoor unit and its terminal coils are connected by refrigerant,
        # not nodes — exclude them from the node-based "unconnected" check.
        refrigerant_keys = {k for r in refrigerant for k in (r.master_key, r.terminal_key)}
        self._add_topology_warnings(producers, consumers, connected | refrigerant_keys)

        return HVACGraph(
            version=self.doc.version,
            loops=loops,
            vertices=vertices,
            nodes=nodes,
            edges=edges,
            zones=zones,
            warnings=tuple(self.warnings),
            refrigerant_edges=refrigerant,
            _by_key={v.key: v for v in vertices},
        )

    def _build_refrigerant_edges(self) -> tuple[HVACRefrigerantEdge, ...]:
        seen: set[tuple[str, str]] = set()
        out: list[HVACRefrigerantEdge] = []
        for master_key, terminal_key in self.refrigerant_links:
            marker = (master_key, terminal_key)
            if marker in seen:
                continue
            seen.add(marker)
            out.append(HVACRefrigerantEdge(master_key=master_key, terminal_key=terminal_key))
        return tuple(out)

    def _build_edges(self, producers: dict[str, list[str]], consumers: dict[str, list[str]]) -> tuple[HVACEdge, ...]:
        edges: list[HVACEdge] = []
        seen: set[tuple[str, str, str]] = set()
        for nk in sorted(producers):
            dsts = consumers.get(nk)
            if not dsts:
                continue
            display = self.node_display.get(nk, nk)
            fluid = self.node_fluid.get(nk, "unknown")
            for src in sorted(producers[nk]):
                for dst in sorted(dsts):
                    if src == dst:
                        continue
                    marker = (src, dst, nk)
                    if marker in seen:
                        continue
                    seen.add(marker)
                    edges.append(HVACEdge(src=src, dst=dst, via_node=display, fluid_type=fluid))
        return tuple(edges)

    def _build_nodes(self, producers: dict[str, list[str]], consumers: dict[str, list[str]]) -> tuple[HVACNode, ...]:
        all_keys = sorted(set(producers) | set(consumers))
        return tuple(
            HVACNode(
                name=self.node_display.get(nk, nk),
                fluid_type=self.node_fluid.get(nk, "unknown"),
                producers=tuple(sorted(producers.get(nk, []))),
                consumers=tuple(sorted(consumers.get(nk, []))),
            )
            for nk in all_keys
        )

    def _build_loops(self) -> tuple[HVACLoop, ...]:
        supply: dict[str, list[str]] = {}
        demand: dict[str, list[str]] = {}
        for vb in self.vertices.values():
            for m in vb.memberships:
                bucket = supply if m.side == "supply" else demand
                bucket.setdefault(m.loop_id, []).append(vb.key)
        ordered = sorted(self.loops, key=lambda lb: (_LOOP_ORDER[lb.loop_type], lb.name))
        return tuple(
            HVACLoop(
                loop_id=lb.loop_id,
                name=lb.name,
                loop_type=lb.loop_type,
                supply_keys=tuple(sorted(supply.get(lb.loop_id, []))),
                demand_keys=tuple(sorted(demand.get(lb.loop_id, []))),
            )
            for lb in ordered
        )

    def _build_zones(self) -> tuple[HVACZone, ...]:
        return tuple(
            HVACZone(
                name=z.name,
                air_node=z.air_node,
                inlet_nodes=tuple(z.inlet_nodes),
                exhaust_nodes=tuple(z.exhaust_nodes),
                return_nodes=tuple(z.return_nodes),
                equipment_keys=tuple(z.equipment_keys),
            )
            for z in sorted(self.zones, key=lambda z: z.name)
        )

    def _add_topology_warnings(
        self, producers: dict[str, list[str]], consumers: dict[str, list[str]], connected: set[str]
    ) -> None:
        for nk in sorted(set(producers) | set(consumers)):
            if nk in self.boundary_nodes:
                continue
            refs = set(producers.get(nk, [])) | set(consumers.get(nk, []))
            if len(refs) == 1:
                display = self.node_display.get(nk, nk)
                self.warnings.append(
                    HVACWarning("suspicious_node", f"Node '{display}' is referenced by only one component", display)
                )
        for vb in sorted(self.vertices.values(), key=lambda v: v.key):
            if vb.key not in connected:
                self.warnings.append(
                    HVACWarning("unconnected_component", f"{vb.obj_type} '{vb.name}' has no connections", vb.key)
                )


def build_hvac_graph(doc: IDFDocument, *, expand: bool = False) -> HVACGraph:
    """Build an :class:`~.model.HVACGraph` from an expanded document.

    Args:
        doc: The model to diagram. It must be *expanded* — free of
            ``HVACTemplate:*`` objects, which are not real HVAC topology.
        expand: When ``True`` and the document still contains templates, run
            :meth:`idfkit.IDFDocument.expand` first (requires an EnergyPlus
            installation). When ``False`` (default), unexpanded templates raise
            :class:`~idfkit.exceptions.HVACDiagramError`.

    Returns:
        The reconstructed HVAC graph. Inspect :attr:`HVACGraph.warnings` for
        non-fatal issues (dangling nodes, unconnected components, ...).

    Raises:
        HVACDiagramError: If the document still contains ``HVACTemplate:*``
            objects and ``expand`` is ``False``.
    """
    templates = hvac_template_types(doc)
    if templates:
        if not expand:
            raise HVACDiagramError(templates)
        doc = doc.expand()
        remaining = hvac_template_types(doc)
        if remaining:
            raise HVACDiagramError(remaining, after_expand=True)
    return _GraphBuilder(doc).build()
