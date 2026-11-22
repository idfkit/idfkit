"""Document types for each supported EnergyPlus version.

Each ``IDFDocumentV<major>_<minor>`` types a document as that release declares its objects,
for type checkers; ``IDFDocument`` is the latest release's. See ``versioned.pyi``.

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from ._document_types import as_version, document_type, release_type_var, release_union
from ._release_aliases import DocumentTypeTarget, ReleaseBound
from .document import AnyIDFDocument, IDFDocument

__all__ = [
    "AnyIDFDocument",
    "DocumentTypeTarget",
    "IDFDocumentBefore9_0",
    "IDFDocumentBefore9_1",
    "IDFDocumentBefore9_2",
    "IDFDocumentBefore9_3",
    "IDFDocumentBefore9_4",
    "IDFDocumentBefore9_5",
    "IDFDocumentBefore9_6",
    "IDFDocumentBefore22_1",
    "IDFDocumentBefore22_2",
    "IDFDocumentBefore23_1",
    "IDFDocumentBefore23_2",
    "IDFDocumentBefore24_1",
    "IDFDocumentBefore24_2",
    "IDFDocumentBefore25_1",
    "IDFDocumentBefore25_2",
    "IDFDocumentBefore26_1",
    "IDFDocumentBefore26_2",
    "IDFDocumentSince8_9",
    "IDFDocumentSince9_0",
    "IDFDocumentSince9_1",
    "IDFDocumentSince9_2",
    "IDFDocumentSince9_3",
    "IDFDocumentSince9_4",
    "IDFDocumentSince9_5",
    "IDFDocumentSince9_6",
    "IDFDocumentSince22_1",
    "IDFDocumentSince22_2",
    "IDFDocumentSince23_1",
    "IDFDocumentSince23_2",
    "IDFDocumentSince24_1",
    "IDFDocumentSince24_2",
    "IDFDocumentSince25_1",
    "IDFDocumentSince25_2",
    "IDFDocumentSince26_1",
    "IDFDocumentSince26_2",
    "IDFDocumentV8_9",
    "IDFDocumentV9_0",
    "IDFDocumentV9_1",
    "IDFDocumentV9_2",
    "IDFDocumentV9_3",
    "IDFDocumentV9_4",
    "IDFDocumentV9_5",
    "IDFDocumentV9_6",
    "IDFDocumentV22_1",
    "IDFDocumentV22_2",
    "IDFDocumentV23_1",
    "IDFDocumentV23_2",
    "IDFDocumentV24_1",
    "IDFDocumentV24_2",
    "IDFDocumentV25_1",
    "IDFDocumentV25_2",
    "IDFDocumentV26_1",
    "IDFDocumentV26_2",
    "ReleaseBound",
    "ReleaseDocumentT",
    "as_version",
]

IDFDocumentV8_9 = document_type("IDFDocumentV8_9", (8, 9, 0))
IDFDocumentV9_0 = document_type("IDFDocumentV9_0", (9, 0, 1))
IDFDocumentV9_1 = document_type("IDFDocumentV9_1", (9, 1, 0))
IDFDocumentV9_2 = document_type("IDFDocumentV9_2", (9, 2, 0))
IDFDocumentV9_3 = document_type("IDFDocumentV9_3", (9, 3, 0))
IDFDocumentV9_4 = document_type("IDFDocumentV9_4", (9, 4, 0))
IDFDocumentV9_5 = document_type("IDFDocumentV9_5", (9, 5, 0))
IDFDocumentV9_6 = document_type("IDFDocumentV9_6", (9, 6, 0))
IDFDocumentV22_1 = document_type("IDFDocumentV22_1", (22, 1, 0))
IDFDocumentV22_2 = document_type("IDFDocumentV22_2", (22, 2, 0))
IDFDocumentV23_1 = document_type("IDFDocumentV23_1", (23, 1, 0))
IDFDocumentV23_2 = document_type("IDFDocumentV23_2", (23, 2, 0))
IDFDocumentV24_1 = document_type("IDFDocumentV24_1", (24, 1, 0))
IDFDocumentV24_2 = document_type("IDFDocumentV24_2", (24, 2, 0))
IDFDocumentV25_1 = document_type("IDFDocumentV25_1", (25, 1, 0))
IDFDocumentV25_2 = document_type("IDFDocumentV25_2", (25, 2, 0))
IDFDocumentV26_1 = document_type("IDFDocumentV26_1", (26, 1, 0))
IDFDocumentV26_2 = IDFDocument

ReleaseDocumentT = release_type_var(
    "ReleaseDocumentT",
    IDFDocumentV8_9,
    IDFDocumentV9_0,
    IDFDocumentV9_1,
    IDFDocumentV9_2,
    IDFDocumentV9_3,
    IDFDocumentV9_4,
    IDFDocumentV9_5,
    IDFDocumentV9_6,
    IDFDocumentV22_1,
    IDFDocumentV22_2,
    IDFDocumentV23_1,
    IDFDocumentV23_2,
    IDFDocumentV24_1,
    IDFDocumentV24_2,
    IDFDocumentV25_1,
    IDFDocumentV25_2,
    IDFDocumentV26_1,
    IDFDocumentV26_2,
)
"""A type variable that is exactly one release's document type.

Constrained to ``IDFDocumentV8_9`` ... ``IDFDocument``, so ``type[ReleaseDocumentT]`` accepts one
release's type and refuses ``AnyIDFDocument``, which names no single release. A union of release
types names none either: mypy refuses it, but pyright tries each member against the constraints
and accepts it, so check at run time too. [idfkit.migration.migrate][idfkit.migration.migrate] takes its target this
way, and raises ``TypeError`` for a union.
"""

# Ranges of releases, typed in versioned.pyi. At run time each is the union of its releases.
IDFDocumentSince8_9 = release_union(
    IDFDocumentV8_9,
    IDFDocumentV9_0,
    IDFDocumentV9_1,
    IDFDocumentV9_2,
    IDFDocumentV9_3,
    IDFDocumentV9_4,
    IDFDocumentV9_5,
    IDFDocumentV9_6,
    IDFDocumentV22_1,
    IDFDocumentV22_2,
    IDFDocumentV23_1,
    IDFDocumentV23_2,
    IDFDocumentV24_1,
    IDFDocumentV24_2,
    IDFDocumentV25_1,
    IDFDocumentV25_2,
    IDFDocumentV26_1,
    IDFDocumentV26_2,
)
IDFDocumentSince9_0 = release_union(
    IDFDocumentV9_0,
    IDFDocumentV9_1,
    IDFDocumentV9_2,
    IDFDocumentV9_3,
    IDFDocumentV9_4,
    IDFDocumentV9_5,
    IDFDocumentV9_6,
    IDFDocumentV22_1,
    IDFDocumentV22_2,
    IDFDocumentV23_1,
    IDFDocumentV23_2,
    IDFDocumentV24_1,
    IDFDocumentV24_2,
    IDFDocumentV25_1,
    IDFDocumentV25_2,
    IDFDocumentV26_1,
    IDFDocumentV26_2,
)
IDFDocumentSince9_1 = release_union(
    IDFDocumentV9_1,
    IDFDocumentV9_2,
    IDFDocumentV9_3,
    IDFDocumentV9_4,
    IDFDocumentV9_5,
    IDFDocumentV9_6,
    IDFDocumentV22_1,
    IDFDocumentV22_2,
    IDFDocumentV23_1,
    IDFDocumentV23_2,
    IDFDocumentV24_1,
    IDFDocumentV24_2,
    IDFDocumentV25_1,
    IDFDocumentV25_2,
    IDFDocumentV26_1,
    IDFDocumentV26_2,
)
IDFDocumentSince9_2 = release_union(
    IDFDocumentV9_2,
    IDFDocumentV9_3,
    IDFDocumentV9_4,
    IDFDocumentV9_5,
    IDFDocumentV9_6,
    IDFDocumentV22_1,
    IDFDocumentV22_2,
    IDFDocumentV23_1,
    IDFDocumentV23_2,
    IDFDocumentV24_1,
    IDFDocumentV24_2,
    IDFDocumentV25_1,
    IDFDocumentV25_2,
    IDFDocumentV26_1,
    IDFDocumentV26_2,
)
IDFDocumentSince9_3 = release_union(
    IDFDocumentV9_3,
    IDFDocumentV9_4,
    IDFDocumentV9_5,
    IDFDocumentV9_6,
    IDFDocumentV22_1,
    IDFDocumentV22_2,
    IDFDocumentV23_1,
    IDFDocumentV23_2,
    IDFDocumentV24_1,
    IDFDocumentV24_2,
    IDFDocumentV25_1,
    IDFDocumentV25_2,
    IDFDocumentV26_1,
    IDFDocumentV26_2,
)
IDFDocumentSince9_4 = release_union(
    IDFDocumentV9_4,
    IDFDocumentV9_5,
    IDFDocumentV9_6,
    IDFDocumentV22_1,
    IDFDocumentV22_2,
    IDFDocumentV23_1,
    IDFDocumentV23_2,
    IDFDocumentV24_1,
    IDFDocumentV24_2,
    IDFDocumentV25_1,
    IDFDocumentV25_2,
    IDFDocumentV26_1,
    IDFDocumentV26_2,
)
IDFDocumentSince9_5 = release_union(
    IDFDocumentV9_5,
    IDFDocumentV9_6,
    IDFDocumentV22_1,
    IDFDocumentV22_2,
    IDFDocumentV23_1,
    IDFDocumentV23_2,
    IDFDocumentV24_1,
    IDFDocumentV24_2,
    IDFDocumentV25_1,
    IDFDocumentV25_2,
    IDFDocumentV26_1,
    IDFDocumentV26_2,
)
IDFDocumentSince9_6 = release_union(
    IDFDocumentV9_6,
    IDFDocumentV22_1,
    IDFDocumentV22_2,
    IDFDocumentV23_1,
    IDFDocumentV23_2,
    IDFDocumentV24_1,
    IDFDocumentV24_2,
    IDFDocumentV25_1,
    IDFDocumentV25_2,
    IDFDocumentV26_1,
    IDFDocumentV26_2,
)
IDFDocumentSince22_1 = release_union(
    IDFDocumentV22_1,
    IDFDocumentV22_2,
    IDFDocumentV23_1,
    IDFDocumentV23_2,
    IDFDocumentV24_1,
    IDFDocumentV24_2,
    IDFDocumentV25_1,
    IDFDocumentV25_2,
    IDFDocumentV26_1,
    IDFDocumentV26_2,
)
IDFDocumentSince22_2 = release_union(
    IDFDocumentV22_2,
    IDFDocumentV23_1,
    IDFDocumentV23_2,
    IDFDocumentV24_1,
    IDFDocumentV24_2,
    IDFDocumentV25_1,
    IDFDocumentV25_2,
    IDFDocumentV26_1,
    IDFDocumentV26_2,
)
IDFDocumentSince23_1 = release_union(
    IDFDocumentV23_1,
    IDFDocumentV23_2,
    IDFDocumentV24_1,
    IDFDocumentV24_2,
    IDFDocumentV25_1,
    IDFDocumentV25_2,
    IDFDocumentV26_1,
    IDFDocumentV26_2,
)
IDFDocumentSince23_2 = release_union(
    IDFDocumentV23_2,
    IDFDocumentV24_1,
    IDFDocumentV24_2,
    IDFDocumentV25_1,
    IDFDocumentV25_2,
    IDFDocumentV26_1,
    IDFDocumentV26_2,
)
IDFDocumentSince24_1 = release_union(
    IDFDocumentV24_1,
    IDFDocumentV24_2,
    IDFDocumentV25_1,
    IDFDocumentV25_2,
    IDFDocumentV26_1,
    IDFDocumentV26_2,
)
IDFDocumentSince24_2 = release_union(
    IDFDocumentV24_2,
    IDFDocumentV25_1,
    IDFDocumentV25_2,
    IDFDocumentV26_1,
    IDFDocumentV26_2,
)
IDFDocumentSince25_1 = release_union(
    IDFDocumentV25_1,
    IDFDocumentV25_2,
    IDFDocumentV26_1,
    IDFDocumentV26_2,
)
IDFDocumentSince25_2 = release_union(
    IDFDocumentV25_2,
    IDFDocumentV26_1,
    IDFDocumentV26_2,
)
IDFDocumentSince26_1 = release_union(
    IDFDocumentV26_1,
    IDFDocumentV26_2,
)
IDFDocumentSince26_2 = release_union(
    IDFDocumentV26_2,
)
IDFDocumentBefore9_0 = release_union(
    IDFDocumentV8_9,
)
IDFDocumentBefore9_1 = release_union(
    IDFDocumentV8_9,
    IDFDocumentV9_0,
)
IDFDocumentBefore9_2 = release_union(
    IDFDocumentV8_9,
    IDFDocumentV9_0,
    IDFDocumentV9_1,
)
IDFDocumentBefore9_3 = release_union(
    IDFDocumentV8_9,
    IDFDocumentV9_0,
    IDFDocumentV9_1,
    IDFDocumentV9_2,
)
IDFDocumentBefore9_4 = release_union(
    IDFDocumentV8_9,
    IDFDocumentV9_0,
    IDFDocumentV9_1,
    IDFDocumentV9_2,
    IDFDocumentV9_3,
)
IDFDocumentBefore9_5 = release_union(
    IDFDocumentV8_9,
    IDFDocumentV9_0,
    IDFDocumentV9_1,
    IDFDocumentV9_2,
    IDFDocumentV9_3,
    IDFDocumentV9_4,
)
IDFDocumentBefore9_6 = release_union(
    IDFDocumentV8_9,
    IDFDocumentV9_0,
    IDFDocumentV9_1,
    IDFDocumentV9_2,
    IDFDocumentV9_3,
    IDFDocumentV9_4,
    IDFDocumentV9_5,
)
IDFDocumentBefore22_1 = release_union(
    IDFDocumentV8_9,
    IDFDocumentV9_0,
    IDFDocumentV9_1,
    IDFDocumentV9_2,
    IDFDocumentV9_3,
    IDFDocumentV9_4,
    IDFDocumentV9_5,
    IDFDocumentV9_6,
)
IDFDocumentBefore22_2 = release_union(
    IDFDocumentV8_9,
    IDFDocumentV9_0,
    IDFDocumentV9_1,
    IDFDocumentV9_2,
    IDFDocumentV9_3,
    IDFDocumentV9_4,
    IDFDocumentV9_5,
    IDFDocumentV9_6,
    IDFDocumentV22_1,
)
IDFDocumentBefore23_1 = release_union(
    IDFDocumentV8_9,
    IDFDocumentV9_0,
    IDFDocumentV9_1,
    IDFDocumentV9_2,
    IDFDocumentV9_3,
    IDFDocumentV9_4,
    IDFDocumentV9_5,
    IDFDocumentV9_6,
    IDFDocumentV22_1,
    IDFDocumentV22_2,
)
IDFDocumentBefore23_2 = release_union(
    IDFDocumentV8_9,
    IDFDocumentV9_0,
    IDFDocumentV9_1,
    IDFDocumentV9_2,
    IDFDocumentV9_3,
    IDFDocumentV9_4,
    IDFDocumentV9_5,
    IDFDocumentV9_6,
    IDFDocumentV22_1,
    IDFDocumentV22_2,
    IDFDocumentV23_1,
)
IDFDocumentBefore24_1 = release_union(
    IDFDocumentV8_9,
    IDFDocumentV9_0,
    IDFDocumentV9_1,
    IDFDocumentV9_2,
    IDFDocumentV9_3,
    IDFDocumentV9_4,
    IDFDocumentV9_5,
    IDFDocumentV9_6,
    IDFDocumentV22_1,
    IDFDocumentV22_2,
    IDFDocumentV23_1,
    IDFDocumentV23_2,
)
IDFDocumentBefore24_2 = release_union(
    IDFDocumentV8_9,
    IDFDocumentV9_0,
    IDFDocumentV9_1,
    IDFDocumentV9_2,
    IDFDocumentV9_3,
    IDFDocumentV9_4,
    IDFDocumentV9_5,
    IDFDocumentV9_6,
    IDFDocumentV22_1,
    IDFDocumentV22_2,
    IDFDocumentV23_1,
    IDFDocumentV23_2,
    IDFDocumentV24_1,
)
IDFDocumentBefore25_1 = release_union(
    IDFDocumentV8_9,
    IDFDocumentV9_0,
    IDFDocumentV9_1,
    IDFDocumentV9_2,
    IDFDocumentV9_3,
    IDFDocumentV9_4,
    IDFDocumentV9_5,
    IDFDocumentV9_6,
    IDFDocumentV22_1,
    IDFDocumentV22_2,
    IDFDocumentV23_1,
    IDFDocumentV23_2,
    IDFDocumentV24_1,
    IDFDocumentV24_2,
)
IDFDocumentBefore25_2 = release_union(
    IDFDocumentV8_9,
    IDFDocumentV9_0,
    IDFDocumentV9_1,
    IDFDocumentV9_2,
    IDFDocumentV9_3,
    IDFDocumentV9_4,
    IDFDocumentV9_5,
    IDFDocumentV9_6,
    IDFDocumentV22_1,
    IDFDocumentV22_2,
    IDFDocumentV23_1,
    IDFDocumentV23_2,
    IDFDocumentV24_1,
    IDFDocumentV24_2,
    IDFDocumentV25_1,
)
IDFDocumentBefore26_1 = release_union(
    IDFDocumentV8_9,
    IDFDocumentV9_0,
    IDFDocumentV9_1,
    IDFDocumentV9_2,
    IDFDocumentV9_3,
    IDFDocumentV9_4,
    IDFDocumentV9_5,
    IDFDocumentV9_6,
    IDFDocumentV22_1,
    IDFDocumentV22_2,
    IDFDocumentV23_1,
    IDFDocumentV23_2,
    IDFDocumentV24_1,
    IDFDocumentV24_2,
    IDFDocumentV25_1,
    IDFDocumentV25_2,
)
IDFDocumentBefore26_2 = release_union(
    IDFDocumentV8_9,
    IDFDocumentV9_0,
    IDFDocumentV9_1,
    IDFDocumentV9_2,
    IDFDocumentV9_3,
    IDFDocumentV9_4,
    IDFDocumentV9_5,
    IDFDocumentV9_6,
    IDFDocumentV22_1,
    IDFDocumentV22_2,
    IDFDocumentV23_1,
    IDFDocumentV23_2,
    IDFDocumentV24_1,
    IDFDocumentV24_2,
    IDFDocumentV25_1,
    IDFDocumentV25_2,
    IDFDocumentV26_1,
)
