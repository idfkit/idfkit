from __future__ import annotations

from idfkit.simulation import SimulationCache, SimulationJob

cache: SimulationCache = ...  # type: ignore[assignment]
jobs: list[SimulationJob] = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import simulate_batch, SimulationCache

cache = SimulationCache()

# Safe: all workers share the cache
batch = simulate_batch(jobs, max_workers=8, cache=cache)
# --8<-- [end:example]
