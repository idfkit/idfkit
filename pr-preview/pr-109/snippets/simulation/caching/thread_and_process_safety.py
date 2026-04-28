from __future__ import annotations

from idfkit.simulation import SimulationCache, SimulationJob, simulate_batch

cache: SimulationCache = ...  # type: ignore[assignment]
jobs: list[SimulationJob] = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Safe: concurrent access from multiple workers
batch = simulate_batch(jobs, max_workers=8, cache=cache)
# --8<-- [end:example]
