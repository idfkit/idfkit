from __future__ import annotations

html_string: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation.parsers.html import HTMLResult

html = HTMLResult.from_file("eplustbl.htm")
html = HTMLResult.from_string(html_string)
# --8<-- [end:example]
