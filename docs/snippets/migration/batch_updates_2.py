from __future__ import annotations

from idfkit._compat import EppyDocumentMixin

# `doc` is an IDFDocument. It is annotated here as the eppy-compatibility mixin
# that actually defines `update`, because the generated IDFDocument stub lists
# the `_ObjectTypeMap` TypedDict first in its bases and TypedDict.update wins
# the MRO lookup. Typing the placeholder this way keeps the real `update`
# signature under drift checking instead of silencing the call.
doc: EppyDocumentMixin = ...  # type: ignore[assignment]
# --8<-- [start:example]
doc.update({
    "Zone.Office.x_origin": 10.0,
    "Zone.Office.y_origin": 5.0,
})
# --8<-- [end:example]
