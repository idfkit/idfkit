from __future__ import annotations

from idfkit.simulation import SimulationProgress
from typing import Any

message_queue: Any = ...  # type: ignore[assignment]
# --8<-- [start:example]
from dataclasses import asdict
import json


def on_progress(event: SimulationProgress) -> None:
    message_queue.publish(json.dumps(asdict(event)))


# --8<-- [end:example]
