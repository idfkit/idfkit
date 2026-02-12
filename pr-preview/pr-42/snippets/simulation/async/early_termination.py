from __future__ import annotations

from idfkit.simulation import SimulationJob, async_simulate_batch_stream

jobs: list[SimulationJob] = ...  # type: ignore[assignment]
# --8<-- [start:example]
async for event in async_simulate_batch_stream(jobs, max_concurrent=4):
    if not event.result.success:
        print(f"Job {event.label} failed — aborting remaining")
        break  # Remaining tasks are cancelled automatically
# --8<-- [end:example]
