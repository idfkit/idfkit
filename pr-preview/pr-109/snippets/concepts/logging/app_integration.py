from __future__ import annotations

# --8<-- [start:example]
import logging

# Your application's own logger
app_logger = logging.getLogger("myapp")

# Configure the root logger once (controls everything)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

# Fine-tune individual libraries
logging.getLogger("idfkit").setLevel(logging.INFO)
logging.getLogger("idfkit.simulation").setLevel(logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)

app_logger.info("Starting energy model workflow")
# Both your logs and idfkit logs flow through the same handlers
# --8<-- [end:example]
