from __future__ import annotations

from idfkit.simulation import SimulationJob, simulate_batch

jobs: list[SimulationJob] = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Use all CPUs
batch = simulate_batch(jobs, max_workers=None)  # Default

# Limit to 4 concurrent simulations
batch = simulate_batch(jobs, max_workers=4)

# Sequential (useful for debugging)
batch = simulate_batch(jobs, max_workers=1)
# --8<-- [end:example]
