"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class GasEquipment_v9_6_to_v23_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
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
        """Create a new ``GasEquipment`` and add it to the document.

        Sets internal gains and contaminant rates for gas equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.2/io-reference/overview/group-internal-gains-people-lights-other/#gasequipment
        """

class GroundHeatExchangerSurface_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        fluid_inlet_node_name: str,
        fluid_outlet_node_name: str,
        hydronic_tubing_inside_diameter: float | None = ...,
        number_of_tubing_circuits: float | None = ...,
        hydronic_tube_spacing: float | None = ...,
        surface_length: float | None = ...,
        surface_width: float | None = ...,
        lower_surface_environment: Literal["", "Exposed", "Ground"] | None = "Ground",
    ) -> None:
        """Create a new ``GroundHeatExchanger:Surface`` and add it to the document.

        A hydronic surface/panel consisting of a multi-layer construction with embedded rows of tubes. Typically used in hybrid geothermal systems and included in the condenser loop. This component may also be used as a simple solar collector. The bottom surface may be defined as ground-coupled or exposed to wind (eg. bridge deck).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-condenser-equipment/#groundheatexchangersurface
        """

class MeterCustomDecrement_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        source_meter_name: str,
        fuel_type: Literal[
            "Coal",
            "Diesel",
            "Electricity",
            "FuelOil#1",
            "FuelOil#2",
            "Gasoline",
            "Generic",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "PropaneGas",
            "Water",
        ]
        | None = ...,
        variable_details: Sequence[
            _g.MeterCustomDecrementVariableDetailsItem | _g.MeterCustomDecrementVariableDetailsGroup
        ] = ...,
    ) -> None:
        """Create a new ``Meter:CustomDecrement`` and add it to the document.

        Used to allow users to combine specific variables and/or meters into 'custom' meter configurations. To access these meters by name, one must first run a simulation to generate the RDD/MDD files and names.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-simulation-parameters/#metercustomdecrement
        """
