from __future__ import annotations

from idfkit import IDFDocument

idf: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
idf.outputtype = "nocomment"
idf.saveas("out.idf")
# --8<-- [end:example]
