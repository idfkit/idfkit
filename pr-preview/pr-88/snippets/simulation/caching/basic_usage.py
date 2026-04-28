from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationCache, SimulationResult

cache: SimulationCache = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
result1: SimulationResult = ...  # type: ignore[assignment]
result2: SimulationResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import simulate, SimulationCache

cache = SimulationCache()

# First run: executes EnergyPlus
result1 = simulate(model, "weather.epw", cache=cache)
print(f"Runtime: {result1.runtime_seconds:.1f}s")

# Second run: instant cache hit
result2 = simulate(model, "weather.epw", cache=cache)
print(f"Runtime: {result2.runtime_seconds:.1f}s")  # Near zero
# --8<-- [end:example]
