"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class WindowMaterialGlazing:
    def __call__(
        self,
        name: str,
        /,
        *,
        optical_data_type: Literal["BSDF", "Spectral", "SpectralAndAngle", "SpectralAverage"],
        thickness: float,
        window_glass_spectral_data_set_name: str | None = ...,
        solar_transmittance_at_normal_incidence: float | None = ...,
        front_side_solar_reflectance_at_normal_incidence: float | None = ...,
        back_side_solar_reflectance_at_normal_incidence: float | None = ...,
        visible_transmittance_at_normal_incidence: float | None = ...,
        front_side_visible_reflectance_at_normal_incidence: float | None = ...,
        back_side_visible_reflectance_at_normal_incidence: float | None = ...,
        infrared_transmittance_at_normal_incidence: float | None = 0,
        front_side_infrared_hemispherical_emissivity: float | None = 0.84,
        back_side_infrared_hemispherical_emissivity: float | None = 0.84,
        conductivity: float | None = 0.9,
        dirt_correction_factor_for_solar_and_visible_transmittance: float | None = 1,
        solar_diffusing: Literal["", "No", "Yes"] | None = "No",
        young_s_modulus: float | None = 72000000000,
        poisson_s_ratio: float | None = 0.22,
        window_glass_spectral_and_incident_angle_transmittance_data_set_table_name: str | None = ...,
        window_glass_spectral_and_incident_angle_front_reflectance_data_set_table_name: str | None = ...,
        window_glass_spectral_and_incident_angle_back_reflectance_data_set_table_name: str | None = ...,
    ) -> None:
        """Create a new ``WindowMaterial:Glazing`` and add it to the document.

        Glass material properties for Windows or Glass Doors Transmittance/Reflectance input method.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialglazing
        """

class SubSurfaceConstructionAssignments:
    def __call__(
        self,
        name: str,
        /,
        *,
        fixed_window_construction_name: str | None = ...,
        operable_window_construction_name: str | None = ...,
        door_construction_name: str | None = ...,
        glass_door_construction_name: str | None = ...,
        overhead_door_construction_name: str | None = ...,
        skylight_construction_name: str | None = ...,
        tubular_daylight_dome_construction_name: str | None = ...,
        tubular_daylight_diffuser_construction_name: str | None = ...,
    ) -> None:
        """Create a new ``SubSurfaceConstructionAssignments`` and add it to the document.

        Defines construction assignments for each sub-surface type for a single boundary-condition category (exterior or interior). The generic Window type (kept for backward compatibility) resolves via the Fixed Window slot.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#subsurfaceconstructionassignments
        """

class WallInterzone:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition_object: str,
        space_name: str | None = ...,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 90,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None:
        """Create a new ``Wall:Interzone`` and add it to the document.

        Allows for simplified entry of interzone walls (walls between zones).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#wallinterzone
        """

class GasEquipment:
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
        power_per_floor_area: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        carbon_dioxide_generation_rate: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``GasEquipment`` and add it to the document.

        Sets internal gains and contaminant rates for gas equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#gasequipment
        """

class HotWaterEquipmentDefinition:
    def __call__(
        self,
        name: str,
        /,
        *,
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
    ) -> None:
        """Create a new ``HotWaterEquipment:Definition`` and add it to the document.

        Defines the physical characteristics (design level and heat gain fractions) for hot water equipment. Referenced by one or more HotWaterEquipment:Instance objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains/#hotwaterequipmentdefinition
        """

class ZoneContaminantSourceAndSinkGenericConstant:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        generation_schedule_name: str,
        removal_schedule_name: str,
        design_generation_rate: float | None = ...,
        design_removal_coefficient: float | None = ...,
    ) -> None:
        """Create a new ``ZoneContaminantSourceAndSink:Generic:Constant`` and add it to the document.

        Sets internal generic contaminant gains and sinks in a zone with constant values.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#zonecontaminantsourceandsinkgenericconstant
        """

class SpaceHVACZoneEquipmentSplitter:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        zone_equipment_object_type: Literal[
            "AirLoopHVAC:UnitarySystem",
            "HeatExchanger:AirToAir:FlatPlate",
            "WaterHeater:HeatPump:PumpedCondenser",
            "WaterHeater:HeatPump:WrappedCondenser",
            "ZoneHVAC:AirDistributionUnit",
            "ZoneHVAC:Baseboard:Convective:Electric",
            "ZoneHVAC:Baseboard:Convective:Water",
            "ZoneHVAC:Baseboard:RadiantConvective:Electric",
            "ZoneHVAC:Baseboard:RadiantConvective:Steam",
            "ZoneHVAC:Baseboard:RadiantConvective:Water",
            "ZoneHVAC:CoolingPanel:RadiantConvective:Water",
            "ZoneHVAC:Dehumidifier:DX",
            "ZoneHVAC:EnergyRecoveryVentilator",
            "ZoneHVAC:EvaporativeCoolerUnit",
            "ZoneHVAC:ForcedAir:UserDefined",
            "ZoneHVAC:FourPipeFanCoil",
            "ZoneHVAC:HighTemperatureRadiant",
            "ZoneHVAC:HybridUnitaryHVAC",
            "ZoneHVAC:IdealLoadsAirSystem",
            "ZoneHVAC:LowTemperatureRadiant:ConstantFlow",
            "ZoneHVAC:LowTemperatureRadiant:Electric",
            "ZoneHVAC:LowTemperatureRadiant:VariableFlow",
            "ZoneHVAC:OutdoorAirUnit",
            "ZoneHVAC:PackagedTerminalAirConditioner",
            "ZoneHVAC:PackagedTerminalHeatPump",
            "ZoneHVAC:RefrigerationChillerSet",
            "ZoneHVAC:TerminalUnit:VariableRefrigerantFlow",
            "ZoneHVAC:UnitHeater",
            "ZoneHVAC:UnitVentilator",
            "ZoneHVAC:VentilatedSlab",
            "ZoneHVAC:WaterToAirHeatPump",
            "ZoneHVAC:WindowAirConditioner",
        ],
        zone_equipment_name: str,
        zone_equipment_outlet_node_name: str | None = ...,
        thermostat_control_method: Literal["", "Ideal", "Maximum", "SingleSpace"] | None = "SingleSpace",
        control_space_name: str | None = ...,
        space_fraction_method: Literal[
            "", "DesignCoolingLoad", "DesignHeatingLoad", "FloorArea", "PerimeterLength", "Volume"
        ]
        | None = "DesignCoolingLoad",
        spaces: Sequence[
            _g.SpaceHVACZoneEquipmentSplitterSpacesItem | _g.SpaceHVACZoneEquipmentSplitterSpacesGroup
        ] = ...,
    ) -> None:
        """Create a new ``SpaceHVAC:ZoneEquipmentSplitter`` and add it to the document.

        Distributes the output from a piece of zone equipment to one or more Spaces in the Zone. If any equipment in a zone has a SpaceHVAC:ZoneEquipmentSplitter, then all equipment in the zone must have one. except Fan:ZoneExhaust. All spaces in the zone must also have a SpaceHVAC:EquipmentConnections object. Used only when ZoneAirHeatBalanceAlgorithm 'Do Space Heat Balance for Simulation' is Yes.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-equipment/#spacehvaczoneequipmentsplitter
        """
