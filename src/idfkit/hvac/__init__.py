"""HVAC topology: how the objects of a model connect through their nodes.

A node is a name shared by the fields of the objects it joins; the reference graph never sees it.
This package derives, from the document, every field that names a node, the connection role
EnergyPlus gives that field, the flow edges between components, and what the view could not cover.

The connection roles are read from EnergyPlus's own node connection report (``eplusout.bnd``) for
the 26.2 example files, with the provenance of every rule recorded. Categories come from the object
type alone, never from names.

Example:
    >>> from idfkit import new_document
    >>> from idfkit.hvac import HVACTopology
    >>> doc = new_document()
    >>> coil = doc.add("Coil:Heating:Electric", "Heater", air_inlet_node_name="Mixed Air",
    ...                air_outlet_node_name="Heated Air", validate=False)
    >>> fan = doc.add("Fan:ConstantVolume", "Fan", air_inlet_node_name="Heated Air",
    ...               air_outlet_node_name="Supply Air", validate=False)
    >>> topo = HVACTopology.from_document(doc)
    >>> [e.target.name for e in topo.downstream(coil, hops=1)]
    ['Fan']
"""

from __future__ import annotations

from idfkit._graph_common import Coverage, ObjectKey, UncoveredPart
from idfkit.hvac._categories import category_of
from idfkit.hvac.topology import HVACTopology
from idfkit.hvac.types import (
    ComponentCategory,
    ConnectionType,
    FlowEdge,
    Fluid,
    LoopMembership,
    NodeRenameResult,
    NodeUse,
    TopologyFinding,
)

__all__ = [
    "ComponentCategory",
    "ConnectionType",
    "Coverage",
    "FlowEdge",
    "Fluid",
    "HVACTopology",
    "LoopMembership",
    "NodeRenameResult",
    "NodeUse",
    "ObjectKey",
    "TopologyFinding",
    "UncoveredPart",
    "category_of",
]
