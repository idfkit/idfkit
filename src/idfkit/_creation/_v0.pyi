"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class OutputControlTableStyle_v24_1_to_v25_1:
    def __call__(
        self,
        /,
        *,
        column_separator: Literal[
            "", "All", "Comma", "CommaAndHTML", "CommaAndXML", "Fixed", "HTML", "Tab", "TabAndHTML", "XML", "XMLandHTML"
        ]
        | None = "Comma",
        unit_conversion: Literal["", "InchPound", "InchPoundExceptElectricity", "JtoGJ", "JtoKWH", "JtoMJ", "None"]
        | None = "None",
    ) -> None:
        """Create a new ``OutputControl:Table:Style`` and add it to the document.

        default style for the OutputControl:Table:Style is comma -- this works well for importing into spreadsheet programs such as Excel(tm) but not so well for word processing programs -- there tab may be a better choice. fixed puts spaces between the 'columns'. HTML produces tables in HTML. XML produces an XML file. note - if no OutputControl:Table:Style is included, the defaults are comma and None.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/standard-output-reports/outputcontrol-table-style/#outputcontroltablestyle
        """

class RunPeriodCustomRange_v8_9:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        begin_month: float,
        begin_day_of_month: float,
        begin_year: float,
        end_month: float,
        end_day_of_month: float,
        end_year: float,
        day_of_week_for_start_day: Literal[
            "", "Friday", "Monday", "Saturday", "Sunday", "Thursday", "Tuesday", "UseWeatherFile", "Wednesday"
        ]
        | None = "UseWeatherFile",
        use_weather_file_holidays_and_special_days: Literal["", "No", "Yes"] | None = "Yes",
        use_weather_file_daylight_saving_period: Literal["", "No", "Yes"] | None = "Yes",
        apply_weekend_holiday_rule: Literal["", "No", "Yes"] | None = "No",
        use_weather_file_rain_indicators: Literal["", "No", "Yes"] | None = "Yes",
        use_weather_file_snow_indicators: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``RunPeriod:CustomRange`` and add it to the document.

        run simulation for a custom created weather file

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.
        """

class FenestrationSurfaceDetailed_v9_0_to_v26_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_type: Literal["Door", "GlassDoor", "TubularDaylightDiffuser", "TubularDaylightDome", "Window"],
        construction_name: str,
        building_surface_name: str,
        vertex_1_x_coordinate: float,
        vertex_1_y_coordinate: float,
        vertex_1_z_coordinate: float,
        vertex_2_x_coordinate: float,
        vertex_2_y_coordinate: float,
        vertex_2_z_coordinate: float,
        vertex_3_x_coordinate: float,
        vertex_3_y_coordinate: float,
        vertex_3_z_coordinate: float,
        outside_boundary_condition_object: str | None = ...,
        view_factor_to_ground: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        frame_and_divider_name: str | None = ...,
        multiplier: float | None = 1,
        number_of_vertices: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        vertex_4_x_coordinate: float | None = ...,
        vertex_4_y_coordinate: float | None = ...,
        vertex_4_z_coordinate: float | None = ...,
    ) -> None:
        """Create a new ``FenestrationSurface:Detailed`` and add it to the document.

        Allows for detailed entry of subsurfaces (windows, doors, glass doors, tubular daylighting devices).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.1/io-reference/overview/group-thermal-zone-description-geometry/#fenestrationsurfacedetailed
        """

class AirLoopHVACOutdoorAirSystem_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        controller_list_name: str,
        outdoor_air_equipment_list_name: str,
        availability_manager_list_name: str | None = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:OutdoorAirSystem`` and add it to the document.

        Outdoor air subsystem for an AirLoopHVAC. Includes an outdoor air mixing box and optional outdoor air conditioning equipment such as heat recovery, preheat, and precool coils. From the perspective of the primary air loop the outdoor air system is treated as a single component.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-air-distribution/#airloophvacoutdoorairsystem
        """

class CoilSystemCoolingDX_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        dx_cooling_coil_system_inlet_node_name: str,
        dx_cooling_coil_system_outlet_node_name: str,
        dx_cooling_coil_system_sensor_node_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:SingleSpeed:ThermalStorage",
            "Coil:Cooling:DX:TwoSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        availability_schedule_name: str | None = ...,
        dehumidification_control_type: Literal["", "CoolReheat", "Multimode", "None"] | None = "None",
        run_on_sensible_load: Literal["", "No", "Yes"] | None = "Yes",
        run_on_latent_load: Literal["", "No", "Yes"] | None = "No",
        use_outdoor_air_dx_cooling_coil: Literal["", "No", "Yes"] | None = "No",
        outdoor_air_dx_cooling_coil_leaving_minimum_air_temperature: float | None = 2,
    ) -> None:
        """Create a new ``CoilSystem:Cooling:DX`` and add it to the document.

        Virtual container component that consists of a DX cooling coil and its associated controls. This control object supports several different types of DX cooling coils and may be placed directly in an air loop branch or outdoor air equipment list.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-heating-and-cooling-coils/#coilsystemcoolingdx
        """

class AirTerminalSingleDuctVAVHeatAndCoolNoReheat_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_outlet_node_name: str,
        air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        zone_minimum_air_flow_fraction: float,
        availability_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume for both cooling and heating, with no reheat coil.
        """

class DemandManagerVentilation_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        limit_control: Literal["FixedRate", "Off", "ReductionRatio"],
        availability_schedule_name: str | None = ...,
        minimum_limit_duration: float | None = ...,
        fixed_rate: float | None = ...,
        reduction_ratio: float | None = ...,
        limit_step_change: float | None = ...,
        selection_control: Literal["", "All", "RotateMany", "RotateOne"] | None = "All",
        rotation_duration: float | None = ...,
        controllers: list[_g.DemandManagerVentilationControllersItem] = ...,
    ) -> None:
        """Create a new ``DemandManager:Ventilation`` and add it to the document.

        used for demand limiting Controller:OutdoorAir objects.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-demand-limiting-controls/#demandmanagerventilation
        """

class PerformancePrecisionTradeoffs_v9_4_to_v9_5:
    def __call__(
        self,
        /,
        *,
        use_coil_direct_solutions: Literal["", "No", "Yes"] | None = "No",
        zone_radiant_exchange_algorithm: Literal["", "CarrollMRT", "ScriptF"] | None = "ScriptF",
        override_mode: Literal[
            "", "Advanced", "Mode01", "Mode02", "Mode03", "Mode04", "Mode05", "Mode06", "Mode07", "Normal"
        ]
        | None = "Normal",
        maxzonetempdiff: float | None = 0.3,
        maxalloweddeltemp: float | None = 0.002,
    ) -> None:
        """Create a new ``PerformancePrecisionTradeoffs`` and add it to the document.

        This object enables users to choose certain options that speed up EnergyPlus simulation, but may lead to small decreases in accuracy of results.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-simulation-parameters/#performanceprecisiontradeoffs
        """

class CoilCoolingDXCurveFitOperatingMode_v9_3_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        speed_1_name: str,
        rated_gross_total_cooling_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        rated_evaporator_air_flow_rate: float | Literal["Autosize"] | None = ...,
        rated_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_cycling_rate: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        latent_capacity_time_constant: float | None = 0,
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        apply_latent_degradation_to_speeds_greater_than_1: Literal["", "No", "Yes"] | None = "No",
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        nominal_evaporative_condenser_pump_power: float | Literal["", "Autosize"] | None = 0,
        nominal_speed_number: float | None = ...,
        speed_2_name: str | None = ...,
        speed_3_name: str | None = ...,
        speed_4_name: str | None = ...,
        speed_5_name: str | None = ...,
        speed_6_name: str | None = ...,
        speed_7_name: str | None = ...,
        speed_8_name: str | None = ...,
        speed_9_name: str | None = ...,
        speed_10_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:CurveFit:OperatingMode`` and add it to the document.

        DX cooling coil performance for a single operating mode which may have one or more speeds.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-coil-cooling-dx/#coilcoolingdxcurvefitoperatingmode
        """

class EnergyManagementSystemProgram_v8_9:
    def __call__(self, name: str, /, *, lines: list[_g.EnergyManagementSystemProgramLinesItem] = ...) -> None:
        """Create a new ``EnergyManagementSystem:Program`` and add it to the document.

        This input defines an Erl program Each field after the name is a line of EMS Runtime Language

        EnergyPlus I/O Reference: https://docs.idfkit.com/v8.9/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemprogram
        """

class ZoneHVACBaseboardRadiantConvectiveWater_v9_5_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        maximum_water_flow_rate: float | Literal["Autosize"],
        design_object: str | None = ...,
        availability_schedule_name: str | None = ...,
        rated_average_water_temperature: float | None = 87.78,
        rated_water_mass_flow_rate: float | None = 0.063,
        heating_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        surface_fractions: list[_g.ZoneHVACBaseboardRadiantConvectiveWaterSurfaceFractionsItem] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:Baseboard:RadiantConvective:Water`` and add it to the document.

        The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-radiative-convective-units/#zonehvacbaseboardradiantconvectivewater
        """
