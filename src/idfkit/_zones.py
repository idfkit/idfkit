"""Zone lookup shared by the helpers that take a zone (geometry, visualization).

A helper that matches surfaces by their ``zone_name`` finds none for a misspelt zone and would
return ``0.0`` or an empty figure. Resolving the zone first turns that into the same
``ObjectNotFoundError`` ("did you mean") that ``doc["Zone"][name]`` raises.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .document import AnyIDFDocument
    from .objects import IDFObject


def resolve_zone_name(doc: AnyIDFDocument, zone: str | IDFObject) -> str:
    """Return the name of the ``Zone`` *zone* names, refusing one the document does not have.

    Args:
        doc: The document holding the zone.
        zone: A zone name (matched case-insensitively) or the ``Zone`` object itself.

    Returns:
        The zone's name as stored in the document.

    Raises:
        ObjectNotFoundError: If *doc* has no ``Zone`` of that name; a ``KeyError``
            whose message suggests the closest zone names, as ``doc["Zone"][name]`` does.
        TypeError: If *zone* is an object of another type than ``Zone``.
    """
    if isinstance(zone, str):
        return doc["Zone"][zone].name
    if zone.obj_type.upper() != "ZONE":
        msg = f"Expected a zone name or a Zone object, got a {zone.obj_type} object ({zone.name!r})"
        raise TypeError(msg)
    return doc["Zone"][zone.name].name
