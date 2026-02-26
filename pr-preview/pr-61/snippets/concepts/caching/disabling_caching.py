from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationCache, simulate

cache: SimulationCache = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
# No caching — always runs EnergyPlus
result = simulate(model, weather)

# With caching
cache = SimulationCache()
result = simulate(model, weather, cache=cache)
# --8<-- [end:example]
