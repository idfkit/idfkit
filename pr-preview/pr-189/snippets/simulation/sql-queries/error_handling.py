from __future__ import annotations

from idfkit.simulation import SimulationResult


# --8<-- [start:example]
def read_zone_temperature(result: SimulationResult) -> None:
    sql = result.sql
    if sql is None:
        print("No SQL output - was Output:SQLite in the model?")
        return

    # Get time series (raises KeyError if not found)
    try:
        ts = sql.get_timeseries("Nonexistent Variable", "ZONE 1")
    except KeyError as e:
        print(f"Variable not found: {e}")


# --8<-- [end:example]
