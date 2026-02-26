from __future__ import annotations

# --8<-- [start:example]
import logging

# Silence everything by default
logging.basicConfig(level=logging.WARNING)

# Enable verbose output only for simulation
logging.getLogger("idfkit.simulation.runner").setLevel(logging.DEBUG)

# Or enable all simulation sub-loggers at once
logging.getLogger("idfkit.simulation").setLevel(logging.DEBUG)
# --8<-- [end:example]
