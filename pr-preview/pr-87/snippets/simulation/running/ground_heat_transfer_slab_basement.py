from __future__ import annotations

from idfkit import IDFDocument

model: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import run_slab_preprocessor, run_basement_preprocessor

# Slab-on-grade foundation
expanded = run_slab_preprocessor(model, weather="weather.epw")

# Basement walls and floors
expanded = run_basement_preprocessor(model, weather="weather.epw")
# --8<-- [end:example]
