"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

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

class ShadowCalculation_v8_9_to_v9_2:
    def __call__(
        self,
        /,
        *,
        calculation_method: Literal["AverageOverDaysInFrequency", "TimestepFrequency"]
        | None = "AverageOverDaysInFrequency",
        calculation_frequency: float | None = 20,
        maximum_figures_in_shadow_overlap_calculations: float | None = 15000,
        polygon_clipping_algorithm: Literal["ConvexWeilerAtherton", "SutherlandHodgman"] | None = "SutherlandHodgman",
        sky_diffuse_modeling_algorithm: Literal["DetailedSkyDiffuseModeling", "SimpleSkyDiffuseModeling"]
        | None = "SimpleSkyDiffuseModeling",
        external_shading_calculation_method: Literal["ImportedShading", "InternalCalculation", "ScheduledShading"]
        | None = "InternalCalculation",
        output_external_shading_calculation_results: Literal["No", "Yes"] | None = "No",
        disable_self_shading_within_shading_zone_groups: Literal["No", "Yes"] | None = "No",
        disable_self_shading_from_shading_zone_groups_to_other_zones: Literal["No", "Yes"] | None = "No",
        shading_zone_groups: Sequence[
            _g.ShadowCalculationShadingZoneGroupsItem | _g.ShadowCalculationShadingZoneGroupsGroup
        ] = ...,
    ) -> None:
        """Create a new ``ShadowCalculation`` and add it to the document.

        This object is used to control details of the solar, shading, and daylighting models

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-simulation-parameters/#shadowcalculation
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
            "InchPound", "InchPoundExceptElectricity", "JtoGJ", "JtoKWH", "JtoMJ", "None", "UseOutputControlTableStyle"
        ]
        | None = "UseOutputControlTableStyle",
    ) -> None:
        """Create a new ``Output:SQLite`` and add it to the document.

        Output from EnergyPlus can be written to an SQLite format file.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/input-for-output/#outputsqlite
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
        control_method: Literal["SmartMixing"] | None = "SmartMixing",
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-plant-equipment/#centralheatpumpsystem
        """
