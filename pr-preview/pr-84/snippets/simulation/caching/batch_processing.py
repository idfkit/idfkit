from __future__ import annotations

from idfkit.simulation import SimulationCache, SimulationJob

cache: SimulationCache = ...  # type: ignore[assignment]
jobs: list[SimulationJob] = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import simulate_batch, SimulationCache

cache = SimulationCache()

# All jobs share the same cache
batch1 = simulate_batch(jobs, cache=cache)

# Re-running unchanged jobs hits cache
batch2 = simulate_batch(jobs, cache=cache)  # Instant for unchanged
# --8<-- [end:example]
