from __future__ import annotations

from idfkit import IDFDocument, load_idf
from idfkit.simulation import simulate

model: IDFDocument = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
model = load_idf("building.idf")
original_count = len(model)

result = simulate(model, weather)

# Model unchanged
assert len(model) == original_count
assert "Output:SQLite" not in model
# --8<-- [end:example]
