from __future__ import annotations

from idfkit import IDFDocument

model: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit import load_idf
from idfkit.simulation import simulate

model = load_idf("building.idf")
result = simulate(model, "weather.epw", annual=True, on_progress="tqdm")
# --8<-- [end:example]
