"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class AnyShadowCalculation:
    def __call__(
        self,
        /,
        *,
        maximum_figures_in_shadow_overlap_calculations: int | None = 15000,
        polygon_clipping_algorithm: Literal["", "ConvexWeilerAtherton", "SutherlandHodgman"]
        | None = "SutherlandHodgman",
        sky_diffuse_modeling_algorithm: Literal["", "DetailedSkyDiffuseModeling", "SimpleSkyDiffuseModeling"]
        | None = "SimpleSkyDiffuseModeling",
        output_external_shading_calculation_results: Literal["", "No", "Yes"] | None = "No",
        disable_self_shading_within_shading_zone_groups: Literal["", "No", "Yes"] | None = "No",
        disable_self_shading_from_shading_zone_groups_to_other_zones: Literal["", "No", "Yes"] | None = "No",
        shading_zone_groups: Sequence[
            _g.ShadowCalculationShadingZoneGroupsItem | _g.ShadowCalculationShadingZoneGroupsGroup
        ] = ...,
    ) -> None:
        """Create a new ``ShadowCalculation`` and add it to the document.

        This object is used to control details of the solar, shading, and daylighting models

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#shadowcalculation
        """

class OtherEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        fuel_type: Literal[
            "",
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = "None",
        design_level_calculation_method: Literal[
            "", "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_floor_area: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        carbon_dioxide_generation_rate: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``OtherEquipment`` and add it to the document.

        Sets internal gains or losses for 'other' equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#otherequipment
        """

class AirLoopHVACSupplyPlenum:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        zone_node_name: str,
        inlet_node_name: str,
        nodes: Sequence[_g.AirLoopHVACSupplyPlenumNodesItem | _g.AirLoopHVACSupplyPlenumNodesGroup] = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:SupplyPlenum`` and add it to the document.

        Connects 1 zone inlet air stream, through zone supply plenum, to one or more outlets. Node names cannot be duplicated within a single supply plenum list.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-path/#airloophvacsupplyplenum
        """

class SetpointManagerSingleZoneOneStageCooling:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_zone_name: str,
        setpoint_node_or_nodelist_name: str,
        cooling_stage_on_supply_air_setpoint_temperature: float | None = -99,
        cooling_stage_off_supply_air_setpoint_temperature: float | None = 99,
    ) -> None:
        """Create a new ``SetpointManager:SingleZone:OneStageCooling`` and add it to the document.

        This object can be used with CoilSystem:Cooling:DX to model on/off cycling control of single stage air systems. Setpoints are modulated to run coil full on or full off depending on zone conditions. Intended for use with ZoneControl:Thermostat:StagedDualSetpoint

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagersinglezoneonestagecooling
        """

class GeneratorFuelCellAuxiliaryHeater:
    def __call__(
        self,
        name: str,
        /,
        *,
        excess_air_ratio: float | None = ...,
        ancillary_power_constant_term: float | None = ...,
        ancillary_power_linear_term: float | None = ...,
        skin_loss_u_factor_times_area_value: float | None = ...,
        skin_loss_destination: Literal["AirInletForFuelCell", "SurroundingZone"] | None = ...,
        zone_name_to_receive_skin_losses: str | None = ...,
        heating_capacity_units: Literal["Watts", "kmol/s"] | None = ...,
        maximum_heating_capacity_in_watts: float | None = ...,
        minimum_heating_capacity_in_watts: float | None = ...,
        maximum_heating_capacity_in_kmol_per_second: float | None = ...,
        minimum_heating_capacity_in_kmol_per_second: float | None = ...,
    ) -> None:
        """Create a new ``Generator:FuelCell:AuxiliaryHeater`` and add it to the document.

        Intended for modeling an auxiliary heater for a fuel cell power generator, however this portion of the model is not yet available. The program still requires one of these objects be included even though the data are not yet used (so that internal data structures can be allocated).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatorfuelcellauxiliaryheater
        """
