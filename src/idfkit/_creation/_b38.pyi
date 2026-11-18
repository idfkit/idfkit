"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class ScheduleFile:
    def __call__(
        self,
        name: str,
        /,
        *,
        file_name: str,
        column_number: int,
        rows_to_skip_at_top: int,
        schedule_type_limits_name: str | None = ...,
        number_of_hours_of_data: float | None = 8760,
        column_separator: Literal["", "Comma", "Semicolon", "Space", "Tab"] | None = "Comma",
        interpolate_to_timestep: Literal["", "No", "Yes"] | None = "No",
        minutes_per_item: int | None = 60,
        adjust_schedule_for_daylight_savings: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``Schedule:File`` and add it to the document.

        A Schedule:File points to a text computer file that has 8760-8784 hours of data.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#schedulefile
        """

class MaterialPropertyHeatAndMoistureTransferSorptionIsotherm:
    def __call__(
        self,
        /,
        *,
        material_name: str,
        number_of_isotherm_coordinates: int,
        relative_humidity_fraction_1: float,
        moisture_content_1: float,
        relative_humidity_fraction_2: float | None = ...,
        moisture_content_2: float | None = ...,
        relative_humidity_fraction_3: float | None = ...,
        moisture_content_3: float | None = ...,
        relative_humidity_fraction_4: float | None = ...,
        moisture_content_4: float | None = ...,
        relative_humidity_fraction_5: float | None = ...,
        moisture_content_5: float | None = ...,
        relative_humidity_fraction_6: float | None = ...,
        moisture_content_6: float | None = ...,
        relative_humidity_fraction_7: float | None = ...,
        moisture_content_7: float | None = ...,
        relative_humidity_fraction_8: float | None = ...,
        moisture_content_8: float | None = ...,
        relative_humidity_fraction_9: float | None = ...,
        moisture_content_9: float | None = ...,
        relative_humidity_fraction_10: float | None = ...,
        moisture_content_10: float | None = ...,
        relative_humidity_fraction_11: float | None = ...,
        moisture_content_11: float | None = ...,
        relative_humidity_fraction_12: float | None = ...,
        moisture_content_12: float | None = ...,
        relative_humidity_fraction_13: float | None = ...,
        moisture_content_13: float | None = ...,
        relative_humidity_fraction_14: float | None = ...,
        moisture_content_14: float | None = ...,
        relative_humidity_fraction_15: float | None = ...,
        moisture_content_15: float | None = ...,
        relative_humidity_fraction_16: float | None = ...,
        moisture_content_16: float | None = ...,
        relative_humidity_fraction_17: float | None = ...,
        moisture_content_17: float | None = ...,
        relative_humidity_fraction_18: float | None = ...,
        moisture_content_18: float | None = ...,
        relative_humidity_fraction_19: float | None = ...,
        moisture_content_19: float | None = ...,
        relative_humidity_fraction_20: float | None = ...,
        moisture_content_20: float | None = ...,
        relative_humidity_fraction_21: float | None = ...,
        moisture_content_21: float | None = ...,
        relative_humidity_fraction_22: float | None = ...,
        moisture_content_22: float | None = ...,
        relative_humidity_fraction_23: float | None = ...,
        moisture_content_23: float | None = ...,
        relative_humidity_fraction_24: float | None = ...,
        moisture_content_24: float | None = ...,
        relative_humidity_fraction_25: float | None = ...,
        moisture_content_25: float | None = ...,
    ) -> None:
        """Create a new ``MaterialProperty:HeatAndMoistureTransfer:SorptionIsotherm`` and add it to the document.

        HeatBalanceAlgorithm = CombinedHeatAndMoistureFiniteElement solution algorithm only. Relationship between moisture content and relative humidity fraction. Has no effect with other HeatBalanceAlgorithm solution algorithms

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertyheatandmoisturetransfersorptionisotherm
        """

class GroundHeatTransferBasementAutoGrid:
    def __call__(
        self,
        /,
        *,
        slabx_x_dimension_of_the_building_slab: float,
        slaby_y_dimension_of_the_building_slab: float,
        clearance_distance_from_outside_of_wall_to_edge_: float | None = 15,
        concagheight_height_of_the_foundation_wall_above_grade: float | None = 0,
        slabdepth_thickness_of_the_floor_slab: float | None = 0.1,
        basedepth_depth_of_the_basement_wall_below_grade: float | None = 2,
    ) -> None:
        """Create a new ``GroundHeatTransfer:Basement:AutoGrid`` and add it to the document.

        AutoGrid only necessary when EquivSizing is false If the modeled building is not a rectangle or square, Equivalent sizing MUST be used to get accurate results

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferbasementautogrid
        """

class OtherEquipmentInstance:
    def __call__(
        self,
        name: str,
        /,
        *,
        other_equipment_definition_name: str,
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
        multiplier: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``OtherEquipment:Instance`` and add it to the document.

        Sets internal gains or losses for 'other' equipment in the zone. The physical characteristics are given by the referenced OtherEquipment:Definition object. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains/#otherequipmentinstance
        """

class IndoorLivingWall:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_name: str,
        schedule_name: str,
        evapotranspiration_calculation_method: Literal["", "Penman-Monteith", "Stanghellini"]
        | None = "Penman-Monteith",
        lighting_method: Literal["Daylight", "LED", "LED-Daylight"] | None = ...,
        led_intensity_schedule_name: str | None = ...,
        daylighting_control_name: str | None = ...,
        led_daylight_targeted_lighting_intensity_schedule_name: str | None = ...,
        total_leaf_area: float | None = ...,
        led_nominal_intensity: float | None = ...,
        led_nominal_power: float | None = ...,
        radiant_fraction_of_led_lights: float | None = 0.6,
    ) -> None:
        """Create a new ``IndoorLivingWall`` and add it to the document.

        Indoor greenery systems such as indoor living walls are panels of plants, which grow hydroponically or from substrates. The living wall structures can be either free-standing or attached to walls. The IndoorLivingWall module directly connects with inside surface heat balance, zone air heat balance, and zone air moisture balance.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#indoorlivingwall
        """

class AnyWaterHeaterStratified:
    def __call__(
        self,
        name: str,
        /,
        *,
        tank_volume: float | Literal["Autosize"],
        tank_height: float | Literal["Autosize"],
        heater_1_setpoint_temperature_schedule_name: str,
        heater_2_setpoint_temperature_schedule_name: str,
        heater_fuel_type: Literal[
            "Coal", "Diesel", "Electricity", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2"
        ],
        heater_thermal_efficiency: float,
        ambient_temperature_indicator: Literal["Outdoors", "Schedule", "Zone"],
        end_use_subcategory: str | None = "General",
        tank_shape: Literal["", "HorizontalCylinder", "Other", "VerticalCylinder"] | None = "VerticalCylinder",
        tank_perimeter: float | None = ...,
        maximum_temperature_limit: float | None = ...,
        heater_priority_control: Literal["", "MasterSlave", "Simultaneous"] | None = "MasterSlave",
        heater_1_deadband_temperature_difference: float | None = 0,
        heater_1_capacity: float | Literal["Autosize"] | None = ...,
        heater_1_height: float | None = ...,
        heater_2_deadband_temperature_difference: float | None = 0,
        heater_2_capacity: float | None = ...,
        heater_2_height: float | None = ...,
        off_cycle_parasitic_fuel_consumption_rate: float | None = 0,
        off_cycle_parasitic_fuel_type: Literal[
            "Coal", "Diesel", "Electricity", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2"
        ]
        | None = ...,
        off_cycle_parasitic_heat_fraction_to_tank: float | None = 0,
        off_cycle_parasitic_height: float | None = 0,
        on_cycle_parasitic_fuel_consumption_rate: float | None = 0,
        on_cycle_parasitic_fuel_type: Literal[
            "Coal", "Diesel", "Electricity", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2"
        ]
        | None = ...,
        on_cycle_parasitic_heat_fraction_to_tank: float | None = 0,
        on_cycle_parasitic_height: float | None = 0,
        ambient_temperature_schedule_name: str | None = ...,
        ambient_temperature_zone_name: str | None = ...,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        uniform_skin_loss_coefficient_per_unit_area_to_ambient_temperature: float | None = ...,
        skin_loss_fraction_to_zone: float | None = 1,
        off_cycle_flue_loss_coefficient_to_ambient_temperature: float | None = ...,
        off_cycle_flue_loss_fraction_to_zone: float | None = 1,
        peak_use_flow_rate: float | None = ...,
        use_flow_rate_fraction_schedule_name: str | None = ...,
        cold_water_supply_temperature_schedule_name: str | None = ...,
        use_side_inlet_node_name: str | None = ...,
        use_side_outlet_node_name: str | None = ...,
        use_side_effectiveness: float | None = 1,
        use_side_inlet_height: float | None = 0,
        use_side_outlet_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        source_side_inlet_node_name: str | None = ...,
        source_side_outlet_node_name: str | None = ...,
        source_side_effectiveness: float | None = 1,
        source_side_inlet_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        source_side_outlet_height: float | None = 0,
        inlet_mode: Literal["", "Fixed", "Seeking"] | None = "Fixed",
        use_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        source_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        indirect_water_heating_recovery_time: float | None = 1.5,
        number_of_nodes: int | None = 1,
        additional_destratification_conductivity: float | None = 0,
        node_1_additional_loss_coefficient: float | None = 0,
        node_2_additional_loss_coefficient: float | None = 0,
        node_3_additional_loss_coefficient: float | None = 0,
        node_4_additional_loss_coefficient: float | None = 0,
        node_5_additional_loss_coefficient: float | None = 0,
        node_6_additional_loss_coefficient: float | None = 0,
        node_7_additional_loss_coefficient: float | None = 0,
        node_8_additional_loss_coefficient: float | None = 0,
        node_9_additional_loss_coefficient: float | None = 0,
        node_10_additional_loss_coefficient: float | None = 0,
        node_11_additional_loss_coefficient: float | None = 0,
        node_12_additional_loss_coefficient: float | None = 0,
        source_side_flow_control_mode: Literal[
            "", "IndirectHeatAlternateSetpoint", "IndirectHeatPrimarySetpoint", "StorageTank"
        ]
        | None = "IndirectHeatPrimarySetpoint",
        indirect_alternate_setpoint_temperature_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``WaterHeater:Stratified`` and add it to the document.

        Water heater with stratified, multi-node water tank. May be used to model a tankless water heater (small tank volume), a hot water storage tank (zero heater capacity), or a heat pump water heater (see WaterHeater:HeatPump:*.)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-heaters/#waterheaterstratified
        """

class AvailabilityManagerScheduled:
    def __call__(self, name: str, /, *, schedule_name: str) -> None:
        """Create a new ``AvailabilityManager:Scheduled`` and add it to the document.

        Determines the availability of a loop or system: whether it is on or off. Schedule overrides fan/pump schedule.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-system-availability-managers/#availabilitymanagerscheduled
        """

class ElectricLoadCenterInverterSimple:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        radiative_fraction: float | None = ...,
        inverter_efficiency: float | None = ...,
    ) -> None:
        """Create a new ``ElectricLoadCenter:Inverter:Simple`` and add it to the document.

        Electric power inverter to convert from direct current (DC) to alternating current (AC) in an electric load center that contains photovoltaic modules. This input object is for the simplest inverter model and uses a fixed efficiency.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#electricloadcenterinvertersimple
        """

class AnyOutputControlSurfaceColorScheme:
    def __call__(
        self,
        name: str,
        /,
        *,
        drawing_element_1_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_1: int | None = ...,
        drawing_element_2_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_2: int | None = ...,
        drawing_element_3_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_3: int | None = ...,
        drawing_element_4_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_4: int | None = ...,
        drawing_element_5_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_5: int | None = ...,
        drawing_element_6_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_6: int | None = ...,
        drawing_element_7_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_7: int | None = ...,
        drawing_element_8_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_8: int | None = ...,
        drawing_element_9_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_9: int | None = ...,
        drawing_element_10_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_10: int | None = ...,
        drawing_element_11_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_11: int | None = ...,
        drawing_element_12_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_12: int | None = ...,
        drawing_element_13_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_13: int | None = ...,
        drawing_element_14_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_14: int | None = ...,
        drawing_element_15_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_15: int | None = ...,
    ) -> None:
        """Create a new ``OutputControl:SurfaceColorScheme`` and add it to the document.

        This object is used to set colors for reporting on various building elements particularly for the DXF reports. We know the user can enter 0 to 255 and the color map is available in DXF output. Therefore, we are limiting the colors in that range. You can extend by editing the IDD but you do so on your own. Colors not changed in any scheme will remain as the default scheme uses.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#outputcontrolsurfacecolorscheme
        """
