from __future__ import annotations

from idfkit.simulation import SimulationJob, simulate_batch

jobs: list[SimulationJob] = ...  # type: ignore[assignment]


# --8<-- [start:example]
def on_progress(completed, total, label, success):
    status = "OK" if success else "FAIL"
    print(f"[{completed}/{total}] {label}: {status}")


batch = simulate_batch(jobs, progress=on_progress)
# --8<-- [end:example]
