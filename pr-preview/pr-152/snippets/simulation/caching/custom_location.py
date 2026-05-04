from __future__ import annotations

from idfkit.simulation import SimulationCache

# --8<-- [start:example]
from pathlib import Path

cache = SimulationCache(cache_dir=Path("/data/sim_cache"))
# --8<-- [end:example]
