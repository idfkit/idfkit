from __future__ import annotations

from idfkit.simulation import BatchResult, SimulationJob, SimulationResult, simulate_batch

batch: BatchResult = ...  # type: ignore[assignment]
jobs: list[SimulationJob] = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
batch = simulate_batch(jobs)

for i, result in enumerate(batch):
    if not result.success:
        print(f"Job {i} failed:")
        print(f"  Exit code: {result.exit_code}")
        print(f"  Stderr: {result.stderr}")
        for err in result.errors.fatal:
            print(f"  Error: {err.message}")
# --8<-- [end:example]
