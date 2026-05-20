from __future__ import annotations

from idfkit.simulation import SQLResult

sql: SQLResult | None = ...  # type: ignore[assignment]
# --8<-- [start:example]
rows = sql.get_tabular_data(report_name="AnnualBuildingUtilityPerformanceSummary")

for row in rows[:5]:
    print(f"{row.table_name} | {row.row_name} | {row.column_name}: {row.value}")
# --8<-- [end:example]
