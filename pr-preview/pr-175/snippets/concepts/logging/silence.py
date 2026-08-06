from __future__ import annotations

# --8<-- [start:example]
import logging

# Suppress all idfkit output
logging.getLogger("idfkit").setLevel(logging.CRITICAL)
# --8<-- [end:example]
