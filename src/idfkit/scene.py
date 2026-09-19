"""Resolve a model's geometry into one frame, without changing the model.

``get_scene(doc)`` reads a document and returns a :class:`Scene`: every surface it could place, in
world coordinates with the building rotation applied, plus what it could not place and what it did
not attempt. It modifies nothing.

WHY THIS IS A NEW MODULE AND NOT AN ADDITION TO ``geometry.py``

``geometry.py`` is the authoring and calculation surface, and it is already long. Nothing here
authors. The one function there this module is related to is ``translate_to_world``, which mutates
the document by design and is corrected to the same rule this module establishes.

THE RULE, WHICH WAS MEASURED RATHER THAN REASONED

Three clauses, in this order, against the engine's own vertex report over 17 models and 532
surfaces:

1. **Only when the model declares the relative system**, rotate each surface by its zone's
   ``direction_of_relative_north`` and then translate it by the zone's origin. The condition is not
   a nicety: twelve of the example models declare ``World`` and carry a non-zero zone origin
   anyway, and applying it displaces every surface in them.
2. **Rotate the whole resolved building** by ``Building.north_axis``, about the world origin, in the
   engine's sense. That sense is clockwise seen from above, so it is the negation of a
   counter-clockwise rotation. Applying it per surface inside its own zone frame instead leaves the
   zone layout unrotated, which is what ``translate_to_world`` does today: every surface correctly
   oriented and every zone in the wrong place, a drawing that passes an eyeball test at up to
   201.98 m of error.
3. **Reverse the vertex order** when the model declares clockwise entry, so that the right-hand
   rule gives the outward normal in every model.

Candidate rules and their agreement with the engine:

===================================================  ====================  ===========
candidate                                            models within 0.01 m  worst error
===================================================  ====================  ===========
the rule in ``_resolve_surfaces``                     5/17                  201.98 m
the rule in ``translate_to_world``                    5/17                  201.98 m
coordinate system read, north axis applied per        8/17                  201.98 m
surface
coordinate system read, north axis applied to the     14/17                 17.59 m
building
all three clauses, compared as rings                  **17/17**             **0.0045 m**
===================================================  ====================  ===========

WHAT IS NOT DONE, AND IS NOT AN OVERSIGHT

The **starting vertex is not renormalised**. The engine's report begins every surface at its
upper-left corner, and matching that would mean discarding the author's ordering to reproduce a
reporting convention. The corpus check carries a fixture whose whole purpose is to fail if someone
adds it.

The **simplified surface family** (``Wall:Exterior``, ``Window``, ``Roof`` and their siblings) is
not read. Those types are keyed on origin, width, height and tilt rather than on vertices and need
their own rule. They are reported in :attr:`Scene.unattempted` so that a model made of them looks
different from a model with no geometry at all.

The **zone multiplier is not expanded**. It is a simulation instruction, and the engine's own report
does not repeat those surfaces either.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Final, Literal, cast

from .geometry import Polygon3D, Vector3D, get_surface_coords

if TYPE_CHECKING:
    from .document import IDFDocument
    from .objects import IDFCollection, IDFObject
    from .schema import EpJSONSchema

__all__ = [
    "AppliedRules",
    "ResolvedSurface",
    "Scene",
    "SceneBounds",
    "UnattemptedType",
    "UnresolvedObject",
    "get_scene",
]

#: The detailed heat transfer surface, its fenestration, and the three detailed shading forms. These
#: are the types this slice reads, and every one of them states its geometry as explicit vertices.
_HEAT_TRANSFER: Final = "BuildingSurface:Detailed"
_FENESTRATION: Final = "FenestrationSurface:Detailed"
_SHADING: Final = (
    "Shading:Site:Detailed",
    "Shading:Building:Detailed",
    "Shading:Zone:Detailed",
)
_READ: Final = (_HEAT_TRANSFER, _FENESTRATION, *_SHADING)

#: Geometry types this slice does not read, reported rather than skipped. The simplified family
#: states a surface as an origin, a width, a height and a tilt, which is a second rule set and a
#: second oracle, deferred rather than forgotten.
_UNREAD: Final = (
    "Wall:Exterior",
    "Wall:Adiabatic",
    "Wall:Interzone",
    "Wall:Underground",
    "Roof",
    "Ceiling:Adiabatic",
    "Ceiling:Interzone",
    "Floor:Adiabatic",
    "Floor:Interzone",
    "Floor:GroundContact",
    "Window",
    "Door",
    "GlazedDoor",
    "Window:Interzone",
    "Door:Interzone",
    "GlazedDoor:Interzone",
    "Shading:Site",
    "Shading:Building",
    "Shading:Overhang",
    "Shading:Overhang:Projection",
    "Shading:Fin",
    "Shading:Fin:Projection",
)

#: What EnergyPlus assumes when ``GlobalGeometryRules`` does not say. The object is required in
#: practice, so these are what a partial model is read as rather than a documented default, and
#: every one of them is recorded in :attr:`AppliedRules.defaulted` when it is used.
_DEFAULT_RULES: Final = {
    "starting_vertex_position": "UpperLeftCorner",
    "vertex_entry_direction": "Counterclockwise",
    "coordinate_system": "Relative",
}

Reason = Literal["too-few-vertices", "zone-not-found", "parent-surface-not-found", "no-vertices"]


@dataclass(frozen=True, slots=True)
class AppliedRules:
    """What resolution read from the model, and what it had to assume."""

    coordinate_system: str
    vertex_entry_direction: str
    starting_vertex_position: str
    north_axis: float
    defaulted: tuple[str, ...] = ()

    @property
    def is_relative(self) -> bool:
        """Whether zone origins and zone rotations apply, which is clause one's condition."""
        return self.coordinate_system.casefold() == "relative"

    @property
    def is_clockwise(self) -> bool:
        """Whether the author entered vertices clockwise, which clause three reverses."""
        return self.vertex_entry_direction.casefold().startswith("clockwise")


@dataclass(frozen=True, slots=True)
class SceneBounds:
    """The box enclosing every resolved vertex, and no more."""

    min: Vector3D
    max: Vector3D


@dataclass(frozen=True, slots=True)
class ResolvedSurface:
    """One surface, placed.

    ``object_type`` together with ``name`` is the address. A name alone is not unique across types,
    and a consumer that must search the document by name to find what its user selected has been
    handed a picture rather than a view of the model.
    """

    object_type: str
    name: str
    polygon: Polygon3D
    zone: str = ""
    surface_type: str = ""
    boundary: str = ""
    construction: str = ""
    parent_surface: str | None = None
    is_shading: bool = False

    @property
    def normal(self) -> Vector3D:
        """The outward normal, signed by the declared entry direction."""
        return self.polygon.normal

    @property
    def area(self) -> float:
        """The area of the resolved polygon."""
        return self.polygon.area


@dataclass(frozen=True, slots=True)
class UnresolvedObject:
    """A geometry object that could not be placed, and why.

    The reason is an enumeration rather than a message, so that a consumer can group on it and a
    reworded string does not change behaviour.
    """

    object_type: str
    name: str
    reason: Reason


@dataclass(frozen=True, slots=True)
class UnattemptedType:
    """A geometry type present in the model that this slice does not read."""

    object_type: str
    count: int


@dataclass(frozen=True, slots=True)
class Scene:
    """A model's geometry, resolved into one frame.

    All three lists are in document order. The corpus compares ``unresolved`` and ``unattempted`` as
    sets, because neither carries a semantically meaningful order; that is a statement about what
    counts as equal and not permission for the producer to vary. A list that reorders between runs
    is a flickering interface and an unreadable diff, and ordering costs nothing here because
    resolution already walks the document in order.
    """

    surfaces: tuple[ResolvedSurface, ...] = ()
    bounds: SceneBounds | None = None
    applied: AppliedRules = field(
        default_factory=lambda: AppliedRules("Relative", "Counterclockwise", "UpperLeftCorner", 0.0)
    )
    unresolved: tuple[UnresolvedObject, ...] = ()
    unattempted: tuple[UnattemptedType, ...] = ()


# ---------------------------------------------------------------------------
# Reading what the model declares
# ---------------------------------------------------------------------------


def _number(obj: IDFObject | None, name: str) -> float:
    """One numeric field, treating absent and blank alike as zero."""
    if obj is None:
        return 0.0
    try:
        return float(obj.data.get(name) or 0.0)
    except (TypeError, ValueError):
        return 0.0


def _objects(doc: IDFDocument, object_type: str) -> list[IDFObject]:
    """Every object of one type, or nothing when the document holds none of them."""
    if object_type not in doc:
        return []
    return list(cast("IDFCollection[IDFObject]", doc[object_type]))


def _first(doc: IDFDocument, object_type: str) -> IDFObject | None:
    """The first object of a type, or None. Singletons here, so first is the one."""
    found = _objects(doc, object_type)
    return found[0] if found else None


def _canonical(schema: EpJSONSchema | None, object_type: str, field_name: str, value: object) -> str:
    """One enumerated field in the schema's spelling.

    EnergyPlus matches these without regard to case, so the example set holds ``Wall``, ``WALL`` and
    ``wall`` for one type. Reporting the schema's spelling is not a claim about the document: the
    schema defines the value, and reporting the author's would hand every consumer the same case
    fold to write and show three kinds of wall in three colours.

    A value outside the enumeration passes through as itself (FR-012b), because a category invented
    for it would say something the model does not.
    """
    text = "" if value is None else str(value).strip()
    if not text or schema is None:
        return text
    field_schema = schema.get_field_schema(object_type, field_name) or {}
    permitted_values: object = field_schema.get("enum")
    if not isinstance(permitted_values, list):
        return text
    for permitted in cast("list[object]", permitted_values):
        if permitted and str(permitted).casefold() == text.casefold():
            return str(permitted)
    return text


def _read_rules(doc: IDFDocument) -> AppliedRules:
    """Read ``GlobalGeometryRules`` and ``Building``, recording what had to be assumed."""
    rules = _first(doc, "GlobalGeometryRules")
    building = _first(doc, "Building")
    schema = doc.schema

    declared: dict[str, str] = {}
    defaulted: list[str] = []
    for name, fallback in _DEFAULT_RULES.items():
        value = _canonical(schema, "GlobalGeometryRules", name, rules.data.get(name) if rules else None)
        if not value:
            value = fallback
            defaulted.append(name)
        declared[name] = value
    if building is None:
        defaulted.append("north_axis")

    return AppliedRules(
        coordinate_system=declared["coordinate_system"],
        vertex_entry_direction=declared["vertex_entry_direction"],
        starting_vertex_position=declared["starting_vertex_position"],
        north_axis=_number(building, "north_axis"),
        defaulted=tuple(defaulted),
    )


# ---------------------------------------------------------------------------
# The three clauses
# ---------------------------------------------------------------------------


def _place(polygon: Polygon3D, zone: IDFObject | None, rules: AppliedRules) -> Polygon3D:
    """Apply clause one and clause two to one polygon.

    Clause one is conditional on the declared coordinate system, which is the whole reason the
    twelve world models with a non-zero zone origin come out right. Clause two is unconditional and
    is applied about the world origin, so that the building turns as one body.

    The north axis is negated because EnergyPlus measures it clockwise from true north, while
    ``rotate_z`` turns counter-clockwise.
    """
    placed = polygon
    if rules.is_relative and zone is not None:
        relative_north = _number(zone, "direction_of_relative_north")
        if relative_north:
            placed = placed.rotate_z(-relative_north, anchor=Vector3D.origin())
        origin = Vector3D(_number(zone, "x_origin"), _number(zone, "y_origin"), _number(zone, "z_origin"))
        if origin != Vector3D.origin():
            placed = placed.translate(origin)
    if rules.north_axis:
        placed = placed.rotate_z(-rules.north_axis, anchor=Vector3D.origin())
    return placed


def _wind(polygon: Polygon3D, rules: AppliedRules) -> Polygon3D:
    """Apply clause three: the author's ring, reversed when the model declares clockwise entry.

    THE FIRST VERTEX STAYS WHERE THE AUTHOR PUT IT.

    Reversing the whole list would send the last vertex to the front, which renormalises the
    starting vertex as a side effect of normalising the orientation. FR-008 forbids exactly that,
    and the corpus cannot catch it: the ring comparison is rotation-insensitive by design, so both
    forms pass. So the head is held and the tail reversed, which is the same ring traversed the
    other way from the same corner.
    """
    if not rules.is_clockwise:
        return polygon
    head, *tail = polygon.vertices
    return Polygon3D([head, *reversed(tail)])


# ---------------------------------------------------------------------------
# Walking the document
# ---------------------------------------------------------------------------


def _in_document_order(doc: IDFDocument, object_types: tuple[str, ...]) -> list[IDFObject]:
    """Every object of the given types, in the order the document states them.

    ``region_of`` gives the byte offset of an object that was parsed from text, which is document
    order exactly. A document built programmatically has no text and no offsets, so those objects
    fall back to the order their collections hold them in, after everything that does have an
    offset. Both are deterministic, which is what the stable-order guarantee actually needs; the
    first is also literally the file's order, which is what makes a diff readable.
    """
    placed: list[tuple[int, int, IDFObject]] = []
    unplaced: list[tuple[int, int, IDFObject]] = []
    for type_index, object_type in enumerate(object_types):
        for position, obj in enumerate(_objects(doc, object_type)):
            span = doc.region_of(obj)
            if span is None:
                unplaced.append((type_index, position, obj))
            else:
                placed.append((span.start, 0, obj))
    placed.sort(key=lambda row: row[0])
    unplaced.sort(key=lambda row: (row[0], row[1]))
    return [obj for _, _, obj in placed] + [obj for _, _, obj in unplaced]


def _zone_of(surface: IDFObject) -> str:
    """The zone a surface names, under whichever of the two field names its type uses."""
    for name in ("zone_name", "zone_or_zonelist_name", "base_surface_name"):
        value = surface.data.get(name)
        if value:
            return str(value)
    return ""


def _resolve_one(
    surface: IDFObject,
    zones: Mapping[str, IDFObject],
    rules: AppliedRules,
    schema: EpJSONSchema | None,
    surfaces_by_name: Mapping[str, IDFObject],
) -> ResolvedSurface | UnresolvedObject:
    """Place one surface, or say why it could not be placed.

    Never raises and never skips. A building with one bad wall is still a building a reader wants to
    see, so an object that cannot be placed becomes an entry rather than an exception.
    """
    object_type = surface.obj_type
    name = surface.name
    is_shading = object_type in _SHADING
    is_fenestration = object_type == _FENESTRATION

    polygon = get_surface_coords(surface)
    if polygon is None:
        vertices = surface.data.get("vertices")
        reason: Reason = "no-vertices" if not vertices else "too-few-vertices"
        return UnresolvedObject(object_type, name, reason)

    parent_surface: str | None = None
    if is_fenestration:
        parent_surface = str(surface.data.get("building_surface_name") or "")
        parent = surfaces_by_name.get(parent_surface.upper())
        if parent is None:
            return UnresolvedObject(object_type, name, "parent-surface-not-found")
        # Fenestration is stated in its parent's frame, so it resolves against the parent's zone.
        zone_name = _zone_of(parent)
    elif object_type == "Shading:Zone:Detailed":
        # Attached to a base surface rather than to a zone, so it inherits that surface's zone.
        base = surfaces_by_name.get(str(surface.data.get("base_surface_name") or "").upper())
        zone_name = _zone_of(base) if base is not None else ""
    elif is_shading:
        # Site and building shading are stated in world coordinates and belong to no zone.
        zone_name = ""
    else:
        zone_name = _zone_of(surface)

    zone = zones.get(zone_name.upper()) if zone_name else None
    if zone_name and zone is None and not is_shading:
        return UnresolvedObject(object_type, name, "zone-not-found")

    placed = _wind(_place(polygon, zone, rules), rules)

    if is_shading:
        # The schema gives a shading surface no surface-type field, so the canonical object type
        # goes in that position (FR-012c). It is neither an empty string, which says nothing, nor
        # an invented word like "Shading", which is in no model a reader can open.
        surface_type = object_type
    else:
        surface_type = _canonical(schema, object_type, "surface_type", surface.data.get("surface_type"))

    return ResolvedSurface(
        object_type=object_type,
        name=name,
        polygon=placed,
        zone="" if is_shading else zone_name,
        surface_type=surface_type,
        boundary=_canonical(
            schema, object_type, "outside_boundary_condition", surface.data.get("outside_boundary_condition")
        ),
        construction=str(surface.data.get("construction_name") or ""),
        parent_surface=parent_surface,
        is_shading=is_shading,
    )


def _bounds(surfaces: tuple[ResolvedSurface, ...]) -> SceneBounds | None:
    """The box enclosing every resolved vertex.

    Absent when nothing resolved, rather than a degenerate box at the origin that a consumer would
    dutifully frame (FR-020).
    """
    vertices = [vertex for surface in surfaces for vertex in surface.polygon.vertices]
    if not vertices:
        return None
    return SceneBounds(
        min=Vector3D(min(v.x for v in vertices), min(v.y for v in vertices), min(v.z for v in vertices)),
        max=Vector3D(max(v.x for v in vertices), max(v.y for v in vertices), max(v.z for v in vertices)),
    )


def _unattempted(doc: IDFDocument) -> tuple[UnattemptedType, ...]:
    """Geometry types the model states that this slice does not read, in first-occurrence order.

    This is what makes a model of simplified surfaces distinguishable from a model with no geometry
    at all (FR-019). Without it, both look like an empty scene and a reader is told nothing.
    """
    found: list[tuple[int, str, int]] = []
    for object_type in _UNREAD:
        objects = _objects(doc, object_type)
        if not objects:
            continue
        offsets = [span.start for span in (doc.region_of(obj) for obj in objects) if span is not None]
        found.append((min(offsets) if offsets else 1 << 62, object_type, len(objects)))
    found.sort(key=lambda row: (row[0], row[1]))
    return tuple(UnattemptedType(object_type, count) for _, object_type, count in found)


def get_scene(doc: IDFDocument) -> Scene:
    """Resolve a model's geometry into one frame, leaving the model untouched.

    One argument, one return, no options. There is no ``include_shading``, no ``zones=`` filter and
    no ``color_by``: a filter is a list operation the caller already has, and a colour is a viewing
    decision this function has no business making.

    Args:
        doc: the document to read. It is not modified, and a preserving write before and after
            yields identical bytes.

    Returns:
        A :class:`Scene` in which every geometry object in the model appears exactly once, as a
        resolved surface, an unresolved object with a reason, or a count under an unattempted type.

    Examples:
        >>> from idfkit import new_document, get_scene
        >>> model = new_document()
        >>> scene = get_scene(model)
        >>> scene.surfaces, scene.bounds
        ((), None)

        An empty model and a model of surfaces this slice cannot read are different answers:

        >>> scene.unattempted
        ()
    """
    rules = _read_rules(doc)
    schema = doc.schema

    zones: dict[str, IDFObject] = {obj.name.upper(): obj for obj in _objects(doc, "Zone")}
    surfaces_by_name: dict[str, IDFObject] = {}
    for object_type in (_HEAT_TRANSFER, *_SHADING):
        for obj in _objects(doc, object_type):
            surfaces_by_name[obj.name.upper()] = obj

    resolved: list[ResolvedSurface] = []
    unresolved: list[UnresolvedObject] = []
    for surface in _in_document_order(doc, _READ):
        outcome = _resolve_one(surface, zones, rules, schema, surfaces_by_name)
        if isinstance(outcome, ResolvedSurface):
            resolved.append(outcome)
        else:
            unresolved.append(outcome)

    surfaces = tuple(resolved)
    return Scene(
        surfaces=surfaces,
        bounds=_bounds(surfaces),
        applied=rules,
        unresolved=tuple(unresolved),
        unattempted=_unattempted(doc),
    )
