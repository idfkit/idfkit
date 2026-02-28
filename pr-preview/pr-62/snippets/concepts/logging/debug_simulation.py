from __future__ import annotations

# --8<-- [start:example]
import logging

# Turn on DEBUG for the simulation subsystem
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)
logging.getLogger("idfkit.simulation").setLevel(logging.DEBUG)

# Now run a simulation — every step is visible:
#   DEBUG idfkit.simulation.config  Trying candidate /usr/local/EnergyPlus-24-2-0
#   INFO  idfkit.simulation.config  Found EnergyPlus 24.2.0 at /usr/local/EnergyPlus-24-2-0
#   DEBUG idfkit.simulation.runner  EnergyPlus: /usr/local/.../energyplus (version 24.2.0)
#   INFO  idfkit.simulation.runner  Starting simulation with weather weather.epw
#   DEBUG idfkit.simulation.runner  Cache miss for key a1b2c3d4e5f6
#   DEBUG idfkit.simulation.runner  Command: /usr/local/.../energyplus -w weather.epw -d ...
#   INFO  idfkit.simulation.runner  Simulation completed successfully in 12.3s
# --8<-- [end:example]
