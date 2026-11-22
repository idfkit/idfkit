"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class FloorDetailed:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition: Literal[
            "Adiabatic",
            "Foundation",
            "Ground",
            "GroundBasementPreprocessorAverageFloor",
            "GroundBasementPreprocessorAverageWall",
            "GroundBasementPreprocessorLowerWall",
            "GroundBasementPreprocessorUpperWall",
            "GroundFCfactorMethod",
            "GroundSlabPreprocessorAverage",
            "GroundSlabPreprocessorCore",
            "GroundSlabPreprocessorPerimeter",
            "OtherSideCoefficients",
            "OtherSideConditionsModel",
            "Outdoors",
            "Space",
            "Surface",
            "Zone",
        ],
        space_name: str | None = ...,
        outside_boundary_condition_object: str | None = ...,
        sun_exposure: Literal["NoSun", "SunExposed"] | None = "SunExposed",
        wind_exposure: Literal["NoWind", "WindExposed"] | None = "WindExposed",
        view_factor_to_ground: float | Literal["Autocalculate"] | None = "Autocalculate",
        number_of_vertices: float | Literal["Autocalculate"] | None = "Autocalculate",
        vertices: Sequence[_g.FloorDetailedVerticesItem | _g.FloorDetailedVerticesGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Floor:Detailed`` and add it to the document.

        Allows for detailed entry of floor heat transfer surfaces.

        ``vertices`` takes the extensible groups in order, one dict per group:

        ```python
        doc["Floor:Detailed"].add(
            "Floor Detailed 1",
            construction_name="Construction 1",
            zone_name="Zone 1",
            outside_boundary_condition="Adiabatic",
            vertices=[
                {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#floordetailed
        """

class SurfacePropertyConvectionCoefficientsMultipleSurface:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        surface_type: Literal[
            "AllExteriorFloors",
            "AllExteriorRoofs",
            "AllExteriorSurfaces",
            "AllExteriorWalls",
            "AllExteriorWindows",
            "AllInteriorCeilings",
            "AllInteriorFloors",
            "AllInteriorSurfaces",
            "AllInteriorWalls",
            "AllInteriorWindows",
        ],
        convection_coefficient_1_location: Literal["Inside", "Outside"],
        convection_coefficient_1_type: Literal[
            "ASHRAEVerticalWall",
            "ASTMC1340",
            "AdaptiveConvectionAlgorithm",
            "AlamdariHammondStableHorizontal",
            "AlamdariHammondUnstableHorizontal",
            "AlamdariHammondVerticalWall",
            "AwbiHattonHeatedFloor",
            "AwbiHattonHeatedWall",
            "BeausoleilMorrisonMixedAssistedWall",
            "BeausoleilMorrisonMixedOpposingWall",
            "BeausoleilMorrisonMixedStableCeiling",
            "BeausoleilMorrisonMixedStableFloor",
            "BeausoleilMorrisonMixedUnstableCeiling",
            "BeausoleilMorrisonMixedUnstableFloor",
            "BlockenWindard",
            "ClearRoof",
            "DOE-2",
            "EmmelRoof",
            "EmmelVertical",
            "FisherPedersenCeilingDiffuserCeiling",
            "FisherPedersenCeilingDiffuserFloor",
            "FisherPedersenCeilingDiffuserWalls",
            "FohannoPolidoriVerticalWall",
            "GoldsteinNovoselacCeilingDiffuserFloor",
            "GoldsteinNovoselacCeilingDiffuserWalls",
            "GoldsteinNovoselacCeilingDiffuserWindow",
            "ISO15099Windows",
            "KaradagChilledCeiling",
            "KhalifaEq3WallAwayFromHeat",
            "KhalifaEq4CeilingAwayFromHeat",
            "KhalifaEq5WallNearHeat",
            "KhalifaEq6NonHeatedWalls",
            "KhalifaEq7Ceiling",
            "McAdams",
            "Mitchell",
            "MoWitt",
            "NusseltJurges",
            "Schedule",
            "Simple",
            "SimpleCombined",
            "TARP",
            "UserCurve",
            "Value",
            "WaltonStableHorizontalOrTilt",
            "WaltonUnstableHorizontalOrTilt",
        ],
        convection_coefficient_1: float | None = ...,
        convection_coefficient_1_schedule_name: str | None = ...,
        convection_coefficient_1_user_curve_name: str | None = ...,
        convection_coefficient_2_location: Literal["Inside", "Outside"] | None = ...,
        convection_coefficient_2_type: Literal[
            "ASHRAEVerticalWall",
            "ASTMC1340",
            "AdaptiveConvectionAlgorithm",
            "AlamdariHammondStableHorizontal",
            "AlamdariHammondUnstableHorizontal",
            "AlamdariHammondVerticalWall",
            "AwbiHattonHeatedFloor",
            "AwbiHattonHeatedWall",
            "BeausoleilMorrisonMixedAssistedWall",
            "BeausoleilMorrisonMixedOpposingWall",
            "BeausoleilMorrisonMixedStableCeiling",
            "BeausoleilMorrisonMixedStableFloor",
            "BeausoleilMorrisonMixedUnstableCeiling",
            "BeausoleilMorrisonMixedUnstableFloor",
            "BlockenWindard",
            "ClearRoof",
            "DOE-2",
            "EmmelRoof",
            "EmmelVertical",
            "FisherPedersenCeilingDiffuserCeiling",
            "FisherPedersenCeilingDiffuserFloor",
            "FisherPedersenCeilingDiffuserWalls",
            "FohannoPolidoriVerticalWall",
            "GoldsteinNovoselacCeilingDiffuserFloor",
            "GoldsteinNovoselacCeilingDiffuserWalls",
            "GoldsteinNovoselacCeilingDiffuserWindow",
            "ISO15099Windows",
            "KaradagChilledCeiling",
            "KhalifaEq3WallAwayFromHeat",
            "KhalifaEq4CeilingAwayFromHeat",
            "KhalifaEq5WallNearHeat",
            "KhalifaEq6NonHeatedWalls",
            "KhalifaEq7Ceiling",
            "McAdams",
            "Mitchell",
            "MoWitt",
            "NusseltJurges",
            "Schedule",
            "Simple",
            "SimpleCombined",
            "TARP",
            "UserCurve",
            "Value",
            "WaltonStableHorizontalOrTilt",
            "WaltonUnstableHorizontalOrTilt",
        ]
        | None = ...,
        convection_coefficient_2: float | None = 0.1,
        convection_coefficient_2_schedule_name: str | None = ...,
        convection_coefficient_2_user_curve_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``SurfaceProperty:ConvectionCoefficients:MultipleSurface`` and add it to the document.

        Allow user settable interior and/or exterior convection coefficients. Note that some other factors may limit the lower bounds for these values, such as for windows, the interior convection coefficient must be >.28, for trombe wall algorithm selection (zone), the interior convection coefficient must be >.1 for TARP interior convection, the lower limit is also .1 Minimum and maximum limits are set in HeatBalanceAlgorithm object. Defaults in HeatBalanceAlgorithm object are [.1,1000].

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyconvectioncoefficientsmultiplesurface
        """

class AirflowNetworkDistributionComponentTerminalUnit:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        terminal_unit_name: str,
        terminal_unit_object_type: Literal[
            "AirTerminal:SingleDuct:ConstantVolume:Reheat", "AirTerminal:SingleDuct:VAV:Reheat"
        ],
        air_path_length: float,
        air_path_hydraulic_diameter: float,
        validate: bool = True,
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:Component:TerminalUnit`` and add it to the document.

        This object defines the name of a terminal unit in an air loop.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkdistributioncomponentterminalunit
        """

class AnyHVACTemplateSystemUnitarySystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        system_availability_schedule_name: str | None = ...,
        control_type: Literal["Load", "SetPoint"] | None = "Load",
        control_zone_or_thermostat_location_name: str | None = ...,
        cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        heating_supply_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        supply_fan_operating_mode_schedule_name: str | None = ...,
        supply_fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 600,
        supply_fan_motor_efficiency: float | None = 0.9,
        supply_fan_motor_in_air_stream_fraction: float | None = 1,
        cooling_coil_type: Literal[
            "ChilledWater",
            "ChilledWaterDetailedFlatModel",
            "HeatExchangerAssistedChilledWater",
            "HeatExchangerAssistedDX",
            "MultiSpeedDX",
            "None",
            "SingleSpeedDX",
            "SingleSpeedDXWaterCooled",
            "TwoSpeedDX",
            "TwoStageDX",
            "TwoStageHumidityControlDX",
        ]
        | None = "SingleSpeedDX",
        number_of_speeds_for_cooling: int | None = 1,
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_design_supply_air_temperature: float | None = 12.8,
        dx_cooling_coil_gross_rated_total_capacity: float | Literal["Autosize"] | None = "Autosize",
        dx_cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["Autosize"] | None = "Autosize",
        dx_cooling_coil_gross_rated_cop: float | None = 3,
        heating_coil_type: Literal[
            "Electric",
            "Gas",
            "HotWater",
            "MultiSpeedDXHeatPumpAirSource",
            "MultiStageElectric",
            "MultiStageGas",
            "None",
            "SingleSpeedDXHeatPumpAirSource",
            "SingleSpeedDXHeatPumpWaterSource",
        ]
        | None = "Gas",
        number_of_speeds_or_stages_for_heating: int | None = 1,
        heating_coil_availability_schedule_name: str | None = ...,
        heating_design_supply_air_temperature: float | None = 50,
        heating_coil_gross_rated_capacity: float | Literal["Autosize"] | None = "Autosize",
        gas_heating_coil_efficiency: float | None = 0.8,
        gas_heating_coil_parasitic_electric_load: float | None = 0,
        heat_pump_heating_coil_gross_rated_cop: float | None = 2.75,
        heat_pump_heating_minimum_outdoor_dry_bulb_temperature: float | None = -8,
        heat_pump_defrost_maximum_outdoor_dry_bulb_temperature: float | None = 5,
        heat_pump_defrost_strategy: Literal["Resistive", "ReverseCycle"] | None = "ReverseCycle",
        heat_pump_defrost_control: Literal["OnDemand", "Timed"] | None = "Timed",
        heat_pump_defrost_time_period_fraction: float | None = 0.058333,
        supplemental_heating_or_reheat_coil_type: Literal["DesuperHeater", "Electric", "Gas", "HotWater", "None"]
        | None = "None",
        supplemental_heating_or_reheat_coil_availability_schedule_name: str | None = ...,
        supplemental_heating_or_reheat_coil_capacity: float | Literal["Autosize"] | None = "Autosize",
        supplemental_heating_or_reheat_coil_maximum_outdoor_dry_bulb_temperature: float | None = 21,
        supplemental_gas_heating_or_reheat_coil_efficiency: float | None = 0.8,
        supplemental_gas_heating_or_reheat_coil_parasitic_electric_load: float | None = 0,
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
        heat_recovery_type: Literal["Enthalpy", "None", "Sensible"] | None = "None",
        sensible_heat_recovery_effectiveness: float | None = 0.7,
        latent_heat_recovery_effectiveness: float | None = 0.65,
        heat_recovery_heat_exchanger_type: Literal["Plate", "Rotary"] | None = "Plate",
        heat_recovery_frost_control_type: Literal[
            "ExhaustAirRecirculation", "ExhaustOnly", "MinimumExhaustTemperature", "None"
        ]
        | None = "None",
        dehumidification_control_type: Literal["CoolReheat", "Multimode", "None"] | None = "None",
        dehumidification_relative_humidity_setpoint: float | None = 60,
        dehumidification_relative_humidity_setpoint_schedule_name: str | None = ...,
        humidifier_type: Literal["ElectricSteam", "None"] | None = "None",
        humidifier_availability_schedule_name: str | None = ...,
        humidifier_rated_capacity: float | None = ...,
        humidifier_rated_electric_power: float | Literal["Autosize"] | None = "Autosize",
        humidifier_control_zone_name: str | None = ...,
        humidifier_relative_humidity_setpoint: float | None = 30,
        humidifier_relative_humidity_setpoint_schedule_name: str | None = ...,
        sizing_option: Literal["Coincident", "NonCoincident"] | None = "NonCoincident",
        return_fan: Literal["No", "Yes"] | None = "No",
        return_fan_total_efficiency: float | None = 0.7,
        return_fan_delta_pressure: float | None = 300,
        return_fan_motor_efficiency: float | None = 0.9,
        return_fan_motor_in_air_stream_fraction: float | None = 1,
        validate: bool = True,
    ) -> None:
        """Create a new ``HVACTemplate:System:UnitarySystem`` and add it to the document.

        Unitary HVAC system with optional cooling and heating. Supports DX and chilled water, cooling, gas, electric, and hot water heating, air-to-air and water-to-air heat pumps.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatesystemunitarysystem
        """

class ZoneHVACFourPipeFanCoil:
    def __call__(
        self,
        name: str,
        /,
        *,
        capacity_control_method: Literal[
            "ASHRAE90VariableFan",
            "ConstantFanVariableFlow",
            "CyclingFan",
            "MultiSpeedFan",
            "VariableFanConstantFlow",
            "VariableFanVariableFlow",
        ],
        maximum_supply_air_flow_rate: float | Literal["Autosize"],
        maximum_outdoor_air_flow_rate: float | Literal["Autosize"],
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel", "Fan:VariableVolume"],
        supply_air_fan_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "CoilSystem:Cooling:Water:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        maximum_cold_water_flow_rate: float | Literal["Autosize"],
        heating_coil_object_type: Literal["Coil:Heating:Electric", "Coil:Heating:Water"],
        heating_coil_name: str,
        maximum_hot_water_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        low_speed_supply_air_flow_ratio: float | None = 0.33,
        medium_speed_supply_air_flow_ratio: float | None = 0.66,
        outdoor_air_schedule_name: str | None = ...,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outdoor_air_mixer_name: str | None = ...,
        minimum_cold_water_flow_rate: float | None = 0,
        cooling_convergence_tolerance: float | None = 0.001,
        minimum_hot_water_flow_rate: float | None = 0,
        heating_convergence_tolerance: float | None = 0.001,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        minimum_supply_air_temperature_in_cooling_mode: float | Literal["Autosize"] | None = "Autosize",
        maximum_supply_air_temperature_in_heating_mode: float | Literal["Autosize"] | None = "Autosize",
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneHVAC:FourPipeFanCoil`` and add it to the document.

        Four pipe fan coil system. Forced-convection hydronic heating-cooling unit with supply fan, hot water heating coil, chilled water cooling coil, and fixed-position outdoor air mixer.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacfourpipefancoil
        """

class AnyAirTerminalDualDuctVAV:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_outlet_node_name: str,
        hot_air_inlet_node_name: str,
        cold_air_inlet_node_name: str,
        maximum_damper_air_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        zone_minimum_air_flow_fraction: float | None = 0.2,
        design_specification_outdoor_air_object_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``AirTerminal:DualDuct:VAV`` and add it to the document.

        Central air system terminal unit, dual duct, variable volume.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminaldualductvav
        """

class ConnectorMixer:
    def __call__(
        self,
        name: str,
        /,
        *,
        outlet_branch_name: str,
        branches: Sequence[_g.ConnectorMixerBranchesItem | _g.ConnectorMixerBranchesGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Connector:Mixer`` and add it to the document.

        Mix N inlet air/water streams into one. Branch names cannot be duplicated within a single mixer list.

        ``branches`` takes the extensible groups in order, one dict per group:

        ```python
        doc["Connector:Mixer"].add(
            "Connector Mixer 1",
            outlet_branch_name="Outlet Branch 1",
            branches=[
                {"inlet_branch_name": "Inlet Branch 1"},
                {"inlet_branch_name": "Inlet Branch 2"},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-node-branch-management/#connectormixer
        """

class SolarCollectorIntegralCollectorStorage:
    def __call__(
        self,
        name: str,
        /,
        *,
        integralcollectorstorageparameters_name: str,
        surface_name: str,
        inlet_node_name: str,
        outlet_node_name: str,
        bottom_surface_boundary_conditions_type: Literal["AmbientAir", "OtherSideConditionsModel"]
        | None = "AmbientAir",
        boundary_condition_model_name: str | None = ...,
        maximum_flow_rate: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``SolarCollector:IntegralCollectorStorage`` and add it to the document.

        Glazed solar collector with integral storage unit. Thermal and optical properties are taken from the referenced SolarCollectorPerformance:IntegralCollectorStorage object. Collector tilt, azimuth, and gross area are taken from the referenced building surface or shading surface. The collector surface participates normally in all shading calculations.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-solar-collectors/#solarcollectorintegralcollectorstorage
        """

class AnyHeatPumpAirToWaterFuelFiredCooling:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        normalized_capacity_function_of_temperature_curve_name: str,
        fuel_energy_input_ratio_function_of_temperature_curve_name: str,
        fuel_energy_input_ratio_function_of_plr_curve_name: str,
        air_source_node_name: str | None = ...,
        companion_heating_heat_pump_name: str | None = ...,
        fuel_type: Literal[
            "Coal",
            "Diesel",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = "NaturalGas",
        end_use_subcategory: str | None = "General",
        nominal_cooling_capacity: float | Literal["Autosize"] | None = ...,
        nominal_cop: float | None = 1,
        design_flow_rate: float | Literal["Autosize"] | None = ...,
        design_supply_temperature: float | None = 7,
        design_temperature_lift: float | Literal["Autosize"] | None = 11.1,
        sizing_factor: float | None = 1,
        flow_mode: Literal["ConstantFlow", "LeavingSetpointModulated", "NotModulated"] | None = "NotModulated",
        outdoor_air_temperature_curve_input_variable: Literal["DryBulb", "WetBulb"] | None = "DryBulb",
        water_temperature_curve_input_variable: Literal["EnteringEvaporator", "LeavingEvaporator"]
        | None = "EnteringEvaporator",
        minimum_part_load_ratio: float | None = 0.1,
        maximum_part_load_ratio: float | None = 1,
        cycling_ratio_factor_curve_name: str | None = ...,
        nominal_auxiliary_electric_power: float | None = ...,
        auxiliary_electric_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        auxiliary_electric_energy_input_ratio_function_of_plr_curve_name: str | None = ...,
        standby_electric_power: float | None = 0,
        validate: bool = True,
    ) -> None:
        """Create a new ``HeatPump:AirToWater:FuelFired:Cooling`` and add it to the document.

        The object defines a fuel-fired absorption heat pump based on equation-fit models.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-heating-and-cooling-equipment/#heatpumpairtowaterfuelfiredcooling
        """

class AnyGeneratorMicroTurbine:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_electrical_power_output: float,
        reference_electrical_efficiency_using_lower_heating_value: float,
        electrical_power_function_of_temperature_and_elevation_curve_name: str,
        electrical_efficiency_function_of_temperature_curve_name: str,
        electrical_efficiency_function_of_part_load_ratio_curve_name: str,
        minimum_full_load_electrical_power_output: float | None = 0,
        maximum_full_load_electrical_power_output: float | None = ...,
        reference_combustion_air_inlet_temperature: float | None = 15,
        reference_combustion_air_inlet_humidity_ratio: float | None = 0.00638,
        reference_elevation: float | None = 0,
        fuel_type: Literal["NaturalGas"] | None = "NaturalGas",
        fuel_higher_heating_value: float | None = 50000,
        fuel_lower_heating_value: float | None = 45450,
        standby_power: float | None = 0,
        ancillary_power: float | None = 0,
        ancillary_power_function_of_fuel_input_curve_name: str | None = ...,
        heat_recovery_water_inlet_node_name: str | None = ...,
        heat_recovery_water_outlet_node_name: str | None = ...,
        reference_thermal_efficiency_using_lower_heat_value: float | None = 0,
        reference_inlet_water_temperature: float | None = ...,
        heat_recovery_water_flow_operating_mode: Literal["InternalControl", "PlantControl"] | None = "PlantControl",
        reference_heat_recovery_water_flow_rate: float | None = ...,
        heat_recovery_water_flow_rate_function_of_temperature_and_power_curve_name: str | None = ...,
        thermal_efficiency_function_of_temperature_and_elevation_curve_name: str | None = ...,
        heat_recovery_rate_function_of_part_load_ratio_curve_name: str | None = ...,
        heat_recovery_rate_function_of_inlet_water_temperature_curve_name: str | None = ...,
        heat_recovery_rate_function_of_water_flow_rate_curve_name: str | None = ...,
        minimum_heat_recovery_water_flow_rate: float | None = 0,
        maximum_heat_recovery_water_flow_rate: float | None = 0,
        maximum_heat_recovery_water_temperature: float | None = ...,
        combustion_air_inlet_node_name: str | None = ...,
        combustion_air_outlet_node_name: str | None = ...,
        reference_exhaust_air_mass_flow_rate: float | None = ...,
        exhaust_air_flow_rate_function_of_temperature_curve_name: str | None = ...,
        exhaust_air_flow_rate_function_of_part_load_ratio_curve_name: str | None = ...,
        nominal_exhaust_air_outlet_temperature: float | None = ...,
        exhaust_air_temperature_function_of_temperature_curve_name: str | None = ...,
        exhaust_air_temperature_function_of_part_load_ratio_curve_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Generator:MicroTurbine`` and add it to the document.

        MicroTurbine generators are small combustion turbines (e.g., 25kW to 500kW). The model calculates electrical power output, fuel use, standby and ancillary power. Energy recovery from exhaust air can be used to heat water.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatormicroturbine
        """

class ElectricLoadCenterInverterPVWatts:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        dc_to_ac_size_ratio: float | None = 1.1,
        inverter_efficiency: float | None = 0.96,
        validate: bool = True,
    ) -> None:
        """Create a new ``ElectricLoadCenter:Inverter:PVWatts`` and add it to the document.

        Electric power inverter to convert from direct current (DC) to alternating current (AC) in an electric load center that contains Generator:PVWatts objects. It implements the PVWatts inverter performance curves.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#electricloadcenterinverterpvwatts
        """

class ParametricFileNameSuffix:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        suffixes: Sequence[_g.ParametricFileNameSuffixSuffixesItem | _g.ParametricFileNameSuffixSuffixesGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Parametric:FileNameSuffix`` and add it to the document.

        Defines the suffixes to be appended to the idf and output file names for each parametric run. If this object is omitted, the suffix will default to the run number.

        ``suffixes`` takes the extensible groups in order, one dict per group:

        ```python
        doc["Parametric:FileNameSuffix"].add(
            "Parametric FileNameSuffix 1",
            suffixes=[
                {"suffix_for_file_name_in_run": "Suffix for File Name in Run"},
                {"suffix_for_file_name_in_run": "Suffix for File Name in Run"},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/parametric-objects/#parametricfilenamesuffix
        """

class OutputMeter:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        key_name: str,
        reporting_frequency: Literal[
            "Annual", "Daily", "Detailed", "Environment", "Hourly", "Monthly", "RunPeriod", "Timestep"
        ]
        | None = "Hourly",
        validate: bool = True,
    ) -> None:
        """Create a new ``Output:Meter`` and add it to the document.

        Each Output:Meter command picks meters to be put onto the standard output file (.eso) and meter file (.mtr). Not all meters are reported in every simulation. A list of meters that can be reported are available after a run on the meter dictionary file (.mdd) if the Output:VariableDictionary has been requested.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-output-reporting/#outputmeter
        """
