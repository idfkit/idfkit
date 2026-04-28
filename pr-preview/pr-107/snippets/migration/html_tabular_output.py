from __future__ import annotations

from idfkit.simulation import HTMLResult

html: HTMLResult | None = ...  # type: ignore[assignment]
# --8<-- [start:example]
from eppy import readhtml

with open("eplustbl.htm") as f:
    html = f.read()
tables = readhtml.titletable(html)
# --8<-- [end:example]
