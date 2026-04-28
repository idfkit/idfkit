from __future__ import annotations

from idfkit.simulation import SimulationCache
from pathlib import Path

# --8<-- [start:example]
cache = SimulationCache(cache_dir=Path("/path/to/cache"))
# --8<-- [end:example]
