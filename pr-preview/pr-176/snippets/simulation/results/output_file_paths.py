from __future__ import annotations

from idfkit.simulation import SimulationResult

result: SimulationResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
result.sql_path  # Path to .sql database
result.err_path  # Path to .err file
result.eso_path  # Path to .eso file
result.csv_path  # Path to .csv file
result.html_path  # Path to HTML table file
result.rdd_path  # Path to .rdd file
result.mdd_path  # Path to .mdd file
# --8<-- [end:example]
