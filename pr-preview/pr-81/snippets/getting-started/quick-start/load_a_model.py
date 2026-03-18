from __future__ import annotations

from idfkit import IDFDocument

model: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit import load_idf

# Load an existing IDF file
model = load_idf("building.idf")
print(f"Loaded {len(model)} objects")

# For migration-only tolerant loading of legacy/noisy files:
model = load_idf("legacy_building.idf", strict=False)
print(f"Tolerant load parsed {len(model)} objects")
# --8<-- [end:example]
