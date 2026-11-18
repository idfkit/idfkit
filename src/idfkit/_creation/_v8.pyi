"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Any, Literal

from .. import versioned as _vd

class GroundHeatExchangerVerticalArray_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        ghe_vertical_properties_object_name: str,
        number_of_boreholes_in_x_direction: float,
        number_of_boreholes_in_y_direction: float,
        borehole_spacing: float,
    ) -> None:
        """Create a new ``GroundHeatExchanger:Vertical:Array`` and add it to the document.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-condenser-equipment/#groundheatexchangerverticalarray
        """

class CeilingAdiabatic_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 0,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        width: float | None = ...,
    ) -> None:
        """Create a new ``Ceiling:Adiabatic`` and add it to the document.

        Allows for simplified entry of interior ceilings.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-thermal-zone-description-geometry/#ceilingadiabatic
        """

class ChillerEngineDriven_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        nominal_capacity: float | Literal["Autosize"],
        nominal_cop: float,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        temperature_rise_coefficient: float,
        fuel_type: Literal[
            "Diesel", "FuelOil#1", "FuelOil#2", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2", "PropaneGas"
        ],
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        design_condenser_inlet_temperature: float | None = ...,
        design_chilled_water_outlet_temperature: float | None = ...,
        design_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_condenser_water_flow_rate: float | Literal["Autosize"] | None = ...,
        coefficient_1_of_capacity_ratio_curve: float | None = ...,
        coefficient_2_of_capacity_ratio_curve: float | None = ...,
        coefficient_3_of_capacity_ratio_curve: float | None = ...,
        coefficient_1_of_power_ratio_curve: float | None = ...,
        coefficient_2_of_power_ratio_curve: float | None = ...,
        coefficient_3_of_power_ratio_curve: float | None = ...,
        coefficient_1_of_full_load_ratio_curve: float | None = ...,
        coefficient_2_of_full_load_ratio_curve: float | None = ...,
        coefficient_3_of_full_load_ratio_curve: float | None = ...,
        chilled_water_outlet_temperature_lower_limit: float | None = ...,
        fuel_use_curve_name: str | None = ...,
        jacket_heat_recovery_curve_name: str | None = ...,
        lube_heat_recovery_curve_name: str | None = ...,
        total_exhaust_energy_curve_name: str | None = ...,
        exhaust_temperature_curve_name: str | None = ...,
        coefficient_1_of_u_factor_times_area_curve: float | None = ...,
        coefficient_2_of_u_factor_times_area_curve: float | None = ...,
        maximum_exhaust_flow_per_unit_of_power_output: float | None = ...,
        design_minimum_exhaust_temperature: float | None = ...,
        fuel_higher_heating_value: float | None = ...,
        design_heat_recovery_water_flow_rate: float | Literal["", "Autosize"] | None = 0,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        chiller_flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"]
        | None = "NotModulated",
        maximum_temperature_for_heat_recovery_at_heat_recovery_outlet_node: float | None = 60,
        sizing_factor: float | None = 1,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        condenser_heat_recovery_relative_capacity_fraction: float | None = ...,
    ) -> None:
        """Create a new ``Chiller:EngineDriven`` and add it to the document.

        This chiller model is the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Chiller performance curves are generated by fitting catalog data to third order polynomial equations. Three sets of coefficients are required.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-plant-equipment/#chillerenginedriven
        """

class OutputTableTimeBins_v8_9_to_v22_1:
    def __call__(
        self,
        /,
        *,
        variable_name: str,
        key_value: str | None = "*",
        interval_start: float | None = ...,
        interval_size: float | None = ...,
        interval_count: float | None = ...,
        schedule_name: str | None = ...,
        variable_type: Literal["Energy", "Power", "Temperature", "VolumetricFlow"] | None = ...,
    ) -> None:
        """Create a new ``Output:Table:TimeBins`` and add it to the document.

        Produces a bin report in the table output file which shows the amount of time in hours that occurs in different bins for a single specific output variable or meter. Two different types of binning are reported: by month and by hour of the day.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/standard-output-reports/output-table-timebins/#outputtabletimebins
        """

class CoilHeatingWaterToAirHeatPumpEquationFit_v23_2_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        rated_air_flow_rate: float | Literal["Autosize"],
        rated_water_flow_rate: float | Literal["Autosize"],
        gross_rated_heating_capacity: float | Literal["Autosize"],
        gross_rated_heating_cop: float,
        heating_capacity_curve_name: str,
        heating_power_consumption_curve_name: str,
        part_load_fraction_correlation_curve_name: str,
        rated_entering_water_temperature: float | None = 20,
        rated_entering_air_dry_bulb_temperature: float | None = 20,
        ratio_of_rated_heating_capacity_to_rated_cooling_capacity: float | None = 1,
    ) -> None:
        """Create a new ``Coil:Heating:WaterToAirHeatPump:EquationFit`` and add it to the document.

        Direct expansion (DX) heating coil for water-to-air heat pump (includes electric compressor), single-speed, equation-fit model. Equation-fit model uses normalized curves to describe the heat pump performance.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-heating-and-cooling-coils/#coilheatingwatertoairheatpumpequationfit
        """

class People_v8_9_to_v9_4:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_name: str,
        number_of_people_schedule_name: str,
        activity_level_schedule_name: str,
        number_of_people_calculation_method: Literal["", "Area/Person", "People", "People/Area"] | None = "People",
        number_of_people: float | None = ...,
        people_per_zone_floor_area: float | None = ...,
        zone_floor_area_per_person: float | None = ...,
        fraction_radiant: float | None = 0.3,
        sensible_heat_fraction: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        carbon_dioxide_generation_rate: float | None = ...,
        enable_ashrae_55_comfort_warnings: Literal["", "No", "Yes"] | None = "No",
        mean_radiant_temperature_calculation_type: Literal["", "AngleFactor", "SurfaceWeighted", "ZoneAveraged"]
        | None = "ZoneAveraged",
        surface_name_angle_factor_list_name: str | None = ...,
        work_efficiency_schedule_name: str | None = ...,
        clothing_insulation_calculation_method: Literal[
            "", "CalculationMethodSchedule", "ClothingInsulationSchedule", "DynamicClothingModelASHRAE55"
        ]
        | None = "ClothingInsulationSchedule",
        clothing_insulation_calculation_method_schedule_name: str | None = ...,
        clothing_insulation_schedule_name: str | None = ...,
        air_velocity_schedule_name: str | None = ...,
        thermal_comfort_model_1_type: Literal["AdaptiveASH55", "AdaptiveCEN15251", "Fanger", "KSU", "Pierce"]
        | None = ...,
        thermal_comfort_model_2_type: Literal["AdaptiveASH55", "AdaptiveCEN15251", "Fanger", "KSU", "Pierce"]
        | None = ...,
        thermal_comfort_model_3_type: Literal["AdaptiveASH55", "AdaptiveCEN15251", "Fanger", "KSU", "Pierce"]
        | None = ...,
        thermal_comfort_model_4_type: Literal["AdaptiveASH55", "AdaptiveCEN15251", "Fanger", "KSU", "Pierce"]
        | None = ...,
        thermal_comfort_model_5_type: Literal["AdaptiveASH55", "AdaptiveCEN15251", "Fanger", "KSU", "Pierce"]
        | None = ...,
    ) -> None:
        """Create a new ``People`` and add it to the document.

        Sets internal gains and contaminant rates for occupants in the zone. If you use a ZoneList in the Zone or ZoneList name field then this definition applies to all the zones in the ZoneList.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-internal-gains-people-lights-other/#people
        """

class ZonePropertyUserViewFactorsbySurfaceName_v9_2_to_v9_3:
    def __call__(
        self,
        /,
        *,
        zone_or_zonelist_name: str | None = ...,
        view_factors: list[_vd.ZonePropertyUserViewFactorsbySurfaceNameViewFactorsItem_v9_2_to_v9_3] = ...,
    ) -> None:
        """Create a new ``ZoneProperty:UserViewFactors:bySurfaceName`` and add it to the document.

        View factors for Surface to Surface in a zone. (Number of Surfaces)**2 are expected. Any omitted surface pairs will be assumed to have a view factor of zero.
        """

class HeaderedPumpsConstantSpeed_v8_9_to_v9_0:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        total_design_flow_rate: float | Literal["Autosize"] | None = ...,
        number_of_pumps_in_bank: float | None = ...,
        flow_sequencing_control_scheme: Literal["", "Sequential"] | None = "Sequential",
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        pump_control_type: Literal["", "Continuous", "Intermittent"] | None = "Continuous",
        pump_flow_rate_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["", "PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
    ) -> None:
        """Create a new ``HeaderedPumps:ConstantSpeed`` and add it to the document.

        This Headered pump object describes a pump bank with more than 1 pump in parallel

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.0/io-reference/overview/group-pumps/#headeredpumpsconstantspeed
        """

class OutputControlSurfaceColorScheme_v8_9_to_v22_1:
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
        color_for_drawing_element_1: float | None = ...,
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
        color_for_drawing_element_2: float | None = ...,
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
        color_for_drawing_element_3: float | None = ...,
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
        color_for_drawing_element_4: float | None = ...,
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
        color_for_drawing_element_5: float | None = ...,
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
        color_for_drawing_element_6: float | None = ...,
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
        color_for_drawing_element_7: float | None = ...,
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
        color_for_drawing_element_8: float | None = ...,
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
        color_for_drawing_element_9: float | None = ...,
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
        color_for_drawing_element_10: float | None = ...,
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
        color_for_drawing_element_11: float | None = ...,
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
        color_for_drawing_element_12: float | None = ...,
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
        color_for_drawing_element_13: float | None = ...,
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
        color_for_drawing_element_14: float | None = ...,
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
        color_for_drawing_element_15: float | None = ...,
    ) -> None:
        """Create a new ``OutputControl:SurfaceColorScheme`` and add it to the document.

        This object is used to set colors for reporting on various building elements particularly for the DXF reports. We know the user can enter 0 to 255 and the color map is available in DXF output. Therefore, we are limiting the colors in that range. You can extend by editing the IDD but you do so on your own. Colors not changed in any scheme will remain as the default scheme uses.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/input-for-output/#outputcontrolsurfacecolorscheme
        """

class ChillerElectricEIR_v8_9_to_v24_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_capacity: float | Literal["Autosize"],
        reference_cop: float,
        cooling_capacity_function_of_temperature_curve_name: str,
        electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str,
        electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        reference_leaving_chilled_water_temperature: float | None = 6.67,
        reference_entering_condenser_fluid_temperature: float | None = 29.4,
        reference_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        reference_condenser_fluid_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_part_load_ratio: float | None = 0.1,
        maximum_part_load_ratio: float | None = 1,
        optimum_part_load_ratio: float | None = 1,
        minimum_unloading_ratio: float | None = 0.2,
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "WaterCooled",
        condenser_fan_power_ratio: float | None = 0,
        fraction_of_compressor_electric_consumption_rejected_by_condenser: float | None = 1,
        leaving_chilled_water_lower_temperature_limit: float | None = 2,
        chiller_flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"]
        | None = "NotModulated",
        design_heat_recovery_water_flow_rate: float | Literal["", "Autosize"] | None = 0,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        sizing_factor: float | None = 1,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        condenser_heat_recovery_relative_capacity_fraction: float | None = ...,
        heat_recovery_inlet_high_temperature_limit_schedule_name: str | None = ...,
        heat_recovery_leaving_temperature_setpoint_node_name: str | None = ...,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``Chiller:Electric:EIR`` and add it to the document.

        This chiller model is the empirical model from the DOE-2 building Energy simulation program. Chiller performance at off-reference conditions is modeled using three polynomial equations. Three curves objects are required.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.1/io-reference/overview/group-plant-equipment/#chillerelectriceir
        """

class ZoneMixing_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        schedule_name: str,
        source_zone_name: str,
        design_flow_rate_calculation_method: Literal["", "AirChanges/Hour", "Flow/Area", "Flow/Person", "Flow/Zone"]
        | None = "Flow/Zone",
        design_flow_rate: float | None = ...,
        flow_rate_per_zone_floor_area: float | None = ...,
        flow_rate_per_person: float | None = ...,
        air_changes_per_hour: float | None = ...,
        delta_temperature: float | None = 0,
        delta_temperature_schedule_name: str | None = ...,
        minimum_zone_temperature_schedule_name: str | None = ...,
        maximum_zone_temperature_schedule_name: str | None = ...,
        minimum_source_zone_temperature_schedule_name: str | None = ...,
        maximum_source_zone_temperature_schedule_name: str | None = ...,
        minimum_outdoor_temperature_schedule_name: str | None = ...,
        maximum_outdoor_temperature_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneMixing`` and add it to the document.

        ZoneMixing is a simple air exchange from one zone to another. Note that this statement only affects the energy balance of the 'receiving' zone and will not produce any effect on the 'source' zone. Mixing statements can be complementary and include multiple zones, but the balancing of flows between zones is left to the user's discretion.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-airflow/#zonemixing
        """

class ZoneEarthtube_v8_9_to_v23_1:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        schedule_name: str,
        design_flow_rate: float,
        minimum_zone_temperature_when_cooling: float,
        maximum_zone_temperature_when_heating: float,
        delta_temperature: float,
        average_soil_surface_temperature: float,
        amplitude_of_soil_surface_temperature: float,
        phase_constant_of_soil_surface_temperature: float,
        earthtube_type: Literal["", "Exhaust", "Intake", "Natural"] | None = "Natural",
        fan_pressure_rise: float | None = 0,
        fan_total_efficiency: float | None = 1,
        pipe_radius: float | None = 1,
        pipe_thickness: float | None = 0.2,
        pipe_length: float | None = 15,
        pipe_thermal_conductivity: float | None = 200,
        pipe_depth_under_ground_surface: float | None = 3,
        soil_condition: Literal["", "HeavyAndDamp", "HeavyAndDry", "HeavyAndSaturated", "LightAndDry"]
        | None = "HeavyAndDamp",
        constant_term_flow_coefficient: float | None = 1,
        temperature_term_flow_coefficient: float | None = 0,
        velocity_term_flow_coefficient: float | None = 0,
        velocity_squared_term_flow_coefficient: float | None = 0,
    ) -> None:
        """Create a new ``ZoneEarthtube`` and add it to the document.

        Earth Tube is specified as a design level which is modified by a Schedule fraction, temperature difference and wind speed: Earthtube=Edesign * Fschedule * (A + B*|(Tzone-Todb)| + C*WindSpd + D * WindSpd**2)

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-airflow/#zoneearthtube
        """

class TableTwoIndependentVariables_v8_9_to_v9_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        curve_type: Literal["BiQuadratic", "QuadraticLinear"],
        interpolation_method: Literal[
            "", "EvaluateCurveToLimits", "LagrangeInterpolationLinearExtrapolation", "LinearInterpolationOfTable"
        ]
        | None = "LagrangeInterpolationLinearExtrapolation",
        minimum_value_of_x: float | None = ...,
        maximum_value_of_x: float | None = ...,
        minimum_value_of_y: float | None = ...,
        maximum_value_of_y: float | None = ...,
        minimum_table_output: float | None = ...,
        maximum_table_output: float | None = ...,
        input_unit_type_for_x: Literal[
            "", "Angle", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        input_unit_type_for_y: Literal[
            "", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow", "Wavelength"
        ]
        | None = "Dimensionless",
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
        normalization_reference: float | None = ...,
        external_file_name: str | None = ...,
        values: list[_vd.TableTwoIndependentVariablesValuesItem_v8_9_to_v9_1] = ...,
    ) -> None:
        """Create a new ``Table:TwoIndependentVariables`` and add it to the document.

        Allows entry of tabular data pairs as alternate input for performance curve objects. Performance curve objects can be created using these inputs. BiQuadratic Table Equation: Output = a + bX + cX**2 + dY + eY**2 + fXY BiQuadratic solution requires a minimum of 6 data pairs QuadraticLinear Table Equation: Output = a + bX + cX**2 + dY + eXY + fX**2Y QuadraticLinear solution requires a minimum of 6 data pairs

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.
        """

class ComfortViewFactorAngles_v8_9_to_v9_5:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        zone_name: str | None = ...,
        surface_1_name: str | None = ...,
        angle_factor_1: float | None = ...,
        surface_2_name: str | None = ...,
        angle_factor_2: float | None = ...,
        surface_3_name: str | None = ...,
        angle_factor_3: float | None = ...,
        surface_4_name: str | None = ...,
        angle_factor_4: float | None = ...,
        surface_5_name: str | None = ...,
        angle_factor_5: float | None = ...,
        surface_6_name: str | None = ...,
        angle_factor_6: float | None = ...,
        surface_7_name: str | None = ...,
        angle_factor_7: float | None = ...,
        surface_8_name: str | None = ...,
        angle_factor_8: float | None = ...,
        surface_9_name: str | None = ...,
        angle_factor_9: float | None = ...,
        surface_10_name: str | None = ...,
        angle_factor_10: float | None = ...,
        surface_11_name: str | None = ...,
        angle_factor_11: float | None = ...,
        surface_12_name: str | None = ...,
        angle_factor_12: float | None = ...,
        surface_13_name: str | None = ...,
        angle_factor_13: float | None = ...,
        surface_14_name: str | None = ...,
        angle_factor_14: float | None = ...,
        surface_15_name: str | None = ...,
        angle_factor_15: float | None = ...,
        surface_16_name: str | None = ...,
        angle_factor_16: float | None = ...,
        surface_17_name: str | None = ...,
        angle_factor_17: float | None = ...,
        surface_18_name: str | None = ...,
        angle_factor_18: float | None = ...,
        surface_19_name: str | None = ...,
        angle_factor_19: float | None = ...,
        surface_20_name: str | None = ...,
        angle_factor_20: float | None = ...,
    ) -> None:
        """Create a new ``ComfortViewFactorAngles`` and add it to the document.

        Used to specify radiant view factors for thermal comfort calculations.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-internal-gains-people-lights-other/#comfortviewfactorangles
        """

class CoilWaterHeatingAirToWaterHeatPumpWrapped_v8_9_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_heating_capacity: float,
        evaporator_air_inlet_node_name: str,
        evaporator_air_outlet_node_name: str,
        rated_cop: float | None = 3.2,
        rated_sensible_heat_ratio: float | None = 0.85,
        rated_evaporator_inlet_air_dry_bulb_temperature: float | None = 19.7,
        rated_evaporator_inlet_air_wet_bulb_temperature: float | None = 13.5,
        rated_condenser_water_temperature: float | None = 57.5,
        rated_evaporator_air_flow_rate: float | Literal["Autocalculate"] | None = ...,
        evaporator_fan_power_included_in_rated_cop: Literal["", "No", "Yes"] | None = "Yes",
        crankcase_heater_capacity: float | None = 0,
        maximum_ambient_temperature_for_crankcase_heater_operation: float | None = 10,
        evaporator_air_temperature_type_for_curve_objects: Literal["", "DryBulbTemperature", "WetBulbTemperature"]
        | None = "WetBulbTemperature",
        heating_capacity_function_of_temperature_curve_name: str | None = ...,
        heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        heating_cop_function_of_temperature_curve_name: str | None = ...,
        heating_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:WaterHeating:AirToWaterHeatPump:Wrapped`` and add it to the document.

        Heat pump water heater (HPWH) heating coil, air-to-water direct-expansion (DX) system which includes a water heating coil, evaporator air coil, evaporator fan, electric compressor, and water pump. Part of a WaterHeater:HeatPump:WrappedCondenser system.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-heating-and-cooling-coils/#coilwaterheatingairtowaterheatpumpwrapped
        """

class PerformancePrecisionTradeoffs_v9_2:
    def __call__(self, /, *, use_coil_direct_solutions: Literal["", "No", "Yes"] | None = "No") -> None:
        """Create a new ``PerformancePrecisionTradeoffs`` and add it to the document.

        This object enables users to choose certain options that speed up EnergyPlus simulation, but may lead to small decreases in accuracy of results.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-simulation-parameters/#performanceprecisiontradeoffs
        """
