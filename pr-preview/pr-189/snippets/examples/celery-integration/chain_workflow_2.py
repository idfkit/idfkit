from __future__ import annotations

# --8<-- [start:example]
# submit.py — compose: simulate → collect_results
from celery import chain

from tasks import collect_results, simulate_building

workflow = chain(
    simulate_building.s(
        idf_path="models/office.idf",
        weather_path="weather/chicago.epw",
        output_dir="/tmp/sim-results/chained",
        design_day=True,
    ),
    collect_results.s(),
)

final = workflow.apply_async()
print(final.get(timeout=3600))
# --8<-- [end:example]
