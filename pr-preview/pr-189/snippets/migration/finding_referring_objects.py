from __future__ import annotations

from idfkit import IDFDocument, IDFObject

idf: IDFDocument = ...  # type: ignore[assignment]
zone: IDFObject = ...  # type: ignore[assignment]
# --8<-- [start:example]
zone = idf.idfobjects["ZONE"][0]
referrers = zone.getreferingobjs()
# --8<-- [end:example]
