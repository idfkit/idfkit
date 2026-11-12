"""Identity and coverage types shared by the model-graph layers.

``ObjectKey``, ``UncoveredPart`` and ``Coverage`` are used by the HVAC topology (``idfkit.hvac``), result linking
(``idfkit.simulation``) and the combined view (``idfkit.graph``). They live in this private module so
that no layer depends on another for them; each layer re-exports them publicly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from idfkit.objects import IDFObject

PSEUDO_TYPES: frozenset[str] = frozenset({"Node", "Aggregate", "Unresolved"})
"""Object types that are not schema types: a fluid node, a report aggregate, an unresolved result key."""

MAX_EXAMPLES = 3
"""The most examples an ``UncoveredPart`` carries."""

UncoveredKind = Literal["hvac_template", "ems_program", "unclassified_type", "unlinked_result"]


@dataclass(frozen=True, slots=True, eq=False)
class ObjectKey:
    """The identity of a model object, or of a node, aggregate or unresolved result key.

    ``object_type`` is a schema object type or one of the pseudo-types ``"Node"``, ``"Aggregate"``
    and ``"Unresolved"``. ``name`` keeps the model's spelling for display; equality and hashing
    compare both fields case-insensitively, as EnergyPlus does.

    Examples:
        >>> ObjectKey("Zone", "Office") == ObjectKey("ZONE", "OFFICE")
        True
        >>> len({ObjectKey("Zone", "Office"), ObjectKey("zone", "office")})
        1
        >>> ObjectKey("Zone", "Office") == ObjectKey("Node", "Office")
        False
    """

    object_type: str
    name: str

    def _folded(self) -> tuple[str, str]:
        return (self.object_type.upper(), self.name.upper())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ObjectKey):
            return NotImplemented
        return self._folded() == other._folded()

    def __hash__(self) -> int:
        return hash(self._folded())


@dataclass(frozen=True, slots=True)
class UncoveredPart:
    """One kind of thing an answer did not look at.

    Attributes:
        kind: ``"hvac_template"`` (unexpanded ``HVACTemplate:*`` systems), ``"ems_program"``
            (``EnergyManagementSystem:Program`` and ``:Subroutine`` objects), ``"unclassified_type"``
            (object types with node fields but no connection rule) or ``"unlinked_result"`` (result
            items that could not be resolved to an object).
        count: Objects or items of this kind left out.
        examples: At most 3. For ``unlinked_result``, the raw keys as ``ObjectKey("Unresolved", key)``.
        reason: One sentence saying what is not visible because of it.
    """

    kind: UncoveredKind
    count: int
    examples: tuple[ObjectKey, ...]
    reason: str

    def __post_init__(self) -> None:
        if len(self.examples) > MAX_EXAMPLES:
            msg = f"UncoveredPart carries at most {MAX_EXAMPLES} examples, got {len(self.examples)}"
            raise ValueError(msg)
        if self.count < 0:
            msg = f"UncoveredPart.count must not be negative, got {self.count}"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class Coverage:
    """What an answer from the graph covered, and what it did not.

    Attached to every answer that comes from matching, linking, inference or walking, in one shape.

    Attributes:
        partial: True when ``uncovered`` is not empty.
        uncovered: What the answer did not look at. Empty means the whole model was covered.
        resolved: For result linking, the items linked to an object. ``None`` elsewhere.
        unresolved: For result linking, the items left unresolved. ``None`` elsewhere.

    Examples:
        >>> Coverage.of(()).partial
        False
        >>> part = UncoveredPart("ems_program", 1, (ObjectKey("EnergyManagementSystem:Program", "P"),), "Not parsed.")
        >>> Coverage.of((part,)).partial
        True
    """

    partial: bool
    uncovered: tuple[UncoveredPart, ...]
    resolved: int | None = None
    unresolved: int | None = None

    def __post_init__(self) -> None:
        if self.partial != bool(self.uncovered):
            msg = "Coverage.partial must be True exactly when uncovered is not empty"
            raise ValueError(msg)

    @classmethod
    def of(
        cls,
        uncovered: tuple[UncoveredPart, ...],
        *,
        resolved: int | None = None,
        unresolved: int | None = None,
    ) -> Coverage:
        """Build a coverage record, deriving ``partial`` from ``uncovered``."""
        return cls(partial=bool(uncovered), uncovered=uncovered, resolved=resolved, unresolved=unresolved)


def display_name(obj: IDFObject) -> str:
    """The name an object is known by: its name, or for unnamed types the zone or space it serves.

    An unnamed object that serves no zone or space is known by its type.
    """
    if obj.name:
        return obj.name
    for field in ("zone_name", "space_name"):
        value = obj.data.get(field)
        if isinstance(value, str) and value:
            return value
    return obj.obj_type
