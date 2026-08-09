from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationJob

jobs: list[SimulationJob] = ...  # type: ignore[assignment]
variant1: IDFDocument = ...  # type: ignore[assignment]
variant2: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import simulate_batch, SimulationJob

jobs = [
    SimulationJob(model=variant1, weather="weather.epw", label="case-1"),
    SimulationJob(model=variant2, weather="weather.epw", label="case-2"),
]

batch = simulate_batch(jobs, max_workers=4)
# --8<-- [end:example]
