from __future__ import annotations

from idfkit import IDFDocument

idf: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
idf.saveas("out.idf")
idf.savecopy("backup.idf")
idf.save()
# --8<-- [end:example]
