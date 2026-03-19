from __future__ import annotations

# --8<-- [start:example]
from idfkit.simulation import get_default_backend

backend = get_default_backend()
print(type(backend).__name__)  # MatplotlibBackend or PlotlyBackend
# --8<-- [end:example]
