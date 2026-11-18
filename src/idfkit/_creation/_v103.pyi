"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class OtherEquipment_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_name: str,
        schedule_name: str,
        fuel_type: Literal[
            "",
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeating",
            "Electricity",
            "FuelOil#1",
            "FuelOil#2",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
            "PropaneGas",
            "Steam",
            "Water",
        ]
        | None = "None",
        design_level_calculation_method: Literal[
            "", "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_zone_floor_area: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        carbon_dioxide_generation_rate: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``OtherEquipment`` and add it to the document.

        Sets internal gains or losses for 'other' equipment in the zone.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-internal-gains-people-lights-other/#otherequipment
        """
