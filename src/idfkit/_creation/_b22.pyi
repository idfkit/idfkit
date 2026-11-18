"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class Construction:
    def __call__(
        self,
        name: str,
        /,
        *,
        outside_layer: str,
        layer_2: str | None = ...,
        layer_3: str | None = ...,
        layer_4: str | None = ...,
        layer_5: str | None = ...,
        layer_6: str | None = ...,
        layer_7: str | None = ...,
        layer_8: str | None = ...,
        layer_9: str | None = ...,
        layer_10: str | None = ...,
    ) -> None:
        """Create a new ``Construction`` and add it to the document.

        Start with outside layer and work your way to the inside layer Up to 10 layers total, 8 for windows Enter the material name for each layer

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/cost-estimating/#construction
        """

class AnyRoof:
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
        """Create a new ``Roof`` and add it to the document.

        Allows for simplified entry of roofs (exterior). View Factor to Ground is automatically calculated.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#roof
        """

class AnyHotWaterEquipment:
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
        """Create a new ``HotWaterEquipment`` and add it to the document.

        Sets internal gains for hot water equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#hotwaterequipment
        """

class SpaceHVACEquipmentConnections:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        space_name: str,
        space_air_node_name: str,
        space_air_inlet_node_or_nodelist_name: str | None = ...,
        space_air_exhaust_node_or_nodelist_name: str | None = ...,
        space_return_air_node_or_nodelist_name: str | None = ...,
        space_return_air_node_1_flow_rate_fraction_schedule_name: str | None = ...,
        space_return_air_node_1_flow_rate_basis_node_or_nodelist_name: str | None = ...,
    ) -> None:
        """Create a new ``SpaceHVAC:EquipmentConnections`` and add it to the document.

        Specifies the HVAC equipment connections for a space. Node names are specified for the space air node, air inlet nodes, air exhaust nodes, and the air return node. If any space in a zone has a SpaceHVAC:EquipmentConnections object, then all spaces in the zone must have one. Used only when ZoneAirHeatBalanceAlgorithm 'Do Space Heat Balance for Simulation' is Yes.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-equipment/#spacehvacequipmentconnections
        """

class AnyCoolingTowerTwoSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        high_fan_speed_air_flow_rate: float | Literal["Autosize"],
        high_fan_speed_fan_power: float | Literal["Autosize"],
        low_fan_speed_air_flow_rate: float | Literal["Autocalculate"],
        low_fan_speed_fan_power: float | Literal["Autocalculate"],
        design_water_flow_rate: float | Literal["Autosize"] | None = ...,
        high_fan_speed_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        low_fan_speed_air_flow_rate_sizing_factor: float | None = 0.5,
        low_fan_speed_fan_power_sizing_factor: float | None = 0.16,
        low_fan_speed_u_factor_times_area_value: float | Literal["Autocalculate"] | None = ...,
        low_fan_speed_u_factor_times_area_sizing_factor: float | None = 0.6,
        free_convection_regime_air_flow_rate: float | Literal["Autocalculate"] | None = 0,
        free_convection_regime_air_flow_rate_sizing_factor: float | None = 0.1,
        free_convection_regime_u_factor_times_area_value: float | Literal["Autocalculate"] | None = 0,
        free_convection_u_factor_times_area_value_sizing_factor: float | None = 0.1,
        performance_input_method: Literal["NominalCapacity", "UFactorTimesAreaAndDesignWaterFlowRate"]
        | None = "UFactorTimesAreaAndDesignWaterFlowRate",
        heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None = 1.25,
        high_speed_nominal_capacity: float | None = ...,
        low_speed_nominal_capacity: float | Literal["Autocalculate"] | None = ...,
        low_speed_nominal_capacity_sizing_factor: float | None = 0.5,
        free_convection_nominal_capacity: float | Literal["Autocalculate"] | None = ...,
        free_convection_nominal_capacity_sizing_factor: float | None = 0.1,
        design_inlet_air_dry_bulb_temperature: float | None = 35,
        design_inlet_air_wet_bulb_temperature: float | None = 25.6,
        design_approach_temperature: float | Literal["Autosize"] | None = "Autosize",
        design_range_temperature: float | Literal["Autosize"] | None = "Autosize",
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        evaporation_loss_mode: Literal["LossFactor", "SaturatedExit"] | None = ...,
        evaporation_loss_factor: float | None = 0.2,
        drift_loss_percent: float | None = 0.008,
        blowdown_calculation_mode: Literal["ConcentrationRatio", "ScheduledRate"] | None = ...,
        blowdown_concentration_ratio: float | None = 3,
        blowdown_makeup_water_usage_schedule_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        outdoor_air_inlet_node_name: str | None = ...,
        number_of_cells: int | None = 1,
        cell_control: Literal["MaximalCell", "MinimalCell"] | None = ...,
        cell_minimum_water_flow_rate_fraction: float | None = 0.33,
        cell_maximum_water_flow_rate_fraction: float | None = 2.5,
        sizing_factor: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``CoolingTower:TwoSpeed`` and add it to the document.

        This tower model is based on Merkel's theory, which is also the basis for the tower model in ASHRAE's HVAC1 Toolkit. The open wet cooling tower is modeled as a counter flow heat exchanger with a two-speed fan drawing air through the tower (induced-draft configuration). For a multi-cell tower, the capacity and air/water flow rate inputs are for the entire tower.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#coolingtowertwospeed
        """

class WaterHeaterMixed:
    def __call__(
        self,
        name: str,
        /,
        *,
        setpoint_temperature_schedule_name: str,
        heater_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ],
        heater_thermal_efficiency: float,
        ambient_temperature_indicator: Literal["Outdoors", "Schedule", "Zone"],
        tank_volume: float | Literal["Autosize"] | None = 0,
        deadband_temperature_difference: float | None = 0,
        maximum_temperature_limit: float | None = ...,
        heater_control_type: Literal["Cycle", "Modulate"] | None = "Cycle",
        heater_maximum_capacity: float | Literal["Autosize"] | None = ...,
        heater_minimum_capacity: float | None = ...,
        heater_ignition_minimum_flow_rate: float | None = 0,
        heater_ignition_delay: float | None = 0,
        part_load_factor_curve_name: str | None = ...,
        off_cycle_parasitic_fuel_consumption_rate: float | None = 0,
        off_cycle_parasitic_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = ...,
        off_cycle_parasitic_heat_fraction_to_tank: float | None = 0,
        on_cycle_parasitic_fuel_consumption_rate: float | None = 0,
        on_cycle_parasitic_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = ...,
        on_cycle_parasitic_heat_fraction_to_tank: float | None = 0,
        ambient_temperature_schedule_name: str | None = ...,
        ambient_temperature_zone_name: str | None = ...,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        off_cycle_loss_coefficient_to_ambient_temperature: float | None = ...,
        off_cycle_loss_fraction_to_zone: float | None = 1,
        on_cycle_loss_coefficient_to_ambient_temperature: float | None = ...,
        on_cycle_loss_fraction_to_zone: float | None = 1,
        peak_use_flow_rate: float | None = ...,
        use_flow_rate_fraction_schedule_name: str | None = ...,
        cold_water_supply_temperature_schedule_name: str | None = ...,
        use_side_inlet_node_name: str | None = ...,
        use_side_outlet_node_name: str | None = ...,
        use_side_effectiveness: float | None = 1,
        source_side_inlet_node_name: str | None = ...,
        source_side_outlet_node_name: str | None = ...,
        source_side_effectiveness: float | None = 1,
        use_side_design_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        source_side_design_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        indirect_water_heating_recovery_time: float | None = 1.5,
        source_side_flow_control_mode: Literal[
            "IndirectHeatAlternateSetpoint", "IndirectHeatPrimarySetpoint", "StorageTank"
        ]
        | None = "IndirectHeatPrimarySetpoint",
        indirect_alternate_setpoint_temperature_schedule_name: str | None = ...,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``WaterHeater:Mixed`` and add it to the document.

        Water heater with well-mixed, single-node water tank. May be used to model a tankless water heater (small tank volume), a hot water storage tank (zero heater capacity), or a heat pump water heater (see WaterHeater:HeatPump:PumpedCondenser.)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-heaters/#waterheatermixed
        """

class CoilUserDefined:
    def __call__(
        self,
        name: str,
        /,
        *,
        model_setup_and_sizing_program_calling_manager_name: str,
        number_of_air_connections: int,
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-user-defined-hvac-and-plant-component/#coiluserdefined
        """

class GeneratorFuelCellStackCooler:
    def __call__(
        self,
        name: str,
        /,
        *,
        heat_recovery_water_inlet_node_name: str | None = ...,
        heat_recovery_water_outlet_node_name: str | None = ...,
        nominal_stack_temperature: float | None = ...,
        actual_stack_temperature: float | None = ...,
        coefficient_r0: float | None = ...,
        coefficient_r1: float | None = ...,
        coefficient_r2: float | None = ...,
        coefficient_r3: float | None = ...,
        stack_coolant_flow_rate: float | None = ...,
        stack_cooler_u_factor_times_area_value: float | None = ...,
        fs_cogen_adjustment_factor: float | None = ...,
        stack_cogeneration_exchanger_area: float | None = ...,
        stack_cogeneration_exchanger_nominal_flow_rate: float | None = ...,
        stack_cogeneration_exchanger_nominal_heat_transfer_coefficient: float | None = ...,
        stack_cogeneration_exchanger_nominal_heat_transfer_coefficient_exponent: float | None = ...,
        stack_cooler_pump_power: float | None = ...,
        stack_cooler_pump_heat_loss_fraction: float | None = ...,
        stack_air_cooler_fan_coefficient_f0: float | None = ...,
        stack_air_cooler_fan_coefficient_f1: float | None = ...,
        stack_air_cooler_fan_coefficient_f2: float | None = ...,
    ) -> None:
        """Create a new ``Generator:FuelCell:StackCooler`` and add it to the document.

        This object is optional and is used to define details needed to model the stack cooler on PEMFC.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatorfuelcellstackcooler
        """
