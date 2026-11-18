"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g
from .. import versioned as _vd

class LoadProfilePlant_v8_9_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        load_schedule_name: str,
        peak_flow_rate: float,
        flow_rate_fraction_schedule_name: str,
    ) -> None:
        """Create a new ``LoadProfile:Plant`` and add it to the document.

        Used to simulate a scheduled plant loop demand profile. Load and flow rate are specified using schedules. Positive values are heating loads, and negative values are cooling loads. The actual load met is dependent on the performance of the supply loop components.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-non-zone-equipment/#loadprofileplant
        """

class ZoneVentilationWindandStackOpenArea_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        opening_area: float | None = 0,
        opening_area_fraction_schedule_name: str | None = ...,
        opening_effectiveness: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        effective_angle: float | None = 0,
        height_difference: float | None = 0,
        discharge_coefficient_for_opening: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        minimum_indoor_temperature: float | None = -100,
        minimum_indoor_temperature_schedule_name: str | None = ...,
        maximum_indoor_temperature: float | None = 100,
        maximum_indoor_temperature_schedule_name: str | None = ...,
        delta_temperature: float | None = -100,
        delta_temperature_schedule_name: str | None = ...,
        minimum_outdoor_temperature: float | None = -100,
        minimum_outdoor_temperature_schedule_name: str | None = ...,
        maximum_outdoor_temperature: float | None = 100,
        maximum_outdoor_temperature_schedule_name: str | None = ...,
        maximum_wind_speed: float | None = 40,
    ) -> None:
        """Create a new ``ZoneVentilation:WindandStackOpenArea`` and add it to the document.

        This object is specified as natural ventilation driven by wind and stack effect only: Ventilation Wind = Cw * Opening Area * Schedule * WindSpd Ventilation Stack = Cd * Opening Area * Schedule * SQRT(2*g*DH*(|(Tzone-Todb)|/Tzone)) Total Ventilation = SQRT((Ventilation Wind)^2 + (Ventilation Stack)^2)

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-airflow/#zoneventilationwindandstackopenarea
        """

class ShadowCalculation_v8_9_to_v9_2:
    def __call__(
        self,
        /,
        *,
        calculation_method: Literal["", "AverageOverDaysInFrequency", "TimestepFrequency"]
        | None = "AverageOverDaysInFrequency",
        calculation_frequency: float | None = 20,
        maximum_figures_in_shadow_overlap_calculations: float | None = 15000,
        polygon_clipping_algorithm: Literal["", "ConvexWeilerAtherton", "SutherlandHodgman"]
        | None = "SutherlandHodgman",
        sky_diffuse_modeling_algorithm: Literal["", "DetailedSkyDiffuseModeling", "SimpleSkyDiffuseModeling"]
        | None = "SimpleSkyDiffuseModeling",
        external_shading_calculation_method: Literal["", "ImportedShading", "InternalCalculation", "ScheduledShading"]
        | None = "InternalCalculation",
        output_external_shading_calculation_results: Literal["", "No", "Yes"] | None = "No",
        disable_self_shading_within_shading_zone_groups: Literal["", "No", "Yes"] | None = "No",
        disable_self_shading_from_shading_zone_groups_to_other_zones: Literal["", "No", "Yes"] | None = "No",
        shading_zone_groups: list[_g.ShadowCalculationShadingZoneGroupsItem] = ...,
    ) -> None:
        """Create a new ``ShadowCalculation`` and add it to the document.

        This object is used to control details of the solar, shading, and daylighting models

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-simulation-parameters/#shadowcalculation
        """

class InternalMass_v9_2_to_v9_5:
    def __call__(
        self, name: str, /, *, construction_name: str, zone_or_zonelist_name: str, surface_area: float
    ) -> None:
        """Create a new ``InternalMass`` and add it to the document.

        Used to describe internal zone surface area that does not need to be part of geometric representation. This should be the total surface area exposed to the zone air. If you use a ZoneList in the Zone or ZoneList name field then this definition applies to all the zones in the ZoneList.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-thermal-zone-description-geometry/#internalmass
        """

class OutputTableSummaryReports_v9_3:
    def __call__(self, /, *, reports: list[_vd.OutputTableSummaryReportsReportsItem_v9_3] = ...) -> None:
        """Create a new ``Output:Table:SummaryReports`` and add it to the document.

        This object allows the user to call report types that are predefined and will appear with the other tabular reports. These predefined reports are sensitive to the OutputControl:Table:Style object and appear in the same files as the tabular reports. The entries for this object is a list of the predefined reports that should appear in the tabular report output file. There should be as many fields (A) in this object as there are keys in the following (minus AllSummary+AllMonthly+AllSummaryAndMonthly)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.3/io-reference/standard-output-reports/output-table-summaryreports/#outputtablesummaryreports
        """

class CoilUserDefined_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        model_setup_and_sizing_program_calling_manager_name: str,
        number_of_air_connections: float,
        air_connection_1_inlet_node_name: str,
        air_connection_1_outlet_node_name: str,
        overall_model_simulation_program_calling_manager_name: str | None = ...,
        air_connection_2_inlet_node_name: str | None = ...,
        air_connection_2_outlet_node_name: str | None = ...,
        plant_connection_is_used: Literal["No", "Yes"] | None = ...,
        plant_connection_inlet_node_name: str | None = ...,
        plant_connection_outlet_node_name: str | None = ...,
        supply_inlet_water_storage_tank_name: str | None = ...,
        collection_outlet_water_storage_tank_name: str | None = ...,
        ambient_zone_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:UserDefined`` and add it to the document.

        Defines a generic air system component for custom modeling using Energy Management System or External Interface

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-user-defined-hvac-and-plant-component/#coiluserdefined
        """

class OutputSQLite_v24_1_to_v25_1:
    def __call__(
        self,
        /,
        *,
        option_type: Literal["Simple", "SimpleAndTabular"] | None = ...,
        unit_conversion_for_tabular_data: Literal[
            "",
            "InchPound",
            "InchPoundExceptElectricity",
            "JtoGJ",
            "JtoKWH",
            "JtoMJ",
            "None",
            "UseOutputControlTableStyle",
        ]
        | None = "UseOutputControlTableStyle",
    ) -> None:
        """Create a new ``Output:SQLite`` and add it to the document.

        Output from EnergyPlus can be written to an SQLite format file.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/input-for-output/#outputsqlite
        """

class WindowPropertyStormWindow_v8_9_to_v22_1:
    def __call__(
        self,
        /,
        *,
        window_name: str,
        storm_glass_layer_name: str,
        month_that_storm_glass_layer_is_put_on: float,
        day_of_month_that_storm_glass_layer_is_put_on: float,
        month_that_storm_glass_layer_is_taken_off: float,
        day_of_month_that_storm_glass_layer_is_taken_off: float,
        distance_between_storm_glass_layer_and_adjacent_glass: float | None = 0.05,
    ) -> None:
        """Create a new ``WindowProperty:StormWindow`` and add it to the document.

        This is a movable exterior glass layer that is usually applied in the winter and removed in the summer.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-thermal-zone-description-geometry/#windowpropertystormwindow
        """

class OutputDiagnostics_v8_9_to_v9_3:
    def __call__(
        self,
        /,
        *,
        key_1: Literal[
            "DisplayAdvancedReportVariables",
            "DisplayAllWarnings",
            "DisplayExtraWarnings",
            "DisplayUnusedObjects",
            "DisplayUnusedSchedules",
            "DisplayWeatherMissingDataWarnings",
            "DisplayZoneAirHeatBalanceOffBalance",
            "DoNotMirrorAttachedShading",
            "DoNotMirrorDetachedShading",
            "ReportDetailedWarmupConvergence",
            "ReportDuringHVACSizingSimulation",
            "ReportDuringWarmup",
        ]
        | None = ...,
        key_2: Literal[
            "DisplayAdvancedReportVariables",
            "DisplayAllWarnings",
            "DisplayExtraWarnings",
            "DisplayUnusedObjects",
            "DisplayUnusedSchedules",
            "DisplayWeatherMissingDataWarnings",
            "DisplayZoneAirHeatBalanceOffBalance",
            "DoNotMirrorAttachedShading",
            "DoNotMirrorDetachedShading",
            "ReportDetailedWarmupConvergence",
            "ReportDuringHVACSizingSimulation",
            "ReportDuringWarmup",
        ]
        | None = ...,
    ) -> None:
        """Create a new ``Output:Diagnostics`` and add it to the document.

        Special keys to produce certain warning messages or effect certain simulation characteristics.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.3/io-reference/overview/group-simulation-parameters/#outputdiagnostics
        """

class CentralHeatPumpSystem_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        cooling_loop_inlet_node_name: str,
        cooling_loop_outlet_node_name: str,
        source_loop_inlet_node_name: str,
        source_loop_outlet_node_name: str,
        heating_loop_inlet_node_name: str,
        heating_loop_outlet_node_name: str,
        chiller_heater_modules_performance_component_object_type_1: Literal["ChillerHeaterPerformance:Electric:EIR"],
        chiller_heater_modules_performance_component_name_1: str,
        chiller_heater_modules_control_schedule_name_1: str,
        control_method: Literal["", "SmartMixing"] | None = "SmartMixing",
        ancillary_power: float | None = 0,
        ancillary_operation_schedule_name: str | None = ...,
        number_of_chiller_heater_modules_1: float | None = 1,
        chiller_heater_modules_performance_component_object_type_2: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_2: str | None = ...,
        chiller_heater_modules_control_schedule_name_2: str | None = ...,
        number_of_chiller_heater_modules_2: float | None = 1,
        chiller_heater_performance_component_object_type_3: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_performance_component_name_3: str | None = ...,
        chiller_heater_modules_control_schedule_name_3: str | None = ...,
        number_of_chiller_heater_modules_3: float | None = 1,
        chiller_heater_modules_performance_component_object_type_4: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_4: str | None = ...,
        chiller_heater_modules_control_schedule_name_4: str | None = ...,
        number_of_chiller_heater_modules_4: float | None = 1,
        chiller_heater_modules_performance_component_object_type_5: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_models_performance_component_name_5: str | None = ...,
        chiller_heater_modules_control_schedule_name_5: str | None = ...,
        number_of_chiller_heater_modules_5: float | None = 1,
        chiller_heater_modules_performance_component_object_type_6: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_6: str | None = ...,
        chiller_heater_modules_control_schedule_name_6: str | None = ...,
        number_of_chiller_heater_modules_6: float | None = 1,
        chiller_heater_modules_performance_component_object_type_7: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_7: str | None = ...,
        chiller_heater_modules_control_schedule_name_7: str | None = ...,
        number_of_chiller_heater_modules_7: float | None = 1,
        chiller_heater_modules_performance_component_object_type_8: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_8: str | None = ...,
        chiller_heater_modules_control_schedule_name_8: str | None = ...,
        number_of_chiller_heater_modules_8: float | None = 1,
        chiller_heater_modules_performance_component_object_type_9: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_9: str | None = ...,
        chiller_heater_modules_control_schedule_name_9: str | None = ...,
        number_of_chiller_heater_modules_9: float | None = 1,
        chiller_heater_modules_performance_component_object_type_10: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_10: str | None = ...,
        chiller_heater_modules_control_schedule_name_10: str | None = ...,
        number_of_chiller_heater_modules_10: float | None = 1,
        chiller_heater_modules_performance_component_object_type_11: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_11: str | None = ...,
        chiller_heater_module_control_schedule_name_11: str | None = ...,
        number_of_chiller_heater_modules_11: float | None = 1,
        chiller_heater_modules_performance_component_object_type_12: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_12: str | None = ...,
        chiller_heater_modules_control_schedule_name_12: str | None = ...,
        number_of_chiller_heater_modules_12: float | None = 1,
        chiller_heater_modules_performance_component_object_type_13: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_13: str | None = ...,
        chiller_heater_modules_control_schedule_name_13: str | None = ...,
        number_of_chiller_heater_modules_13: float | None = 1,
        chiller_heater_modules_performance_component_object_type_14: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_14: str | None = ...,
        chiller_heater_modules_control_schedule_name_14: str | None = ...,
        number_of_chiller_heater_modules_14: float | None = 1,
        chiller_heater_modules_performance_component_object_type_15: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_15: str | None = ...,
        chiller_heater_modules_control_schedule_name_15: str | None = ...,
        number_of_chiller_heater_modules_15: float | None = 1,
        chiller_heater_modules_performance_component_object_type_16: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_16: str | None = ...,
        chiller_heater_modules_control_schedule_name_16: str | None = ...,
        number_of_chiller_heater_modules_16: float | None = 1,
        chiller_heater_modules_performance_component_object_type_17: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_17: str | None = ...,
        chiller_heater_modules_control_schedule_name_17: str | None = ...,
        number_of_chiller_heater_modules_17: float | None = 1,
        chiller_heater_modules_performance_component_object_type_18: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_18: str | None = ...,
        chiller_heater_modules_control_control_schedule_name_18: str | None = ...,
        number_of_chiller_heater_modules_18: float | None = 1,
        chiller_heater_modules_performance_component_object_type_19: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_19: str | None = ...,
        chiller_heater_modules_control_schedule_name_19: str | None = ...,
        number_of_chiller_heater_modules_19: float | None = 1,
        chiller_heater_modules_performance_component_object_type_20: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_20: str | None = ...,
        chiller_heater_modules_control_schedule_name_20: str | None = ...,
        number_of_chiller_heater_modules_20: float | None = 1,
    ) -> None:
        """Create a new ``CentralHeatPumpSystem`` and add it to the document.

        This chiller bank can contain multiple chiller heaters and heat pump performance objects. Its function is to encapsulate the extra controls needed to turn individual modules on/off and whether they are to operate in cooling-only, heating-only or simultaneous cooling/heating mode and whether to connect the source water to the evaporator or condenser side.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-plant-equipment/#centralheatpumpsystem
        """

class MatrixTwoDimension_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        number_of_rows: float,
        number_of_columns: float,
        values: list[_g.MatrixTwoDimensionValuesItem] = ...,
    ) -> None:
        """Create a new ``Matrix:TwoDimension`` and add it to the document.

        matrix data in row-major order list each row keeping the columns in order number of values must equal N1 x N2

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-surface-construction-elements/#matrixtwodimension
        """

class WallExterior_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 90,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None:
        """Create a new ``Wall:Exterior`` and add it to the document.

        Allows for simplified entry of exterior walls. View Factor to Ground is automatically calculated.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-thermal-zone-description-geometry/#wallexterior
        """
