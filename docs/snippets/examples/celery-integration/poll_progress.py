from __future__ import annotations

# --8<-- [start:example]
import time

from tasks import simulate_with_progress

result = simulate_with_progress.delay(
    idf_path="models/office.idf",
    weather_path="weather/chicago.epw",
    output_dir="/tmp/sim-results/progress-demo",
)

while not result.ready():
    meta = result.info  # dict with progress metadata
    if isinstance(meta, dict) and "percent" in meta:
        pct = meta["percent"]
        env = meta["environment"]
        print(f"  {pct:.0f}%  —  {env}")
    time.sleep(2)

print("Done:", result.get())
# --8<-- [end:example]
