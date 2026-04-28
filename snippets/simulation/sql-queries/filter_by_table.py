from __future__ import annotations

from idfkit.simulation import SQLResult

sql: SQLResult | None = ...  # type: ignore[assignment]
# --8<-- [start:example]
rows = sql.get_tabular_data(
    report_name="AnnualBuildingUtilityPerformanceSummary",
    table_name="Site and Source Energy",
)
# --8<-- [end:example]
