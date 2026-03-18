from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationCache, simulate

model: IDFDocument = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
# No caching
result = simulate(model, weather)

# With caching
result = simulate(model, weather, cache=SimulationCache())
# --8<-- [end:example]
