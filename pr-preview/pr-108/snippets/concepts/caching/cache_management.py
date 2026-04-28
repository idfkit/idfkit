from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import CacheKey, SimulationCache

cache: SimulationCache = ...  # type: ignore[assignment]
key: CacheKey = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Check if a result would hit cache
key = cache.compute_key(model, weather, design_day=True)
if cache.contains(key):
    print("Would be a cache hit")

# Clear all cached results
cache.clear()
# --8<-- [end:example]
