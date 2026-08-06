from __future__ import annotations

from idfkit import load_idf

# --8<-- [start:example]
doc = load_idf("in.idf", version=(24, 1, 0))
# --8<-- [end:example]
