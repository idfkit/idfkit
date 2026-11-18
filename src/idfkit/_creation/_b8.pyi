"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class WindowMaterialShade:
    def __call__(
        self,
        name: str,
        /,
        *,
        solar_transmittance: float,
        solar_reflectance: float,
        visible_transmittance: float,
        visible_reflectance: float,
        infrared_hemispherical_emissivity: float,
        infrared_transmittance: float,
        thickness: float,
        conductivity: float,
        shade_to_glass_distance: float | None = 0.05,
        top_opening_multiplier: float | None = 0.5,
        bottom_opening_multiplier: float | None = 0.5,
        left_side_opening_multiplier: float | None = 0.5,
        right_side_opening_multiplier: float | None = 0.5,
        airflow_permeability: float | None = 0,
    ) -> None:
        """Create a new ``WindowMaterial:Shade`` and add it to the document.

        Specifies the properties of window shade materials. Reflectance and emissivity properties are assumed to be the same on both sides of the shade. Shades are considered to be perfect diffusers (all transmitted and reflected radiation is hemispherically-diffuse) independent of angle of incidence.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialshade
        """

class MaterialPropertyGlazingSpectralData:
    def __call__(
        self,
        name: str,
        /,
        *,
        wavelength_1: float | None = ...,
        transmittance_1: float | None = ...,
        front_reflectance_1: float | None = ...,
        back_reflectance_1: float | None = ...,
        wavelength_2: float | None = ...,
        transmittance_2: float | None = ...,
        front_reflectance_2: float | None = ...,
        back_reflectance_2: float | None = ...,
        wavelength_3: float | None = ...,
        transmittance_3: float | None = ...,
        front_reflectance_3: float | None = ...,
        back_reflectance_3: float | None = ...,
        wavelength_4: float | None = ...,
        transmittance_4: float | None = ...,
        front_reflectance_4: float | None = ...,
        back_reflectance_4: float | None = ...,
        extensions: Sequence[
            _g.MaterialPropertyGlazingSpectralDataExtensionsItem | _g.MaterialPropertyGlazingSpectralDataExtensionsGroup
        ] = ...,
    ) -> None:
        """Create a new ``MaterialProperty:GlazingSpectralData`` and add it to the document.

        Name is followed by up to 800 sets of normal-incidence measured values of [wavelength, transmittance, front reflectance, back reflectance] for wavelengths covering the solar spectrum (from about 0.25 to 2.5 microns)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertyglazingspectraldata
        """

class AnySpace:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        floor_area: float | Literal["Autocalculate"] | None = "Autocalculate",
        space_type: str | None = "General",
        tags: Sequence[_g.SpaceTagsItem | _g.SpaceTagsGroup] = ...,
    ) -> None:
        """Create a new ``Space`` and add it to the document.

        Defines a space (room) in the building. All Spaces are part of a Zone. Every Zone contains one or more spaces. Space is an optional input. If a Zone has no Space(s) specified in input then a default Space named <Zone Name> will be created. If some surfaces in a Zone are assigned to a space and some are not, then a default Space named <Zone Name>-Remainder will be created. Input references to Space Names must have a matching Space object (default space names may not be referenced except in output variable keys).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#space
        """

class ShadingBuildingDetailed:
    def __call__(
        self,
        name: str,
        /,
        *,
        transmittance_schedule_name: str | None = ...,
        number_of_vertices: float | Literal["Autocalculate"] | None = "Autocalculate",
        vertices: Sequence[_g.ShadingBuildingDetailedVerticesItem | _g.ShadingBuildingDetailedVerticesGroup] = ...,
    ) -> None:
        """Create a new ``Shading:Building:Detailed`` and add it to the document.

        used for shading elements such as trees, other buildings, parts of this building not being modeled these items are relative to the current building and would move with relative geometry

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zones-and-surfaces/#shadingbuildingdetailed
        """

class AnyElectricEquipmentITEAirCooled:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        cpu_power_input_function_of_loading_and_air_temperature_curve_name: str,
        design_fan_air_flow_rate_per_power_input: float,
        air_flow_function_of_loading_and_air_temperature_curve_name: str,
        fan_power_input_function_of_flow_curve_name: str,
        air_flow_calculation_method: Literal["FlowControlWithApproachTemperatures", "FlowFromSystem"]
        | None = "FlowFromSystem",
        design_power_input_calculation_method: Literal["Watts/Area", "Watts/Unit"] | None = "Watts/Unit",
        watts_per_unit: float | None = ...,
        number_of_units: float | None = 1,
        design_power_input_schedule_name: str | None = ...,
        cpu_loading_schedule_name: str | None = ...,
        design_fan_power_input_fraction: float | None = 0,
        design_entering_air_temperature: float | None = 15,
        environmental_class: Literal["A1", "A2", "A3", "A4", "B", "C", "None"] | None = "None",
        air_inlet_connection_type: Literal["AdjustedSupply", "RoomAirModel", "ZoneAirNode"] | None = "AdjustedSupply",
        air_inlet_room_air_model_node_name: str | None = ...,
        air_outlet_room_air_model_node_name: str | None = ...,
        supply_air_node_name: str | None = ...,
        design_recirculation_fraction: float | None = 0,
        recirculation_function_of_loading_and_supply_temperature_curve_name: str | None = ...,
        design_electric_power_supply_efficiency: float | None = 1,
        electric_power_supply_efficiency_function_of_part_load_ratio_curve_name: str | None = ...,
        fraction_of_electric_power_supply_losses_to_zone: float | None = 1,
        cpu_end_use_subcategory: str | None = "ITE-CPU",
        fan_end_use_subcategory: str | None = "ITE-Fans",
        electric_power_supply_end_use_subcategory: str | None = "ITE-UPS",
        supply_temperature_difference: float | None = ...,
        supply_temperature_difference_schedule: str | None = ...,
        return_temperature_difference: float | None = ...,
        return_temperature_difference_schedule: str | None = ...,
    ) -> None:
        """Create a new ``ElectricEquipment:ITE:AirCooled`` and add it to the document.

        This object describes air-cooled electric information technology equipment (ITE) which has variable power consumption as a function of loading and temperature. If a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#electricequipmentiteaircooled
        """

class ZoneThermalChimney:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        width_of_the_absorber_wall: float,
        cross_sectional_area_of_air_channel_outlet: float,
        zone_or_space_name_1: str,
        distance_from_top_of_thermal_chimney_to_inlet_1: float,
        cross_sectional_areas_of_air_channel_inlet_1: float,
        availability_schedule_name: str | None = ...,
        discharge_coefficient: float | None = 0.8,
        relative_ratios_of_air_flow_rates_passing_through_inlet_1: float | None = 1,
        zone_or_space_name_2: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_2: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_inlet_2: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_2: float | None = ...,
        zone_or_space_name_3: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_3: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_inlet_3: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_3: float | None = ...,
        zone_or_space_name_4: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_4: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_inlet_4: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_4: float | None = ...,
        zone_or_space_name_5: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_5: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_inlet_5: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_5: float | None = ...,
        zone_or_space_name_6: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_6: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_inlet_6: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_6: float | None = ...,
        zone_or_space_name_7: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_7: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_inlet_7: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_7: float | None = ...,
        zone_or_space_name_8: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_8: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_inlet_8: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_8: float | None = ...,
        zone_or_space_name_9: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_9: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_inlet_9: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_9: float | None = ...,
        zone_or_space_name_10: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_10: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_inlet_10: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_10: float | None = ...,
        zone_or_space_name_11: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_11: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_inlet_11: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_11: float | None = ...,
        zone_or_space_name_12: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_12: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_inlet_12: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_12: float | None = ...,
        zone_or_space_name_13: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_13: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_inlet_13: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_13: float | None = ...,
        zone_or_space_name_14: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_14: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_inlet_14: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_14: float | None = ...,
        zone_or_space_name_15: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_15: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_inlet_15: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_15: float | None = ...,
        zone_or_space_name_16: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_16: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_inlet_16: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_16: float | None = ...,
        zone_or_space_name_17: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_17: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_inlet_17: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_17: float | None = ...,
        zone_or_space_name_18: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_18: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_inlet_18: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_18: float | None = ...,
        zone_or_space_name_19: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_19: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_inlet_19: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_19: float | None = ...,
        zone_or_space_name_20: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_20: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_inlet_20: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_20: float | None = ...,
    ) -> None:
        """Create a new ``ZoneThermalChimney`` and add it to the document.

        A thermal chimney is a vertical shaft utilizing solar radiation to enhance natural ventilation. It consists of an absorber wall, air gap and glass cover with high solar transmissivity.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zonethermalchimney
        """

class CoilHeatingElectricMultiStage:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        number_of_stages: int,
        stage_1_efficiency: float,
        stage_1_nominal_capacity: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        temperature_setpoint_node_name: str | None = ...,
        stage_2_efficiency: float | None = ...,
        stage_2_nominal_capacity: float | Literal["Autosize"] | None = ...,
        stage_3_efficiency: float | None = ...,
        stage_3_nominal_capacity: float | Literal["Autosize"] | None = ...,
        stage_4_efficiency: float | None = ...,
        stage_4_nominal_capacity: float | Literal["Autosize"] | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:Electric:MultiStage`` and add it to the document.

        Electric heating coil, multi-stage. If the coil is located directly in an air loop branch or outdoor air equipment list, then it is controlled on leaving air temperature and the Temperature Setpoint Node Name must be specified. If the coil is contained within another component such as an air terminal unit, zone HVAC equipment, or unitary system, then the coil is controlled by the parent component and the setpoint node name is not entered.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilheatingelectricmultistage
        """

class AnyCoilWaterHeatingDesuperheater:
    def __call__(
        self,
        name: str,
        /,
        *,
        setpoint_temperature_schedule_name: str,
        rated_inlet_water_temperature: float,
        rated_outdoor_air_temperature: float,
        maximum_inlet_water_temperature_for_heat_reclaim: float,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        tank_name: str,
        heating_source_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:TwoSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
            "Refrigeration:CompressorRack",
            "Refrigeration:Condenser:AirCooled",
            "Refrigeration:Condenser:EvaporativeCooled",
            "Refrigeration:Condenser:WaterCooled",
        ],
        heating_source_name: str,
        water_flow_rate: float,
        availability_schedule_name: str | None = ...,
        dead_band_temperature_difference: float | None = 5,
        rated_heat_reclaim_recovery_efficiency: float | None = ...,
        heat_reclaim_efficiency_function_of_temperature_curve_name: str | None = ...,
        tank_object_type: Literal["WaterHeater:Mixed"] | None = "WaterHeater:Mixed",
        water_pump_power: float | None = 0,
        fraction_of_pump_heat_to_water: float | None = 0.2,
        on_cycle_parasitic_electric_load: float | None = 0,
        off_cycle_parasitic_electric_load: float | None = 0,
    ) -> None:
        """Create a new ``Coil:WaterHeating:Desuperheater`` and add it to the document.

        Desuperheater air heating coil. The heating energy provided by this coil is reclaimed from the superheated refrigerant gas leaving a compressor and does not impact the performance of the compressor. This coil must be used with a water heater tank, see Water Heater:Mixed.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilwaterheatingdesuperheater
        """

class AnyAirLoopHVACUnitaryHeatCoolVAVChangeoverBypass:
    def __call__(
        self,
        name: str,
        /,
        *,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        cooling_outdoor_air_flow_rate: float | Literal["Autosize"],
        heating_outdoor_air_flow_rate: float | Literal["Autosize"],
        air_inlet_node_name: str,
        bypass_duct_mixer_node_name: str,
        bypass_duct_splitter_node_name: str,
        air_outlet_node_name: str,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"],
        outdoor_air_mixer_name: str,
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel"],
        supply_air_fan_name: str,
        supply_air_fan_placement: Literal["BlowThrough", "DrawThrough"],
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:DX:SingleSpeed",
            "Coil:Heating:DX:VariableSpeed",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
        ],
        heating_coil_name: str,
        availability_schedule_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        outdoor_air_flow_rate_multiplier_schedule_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        priority_control_mode: Literal["CoolingPriority", "HeatingPriority", "ZonePriority"] | None = "ZonePriority",
        minimum_outlet_air_temperature_during_cooling_operation: float | None = 8,
        maximum_outlet_air_temperature_during_heating_operation: float | None = 50,
        dehumidification_control_type: Literal["CoolReheat", "Multimode", "None"] | None = "None",
    ) -> None:
        """Create a new ``AirLoopHVAC:UnitaryHeatCool:VAVChangeoverBypass`` and add it to the document.

        Unitary system, heating and cooling with constant volume supply fan (continuous or cycling), direct expansion (DX) cooling coil, heating coil (gas, electric, hot water, steam, or DX air-to-air heat pump) and bypass damper for variable volume flow to terminal units. Used with AirTerminal:SingleDuct:VAV:HeatAndCool:Reheat or AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#airloophvacunitaryheatcoolvavchangeoverbypass
        """

class EnergyManagementSystemCurveOrTableIndexVariable:
    def __call__(self, name: str, /, *, curve_or_table_object_name: str) -> None:
        """Create a new ``EnergyManagementSystem:CurveOrTableIndexVariable`` and add it to the document.

        Declares EMS variable that identifies a curve or table

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemcurveortableindexvariable
        """
