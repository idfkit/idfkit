from __future__ import annotations

from idfkit import IDFDocument

model: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit import load_idf

# Load an existing IDF file
model = load_idf("building.idf")
print(f"Loaded {len(model)} objects")
# --8<-- [end:example]
