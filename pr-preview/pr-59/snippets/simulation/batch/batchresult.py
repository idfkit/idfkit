from __future__ import annotations

from idfkit.simulation import BatchResult, SimulationJob, simulate_batch

batch: BatchResult = ...  # type: ignore[assignment]
jobs: list[SimulationJob] = ...  # type: ignore[assignment]
# --8<-- [start:example]
batch = simulate_batch(jobs)

# Access results
batch.results  # All results as tuple
batch[0]  # First result (by index)
len(batch)  # Number of jobs

# Filter by success
batch.succeeded  # Only successful results
batch.failed  # Only failed results
batch.all_succeeded  # True if all succeeded

# Timing
print(f"Total time: {batch.total_runtime_seconds:.1f}s")
# --8<-- [end:example]
