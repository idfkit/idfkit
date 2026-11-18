"""Type-check fixture for the public loaders (never called; checked by ``make check``).

``load_idf``, ``load_idf_with_diagnostics`` and ``load_epjson`` accept a ``pathlib.Path`` as well as a
``str``, the same as ``save_idf`` and ``save_epjson``. Each seeded error below carries a ``pyright: ignore``
naming the rule it must trigger, and this file turns on ``reportUnnecessaryTypeIgnoreComment``, so the
fixture proves a non-path argument is still rejected.
"""

# pyright: strict, reportUnnecessaryTypeIgnoreComment=true

from __future__ import annotations

from pathlib import Path

from idfkit import load_epjson, load_idf, load_idf_with_diagnostics


def correct_calls(folder: Path) -> None:
    load_idf(folder / "model.idf")
    load_idf("model.idf")
    load_idf(Path("model.idf"), strict=False)
    load_idf_with_diagnostics(folder / "model.idf")
    load_epjson(folder / "model.epJSON")
    load_epjson(Path("model.epJSON"), strict=False)


def seeded_errors() -> None:
    load_idf(42)  # pyright: ignore[reportArgumentType]
    load_epjson(b"model.epJSON")  # pyright: ignore[reportArgumentType]
