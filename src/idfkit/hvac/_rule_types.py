"""The row type of the generated connection-rule table (``_port_rules.py``). Internal, not on the wire."""

from __future__ import annotations

from typing import Literal, NamedTuple

from idfkit.hvac.types import ConnectionType, Fluid, Provenance


class PortRule(NamedTuple):
    """How one node field of one object type connects, as EnergyPlus reports it.

    Attributes:
        field: The Python field name. An extensible sub-field is ``group.field`` where ``group`` is
            the schema's extensible wrapper key.
        connection: The connection type.
        stream: The fluid stream, at least 1. Pairs an inlet with an outlet of the same fluid.
        fluid: The fluid on the node.
        is_parent: True when the object is a parent for this field; parent uses add no flow edge.
        accepts_nodelist: True when the field may name a ``NodeList``.
        when: A value predicate ``(field, value)``, compared case-insensitively, or ``None``.
        provenance: Where the rule came from.
    """

    field: str
    connection: ConnectionType
    stream: int
    fluid: Fluid
    is_parent: bool
    accepts_nodelist: bool
    when: tuple[str, str] | None
    provenance: Provenance


class VersionCap(NamedTuple):
    """The most severe a check may be on models of one measured EnergyPlus version (research R-34).

    Attributes:
        code: The check code, for example ``"T011"``.
        version: The measured version.
        max_severity: ``"warning"`` or ``"info"``.
        models: Example files measured.
        false_findings: Findings on those files that a reviewer judged false.
    """

    code: str
    version: tuple[int, int, int]
    max_severity: Literal["warning", "info"]
    models: int
    false_findings: int
