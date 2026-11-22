"""Object type names and surface classification shared by the geometry and validation modules."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from .objects import IDFObject

# Surface types that carry vertex geometry, as literals: ``doc[stype]`` in a loop over this tuple is
# typed and checked against every release. ``geometry.VERTEX_SURFACE_TYPES`` is the public list form.
VERTEX_SURFACE_TYPES: Final = (
    "BuildingSurface:Detailed",
    "FenestrationSurface:Detailed",
    "Shading:Site:Detailed",
    "Shading:Building:Detailed",
    "Shading:Zone:Detailed",
)


def is_fenestration_door(obj: IDFObject) -> bool:
    """Whether *obj* is a ``FenestrationSurface:Detailed`` of surface type ``Door`` (opaque).

    Every other fenestration surface, one with no surface type included, counts as glazed: this is
    the rule both ``E013`` and [set_default_constructions][idfkit.geometry_builders.set_default_constructions] apply.
    """
    if obj.obj_type != "FenestrationSurface:Detailed":
        return False
    surface_type = obj.data.get("surface_type")
    return isinstance(surface_type, str) and surface_type.casefold() == "door"
