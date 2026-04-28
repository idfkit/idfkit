from __future__ import annotations

from idfkit import IDFDocument
from typing import Any

model: IDFDocument = ...  # type: ignore[assignment]
redis_client: Any = ...  # type: ignore[assignment]
# --8<-- [start:example]
from dataclasses import asdict
import json
from idfkit.simulation import simulate, SimulationProgress


def make_queue_callback(queue_client, channel: str):
    """Create a callback that publishes events to a message queue."""

    def on_progress(event: SimulationProgress) -> None:
        queue_client.publish(channel, json.dumps(asdict(event)))

    return on_progress


cb = make_queue_callback(redis_client, "sim:progress:run-001")
result = simulate(model, "weather.epw", on_progress=cb)
# --8<-- [end:example]
