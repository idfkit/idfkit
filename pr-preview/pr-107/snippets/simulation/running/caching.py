from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationCache, simulate

cache: SimulationCache = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import SimulationCache

cache = SimulationCache()

# First run: executes simulation
result1 = simulate(model, weather, cache=cache)

# Second run: instant cache hit
result2 = simulate(model, weather, cache=cache)
# --8<-- [end:example]
