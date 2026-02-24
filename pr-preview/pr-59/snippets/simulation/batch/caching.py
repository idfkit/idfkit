from __future__ import annotations

from idfkit.simulation import SimulationCache, SimulationJob, simulate_batch

cache: SimulationCache = ...  # type: ignore[assignment]
jobs: list[SimulationJob] = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import SimulationCache

cache = SimulationCache()

# All jobs share the same cache
batch = simulate_batch(jobs, cache=cache)

# Re-running is instant for unchanged models
batch2 = simulate_batch(jobs, cache=cache)  # Cache hits
# --8<-- [end:example]
