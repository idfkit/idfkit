from __future__ import annotations

# --8<-- [start:example]
# submit.py — send a single simulation to the queue
from tasks import simulate_building

result = simulate_building.delay(
    idf_path="models/office.idf",
    weather_path="weather/chicago.epw",
    output_dir="/tmp/sim-results/run-001",
    design_day=True,
)

# Block until done (or poll with result.ready())
summary = result.get(timeout=3600)
print(summary)
# {"success": True, "runtime": 42.3, "output_dir": "/tmp/sim-results/run-001"}
# --8<-- [end:example]
