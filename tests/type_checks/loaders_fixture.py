"""Type-check fixture for the public loaders (never called; checked by ``make check``).

``load_idf``, ``load_idf_with_diagnostics`` and ``load_epjson`` accept a ``pathlib.Path`` as well as a
``str``, the same as ``save_idf`` and ``save_epjson``.

A model's release is read from its file, so a loaded document is typed as ``AnyIDFDocument``: forgetting
to state the release can never check a model against the wrong release's object types and fields.
``as_type=``, ``since=`` and ``before=`` state it, and type the document for it, as ``as_version`` does.

Each seeded error below carries a ``pyright: ignore`` naming the rule it must trigger, and this file
turns on ``reportUnnecessaryTypeIgnoreComment``, so the fixture proves the errors are caught rather than
merely tolerated.
"""

# pyright: strict, reportUnnecessaryTypeIgnoreComment=true

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from typing_extensions import assert_type

from idfkit import IDFDocument, load_epjson, load_idf, load_idf_with_diagnostics
from idfkit.idf_parser import ParseResult
from idfkit.versioned import (
    AnyIDFDocument,
    IDFDocumentBefore9_6,
    IDFDocumentSince9_6,
    IDFDocumentSince26_1,
    IDFDocumentV9_4,
    IDFDocumentV9_6,
    IDFDocumentV25_2,
    IDFDocumentV26_1,
    IDFDocumentV26_2,
)


def correct_calls(folder: Path) -> None:
    load_idf(folder / "model.idf")
    load_idf("model.idf")
    load_idf(Path("model.idf"), strict=False)
    load_idf_with_diagnostics(folder / "model.idf")
    load_epjson(folder / "model.epJSON")
    load_epjson(Path("model.epJSON"), strict=False)


def any_release(path: Path) -> None:
    """Without a target, a loaded document is of any release, as strict as asked."""
    assert_type(load_idf(path), AnyIDFDocument[Literal[True]])
    assert_type(load_idf(path, strict=False), AnyIDFDocument[Literal[False]])
    assert_type(load_epjson(path), AnyIDFDocument[Literal[True]])
    assert_type(load_epjson(path, strict=False), AnyIDFDocument[Literal[False]])
    assert_type(load_idf_with_diagnostics(path), ParseResult[AnyIDFDocument[Literal[True]]])
    assert_type(load_idf_with_diagnostics(path, strict=False).document, AnyIDFDocument[Literal[False]])
    # A version override rewrites the release at run time; a type checker does not read the tuple.
    assert_type(load_idf(path, (9, 4, 0)), AnyIDFDocument[Literal[True]])
    # What every release has type-checks.
    model = load_idf(path)
    for zone in model.zones:
        print(zone.name, zone.ceiling_height)
    for surface in model["BuildingSurface:Detailed"]:
        print(surface.construction_name)


def one_release(path: Path) -> None:
    """``as_type=`` names the release, as ``as_version(doc, ...)`` and ``new_document(...)`` take it."""
    assert_type(load_idf(path, as_type=IDFDocumentV26_1), IDFDocumentV26_1)
    assert_type(load_idf(path, as_type=IDFDocumentV26_2), IDFDocument)
    assert_type(load_epjson(path, as_type=IDFDocumentV9_4), IDFDocumentV9_4)
    assert_type(load_idf_with_diagnostics(path, as_type=IDFDocumentV9_4), ParseResult[IDFDocumentV9_4])
    assert_type(load_idf(path, as_type=IDFDocumentV9_4[Literal[False]], strict=False), IDFDocumentV9_4[Literal[False]])
    assert_type(load_idf(path, (9, 4, 0), as_type=IDFDocumentV9_4), IDFDocumentV9_4)
    assert_type(load_idf(path, as_type=(IDFDocumentV9_6, IDFDocumentV26_1)), IDFDocumentV9_6 | IDFDocumentV26_1)
    legacy = load_idf(path, as_type=IDFDocumentV9_4)
    legacy["People"]["Office"].zone_or_zonelist_name = "Office"  # the 9.4 name
    legacy["WaterHeater:Mixed"]["Heater"].heater_fuel_type = "DistrictHeating"  # a 9.4 choice
    # 26.2 made a surface's construction optional; a model stated to be 26.2 may leave it out.
    load_idf(path, as_type=IDFDocumentV26_2)["BuildingSurface:Detailed"].add(
        "Wall", surface_type="Wall", zone_name="Office", outside_boundary_condition="Outdoors"
    )


def a_range(path: Path, first: str) -> None:
    """``since=`` and ``before=`` name a range of releases, as for ``as_version``."""
    assert_type(load_idf(path, since="26.1"), IDFDocumentSince26_1)
    assert_type(load_idf(path, since=IDFDocumentV9_6), IDFDocumentSince9_6)
    assert_type(load_idf(path, since="9.6.0", strict=False), IDFDocumentSince9_6)
    assert_type(load_idf(path, before="9.6"), IDFDocumentBefore9_6)
    assert_type(load_idf(path, since="25.2", before="26.2"), IDFDocumentV25_2 | IDFDocumentV26_1)
    assert_type(load_epjson(path, since="26.1"), IDFDocumentSince26_1)
    assert_type(load_idf_with_diagnostics(path, since="26.1"), ParseResult[IDFDocumentSince26_1])
    load_idf(path, since="9.6")["Space"].first()  # every release from 9.6 on has Space
    # A bound a type checker cannot read as one release is checked only when the call runs.
    assert_type(load_idf(path, since=first), AnyIDFDocument)
    assert_type(load_idf(path, before=(9, 6, 0)), AnyIDFDocument)


def latest_only(doc: IDFDocument[Any]) -> None: ...


def seeded_errors(path: Path) -> None:
    load_idf(42)  # pyright: ignore[reportArgumentType]
    load_epjson(b"model.epJSON")  # pyright: ignore[reportArgumentType]
    # Forgetting to state the release: a loaded model is not taken for the latest release ...
    latest_only(load_idf(path))  # pyright: ignore[reportArgumentType]
    # ... nor offered what only some releases have.
    load_idf(path)["Space"]  # pyright: ignore[reportCallIssue, reportArgumentType]  (Space is new in 9.6)
    # A 26.1 model requires a surface's construction, which 26.2 made optional: through the loaded
    # model leaving it out is an error, as it would be for the 26.1 file this may be.
    load_idf(path)["BuildingSurface:Detailed"].add(  # pyright: ignore[reportCallIssue]
        "Wall", surface_type="Wall", zone_name="Office", outside_boundary_condition="Outdoors"
    )
    load_idf(path, as_type=IDFDocumentV26_1)["BuildingSurface:Detailed"].add(  # pyright: ignore[reportCallIssue]
        "Wall", surface_type="Wall", zone_name="Office", outside_boundary_condition="Outdoors"
    )
    # Stated, the release's own types apply.
    load_idf(path, as_type=IDFDocumentV9_4)["Space"]  # pyright: ignore[reportCallIssue, reportArgumentType]
    load_idf(path, before="9.6")["Space"]  # pyright: ignore[reportCallIssue, reportArgumentType]
    # A document type and a range together are refused, as by as_version.
    load_idf(path, as_type=IDFDocumentV26_1, since="26.1")  # pyright: ignore[reportCallIssue]
