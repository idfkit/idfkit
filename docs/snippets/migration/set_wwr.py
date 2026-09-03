from __future__ import annotations

from typing import Any

# `idf` is an eppy/geomeppy IDF object, not an idfkit IDFDocument: this block
# shows the API being migrated *from*.
idf: Any = ...  # type: ignore[assignment]
# --8<-- [start:example]
# geomeppy (extends eppy)
idf.set_wwr(0.4)
idf.set_wwr(0.4, construction="SimpleGlazing")
idf.set_wwr(0.25, orientation="south")
# --8<-- [end:example]
