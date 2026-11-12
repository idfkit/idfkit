"""The integer structures of a topology view, handed to the checks (internal).

``HVACTopology`` builds this from its own fields and passes it to ``idfkit.hvac.checks``, so the
checks run over the same integer structures as the view without reaching into its private state.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from idfkit._graph_common import Coverage, ObjectKey
    from idfkit.document import IDFDocument
    from idfkit.hvac.types import ComponentCategory
    from idfkit.objects import IDFObject

Use = tuple[int, int, int, int, "str | None"]
"""``(object or node id, meta id, connection code, stream, NodeList name or None)``."""

Meta = tuple[str, int, bool, "int | None", "str | None"]
"""``(field, fluid code, is_parent, provenance code or None, rule tag or None)``."""


class TopologyIndex(NamedTuple):
    doc: IDFDocument
    node_name: list[str]
    node_id: dict[str, int]
    uses: list[list[Use]]
    """Per node id."""
    obj: list[IDFObject]
    obj_key: list[ObjectKey]
    obj_cat: list[ComponentCategory]
    obj_uses: list[list[Use]]
    """Per object id; the first element of each use is a node id."""
    meta: list[Meta]
    loop_nodes: frozenset[int]
    """Node ids a loop object names: loop inlets and outlets, joined inside the loop."""
    coverage: Coverage
