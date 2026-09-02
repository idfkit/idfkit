from __future__ import annotations

from idfkit import IDFDocument

model: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit import write_idf, save_idf, save_epjson

# Write to IDF format
save_idf(model, "output.idf")

# Or write to epJSON format
save_epjson(model, "output.epJSON")

# Get the text back instead
idf_string = write_idf(model)
# --8<-- [end:example]
