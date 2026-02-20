from __future__ import annotations

# --8<-- [start:example]
import logging
import json
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    """Emit each log record as a single JSON line."""

    def format(self, record: logging.LogRecord) -> str:
        return json.dumps({
            "ts": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        })


handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())

logging.getLogger("idfkit").addHandler(handler)
logging.getLogger("idfkit").setLevel(logging.INFO)
# --8<-- [end:example]
