"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class SurfaceConvectionAlgorithmInside:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        algorithm: Literal["ASTMC1340", "AdaptiveConvectionAlgorithm", "CeilingDiffuser", "Simple", "TARP"]
        | None = "TARP",
    ) -> None:
        """Create a new ``SurfaceConvectionAlgorithm:Inside`` and add it to the document.

        Default indoor surface heat transfer convection algorithm to be used for all zones

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#surfaceconvectionalgorithminside
        """

class WindowMaterialScreen:
    def __call__(
        self,
        name: str,
        /,
        *,
        diffuse_solar_reflectance: float,
        diffuse_visible_reflectance: float,
        screen_material_spacing: float,
        screen_material_diameter: float,
        reflected_beam_transmittance_accounting_method: Literal["DoNotModel", "ModelAsDiffuse", "ModelAsDirectBeam"]
        | None = "ModelAsDiffuse",
        thermal_hemispherical_emissivity: float | None = 0.9,
        conductivity: float | None = 221,
        screen_to_glass_distance: float | None = 0.025,
        top_opening_multiplier: float | None = 0,
        bottom_opening_multiplier: float | None = 0,
        left_side_opening_multiplier: float | None = 0,
        right_side_opening_multiplier: float | None = 0,
        angle_of_resolution_for_screen_transmittance_output_map: Literal[0, 1, 2, 3, 5] | None = 0,
    ) -> None:
        """Create a new ``WindowMaterial:Screen`` and add it to the document.

        Window screen physical properties. Can only be located on the exterior side of a window construction.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialscreen
        """

class FoundationKivaSettings:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        soil_conductivity: float | None = 1.73,
        soil_density: float | None = 1842,
        soil_specific_heat: float | None = 419,
        ground_solar_absorptivity: float | None = 0.9,
        ground_thermal_absorptivity: float | None = 0.9,
        ground_surface_roughness: float | None = 0.03,
        far_field_width: float | None = 40,
        deep_ground_boundary_condition: Literal["Autoselect", "GroundWater", "ZeroFlux"] | None = "Autoselect",
        deep_ground_depth: float | Literal["Autocalculate"] | None = "Autocalculate",
        minimum_cell_dimension: float | None = 0.02,
        maximum_cell_growth_coefficient: float | None = 1.5,
        simulation_timestep: Literal["Hourly", "Timestep"] | None = "Hourly",
    ) -> None:
        """Create a new ``Foundation:Kiva:Settings`` and add it to the document.

        Settings applied across all Kiva foundation calculations. Object is not required. If not defined, defaults will be applied.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#foundationkivasettings
        """

class AirflowNetworkDistributionComponentLeak:
    def __call__(
        self, name: str, /, *, air_mass_flow_coefficient: float, air_mass_flow_exponent: float | None = 0.65
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:Component:Leak`` and add it to the document.

        This object defines the characteristics of a supply or return air leak.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkdistributioncomponentleak
        """

class CoilCoolingDXVariableRefrigerantFlowFluidTemperatureControl:
    def __call__(
        self,
        name: str,
        /,
        *,
        coil_air_inlet_node: str,
        coil_air_outlet_node: str,
        rated_total_cooling_capacity: float | Literal["Autosize"],
        rated_sensible_heat_ratio: float | Literal["Autosize"],
        indoor_unit_evaporating_temperature_function_of_superheating_curve_name: str,
        availability_schedule_name: str | None = ...,
        indoor_unit_reference_superheating: float | None = 5,
        name_of_water_storage_tank_for_condensate_collection: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:VariableRefrigerantFlow:FluidTemperatureControl`` and add it to the document.

        This is a key object in the new physics based VRF model applicable for Fluid Temperature Control. It describes the the indoor unit coil of the system at cooling mode. Used with ZoneHVAC:TerminalUnit:VariableRefrigerantFlow. Outdoor unit is modeled separately, see AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl or AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl:HR

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxvariablerefrigerantflowfluidtemperaturecontrol
        """

class OutdoorAirNode:
    def __call__(
        self,
        name: str,
        /,
        *,
        height_above_ground: float | None = -1,
        drybulb_temperature_schedule_name: str | None = ...,
        wetbulb_temperature_schedule_name: str | None = ...,
        wind_speed_schedule_name: str | None = ...,
        wind_direction_schedule_name: str | None = ...,
        wind_pressure_coefficient_curve_name: str | None = ...,
        symmetric_wind_pressure_coefficient_curve: Literal["No", "Yes"] | None = "No",
        wind_angle_type: Literal["Absolute", "Relative"] | None = "Absolute",
    ) -> None:
        """Create a new ``OutdoorAir:Node`` and add it to the document.

        This object sets the temperature and humidity conditions for an outdoor air node. It allows the height above ground to be specified. This object may be used more than once. The same node name may not appear in both an OutdoorAir:Node object and an OutdoorAir:NodeList object. This object defines local outdoor air environmental conditions.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution/#outdoorairnode
        """

class PlantLoop:
    def __call__(
        self,
        name: str,
        /,
        *,
        plant_equipment_operation_scheme_name: str,
        loop_temperature_setpoint_node_name: str,
        maximum_loop_temperature: float,
        minimum_loop_temperature: float,
        maximum_loop_flow_rate: float | Literal["Autosize"],
        plant_side_inlet_node_name: str,
        plant_side_outlet_node_name: str,
        plant_side_branch_list_name: str,
        demand_side_inlet_node_name: str,
        demand_side_outlet_node_name: str,
        demand_side_branch_list_name: str,
        fluid_type: Literal["Steam", "UserDefinedFluidType", "Water"] | None = "Water",
        user_defined_fluid_type: str | None = ...,
        minimum_loop_flow_rate: float | None = 0,
        plant_loop_volume: float | Literal["Autocalculate"] | None = "Autocalculate",
        plant_side_connector_list_name: str | None = ...,
        demand_side_connector_list_name: str | None = ...,
        load_distribution_scheme: Literal[
            "Optimal", "SequentialLoad", "SequentialUniformPLR", "UniformLoad", "UniformPLR"
        ]
        | None = "SequentialLoad",
        availability_manager_list_name: str | None = ...,
        plant_loop_demand_calculation_scheme: Literal["DualSetpointDeadband", "SingleSetpoint"]
        | None = "SingleSetpoint",
        common_pipe_simulation: Literal["CommonPipe", "None", "TwoWayCommonPipe"] | None = "None",
        pressure_simulation_type: Literal["LoopFlowCorrection", "None", "PumpPowerCorrection"] | None = "None",
        loop_circulation_time: float | None = 2,
    ) -> None:
        """Create a new ``PlantLoop`` and add it to the document.

        Defines a central plant loop.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-loops/#plantloop
        """

class PlantEquipmentOperationOutdoorDryBulb:
    def __call__(
        self,
        name: str,
        /,
        *,
        dry_bulb_temperature_range_1_lower_limit: float,
        dry_bulb_temperature_range_1_upper_limit: float,
        range_1_equipment_list_name: str,
        dry_bulb_temperature_range_2_lower_limit: float | None = ...,
        dry_bulb_temperature_range_2_upper_limit: float | None = ...,
        range_2_equipment_list_name: str | None = ...,
        dry_bulb_temperature_range_3_lower_limit: float | None = ...,
        dry_bulb_temperature_range_3_upper_limit: float | None = ...,
        range_3_equipment_list_name: str | None = ...,
        dry_bulb_temperature_range_4_lower_limit: float | None = ...,
        dry_bulb_temperature_range_4_upper_limit: float | None = ...,
        range_4_equipment_list_name: str | None = ...,
        dry_bulb_temperature_range_5_lower_limit: float | None = ...,
        dry_bulb_temperature_range_5_upper_limit: float | None = ...,
        range_5_equipment_list_name: str | None = ...,
        dry_bulb_temperature_range_6_lower_limit: float | None = ...,
        dry_bulb_temperature_range_6_upper_limit: float | None = ...,
        range_6_equipment_list_name: str | None = ...,
        dry_bulb_temperature_range_7_lower_limit: float | None = ...,
        dry_bulb_temperature_range_7_upper_limit: float | None = ...,
        range_7_equipment_list_name: str | None = ...,
        dry_bulb_temperature_range_8_lower_limit: float | None = ...,
        dry_bulb_temperature_range_8_upper_limit: float | None = ...,
        range_8_equipment_list_name: str | None = ...,
        dry_bulb_temperature_range_9_lower_limit: float | None = ...,
        dry_bulb_temperature_range_9_upper_limit: float | None = ...,
        range_9_equipment_list_name: str | None = ...,
        dry_bulb_temperature_range_10_lower_limit: float | None = ...,
        dry_bulb_temperature_range_10_upper_limit: float | None = ...,
        range_10_equipment_list_name: str | None = ...,
    ) -> None:
        """Create a new ``PlantEquipmentOperation:OutdoorDryBulb`` and add it to the document.

        Plant equipment operation scheme for outdoor dry-bulb temperature range operation. Specifies one or more groups of equipment which are available to operate for successive outdoor dry-bulb temperature ranges.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationoutdoordrybulb
        """

class SetpointManagerMultiZoneCoolingAverage:
    def __call__(
        self,
        name: str,
        /,
        *,
        hvac_air_loop_name: str,
        setpoint_node_or_nodelist_name: str,
        minimum_setpoint_temperature: float | None = 12,
        maximum_setpoint_temperature: float | None = 18,
    ) -> None:
        """Create a new ``SetpointManager:MultiZone:Cooling:Average`` and add it to the document.

        This setpoint manager sets the average supply air temperature based on the cooling load requirements of all controlled zones in an air loop served by a central air-conditioner.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagermultizonecoolingaverage
        """

class ElectricLoadCenterDistribution:
    def __call__(
        self,
        name: str,
        /,
        *,
        generator_list_name: str | None = ...,
        generator_operation_scheme_type: Literal[
            "Baseload",
            "DemandLimit",
            "FollowThermal",
            "FollowThermalLimitElectrical",
            "TrackElectrical",
            "TrackMeter",
            "TrackSchedule",
        ]
        | None = ...,
        generator_demand_limit_scheme_purchased_electric_demand_limit: float | None = ...,
        generator_track_schedule_name_scheme_schedule_name: str | None = ...,
        generator_track_meter_scheme_meter_name: str | None = ...,
        electrical_buss_type: Literal[
            "AlternatingCurrent",
            "AlternatingCurrentWithStorage",
            "DirectCurrentWithInverter",
            "DirectCurrentWithInverterACStorage",
            "DirectCurrentWithInverterDCStorage",
        ]
        | None = "AlternatingCurrent",
        inverter_name: str | None = ...,
        electrical_storage_object_name: str | None = ...,
        transformer_object_name: str | None = ...,
        storage_operation_scheme: Literal[
            "FacilityDemandLeveling",
            "TrackChargeDischargeSchedules",
            "TrackFacilityElectricDemandStoreExcessOnSite",
            "TrackMeterDemandStoreExcessOnSite",
        ]
        | None = ...,
        storage_control_track_meter_name: str | None = ...,
        storage_converter_object_name: str | None = ...,
        maximum_storage_state_of_charge_fraction: float | None = 1,
        minimum_storage_state_of_charge_fraction: float | None = 0,
        design_storage_control_charge_power: float | None = ...,
        storage_charge_power_fraction_schedule_name: str | None = ...,
        design_storage_control_discharge_power: float | None = ...,
        storage_discharge_power_fraction_schedule_name: str | None = ...,
        storage_control_utility_demand_target: float | None = ...,
        storage_control_utility_demand_target_fraction_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``ElectricLoadCenter:Distribution`` and add it to the document.

        ElectricLoadCenter:Distribution objects are used to include on-site electricity generators and or storage in a simulation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#electricloadcenterdistribution
        """

class AnyHybridModelZone:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        zone_measured_air_temperature_schedule_name: str,
        begin_month: int,
        begin_day_of_month: int,
        end_month: int,
        end_day_of_month: int,
        calculate_zone_internal_thermal_mass: Literal["No", "Yes"] | None = "No",
        calculate_zone_air_infiltration_rate: Literal["No", "Yes"] | None = "No",
    ) -> None:
        """Create a new ``HybridModel:Zone`` and add it to the document.

        Zones with measured air temperature data and a range of dates. If the range of temperature measurement dates includes a leap day, the weather data should include a leap day.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-hybrid-model/#hybridmodelzone
        """

class ParametricRunControl:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        runs: Sequence[_g.ParametricRunControlRunsItem | _g.ParametricRunControlRunsGroup] = ...,
    ) -> None:
        """Create a new ``Parametric:RunControl`` and add it to the document.

        Controls which parametric runs are simulated. This object is optional. If it is not included, then all parametric runs are performed.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/parametric-objects/#parametricruncontrol
        """
