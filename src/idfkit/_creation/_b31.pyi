"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitegroundtemperatureundisturbedfinitedifference
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
        surface_layer_penetration_depth: float | Literal["Autocalculate"] | None = "Autocalculate",
        deep_layer_penetration_depth: float | Literal["Autocalculate"] | None = "Autocalculate",
    ) -> None:
        """Create a new ``MaterialProperty:MoisturePenetrationDepth:Settings`` and add it to the document.

        Additional properties for moisture using EMPD procedure HeatBalanceAlgorithm choice=MoisturePenetrationDepthConductionTransferFunction only Has no effect with other HeatBalanceAlgorithm solution algorithms

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertymoisturepenetrationdepthsettings
        """

class GroundHeatTransferSlabManualGrid:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
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

class RoomAirSettingsAirflowNetwork:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        control_point_roomairflownetwork_node_name: str | None = ...,
        nodes: Sequence[_g.RoomAirSettingsAirflowNetworkNodesItem | _g.RoomAirSettingsAirflowNetworkNodesGroup] = ...,
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
            "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
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
        this_domain_includes_basement_surface_interaction: Literal["No", "Yes"] | None = "No",
        width_of_basement_floor_in_ground_domain: float | None = ...,
        depth_of_basement_wall_in_ground_domain: float | None = ...,
        shift_pipe_x_coordinates_by_basement_width: Literal["No", "Yes"] | None = ...,
        name_of_basement_wall_boundary_condition_model: str | None = ...,
        name_of_basement_floor_boundary_condition_model: str | None = ...,
        convergence_criterion_for_the_outer_cartesian_domain_iteration_loop: float | None = 0.001,
        maximum_iterations_in_the_outer_cartesian_domain_iteration_loop: int | None = 500,
        evapotranspiration_ground_cover_parameter: float | None = 0.4,
        pipe_circuits: Sequence[
            _g.PipingSystemUndergroundDomainPipeCircuitsItem | _g.PipingSystemUndergroundDomainPipeCircuitsGroup
        ] = ...,
    ) -> None:
        """Create a new ``PipingSystem:Underground:Domain`` and add it to the document.

        The ground domain object for underground piping system simulation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-node-branch-management/#pipingsystemundergrounddomain
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
        condenser_type: Literal["AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
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
        design_heat_recovery_water_flow_rate: float | Literal["Autosize"] | None = 0,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        chiller_flow_mode: Literal["ConstantFlow", "LeavingSetpointModulated", "NotModulated"] | None = "NotModulated",
        maximum_temperature_for_heat_recovery_at_heat_recovery_outlet_node: float | None = 60,
        sizing_factor: float | None = 1,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        condenser_heat_recovery_relative_capacity_fraction: float | None = ...,
    ) -> None:
        """Create a new ``Chiller:EngineDriven`` and add it to the document.

        This chiller model is the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Chiller performance curves are generated by fitting catalog data to third order polynomial equations. Three sets of coefficients are required.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#chillerenginedriven
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#photovoltaicperformanceequivalentone-diode
        """
