from __future__ import annotations

# --8<-- [start:example]
from idfkit import load_idf, write_idf

# Build a CST to preserve original formatting
model = load_idf("building.idf", preserve_formatting=True)

# Modify a zone ceiling height
model["Zone"]["Office"].ceiling_height = 3.5

# Unmodified objects keep their original formatting, comments,
# and whitespace; only the changed object is re-serialised.
write_idf(model, "building_updated.idf")
# --8<-- [end:example]
