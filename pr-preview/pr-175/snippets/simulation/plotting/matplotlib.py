from __future__ import annotations

from typing import Any

fig: Any = ...  # type: ignore[assignment]
# --8<-- [start:example]
fig.savefig("plot.png", dpi=300, bbox_inches="tight")
fig.savefig("plot.pdf")
fig.savefig("plot.svg")
# --8<-- [end:example]
