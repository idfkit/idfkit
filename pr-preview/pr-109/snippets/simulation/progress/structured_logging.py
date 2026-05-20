from __future__ import annotations

from idfkit import IDFDocument

model: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
import logging
from idfkit.simulation import simulate, SimulationProgress

logger = logging.getLogger("simulation")


def on_progress(event: SimulationProgress) -> None:
    logger.info(
        "simulation_progress",
        extra={
            "phase": event.phase,
            "percent": event.percent,
            "environment": event.environment,
            "message": event.message,
        },
    )


result = simulate(model, "weather.epw", on_progress=on_progress)
# --8<-- [end:example]
