"""Reviewed table: object type to component category (research R-36).

A category comes from the object type alone, by exact type first and then by the longest matching
type prefix. It never comes from an object's name, so it is a fact about the model and not a
guess. A type that matches nothing here is ``other``; ``tests/test_hvac_categories.py`` lists every
node-bearing type that ends up there, so the table is reviewed whenever the rules are regenerated.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Final

from idfkit.hvac.types import ComponentCategory

_C = ComponentCategory

EXACT: Final[dict[str, ComponentCategory]] = {
    "ZONEHVAC:AIRDISTRIBUTIONUNIT": _C.TERMINAL_UNIT,
}
"""Exact upper-cased object types, checked before any prefix."""

PREFIXES: Final[tuple[tuple[str, ComponentCategory], ...]] = (
    ("COIL:HEATING:", _C.HEATING_COIL),
    ("COIL:COOLING:", _C.COOLING_COIL),
    ("FAN:", _C.FAN),
    ("PUMP:", _C.PUMP),
    ("HEADEREDPUMPS:", _C.PUMP),
    ("AIRTERMINAL:", _C.TERMINAL_UNIT),
    ("CHILLER:", _C.CHILLER),
    ("CHILLERHEATER:", _C.CHILLER),
    ("BOILER:", _C.BOILER),
    ("COOLINGTOWER:", _C.HEAT_REJECTION),
    ("FLUIDCOOLER:", _C.HEAT_REJECTION),
    ("EVAPORATIVEFLUIDCOOLER:", _C.HEAT_REJECTION),
    ("HUMIDIFIER:", _C.HUMIDIFIER),
    ("HEATEXCHANGER:", _C.HEAT_EXCHANGER),
    ("ZONEHVAC:", _C.ZONE_EQUIPMENT),
    ("AIRLOOPHVAC:UNITARY", _C.UNITARY),
    ("COILSYSTEM:", _C.UNITARY),
    ("AIRLOOPHVAC:OUTDOORAIRSYSTEM", _C.OUTDOOR_AIR),
    ("OUTDOORAIR:", _C.OUTDOOR_AIR),
    ("SETPOINTMANAGER:", _C.SETPOINT_MANAGER),
    ("CONTROLLER:", _C.CONTROLLER),
)
"""Upper-cased type prefixes. The longest match wins, so order does not decide."""


@lru_cache(maxsize=2048)
def category_of(object_type: str) -> ComponentCategory:
    """Return the component category of an object type.

    The category is decided by the type alone: an exact entry first, then the longest matching
    prefix. A type that matches nothing, including an unknown one, is ``other``.

    Args:
        object_type: An EnergyPlus object type, in any letter case.

    Returns:
        The category.

    Examples:
        >>> category_of("Coil:Heating:Water").value
        'heating_coil'
        >>> category_of("ZoneHVAC:AirDistributionUnit").value
        'terminal_unit'
        >>> category_of("ZoneHVAC:FourPipeFanCoil").value
        'zone_equipment'
        >>> category_of("Branch").value
        'other'
    """
    upper = object_type.upper()
    exact = EXACT.get(upper)
    if exact is not None:
        return exact
    best: ComponentCategory = _C.OTHER
    best_len = 0
    for prefix, category in PREFIXES:
        if len(prefix) > best_len and upper.startswith(prefix):
            best, best_len = category, len(prefix)
    return best
