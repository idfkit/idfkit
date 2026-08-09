from __future__ import annotations

# --8<-- [start:example]
from celery import group
from tasks import simulate_building

# Fan-out: submit many simulations at once
jobs = group(
    simulate_building.s(
        idf_path=f"models/variant_{i}.idf",
        weather_path="weather/chicago.epw",
        output_dir=f"/tmp/sim-results/variant-{i}",
    )
    for i in range(20)
)

batch = jobs.apply_async()

# Wait for all results
results = batch.get(timeout=7200)
succeeded = [r for r in results if r["success"]]
print(f"{len(succeeded)}/{len(results)} simulations succeeded")
# --8<-- [end:example]
