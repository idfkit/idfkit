from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import CacheKey, SimulationCache

cache: SimulationCache = ...  # type: ignore[assignment]
key: CacheKey = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
key = cache.compute_key(
    model,
    "weather.epw",
    design_day=True,
    annual=False,
)
print(f"Cache key: {key.hex_digest[:16]}...")
# --8<-- [end:example]
