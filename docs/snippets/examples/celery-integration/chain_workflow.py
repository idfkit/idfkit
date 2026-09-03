from __future__ import annotations

# --8<-- [start:example]
# tasks.py
from celery import Celery

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
        "peak_heating_W": max(heating.values),
    }


# --8<-- [end:example]
