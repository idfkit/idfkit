from __future__ import annotations

# --8<-- [start:example]
from scythe.worker import ScytheWorkerConfig

# Import your experiments so they are registered
from experiments.building_energy import simulate_building  # noqa: F401

if __name__ == "__main__":
    worker_config = ScytheWorkerConfig()
    worker_config.start()
# --8<-- [end:example]
