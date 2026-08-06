from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import simulate

model: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
result = simulate(model, "weather.epw", annual=True, on_progress="tqdm")
# --8<-- [end:example]
