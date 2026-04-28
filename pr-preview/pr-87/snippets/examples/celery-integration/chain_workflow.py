from __future__ import annotations

# --8<-- [start:example]
from celery import Celery, chain

app = Celery("tasks")
app.config_from_object("celeryconfig")


@app.task(name="collect_results")
def collect_results(sim_result: dict) -> dict:
    """Post-process a simulation result (runs after the simulation task)."""
    if not sim_result["success"]:
        return {"error": "simulation failed", **sim_result}

    from idfkit.simulation import SimulationResult

    result = SimulationResult.from_directory(sim_result["output_dir"])
    heating = result.sql.get_timeseries(
        variable_name="Zone Ideal Loads Heating Energy",
        key_value="OFFICE",
    )
    return {
        **sim_result,
        "peak_heating_W": float(heating.max()),
    }


# Compose: simulate → collect_results
from tasks import simulate_building

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
