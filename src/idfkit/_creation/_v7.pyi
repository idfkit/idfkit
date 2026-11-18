"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class DistrictHeating_v8_9_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        hot_water_inlet_node_name: str,
        hot_water_outlet_node_name: str,
        nominal_capacity: float | Literal["Autosize"] | None = ...,
        capacity_fraction_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``DistrictHeating`` and add it to the document.

        Centralized source of hot water, such as a district heating system.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-plant-heating-and-cooling-equipment/#districtheating
        """

class ZoneHVACOutdoorAirUnitEquipmentList_v8_9:
    def __call__(
        self,
        name: str,
        /,
        *,
        component_1_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_1_name: str | None = ...,
        component_2_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_2_name: str | None = ...,
        component_3_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_3_name: str | None = ...,
        component_4_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_4_name: str | None = ...,
        component_5_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_5_name: str | None = ...,
        component_6_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_6_name: str | None = ...,
        component_7_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_7_name: str | None = ...,
        component_8_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_8_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:OutdoorAirUnit:EquipmentList`` and add it to the document.

        Equipment list for components in a ZoneHVAC:OutdoorAirUnit. Components are simulated sequentially in the order given in the equipment list.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v8.9/io-reference/overview/group-zone-forced-air-units/#zonehvacoutdoorairunitequipmentlist
        """

class SteamEquipment_v8_9_to_v9_5:
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
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``SteamEquipment`` and add it to the document.

        Sets internal gains for steam equipment in the zone.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-internal-gains-people-lights-other/#steamequipment
        """

class ZoneInfiltrationDesignFlowRate_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_name: str,
        schedule_name: str,
        design_flow_rate_calculation_method: Literal[
            "AirChanges/Hour", "Flow/Area", "Flow/ExteriorArea", "Flow/ExteriorWallArea", "Flow/Zone"
        ]
        | None = "Flow/Zone",
        design_flow_rate: float | None = ...,
        flow_per_zone_floor_area: float | None = ...,
        flow_per_exterior_surface_area: float | None = ...,
        air_changes_per_hour: float | None = ...,
        constant_term_coefficient: float | None = 1,
        temperature_term_coefficient: float | None = 0,
        velocity_term_coefficient: float | None = 0,
        velocity_squared_term_coefficient: float | None = 0,
    ) -> None:
        """Create a new ``ZoneInfiltration:DesignFlowRate`` and add it to the document.

        Infiltration is specified as a design level which is modified by a Schedule fraction, temperature difference and wind speed: Infiltration=Idesign * FSchedule * (A + B*|(Tzone-Todb)| + C*WindSpd + D * WindSpd**2) If you use a ZoneList in the Zone or ZoneList name field then this definition applies to all the zones in the ZoneList.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-airflow/#zoneinfiltrationdesignflowrate
        """

class AirTerminalSingleDuctConstantVolumeCooledBeam_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        cooled_beam_type: Literal["Active", "Passive"],
        supply_air_inlet_node_name: str,
        supply_air_outlet_node_name: str,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        supply_air_volumetric_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        maximum_total_chilled_water_volumetric_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        number_of_beams: float | Literal["Autosize"] | None = "Autosize",
        beam_length: float | Literal["Autosize"] | None = "Autosize",
        design_inlet_water_temperature: float | None = 15,
        design_outlet_water_temperature: float | None = 17,
        coil_surface_area_per_coil_length: float | None = 5.422,
        model_parameter_a: float | None = 15.3,
        model_parameter_n1: float | None = 0,
        model_parameter_n2: float | None = 0.84,
        model_parameter_n3: float | None = 0.12,
        model_parameter_a0: float | None = 0.171,
        model_parameter_k1: float | None = 0.0057,
        model_parameter_n: float | None = 0.4,
        coefficient_of_induction_kin: float | Literal["Autocalculate"] | None = "Autocalculate",
        leaving_pipe_inside_diameter: float | None = 0.0145,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:ConstantVolume:CooledBeam`` and add it to the document.

        Central air system terminal unit, single duct, constant volume, with cooled beam (active or passive).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-air-distribution-equipment/#airterminalsingleductconstantvolumecooledbeam
        """

class WindowPropertyFrameAndDivider_v22_1_to_v26_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        frame_width: float | None = 0,
        frame_outside_projection: float | None = 0,
        frame_inside_projection: float | None = 0,
        frame_conductance: float | None = ...,
        ratio_of_frame_edge_glass_conductance_to_center_of_glass_conductance: float | None = 1,
        frame_solar_absorptance: float | None = 0.7,
        frame_visible_absorptance: float | None = 0.7,
        frame_thermal_hemispherical_emissivity: float | None = 0.9,
        divider_type: Literal["DividedLite", "Suspended"] | None = "DividedLite",
        divider_width: float | None = 0,
        number_of_horizontal_dividers: float | None = 0,
        number_of_vertical_dividers: float | None = 0,
        divider_outside_projection: float | None = 0,
        divider_inside_projection: float | None = 0,
        divider_conductance: float | None = 0,
        ratio_of_divider_edge_glass_conductance_to_center_of_glass_conductance: float | None = 1,
        divider_solar_absorptance: float | None = 0,
        divider_visible_absorptance: float | None = 0,
        divider_thermal_hemispherical_emissivity: float | None = 0.9,
        outside_reveal_solar_absorptance: float | None = 0,
        inside_sill_depth: float | None = 0,
        inside_sill_solar_absorptance: float | None = 0,
        inside_reveal_depth: float | None = 0,
        inside_reveal_solar_absorptance: float | None = 0,
        nfrc_product_type_for_assembly_calculations: Literal[
            "CasementDouble",
            "CasementSingle",
            "CurtainWall",
            "DoorSidelite",
            "DoorTransom",
            "DualAction",
            "Fixed",
            "Garage",
            "Greenhouse",
            "HingedEscape",
            "HorizontalSlider",
            "Jal",
            "Pivoted",
            "ProjectingDual",
            "ProjectingSingle",
            "SideHingedDoor",
            "Skylight",
            "SlidingPatioDoor",
            "SpandrelPanel",
            "TropicalAwning",
            "TubularDaylightingDevice",
            "VerticalSlider",
        ]
        | None = "CurtainWall",
    ) -> None:
        """Create a new ``WindowProperty:FrameAndDivider`` and add it to the document.

        Specifies the dimensions of a window frame, dividers, and inside reveal surfaces. Referenced by the surface objects for exterior windows and glass doors (ref: FenestrationSurface:Detailed, Window, and GlazedDoor).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.1/io-reference/overview/group-thermal-zone-description-geometry/#windowpropertyframeanddivider
        """
