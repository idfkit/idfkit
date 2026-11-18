"""How a whole number in a ``"number"`` field is stored.

The value is kept as it arrived: no ``int`` is turned into a ``float``. A field typed ``float``
accepts an ``int`` (PEP 484), and EnergyPlus's own ``ConvertInputFormat`` writes whole numbers in
number fields as ``0``, not ``0.0``. Coercing them at load would make every epJSON round trip rewrite
those literals. Readers that need to tell a number from ``"Autocalculate"`` or ``None`` test for the
string and for ``None``, not with ``isinstance(value, float)``.
"""

from __future__ import annotations

import json
from pathlib import Path

from idfkit import load_epjson, load_idf, new_document, write_epjson, write_idf


def test_add_assign_and_update_keep_an_int() -> None:
    doc = new_document()
    zone = doc.zones.add("A", ceiling_height=3)
    assert type(zone.ceiling_height) is int
    zone.ceiling_height = 4
    assert type(zone.ceiling_height) is int
    zone.update(ceiling_height=5)
    assert type(zone.ceiling_height) is int


def test_idf_load_reads_a_number_field_as_float(tmp_path: Path) -> None:
    doc = new_document()
    doc.zones.add("A", ceiling_height=3)
    path = tmp_path / "a.idf"
    path.write_text(write_idf(doc))
    loaded = load_idf(path)
    assert type(loaded["Zone"]["A"].ceiling_height) is float
    assert loaded["Zone"]["A"].ceiling_height == 3


def test_int_and_float_write_the_same_idf_text() -> None:
    doc = new_document()
    doc.zones.add("A", ceiling_height=3)
    doc.zones.add("B", ceiling_height=3.0)
    lines = [line for line in write_idf(doc).splitlines() if "Ceiling Height" in line]
    assert len(lines) == 2
    assert lines[0] == lines[1]


def test_epjson_round_trip_keeps_whole_numbers_as_written(tmp_path: Path) -> None:
    doc = new_document()
    doc.zones.add("A", ceiling_height=3, x_origin=1.5)
    path = tmp_path / "a.epJSON"
    path.write_text(write_epjson(doc))
    loaded = load_epjson(path)
    zone = json.loads(write_epjson(loaded))["Zone"]["A"]
    assert type(zone["ceiling_height"]) is int
    assert type(zone["x_origin"]) is float
