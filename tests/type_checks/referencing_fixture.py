"""Type-check fixture for typed reference-graph queries (never called; checked by ``make check``).

``IDFCollection.referencing`` is typed as the collection's objects, so a query read through
``doc["BuildingSurface:Detailed"]`` comes back as a list typed for the document's release: the latest class
through ``IDFDocument``, the release's own class through ``IDFDocumentV9_4``, and the ``Any``
class (or a union with it) through ``AnyIDFDocument``. ``get_referencing`` keeps returning plain
``IDFObject``.

Each seeded error below carries a ``pyright: ignore`` naming the rule it must trigger, and this file
turns on ``reportUnnecessaryTypeIgnoreComment``: if a seeded error stops being reported, the ignore
becomes unnecessary and the check fails, so the fixture proves the errors are caught.
"""

# pyright: strict, reportUnnecessaryTypeIgnoreComment=true

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from typing_extensions import assert_type

from idfkit import IDFDocument
from idfkit.objects import IDFObject
from idfkit.versioned import AnyIDFDocument, IDFDocumentV9_4

if TYPE_CHECKING:
    from idfkit.document import AnyBuildingSurfaceDetailed, BuildingSurfaceDetailed, FenestrationSurfaceDetailed
    from idfkit.versioned import BuildingSurfaceDetailed_v8_9_to_v9_5


def latest(doc: IDFDocument[Any]) -> None:
    zone = doc["Zone"]["Office"]
    # By object or by name, and through the attribute accessor as well as the type name.
    assert_type(doc["BuildingSurface:Detailed"].referencing(zone), list[BuildingSurfaceDetailed])
    assert_type(doc["BuildingSurface:Detailed"].referencing("Office"), list[BuildingSurfaceDetailed])
    assert_type(doc.building_surface_detaileds.referencing(zone), list[BuildingSurfaceDetailed])
    for surface in doc["BuildingSurface:Detailed"].referencing(zone):
        zone_name: str | None = surface.zone_name
        print(zone_name)
        for window in doc["FenestrationSurface:Detailed"].referencing(surface):
            assert_type(window, FenestrationSurfaceDetailed)
            host: str | None = window.building_surface_name
            print(host)
    # The untyped query is unchanged.
    assert_type(doc.get_referencing("Office"), set[IDFObject])


def release_specific(doc: IDFDocumentV9_4) -> None:
    assert_type(doc["BuildingSurface:Detailed"].referencing("Office"), list[BuildingSurfaceDetailed_v8_9_to_v9_5])


def any_release(doc: AnyIDFDocument) -> None:
    for surface in doc["BuildingSurface:Detailed"].referencing("Office"):
        assert_type(surface, AnyBuildingSurfaceDetailed)
        zone_name: str | None = surface.zone_name
        print(zone_name)


def seeded_errors(doc: IDFDocument[Any]) -> None:
    for surface in doc["BuildingSurface:Detailed"].referencing("Office"):
        print(surface.zone_nam)  # pyright: ignore[reportArgumentType]  (typo in a field name)
    doc["Zone"].referencing(42)  # pyright: ignore[reportArgumentType]  (not a name or an object)
