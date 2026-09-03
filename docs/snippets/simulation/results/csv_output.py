from __future__ import annotations

from idfkit.simulation import CSVResult, SimulationResult

csv_result: CSVResult | None = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
csv_result = result.csv
if csv_result is not None:
    # List all columns
    for col in csv_result.columns:
        print(f"{col.variable_name} ({col.key_value}) [{col.units}]")

    # Get data for a specific column
    column = csv_result.get_column("Zone Mean Air Temperature", "THERMAL ZONE 1")
    if column is not None:
        values = column.values
# --8<-- [end:example]
