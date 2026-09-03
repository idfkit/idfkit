from __future__ import annotations

from idfkit._compat import EppyDocumentMixin

# `doc` is an IDFDocument at runtime. It is annotated here as the
# eppy-compatibility mixin that actually defines `update`, and that is the
# correct annotation rather than a workaround.
#
# `IDFDocument` inherits the generated `_ObjectTypeMap` TypedDict, which is what
# resolves `doc["Zone"]` to `IDFCollection[Zone]` in O(1) with no overload stack.
# Pyright synthesises `update` for every class in a TypedDict hierarchy, and that
# synthesised method outranks anything else: reordering the bases does not help,
# redeclaring `update` on `IDFDocument` does not help, and declaring it as a
# callable attribute does not help. All three were measured. The only way to make
# `IDFDocument.update` statically visible is to stop inheriting the TypedDict,
# which would cost every typed lookup on the document.
#
# `update` is a quotation of eppy's `json_functions.updateidf`, registered as part
# of the excluded eppy compatibility surface, so reaching it through the mixin
# that defines it says exactly what is going on. This keeps the real signature
# under drift checking instead of silencing the call.
doc: EppyDocumentMixin = ...  # type: ignore[assignment]
# --8<-- [start:example]
doc.update({
    "Zone.Office.x_origin": 10.0,
    "Zone.Office.y_origin": 5.0,
})
# --8<-- [end:example]
