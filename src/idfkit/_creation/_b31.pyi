"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class Version:
    def __call__(self, /, *, version_identifier: str | None = ...) -> None:
        """Create a new ``Version`` and add it to the document.

        Specifies the EnergyPlus version of the IDF file.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#version
        """

class HVACSystemRootFindingAlgorithm:
    def __call__(
        self,
        /,
        *,
        algorithm: Literal[
            "", "Alternation", "Bisection", "BisectionThenRegulaFalsi", "RegulaFalsi", "RegulaFalsiThenBisection"
        ]
        | None = "RegulaFalsi",
        number_of_iterations_before_algorithm_switch: int | None = 5,
    ) -> None:
        """Create a new ``HVACSystemRootFindingAlgorithm`` and add it to the document.

        Specifies a HVAC system solver algorithm to find a root

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#hvacsystemrootfindingalgorithm
        """

class SiteGroundTemperatureUndisturbedFiniteDifference:
    def __call__(
        self,
        name: str,
        /,
        *,
        soil_thermal_conductivity: float,
        soil_density: float,
        soil_specific_heat: float,
        soil_moisture_content_volume_fraction: float | None = 30,
        soil_moisture_content_volume_fraction_at_saturation: float | None = 50,
        evapotranspiration_ground_cover_parameter: float | None = 0.4,
    ) -> None:
        """Create a new ``Site:GroundTemperature:Undisturbed:FiniteDifference`` and add it to the document.

        Undisturbed ground temperature object using a detailed finite difference 1-D model

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitegroundtemperatureundisturbedfinitedifference
        """

class SiteGroundDomainSlab:
    def __call__(
        self,
        name: str,
        /,
        *,
        undisturbed_ground_temperature_model_type: Literal[
            "Site:GroundTemperature:Undisturbed:FiniteDifference",
            "Site:GroundTemperature:Undisturbed:KusudaAchenbach",
            "Site:GroundTemperature:Undisturbed:Xing",
        ],
        undisturbed_ground_temperature_model_name: str,
        slab_boundary_condition_model_name: str,
        slab_location: Literal["InGrade", "OnGrade"],
        ground_domain_depth: float | None = 10,
        aspect_ratio: float | None = 1,
        perimeter_offset: float | None = 5,
        soil_thermal_conductivity: float | None = 1.5,
        soil_density: float | None = 2800,
        soil_specific_heat: float | None = 850,
        soil_moisture_content_volume_fraction: float | None = 30,
        soil_moisture_content_volume_fraction_at_saturation: float | None = 50,
        evapotranspiration_ground_cover_parameter: float | None = 0.4,
        slab_material_name: str | None = ...,
        horizontal_insulation: Literal["", "No", "Yes"] | None = "No",
        horizontal_insulation_material_name: str | None = ...,
        horizontal_insulation_extents: Literal["", "Full", "Perimeter"] | None = "Full",
        perimeter_insulation_width: float | None = ...,
        vertical_insulation: Literal["", "No", "Yes"] | None = "No",
        vertical_insulation_material_name: str | None = ...,
        vertical_insulation_depth: float | None = ...,
        simulation_timestep: Literal["", "Hourly", "Timestep"] | None = "Hourly",
        geometric_mesh_coefficient: float | None = 1.6,
        mesh_density_parameter: int | None = 6,
    ) -> None:
        """Create a new ``Site:GroundDomain:Slab`` and add it to the document.

        Ground-coupled slab model for on-grade and in-grade cases with or without insulation.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitegrounddomainslab
        """

class ScheduleConstant:
    def __call__(
        self, name: str, /, *, schedule_type_limits_name: str | None = ..., hourly_value: float | None = 0
    ) -> None:
        """Create a new ``Schedule:Constant`` and add it to the document.

        Constant hourly value for entire year.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#scheduleconstant
        """

class WindowMaterialGasMixture:
    def __call__(
        self,
        name: str,
        /,
        *,
        thickness: float,
        number_of_gases_in_mixture: int,
        gas_1_type: Literal["Air", "Argon", "Krypton", "Xenon"],
        gas_1_fraction: float,
        gas_2_type: Literal["Air", "Argon", "Krypton", "Xenon"],
        gas_2_fraction: float,
        gas_3_type: Literal["Air", "Argon", "Krypton", "Xenon"] | None = ...,
        gas_3_fraction: float | None = ...,
        gas_4_type: Literal["Air", "Argon", "Krypton", "Xenon"] | None = ...,
        gas_4_fraction: float | None = ...,
    ) -> None:
        """Create a new ``WindowMaterial:GasMixture`` and add it to the document.

        Gas mixtures that are used in Windows or Glass Doors

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialgasmixture
        """

class MaterialPropertyMoisturePenetrationDepthSettings:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_vapor_diffusion_resistance_factor: float,
        moisture_equation_coefficient_a: float,
        moisture_equation_coefficient_b: float,
        moisture_equation_coefficient_c: float,
        moisture_equation_coefficient_d: float,
        coating_layer_thickness: float,
        coating_layer_water_vapor_diffusion_resistance_factor: float,
        surface_layer_penetration_depth: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        deep_layer_penetration_depth: float | Literal["", "Autocalculate"] | None = "Autocalculate",
    ) -> None:
        """Create a new ``MaterialProperty:MoisturePenetrationDepth:Settings`` and add it to the document.

        Additional properties for moisture using EMPD procedure HeatBalanceAlgorithm choice=MoisturePenetrationDepthConductionTransferFunction only Has no effect with other HeatBalanceAlgorithm solution algorithms

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertymoisturepenetrationdepthsettings
        """

class GroundHeatTransferSlabManualGrid:
    def __call__(
        self,
        /,
        *,
        nx_number_of_cells_in_the_x_direction: float,
        ny_number_of_cells_in_the_y_direction: float,
        nz_number_of_cells_in_the_z_direction: float,
        ibox_x_direction_cell_indicator_of_slab_edge: float,
        jbox_y_direction_cell_indicator_of_slab_edge: float,
    ) -> None:
        """Create a new ``GroundHeatTransfer:Slab:ManualGrid`` and add it to the document.

        Manual Grid only necessary when using manual gridding (not recommended) Used only in special cases when previous two objects are not used. User must input complete gridding information.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferslabmanualgrid
        """

class AnyRoomAirTemperaturePatternConstantGradient:
    def __call__(
        self,
        /,
        *,
        room_air_temperature_pattern_constant_gradient_name: str,
        control_integer_for_pattern_control_schedule_name: int,
        thermostat_offset: float | None = ...,
        return_air_offset: float | None = ...,
        exhaust_air_offset: float | None = ...,
        temperature_gradient: float | None = ...,
    ) -> None:
        """Create a new ``RoomAir:TemperaturePattern:ConstantGradient`` and add it to the document.

        Used to model room air with a fixed temperature gradient in the vertical direction. Used in combination with RoomAir:TemperaturePattern:UserDefined.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairtemperaturepatternconstantgradient
        """

class RoomAirSettingsAirflowNetwork:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        control_point_roomairflownetwork_node_name: str | None = ...,
        nodes: list[_g.RoomAirSettingsAirflowNetworkNodesItem] = ...,
    ) -> None:
        """Create a new ``RoomAirSettings:AirflowNetwork`` and add it to the document.

        RoomAir modeling using Airflow pressure network solver

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairsettingsairflownetwork
        """

class AnySteamEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        schedule_name: str,
        design_level_calculation_method: Literal[
            "", "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``SteamEquipment`` and add it to the document.

        Sets internal gains for steam equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        No call suits every release: narrow the document with ``as_version`` first.
        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#steamequipment
        """

class ZoneContaminantSourceAndSinkGenericCutoffModel:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        schedule_name: str,
        design_generation_rate_coefficient: float | None = ...,
        cutoff_generic_contaminant_at_which_emission_ceases: float | None = ...,
    ) -> None:
        """Create a new ``ZoneContaminantSourceAndSink:Generic:CutoffModel`` and add it to the document.

        Simulate generic contaminant source driven by the cutoff concentration model.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#zonecontaminantsourceandsinkgenericcutoffmodel
        """

class AnyZoneInfiltrationFlowCoefficient:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        schedule_name: str,
        flow_coefficient: float,
        stack_coefficient: float,
        wind_coefficient: float,
        shelter_factor: float,
        pressure_exponent: float | None = 0.67,
    ) -> None:
        """Create a new ``ZoneInfiltration:FlowCoefficient`` and add it to the document.

        Infiltration is specified as flow coefficient, schedule fraction, stack and wind coefficients, and is a function of temperature difference and wind speed: Infiltration=FSchedule * SQRT( (c * Cs*|(Tzone-Todb)|**n)**2 + (c* Cw*(s * WindSpd)**2n)**2 ) If a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        No call suits every release: narrow the document with ``as_version`` first.
        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zoneinfiltrationflowcoefficient
        """

class AnyZoneEarthtube:
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zoneearthtube
        """

class AirflowNetworkDistributionComponentFan:
    def __call__(
        self,
        /,
        *,
        fan_name: str,
        supply_fan_object_type: Literal["", "Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel", "Fan:VariableVolume"]
        | None = "Fan:ConstantVolume",
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:Component:Fan`` and add it to the document.

        This object defines the name of the supply Air Fan used in an Air loop.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkdistributioncomponentfan
        """

class AirflowNetworkDistributionComponentCoil:
    def __call__(
        self,
        /,
        *,
        coil_name: str,
        coil_object_type: Literal[
            "Coil:Cooling:DX",
            "Coil:Cooling:DX:MultiSpeed",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:TwoSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Cooling:WaterToAirHeatPump:EquationFit",
            "Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit",
            "Coil:Heating:DX:MultiSpeed",
            "Coil:Heating:DX:SingleSpeed",
            "Coil:Heating:DX:VariableSpeed",
            "Coil:Heating:Desuperheater",
            "Coil:Heating:Electric",
            "Coil:Heating:Electric:MultiStage",
            "Coil:Heating:Fuel",
            "Coil:Heating:Gas:MultiStage",
            "Coil:Heating:Water",
            "Coil:Heating:WaterToAirHeatPump:EquationFit",
            "Coil:Heating:WaterToAirHeatPump:VariableSpeedEquationFit",
        ],
        air_path_length: float,
        air_path_hydraulic_diameter: float,
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:Component:Coil`` and add it to the document.

        This object defines the name of a coil used in an air loop.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkdistributioncomponentcoil
        """

class AirflowNetworkDistributionComponentOutdoorAirFlow:
    def __call__(
        self,
        name: str,
        /,
        *,
        outdoor_air_mixer_name: str,
        air_mass_flow_coefficient_when_no_outdoor_air_flow_at_reference_conditions: float,
        air_mass_flow_exponent_when_no_outdoor_air_flow: float | None = 0.65,
        reference_crack_conditions: str | None = ...,
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:Component:OutdoorAirFlow`` and add it to the document.

        This object includes the outdoor air flow rate set by the Controller:OutdoorAir object in the airflow network.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkdistributioncomponentoutdoorairflow
        """

class AnyZoneHVACIdealLoadsAirSystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_supply_air_node_name: str,
        availability_schedule_name: str | None = ...,
        zone_exhaust_air_node_name: str | None = ...,
        system_inlet_air_node_name: str | None = ...,
        maximum_heating_supply_air_temperature: float | None = 50,
        minimum_cooling_supply_air_temperature: float | None = 13,
        maximum_heating_supply_air_humidity_ratio: float | None = 0.0156,
        minimum_cooling_supply_air_humidity_ratio: float | None = 0.0077,
        heating_limit: Literal["", "LimitCapacity", "LimitFlowRate", "LimitFlowRateAndCapacity", "NoLimit"]
        | None = "NoLimit",
        maximum_heating_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_sensible_heating_capacity: float | Literal["Autosize"] | None = ...,
        cooling_limit: Literal["", "LimitCapacity", "LimitFlowRate", "LimitFlowRateAndCapacity", "NoLimit"]
        | None = "NoLimit",
        maximum_cooling_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_total_cooling_capacity: float | Literal["Autosize"] | None = ...,
        heating_availability_schedule_name: str | None = ...,
        cooling_availability_schedule_name: str | None = ...,
        dehumidification_control_type: Literal[
            "", "ConstantSensibleHeatRatio", "ConstantSupplyHumidityRatio", "Humidistat", "None"
        ]
        | None = "ConstantSensibleHeatRatio",
        cooling_sensible_heat_ratio: float | None = 0.7,
        humidification_control_type: Literal["", "ConstantSupplyHumidityRatio", "Humidistat", "None"] | None = "None",
        design_specification_outdoor_air_object_name: str | None = ...,
        outdoor_air_inlet_node_name: str | None = ...,
        demand_controlled_ventilation_type: Literal["", "CO2Setpoint", "None", "OccupancySchedule"] | None = "None",
        outdoor_air_economizer_type: Literal["", "DifferentialDryBulb", "DifferentialEnthalpy", "NoEconomizer"]
        | None = "NoEconomizer",
        heat_recovery_type: Literal["", "Enthalpy", "None", "Sensible"] | None = "None",
        sensible_heat_recovery_effectiveness: float | None = 0.7,
        latent_heat_recovery_effectiveness: float | None = 0.65,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:IdealLoadsAirSystem`` and add it to the document.

        Ideal system used to calculate loads without modeling a full HVAC system. All that is required for the ideal system are zone controls, zone equipment configurations, and the ideal loads system component. This component can be thought of as an ideal unit that mixes zone air with the specified amount of outdoor air and then adds or removes heat and moisture at 100% efficiency in order to meet the specified controls. Energy use is reported as DistrictHeatingWater and DistrictCooling.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacidealloadsairsystem
        """

class AnyZoneHVACBaseboardRadiantConvectiveSteam:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        inlet_node_name: str,
        outlet_node_name: str,
        maximum_steam_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        heating_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        degree_of_subcooling: float | None = 5,
        surface_fractions: list[_g.ZoneHVACBaseboardRadiantConvectiveSteamSurfaceFractionsItem] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:Baseboard:RadiantConvective:Steam`` and add it to the document.

        The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list.

        No call suits every release: narrow the document with ``as_version`` first.
        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvacbaseboardradiantconvectivesteam
        """

class ZoneHVACLowTemperatureRadiantVariableFlow:
    def __call__(
        self,
        name: str,
        /,
        *,
        design_object: str,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        surface_name_or_radiant_surface_group_name: str | None = ...,
        hydronic_tubing_length: float | Literal["", "Autosize"] | None = "Autosize",
        heating_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_hot_water_flow: float | Literal["Autosize"] | None = ...,
        heating_water_inlet_node_name: str | None = ...,
        heating_water_outlet_node_name: str | None = ...,
        cooling_design_capacity: float | Literal["Autosize"] | None = ...,
        maximum_cold_water_flow: float | Literal["Autosize"] | None = ...,
        cooling_water_inlet_node_name: str | None = ...,
        cooling_water_outlet_node_name: str | None = ...,
        number_of_circuits: Literal["", "CalculateFromCircuitLength", "OnePerSurface"] | None = "OnePerSurface",
        circuit_length: float | None = 106.7,
    ) -> None:
        """Create a new ``ZoneHVAC:LowTemperatureRadiant:VariableFlow`` and add it to the document.

        Low temperature hydronic radiant heating and/or cooling system embedded in a building surface (wall, ceiling, or floor). Controlled by varying the hot or chilled water flow to the unit.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvaclowtemperatureradiantvariableflow
        """

class AirTerminalSingleDuctVAVNoReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_outlet_node_name: str,
        air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        zone_minimum_air_flow_input_method: Literal["", "Constant", "FixedFlowRate", "Scheduled"] | None = "Constant",
        constant_minimum_air_flow_fraction: float | Literal["", "Autosize"] | None = "Autosize",
        fixed_minimum_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_air_flow_fraction_schedule_name: str | None = ...,
        design_specification_outdoor_air_object_name: str | None = ...,
        minimum_air_flow_turndown_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:VAV:NoReheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume, with no reheat coil.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-hvac-air-loop-terminal-units/#airterminalsingleductvavnoreheat
        """

class CoilCoolingDXTwoSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        high_speed_gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        high_speed_rated_sensible_heat_ratio: float | Literal["Autosize"],
        high_speed_rated_air_flow_rate: float | Literal["Autosize"],
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        total_cooling_capacity_function_of_temperature_curve_name: str,
        total_cooling_capacity_function_of_flow_fraction_curve_name: str,
        energy_input_ratio_function_of_temperature_curve_name: str,
        energy_input_ratio_function_of_flow_fraction_curve_name: str,
        part_load_fraction_correlation_curve_name: str,
        low_speed_gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        low_speed_gross_rated_sensible_heat_ratio: float | Literal["Autosize"],
        low_speed_rated_air_flow_rate: float | Literal["Autosize"],
        low_speed_total_cooling_capacity_function_of_temperature_curve_name: str,
        low_speed_energy_input_ratio_function_of_temperature_curve_name: str,
        availability_schedule_name: str | None = ...,
        high_speed_gross_rated_cooling_cop: float | None = 3,
        high_speed_2017_rated_evaporator_fan_power_per_volume_flow_rate: float | None = 773.3,
        high_speed_2023_rated_evaporator_fan_power_per_volume_flow_rate: float | None = 934.4,
        unit_internal_static_air_pressure: float | None = ...,
        low_speed_gross_rated_cooling_cop: float | None = 3,
        low_speed_2017_rated_evaporator_fan_power_per_volume_flow_rate: float | None = 773.3,
        low_speed_2023_rated_evaporator_fan_power_per_volume_flow_rate: float | None = 934.4,
        condenser_air_inlet_node_name: str | None = ...,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -25,
        high_speed_evaporative_condenser_effectiveness: float | None = 0.9,
        high_speed_evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        high_speed_evaporative_condenser_pump_rated_power_consumption: float | Literal["Autosize"] | None = ...,
        low_speed_evaporative_condenser_effectiveness: float | None = 0.9,
        low_speed_evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        low_speed_evaporative_condenser_pump_rated_power_consumption: float | Literal["Autosize"] | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        condensate_collection_water_storage_tank_name: str | None = ...,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        sensible_heat_ratio_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        low_speed_sensible_heat_ratio_function_of_temperature_curve_name: str | None = ...,
        low_speed_sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        zone_name_for_condenser_placement: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:TwoSpeed`` and add it to the document.

        Direct expansion (DX) cooling coil and condensing unit (includes electric compressor and condenser fan), two-speed (or variable-speed). Requires two sets of performance data and will interpolate between speeds. Modeled as a single coil (multi-speed compressor or multiple compressors with row split or intertwined coil).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxtwospeed
        """

class EvaporativeCoolerIndirectWetCoil:
    def __call__(
        self,
        name: str,
        /,
        *,
        coil_maximum_efficiency: float,
        recirculating_water_pump_power_consumption: float,
        secondary_air_fan_flow_rate: float,
        secondary_air_fan_total_efficiency: float,
        secondary_air_fan_delta_pressure: float,
        primary_air_inlet_node_name: str,
        primary_air_outlet_node_name: str,
        secondary_air_inlet_node_name: str,
        availability_schedule_name: str | None = ...,
        coil_flow_ratio: float | None = ...,
        control_type: str | None = ...,
        water_supply_storage_tank_name: str | None = ...,
    ) -> None:
        """Create a new ``EvaporativeCooler:Indirect:WetCoil`` and add it to the document.

        Indirect evaporative cooler with wetted coil, recirculating water pump, and secondary air fan. This model has no controls other than its availability schedule.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-evaporative-coolers/#evaporativecoolerindirectwetcoil
        """

class AnyHeatExchangerAirToAirSensibleAndLatent:
    def __call__(
        self,
        name: str,
        /,
        *,
        nominal_supply_air_flow_rate: float | Literal["Autosize"],
        supply_air_inlet_node_name: str,
        supply_air_outlet_node_name: str,
        exhaust_air_inlet_node_name: str,
        exhaust_air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        sensible_effectiveness_at_100_heating_air_flow: float | None = 0,
        latent_effectiveness_at_100_heating_air_flow: float | None = 0,
        sensible_effectiveness_at_100_cooling_air_flow: float | None = 0,
        latent_effectiveness_at_100_cooling_air_flow: float | None = 0,
        nominal_electric_power: float | None = 0,
        supply_air_outlet_temperature_control: Literal["", "No", "Yes"] | None = "No",
        heat_exchanger_type: Literal["", "Plate", "Rotary"] | None = "Plate",
        frost_control_type: Literal["", "ExhaustAirRecirculation", "ExhaustOnly", "MinimumExhaustTemperature", "None"]
        | None = "None",
        threshold_temperature: float | None = 1.7,
        initial_defrost_time_fraction: float | None = 0.083,
        rate_of_defrost_time_fraction_increase: float | None = 0.012,
        economizer_lockout: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``HeatExchanger:AirToAir:SensibleAndLatent`` and add it to the document.

        This object models an air-to-air heat exchanger using effectiveness relationships. The heat exchanger can transfer sensible energy, latent energy, or both between the supply (primary) and exhaust (secondary) air streams.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heat-recovery/#heatexchangerairtoairsensibleandlatent
        """

class AnyAirLoopHVACDedicatedOutdoorAirSystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        airloophvac_mixer_name: str,
        airloophvac_splitter_name: str,
        preheat_design_temperature: float,
        preheat_design_humidity_ratio: float,
        precool_design_temperature: float,
        precool_design_humidity_ratio: float,
        number_of_airloophvac: int,
        airloophvac_outdoorairsystem_name: str | None = ...,
        availability_schedule_name: str | None = ...,
        airloophvacs: list[_g.AirLoopHVACDedicatedOutdoorAirSystemAirloophvacsItem] = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:DedicatedOutdoorAirSystem`` and add it to the document.

        Defines a central forced air system to provide dedicated outdoor air to multiple AirLoopHVACs.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-path/#airloophvacdedicatedoutdoorairsystem
        """

class AnyPipingSystemUndergroundDomain:
    def __call__(
        self,
        name: str,
        /,
        *,
        xmax: float,
        ymax: float,
        zmax: float,
        x_direction_mesh_type: Literal["SymmetricGeometric", "Uniform"],
        y_direction_mesh_type: Literal["SymmetricGeometric", "Uniform"],
        z_direction_mesh_type: Literal["SymmetricGeometric", "Uniform"],
        soil_thermal_conductivity: float,
        soil_density: float,
        soil_specific_heat: float,
        undisturbed_ground_temperature_model_type: Literal[
            "Site:GroundTemperature:Undisturbed:FiniteDifference",
            "Site:GroundTemperature:Undisturbed:KusudaAchenbach",
            "Site:GroundTemperature:Undisturbed:Xing",
        ],
        undisturbed_ground_temperature_model_name: str,
        number_of_pipe_circuits_entered_for_this_domain: int,
        x_direction_mesh_density_parameter: int | None = 4,
        x_direction_geometric_coefficient: float | None = 1.3,
        y_direction_mesh_density_parameter: int | None = 4,
        y_direction_geometric_coefficient: float | None = 1.3,
        z_direction_mesh_density_parameter: int | None = 4,
        z_direction_geometric_coefficient: float | None = 1.3,
        soil_moisture_content_volume_fraction: float | None = 30,
        soil_moisture_content_volume_fraction_at_saturation: float | None = 50,
        this_domain_includes_basement_surface_interaction: Literal["", "No", "Yes"] | None = "No",
        width_of_basement_floor_in_ground_domain: float | None = ...,
        depth_of_basement_wall_in_ground_domain: float | None = ...,
        shift_pipe_x_coordinates_by_basement_width: Literal["No", "Yes"] | None = ...,
        name_of_basement_wall_boundary_condition_model: str | None = ...,
        name_of_basement_floor_boundary_condition_model: str | None = ...,
        convergence_criterion_for_the_outer_cartesian_domain_iteration_loop: float | None = 0.001,
        maximum_iterations_in_the_outer_cartesian_domain_iteration_loop: int | None = 500,
        evapotranspiration_ground_cover_parameter: float | None = 0.4,
        pipe_circuits: list[_g.PipingSystemUndergroundDomainPipeCircuitsItem] = ...,
    ) -> None:
        """Create a new ``PipingSystem:Underground:Domain`` and add it to the document.

        The ground domain object for underground piping system simulation.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-node-branch-management/#pipingsystemundergrounddomain
        """

class ChillerElectricEIR:
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
        condenser_flow_control: Literal[
            "", "ConstantFlow", "ModulatedChillerPLR", "ModulatedDeltaTemperature", "ModulatedLoopPLR"
        ]
        | None = "ConstantFlow",
        condenser_loop_flow_rate_fraction_function_of_loop_part_load_ratio_curve_name: str | None = ...,
        temperature_difference_across_condenser_schedule_name: str | None = ...,
        condenser_minimum_flow_fraction: float | None = ...,
        thermosiphon_capacity_fraction_curve_name: str | None = ...,
        thermosiphon_minimum_temperature_difference: float | None = 0,
    ) -> None:
        """Create a new ``Chiller:Electric:EIR`` and add it to the document.

        This chiller model is the empirical model from the DOE-2 building Energy simulation program. Chiller performance at off-reference conditions is modeled using three polynomial equations. Three curves objects are required.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#chillerelectriceir
        """

class AnyChillerEngineDriven:
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
        fuel_type: Literal["Diesel", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2"],
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#chillerenginedriven
        """

class AnyCoolingTowerVariableSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        design_water_flow_rate: float | Literal["Autosize"],
        design_air_flow_rate: float | Literal["Autosize"],
        design_fan_power: float | Literal["Autosize"],
        model_type: Literal["", "CoolToolsCrossFlow", "CoolToolsUserDefined", "YorkCalc", "YorkCalcUserDefined"]
        | None = "YorkCalc",
        model_coefficient_name: str | None = ...,
        design_inlet_air_wet_bulb_temperature: float | None = 25.6,
        design_approach_temperature: float | None = 3.9,
        design_range_temperature: float | None = 5.6,
        fan_power_ratio_function_of_air_flow_rate_ratio_curve_name: str | None = ...,
        minimum_air_flow_rate_ratio: float | None = 0.2,
        fraction_of_tower_capacity_in_free_convection_regime: float | None = 0.125,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        evaporation_loss_mode: Literal["LossFactor", "SaturatedExit"] | None = ...,
        evaporation_loss_factor: float | None = 0.2,
        drift_loss_percent: float | None = ...,
        blowdown_calculation_mode: Literal["ConcentrationRatio", "ScheduledRate"] | None = ...,
        blowdown_concentration_ratio: float | None = 3,
        blowdown_makeup_water_usage_schedule_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        outdoor_air_inlet_node_name: str | None = ...,
        number_of_cells: int | None = 1,
        cell_control: Literal["", "MaximalCell", "MinimalCell"] | None = ...,
        cell_minimum_water_flow_rate_fraction: float | None = 0.33,
        cell_maximum_water_flow_rate_fraction: float | None = 2.5,
        sizing_factor: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``CoolingTower:VariableSpeed`` and add it to the document.

        This open wet tower model is based on purely empirical algorithms derived from manufacturer's performance data or field measurements. The user can select from two existing algorithms (CoolTools or YorkCalc), or they can enter their own correlation for approach temperature by using a variable speed tower model coefficient object. For a multi-cell tower, the capacity and air/water flow rate inputs are for the entire tower.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#coolingtowervariablespeed
        """

class AnyDemandManagerExteriorLights:
    def __call__(
        self,
        name: str,
        /,
        *,
        limit_control: Literal["Fixed", "Off"],
        selection_control: Literal["All", "RotateMany", "RotateOne"],
        availability_schedule_name: str | None = ...,
        minimum_limit_duration: int | None = ...,
        maximum_limit_fraction: float | None = ...,
        limit_step_change: float | None = ...,
        rotation_duration: int | None = ...,
        lights: list[_g.DemandManagerExteriorLightsLightsItem] = ...,
    ) -> None:
        """Create a new ``DemandManager:ExteriorLights`` and add it to the document.

        used for demand limiting Exterior:Lights objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-demand-limiting-controls/#demandmanagerexteriorlights
        """

class PhotovoltaicPerformanceEquivalentOneDiode:
    def __call__(
        self,
        name: str,
        /,
        *,
        cell_type: Literal["AmorphousSilicon", "CrystallineSilicon"] | None = ...,
        number_of_cells_in_series: int | None = 36,
        active_area: float | None = 0.89,
        transmittance_absorptance_product: float | None = 0.95,
        semiconductor_bandgap: float | None = 1.12,
        shunt_resistance: float | None = 1000000,
        short_circuit_current: float | None = 6.5,
        open_circuit_voltage: float | None = 21.6,
        reference_temperature: float | None = 25,
        reference_insolation: float | None = 1000,
        module_current_at_maximum_power: float | None = 5.9,
        module_voltage_at_maximum_power: float | None = 17,
        temperature_coefficient_of_short_circuit_current: float | None = 0.02,
        temperature_coefficient_of_open_circuit_voltage: float | None = -0.079,
        nominal_operating_cell_temperature_test_ambient_temperature: float | None = 20,
        nominal_operating_cell_temperature_test_cell_temperature: float | None = 40,
        nominal_operating_cell_temperature_test_insolation: float | None = 800,
        module_heat_loss_coefficient: float | None = 30,
        total_heat_capacity: float | None = 50000,
    ) -> None:
        """Create a new ``PhotovoltaicPerformance:EquivalentOne-Diode`` and add it to the document.

        Describes the performance characteristics of Photovoltaic (PV) modules to be modeled using an equivalent one-diode circuit. This model is also known as the 4- or 5-parameter TRNSYS model for photovoltaics.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#photovoltaicperformanceequivalentone-diode
        """

class ElectricLoadCenterInverterFunctionOfPower:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        radiative_fraction: float | None = ...,
        efficiency_function_of_power_curve_name: str | None = ...,
        rated_maximum_continuous_input_power: float | None = ...,
        minimum_efficiency: float | None = ...,
        maximum_efficiency: float | None = ...,
        minimum_power_output: float | None = ...,
        maximum_power_output: float | None = ...,
        ancillary_power_consumed_in_standby: float | None = ...,
    ) -> None:
        """Create a new ``ElectricLoadCenter:Inverter:FunctionOfPower`` and add it to the document.

        Electric power inverter to convert from direct current (DC) to alternating current (AC) in an electric load center that contains photovoltaic modules. This input object is for an inverter model where efficiency is a function of normalized power.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#electricloadcenterinverterfunctionofpower
        """

class FaultModelThermostatOffset:
    def __call__(
        self,
        name: str,
        /,
        *,
        thermostat_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        reference_thermostat_offset: float | None = 2,
    ) -> None:
        """Create a new ``FaultModel:ThermostatOffset`` and add it to the document.

        This object describes fault of thermostat offset

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-operational-faults/#faultmodelthermostatoffset
        """

class AnyMatrixTwoDimension:
    def __call__(
        self,
        name: str,
        /,
        *,
        number_of_rows: int,
        number_of_columns: int,
        values: list[_g.MatrixTwoDimensionValuesItem] = ...,
    ) -> None:
        """Create a new ``Matrix:TwoDimension`` and add it to the document.

        matrix data in row-major order list each row keeping the columns in order number of values must equal N1 x N2

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#matrixtwodimension
        """
