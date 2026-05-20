from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import HTMLResult, SimulationResult, simulate
from typing import Any

doc: IDFDocument = ...  # type: ignore[assignment]
html: HTMLResult | None = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
table: Any = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
result = simulate(doc, weather)
html = result.html  # HTMLResult, lazily parsed

# eppy-compatible (title, rows) pairs
for title, rows in html.titletable():
    print(title, len(rows), "rows")

# Lookup by name
table = html.tablebyname("Site and Source Energy")
print(table.to_dict())  # {row_key: {col_header: value}}

# Filter by report
annual = html.tablesbyreport("Annual Building Utility Performance Summary")
# --8<-- [end:example]
