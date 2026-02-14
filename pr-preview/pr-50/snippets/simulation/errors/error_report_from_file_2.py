from __future__ import annotations

from idfkit.simulation import ErrorReport
from pathlib import Path

# --8<-- [start:example]
err_text = Path("eplusout.err").read_text()
errors = ErrorReport.from_string(err_text)
# --8<-- [end:example]
