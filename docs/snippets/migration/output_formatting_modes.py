from __future__ import annotations

from typing import Any

# `idf` is an eppy IDF object, not an idfkit IDFDocument: this block shows the
# API being migrated *from*.
idf: Any = ...  # type: ignore[assignment]
# --8<-- [start:example]
idf.outputtype = "nocomment"
idf.saveas("out.idf")
# --8<-- [end:example]
