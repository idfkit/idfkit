"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class AnySizingPeriodWeatherFileDays:
    def __call__(
        self,
        name: str,
        /,
        *,
        begin_month: int,
        begin_day_of_month: int,
        end_month: int,
        end_day_of_month: int,
        day_of_week_for_start_day: Literal[
            "",
            "CustomDay1",
            "CustomDay2",
            "Friday",
            "Monday",
            "Saturday",
            "SummerDesignDay",
            "Sunday",
            "Thursday",
            "Tuesday",
            "Wednesday",
            "WinterDesignDay",
        ]
        | None = "Monday",
        use_weather_file_daylight_saving_period: Literal["", "No", "Yes"] | None = "Yes",
        use_weather_file_rain_and_snow_indicators: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``SizingPeriod:WeatherFileDays`` and add it to the document.

        Use a weather file period for design sizing calculations.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sizingperiodweatherfiledays
        """

class SurfacePropertySolarIncidentInside:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_name: str,
        construction_name: str,
        inside_surface_incident_sun_solar_radiation_schedule_name: str,
    ) -> None:
        """Create a new ``SurfaceProperty:SolarIncidentInside`` and add it to the document.

        Used to provide incident solar radiation on the inside of the surface. Reference surface-construction pair and if that pair is used in a simulation, then program will use value provided in schedule instead of calculating it.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertysolarincidentinside
        """

class ExteriorWaterEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        schedule_name: str,
        design_level: float,
        fuel_use_type: Literal["", "Water"] | None = "Water",
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``Exterior:WaterEquipment`` and add it to the document.

        only used for Meter type reporting, does not affect building loads

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-exterior-energy-use-equipment/#exteriorwaterequipment
        """

class ZoneHVACVentilatedSlab:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        outdoor_air_control_type: Literal["FixedAmount", "FixedTemperature", "VariablePercent"],
        minimum_outdoor_air_flow_rate: float | Literal["Autosize"],
        minimum_outdoor_air_schedule_name: str,
        maximum_outdoor_air_flow_rate: float | Literal["Autosize"],
        maximum_outdoor_air_fraction_or_temperature_schedule_name: str,
        heating_high_air_temperature_schedule_name: str,
        heating_low_air_temperature_schedule_name: str,
        heating_high_control_temperature_schedule_name: str,
        heating_low_control_temperature_schedule_name: str,
        cooling_high_air_temperature_schedule_name: str,
        cooling_low_air_temperature_schedule_name: str,
        cooling_high_control_temperature_schedule_name: str,
        cooling_low_control_temperature_schedule_name: str,
        return_air_node_name: str,
        slab_in_node_name: str,
        outdoor_air_node_name: str,
        relief_air_node_name: str,
        outdoor_air_mixer_outlet_node_name: str,
        fan_outlet_node_name: str,
        fan_name: str,
        coil_option_type: Literal["Cooling", "Heating", "HeatingAndCooling", "None"],
        availability_schedule_name: str | None = ...,
        surface_name_or_radiant_surface_group_name: str | None = ...,
        system_configuration_type: Literal["", "SeriesSlabs", "SlabAndZone", "SlabOnly"] | None = "SlabOnly",
        hollow_core_inside_diameter: float | None = 0.05,
        hollow_core_length: float | None = ...,
        number_of_cores: float | None = ...,
        temperature_control_type: Literal[
            "",
            "MeanAirTemperature",
            "MeanRadiantTemperature",
            "OperativeTemperature",
            "OutdoorDryBulbTemperature",
            "OutdoorWetBulbTemperature",
            "SurfaceTemperature",
            "ZoneAirDewPointTemperature",
        ]
        | None = "OutdoorDryBulbTemperature",
        zone_supply_air_node_name: str | None = ...,
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ]
        | None = ...,
        heating_coil_name: str | None = ...,
        hot_water_or_steam_inlet_node_name: str | None = ...,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "CoilSystem:Cooling:Water:HeatExchangerAssisted",
        ]
        | None = ...,
        cooling_coil_name: str | None = ...,
        cold_water_inlet_node_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:VentilatedSlab`` and add it to the document.

        Ventilated slab system where outdoor air flows through hollow cores in a building surface (wall, ceiling, or floor).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvacventilatedslab
        """

class CoilCoolingWaterToAirHeatPumpEquationFit:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        rated_air_flow_rate: float | Literal["Autosize"],
        rated_water_flow_rate: float | Literal["Autosize"],
        gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        gross_rated_sensible_cooling_capacity: float | Literal["Autosize"],
        gross_rated_cooling_cop: float,
        total_cooling_capacity_curve_name: str,
        sensible_cooling_capacity_curve_name: str,
        cooling_power_consumption_curve_name: str,
        part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        rated_entering_water_temperature: float | None = 30,
        rated_entering_air_dry_bulb_temperature: float | None = 27,
        rated_entering_air_wet_bulb_temperature: float | None = 19,
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        maximum_cycling_rate: float | None = 0,
        latent_capacity_time_constant: float | None = 0,
        fan_delay_time: float | None = 60,
    ) -> None:
        """Create a new ``Coil:Cooling:WaterToAirHeatPump:EquationFit`` and add it to the document.

        Direct expansion (DX) cooling coil for water-to-air heat pump (includes electric compressor), single-speed, equation-fit model. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Equation-fit model uses normalized curves to describe the heat pump performance.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwatertoairheatpumpequationfit
        """

class AirLoopHVACUnitaryHeatPumpAirToAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        controlling_zone_or_thermostat_location: str,
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:DX:SingleSpeed", "Coil:Heating:DX:VariableSpeed", "CoilSystem:IntegratedHeatPump:AirSource"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
            "CoilSystem:IntegratedHeatPump:AirSource",
        ],
        cooling_coil_name: str,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        supplemental_heating_coil_name: str,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        dehumidification_control_type: Literal["", "CoolReheat", "Multimode", "None"] | None = "None",
        dx_heating_coil_sizing_ratio: float | None = 1,
    ) -> None:
        """Create a new ``AirLoopHVAC:UnitaryHeatPump:AirToAir`` and add it to the document.

        Unitary heat pump system, heating and cooling, single-speed with supply fan, direct expansion (DX) cooling coil, DX heating coil (air-to-air heat pump), and supplemental heating coil (gas, electric, hot water, or steam).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#airloophvacunitaryheatpumpairtoair
        """

class SolarCollectorPerformancePhotovoltaicThermalBIPVT:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        boundary_conditions_model_name: str,
        effective_plenum_gap_thickness_behind_pv_modules: float,
        availability_schedule_name: str | None = ...,
        pv_cell_normal_transmittance_absorptance_product: float | None = 0.957,
        backing_material_normal_transmittance_absorptance_product: float | None = 0.87,
        cladding_normal_transmittance_absorptance_product: float | None = 0.85,
        fraction_of_collector_gross_area_covered_by_pv_module: float | None = 0.85,
        fraction_of_pv_cell_area_to_pv_module_area: float | None = 0.9,
        pv_module_top_thermal_resistance: float | None = 0.0044,
        pv_module_bottom_thermal_resistance: float | None = 0.0039,
        pv_module_front_longwave_emissivity: float | None = 0.85,
        pv_module_back_longwave_emissivity: float | None = 0.9,
        glass_thickness: float | None = 0.002,
        glass_refraction_index: float | None = 1.526,
        glass_extinction_coefficient: float | None = 4,
    ) -> None:
        """Create a new ``SolarCollectorPerformance:PhotovoltaicThermal:BIPVT`` and add it to the document.

        Thermal performance parameters for Building-Integrated Photovoltaic-Thermal (BIPVT) solar collector.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-solar-collectors/#solarcollectorperformancephotovoltaicthermalbipvt
        """

class CoolingTowerVariableSpeed:
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
        evaporation_loss_mode: Literal["", "LossFactor", "SaturatedExit"] | None = "SaturatedExit",
        evaporation_loss_factor: float | None = 0.2,
        drift_loss_percent: float | None = 0.008,
        blowdown_calculation_mode: Literal["", "ConcentrationRatio", "ScheduledRate"] | None = "ConcentrationRatio",
        blowdown_concentration_ratio: float | None = 3,
        blowdown_makeup_water_usage_schedule_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        outdoor_air_inlet_node_name: str | None = ...,
        number_of_cells: int | None = 1,
        cell_control: Literal["", "MaximalCell", "MinimalCell"] | None = "MaximalCell",
        cell_minimum_water_flow_rate_fraction: float | None = 0.33,
        cell_maximum_water_flow_rate_fraction: float | None = 2.5,
        sizing_factor: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``CoolingTower:VariableSpeed`` and add it to the document.

        This open wet tower model is based on purely empirical algorithms derived from manufacturer's performance data or field measurements. The user can select from two existing algorithms (CoolTools or YorkCalc), or they can enter their own correlation for approach temperature by using a variable speed tower model coefficient object. For a multi-cell tower, the capacity and air/water flow rate inputs are for the entire tower.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#coolingtowervariablespeed
        """

class RefrigerationCondenserCascade:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_condensing_temperature: float,
        rated_effective_total_heat_rejection_rate: float,
        rated_approach_temperature_difference: float | None = 3,
        condensing_temperature_control_type: Literal["", "Fixed", "Float"] | None = "Fixed",
        condenser_refrigerant_operating_charge_inventory: float | None = ...,
        condensate_receiver_refrigerant_inventory: float | None = ...,
        condensate_piping_refrigerant_inventory: float | None = ...,
    ) -> None:
        """Create a new ``Refrigeration:Condenser:Cascade`` and add it to the document.

        Cascade condenser for a refrigeration system (Refrigeration:System). The cascade condenser is unlike the other condenser options because it rejects heat to another, higher-temperature, refrigeration system. That is, the cascade condenser acts as a heat rejection object for one system, but acts as a refrigeration load for another system.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationcondensercascade
        """

class FaultModelHumidistatOffset:
    def __call__(
        self,
        name: str,
        /,
        *,
        humidistat_name: str,
        humidistat_offset_type: Literal["", "ThermostatOffsetDependent", "ThermostatOffsetIndependent"]
        | None = "ThermostatOffsetIndependent",
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        reference_humidistat_offset: float | None = 5,
        related_thermostat_offset_fault_name: str | None = ...,
    ) -> None:
        """Create a new ``FaultModel:HumidistatOffset`` and add it to the document.

        This object describes fault of humidistat offset

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-operational-faults/#faultmodelhumidistatoffset
        """

class AnyPythonPluginOutputVariable:
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
            "Electricity",
            "ElectricityProducedOnSite",
            "EnergyTransfer",
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
    ) -> None:
        """Create a new ``PythonPlugin:OutputVariable`` and add it to the document.

        This object sets up an EnergyPlus output variable from a Python Plugin variable

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-python-plugin-system/#pythonpluginoutputvariable
        """

class PythonPluginOutputVariable:
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
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "ElectricityProducedOnSite",
            "EnergyTransfer",
            "FuelOilNo1",
            "FuelOilNo2",
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
    ) -> None:
        """Create a new ``PythonPlugin:OutputVariable`` and add it to the document.

        This object sets up an EnergyPlus output variable from a Python Plugin variable

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-python-plugin-system/#pythonpluginoutputvariable
        """
