from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import CacheKey, SimulationCache, SimulationResult, simulate

cache: SimulationCache = ...  # type: ignore[assignment]
cached_result: SimulationResult | None = ...  # type: ignore[assignment]
key: CacheKey = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Compute key
key = cache.compute_key(model, weather)

# Check cache
cached_result = cache.get(key)
if cached_result is not None:
    print("Cache hit!")
else:
    # Run simulation
    result = simulate(model, weather)

    # Store in cache (only successful results)
    cache.put(key, result)
# --8<-- [end:example]
