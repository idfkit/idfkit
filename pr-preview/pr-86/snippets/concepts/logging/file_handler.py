from __future__ import annotations

# --8<-- [start:example]
import logging

# Create a file handler for idfkit logs
handler = logging.FileHandler("idfkit.log")
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s"))

# Attach it to the top-level idfkit logger
logging.getLogger("idfkit").addHandler(handler)
# --8<-- [end:example]
