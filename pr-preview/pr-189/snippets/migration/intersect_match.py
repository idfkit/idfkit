from __future__ import annotations

from typing import Any

# `idf` is an eppy/geomeppy IDF object, not an idfkit IDFDocument: this block
# shows the API being migrated *from*.
idf: Any = ...  # type: ignore[assignment]
# --8<-- [start:example]
# geomeppy (extends eppy)
idf.intersect_match()
# --8<-- [end:example]
