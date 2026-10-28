"""Document types for each supported EnergyPlus version.

Each ``IDFDocumentV<major>_<minor>`` types a document as that release declares its objects,
for type checkers; ``IDFDocument`` is the latest release's. See ``versioned.pyi``.

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from ._document_types import as_version, document_type
from .document import AnyIDFDocument, IDFDocument

__all__ = [
    "AnyIDFDocument",
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
