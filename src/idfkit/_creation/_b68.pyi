"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class ConstructionPropertyInternalHeatSource:
    def __call__(
        self,
        name: str,
        /,
        *,
        thermal_source_present_after_layer_number: int,
        temperature_calculation_requested_after_layer_number: int,
        dimensions_for_the_ctf_calculation: int,
        tube_spacing: float,
        construction_name: str | None = ...,
        two_dimensional_temperature_calculation_position: float | None = 0,
    ) -> None:
        """Create a new ``ConstructionProperty:InternalHeatSource`` and add it to the document.

        Internal heat source to be attached to a construction layer

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#constructionpropertyinternalheatsource
        """

class AnySurfacePropertyLocalEnvironment:
    def __call__(
        self,
        name: str,
        /,
        *,
        exterior_surface_name: str | None = ...,
        surrounding_surfaces_object_name: str | None = ...,
        outdoor_air_node_name: str | None = ...,
    ) -> None:
        """Create a new ``SurfaceProperty:LocalEnvironment`` and add it to the document.

        This object defines the local environment properties of an exterior surface. One or more environment properties have to be defined and linked to the exterior surface.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertylocalenvironment
        """

class LightsInstance:
    def __call__(
        self,
        name: str,
        /,
        *,
        lights_definition_name: str,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        fraction_replaceable: float | None = 1,
        multiplier: float | None = 1,
        end_use_subcategory: str | None = "General",
        return_air_heat_gain_node_name: str | None = ...,
        exhaust_air_heat_gain_node_name: str | None = ...,
    ) -> None:
        """Create a new ``Lights:Instance`` and add it to the document.

        Sets internal gains for lights in the zone. The physical characteristics are given by the referenced Lights:Definition object. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains/#lightsinstance
        """

class DaylightingDeviceLightWell:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        exterior_window_name: str,
        height_of_well: float,
        perimeter_of_bottom_of_well: float,
        area_of_bottom_of_well: float,
        visible_reflectance_of_well_walls: float,
    ) -> None:
        """Create a new ``DaylightingDevice:LightWell`` and add it to the document.

        Applies only to exterior windows in daylighting-controlled zones or in zones that share an interior window with a daylighting-controlled zone. Generally used with skylights.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-daylighting/#daylightingdevicelightwell
        """

class HVACTemplateSystemUnitaryHeatPumpAirToAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_zone_or_thermostat_location_name: str,
        system_availability_schedule_name: str | None = ...,
        cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        heating_supply_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        supply_fan_operating_mode_schedule_name: str | None = ...,
        supply_fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 600,
        supply_fan_motor_efficiency: float | None = 0.9,
        supply_fan_motor_in_air_stream_fraction: float | None = 1,
        cooling_coil_type: Literal["SingleSpeedDX"] | None = "SingleSpeedDX",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_design_supply_air_temperature: float | None = 12.8,
        cooling_coil_gross_rated_total_capacity: float | Literal["Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_cop: float | None = 3,
        heat_pump_heating_coil_type: Literal["SingleSpeedDXHeatPump"] | None = "SingleSpeedDXHeatPump",
        heat_pump_heating_coil_availability_schedule_name: str | None = ...,
        heating_design_supply_air_temperature: float | None = 50,
        heat_pump_heating_coil_gross_rated_capacity: float | Literal["Autosize"] | None = "Autosize",
        heat_pump_heating_coil_rated_cop: float | None = 2.75,
        heat_pump_heating_minimum_outdoor_dry_bulb_temperature: float | None = -8,
        heat_pump_defrost_maximum_outdoor_dry_bulb_temperature: float | None = 5,
        heat_pump_defrost_strategy: Literal["Resistive", "ReverseCycle"] | None = "ReverseCycle",
        heat_pump_defrost_control: Literal["OnDemand", "Timed"] | None = "Timed",
        heat_pump_defrost_time_period_fraction: float | None = 0.058333,
        supplemental_heating_coil_type: Literal["Electric", "Gas", "HotWater"] | None = "Electric",
        supplemental_heating_coil_availability_schedule_name: str | None = ...,
        supplemental_heating_coil_capacity: float | Literal["Autosize"] | None = "Autosize",
        supplemental_heating_coil_maximum_outdoor_dry_bulb_temperature: float | None = 21,
        supplemental_gas_heating_coil_efficiency: float | None = 0.8,
        supplemental_gas_heating_coil_parasitic_electric_load: float | None = 0,
        maximum_outdoor_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        minimum_outdoor_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        minimum_outdoor_air_schedule_name: str | None = ...,
        economizer_type: Literal[
            "DifferentialDryBulb",
            "DifferentialDryBulbAndEnthalpy",
            "DifferentialEnthalpy",
            "ElectronicEnthalpy",
            "FixedDewPointAndDryBulb",
            "FixedDryBulb",
            "FixedEnthalpy",
            "NoEconomizer",
        ]
        | None = "NoEconomizer",
        economizer_lockout: Literal["LockoutWithCompressor", "LockoutWithHeating", "NoLockout"] | None = "NoLockout",
        economizer_maximum_limit_dry_bulb_temperature: float | None = ...,
        economizer_maximum_limit_enthalpy: float | None = ...,
        economizer_maximum_limit_dewpoint_temperature: float | None = ...,
        economizer_minimum_limit_dry_bulb_temperature: float | None = ...,
        supply_plenum_name: str | None = ...,
        return_plenum_name: str | None = ...,
        night_cycle_control: Literal["CycleOnAny", "CycleOnControlZone", "StayOff"] | None = "StayOff",
        night_cycle_control_zone_name: str | None = ...,
        heat_recovery_type: Literal["Enthalpy", "None", "Sensible"] | None = "None",
        sensible_heat_recovery_effectiveness: float | None = 0.7,
        latent_heat_recovery_effectiveness: float | None = 0.65,
        humidifier_type: Literal["ElectricSteam", "None"] | None = "None",
        humidifier_availability_schedule_name: str | None = ...,
        humidifier_rated_capacity: float | None = ...,
        humidifier_rated_electric_power: float | Literal["Autosize"] | None = "Autosize",
        humidifier_control_zone_name: str | None = ...,
        humidifier_setpoint: float | None = 30,
        return_fan: Literal["No", "Yes"] | None = "No",
        return_fan_total_efficiency: float | None = 0.7,
        return_fan_delta_pressure: float | None = 500,
        return_fan_motor_efficiency: float | None = 0.9,
        return_fan_motor_in_air_stream_fraction: float | None = 1,
    ) -> None:
        """Create a new ``HVACTemplate:System:UnitaryHeatPump:AirToAir`` and add it to the document.

        Unitary furnace with electric air-to-air heat pump

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatesystemunitaryheatpumpairtoair
        """

class AnySizingZone:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        zone_or_zonelist_name: str,
        zone_cooling_design_supply_air_humidity_ratio: float,
        zone_heating_design_supply_air_humidity_ratio: float,
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_cooling_design_supply_air_temperature: float | None = ...,
        zone_cooling_design_supply_air_temperature_difference: float | None = ...,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = ...,
        zone_heating_design_supply_air_temperature_difference: float | None = ...,
        design_specification_outdoor_air_object_name: str | None = ...,
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        cooling_design_air_flow_method: Literal["DesignDay", "DesignDayWithLimit", "Flow/Zone"] | None = "DesignDay",
        cooling_design_air_flow_rate: float | None = 0,
        cooling_minimum_air_flow_per_zone_floor_area: float | None = 0.000762,
        cooling_minimum_air_flow: float | None = 0,
        cooling_minimum_air_flow_fraction: float | None = 0.2,
        heating_design_air_flow_method: Literal["DesignDay", "DesignDayWithLimit", "Flow/Zone"] | None = "DesignDay",
        heating_design_air_flow_rate: float | None = 0,
        heating_maximum_air_flow_per_zone_floor_area: float | None = 0.002032,
        heating_maximum_air_flow: float | None = 0.1415762,
        heating_maximum_air_flow_fraction: float | None = 0.3,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        account_for_dedicated_outdoor_air_system: Literal["No", "Yes"] | None = "No",
        dedicated_outdoor_air_system_control_strategy: Literal[
            "ColdSupplyAir", "NeutralDehumidifiedSupplyAir", "NeutralSupplyAir"
        ]
        | None = "NeutralSupplyAir",
        dedicated_outdoor_air_low_setpoint_temperature_for_design: float | Literal["Autosize"] | None = "Autosize",
        dedicated_outdoor_air_high_setpoint_temperature_for_design: float | Literal["Autosize"] | None = "Autosize",
    ) -> None:
        """Create a new ``Sizing:Zone`` and add it to the document.

        Specifies the data needed to perform a zone design air flow calculation. The calculation is done for every sizing period included in the input. The maximum cooling and heating load and cooling, heating, and ventilation air flows are then saved for system level and zone component design calculations.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-design-objects/#sizingzone
        """

class FanPerformanceNightVentilation:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        fan_name: str,
        fan_total_efficiency: float,
        pressure_rise: float,
        motor_efficiency: float,
        maximum_flow_rate: float | Literal["Autosize"] | None = ...,
        motor_in_airstream_fraction: float | None = 1,
    ) -> None:
        """Create a new ``FanPerformance:NightVentilation`` and add it to the document.

        Specifies an alternate set of performance parameters for a fan. These alternate parameters are used when a system manager (such as AvailabilityManager:NightVentilation) sets a specified flow rate. May be used with Fan:ConstantVolume, Fan:VariableVolume, Fan:ZoneExhaust, and Fan:OnOff (not Fan:ComponentModel). Fan:SystemModel has its own night ventilation settings. If the fan model senses that a fixed flow rate has been set, it will use these alternate performance parameters. It is assumed that the fan will run at a fixed speed in the alternate mode.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-fans/#fanperformancenightventilation
        """

class CoilSystemCoolingDXHeatExchangerAssisted:
    def __call__(
        self,
        name: str,
        /,
        *,
        heat_exchanger_object_type: Literal[
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
            "HeatExchanger:Desiccant:BalancedFlow",
        ],
        heat_exchanger_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX", "Coil:Cooling:DX:SingleSpeed", "Coil:Cooling:DX:VariableSpeed"
        ],
        cooling_coil_name: str,
    ) -> None:
        """Create a new ``CoilSystem:Cooling:DX:HeatExchangerAssisted`` and add it to the document.

        Virtual component consisting of a direct expansion (DX) cooling coil and an air-to-air heat exchanger. The air-to-air heat exchanger precools the air entering the cooling coil and reuses this energy to reheat the supply air leaving the cooling coil. This heat exchange process improves the latent removal performance of the cooling coil (lower sensible heat ratio).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilsystemcoolingdxheatexchangerassisted
        """

class PipingSystemUndergroundPipeCircuit:
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

class HeatPumpWaterToWaterEquationFitCooling:
    def __call__(
        self,
        name: str,
        /,
        *,
        source_side_inlet_node_name: str,
        source_side_outlet_node_name: str,
        load_side_inlet_node_name: str,
        load_side_outlet_node_name: str,
        reference_load_side_flow_rate: float | Literal["Autosize"],
        reference_source_side_flow_rate: float | Literal["Autosize"],
        reference_cooling_capacity: float | Literal["Autosize"],
        reference_cooling_power_consumption: float | Literal["Autosize"],
        cooling_capacity_curve_name: str,
        cooling_compressor_power_curve_name: str,
        reference_coefficient_of_performance: float | None = 8,
        sizing_factor: float | None = 1,
        companion_heating_heat_pump_name: str | None = ...,
    ) -> None:
        """Create a new ``HeatPump:WaterToWater:EquationFit:Cooling`` and add it to the document.

        simple water-water heat pump curve-fit model

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#heatpumpwatertowaterequationfitcooling
        """

class ThermalStoragePCM:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str,
        plant_side_inlet_node_name: str,
        plant_side_outlet_node_name: str,
        use_side_inlet_node_name: str,
        use_side_outlet_node_name: str,
        pcm_material_name: str,
        tank_capacity: float | Literal["Autosize"],
        use_side_design_flow_rate: float | Literal["Autosize"],
        plant_side_design_flow_rate: float | Literal["Autosize"],
        heat_loss_rate: float | None = 0,
    ) -> None:
        """Create a new ``ThermalStorage:PCM`` and add it to the document.

        This thermal storage model is PCM-based It requires PCM material property connection In addition to the object linking, this object needs PCM Latent heat storage capacity and Heat Loss Rate This model needs 4 nodes: 2 plant side nodes and 2 use side nodes.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-heaters/#thermalstoragepcm
        """
