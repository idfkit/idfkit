"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class GasEquipment_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_name: str,
        schedule_name: str,
        design_level_calculation_method: Literal[
            "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
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
        validate: bool = True,
    ) -> None:
        """Create a new ``GasEquipment`` and add it to the document.

        Sets internal gains and contaminant rates for gas equipment in the zone. If you use a ZoneList in the Zone name field then this definition applies to all those zones.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-internal-gains-people-lights-other/#gasequipment
        """

class ZoneHVACBaseboardRadiantConvectiveSteam_v8_9_to_v9_4:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        maximum_steam_flow_rate: float | Literal["Autosize"],
        fraction_radiant: float,
        availability_schedule_name: str | None = ...,
        heating_design_capacity_method: Literal[
            "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity: float | Literal["Autosize"] | None = "Autosize",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = 1,
        degree_of_subcooling: float | None = 5,
        convergence_tolerance: float | None = 0.001,
        fraction_of_radiant_energy_incident_on_people: float | None = ...,
        surface_fractions: Sequence[
            _g.ZoneHVACBaseboardRadiantConvectiveSteamSurfaceFractionsItem
            | _g.ZoneHVACBaseboardRadiantConvectiveSteamSurfaceFractionsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneHVAC:Baseboard:RadiantConvective:Steam`` and add it to the document.

        The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list

        ``surface_fractions`` takes the extensible groups in order, one dict per group:

        ```python
        doc["ZoneHVAC:Baseboard:RadiantConvective:Steam"].add(
            "ZoneHVAC Baseboard RadiantConvective Steam 1",
            inlet_node_name="Inlet Node Name",
            outlet_node_name="Outlet Node Name",
            maximum_steam_flow_rate=2.0,
            fraction_radiant=0.0,
            surface_fractions=[
                {"surface_name": "Surface 1", "fraction_of_radiant_energy_to_surface": 0.0},
                {"surface_name": "Surface 2", "fraction_of_radiant_energy_to_surface": 0.0},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-radiative-convective-units/#zonehvacbaseboardradiantconvectivesteam
        """

class CoilHeatingFuel_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        fuel_type: Literal[
            "Diesel", "FuelOil#1", "FuelOil#2", "Gas", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2", "Propane"
        ]
        | None = "Gas",
        burner_efficiency: float | None = 0.8,
        nominal_capacity: float | Literal["Autosize"] | None = ...,
        temperature_setpoint_node_name: str | None = ...,
        parasitic_electric_load: float | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
        parasitic_fuel_load: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:Heating:Fuel`` and add it to the document.

        Gas or other fuel heating coil. If the coil is located directly in an air loop branch or outdoor air equipment list, then it is controlled on leaving air temperature and the Temperature Setpoint Node Name must be specified. If the coil is contained within another component such as an air terminal unit, zone HVAC equipment, or unitary system, then the coil is controlled by the parent component and the setpoint node name is not entered.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/energyplus-economics/cost-estimating/#coilheatingfuel
        """
