"""Non-finite numbers (NaN and infinity), which no EnergyPlus field takes.

A NaN usually arrives from a pandas column with a missing value. Neither format can carry one:
``json`` writes ``NaN``, which is not JSON and which EnergyPlus's epJSON reader refuses, and the IDF
writer writes ``nan``, which EnergyPlus reads as something else and fails on far from the cause.
These helpers let the places a value enters a document, and the places it leaves, name the field.
"""

from __future__ import annotations

import math
from collections.abc import Iterator, Mapping
from typing import Any, cast

#: The reason given wherever a non-finite value is refused.
NON_FINITE_DETAIL = "NaN and infinity are not numbers EnergyPlus or epJSON can hold; give a finite number"


def is_non_finite(value: object) -> bool:
    """Whether *value* is a float NaN or infinity (a ``numpy.float64`` is a ``float``, so it counts)."""
    return isinstance(value, float) and not math.isfinite(value)


def non_finite_fields(data: Mapping[str, Any]) -> Iterator[tuple[str, float]]:
    """``(field, value)`` for each non-finite value in an object's *data*, groups included.

    A value inside an extensible group is named ``wrapper[i].slot``, ``i`` counting from 0 as the
    list is indexed.
    """
    for key, value in data.items():
        if isinstance(value, float):
            if not math.isfinite(value):
                yield key, value
        elif isinstance(value, list):
            for index, group in enumerate(cast("list[Any]", value)):
                if isinstance(group, dict):
                    for slot, item in cast("dict[str, Any]", group).items():
                        if isinstance(item, float) and not math.isfinite(item):
                            yield f"{key}[{index}].{slot}", item
                elif isinstance(group, float) and not math.isfinite(group):
                    yield f"{key}[{index}]", group


def non_finite_message(where: str, field_name: str, value: float) -> str:
    """The message for a non-finite *value* in *field_name* of the object described by *where*."""
    return f"{where} field {field_name!r} is {value!r}. {NON_FINITE_DETAIL}."
