"""Public types of the HVAC topology view.

The dataclasses here are the *returned* shape. :class:`~idfkit.hvac.HVACTopology` stores compact
integer-indexed tuples and builds these only for the items a call returns (research R-21).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Literal

from idfkit._graph_common import ObjectKey

Provenance = Literal["eplus_examples", "eplus_test_model", "hand_written"]
"""Where a connection rule came from.

``eplus_examples`` and ``eplus_test_model`` rules were read from EnergyPlus's own connection report
(``eplusout.bnd``) for the 26.2 example files or for a minimal test model. ``hand_written`` rules
were not, and a finding that relies on one is never an error.
"""

Severity = Literal["error", "warning", "info"]
LoopKind = Literal["air", "plant", "condenser", "zone_equipment"]
LoopSide = Literal["supply", "demand"]
FlowEdgeKind = Literal["component", "branch_junction", "zone"]


class ConnectionType(str, Enum):
    """How an object uses a node, mirroring EnergyPlus's node connection types.

    Flow roles are ``Inlet``, ``Outlet``, ``ZoneInlet``, ``ZoneReturn`` and ``ZoneExhaust``.
    Control roles are ``Sensor``, ``Actuator`` and ``Setpoint``. Boundary roles are ``OutsideAir``
    and ``ReliefAir``.
    """

    INLET = "Inlet"
    OUTLET = "Outlet"
    INTERNAL = "Internal"
    ZONE_NODE = "ZoneNode"
    SENSOR = "Sensor"
    ACTUATOR = "Actuator"
    OUTSIDE_AIR = "OutsideAir"
    RELIEF_AIR = "ReliefAir"
    ZONE_INLET = "ZoneInlet"
    ZONE_RETURN = "ZoneReturn"
    ZONE_EXHAUST = "ZoneExhaust"
    SETPOINT = "Setpoint"


class Fluid(str, Enum):
    """The fluid a node carries, as EnergyPlus reports it."""

    AIR = "Air"
    WATER = "Water"
    STEAM = "Steam"
    REFRIGERANT = "Refrigerant"
    UNKNOWN = "Unknown"


class ComponentCategory(str, Enum):
    """The kind of component an object is, from its object type alone (research R-36).

    The vocabulary is closed within a release; adding a member is a minor change. A type the
    category table does not list is ``other``. Categories never come from object names.
    """

    HEATING_COIL = "heating_coil"
    COOLING_COIL = "cooling_coil"
    FAN = "fan"
    PUMP = "pump"
    TERMINAL_UNIT = "terminal_unit"
    CHILLER = "chiller"
    BOILER = "boiler"
    HEAT_REJECTION = "heat_rejection"
    HUMIDIFIER = "humidifier"
    HEAT_EXCHANGER = "heat_exchanger"
    ZONE_EQUIPMENT = "zone_equipment"
    UNITARY = "unitary"
    OUTDOOR_AIR = "outdoor_air"
    SETPOINT_MANAGER = "setpoint_manager"
    CONTROLLER = "controller"
    OTHER = "other"


@dataclass(frozen=True, slots=True)
class NodeUse:
    """One field of one object naming a node.

    Attributes:
        node: The node name in the model's spelling.
        object: The object whose field names the node.
        category: The owner's component category.
        field: The Python field name. An extensible sub-field is ``group.field``.
        connection: The connection type, or ``None`` when no rule classifies the field.
        stream: The fluid stream number, pairing an inlet with an outlet of the same fluid.
        fluid: The fluid on the node. For a parent object or a control use, which can sit on air or
            water, it is the fluid the components moving flow through the node give it.
        is_parent: True for a parent object, whose nodes repeat its children's and add no flow edge.
        via_nodelist: The ``NodeList`` name when the field names a list that contains the node.
        rule: ``"ems_key"`` for an EMS sensor or actuator use, ``None`` for a port rule.
        provenance: Where the rule came from. ``None`` when unclassified.
    """

    node: str
    object: ObjectKey
    category: ComponentCategory
    field: str
    connection: ConnectionType | None
    stream: int
    fluid: Fluid
    is_parent: bool
    via_nodelist: str | None = None
    rule: str | None = None
    provenance: Provenance | None = None


@dataclass(frozen=True, slots=True)
class LoopMembership:
    """One loop a component sits on.

    Attributes:
        loop: The ``AirLoopHVAC``, ``PlantLoop`` or ``CondenserLoop``, or the
            ``ZoneHVAC:EquipmentConnections`` for zone equipment.
        kind: ``"air"``, ``"plant"``, ``"condenser"`` or ``"zone_equipment"``.
        side: ``"supply"`` or ``"demand"``; ``None`` for zone equipment.
        branch: The branch the component is listed on, when it is on one.
        position: The 0-based index of the component on that branch.
        stream: The component's fluid stream that carries this membership.
    """

    loop: ObjectKey
    kind: LoopKind
    side: LoopSide | None
    branch: ObjectKey | None
    position: int | None
    stream: int


@dataclass(frozen=True, slots=True)
class FlowEdge:
    """A flow connection between two non-parent components, or a component and a zone, through one node.

    Attributes:
        source: The upstream component or zone.
        target: The downstream component or zone.
        node: The node they share, in the model's spelling.
        fluid: The fluid on the node.
        kind: ``"component"``, ``"branch_junction"`` (through a splitter or mixer between branches)
            or ``"zone"``.
    """

    source: ObjectKey
    target: ObjectKey
    node: str
    fluid: Fluid
    kind: FlowEdgeKind


@dataclass(frozen=True, slots=True)
class TopologyFinding:
    """A connection finding from the static checks.

    Attributes:
        code: Stable check code, for example ``"T010"``.
        severity: The effective severity, after the version cap. Only qualified codes are ever
            ``"error"``.
        objects: The objects involved. At least one, unless ``node`` is set.
        message: One sentence naming what is wrong.
        provenance: The weakest provenance among the rules the finding relied on.
        node: The node involved, in the model's spelling.
        field: The field involved.
        expected: For a mismatch, what the other side says.
        actual: For a mismatch, what the object itself says.
        capped_from: ``"error"`` when the model's version capped the severity.
        cap_reason: Why the version cap applied.
    """

    code: str
    severity: Severity
    objects: tuple[ObjectKey, ...]
    message: str
    provenance: Provenance
    node: str | None = None
    field: str | None = None
    expected: str | None = None
    actual: str | None = None
    capped_from: Literal["error"] | None = None
    cap_reason: str | None = None

    def __post_init__(self) -> None:
        if not self.objects and self.node is None:
            msg = "A TopologyFinding names at least one object or a node"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class NodeRenameResult:
    """What :meth:`IDFDocument.rename_node <idfkit.document.IDFDocument.rename_node>` changed.

    Attributes:
        old: The node name before the rename.
        new: The node name after it.
        fields_updated: Node fields and ``NodeList`` entries rewritten.
        objects: The objects whose fields changed.
    """

    old: str
    new: str
    fields_updated: int
    objects: tuple[ObjectKey, ...]
