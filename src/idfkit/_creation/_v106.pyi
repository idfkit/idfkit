"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class ElectricEquipmentITEAirCooled_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        cpu_power_input_function_of_loading_and_air_temperature_curve_name: str,
        design_fan_air_flow_rate_per_power_input: float,
        air_flow_function_of_loading_and_air_temperature_curve_name: str,
        fan_power_input_function_of_flow_curve_name: str,
        air_flow_calculation_method: Literal["FlowControlWithApproachTemperatures", "FlowFromSystem"]
        | None = "FlowFromSystem",
        design_power_input_calculation_method: Literal["Watts/Area", "Watts/Unit"] | None = "Watts/Unit",
        watts_per_unit: float | None = ...,
        number_of_units: float | None = 1,
        watts_per_zone_floor_area: float | None = ...,
        design_power_input_schedule_name: str | None = ...,
        cpu_loading_schedule_name: str | None = ...,
        design_fan_power_input_fraction: float | None = 0,
        design_entering_air_temperature: float | None = 15,
        environmental_class: Literal["A1", "A2", "A3", "A4", "B", "C", "None"] | None = "None",
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
        validate: bool = True,
    ) -> None:
        """Create a new ``ElectricEquipment:ITE:AirCooled`` and add it to the document.

        This object describes air-cooled electric information technology equipment (ITE) which has variable power consumption as a function of loading and temperature.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-internal-gains-people-lights-other/#electricequipmentiteaircooled
        """

class DesignSpecificationOutdoorAir_v8_9_to_v9_4:
    def __call__(
        self,
        name: str,
        /,
        *,
        outdoor_air_method: Literal[
            "AirChanges/Hour",
            "Flow/Area",
            "Flow/Person",
            "Flow/Zone",
            "IndoorAirQualityProcedure",
            "Maximum",
            "ProportionalControlBasedOnDesignOccupancy",
            "ProportionalControlBasedonOccupancySchedule",
            "Sum",
        ]
        | None = "Flow/Person",
        outdoor_air_flow_per_person: float | None = 0.00944,
        outdoor_air_flow_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_per_zone: float | None = 0,
        outdoor_air_flow_air_changes_per_hour: float | None = 0,
        outdoor_air_schedule_name: str | None = ...,
        proportional_control_minimum_outdoor_air_flow_rate_schedule_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``DesignSpecification:OutdoorAir`` and add it to the document.

        This object is used to describe general outdoor air requirements which are referenced by other objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-design-objects/#designspecificationoutdoorair
        """

class AirLoopHVACUnitaryFurnaceHeatCool_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        furnace_air_inlet_node_name: str,
        furnace_air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        controlling_zone_or_thermostat_location: str,
        supply_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff"],
        supply_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal["Coil:Cooling:DX:SingleSpeed", "CoilSystem:Cooling:DX:HeatExchangerAssisted"],
        cooling_coil_name: str,
        availability_schedule_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        maximum_supply_air_temperature: float | Literal["Autosize"] | None = 80,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "BlowThrough",
        dehumidification_control_type: Literal["CoolReheat", "Multimode", "None"] | None = "None",
        reheat_coil_object_type: Literal[
            "Coil:Heating:Desuperheater",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
        ]
        | None = ...,
        reheat_coil_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``AirLoopHVAC:Unitary:Furnace:HeatCool`` and add it to the document.

        Unitary system, heating and cooling with constant volume supply fan (continuous or cycling), direct expansion (DX) cooling coil, heating coil (gas, electric, hot water, or steam), and optional reheat coil for dehumidification control. Identical to AirLoopHVAC:UnitaryHeatCool.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-unitary-equipment/#airloophvacunitaryfurnaceheatcool
        """

class ChillerCombustionTurbine_v8_9_to_v9_2:
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
        coefficient_1_of_fuel_input_curve: float | None = ...,
        coefficient_2_of_fuel_input_curve: float | None = ...,
        coefficient_3_of_fuel_input_curve: float | None = ...,
        coefficient_1_of_temperature_based_fuel_input_curve: float | None = ...,
        coefficient_2_of_temperature_based_fuel_input_curve: float | None = ...,
        coefficient_3_of_temperature_based_fuel_input_curve: float | None = ...,
        coefficient_1_of_exhaust_flow_curve: float | None = ...,
        coefficient_2_of_exhaust_flow_curve: float | None = ...,
        coefficient_3_of_exhaust_flow_curve: float | None = ...,
        coefficient_1_of_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_2_of_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_3_of_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_1_of_temperature_based_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_2_of_temperature_based_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_3_of_temperature_based_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_1_of_recovery_lube_heat_curve: float | None = ...,
        coefficient_2_of_recovery_lube_heat_curve: float | None = ...,
        coefficient_3_of_recovery_lube_heat_curve: float | None = ...,
        coefficient_1_of_u_factor_times_area_curve: float | None = ...,
        coefficient_2_of_u_factor_times_area_curve: float | None = ...,
        gas_turbine_engine_capacity: float | Literal["Autosize"] | None = ...,
        maximum_exhaust_flow_per_unit_of_power_output: float | None = ...,
        design_steam_saturation_temperature: float | None = ...,
        fuel_higher_heating_value: float | None = ...,
        design_heat_recovery_water_flow_rate: float | Literal["Autosize"] | None = 0,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        chiller_flow_mode: Literal["ConstantFlow", "LeavingSetpointModulated", "NotModulated"] | None = "NotModulated",
        fuel_type: Literal[
            "Diesel", "FuelOil#1", "FuelOil#2", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2", "PropaneGas"
        ]
        | None = "NaturalGas",
        heat_recovery_maximum_temperature: float | None = 80,
        sizing_factor: float | None = 1,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        condenser_heat_recovery_relative_capacity_fraction: float | None = ...,
        turbine_engine_efficiency: float | None = 0.35,
        validate: bool = True,
    ) -> None:
        """Create a new ``Chiller:CombustionTurbine`` and add it to the document.

        This chiller model is the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Chiller performance curves are generated by fitting catalog data to third order polynomial equations. Three sets of coefficients are required.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-plant-equipment/#chillercombustionturbine
        """

class ConstructionInternalSource_v9_4:
    def __call__(
        self,
        name: str,
        /,
        *,
        source_present_after_layer_number: float,
        temperature_calculation_requested_after_layer_number: float,
        dimensions_for_the_ctf_calculation: float,
        tube_spacing: float,
        outside_layer: str,
        two_dimensional_temperature_calculation_position: float | None = 0,
        layer_2: str | None = ...,
        layer_3: str | None = ...,
        layer_4: str | None = ...,
        layer_5: str | None = ...,
        layer_6: str | None = ...,
        layer_7: str | None = ...,
        layer_8: str | None = ...,
        layer_9: str | None = ...,
        layer_10: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Construction:InternalSource`` and add it to the document.

        Start with outside layer and work your way to the inside Layer Up to 10 layers total Enter the material name for each layer
        """

class HeatPumpWaterToWaterEIRHeating_v9_1_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        load_side_inlet_node_name: str,
        load_side_outlet_node_name: str,
        source_side_inlet_node_name: str,
        source_side_outlet_node_name: str,
        capacity_modifier_function_of_temperature_curve_name: str,
        electric_input_to_output_ratio_modifier_function_of_temperature_curve_name: str,
        electric_input_to_output_ratio_modifier_function_of_part_load_ratio_curve_name: str,
        companion_heat_pump_name: str | None = ...,
        load_side_reference_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        source_side_reference_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        reference_capacity: float | Literal["Autosize"] | None = "Autosize",
        reference_coefficient_of_performance: float | None = 7.5,
        sizing_factor: float | None = 1,
        validate: bool = True,
    ) -> None:
        """Create a new ``HeatPump:WaterToWater:EIR:Heating`` and add it to the document.

        An EIR formulated water to water heat pump model, heating operation
        """

class PythonPluginOutputVariable_v9_3:
    def __call__(
        self,
        name: str,
        /,
        *,
        python_plugin_variable_name: str,
        type_of_data_in_variable: Literal["Averaged", "Metered", "Summed"],
        update_frequency: Literal["SystemTimestep", "ZoneTimestep"],
        units: str | None = ...,
        resource_type: Literal[
            "Coal",
            "CondensateWaterCollected",
            "Diesel",
            "DistrictCooling",
            "DistrictHeating",
            "Electricity",
            "ElectricityProducedOnSite",
            "EnergyTransfer",
            "FuelOil#1",
            "FuelOil#2",
            "Gasoline",
            "MainsWaterSupply",
            "NaturalGas",
            "OnSiteWaterProduced",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "RainWaterCollected",
            "SolarAirHeating",
            "SolarWaterHeating",
            "Steam",
            "WaterUse",
            "WellWaterDrawn",
        ]
        | None = ...,
        group_type: Literal["Building", "HVAC", "Plant", "System"] | None = ...,
        end_use_category: Literal[
            "Baseboard",
            "Boilers",
            "Chillers",
            "Cooling",
            "CoolingCoils",
            "ExteriorEquipment",
            "ExteriorLights",
            "Fans",
            "HeatRecovery",
            "HeatRecoveryForCooling",
            "HeatRecoveryForHeating",
            "HeatRejection",
            "Heating",
            "HeatingCoils",
            "Humidifier",
            "InteriorEquipment",
            "InteriorLights",
            "OnSiteGeneration",
            "Pumps",
            "Refrigeration",
            "WaterSystems",
        ]
        | None = ...,
        end_use_subcategory: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``PythonPlugin:OutputVariable`` and add it to the document.

        This object sets up an EnergyPlus output variable from a Python Plugin variable
        """
