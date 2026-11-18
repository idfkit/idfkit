"""Object type names shared by the geometry modules."""

from __future__ import annotations

from typing import Final

# Surface types that carry vertex geometry, as literals: ``doc[stype]`` in a loop over this tuple is
# typed and checked against every release. ``geometry.VERTEX_SURFACE_TYPES`` is the public list form.
VERTEX_SURFACE_TYPES: Final = (
    "BuildingSurface:Detailed",
    "FenestrationSurface:Detailed",
    "Shading:Site:Detailed",
    "Shading:Building:Detailed",
    "Shading:Zone:Detailed",
)
