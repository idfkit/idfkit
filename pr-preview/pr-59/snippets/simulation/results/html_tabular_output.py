from __future__ import annotations

from idfkit.simulation import HTMLResult, SimulationResult
from typing import Any

data: Any = ...  # type: ignore[assignment]
html: HTMLResult | None = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
table: Any = ...  # type: ignore[assignment]
# --8<-- [start:example]
html = result.html
if html is not None:
    # Iterate all tables
    for table in html:
        print(f"{table.title}: {len(table.rows)} rows")

    # eppy-compatible (title, rows) pairs
    for title, rows in html.titletable():
        print(title)

    # Look up a table by title (case-insensitive substring match)
    table = html.tablebyname("Site and Source Energy")
    if table:
        data = table.to_dict()  # {row_key: {col_header: value}}
        print(data)

    # Get all tables from a specific report
    annual = html.tablesbyreport("Annual Building Utility Performance Summary")

    # Access by index
    first = html.tablebyindex(0)
# --8<-- [end:example]
