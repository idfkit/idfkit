from __future__ import annotations

# --8<-- [start:example]
import itertools

from celery import group
from tasks import run_parametric_case

conductivities = [0.5, 1.0, 1.5]
u_factors = [1.5, 2.5, 3.5]

jobs = group(
    run_parametric_case.s(
        base_idf_path="models/office.idf",
        weather_path="weather/chicago.epw",
        output_dir=f"/tmp/parametric/k{k}_u{u}",
        wall_conductivity=k,
        window_u_factor=u,
        label=f"k={k}, U={u}",
    )
    for k, u in itertools.product(conductivities, u_factors)
)

batch = jobs.apply_async()
results = batch.get(timeout=7200)

for r in sorted(results, key=lambda x: x["label"]):
    status = "OK" if r["success"] else "FAIL"
    print(f"[{status}] {r['label']}  ({r['runtime']:.1f}s)")
# --8<-- [end:example]
