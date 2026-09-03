from __future__ import annotations

# --8<-- [start:example]
from eppy import readhtml

with open("eplustbl.htm") as f:
    html = f.read()
tables = readhtml.titletable(html)
# --8<-- [end:example]
