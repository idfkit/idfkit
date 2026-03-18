from __future__ import annotations

from idfkit import IDFDocument

doc: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit import write_idf, write_epjson

write_idf(doc, "out.idf")
write_epjson(doc, "out.epJSON")  # or convert to epJSON
# --8<-- [end:example]
