from __future__ import annotations

from typing import Any

fig: Any = ...  # type: ignore[assignment]
# --8<-- [start:example]
fig.write_html("plot.html")
fig.write_image("plot.png")  # Requires kaleido
fig.write_image("plot.pdf")
# --8<-- [end:example]
