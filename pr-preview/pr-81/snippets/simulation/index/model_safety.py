from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import simulate

model: IDFDocument = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
result = simulate(model, weather)
assert "Output:SQLite" not in model  # Original unchanged
# --8<-- [end:example]
