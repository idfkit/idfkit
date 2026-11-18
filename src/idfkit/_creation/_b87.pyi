"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class AnyZoneAirMassFlowConservation:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        infiltration_balancing_method: Literal["AddInfiltrationFlow", "AdjustInfiltrationFlow", "None"]
        | None = "AddInfiltrationFlow",
        infiltration_balancing_zones: Literal["AllZones", "MixingSourceZonesOnly"] | None = "MixingSourceZonesOnly",
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneAirMassFlowConservation`` and add it to the document.

        Enforces the zone air mass flow balance by either adjusting zone mixing object flow only, adjusting zone total return flow only, zone mixing and the zone total return flows, or adjusting the zone total return and zone mixing object flows. Zone infiltration flow air flow is increased or decreased depending user selection in the infiltration treatment method. If either of zone mixing or zone return flow adjusting methods or infiltration is active, then the zone air mass flow balance calculation will attempt to enforce conservation of mass for each zone. If flow balancing method is 'None' and infiltration is 'None', then the zone air mass flow calculation defaults to assume self-balanced simple flow mixing and infiltration objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zoneairmassflowconservation
        """

class AnyOtherEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        schedule_name: str,
        fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "Electricity",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
        ]
        | None = "None",
        design_level_calculation_method: Literal[
            "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        carbon_dioxide_generation_rate: float | None = 0,
        end_use_subcategory: str | None = "General",
        validate: bool = True,
    ) -> None:
        """Create a new ``OtherEquipment`` and add it to the document.

        Sets internal gains or losses for 'other' equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#otherequipment
        """

class CoilSystemHeatingDX:
    def __call__(
        self,
        name: str,
        /,
        *,
        heating_coil_object_type: Literal["Coil:Heating:DX:SingleSpeed", "Coil:Heating:DX:VariableSpeed"],
        heating_coil_name: str,
        availability_schedule_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``CoilSystem:Heating:DX`` and add it to the document.

        Virtual container component that consists of a DX heating coil (heat pump) and its associated controls. This control object supports two different types of DX heating coils and may be placed directly in an air loop branch or outdoor air equipment list.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilsystemheatingdx
        """

class SolarCollectorPerformanceIntegralCollectorStorage:
    def __call__(
        self,
        name: str,
        /,
        *,
        ics_collector_type: Literal["RectangularTank"] | None = "RectangularTank",
        gross_area: float | None = ...,
        collector_water_volume: float | None = ...,
        bottom_heat_loss_conductance: float | None = 0.4,
        side_heat_loss_conductance: float | None = 0.6,
        aspect_ratio: float | None = 0.8,
        collector_side_height: float | None = 0.2,
        thermal_mass_of_absorber_plate: float | None = 0,
        number_of_covers: int | None = 2,
        cover_spacing: float | None = 0.05,
        refractive_index_of_outer_cover: float | None = 1.526,
        extinction_coefficient_times_thickness_of_outer_cover: float | None = 0.045,
        emissivity_of_outer_cover: float | None = 0.88,
        refractive_index_of_inner_cover: float | None = 1.37,
        extinction_coefficient_times_thickness_of_the_inner_cover: float | None = 0.008,
        emissivity_of_inner_cover: float | None = 0.88,
        absorptance_of_absorber_plate: float | None = 0.96,
        emissivity_of_absorber_plate: float | None = 0.3,
        validate: bool = True,
    ) -> None:
        """Create a new ``SolarCollectorPerformance:IntegralCollectorStorage`` and add it to the document.

        Thermal and optical performance parameters for a single glazed solar collector with integral storage unit.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-solar-collectors/#solarcollectorperformanceintegralcollectorstorage
        """

class RefrigerationGasCoolerAirCooled:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_total_heat_rejection_rate_curve_name: str,
        gas_cooler_fan_speed_control_type: Literal["Fixed", "FixedLinear", "TwoSpeed", "VariableSpeed"]
        | None = "Fixed",
        rated_fan_power: float | None = 5000,
        minimum_fan_air_flow_ratio: float | None = 0.2,
        transition_temperature: float | None = 27,
        transcritical_approach_temperature: float | None = 3,
        subcritical_temperature_difference: float | None = 10,
        minimum_condensing_temperature: float | None = 10,
        air_inlet_node_name: str | None = ...,
        end_use_subcategory: str | None = "General",
        gas_cooler_refrigerant_operating_charge_inventory: float | None = 0,
        gas_cooler_receiver_refrigerant_inventory: float | None = 0,
        gas_cooler_outlet_piping_refrigerant_inventory: float | None = 0,
        validate: bool = True,
    ) -> None:
        """Create a new ``Refrigeration:GasCooler:AirCooled`` and add it to the document.

        The transcritical refrigeration system requires a single gas cooler to reject the system heat.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationgascooleraircooled
        """

class ElectricLoadCenterGenerators:
    def __call__(
        self,
        name: str,
        /,
        *,
        generator_outputs: Sequence[
            _g.ElectricLoadCenterGeneratorsGeneratorOutputsItem | _g.ElectricLoadCenterGeneratorsGeneratorOutputsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ElectricLoadCenter:Generators`` and add it to the document.

        List of electric power generators to include in the simulation including the name and type of each generators along with availability schedule, rated power output, and thermal-to-electrical power ratio.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#electricloadcentergenerators
        """
