from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationJob

jobs: list[SimulationJob] = ...  # type: ignore[assignment]
variant: IDFDocument = ...  # type: ignore[assignment]
variants: list[IDFDocument] = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import SimulationJob

jobs = [
    SimulationJob(
        model=variant,
        weather="weather.epw",
        label=f"case-{i}",
        output_dir=f"case-{i}",
    )
    for i, variant in enumerate(variants)
]
# --8<-- [end:example]
