"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class SurfacePropertyExteriorNaturalVentedCavity:
    def __call__(
        self,
        name: str,
        /,
        *,
        boundary_conditions_model_name: str,
        roughness_of_exterior_surface: Literal[
            "MediumRough", "MediumSmooth", "Rough", "Smooth", "VeryRough", "VerySmooth"
        ],
        area_fraction_of_openings: float | None = ...,
        thermal_emissivity_of_exterior_baffle_material: float | None = ...,
        solar_absorbtivity_of_exterior_baffle: float | None = ...,
        height_scale_for_buoyancy_driven_ventilation: float | None = ...,
        effective_thickness_of_cavity_behind_exterior_baffle: float | None = ...,
        ratio_of_actual_surface_area_to_projected_surface_area: float | None = 1,
        effectiveness_for_perforations_with_respect_to_wind: float | None = 0.25,
        discharge_coefficient_for_openings_with_respect_to_buoyancy_driven_flow: float | None = 0.65,
        surface: Sequence[
            _g.SurfacePropertyExteriorNaturalVentedCavitySurfaceItem
            | _g.SurfacePropertyExteriorNaturalVentedCavitySurfaceGroup
        ] = ...,
    ) -> None:
        """Create a new ``SurfaceProperty:ExteriorNaturalVentedCavity`` and add it to the document.

        Used to describe the decoupled layer, or baffle, and the characteristics of the cavity and openings for naturally ventilated exterior surfaces. This object is also used in conjunction with the OtherSideConditionsModel.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyexteriornaturalventedcavity
        """

class GroundHeatTransferSlabAutoGrid:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        slabx_x_dimension_of_the_building_slab: float,
        slaby_y_dimension_of_the_building_slab: float,
        slabdepth_thickness_of_slab_on_grade: float | None = 0.1,
        clearance_distance_from_edge_of_slab_to_domain_edge: float | None = 15,
        zclearance_distance_from_bottom_of_slab_to_domain_bottom: float | None = 15,
    ) -> None:
        """Create a new ``GroundHeatTransfer:Slab:AutoGrid`` and add it to the document.

        AutoGrid only necessary when EquivalentSlab option not chosen. Not normally needed by EnergyPlus users. This object permits user selection of rectangular slab dimensions. NO SLAB DIMENSIONS LESS THAN 6 m.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferslabautogrid
        """

class GroundHeatTransferBasementInsulation:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        insfull_flag_is_the_wall_fully_insulated_: Literal["FALSE", "TRUE"],
        rext_r_value_of_any_exterior_insulation: float | None = ...,
    ) -> None:
        """Create a new ``GroundHeatTransfer:Basement:Insulation`` and add it to the document.

        Describes the insulation used on an exterior basement wall for the Basement preprocessor ground heat transfer simulation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferbasementinsulation
        """

class DesignSpecificationZoneHVACSizing:
    def __call__(
        self,
        name: str,
        /,
        *,
        cooling_supply_air_flow_rate_method: Literal[
            "",
            "FlowPerCoolingCapacity",
            "FlowPerFloorArea",
            "FractionOfAutosizedCoolingAirflow",
            "None",
            "SupplyAirFlowRate",
        ]
        | None = "SupplyAirFlowRate",
        cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        cooling_supply_air_flow_rate_per_floor_area: float | None = ...,
        cooling_fraction_of_autosized_cooling_supply_air_flow_rate: float | None = ...,
        cooling_supply_air_flow_rate_per_unit_cooling_capacity: float | None = ...,
        no_load_supply_air_flow_rate_method: Literal[
            "",
            "FlowPerFloorArea",
            "FractionOfAutosizedCoolingAirflow",
            "FractionOfAutosizedHeatingAirflow",
            "None",
            "SupplyAirFlowRate",
        ]
        | None = "SupplyAirFlowRate",
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_supply_air_flow_rate_per_floor_area: float | None = ...,
        no_load_fraction_of_cooling_supply_air_flow_rate: float | None = ...,
        no_load_fraction_of_heating_supply_air_flow_rate: float | None = ...,
        heating_supply_air_flow_rate_method: Literal[
            "",
            "FlowPerFloorArea",
            "FlowPerHeatingCapacity",
            "FractionOfAutosizedHeatingAirflow",
            "None",
            "SupplyAirFlowRate",
        ]
        | None = "SupplyAirFlowRate",
        heating_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_supply_air_flow_rate_per_floor_area: float | None = ...,
        heating_fraction_of_heating_supply_air_flow_rate: float | None = ...,
        heating_supply_air_flow_rate_per_unit_heating_capacity: float | None = ...,
        cooling_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "CoolingDesignCapacity", "FractionOfAutosizedCoolingCapacity", "None"
        ]
        | None = "None",
        cooling_design_capacity: float | Literal["Autosize"] | None = ...,
        cooling_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_cooling_design_capacity: float | None = ...,
        heating_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity", "None"
        ]
        | None = "None",
        heating_design_capacity: float | Literal["Autosize"] | None = ...,
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = ...,
    ) -> None:
        """Create a new ``DesignSpecification:ZoneHVAC:Sizing`` and add it to the document.

        This object is used to describe general scalable zone HVAC equipment sizing which are referenced by other objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-design-objects/#designspecificationzonehvacsizing
        """

class ZoneHVACDehumidifierDX:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        rated_water_removal: float,
        rated_energy_factor: float,
        rated_air_flow_rate: float,
        water_removal_curve_name: str,
        energy_factor_curve_name: str,
        part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        minimum_dry_bulb_temperature_for_dehumidifier_operation: float | None = 10,
        maximum_dry_bulb_temperature_for_dehumidifier_operation: float | None = 35,
        off_cycle_parasitic_electric_load: float | None = 0,
        condensate_collection_water_storage_tank_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:Dehumidifier:DX`` and add it to the document.

        This object calculates the performance of zone (room) air dehumidifiers. Meant to model conventional direct expansion (DX) cooling-based room air dehumidifiers (reject 100% of condenser heat to the zone air), but this object might be able to be used to model other room air dehumidifier types.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacdehumidifierdx
        """

class AirLoopHVACControllerList:
    def __call__(
        self,
        name: str,
        /,
        *,
        controller_1_object_type: Literal["Controller:OutdoorAir", "Controller:WaterCoil"],
        controller_1_name: str,
        controller_2_object_type: Literal["Controller:OutdoorAir", "Controller:WaterCoil"] | None = ...,
        controller_2_name: str | None = ...,
        controller_3_object_type: Literal["Controller:OutdoorAir", "Controller:WaterCoil"] | None = ...,
        controller_3_name: str | None = ...,
        controller_4_object_type: Literal["Controller:OutdoorAir", "Controller:WaterCoil"] | None = ...,
        controller_4_name: str | None = ...,
        controller_5_object_type: Literal["Controller:OutdoorAir", "Controller:WaterCoil"] | None = ...,
        controller_5_name: str | None = ...,
        controller_6_object_type: Literal["Controller:OutdoorAir", "Controller:WaterCoil"] | None = ...,
        controller_6_name: str | None = ...,
        controller_7_object_type: Literal["Controller:OutdoorAir", "Controller:WaterCoil"] | None = ...,
        controller_7_name: str | None = ...,
        controller_8_object_type: Literal["Controller:OutdoorAir", "Controller:WaterCoil"] | None = ...,
        controller_8_name: str | None = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:ControllerList`` and add it to the document.

        List controllers in order of control sequence

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution/#airloophvaccontrollerlist
        """

class AnyPipingSystemUndergroundPipeCircuit:
    def __call__(
        self,
        name: str,
        /,
        *,
        pipe_thermal_conductivity: float,
        pipe_density: float,
        pipe_specific_heat: float,
        pipe_inner_diameter: float,
        pipe_outer_diameter: float,
        design_flow_rate: float,
        circuit_inlet_node: str,
        circuit_outlet_node: str,
        radial_thickness_of_inner_radial_near_pipe_mesh_region: float,
        number_of_pipe_segments_entered_for_this_pipe_circuit: int,
        convergence_criterion_for_the_inner_radial_iteration_loop: float | None = 0.001,
        maximum_iterations_in_the_inner_radial_iteration_loop: int | None = 500,
        number_of_soil_nodes_in_the_inner_radial_near_pipe_mesh_region: int | None = 3,
        pipe_segments: Sequence[
            _g.PipingSystemUndergroundPipeCircuitPipeSegmentsItem
            | _g.PipingSystemUndergroundPipeCircuitPipeSegmentsGroup
        ] = ...,
    ) -> None:
        """Create a new ``PipingSystem:Underground:PipeCircuit`` and add it to the document.

        The pipe circuit object in an underground piping system. This object is simulated within an underground piping domain object and connected on a branch on a plant loop.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-node-branch-management/#pipingsystemundergroundpipecircuit
        """

class ThermalStorageSizing:
    def __call__(
        self,
        name: str,
        /,
        *,
        on_peak_period_start_time: float,
        on_peak_period_end_time: float,
        sizing_factor: float | None = 1,
    ) -> None:
        """Create a new ``ThermalStorage:Sizing`` and add it to the document.

        Sizing information for thermal energy stoarge capacity.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-heaters/#thermalstoragesizing
        """

class EnergyManagementSystemGlobalVariable:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        variables: Sequence[
            _g.EnergyManagementSystemGlobalVariableVariablesItem | _g.EnergyManagementSystemGlobalVariableVariablesGroup
        ] = ...,
    ) -> None:
        """Create a new ``EnergyManagementSystem:GlobalVariable`` and add it to the document.

        Declares Erl variable as having global scope No spaces allowed in names used for Erl variables

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemglobalvariable
        """

class AvailabilityManagerHybridVentilation:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_zone_name: str,
        ventilation_control_mode_schedule_name: str,
        hvac_air_loop_name: str | None = ...,
        use_weather_file_rain_indicators: Literal["", "No", "Yes"] | None = "Yes",
        maximum_wind_speed: float | None = 40,
        minimum_outdoor_temperature: float | None = -100,
        maximum_outdoor_temperature: float | None = 100,
        minimum_outdoor_enthalpy: float | None = ...,
        maximum_outdoor_enthalpy: float | None = ...,
        minimum_outdoor_dewpoint: float | None = -100,
        maximum_outdoor_dewpoint: float | None = 100,
        minimum_outdoor_ventilation_air_schedule_name: str | None = ...,
        opening_factor_function_of_wind_speed_curve_name: str | None = ...,
        airflownetwork_control_type_schedule_name: str | None = ...,
        simple_airflow_control_type_schedule_name: str | None = ...,
        zoneventilation_object_name: str | None = ...,
        minimum_hvac_operation_time: float | None = 0,
        minimum_ventilation_time: float | None = 0,
    ) -> None:
        """Create a new ``AvailabilityManager:HybridVentilation`` and add it to the document.

        Depending on zone and outdoor conditions overrides window/door opening controls to maximize natural ventilation and turn off an HVAC system when ventilation control conditions are met. This object (zone ventilation object name) has not been instrumented to work with global Zone or Zone List names option for Ventilation:DesignFlowRate. In order to use, you must enter the single <Ventilation:DesignFlowRate> name in that field. If it is a part of a global ventilation assignment the name will be <Zone Name> <global Ventilation:DesignFlowRate> name. Currently, hybrid ventilation manager is restricted to one per zone. It can either be applied through the air loop or directly to the zone. If hybrid ventilation manager is applied to an air loop and one of the zones served by that air loop also has hybrid ventilation manager, then zone hybrid ventilation manager is disabled.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-system-availability-managers/#availabilitymanagerhybridventilation
        """
