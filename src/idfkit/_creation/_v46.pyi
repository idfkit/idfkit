"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class ComponentCostLineItem_v8_9_to_v9_5:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        line_item_type: Literal[
            "Chiller:Electric",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:DX",
            "Coil:Heating:Fuel",
            "Construction",
            "Daylighting:Controls",
            "General",
            "Generator:Photovoltaic",
            "Lights",
            "Shading:Zone:Detailed",
        ],
        item_name: str,
        type: str | None = ...,
        object_end_use_key: str | None = ...,
        cost_per_each: float | None = ...,
        cost_per_area: float | None = ...,
        cost_per_unit_of_output_capacity: float | None = ...,
        cost_per_unit_of_output_capacity_per_cop: float | None = ...,
        cost_per_volume: float | None = ...,
        cost_per_volume_rate: float | None = ...,
        cost_per_energy_per_temperature_difference: float | None = ...,
        quantity: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ComponentCost:LineItem`` and add it to the document.

        Each instance of this object creates a cost line item and will contribute to the total for a cost estimate.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/energyplus-economics/cost-estimating/#componentcostlineitem
        """

class HybridModelZone_v9_1_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        begin_month: float,
        begin_day_of_month: float,
        end_month: float,
        end_day_of_month: float,
        calculate_zone_internal_thermal_mass: Literal["No", "Yes"] | None = "No",
        calculate_zone_air_infiltration_rate: Literal["No", "Yes"] | None = "No",
        calculate_zone_people_count: Literal["No", "Yes"] | None = "No",
        zone_measured_air_temperature_schedule_name: str | None = ...,
        zone_measured_air_humidity_ratio_schedule_name: str | None = ...,
        zone_measured_air_co2_concentration_schedule_name: str | None = ...,
        zone_input_people_activity_schedule_name: str | None = ...,
        zone_input_people_sensible_heat_fraction_schedule_name: str | None = ...,
        zone_input_people_radiant_heat_fraction_schedule_name: str | None = ...,
        zone_input_people_co2_generation_rate_schedule_name: str | None = ...,
        zone_input_supply_air_temperature_schedule_name: str | None = ...,
        zone_input_supply_air_mass_flow_rate_schedule_name: str | None = ...,
        zone_input_supply_air_humidity_ratio_schedule_name: str | None = ...,
        zone_input_supply_air_co2_concentration_schedule_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``HybridModel:Zone`` and add it to the document.

        Zones with measured air temperature data and a range of dates. If the range of temperature measurement dates includes a leap day, the weather data should include a leap day.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-hybrid-model/#hybridmodelzone
        """

class LifeCycleCostUsePriceEscalation_v22_2_to_v23_1:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        lcc_price_escalation_name: str,
        resource: Literal[
            "Coal",
            "Diesel",
            "Electricity",
            "ElectricityNet",
            "ElectricityProduced",
            "ElectricityPurchased",
            "ElectricitySurplusSold",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Steam",
            "Water",
        ],
        escalation_start_year: int | None = ...,
        escalation_start_month: Literal[
            "April",
            "August",
            "December",
            "February",
            "January",
            "July",
            "June",
            "March",
            "May",
            "November",
            "October",
            "September",
        ]
        | None = "January",
        escalations: Sequence[
            _g.LifeCycleCostUsePriceEscalationEscalationsItem | _g.LifeCycleCostUsePriceEscalationEscalationsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``LifeCycleCost:UsePriceEscalation`` and add it to the document.

        Life cycle cost escalation factors. The values for this object may be found in the annual supplement to NIST Handbook 135 in Tables Ca-1 to Ca-5 and are included in an EnergyPlus dataset file.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/energyplus-economics/lifecyclecost-usepriceescalation/#lifecyclecostusepriceescalation
        """
