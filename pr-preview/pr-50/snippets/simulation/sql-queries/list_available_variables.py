from __future__ import annotations

from idfkit.simulation import OutputVariableIndex, SQLResult

sql: SQLResult | None = ...  # type: ignore[assignment]
variables: OutputVariableIndex | None = ...  # type: ignore[assignment]
# --8<-- [start:example]
variables = sql.list_variables()

for var in variables[:10]:
    print(f"{var.name} ({var.key_value}) [{var.units}] - {var.frequency}")
# --8<-- [end:example]
