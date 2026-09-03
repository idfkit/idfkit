from __future__ import annotations

from idfkit import IDFDocument

doc: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit import save_idf, save_epjson

save_idf(doc, "out.idf")
save_epjson(doc, "out.epJSON")  # or convert to epJSON
# --8<-- [end:example]
