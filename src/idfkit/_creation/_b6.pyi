"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class WindowMaterialGlazingGroupThermochromic:
    def __call__(
        self,
        name: str,
        /,
        *,
        temperature_data: Sequence[
            _g.WindowMaterialGlazingGroupThermochromicTemperatureDataItem
            | _g.WindowMaterialGlazingGroupThermochromicTemperatureDataGroup
        ] = ...,
    ) -> None:
        """Create a new ``WindowMaterial:GlazingGroup:Thermochromic`` and add it to the document.

        thermochromic glass at different temperatures

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialglazinggroupthermochromic
        """

class ConstructionCfactorUndergroundWall:
    def __call__(self, name: str, /, *, c_factor: float, height: float) -> None:
        """Create a new ``Construction:CfactorUndergroundWall`` and add it to the document.

        Alternate method of describing underground wall constructions

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#constructioncfactorundergroundwall
        """

class SurfaceControlMovableInsulation:
    def __call__(
        self,
        /,
        *,
        insulation_type: Literal["Inside", "Outside"],
        surface_name: str,
        material_name: str,
        schedule_name: str,
    ) -> None:
        """Create a new ``SurfaceControl:MovableInsulation`` and add it to the document.

        Exterior or Interior Insulation on opaque surfaces

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacecontrolmovableinsulation
        """

class ComfortViewFactorAngles:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        angles: Sequence[_g.ComfortViewFactorAnglesAnglesItem | _g.ComfortViewFactorAnglesAnglesGroup] = ...,
    ) -> None:
        """Create a new ``ComfortViewFactorAngles`` and add it to the document.

        Used to specify radiant view factors for thermal comfort calculations. Note that the following angle factor fractions must sum up to 1.0 All surfaces must be in the same enclosure.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#comfortviewfactorangles
        """

class ElectricEquipmentITEAirCooled:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_space_name: str,
        cpu_power_input_function_of_loading_and_air_temperature_curve_name: str,
        design_fan_air_flow_rate_per_power_input: float,
        air_flow_function_of_loading_and_air_temperature_curve_name: str,
        fan_power_input_function_of_flow_curve_name: str,
        air_flow_calculation_method: Literal["FlowControlWithApproachTemperatures", "FlowFromSystem"]
        | None = "FlowFromSystem",
        design_power_input_calculation_method: Literal["Watts/Area", "Watts/Unit"] | None = "Watts/Unit",
        watts_per_unit: float | None = ...,
        number_of_units: float | None = 1,
        watts_per_floor_area: float | None = ...,
        design_power_input_schedule_name: str | None = ...,
        cpu_loading_schedule_name: str | None = ...,
        design_fan_power_input_fraction: float | None = 0,
        design_entering_air_temperature: float | None = 15,
        environmental_class: Literal["A1", "A2", "A3", "A4", "B", "C", "H1", "None"] | None = "None",
        air_inlet_connection_type: Literal["AdjustedSupply", "RoomAirModel", "ZoneAirNode"] | None = "AdjustedSupply",
        air_inlet_room_air_model_node_name: str | None = ...,
        air_outlet_room_air_model_node_name: str | None = ...,
        supply_air_node_name: str | None = ...,
        design_recirculation_fraction: float | None = 0,
        recirculation_function_of_loading_and_supply_temperature_curve_name: str | None = ...,
        design_electric_power_supply_efficiency: float | None = 1,
        electric_power_supply_efficiency_function_of_part_load_ratio_curve_name: str | None = ...,
        fraction_of_electric_power_supply_losses_to_zone: float | None = 1,
        cpu_end_use_subcategory: str | None = "ITE-CPU",
        fan_end_use_subcategory: str | None = "ITE-Fans",
        electric_power_supply_end_use_subcategory: str | None = "ITE-UPS",
        supply_temperature_difference: float | None = ...,
        supply_temperature_difference_schedule: str | None = ...,
        return_temperature_difference: float | None = ...,
        return_temperature_difference_schedule: str | None = ...,
    ) -> None:
        """Create a new ``ElectricEquipment:ITE:AirCooled`` and add it to the document.

        This object describes air-cooled electric information technology equipment (ITE) which has variable power consumption as a function of loading and temperature. If a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#electricequipmentiteaircooled
        """

class ZoneControlThermostat:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_name: str,
        control_type_schedule_name: str,
        control_1_object_type: Literal[
            "ThermostatSetpoint:DualSetpoint",
            "ThermostatSetpoint:SingleCooling",
            "ThermostatSetpoint:SingleHeating",
            "ThermostatSetpoint:SingleHeatingOrCooling",
        ],
        control_1_name: str,
        control_2_object_type: Literal[
            "ThermostatSetpoint:DualSetpoint",
            "ThermostatSetpoint:SingleCooling",
            "ThermostatSetpoint:SingleHeating",
            "ThermostatSetpoint:SingleHeatingOrCooling",
        ]
        | None = ...,
        control_2_name: str | None = ...,
        control_3_object_type: Literal[
            "ThermostatSetpoint:DualSetpoint",
            "ThermostatSetpoint:SingleCooling",
            "ThermostatSetpoint:SingleHeating",
            "ThermostatSetpoint:SingleHeatingOrCooling",
        ]
        | None = ...,
        control_3_name: str | None = ...,
        control_4_object_type: Literal[
            "ThermostatSetpoint:DualSetpoint",
            "ThermostatSetpoint:SingleCooling",
            "ThermostatSetpoint:SingleHeating",
            "ThermostatSetpoint:SingleHeatingOrCooling",
        ]
        | None = ...,
        control_4_name: str | None = ...,
        temperature_difference_between_cutout_and_setpoint: float | None = 0,
    ) -> None:
        """Create a new ``ZoneControl:Thermostat`` and add it to the document.

        Define the Thermostat settings for a zone or list of zones. If you use a ZoneList in the Zone or ZoneList name field then this definition applies to all the zones in the ZoneList.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-controls-thermostats/#zonecontrolthermostat
        """

class ThermostatSetpointSingleHeatingOrCooling:
    def __call__(self, name: str, /, *, setpoint_temperature_schedule_name: str | None = ...) -> None:
        """Create a new ``ThermostatSetpoint:SingleHeatingOrCooling`` and add it to the document.

        Used for a heating and cooling thermostat with a single setpoint. The setpoint can be scheduled and varied throughout the simulation for both heating and cooling.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-controls-thermostats/#thermostatsetpointsingleheatingorcooling
        """

class AnyZoneHVACTerminalUnitVariableRefrigerantFlow:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        terminal_unit_air_inlet_node_name: str,
        terminal_unit_air_outlet_node_name: str,
        supply_air_fan_operating_mode_schedule_name: str,
        supply_air_fan_object_name: str,
        terminal_unit_availability_schedule: str | None = ...,
        cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_heating_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        cooling_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        supply_air_fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel"]
        | None = "Fan:ConstantVolume",
        outside_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outside_air_mixer_object_name: str | None = ...,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:VariableRefrigerantFlow", "Coil:Cooling:DX:VariableRefrigerantFlow:FluidTemperatureControl"
        ]
        | None = ...,
        cooling_coil_object_name: str | None = ...,
        heating_coil_object_type: Literal[
            "Coil:Heating:DX:VariableRefrigerantFlow", "Coil:Heating:DX:VariableRefrigerantFlow:FluidTemperatureControl"
        ]
        | None = ...,
        heating_coil_object_name: str | None = ...,
        zone_terminal_unit_on_parasitic_electric_energy_use: float | None = 0,
        zone_terminal_unit_off_parasitic_electric_energy_use: float | None = 0,
        rated_heating_capacity_sizing_ratio: float | None = 1,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:TerminalUnit:VariableRefrigerantFlow`` and add it to the document.

        A terminal unit with variable refrigerant flow (VRF) DX cooling and heating coils (air-to-air heat pump). The VRF terminal units are served by an AirConditioner:VariableRefrigerantFlow or AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl:* system. Terminal units can be configured as zone, air loop or outside air system equipment.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacterminalunitvariablerefrigerantflow
        """

class AirTerminalSingleDuctVAVHeatAndCoolReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        damper_air_outlet_node_name: str,
        air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        zone_minimum_air_flow_fraction: float,
        reheat_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        reheat_coil_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        convergence_tolerance: float | None = 0.001,
        maximum_reheat_air_temperature: float | None = ...,
        minimum_air_flow_turndown_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:VAV:HeatAndCool:Reheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume for both cooling and heating, with reheat coil (hot water, electric, gas, or steam).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-hvac-air-loop-terminal-units/#airterminalsingleductvavheatandcoolreheat
        """

class AnyCoilHeatingElectricMultiStage:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        number_of_stages: int,
        stage_1_efficiency: float,
        stage_1_nominal_capacity: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        temperature_setpoint_node_name: str | None = ...,
        stage_2_efficiency: float | None = ...,
        stage_2_nominal_capacity: float | Literal["Autosize"] | None = ...,
        stage_3_efficiency: float | None = ...,
        stage_3_nominal_capacity: float | Literal["Autosize"] | None = ...,
        stage_4_efficiency: float | None = ...,
        stage_4_nominal_capacity: float | Literal["Autosize"] | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:Electric:MultiStage`` and add it to the document.

        Electric heating coil, multi-stage. If the coil is located directly in an air loop branch or outdoor air equipment list, then it is controlled on leaving air temperature and the Temperature Setpoint Node Name must be specified. If the coil is contained within another component such as an air terminal unit, zone HVAC equipment, or unitary system, then the coil is controlled by the parent component and the setpoint node name is not entered.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilheatingelectricmultistage
        """

class AnyCoilCoolingWaterToAirHeatPumpEquationFit:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        rated_air_flow_rate: float | Literal["Autosize"],
        rated_water_flow_rate: float | Literal["Autosize"],
        gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        gross_rated_sensible_cooling_capacity: float | Literal["Autosize"],
        gross_rated_cooling_cop: float,
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
    ) -> None:
        """Create a new ``Coil:Cooling:WaterToAirHeatPump:EquationFit`` and add it to the document.

        Direct expansion (DX) cooling coil for water-to-air heat pump (includes electric compressor), single-speed, equation-fit model. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Equation-fit model uses normalized curves to describe the heat pump performance.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwatertoairheatpumpequationfit
        """

class CoilWaterHeatingDesuperheater:
    def __call__(
        self,
        name: str,
        /,
        *,
        setpoint_temperature_schedule_name: str,
        rated_inlet_water_temperature: float,
        rated_outdoor_air_temperature: float,
        maximum_inlet_water_temperature_for_heat_reclaim: float,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        tank_name: str,
        heating_source_object_type: Literal[
            "Coil:Cooling:DX",
            "Coil:Cooling:DX:MultiSpeed",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:TwoSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
            "Coil:Cooling:WaterToAirHeatPump:EquationFit",
            "Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit",
            "Refrigeration:CompressorRack",
            "Refrigeration:Condenser:AirCooled",
            "Refrigeration:Condenser:EvaporativeCooled",
            "Refrigeration:Condenser:WaterCooled",
        ],
        heating_source_name: str,
        water_flow_rate: float,
        availability_schedule_name: str | None = ...,
        dead_band_temperature_difference: float | None = 5,
        rated_heat_reclaim_recovery_efficiency: float | None = ...,
        heat_reclaim_efficiency_function_of_temperature_curve_name: str | None = ...,
        tank_object_type: Literal["WaterHeater:Mixed", "WaterHeater:Stratified"] | None = "WaterHeater:Mixed",
        water_pump_power: float | None = 0,
        fraction_of_pump_heat_to_water: float | None = 0.2,
        on_cycle_parasitic_electric_load: float | None = 0,
        off_cycle_parasitic_electric_load: float | None = 0,
    ) -> None:
        """Create a new ``Coil:WaterHeating:Desuperheater`` and add it to the document.

        Desuperheater air heating coil. The heating energy provided by this coil is reclaimed from the superheated refrigerant gas leaving a compressor and does not impact the performance of the compressor. This coil must be used with a water heater tank, see Water Heater:Mixed.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilwaterheatingdesuperheater
        """

class AnyExternalInterfaceFunctionalMockupUnitImport:
    def __call__(self, /, *, fmu_file_name: str, fmu_timeout: float | None = 0, fmu_loggingon: int | None = 0) -> None:
        """Create a new ``ExternalInterface:FunctionalMockupUnitImport`` and add it to the document.

        This object declares an FMU

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-externalinterface/#externalinterfacefunctionalmockupunitimport
        """

class FaultModelEnthalpySensorOffsetReturnAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        controller_object_type: Literal["Controller:OutdoorAir"],
        controller_object_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        enthalpy_sensor_offset: float | None = 0,
    ) -> None:
        """Create a new ``FaultModel:EnthalpySensorOffset:ReturnAir`` and add it to the document.

        This object describes return air enthalpy sensor offset

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-operational-faults/#faultmodelenthalpysensoroffsetreturnair
        """

class FaultModelFoulingCoolingTower:
    def __call__(
        self,
        name: str,
        /,
        *,
        cooling_tower_object_type: Literal[
            "CoolingTower:SingleSpeed", "CoolingTower:TwoSpeed", "CoolingTower:VariableSpeed:MERKEL"
        ],
        cooling_tower_object_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        reference_ua_reduction_factor: float | None = ...,
    ) -> None:
        """Create a new ``FaultModel:Fouling:CoolingTower`` and add it to the document.

        This object describes the fault of fouling cooling towers

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-operational-faults/#faultmodelfoulingcoolingtower
        """

class FuelFactors:
    def __call__(
        self,
        /,
        *,
        existing_fuel_resource_name: Literal[
            "Coal",
            "Diesel",
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
        source_energy_factor: float | None = ...,
        source_energy_schedule_name: str | None = ...,
        co2_emission_factor: float | None = ...,
        co2_emission_factor_schedule_name: str | None = ...,
        co_emission_factor: float | None = ...,
        co_emission_factor_schedule_name: str | None = ...,
        ch4_emission_factor: float | None = ...,
        ch4_emission_factor_schedule_name: str | None = ...,
        nox_emission_factor: float | None = ...,
        nox_emission_factor_schedule_name: str | None = ...,
        n2o_emission_factor: float | None = ...,
        n2o_emission_factor_schedule_name: str | None = ...,
        so2_emission_factor: float | None = ...,
        so2_emission_factor_schedule_name: str | None = ...,
        pm_emission_factor: float | None = ...,
        pm_emission_factor_schedule_name: str | None = ...,
        pm10_emission_factor: float | None = ...,
        pm10_emission_factor_schedule_name: str | None = ...,
        pm2_5_emission_factor: float | None = ...,
        pm2_5_emission_factor_schedule_name: str | None = ...,
        nh3_emission_factor: float | None = ...,
        nh3_emission_factor_schedule_name: str | None = ...,
        nmvoc_emission_factor: float | None = ...,
        nmvoc_emission_factor_schedule_name: str | None = ...,
        hg_emission_factor: float | None = ...,
        hg_emission_factor_schedule_name: str | None = ...,
        pb_emission_factor: float | None = ...,
        pb_emission_factor_schedule_name: str | None = ...,
        water_emission_factor: float | None = ...,
        water_emission_factor_schedule_name: str | None = ...,
        nuclear_high_level_emission_factor: float | None = ...,
        nuclear_high_level_emission_factor_schedule_name: str | None = ...,
        nuclear_low_level_emission_factor: float | None = ...,
        nuclear_low_level_emission_factor_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``FuelFactors`` and add it to the document.

        Provides Fuel Factors for Emissions as well as Source=>Site conversions. OtherFuel1, OtherFuel2 provide options for users who want to create and use fuels that may not be mainstream (biomass, wood, pellets).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#fuelfactors
        """
